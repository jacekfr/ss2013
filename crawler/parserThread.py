'''
Created on 17-07-2012

@author: pogoma
'''

import threading
import time
from newsStruct import newsStruct
from defaultParser import defaultParser

class parserThread( threading.Thread ):
  def __init__( self, _threadType, _fileHnd, _url, _parser, _i, _n, _ui = None ):
    threading.Thread.__init__( self )
    self.ui = _ui
    self.threadType = _threadType
    self.fileHnd = _fileHnd
    self.url = _url
    self.parser = _parser
    self.news = newsStruct()
    self.n = _n
    self.i = _i
    self.stop = False

  def terminate( self ):
    self.stop = True

  def getI( self ):
    return self.i

  def run( self ):
    start = time.clock()
    print 'Watek [ ' + self.threadType + ' ' + str( self.i ) + ' / ' + str( self.n ) + ' ] zaczyna dzialanie ( ' + str( start ) + 's. )'
    self.getNews()
    if self.stop :
      return
    self.fileHnd.write( self.news.getXML() )
    print 'Watek [ ' + self.threadType + ' ' + str( self.i ) + ' / ' + str( self.n ) + ' ] konczy dzialanie ( ' + str( time.clock() - start ) + 's. )'
    if not self.ui == None:
      self.ui.endThread( self.threadType )

  def getNews( self ):
    self.parser.parsePageSource( self.url )
    if self.stop:
      return
    self.news.setContent( self.parser.content )
    self.news.setTime( self.parser.timestamp )
    self.news.setTitle( self.parser.title )
    self.news.setUrl( self.url )
    for cat in self.parser.categories:
      self.news.addCategory( cat )


