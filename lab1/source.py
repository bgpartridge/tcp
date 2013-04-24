"""
  Source: Use as your first link layer test.  Sends a single packet over
  the router's link.  Be sure to modify the network layer deliver() method
  to print out the contents of the packet.  You should see the sink receive
  the packet we are sending here.

  Author: Daniel Zappala, Brigham Young University
  
  This program is licensed under the GPL; see LICENSE for details.

"""


import socket
import sys

sys.path.append("./src")
from router import *

r = Router()
r.link.link(0,"localhost",5000,"localhost",5001,10,128,10,1024)

packet = "test data"

junk = raw_input("Press enter to start: ")

r.link.send(packet,0)

# terminate on readline
junk = sys.stdin.readline()
