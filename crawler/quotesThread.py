'''
Created on 24-07-2012

@author: staz
'''

import threading
import time

class quotesThread( threading.Thread ):
  def __init__( self, _id, _ui = None ):
    threading.Thread.__init__( self )
    self.id = _id
    self.startTime = 0
    self.ui = _ui

  def run( self ):
    self.startTime = time.clock()
