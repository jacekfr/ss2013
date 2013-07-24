'''
Created on 08-08-2012

@author: staz
'''

import ibm_db

class databaseConn():
  def __init__( self, _uid, _pass, _database, _host = 'localhost', _port = '50000' ):
    self.host = _host
    self.port = _port
    self.userId = _uid
    self.password = _pass
    self.database = _database

    db = "DATABASE=" + _database + ";HOSTNAME=" + _host + ";PORT=" + _port + ";UID=" + _uid + ";PWD=" + _pass

    self.connection = ibm_db.connect( db, _uid, _pass )

  def query( self, _sql ):
    stmt = ibm_db.exec_immediate( self.connection, _sql )
    return stmt

  def queryTuples( self, _sql ):
    stmt = ibm_db.exec_immediate( self.connection, _sql )
    tuples = []
    tup = ibm_db.fetch_tuple( stmt )
    while tup != False:
      tuples.append( tup )
      tup = ibm_db.fetch_tuple( stmt )
    return tuples

  def queryDict( self, _sql ):
    stmt = ibm_db.exec_immediate( self.connection, _sql )
    dictionary = []
    item = ibm_db.fetch_assoc( stmt )
    while item != False:
      dictionary.append( item )
      item = ibm_db.fetch_tuple( stmt )
    return dictionary


