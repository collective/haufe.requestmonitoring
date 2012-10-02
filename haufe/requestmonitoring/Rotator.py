#       $Id: Rotator.py,v 1.1.156.2 2007-11-27 09:35:56 hamannu Exp $
'''A daily rotating file.'''

from time import time, mktime, localtime, strftime
from threading import Lock


class RotatorInfo:
  '''information about a rotating file.'''
  def __init__(self,base,format='.%y%m%d'):
    self._base= base
    self._format= format
    self._setup()

  def toSwitch(self):
    '''true, when we should switch filename.'''
    return time() > self._limit

  def getFilename(self):
    '''the current filename.'''
    if self.toSwitch(): self._setup()
    return self._filename

  def _setup(self,_t= (0,0,0)):
    lt= localtime(time())
    st= lt[:3] + _t + lt[6:]
    self._limit= mktime(st[:2] + (st[2]+1,) + st[3:])
    self._filename= self._base + strftime(self._format,st)

class Rotator(RotatorInfo):
  '''a rotating writable file like object.'''
  def __init__(self,base,format='.%y%m%d',lock=0):
    RotatorInfo.__init__(self,base,format)
    self._lock= lock and Lock()
    self._open()

  def write(self,str):
    '''write *str* and flush.'''
    lock= self._lock
    if lock: lock.acquire()
    try:
      if self.toSwitch(): self._open()
      f= self._file
      f.write(str)
      f.flush()
    finally:
      if lock: lock.release()

  def flush(self):
    '''helper to support applications that want to flush themselves.'''
    pass

  def close(self):
    if self._file is not None:
      self._file.close()
      self._file = None

  def _open(self):
    self._file= open(self.getFilename(),"a") # ATT: developped for Unix



    
