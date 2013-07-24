'''
Created on 18-07-2012

@author: pogoma
'''

import string
import re
from defaultParser import defaultParser

class BloombergParser( defaultParser ):
  def reset( self ):
    defaultParser.reset( self )
    self.id = "bloomberg"
    self.endTimestamp = False
    self.midArt = False
    self.endContent = False
    self.divX = 0
    self.divArt = 0
    self.addr = "http://www.bloomberg.com/archive/news/{YEAR}-{MONTH}-{DAY}/"

  def start_span( self, attrs ):
    idc = [v for k, v in attrs if k == 'class']
    idc.append( "0" )
    if idc[0].find( "datestamp" ) >= 0:
      self.data = [];
      self.endTimestamp = False


  def end_span( self ):
    if  not self.endTimestamp:
      self.timestamp = string.join( self.data, "" )
      self.endTimestamp = True
      self.data = []

  def start_div( self, attrs ):
    self.divX = self.divX + 1
    idc = [v for k, v in attrs if k == 'id']
    idc.append( "0" )
    if idc[0].find( "story_content" ) >= 0:
      self.data = []
      self.midArt = True

      self.divArt = self.divX



  def end_div( self ):
    if  self.midArt and self.divArt == self.divX:
      self.content = string.join( self.data, "" ).replace( "/", "" )
      self.content = re.sub( "To contact the reporter on this story:[ A-Za-z.]*", "", self.content )
      self.midArt = False
      self.data = []

    self.divX = self.divX - 1

  def start_title( self, attrs ):
    self.data = []

  def end_title( self ):
    self.title = string.join( self.data, "" )
    self.title = self.title.replace( "\n", "" )
    self.title = self.title.replace( "  ", "" )
    self.title = self.title.replace( "- Bloomberg", "" )
    self.title = self.title.replace( "&", "and" )

  def getAddrList( self ):
    addrList = []
    for url in self.addrs:
      if url[0].find( 'news' ) >= 0:
        if re.match( "/news/[0-9][0-9][0-9][0-9]-[0-9][0-9]", url[0] ) >= 0:
          if not url[0].find( "achive" ) >= 0:
            addrList.append( "http://www.bloomberg.com" + url[0] )
    return addrList

