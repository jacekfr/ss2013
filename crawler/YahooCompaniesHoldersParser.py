'''
Created on 25-07-2012

@author: staz
'''

from defaultParser import defaultParser

class YahooCompaniesHoldersParser( defaultParser ):
  def reset( self ):
    defaultParser.reset( self )
    self.id = 'yahooCompaniesHoldersParser'
    self.addr = 'http://finance.yahoo.com/q/ir?s={SYMBOL}'

  def getAddr( self, _symbol ):
    addr = self.addr.replace( '{SYMBOL}', _symbol )
    return addr

  def getHoldersList( self ):
    hList = []
    for addr in self.addrs:
      if addr[0].find( 'http://biz.yahoo.com/t/' ) >= 0:
        hList.append( addr[1] )
    return hList
