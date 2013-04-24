"""
  LinkLayer: Implements the link layer for a virtual network.  The router
  can have multiple incoming and outgoing links.  Each link should emulate
  both the transmission and propagation delay using a call to time.sleep().

  Author: Daniel Zappala, Brigham Young University
  
  This program is licensed under the GPL; see LICENSE for details.

"""

import socket
import sys
import threading
import time

# delete the following two lines if you have Python 2.5 installed
sys.path.append(".")
from queue import *

__all__ = [ "LinkLayer" , "MTUExceeded" ]

class LinkLayer:
    """ Provide an emulated interface to the link layer of a host or
    router.
    """
    def __init__(self):
        """ Initialize the link layer."""
        # initialize member variables
        self.inlinks = {}
        self.outlinks = {}
        LinkLayer.statsfile = None

    def up_layer(self,layer):
        self.network = layer

    def down_layer(self,layer):
        pass

    def stats_file(self,file):
        if LinkLayer.statsfile:
            LinkLayer.statsfile.close()
        LinkLayer.statsfile = open(file,"w")

    def stats(self,string):
        if LinkLayer.statsfile:
            LinkLayer.statsfile.write(string+"\n")
            LinkLayer.statsfile.flush()

    def link(self,linkID,myhost,myport,host,port,size,rate,delay,mtu):
        """ Create a link to another computer.

        linkID -- identifier for this link
        myhost -- host name for this end of the link
        myport -- UDP port for this end of the link
        host   -- host name for the other end of the link
        port   -- UDP port for the other end of the link
        size   -- size of the queue for the link
        rate   -- emulated rate for the link, in kbps
        delay  -- propagation delay for the link
        mtu    -- maximum transmission unit for the link in bytes
        """
        # if an IncomingLink already exists for this linkID, close it
        if linkID in self.inlinks:
            self.inlinks[linkID].stop()
        # create an instance of IncomingLink and an instance of
        #  OutgoingLink with the appropriate parameters
        self.inlinks[linkID] = IncomingLink(self.network,myport,host,delay,mtu)
        self.outlinks[linkID] = OutgoingLink(host,port,size,rate,mtu)
        # set daemon on threads
        self.inlinks[linkID].setDaemon(True)
        self.outlinks[linkID].setDaemon(True)
        # start the IncomingLink and OutgoingLink threads
        self.inlinks[linkID].start()
        self.outlinks[linkID].start()

    def reset(self,linkID):
        """ Reset the sequence number for the link. """
        if linkID in self.outlinks:
            self.outlinks[linkID].reset()

    def send(self,packet,linkID):
        """ Send a packet on the appropriate outgoing link

        packet -- packet to send
        linkID -- outgoing link identifier

        Return value: none
        
        """
        # look up instance of OutgoingLink and enqueue the packet
        self.outlinks[linkID].enqueue(packet)


class IncomingLink(LinkLayer,threading.Thread):
    """ Receive incoming packets for one link on the router. """
    
    def __init__(self,network,port,host,delay,mtu):
        """ Initialize incoming link.

        network -- network layer
        port    -- UDP port for this end of the link
        host    -- host name for the other end of the link
        delay   -- propagation delay for the link in ms
        mtu     -- maximum transmission unit for the link in bytes
        """
        threading.Thread.__init__(self)
        # initialize member variables
        self.network = network
        self.port = port
        self.host = socket.gethostbyname(host)
        self.delay = float(delay)/1000
        self.mtu = mtu
        self.running = True
        # setup UDP server socket to receive incoming packets
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("",self.port))
        self.sock.settimeout(1)

    def stop(self):
        """ Stop this link. """
        self.running = False
        time.sleep(1)
        self.sock.close()
        
    def run(self):
        """ Continuously receive packets.  This method is activated by
        a call to start() on the object and runs in a separate thread. """
        while self.running:
            # receive incoming packets
            try:
                packet,address = self.sock.recvfrom(self.mtu)
            except socket.timeout:
                continue
            # check that source has the expected IP address
            if address[0] != self.host:
                continue
            # sleep for configured propagation delay
            time.sleep(self.delay)
            # deliver the packet
            self.network.deliver(packet)

            # TBD: the sleep above is broken.  Figure out why and
            # fix it.


class OutgoingLink(LinkLayer,threading.Thread):
    """ Send outgoing packets for one link on the router. """

    def __init__(self,host,port,size,rate,mtu):
        """ Initialize outgoing link.

        host -- IP address for the other end of the link
        port -- UDP port for the other end of the link
        size -- maximum queue size
        rate -- emulated rate for the link, in kbps
        """
        threading.Thread.__init__(self)
        # initialize member variables
        self.host = host
        self.port = port
        self.size = size
        self.rate = rate
        self.mtu = mtu
        # initialize socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # initialize the queue
        self.queue = Queue(self.size)
        # initialize sequence number
        self.sequence = -1
        self.maxint = 10**9

    def reset(self):
        """ Reset the sequence number for this link """
        self.sequence = -1

    def enqueue(self,packet):
        """ Queue a packet on this link """
        # increment and wrap around sequence number
        if self.sequence == self.maxint:
            self.sequence = 0
        else:
            self.sequence += 1
        # take the time for stats
        t1 = time.time()

        # TBD: reject packet if it exceeds the MTU and raise the MTUExceeded
        # exception

        # TBD: use the following when a packet exceeds the MTU
        self.stats("%f %d m" % (t1,self.sequence))

        # TBD: put (sequence,packet) in queue if there is room, otherwise
        # drop the packet

        # TBD: use the following when adding a packet
        self.stats("%f %d a" % (t1,self.sequence))
        # TBD: use the following when dropping a packet
        self.stats("%f %d d" % (t1,self.sequence))

    def run(self):
        """ Continuously send packets in the queue for this link,
        using an emulated bandwidth given by the configured rate.
        This method is activated by a call to start() on the object
        and runs in a separate thread."""
        while True:
            # TBD: dequeue (sequence, packet)

            t1 = time.time()
            self.stats("%f %d s" % (t1,sequence))
            # TBD: calculate the time required to send this packet

            # TBD: sleep for this amount of time

            # send the packet using UDP to the configured host and port
            try:
                self.sock.sendto(packet,(self.host,self.port))
            except:
                print "** Error using UDP socket, closing link to",self.host
                print "  ",sys.exc_info()[0],sys.exc_info()[1]
                return


class MTUExceeded(Exception):
    """ MTUExceeded exception to raise when MTU is too large """
    pass
