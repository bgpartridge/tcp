"""
  Queue: Implements a shared queue for those systems that don't have Python
  2.5 installed.  If you have Python 2.5 you can ignore this code.

  This implementation is based on the spec of Queue for Python 2.5,
  but includes only the put_nowait() and get() methods, since those are
  the only ones currently needed.

  Author: Daniel Zappala, Brigham Young University
  
  This program is licensed under the GPL; see LICENSE for details.

"""

import threading

__all__ = [ "Queue", "Full" ]

class Full(Exception):
    pass
    
class Queue:
    def __init__(self,size):
        self.size = size
        self.queue = []
        self.qcv = threading.Condition()
        
    def put_nowait(self,item):
        self.qcv.acquire()
        if self.size > 0 and len(self.queue) >= self.size:
            self.qcv.release()
            raise Full
        self.queue.append(item)
        self.qcv.notify()
        self.qcv.release()

    def get(self):
        self.qcv.acquire()
        while len(self.queue) == 0:
            self.qcv.wait()
        item = self.queue.pop(0)
        self.qcv.release()
        return item
