"""
  Traffic generator: A simple traffic generator to run queueing experiments.
  This code will setup a 128 Kbps link, then test queue sizes of unlimited (0),
  20, and 10 packets, with loads ranging from very light traffic to very
  heavy traffic.  All statistics are stored in the stats directory using
  the naming convention:

    queue-[rate]-[queueSize]-[load].txt

  If you are writing the events properly to the log file, then you should
  have an easy to parse format:

    [time] [sequence] [event]

  where [event] is:

    a - added to queue
    d - dropped
    m - mtu exceeded
    s - sent

  Author: Daniel Zappala, Brigham Young University
  
  This program is licensed under the GPL; see LICENSE for details.

"""

import random
import socket
import sys
import time

sys.path.append("./src")
from router import *

rates = [128]
qsizes = [0,20,10]
# loads are given in packets per second
loads = [1.5625,7.8125,11.71875,15.625,17.1875,23.4375,31.25]

packets = 100
mtu = 1024
prop = 50

# configure router
r = Router()

for rate in rates:
    for qsize in qsizes:
        r.link.link(0,"localhost",5000,"localhost",5001,qsize,rate,prop,mtu)
        # banner
        print "Rate: %d kbps Queue Size: %d" % (rate,qsize)
        # generate and send packets using an exponential distribution
        for load in loads:
            time.sleep(5)
            print "  %s Packets per second..." % str(load)
            r.link.stats_file("stats/queue-%d-%d-%s.txt" %(rate,qsize,str(load)))
            r.link.reset(0)
            for i in range(0,packets):
                t = random.expovariate(load)
                time.sleep(t)
                packet = str(i) +  " "
                packet += "x"*(1024 - len(packet))
                r.link.send(packet,0)

# terminate after sleep (be sure this is long enough)
time.sleep(2)
