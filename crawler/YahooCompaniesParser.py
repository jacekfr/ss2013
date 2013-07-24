'''
Created on 24-07-2012

@author: staz
'''
from defaultParser import defaultParser
import string
import re

class YahooCompaniesParser( defaultParser ):
  def reset( self ):
    defaultParser.reset( self )
    self.description = ""
    self.sector = ""
    self.companyUrl = ""
    self.industry = ""
    self.endDescription = False
    self.rdDescription = False
    self.canReadDescription = False
    self.id = "yahooCompaniesParser"
    self.addr = "http://finance.yahoo.com/q/pr?s={SYMBOL}"

  def getAddr( self, _symbol ):
    addr = self.addr.replace( '{SYMBOL}', _symbol )
    return addr

  def start_body( self, attrs ):
    self.data = []

  def split( self, _text ):
    x = _text.split( ' - ' )
    z = []
    for y in x:
      w = y.split( '&' )
      for v in w:
        r = v.split( '/' )
        for p in r:
          z.append( p.strip() )
    return z

  def end_body( self ):
    self.description = string.join( self.data, "" )
    m = re.search( "Website:[ ]*(.*)Details", self.description )
    if not m == None:
      self.companyUrl = m.group( 1 )
    m = re.search( "Sector:(.*)Key Statistics", self.description )
    if not m == None:
      self.description = m.group( 0 )
      n = re.search( "Sector:(.*)Industry:(.*)Full Time Employees:(.*)Business Summary(.*)Key Statistics", self.description )
      if not n == None:
        self.sector = self.split( n.group( 1 ) )
        self.industry = self.split( n.group( 2 ) )
        self.description = n.group( 4 )


