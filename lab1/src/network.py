"""
  NetworkLayer: Implements the network layer for a virtual network.  Currently
  incomplete, it includes only a simple delivery function that measures the
  received rate.

  Author: Daniel Zappala, Brigham Young University
  
  This program is licensed under the GPL; see LICENSE for details.

"""

import time

__all__ = [ "NetworkLayer" ]

class NetworkLayer:
    """ Provide an emulated interface to the network layer of a
    router.
    """
    def __init__(self):
        """ Initialize the network layer. """
        self.times = []
        self.bytes = []

    def route(self,ip,linkid):
        """ add/change the route for the IP address to use the given link ID
        """
        pass

    def send(self,packet):
        """ Send a packet. """
        pass

    def deliver(self,packet):
        """ The link layer calls this method to deliver a packet to the
        network layer."""
        # Uncomment the following two lines when you first begin testing.
        # print packet
        # return
        
        # Measure the received rate by averaging over every 10 packets
        # received, using a sliding window.  Note, if there is a large
        # delay between packets, this rate will be off -- it only works
        # for a steady stream of packets.
        t1 = time.time()
        self.times.append(t1)
        self.bytes.append(len(packet))
        if len(self.bytes) == 11:
            total = 0
            for byte in self.bytes[1:]:
                total += byte
            rate = (total*8.0)/(1000*(t1 - self.times[0]))
            print "Rate: %f kbps" % rate
            self.bytes.pop(0)
            self.times.pop(0)
            
