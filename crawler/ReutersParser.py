'''
Created on 17-07-2012

@author: pogoma
'''

import string
from defaultParser import defaultParser

class ReutersParser( defaultParser ):
  def reset( self ):
    defaultParser.reset( self )
    self.id = "reuters"
    self.endTimestamp = False
    self.midArt = False
    self.endContent = False
    self.spanX = 0
    self.spanArt = 0
    self.spanTime = 0
    self.addr = "http://www.reuters.com/resources/archive/us/{YEAR}{MONTH}{DAY}.html"

  def start_span( self, attrs ):
    self.spanX = self.spanX + 1
    idc = [v for k, v in attrs if k == 'id']
    idc.append( "0" )
    if idc[0].find( "articleText" ) >= 0:
      self.data = [];
      self.spanArt = self.spanX
      self.midArt = True
    idc = [v for k, v in attrs if k == 'class']
    idc.append( "0" )
    if idc[0].find( "timestamp" ) >= 0 and not self.endContent and self.midArt:
      self.data = [];
      self.spanTime = self.spanX

  def end_span( self ):

    if self.spanX == self.spanArt and self.midArt:

      self.content = self.content + string.join( self.data, "" )
      self.endContent = True
      self.midArt = False
    if self.spanX == self.spanTime and not self.endTimestamp:
      self.timestamp = string.join( self.data, "" )
      self.endTimestamp = True
      self.data = []
    self.spanX = self.spanX - 1

  def start_title( self, attrs ):
    self.data = []

  def end_title( self ):
    self.title = string.join( self.data, "" )
    self.title = self.title.replace( "\n", "" )
    self.title = self.title.replace( "  ", "" )
    self.title = self.title.replace( "| Reuters", "" )
    self.title = self.title.replace( "&", "and" )

  def getAddrList( self ):
    addrList = []
    for url in self.addrs:
      if url[0].find( 'article' ) > 0:
        if not url[1].find( 'Following Is a Test Release' ) >= 0:
          if not url[1].find( 'REG-' ) >= 0:
            addrList.append( url[0] )
    return addrList

