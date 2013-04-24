"""
  Sink: Use as the receiving side of a link.  By default it will use
  the network layer to print the received rate over a sliding window
  of 10 packets.

  Author: Daniel Zappala, Brigham Young University
  
  This program is licensed under the GPL; see LICENSE for details.

"""

import socket
import sys

sys.path.append("./src")
from router import *

qsize = 10
rate = 128
prop = 50
mtu = 1024

# configure router
r = Router()
r.link.link(0,"localhost",5001,"localhost",5000,10,128,50,1024)

# terminate on readline
junk = raw_input("Press enter to stop: ")
