'''
Created on 25-07-2012

@author: staz
'''

from defaultParser import defaultParser
import re

class YahooIndustryindexParser( defaultParser ):
  def reset( self ):
    defaultParser.reset( self )
    self.id = 'yahooIndustryindex'
    self.addr = 'http://biz.yahoo.com/ic/ind_index.html'

  def getIndicesList( self ):
    iList = []
    for addr in self.addrs:
      if addr[0].find( '/finance/industry/industryindex/' ) >= 0:
        m = re.search( "http://biz.yahoo.com/ic/([0-9]+)\.html", addr[0] )
        if not m == None:
          if not m.group( 1 ) == None and not m.group( 1 ) == "":
            iList.append( m.group( 1 ) )
    return iList
