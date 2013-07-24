'''
Created on 17-07-2012

@author: pogoma
'''

import string
import re
from defaultParser import defaultParser

class ReutersMobileParser( defaultParser ):
  def reset( self ):
    defaultParser.reset( self )
    self.id = "reutersM"
    self.rdTimestamp = False
    self.endTimestamp = False
    self.endContent = False
    self.spanX = 0
    self.spanArt = 0
    self.spanTime = 0
    self.addr = "http://www.reuters.com/resources/archive/us/{YEAR}{MONTH}{DAY}.html"

  def start_div( self, attrs ):
    idc = [v for k, v in attrs if k == 'class']
    idc.append( "0" )
    if idc[0].find( "sm" ) >= 0 and not self.endTimestamp:
      self.data = [];
      self.rdTimestamp = True
      self.endContent = False
    if idc[0].find( "lnk" ) >= 0 and not self.endContent:
      tmp = string.join( self.data, "" )
      tmp = tmp.replace( "\t", " " )
      tmp = tmp.replace( "&", "and" )
      tmp = re.sub( "[\n]+", " ", tmp )
      tmp = re.sub( "[\r]+", " ", tmp )
      tmp = re.sub( "[-]+", " ", tmp )
      tmp = re.sub( " [ ]+", " ", tmp )
      tmp = tmp.replace( "Email Article", "" )
      self.content = tmp
      self.data = []
      self.endContent = True

  def end_div( self ):
    if self.rdTimestamp:
      self.timestamp = string.join( self.data, "" )
      self.data = []
      self.rdTimestamp = False
      self.endTimestamp = True
      self.endContent = False

  def start_title( self, attrs ):
    self.data = []

  def end_title( self ):
    self.title = string.join( self.data, "" )
    self.title = self.title.replace( "\n", "" )
    self.title = self.title.replace( "  ", "" )
    self.title = self.title.replace( "| Reuters.com", "" )
    self.title = self.title.replace( "| Reuters", "" )
    self.title = self.title.replace( "&", "and" )

  def getAddrList( self ):
    addrList = []
    for url in self.addrs:
      if url[0].find( 'article' ) > 0:
        if not url[1].find( 'Following Is a Test Release' ) >= 0:
          if not url[1].find( 'REG-' ) >= 0:
            if not url[1].find( 'REG -' ) >= 0:
              if not url[0].find( "/id" ) >= 0:
                tmp = re.sub( "[^/]*-", "", url[0] )
                tmp = re.sub( "[^/]*\+", "", tmp )
              else:
                tmp = url[0]
              addrList.append( tmp.replace( 'http://www', 'http://mobile' ) )
    return addrList

  def parsePageSource( self, _url ):
    defaultParser.parsePageSource( self, _url )
    tit = self.title
    tim = self.timestamp
    con = self.content
    tmp = self.content[:15]
    m = re.search( "[0-9]+ of ([0-9]+)", tmp )
    if not m == None:
      for i in range ( int( m.group( 1 ) ) ):
        if i > 0:
          tmpUrl = _url + "?i=" + str( i + 1 )
          defaultParser.parsePageSource( self, tmpUrl )
          con = con + self.content
    self.title = tit
    self.timestamp = tim
    self.content = con
