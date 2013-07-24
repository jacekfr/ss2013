'''
Created on 17-07-2012

@author: pogoma
'''

from sgmllib import SGMLParser
import string
import urllib
import re

class defaultParser( SGMLParser ):
  def reset( self ):
    SGMLParser.reset( self )
    self.id = "default"
    self.addr = "{DAY}{MONTH}{YEAR}"
    self.urls = []
    self.data = None
    self.data_url = None
    self.addrs = []
    self.title = ""
    self.timestamp = ""
    self.content = ""
    self.categories = []

  def clearSource( self, _source ):
    _source = re.sub( "<.* />", "", _source )
    return _source

  def cleanTags( self, _source ):
    _source = re.sub( "<.* />", "", _source )
    _source = re.sub( "<.{1,100}>", "", _source )
    _source = _source.replace( "<", "" )
    _source = _source.replace( ">", "" )
    return _source

  def getId( self ):
    return self.id

  def handle_data( self, data ):
    if self.data is not None:
      self.data.append( data )
    if self.data_url is not None:
      self.data_url.append( data )


  def start_a( self, attrs ):
    href = [v for k, v in attrs if k == 'href']
    if href:
      self.urls.extend( href )
    self.data_url = []

  def end_a( self ):
    val = string.join( self.data_url, "" )
    if self.urls.__len__() >= 1 :
      self.addrs.append( ( self.urls[-1], val ) )
    self.data_url = []

  def getAddrE( self ):
    return self.addr

  def getAddr( self, _day, _month, _year ):
    addr = self.addr.replace( '{MONTH}', _month )
    addr = addr.replace( '{DAY}', _day )
    addr = addr.replace( '{YEAR}', _year )
    return addr

  def getAddrList( self ):
    return []

  def parsePageSource( self, _url ):
    self.endContent = False
    self.endTimestamp = False
    try:
      sock = urllib.urlopen( _url )
      htmlSource = sock.read()
      sock.close()
    except:
      return
    self.feed( self.clearSource( htmlSource ) )
    self.content = self.cleanTags( self.content )
