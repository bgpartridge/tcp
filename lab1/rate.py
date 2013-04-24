"""
  Rate tester: Use to test whether the transmission and propagation delay are
  implemented correctly.  Start a sink and then start this rate tester.

  Author: Daniel Zappala, Brigham Young University
  
  This program is licensed under the GPL; see LICENSE for details.

"""

import random
import socket
import sys
import time

sys.path.append("./src")
from router import *

size = 1024
prop = 10
qsize = 10
packets = 100

rate = raw_input("Enter rate to test in kbps: ")
rate = int(rate)

# choose a load that exceeds the rate by 25%
load = (1000.0*rate)/(8.0*size)*1.25

# configure router
r = Router()
r.link.link(0,"localhost",5000,"localhost",5001,qsize,rate,prop,size)

# banner
print "Rate: %d kbps Queue Size: %d" % (rate,qsize)

# generate and send packets using an exponential distribution
print "  %s Packets per second..." % str(load)
for i in range(0,packets):
    t = random.expovariate(load)
    time.sleep(t)
    packet = str(i) +  " "
    packet += "x"*(1024 - len(packet))
    r.link.send(packet,0)

# terminate after sleep
time.sleep(2)
