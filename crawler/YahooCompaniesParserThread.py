'''
Created on 25-07-2012

@author: staz
'''

import time
import threading
from companyStruct import companyStruct

class YahooCompaniesParserThread( threading.Thread ):
  def __init__( self, _threadType, _fileHnd, _parserC, _parserH, _company, _i, _n, _ui = None, _db = -1 ):
    threading.Thread.__init__( self )
    self.threadType = _threadType
    self.ui = _ui
    self.fileHnd = _fileHnd
    self.parserC = _parserC
    self.parserH = _parserH
    self.company = _company
    self.db = _db
    self.n = _n
    self.i = _i

  def run( self ):
    start = time.clock()
    print 'Watek [ ' + self.threadType + ' ' + str( self.i ) + ' / ' + str( self.n ) + ' ] zaczyna dzialanie ( ' + str( start ) + 's. )' + "\n     [ " + self.company.getName() + ' ]'
    self.getCompany()
    if self.parserC.industry.__len__() > 0 and self.parserC.sector.__len__() > 0:
      if self.db == -1:
        self.fileHnd.write( self.company.getXML() )
      else:
        self.company.toDatabase( self.db )
    print 'Watek [ ' + self.threadType + ' ' + str( self.i ) + ' / ' + str( self.n ) + ' ] konczy dzialanie ( ' + str( time.clock() - start ) + 's. )'
    if not self.ui == None:
      self.ui.endThread( self.threadType )

  def getCompany( self ):
    self.parserC.parsePageSource( self.parserC.getAddr( self.company.getSymbol() ) )
    self.company.setDescription( self.parserC.description )
    self.company.setUrl( self.parserC.companyUrl )
    for industry in self.parserC.industry:
      self.company.addIndustry( industry )
    for sector in self.parserC.sector:
      self.company.addSector( sector )
    self.parserH.parsePageSource( self.parserH.getAddr( self.company.getSymbol() ) )
    if not self.parserH.getHoldersList() == None and self.parserH.getHoldersList().__len__() > 0:
      for holder in self.parserH.getHoldersList():
        self.company.addHolder( holder )

