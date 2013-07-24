'''
Created on 17-07-2012

@author: pogoma
'''

import re

class newsStruct( object ):

  def __init__( self ):
    self.time = ""
    self.title = ""
    self.content = ""
    self.url = ""
    self.categeries = []

  def removeChars( self, _text ):
    _text = _text.strip()
    _text = _text.strip().replace( '&', "" ).replace( '\n', "" )
    _text = _text.replace( '"', "'" )
    _text = re.sub( '<.*>', '', _text )
    _text = re.sub( '[<|>][<|>]', '', _text )
    self.content = re.sub( "[\r]+", " ", self.content )
    return _text

  def setUrl( self, _url ):
    self.url = _url

  def getUrl( self ):
    return self.url

  def setTime( self, _time ):
    self.time = _time

  def setTitle( self, _title ):
    self.title = self.removeChars( _title )

  def setContent( self, _content ):
    self.content = self.removeChars( _content )

  def getTime( self ):
    return self.time

  def getTitle( self ):
    return self.title

  def getContent( self ):
    return self.content

  def addCategory( self, _category ):
    self.categeries.append( self.removeChars( _category ) )

  def getCategories( self ):
    return self.categeries

  def getXML( self ):
    XMLt = ""
    XMLt = XMLt + '<article title="' + self.getTitle() + '" '
    XMLt = XMLt + 'time="' + self.getTime() + '" url="' + self.getUrl() + '">' + "\n"
    XMLt = XMLt + "<text>\n" + self.getContent()
    XMLt = XMLt + "\n</text>\n</article>\n"
    return XMLt
