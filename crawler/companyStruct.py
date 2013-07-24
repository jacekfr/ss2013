'''
Created on 24-07-2012

@author: staz
'''

import re
import databaseConn
from mimetypes import _db

class companyStruct():
  def __init__( self ):
    self.name = ""
    self.symbol = ""
    self.description = ""
    self.sectors = []
    self.industries = []
    self.holders = []
    self.url = ""

  def clean( self, _text ):
    _text = re.sub( u"[\x7f-\xff]", u"", _text )
    _text = re.sub( u"[\u0092-\uffff]*", u"", _text )
    _text = re.sub( u"\ufffd", u"", _text )
    _text = _text.replace( u'&', 'and' )
    _text = _text.replace( u'"', "'" )
    _text = _text.encode( "ascii", "ignore" )
    return _text

  def cleanDatabase( self, _text ):
    _text = _text.strip()
    _text = _text.replace( "`", "'" )
    return _text

  def encDatabase( self, _text ):
    _text = _text.replace( "&amp", "'" )
    return _text

  def setName( self, _name ):
    self.name = _name

  def getName( self ):
    return self.name

  def setUrl( self, _url ):
    self.url = _url

  def getUrl( self ):
    return self.url

  def setSymbol( self, _symbol ):
    self.symbol = _symbol

  def getSymbol( self ):
    return self.symbol

  def setDescription( self, _description ):
    self.description = _description

  def getDescription( self ):
    return self.description

  def addIndustry( self, _industry ):
    self.industries.append( _industry )

  def addSector( self, _sector ):
    self.sectors.append( _sector )

  def addHolder( self, _holder ):
    self.holders.append( _holder )

  def toDatabase( self, _db ):
    sql = "INSERT INTO NEWSA.COMPANIESV ( name, url, symbol, description ) VALUES "
    sql = sql + "('" + self.cleanDatabase( self.getName() ) + "', "
    sql = sql + "'" + self.cleanDatabase( self.getUrl() ) + "', "
    sql = sql + "'" + self.cleanDatabase( self.getSymbol() ) + "', "
    sql = sql + "'" + self.cleanDatabase( self.getDescription() ) + "')"
    _db.query( sql )
    d = _db.queryTuples( "SELECT companyID from NEWSA.COMPANIES WHERE symbol = '" + self.getSymbol() + "';" )
    cId = d[0][0]
    for sector in self.sectors:
      try:
        sql = "INSERT INTO NEWSA.SECTORSV( name ) VALUES (' " + self.cleanDatabase( sector ) + "' );"
        _db.query( sql )
        sql = "SELECT sectorID from NEWSA.SECTORS WHERE name LIKE '%" + sector + "%';"
        d = _db.queryTuples( sql )
        sectId = d[0][0]
        sql = "INSERT INTO NEWSA.COMPANIESSECTORS (companyId, sectorId) VALUES ( " + str( cId ) + ", " + str( sectId ) + " );"
        _db.query( sql )
      except:
        print "WARNING: DB [SECTORS] - " + sector
    for industry in self.industries:
      try:
        sql = "INSERT INTO NEWSA.INDUSTRIESV( name ) VALUES (' " + self.cleanDatabase( industry ) + "' );"
        _db.query( sql )
        sql = "SELECT industryID from NEWSA.INDUSTRIES WHERE name LIKE '%" + industry + "%';"
        d = _db.queryTuples( sql )
        indId = d[0][0]
        sql = "INSERT INTO NEWSA.COMPANIESINDUSTRIES (companyId, industryId) VALUES ( " + str( cId ) + ", " + str( indId ) + " );"
        _db.query( sql )
      except:
        print "WARNING: DB [INDUSTRIES] - " + industry
    for holder in self.holders:
      try:
        sql = "INSERT INTO NEWSA.HOLDERSV( name ) VALUES (' " + self.cleanDatabase( holder ) + "' );"
        _db.query( sql )
        sql = "SELECT holderID from NEWSA.HOLDERS WHERE name LIKE '%" + holder + "%';"
        d = _db.queryTuples( sql )
        holdId = d[0][0]
        sql = "INSERT INTO NEWSA.COMPANIESHOLDERS (companyId, holderId) VALUES ( " + str( cId ) + ", " + str( holdId ) + " );"
        _db.query( sql )
      except:
        print "WARNING: DB [HOLDERS] - " + holder
  def getXML( self ):
    XMLt = "\n"
    XMLt = XMLt + '<company name="' + self.clean( self.getName() ) + '" '
    XMLt = XMLt + 'symbol="' + self.clean( self.getSymbol() ) + '" >' + "\n"
    XMLt = XMLt + "<info>\n"
    XMLt = XMLt + "<sectors>\n"
    for sector in self.sectors:
      XMLt = XMLt + "<sector>" + self.clean( sector ) + "</sector>\n"
    XMLt = XMLt + "</sectors>\n"
    XMLt = XMLt + "<industries>\n"
    for industry in self.industries:
      XMLt = XMLt + "<industry>" + self.clean( industry ) + "</industry>\n"
    XMLt = XMLt + "</industries>\n"
    XMLt = XMLt + "<holders>\n"
    for holder in self.holders:
      XMLt = XMLt + "<holder>" + self.clean( holder ) + "</holder>\n"
    XMLt = XMLt + "</holders>\n"
    XMLt = XMLt + "</info>\n"
    XMLt = XMLt + "<description>\n" + self.clean( self.getDescription() ) + "\n</description>\n"
    XMLt = XMLt + "</company>\n"
    return XMLt
