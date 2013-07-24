'''
Created on 17-07-2012

@author: pogoma
'''

import dateTimeTools
import threading
import time
import datetime

from defaultParser import defaultParser
from ReutersParser import ReutersParser
from parserThread import parserThread
from BloombergParser import BloombergParser
from ReutersMobileParser import ReutersMobileParser
import sys
from BloombergMobileParser import BloombergMobileParser

class crawlerThread( threading.Thread ):
  def __init__( self, _type, _startDate, _endDate, _ui = None ):
    self.type = _type
    self.ui = _ui
    self.startDate = _startDate
    self.endDate = _endDate
    self.count = 0;
    threading.Thread.__init__( self )

  def run( self ):
    start = time.clock()
    cDate = self.startDate
    days = self.endDate - self.startDate
    for interval in range( days.days + 1 ):
      td = datetime.timedelta( interval )
      cDate = self.startDate + td
      self.day = dateTimeTools.dayToString( cDate )
      self.month = dateTimeTools.monthToString( cDate )
      self.year = dateTimeTools.yearToString( cDate )
      self.fileName = 'xmls/' + self.type + '_' + self.day + '_' + self.month + '_' + self.year + '.xml'
      self.fileHnd = open( self.fileName, 'w+' )
      self.fileHnd.write( "<articles>\n" )
      hParser = self.createParser()
      print 'Stworzono obiekt parsera typu: ' + self.type
      print 'Wyciagnieto adres strony: ' + hParser.getAddr( self.day, self.month, self.year )
      hParser.parsePageSource( hParser.getAddr( self.day, self.month, self.year ) )
      self.count = hParser.getAddrList().__len__()
      if not self.ui == None:
        self.ui.setNoONews( self.count )
      print 'Ilosc adresow: ' + str( self.count )
      threads = []
      for url in hParser.getAddrList():
        nxt = True
        while nxt:
          try:
            time.sleep( 0.15 )
            pParser = self.createParser()
            pThread = parserThread( self.type, self.fileHnd, url, pParser, threads.__len__() + 1, self.count, self.ui )
            threads.append( pThread )
            pThread.start()
            nxt = False
          except:
            msg = 'Nie udalo sie utworzyc watku [ ' + self.type + ' ' + str( threads.__len__() ) + ' / ' + str( self.count ) + ' ]' + "\n"
            sys.stderr.write( msg )
            threads.remove( pThread )
            pThread.terminate()
            time.sleep( 0.5 )
            nxt = True
      print 'Utworzono wszystkie watki'
      print 'Oczekiwanie na zakonczenie'
      time.sleep( 5 )
      for thread in threads:
        try:
          print 'Oczekiwanie na zakonczenie watku: ' + str( thread.getI() )
          thread.join( 1.0 )
          thread.terminate()
        except:
          continue
      threads = []
      self.fileHnd.write( "\n</articles>" )
      self.fileHnd.close()
      print 'Watek [ ' + self.type + ' ' + self.day + '-' + self.month + '-' + self.year + ' ] konczy dzialanie. ( ' + str( time.clock() - start ) + 's. )'

  def createParser( self ):
    try:
      result = {

        'default'    : defaultParser(),
        'reuters'    : ReutersParser(),
        'bloomberg'  : BloombergParser(),
        'reutersM'   : ReutersMobileParser(),
        'bloombergM' : BloombergMobileParser()

      }[self.type]
    except:
      result = defaultParser()
    return result
