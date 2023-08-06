import os,sys
import random
import pandas as pd
import numpy as np
from pathlib import Path
import time
from multiprocessing import shared_memory
import gzip,io,shutil,hashlib,threading
from datetime import datetime
from numba import njit

from SharedData.Logger import Logger
from SharedData.SharedDataAWSS3 import S3Upload,S3Download,UpdateModTime

class SharedDataTable:

    def __init__(self, sharedDataFeeder, dataset, records=None,\
                 names=None,formats=None,size=None):
        self.sharedDataFeeder = sharedDataFeeder
        self.sharedData = self.sharedDataFeeder.sharedData
        self.feeder = self.sharedDataFeeder.feeder
        self.dataset = dataset
        
        self.init_pkey()

        self.create_map = 'na'
        self.init_time = time.time()
        self.download_time = pd.NaT
                        
        # file partitioning threshold
        self.maxtailbytes = int(100*10**6)
        self.minheadbytes = self.maxtailbytes
        # head header
        self.hdrnames = ['headersize','headerdescr','semaphore','md5hash','mtime','itemsize','recordssize','count',\
                         'headsize','pkeysize','minchgid','hastail','descr']
        self.hdrformats = ['<i8','|S250','<u1','|S16','<f8','<i8','<i8','<i8',\
                         '<i8','<i8','<i8','<u1','|S400']
        self.hdrdtype = np.dtype({'names':self.hdrnames,'formats':self.hdrformats})
        self.hdr = np.recarray(shape=(1,), dtype=self.hdrdtype)[0]
        self.hdr['headsize']=0 #initialize headers
        # tail header
        self.tailhdrnames = ['headersize','headerdescr','md5hash','mtime','tailsize']
        self.tailhdrformats = ['<i8','|S80','|S16','<f8','<i8']        
        self.tailhdrdtype = np.dtype({'names':self.tailhdrnames,'formats':self.tailhdrformats})
        self.tailhdr = np.recarray(shape=(1,), dtype=self.tailhdrdtype)[0]
        self.tailhdr['tailsize']=0 #initialize headers
        self.tailhdr['headersize'] = 80
        _headerdescr = ','.join(self.tailhdrnames) +';'+','.join(self.tailhdrformats)
        _headerdescr_b = str.encode(_headerdescr,encoding='UTF-8',errors='ignore')
        self.tailhdr['headerdescr'] = _headerdescr_b
        # primary key hash table
        self.pkey = np.ndarray([])
        self.pkey_initialized = False
        # records
        self.recnames = []
        self.recformats = []
        self.recdtype = None
        self.records = np.ndarray([]) 
        # shared memory
        self.shm = None
        # initalize
        if not names is None:
            self.create(names,formats,size)
        elif records is None: #Read dataset tag
            self.malloc()
        else:
            if isinstance(records,pd.DataFrame):
                records = self.df2records(records)
            self.malloc(records=records)

        self.init_time = time.time() - self.init_time

    def init_pkey(self):

        self.create_pkey_func = None
        self.upsert_func = None
        self.get_loc_func = None
        self.sort_index_func = None

        self.pkeycolumns = SharedDataTableKeys.get_pkeycolumns(self.sharedData.database)

        create_pkey_fname = 'create_pkey_'+str.lower(self.sharedData.database) + '_jit'
        if hasattr(SharedDataTableKeys,create_pkey_fname):
            self.create_pkey_func = getattr(SharedDataTableKeys,create_pkey_fname)
        else:
            raise Exception('create_pkey function not found for database %s!' \
                % (self.sharedData.database))

        upsert_fname = 'upsert_'+str.lower(self.sharedData.database) + '_jit'
        if hasattr(SharedDataTableKeys,upsert_fname):
            self.upsert_func = getattr(SharedDataTableKeys,upsert_fname)
        else:
            raise Exception('upsert function not found for database %s!' \
                % (self.sharedData.database))

        get_loc_fname = 'get_loc_'+str.lower(self.sharedData.database) + '_jit'
        if hasattr(SharedDataTableKeys,get_loc_fname):
            self.get_loc_func = getattr(SharedDataTableKeys,upsert_fname)
        else:
            raise Exception('get_loc function not found for database %s!' \
                % (self.sharedData.database))
            
    def create(self, names, formats, size):
        path, shm_name = self.get_path(iswrite=True)
        check_pkey = True
        npkeys = len(self.pkeycolumns)
        for k in range(npkeys):
            check_pkey = (check_pkey) & (names[k]==self.pkeycolumns[k])
        if not check_pkey:
            raise Exception('First columns must be %s!' % (self.pkeycolumns))
        else:
            if not 'mtime' in names:
                names.insert(npkeys,'mtime')
                formats.insert(npkeys,'<M8[ns]')
                
            # malloc recarray
            self.recnames = names
            self.rectypes = formats     
            self.recdtype = np.dtype({'names':self.recnames,'formats':self.rectypes})
            pkey_str = ','.join(self.pkeycolumns)
            descr_str = ','.join(self.recnames)+';'+','.join(self.rectypes)+';'+pkey_str
            descr_str_b = str.encode(descr_str,encoding='UTF-8',errors='ignore')
            len_descr = len(descr_str_b)
            
            # build header
            self.hdrnames = ['headersize','headerdescr','semaphore','md5hash','mtime','itemsize','recordssize','count',\
                    'headsize','pkeysize','minchgid','hastail','descr']
            self.hdrformats = ['<i8','|S250','<u1','|S16','<f8','<i8','<i8','<i8',\
                            '<i8','<i8','<i8','<u1','|S'+str(len_descr)]
            hdrnames = ','.join(self.hdrnames)
            hdrdtypes = ','.join(self.hdrformats)
            hdrdescr_str = hdrnames+';'+hdrdtypes
            hdrdescr_str_b = str.encode(hdrdescr_str,encoding='UTF-8',errors='ignore')
                            
            self.hdrdtype = np.dtype({'names':self.hdrnames,'formats':self.hdrformats})
            self.hdr = np.recarray(shape=(1,), dtype=self.hdrdtype)[0]
            self.hdr['headersize']=250
            self.hdr['headerdescr']=hdrdescr_str_b
            self.hdr['mtime'] = datetime.now().timestamp()
            self.hdr['count'] = 0
            self.hdr['minchgid'] = self.hdr['count']
            self.hdr['itemsize'] = int(self.recdtype.itemsize)
            self.hdr['recordssize'] = int(size)
            self.hdr['headsize']=0
            self.hdr['pkeysize']=int(5*size) # around 10% collisions
            self.hdr['descr'] = descr_str_b

            # create memory space                
            self.malloc_create(shm_name)

    def malloc_create(self,shm_name):
        nb_hdr = self.hdrdtype.itemsize # number of header bytes        
        nb_pkey = int(self.hdr['pkeysize']*4) # number of primary key bytes
        nb_records = int(self.hdr['recordssize']*self.hdr['itemsize']) #number of data bytes
        total_size = int(nb_hdr+nb_pkey+nb_records)

        if os.name=='posix':
            try:
                shm = shared_memory.SharedMemory(\
                    name = shm_name,create=False)
                # Release the shared memory
                shm.close()
                shm.unlink()
            except:
                pass

        self.shm = shared_memory.SharedMemory(\
            name=shm_name,create=True,size=total_size)
        
        self.shm.buf[0:nb_hdr] = self.hdr.tobytes()
        self.hdr = np.ndarray((1,),dtype=self.hdrdtype,buffer=self.shm.buf)[0]

        self.pkey = np.ndarray((self.hdr['pkeysize'],),\
            dtype=np.int32,buffer=self.shm.buf,offset=nb_hdr)
        self.pkey[:] = -1

        descr = self.hdr['descr'].decode(encoding='UTF-8',errors='ignore')
        self.recnames = descr.split(';')[0].split(',')
        self.recformats = descr.split(';')[1].split(',')
        self.recdtype = np.dtype({'names':self.recnames,'formats':self.recformats})
        self.records = SharedNumpy((self.hdr['recordssize'],),\
            dtype=self.recdtype,buffer=self.shm.buf, offset=nb_hdr+nb_pkey)
        self.records.master = self        
        
    def malloc(self,records=None, mtime=None):
        tini=time.time()
        
        path, shm_name = self.get_path(iswrite=True)
        # test if shared memory already exists        
        try:
            self.shm = shared_memory.SharedMemory(\
                name = shm_name,create=False)
            self.create_map = 'map'
        except:
            self.create_map = 'create'

        if records is None:
            if self.create_map == 'map':
                self.malloc_map(shm_name)
                return True
            else:
                tini = time.time()
                self.read(path,shm_name)
                te = time.time()-tini+0.000001
                datasize = self.hdr['count']*self.hdr['itemsize']/1000000
                Logger.log.debug('read %s/%s %.2fMB in %.2fs %.2fMBps ' % \
                    (self.feeder,self.dataset,datasize,te,datasize/te))
                return True
        else:            
            if self.create_map == 'map':
                self.malloc_map(shm_name)
            else:
                descr = records.__array_interface__['descr']
                names = [item[0] for item in descr]
                formats = [item[1] for item in descr]
                size = records.size*1.1
                self.create(names,formats,size)                
                self.records.insert(records)
                #self.hdr['minchgid'] = self.records.count

            return True        

    def malloc_map(self, shm_name):
        # Open the shared memory
        self.shm = shared_memory.SharedMemory(name=shm_name, create=False)
        
        # Read the header
        nbhdrdescr = int.from_bytes(self.shm.buf[0:8],byteorder='little')
        hdrdescr_b = self.shm.buf[8:8+nbhdrdescr].tobytes()
        hdrdescr = hdrdescr_b.decode(encoding='UTF-8',errors='ignore')
        hdrdescr = hdrdescr.replace('\x00','')
        self.hdrnames = hdrdescr.split(';')[0].split(',')
        self.hdrformats = hdrdescr.split(';')[1].split(',')
        self.hdrdtype = np.dtype({'names':self.hdrnames,'formats':self.hdrformats})
        nb_hdr = self.hdrdtype.itemsize
        self.hdr = np.ndarray((1,),dtype=self.hdrdtype,buffer=self.shm.buf)[0]

        nb_pkey = int(self.hdr['pkeysize']*4) # number of primary key bytes
        self.pkey = np.ndarray((self.hdr['pkeysize'],),\
            dtype=np.int32,buffer=self.shm.buf,offset=nb_hdr)
        self.pkey_initialized = (self.pkey!=-1).any()
                
        descr = self.hdr['descr'].decode(encoding='UTF-8',errors='ignore')
        self.recnames = descr.split(';')[0].split(',')
        self.recformats = descr.split(';')[1].split(',')
        self.recdtype = np.dtype({'names':self.recnames,'formats':self.recformats})
        self.records = SharedNumpy((self.hdr['recordssize'],),\
            dtype=self.recdtype,buffer=self.shm.buf, offset=nb_hdr+nb_pkey)
        self.records.master = self
            
    def records2df(self,records):                
        df = pd.DataFrame(records, copy=False)
        dtypes = df.dtypes.reset_index()
        dtypes.columns = ['tag','dtype']
        # convert object to string
        string_idx = ['|S' in str(dt) for dt in dtypes['dtype']]
        string_idx = (string_idx) | (dtypes['dtype']=='object')
        tags_obj =  dtypes['tag'][string_idx].values
        for tag in tags_obj:
            try:
                df[tag] = df[tag].str.decode(encoding='utf-8',errors='ignore')
            except:
                pass
        df = df.set_index(self.pkeycolumns)
        return df

    def df2records(self,df):
        check_pkey = True
        if len(self.pkeycolumns) == len(df.index.names):
            for k in range(len(self.pkeycolumns)):
                check_pkey = (check_pkey) & (df.index.names[k]==self.pkeycolumns[k])
        else:
            check_pkey = False
        if not check_pkey:
            raise Exception('First columns must be %s!' % (self.pkeycolumns))
        else:
            if self.recdtype is None:
                df = df.reset_index()
                dtypes = df.dtypes.reset_index()
                dtypes.columns = ['tag','dtype']
                # convert object to string
                tags_obj =  dtypes['tag'][dtypes['dtype']=='object'].values
                for tag in tags_obj:
                    try:
                        df[tag] = df[tag].str.encode(encoding='utf-8',errors='ignore')
                    except:
                        Logger.log.error('Could not convert %s!' % (tag))                        
                    df[tag] = df[tag].astype('|S')        
                return np.ascontiguousarray(df.to_records(index=False))
            else:
                df = df.reset_index()
                dtypes = self.recdtype
                rec = np.full((df.shape[0],),fill_value=np.nan,dtype=dtypes)
                for col in dtypes.names:
                    try:  
                        if col in df.columns:
                            rec[col] = df[col].astype(dtypes[col])
                    except:
                        Logger.log.error('Could not convert %s!' % (col))                                               
                
                return rec
        
    def get_path(self, iswrite=False):
        shm_name = self.sharedData.user + '/' + self.sharedData.database + '/' \
            + self.sharedDataFeeder.feeder + '/' + self.dataset 
        if os.name=='posix':
            shm_name = shm_name.replace('/','\\')
        
        path = Path(os.environ['DATABASE_FOLDER'])
        path = path / self.sharedData.user
        path = path / self.sharedData.database
        path = path / self.sharedDataFeeder.feeder
        path = path / self.dataset        
        path = Path(str(path).replace('\\','/'))
        if self.sharedData.save_local:
            if not os.path.isdir(path):
                os.makedirs(path)
        
        return path, shm_name
    
    def read(self, path, shm_name):
        head_io = None
        head_io_remote_isnewer = False
        tail_io = None
        tail_io_remote_isnewer = False
        headpath = path / 'head.bin'
        tailpath = path / 'tail.bin'

        # open head_io to read header
        # download remote head if its newer than local
        if self.sharedData.s3read:
            force_download= (not self.sharedData.save_local)     
            tini = time.time()
            [head_io_gzip, head_local_mtime, head_remote_mtime] = \
                S3Download(str(headpath),str(headpath)+'.gzip',force_download)            
            if not head_io_gzip is None:
                te = time.time()-tini+0.000001
                datasize = head_io_gzip.getbuffer().nbytes/1000000
                Logger.log.debug('download head %s/%s %.2fMB in %.2fs %.2fMBps ' % \
                    (self.feeder,self.dataset,datasize,te,datasize/te))
                
                head_io_remote_isnewer = True
                head_io_gzip.seek(0)
                head_io = gzip.GzipFile(fileobj=head_io_gzip, mode='rb')                
                
        # open head_io to read header
        if self.sharedData.save_local:
            if head_io is None:
                if headpath.exists():
                    head_io = open(headpath, 'rb')

        # read header
        if not head_io is None:
            head_io.seek(0)
            nbhdrdescr = int.from_bytes(head_io.read(8),byteorder='little')
            hdrdescr_b = head_io.read(nbhdrdescr)
            hdrdescr = hdrdescr_b.decode(encoding='UTF-8',errors='ignore')
            hdrdescr = hdrdescr.replace('\x00','')
            self.hdrnames = hdrdescr.split(';')[0].split(',')
            self.hdrformats = hdrdescr.split(';')[1].split(',')
            self.hdrdtype = np.dtype({'names':self.hdrnames,'formats':self.hdrformats})
            nb_hdr = self.hdrdtype.itemsize            
            head_io.seek(0)
            self.hdr = np.ndarray((1,),dtype=self.hdrdtype,\
                buffer=head_io.read(nb_hdr))[0]
            self.hdr = self.hdr.copy()            
            
            if self.sharedData.s3read:
                if self.hdr['hastail']==1:
                    tini = time.time()
                    [tail_io_gzip, tail_local_mtime, tail_remote_mtime] = \
                        S3Download(str(tailpath),str(tailpath)+'.gzip',force_download)
                    if not tail_io_gzip is None:
                        te = time.time()-tini+0.000001
                        datasize = tail_io_gzip.getbuffer().nbytes/1000000
                        Logger.log.debug('download tail %s/%s %.2fMB in %.2fs %.2fMBps ' % \
                            (self.feeder,self.dataset,datasize,te,datasize/te))
                        
                        tail_io_remote_isnewer = True
                        tail_io_gzip.seek(0)                        
                        tail_io = gzip.GzipFile(fileobj=tail_io_gzip, mode='rb')
             
            if self.sharedData.save_local:
                if self.hdr['hastail']==1:
                    if tail_io is None:                    
                        if tailpath.exists():
                            tail_io = open(tailpath, 'rb')

            # read tail header if exists
            if not tail_io is None:
                tail_io.seek(0)
                tailnbhdrdescr = int.from_bytes(tail_io.read(8),byteorder='little')
                tailhdrdescr_b = tail_io.read(tailnbhdrdescr)
                tailhdrdescr = tailhdrdescr_b.decode(encoding='UTF-8',errors='ignore')
                tailhdrdescr = tailhdrdescr.replace('\x00','')
                self.tailhdrnames = tailhdrdescr.split(';')[0].split(',')
                self.tailhdrformats = tailhdrdescr.split(';')[1].split(',')                
                self.tailhdrdtype = np.dtype({'names':self.tailhdrnames,'formats':self.tailhdrformats})
                                                      
                nbtailhdr = self.tailhdrdtype.itemsize
                tail_io.seek(0)
                tailheader_buf = tail_io.read(nbtailhdr)
                self.tailhdr = np.ndarray((1,),\
                    dtype=self.tailhdrdtype,buffer=tailheader_buf)[0]
                self.tailhdr = self.tailhdr.copy()                 
                self.tailhdr['headersize'] = tailnbhdrdescr     
                self.hdr['count'] = self.hdr['headsize']+self.tailhdr['tailsize']
            
            self.hdr['recordssize'] = int(self.hdr['count']*1.1) # add 10% space for growth
            # malloc create shared memory with recordssize rows
            self.malloc_create(shm_name)
            nb_pkey = int(self.hdr['pkeysize']*4)
            
            # read head data to shared memory            
            head_io.seek(0)
            self.shm.buf[0:nb_hdr] = head_io.read(nb_hdr)
            nb_head = int(self.hdr['headsize']*self.hdr['itemsize'])
            self.shm.buf[nb_hdr+nb_pkey:nb_hdr+nb_pkey+nb_head] = head_io.read(nb_head)

            # latch the hash value
            md5hash = np.copy(self.hdr['md5hash'])
            if not tail_io is None:
                # replace the hash value with tail value
                md5hash = np.copy(self.tailhdr['md5hash'])
                nb_tail = int(self.tailhdr['tailsize']*self.hdr['itemsize'])
                # read tail data to shared memory
                self.shm.buf[nb_hdr+nb_pkey+nb_head:nb_hdr+nb_pkey+nb_head+nb_tail] = tail_io.read(nb_tail)

            #restore header values
            self.hdr['count'] = self.hdr['headsize']+self.tailhdr['tailsize']
            self.hdr['minchgid'] = self.hdr['count']
            self.hdr['recordssize'] = int(self.hdr['count']*1.1) # add 10% space for growth
            
            # check if data is corrupted            
            nb_records = self.hdr['count']*self.hdr['itemsize']
            self.hdr['md5hash'] = 0
            m = hashlib.md5(self.shm.buf[nb_hdr+nb_pkey:nb_hdr+nb_pkey+nb_records])
            if md5hash != m.digest():
                Logger.log.error('File corrupted %s!' % (path))
                raise Exception('File corrupted %s!' % (path))
            
                        
        if self.sharedData.save_local:
            if (head_io_remote_isnewer) | (tail_io_remote_isnewer):
                self.acquire()
                
                # create header                
                [write_head,nb_header,nb_pkey,nb_head,nb_tail] = self.fill_header()
                # save local
                if (head_io_remote_isnewer) | (write_head):
                    self.write_head(path,nb_header,nb_pkey,nb_head,head_remote_mtime)
                    UpdateModTime(path/'head.bin',head_remote_mtime)                  
                if (tail_io_remote_isnewer):
                    self.write_tail(path,nb_header,nb_pkey,nb_head,nb_tail,tail_remote_mtime)
                    UpdateModTime(path/'tail.bin',tail_remote_mtime)

        self.release()

    def write(self):
        path, shm_name = self.get_path(iswrite=True)

        self.acquire()

        tini = time.time()
        # create header
        mtime = self.hdr['mtime']
        [write_head,nb_header,nb_pkey,nb_head,nb_tail] = self.fill_header()
                                     
        # TODO: split write local and remote
        if self.sharedData.s3write:
            if write_head:
                self.upload_head(path,nb_header,nb_pkey,nb_head,mtime)                
            
            if self.hdr['hastail']==1:        
                self.upload_tail(path,nb_header,nb_pkey,nb_head,nb_tail,mtime)        
                
        if self.sharedData.save_local:
            if write_head:
                self.write_head(path,nb_header,nb_pkey,nb_head,mtime)
            
            if self.hdr['hastail']==1:
                self.write_tail(path,nb_header,nb_pkey,nb_head,nb_tail,mtime)

        te = time.time()-tini
        datasize = self.hdr['count']*self.hdr['itemsize']/1000000
        Logger.log.debug('write %s/%s %.2fMB in %.2fs %.2fMBps ' % \
            (self.feeder,self.dataset,datasize,te,datasize/te))
        
        self.release()

    def fill_header(self):
        maxtailsize = int(self.maxtailbytes / self.hdr['itemsize'])
        if self.hdr['count']<=maxtailsize:
            tailsize = 0
            headsize = self.hdr['count']            
            self.hdr['hastail']=0
        else:
            tailsize = self.hdr['count'] % maxtailsize            
            headsize = self.hdr['count'] - tailsize
            self.hdr['hastail']=1
        
        
        headsize_chg = (headsize != self.hdr['headsize'])
        self.hdr['headsize'] = headsize

        head_modified = (self.hdr['minchgid']<=self.hdr['headsize'])
        write_head = (head_modified) | (headsize_chg)

        nb_header = int(self.hdrdtype.itemsize)
        nb_pkey = int(self.hdr['pkeysize']*4)        
        nb_head = int(self.hdr['headsize']*self.hdr['itemsize'])
        nb_tail = int(tailsize*self.hdr['itemsize'])
        
        self.tailhdr['mtime'] = self.hdr['mtime']
        self.tailhdr['tailsize'] = tailsize

        self.hdr['md5hash']=0 # reset the hash value        
        m = hashlib.md5(self.shm.buf[nb_header+nb_pkey:nb_header+nb_pkey+nb_head+nb_tail])
        self.hdr['md5hash'] = m.digest()
        self.tailhdr['md5hash'] = self.hdr['md5hash']
        return [write_head,nb_header,nb_pkey,nb_head,nb_tail]
    
    def upload_head(self,path,nb_header,nb_pkey,nb_head,mtime):
        gzip_io = io.BytesIO()
        with gzip.GzipFile(fileobj=gzip_io, mode='wb', compresslevel=1) as gz:
            gz.write(self.shm.buf[0:nb_header])
            gz.write(self.shm.buf[nb_header+nb_pkey:nb_header+nb_pkey+nb_head])
        S3Upload(gzip_io,path/'head.bin.gzip',mtime)

    def upload_tail(self,path,nb_header,nb_pkey,nb_head,nb_tail,mtime):
        gzip_io = io.BytesIO()
        with gzip.GzipFile(fileobj=gzip_io, mode='wb', compresslevel=1) as gz:
            gz.write(self.tailhdr.tobytes())
            gz.write(self.shm.buf[nb_header+nb_pkey+nb_head:nb_header+nb_pkey+nb_head+nb_tail])
        S3Upload(gzip_io,path/'tail.bin.gzip',mtime)

    def write_head(self,path,nb_header,nb_pkey,nb_head,mtime):
        with open(path/'head.bin', 'wb') as f:
            f.write(self.shm.buf[0:nb_header])
            f.write(self.shm.buf[nb_header+nb_pkey:nb_header+nb_pkey+nb_head])
            f.flush()
        os.utime(path, (mtime, mtime))
        
    def write_tail(self,path,nb_header,nb_pkey,nb_head,nb_tail,mtime):
        with open(path/'tail.bin', 'wb') as f:
            f.write(self.tailhdr)
            f.write(self.shm.buf[nb_header+nb_pkey+nb_head:nb_header+nb_pkey+nb_head+nb_tail])
            f.flush()
        os.utime(path, (mtime, mtime))
    
    def acquire(self,timeout=1):
        # TODO: ensure that the semaphore is thread safe
        telapsed = 0
        while self.hdr['semaphore']==1:
            tsleep = 0.000001+random.random()/1000000
            telapsed += tsleep
            if telapsed>timeout:
                raise TimeoutError('Timeout waiting for semaphore')
            time.sleep(tsleep)            
        self.hdr['semaphore']=1

    def release(self):
        self.hdr['semaphore']=0

class SharedNumpy(np.ndarray):
    
    def __new__(cls, shape, dtype=None, buffer=None, offset=0, strides=None, order=None):
        obj = np.ndarray.__new__(cls, shape, dtype, buffer, offset, strides, order)
        obj.master = None
        return obj
            
    ############################## KEYLESS OPERATIONS ########################################
    
    def insert(self,new_records):
        self.master.acquire()

        nrec = new_records.size           
        _count = self.count
        if (_count + nrec <= self.size):
            arr = super().__getitem__(slice(0, self.size))
            arr[_count:_count+nrec] = new_records
            self.count = _count + nrec            
            self.mtime = datetime.now().timestamp()
        else:
            Logger.log.error('Dataset max size reached!')

        self.master.release()

    def overwrite(self,new_records):
        self.master.acquire()

        # assume new_records is sorted 
        # overwrite based on the first date
        if isinstance(new_records,pd.DataFrame):
            new_records = self.master.df2records(new_records)
        elif (self.dtype != new_records.dtype):
            new_records = self.convert(new_records)

        nrec = new_records.size
        _count = self.count
        # overwrite from first date
        fdate = new_records[0]['date']
        fdateid = np.where(self['date']>=fdate)[0]        
        if np.any(fdateid):
            _count = fdateid[0]
        # set data
        if (_count + nrec <= self.size):                        
            arr = super().__getitem__(slice(0, self.size))
            arr[_count:_count+nrec] = new_records
            self.count = _count + nrec
            self.minchgid = _count
            self.mtime = datetime.now().timestamp()
        else:
            Logger.log.error('Dataset max size reached!')

        self.master.release()

    ############################## PRIMARY KEY OPERATIONS ########################################
    
    def create_pkey(self,start=0):
        arr = super().__getitem__(slice(0, self.size))
        self.master.create_pkey_func(arr,self.count,self.pkey,start)        
        if start==0:
            self.pkey_initialized = True

    def upsert(self,new_records):
        self.master.acquire()        
        
        if not self.pkey_initialized:
            self.create_pkey()

        if isinstance(new_records,pd.DataFrame):
            new_records = self.master.df2records(new_records)
        elif (self.dtype != new_records.dtype):
            new_records = self.convert(new_records)

        # fill mtime
        nidx = np.isnat(new_records['mtime'])
        if nidx.any():
            new_records['mtime'][nidx] = time.time_ns()

        minchgid = self.count        
        if new_records.size==1:
            SharedDataTableKeys.upsert_single(self,new_records)
        else:            
            arr = super().__getitem__(slice(0, self.size))
            self.count,minchgid = self.master.upsert_func(arr,self.count,new_records,self.pkey)

        if self.count == self.size:
            Logger.log.warning('Dataset %s/%s is full!' % \
                (self.master.feeder,self.master.dataset))

        self.minchgid = minchgid
        self.mtime = datetime.now().timestamp()

        self.master.release()
        return minchgid
            
    def get_loc(self,keys):
        self.master.acquire()
        if not self.pkey_initialized:
            self.create_pkey()  
        loc = self.master.get_loc_func(self[:],self.pkey,keys).astype(int)
        self.master.release()
        return loc
                
    def sort_index(self,start=0):
        self.master.acquire()

        # TODO: generalize to multiple keys
        keys = tuple(self[column][start:] for column in self.master.pkeycolumns[::-1])
        idx = np.lexsort(keys)
        
        shift_idx = np.roll(idx, 1)
        if len(shift_idx)>0:
            shift_idx[0] = -1
            idx_diff = idx - shift_idx
            unsortered_idx = np.where(idx_diff != 1)[0]
            if np.where(idx_diff != 1)[0].any():
                _minchgid = np.min(unsortered_idx) + start
                self.minchgid = _minchgid
                self[start:] = self[start:][idx]
                if not self.pkey_initialized:
                    self.create_pkey()
                else:
                    self.create_pkey(_minchgid)

        self.master.release()

    def write(self):
        self.master.write()

    def records2df(self,records):
        return self.master.records2df(records)
    
    def convert(self,new_records):
        rec = np.full((new_records.size,),fill_value=np.nan,dtype=self.dtype)        
        for col in self.dtype.names:
            if col in new_records.dtype.names:
                try:
                    rec[col] = new_records[col].astype(self.dtype[col])
                except:
                    Logger.log.error('Could not convert %s!' % (col))
        return rec

    ############################## GETTERS / SETTERS ##############################
    
    def __getitem__(self, key):
        if hasattr(self,'master'):
            if self.count>0:
                arr = super().__getitem__(slice(0, self.count)) # slice arr
                return arr.__getitem__(key)
            else:
                return np.array([])
        else:
            return super().__getitem__(key)
        
    @property
    def count(self):
        return self.master.hdr['count']
    
    @count.setter
    def count(self,value):
        self.master.hdr['count'] = value
    
    @property
    def mtime(self):
        return self.master.hdr['mtime']
    
    @mtime.setter
    def mtime(self,value):
        self.master.hdr['mtime'] = value

    @property
    def minchgid(self):
        return self.master.hdr['minchgid']
    
    @minchgid.setter
    def minchgid(self,value):
        value = min(value,self.master.hdr['minchgid'])
        self.master.hdr['minchgid'] = value
            
    @property
    def pkey(self):
        return self.master.pkey
    
    @pkey.setter
    def pkey(self,value):        
        self.master.pkey = value
    
    @property
    def pkey_initialized(self):
        return self.master.pkey_initialized
    
    @pkey_initialized.setter
    def pkey_initialized(self,value):        
        self.master.pkey_initialized = value

        
class SharedDataTableKeys():
    
    def get_pkeycolumns(database):
        if database == 'MarketData':
            return ['date','symbol']
        elif database == 'Signals':
            return ['date','signal','riskfactor']
        elif database == 'Portfolios':
            return ['date','portfolio']
        elif database == 'Risk':
            return ['date','portfolio','riskfactor']
        elif database == 'Positions':
            return ['date','portfolio','symbol']
        elif database == 'Orders':
            return ['date','portfolio','symbol','clordid']
        elif database == 'Trades':
            return ['date','portfolio','symbol','tradeid']
        else:
            return ['date','symbol']

    ############################## NUMBA JIT FUNCTIONS ##############################
    def upsert_single(sharednp,new_record):
        n = sharednp.pkey.size-1
        pkeycolumns=sharednp.master.pkeycolumns
        if sharednp.count < sharednp.size:
            h = hash(new_record[pkeycolumns[0]])
            for key in pkeycolumns[1:]:
                h = h ^ hash(new_record[key])
            h = h % n            
            id = sharednp.pkey[h]
            if id == -1: 
                # new record doesnt exist
                sharednp.pkey[h] = sharednp.count
                sharednp[sharednp.count] = new_record
                sharednp.count = sharednp.count + 1
            else:
                # check for hash collision
                j = 1            
                ismatch = True
                for key in pkeycolumns:
                    ismatch = (ismatch) & (sharednp[id][key] == new_record[key])
                while not ismatch:
                    h = (h + j**2) % n
                    id = sharednp.pkey[h]
                    if id==-1:
                        break
                    ismatch = True
                    for key in pkeycolumns:
                        ismatch = (ismatch) & (sharednp[id][key] == new_record[key])
                    j += 1

                if id == -1: 
                    # new record doesnt exist
                    sharednp.pkey[h] = sharednp.count
                    sharednp[sharednp.count] = new_record
                    sharednp.count = sharednp.count + 1
                else:
                    # new record exists                    
                    sharednp[id] = new_record

    @staticmethod
    @njit(cache=True)
    def upsert_marketdata_jit(records,count,new_records,pkey):
        n = pkey.size-1                
        minchgid = count
        maxsize = records.size        
        nrec = new_records.size
        for i in range(nrec):            
            h1 = hash(new_records['date'][i])
            h2 = hash(new_records['symbol'][i])
            h3 = h1 ^ h2
            h = h3 % n            
            id = pkey[h]
            if id == -1: 
                # new record doesnt exist
                pkey[h] = count                
                records[count] = new_records[i]
                if count < maxsize:
                    count = count + 1
                else:
                    break
            else:
                # check for hash collision
                j = 1            
                while (records[id]['date'] != new_records[i]['date'])\
                    | (records[id]['symbol'] != new_records[i]['symbol']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1

                if id == -1: 
                    # new record doesnt exist
                    pkey[h] = count                    
                    records[count] = new_records[i]
                    if count < maxsize:
                        count = count + 1
                    else:
                        break
                else:
                    # new record exists                    
                    records[id] = new_records[i]
                    if id < minchgid:
                        minchgid = id
        return count,minchgid
              
    @staticmethod
    @njit(cache=True)
    def upsert_signals_jit(records,count,new_records,pkey):
        n = pkey.size-1                
        minchgid = count
        maxsize = records.size
        nrec = new_records.size
        for i in range(nrec):        
            h1 = hash(new_records['date'][i])
            h2 = hash(new_records['signal'][i])
            h3 = hash(new_records['symbol'][i])            
            h4 = h1 ^ h2 ^ h3
            h = h4 % n
            id = pkey[h]
            if id == -1: 
                # new record doesnt exist
                pkey[h] = count
                records[count] = new_records[i]
                if count < maxsize:
                    count = count + 1
                else:
                    break
            else:
                # check for hash collision
                j = 1
                while (records[id]['date'] != new_records[i]['date'])\
                    | (records[id]['signal'] != new_records[i]['signal'])\
                    | (records[id]['symbol'] != new_records[i]['symbol']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1

                if id == -1: 
                    # new record doesnt exist
                    pkey[h] = count
                    records[count] = new_records[i]
                    if count < maxsize:
                        count = count + 1
                    else:
                        break
                else:
                    # new record exists
                    records[id] = new_records[i]
                    if id < minchgid:
                        minchgid = id
        return count,minchgid

    @staticmethod
    @njit(cache=True)
    def upsert_portfolio_jit(records,count,new_records,pkey):
        n = pkey.size-1                
        minchgid = count
        maxsize = records.size
        nrec = new_records.size
        for i in range(nrec):            
            h1 = hash(new_records['date'][i])
            h2 = hash(new_records['portfolio'][i])
            h3 = hash(new_records['symbol'][i])                
            h4 = h1 ^ h2 ^ h3
            h = h4 % n
            id = pkey[h]
            if id == -1: 
                # new record doesnt exist
                pkey[h] = count                
                records[count] = new_records[i]
                if count < maxsize:
                    count = count + 1
                else:
                    break
            else:
                # check for hash collision
                j = 1                
                while (records[id]['date'] != new_records[i]['date'])\
                    | (records[id]['portfolio'] != new_records[i]['portfolio'])\
                    | (records[id]['symbol'] != new_records[i]['symbol']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1

                if id == -1: 
                    # new record doesnt exist
                    pkey[h] = count
                    records[count] = new_records[i]
                    if count < maxsize:
                        count = count + 1
                    else:
                        break
                else:
                    # new record exists
                    records[id] = new_records[i]
                    if id < minchgid:
                        minchgid = id
        return count,minchgid
      
    @staticmethod
    @njit(cache=True)
    def create_pkey_marketdata_jit(records,count,pkey,start):
        n = pkey.size-1        
        pkey[:] = -1
        for i in range(start,count):
            h1 = hash(records['date'][i])
            h2 = hash(records['symbol'][i])
            h3 = h1 ^ h2
            h = h3 % n            
            id = pkey[h]
            if id == -1:
                pkey[h] = i
            else:
                # check for hash collision
                j = 1
                while (records[id]['date'] != records[i]['date'])\
                    | (records[id]['symbol'] != records[i]['symbol']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1

                if id == -1: 
                    # new record doesnt exist
                    pkey[h] = i
                else:
                    raise Exception('error duplicated index!')                    
                
    @staticmethod
    @njit(cache=True)
    def create_pkey_signals_jit(records,count,pkey,start):
        n = pkey.size-1        
        pkey[:] = -1
        for i in range(start,count):
            h1 = hash(records['date'][i])
            h2 = hash(records['signal'][i])
            h3 = hash(records['symbol'][i])
            h4 = h1 ^ h2 ^ h3
            h = h4 % n            
            id = pkey[h]
            if id == -1:                 
                pkey[h] = i
            else:
                # check for hash collision
                j = 1
                while (records[id]['date'] != records[i]['date'])\
                    | (records[id]['signal'] != records[i]['signal'])\
                    | (records[id]['symbol'] != records[i]['symbol']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1

                if id == -1: 
                    # new record doesnt exist
                    pkey[h] = i
                else:
                    raise Exception('error duplicated index!')                    
    
    @staticmethod
    @njit(cache=True)
    def create_pkey_portfolio_jit(records,count,pkey,start):
        n = pkey.size-1        
        pkey[:] = -1
        for i in range(start,count):
            h1 = hash(records['date'][i])
            h2 = hash(records['portfolio'][i])
            h3 = hash(records['symbol'][i])
            h4 = h1 ^ h2 ^ h3
            h = h4 % n            
            id = pkey[h]
            if id == -1:                 
                pkey[h] = i
            else:
                # check for hash collision
                j = 1
                while (records[id]['date'] != records[i]['date'])\
                    | (records[id]['portfolio'] != records[i]['portfolio'])\
                    | (records[id]['symbol'] != records[i]['symbol']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1

                if id == -1: 
                    # new record doesnt exist
                    pkey[h] = i
                else:
                    raise Exception('error duplicated index!')                    

    @staticmethod
    @njit(cache=True)
    def get_loc_marketdata_jit(records,pkey,keys):
        n = pkey.size-1
        loc = np.empty((keys.size, ))
        for i in range(keys.size):
            h1 = hash(keys['date'][i])
            h2 = hash(keys['symbol'][i])
            h3 = h1 ^ h2
            h = h3 % n            
            id = pkey[h]
            if id == -1:
                loc[i] = id
            else:
                # check for hash collision
                j = 1
                while (records[id]['date'] != keys[i]['date'])\
                    | (records[id]['symbol'] != keys[i]['symbol']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1
                loc[i] = id
        return loc
    
    @staticmethod
    @njit(cache=True)
    def get_loc_signals_jit(records,pkey,keys):
        n = pkey.size-1
        loc = np.empty((keys.size, ))
        for i in range(keys.size):
            h1 = hash(records['date'][i])
            h2 = hash(records['signal'][i])
            h3 = hash(records['symbol'][i])
            h4 = h1 ^ h2 ^ h3
            h = h4 % n
            id = pkey[h]
            if id == -1:
                loc[i] = id
            else:
                # check for hash collision
                j = 1
                while (records[id]['date'] != records[i]['date'])\
                    | (records[id]['signal'] != records[i]['signal'])\
                    | (records[id]['symbol'] != records[i]['symbol']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1
                loc[i] = id
        return loc
    
    @staticmethod
    @njit(cache=True)
    def get_loc_portfolio_jit(records,pkey,keys):
        n = pkey.size-1
        loc = np.empty((keys.size, ))
        for i in range(keys.size):
            h1 = hash(records['date'][i])
            h2 = hash(records['portfolio'][i])
            h3 = hash(records['symbol'][i])
            h4 = h1 ^ h2 ^ h3
            h = h4 % n
            id = pkey[h]
            if id == -1:
                loc[i] = id
            else:
                # check for hash collision
                j = 1
                while (records[id]['date'] != records[i]['date'])\
                    | (records[id]['portfolio'] != records[i]['portfolio'])\
                    | (records[id]['symbol'] != records[i]['symbol']):
                    h = (h + j**2) % n
                    id = pkey[h]
                    if id==-1:
                        break
                    j += 1
                loc[i] = id
        return loc
                
