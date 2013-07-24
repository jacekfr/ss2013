'''
Created on 26-07-2012

@author: staz
'''

import string
import re
from defaultParser import defaultParser


class BloombergMobileParser( defaultParser ):
  def reset( self ):
    defaultParser.reset( self )
    self.id = "bloombergM"
    self.endTimestamp = False
    self.rdTimestamp = False
    self.midArt = False
    self.endContent = False
    self.divX = 0
    self.divArt = 0
    self.addr = "http://www.bloomberg.com/archive/news/{YEAR}-{MONTH}-{DAY}/"

  def start_div( self, attrs ):
    idc = [v for k, v in attrs if k == 'class']
    idc.append( "0" )
    if idc[0].find( "timestamp" ) >= 0 and not self.endTimestamp:
      self.data = [];
      self.rdTimestamp = True
      self.endTimestamp = False
    if idc[0].find( "first-paragraph" ) >= 0 and not self.midArt:
      self.data = []
      self.midArt = True
    if idc[0].find( "clear" ) >= 0 and self.midArt:
      tmp = string.join( self.data, "" )
      tmp = re.sub( "[\n\r]", " ", tmp )
      tmp = re.sub( "[\t]+", " ", tmp )
      tmp = re.sub( "[ ]+", " ", tmp )
      tmp = re.sub( "To contact the reporter on this story:.*", "", tmp )
      self.content = tmp
      self.midArt = False

  def end_div( self ):
    if not self.endTimestamp and self.rdTimestamp:
      tmp = string.join( self.data, "" )
      m = re.search( '[A-Za-z]+ [0-9]{1,2}, [0-9]{4} [0-9]{1,2}:[0-9]{1,2} [p|P|a|A][m|M] [A-Za-z]{1,10}', tmp )
      if not m == None:
        self.timestamp = m.group( 0 )
      self.endTimestamp = True
      self.rdTimestamp = False
      self.data = []


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
            addrList.append( "http://mobile.bloomberg.com" + url[0] )
    return addrList

