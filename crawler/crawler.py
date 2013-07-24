'''
Created on 17-07-2012

@author: pogoma
'''

import re
import sys
import getopt
import datetime
from databaseConn import databaseConn
from crawlerThread import crawlerThread
from YahooCompaniesThread import YahooCompaniesThread
from YahooFinanceQuotesThread import YahooFinanceQuotesThread

def printUsage( argv ):
  print ""
  print "Usage: " + argv[0] + " --service=[SERWIS] [PRZEDZIAL_CZASU]"
  print ""
  print "Format daty: [dzien]-[miesiac]-[rok] (dd-mm-yyyy)"
  print ""
  print "Parametry:"
  print ""
  print "   Dane tylko z jednego dnia:"
  print "   --sdate=[dd-mm-rrrr]"
  print "   lub:"
  print "   --date=[dd-mm-rrrr]"
  print ""
  print "   Dane z przedzialu czasu:"
  print "   --sdate=[dd-mm-rrrr] data poczatkowa"
  print "   --edate=[dd-mm-rrrr] data koncowa"
  print ""
  print "Dostepne serwisy:"
  print "reuters        - Agencja Reutersa - reuters.com"
  print "reutersM       - Agencja Reutersa (serwis mobilny) - mobile.reuters.com"
  print "bloomberg      - Serwis Bloomberg - bloomberg.com"
  print "bloombergM     - Serwis Bloomberg (serwis mobilny)- mobile.bloomberg.com"
  print "yahooCompanies - dane o spolkach z serwisu Yahoo! Finance - finance.yahoo.com"
  print "yahooQuotes    - notowania historyczne spolek z serwisu Yahoo! Finance - finance.yahoo.com"
  print ""

def getThread( argv, _type, _sdate, _edate, _ui = None, _db = -1 ):
  types = ( "bloomberg", "bloombergM", "reuters", "reutersM", "yahooCompanies", "yahooQuotes" )

  thread = None
  if _type in types:
    thread = {

        'default'        : None,
        'reuters'        : crawlerThread( _type, _sdate, _edate, _ui ),
        'bloomberg'      : crawlerThread( _type, _sdate, _edate, _ui ),
        'reutersM'       : crawlerThread( _type, _sdate, _edate, _ui ),
        'bloombergM'     : crawlerThread( _type, _sdate, _edate, _ui ),
        'yahooCompanies' : YahooCompaniesThread( "yahooCompanies", "yahooCompanies", _ui, _db ),
        'yahooQuotes'    : YahooFinanceQuotesThread( _type, _sdate, _edate, _ui, _db )

      }[_type]

    return thread
  else:
    printUsage( argv )
    sys.exit( 2 )

def run( argv ):
  service = -1
  datetype = -1

  sd = -1
  sm = -1
  sy = -1
  ed = -1
  em = -1
  ey = -1

  sdate = -1
  edate = -1

  try:
    opts, args = getopt.getopt( argv[1:], "", ["help", "service=", "date=", "sdate=", "edate="] )
  except:
    printUsage( argv )
    sys.exit( 2 )

  for opt, arg in opts:
    if opt == "--help":
      printUsage( argv )

    if opt == "--service":
      service = arg

    if opt in ( "--date", "--sdate" ):
      datetype = 1
      m = re.search( "([0-9]{1,2})-([0-9]{1,2})-([0-9]{4})", arg )
      if not m == None:
        sd = int( m.group( 1 ) )
        sm = int( m.group( 2 ) )
        sy = int( m.group( 3 ) )

    if opt == "--edate":
      datetype = 1
      m = re.search( "([0-9]{1,2})-([0-9]{1,2})-([0-9]{4})", arg )
      if not m == None:
        ed = int( m.group( 1 ) )
        em = int( m.group( 2 ) )
        ey = int( m.group( 3 ) )

  if ed == -1 or em == -1 or ey == -1:
    ed = sd
    em = sm
    ey = sy

  try:
    sdate = datetime.date( day = sd, month = sm, year = sy )
    edate = datetime.date( day = ed, month = em, year = ey )

  except:
    printUsage( argv )
    sys.exit( 2 )


  if service == -1 or datetype == -1:
    printUsage( argv )
    sys.exit( 2 )

  cThread = getThread( argv, service, sdate, edate )
  cThread.start()

def getNewDBHnd():
  dbHnd = databaseConn( 'staz', 'adadadad', 'staz' )
  return dbHnd

if __name__ == "__main__":
  addr = run( sys.argv )

