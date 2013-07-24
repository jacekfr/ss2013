'''
Created on 24-07-2012

@author: staz
'''

import sys
import yql
import time
from quotesThread import quotesThread
from YahooCompaniesParser import YahooCompaniesParser
from companyStruct import companyStruct
from YahooIndustryindexParser import YahooIndustryindexParser
from YahooCompaniesParserThread import YahooCompaniesParserThread
from YahooCompaniesHoldersParser import YahooCompaniesHoldersParser

class YahooCompaniesThread( quotesThread ):
  def __init__( self, _id, _fileName, _ui = None, _db = -1 ):
    quotesThread.__init__( self, _id, _ui )
    self.yqlObj = yql.Public()
    self.ui = _ui
    self.fileName = 'xmls/' + _fileName + '.xml'
    if _db == -1:
      self.fileHnd = open( self.fileName, 'w+' )
    else:
      self.fileHnd = -1
    self.id = _id
    self.db = _db

  def createQuery( self, _id ):
    query = 'use "http://www.datatables.org/yahoo/finance/yahoo.finance.industry.xml" as yahoo.finance.industry;'
    query = query + 'select * from yahoo.finance.industry where id="' + str( _id ) + '"'
    return query

  def executeQuery( self, _query ):
    result = self.yqlObj.execute( _query )
    return result.rows

  def run( self ):
    quotesThread.run( self )
    if self.db == -1:
      self.fileHnd.write( "<companies>\n" )
    companies = []
    print 'Tworzenie listy indeksow'
    yP = YahooIndustryindexParser()
    yP.parsePageSource( yP.getAddrE() )
    print 'Znaleziono ' + str( yP.getIndicesList().__len__() ) + ' indeksow'
    print 'Tworzenie listy spolek'
    for i in yP.getIndicesList():
      rows = self.executeQuery( self.createQuery( i ) )
      if rows.__len__() > 0:
        if not rows[0].get( "company" ) == None:
          for row in rows[0].get( "company" ):
            try:
              tmpSymbol = row.get( "symbol" )
              tmpName = row.get( "name" )
              company = companyStruct()
              company.setName( tmpName )
              company.setSymbol( tmpSymbol )
              companies.append( company )
            except:
              continue
    self.count = companies.__len__()
    print 'Znaleziono ' + str( companies.__len__() ) + ' spolek'
    print 'Poczatek przetwarzania spolek'
    print 'Pobieranie podstawowych danych'
    threads = []
    if not self.ui == None:
      self.ui.setNoONews( self.count )
    for company in companies:
      nxt = True
      while nxt:
        #try:
          time.sleep( 0.4 )
          cParser = YahooCompaniesParser()
          hParser = YahooCompaniesHoldersParser()
          pThread = YahooCompaniesParserThread( self.id, self.fileHnd, cParser, hParser, company, threads.__len__(), self.count, self.ui, self.db )
          pThread.start()
          threads.append( pThread )
          nxt = False
        #except:
          #msg = 'Nie udalo sie utworzyc watku [ ' + self.id + ' ' + str( threads.__len__() ) + ' / ' + str( self.count ) + ' ]' + "\n"
          #sys.stderr.write( msg )
          #nxt = True
    for thread in threads:
        thread.join( 1.0 )
    print 'Koniec przetwarzania spolek'
    if self.db == -1:
      self.fileHnd.write( "</companies>\n" )
      self.fileHnd.close()
