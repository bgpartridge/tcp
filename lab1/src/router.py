"""
  Router: Implements a router for a virtual network.  Currently
  incomplete, it includes only a network and link layer.

  Author: Daniel Zappala, Brigham Young University
  
  This program is licensed under the GPL; see LICENSE for details.

"""

import sys

sys.path.append(".")
from link import *
from network import *

__all__ = [ "Router" ]

class Router:
    def __init__(self):
        self.network = NetworkLayer()
        self.link = LinkLayer()
        self.link.up_layer(self.network)
