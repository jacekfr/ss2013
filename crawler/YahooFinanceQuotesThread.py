'''
Created on 24-07-2012

@author: staz
'''

import yql
import datetime
import dateTimeTools
from quotesThread import quotesThread
from sqlalchemy import sql

class YahooFinanceQuotesThread( quotesThread ):
  def __init__( self, _id, _startDate, _endDate, _ui = None, _db = -1, _companies = -1, ):
    quotesThread.__init__( self, _id, _ui )
    self.startDate = dateTimeTools.getYahooDate( _startDate )
    self.endDate = dateTimeTools.getYahooDate( _endDate )
    self.yqlObj = yql.Public()
    self.ui = _ui
    self.db = _db
    if _companies == -1:
      if _db == -1:
        self.process = 0
      else:
        self.companiesList = []
        self.process = 1
        try:
          d = self.db.queryTuples( "SELECT symbol from NEWSA.COMPANIES WHERE 1=1;" )
          for symbol in d:
            self.companiesList.append( symbol[0] )
        except:
          print "ERROR: DB [QUOTES] - Get symbols"
          self.process = 0
    else:
      self.companiesList = _companies

  def createQuery( self, _company ):
    query = 'use "http://www.datatables.org/yahoo/finance/yahoo.finance.historicaldata.xml" as yahoo.finance.quotes;'
    query = query + 'select * from yahoo.finance.quotes where symbol = "' + _company + '" and startDate="' + self.startDate + '" and endDate = "' + self.endDate + '"'
    return query

  def executeQuery( self, _query ):
    result = self.yqlObj.execute( _query )
    return result.rows

  def toDatabase( self, _symbol, _data ):
    d = self.db.queryTuples( "SELECT companyID from NEWSA.COMPANIES WHERE symbol = '" + _symbol + "';" )
    cId = d[0][0]
    sql = "INSERT INTO NEWSA.QUOTESV( companyId, QDate, open, close, low, high, volume, adjClose ) VALUES "
    n = 1
    for __data in _data:
      sql = sql + "(" + str( cId ) + ", '" + __data['date'] + " 00:00:00.0', " + __data['Open'] + ', '
      sql = sql + __data['Close'] + ', ' + __data['Low'] + ', ' + __data['High'] + ', '
      sql = sql + __data['Volume'] + ', ' + __data['Adj_Close'] + ' )'
      if n == _data.__len__():
        sql = sql + ';'
      else:
        sql = sql + ','
      n = n + 1
      if not self.ui == None:
        self.ui.endQuote()
    #print sql
    if _data.__len__() > 1:
      self.db.query( sql )
    return 0

  def run( self ):
    if self.process == 0:
      return
    quotesThread.run( self )
    if not self.ui == None:
      self.ui.setNoOCompanys( self.companiesList.__len__() )
    for company in self.companiesList:
      rows = self.executeQuery( self.createQuery( company ) )
      #print company
      if not self.ui == None:
        self.ui.setNoOQuotes( rows.__len__() )
        self.toDatabase( company, rows )
      #for row in rows:
        #self.toDatabase( company, row )
        #if not self.ui == None:
          #self.ui.endQuote()
      if not self.ui == None:
        self.ui.endCompany()

