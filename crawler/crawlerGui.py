'''
Created on 31-07-2012

@author: staz
'''

import pygtk
import gtk
import crawler
import datetime

class crawlerGui():

  def setNoOQuotes( self, _no ):
    self.number = _no
    self.ended = 0
    self.progress3.set_fraction( 0.0 )
    self.progress3.set_text( "0 / " + str( _no ) )

  def setNoOCompanys( self, _no ):
    self.noCompanys = _no
    self.endedCompanys = 0
    self.progress2.set_fraction( 0.0 )
    self.progress2.set_text( " 0 / " + str( _no ) )

  def endQuote( self ):
    self.ended = self.ended + 1
    frac = float( float( self.ended ) / float( self.number ) )
    self.progress3.set_fraction( frac )
    self.progress3.set_text( str( self.ended ) + " / " + str( self.number ) )

  def endCompany( self ):
    self.endedCompanys = self.endedCompanys + 1
    frac = float( float( self.endedCompanys ) / float( self.noCompanys ) )
    self.progress2.set_fraction( frac )
    self.progress2.set_text( str( self.endedCompanys ) + " / " + str( self.noCompanys ) )

  def endThread( self, _type ):
    type = _type #[TODO]
    self.ended = self.ended + 1
    frac = float( float( self.ended ) / float( self.number ) )
    self.progress3.set_fraction( frac )
    self.progress3.set_text( str( self.ended ) + " / " + str( self.number ) )

  def setNoONews( self, _no ):
    self.number = _no
    self.ended = 0
    self.progress3.set_fraction( 0.0 )
    self.progress3.set_text( "0 / " + str( _no ) )

  def setService( self, widget, data = None ):
    if data in self.services:
      self.services.remove( data )
    else:
      self.services.append( data )

  def toDate( self, _tuple ):
    d = _tuple[2]
    m = _tuple[1] + 1
    y = _tuple[0]
    return datetime.date( day = d, month = m, year = y )

  def start( self, widget, data = None ):
    sdate = self.toDate( self.calendar1.get_date() )
    edate = self.toDate( self.calendar2.get_date() )

    for service in self.services:
      cThread = crawler.getThread( [], service, sdate, edate, self, crawler.getNewDBHnd() )
      cThread.start()
      #cThread.join()

  def deleteEvent( self, widget, event, data = None ):
    print "delete event"

  def destroy( self, widget, data = None ):
    gtk.main_quit()

  def __init__( self ):
    self.services = []
    gtk.gdk.threads_init()
    self.number = 0;
    self.ended = 0;
    self.window = gtk.Window( gtk.WINDOW_TOPLEVEL )
    self.window.connect( "delete_event", self.deleteEvent )
    self.window.connect( "destroy", self.destroy )
    self.window.set_border_width( 10 )
    vbox = gtk.VBox( True, 1 )
    buttons = []
    buttons.append( gtk.ToggleButton( "Reuters" ) )
    buttons.append( gtk.ToggleButton( "Reuters Mobile" ) )
    buttons.append( gtk.ToggleButton( "Bloomberg" ) )
    buttons.append( gtk.ToggleButton( "Bloomberg Mobile" ) )
    buttons.append( gtk.ToggleButton( "Yahoo! Finance - Companies" ) )
    buttons.append( gtk.ToggleButton( "Yahoo! Finance - Quotes" ) )
    buttons[0].connect( "toggled", self.setService, "reuters" )
    buttons[1].connect( "toggled", self.setService, "reutersM" )
    buttons[2].connect( "toggled", self.setService, "bloomberg" )
    buttons[3].connect( "toggled", self.setService, "bloombergM" )
    buttons[4].connect( "toggled", self.setService, "yahooCompanies" )
    buttons[5].connect( "toggled", self.setService, "yahooQuotes" )

    for button in buttons:
      vbox.pack_start( button, True, True, 1 )
      button.show()

    frame1 = gtk.Frame( "Data poczatkowa" )
    frame2 = gtk.Frame( "Data koncowa" )
    self.calendar1 = gtk.Calendar()
    self.calendar2 = gtk.Calendar()
    frame1.add( self.calendar1 )
    frame2.add( self.calendar2 )

    hbox = gtk.HBox( True, 1 )
    #self.window.add( hbox )
    hbox.pack_start( vbox, True, True, 1 )
    hbox.pack_start( frame1, True, True, 1 )
    hbox.pack_start( frame2, True, True, 1 )

    self.calendar1.show()
    self.calendar2.show()

    frame1.show()
    frame2.show()
    hbox.show()
    vbox.show()

    hbox2 = gtk.HBox( True, 1 )
    vbox2 = gtk.VBox( True, 1 )

    #self.window.add( vbox2 )

    self.progress1 = gtk.ProgressBar()
    self.progress2 = gtk.ProgressBar()
    self.progress3 = gtk.ProgressBar()

    vbox2.pack_start( self.progress1 )
    vbox2.pack_start( self.progress2 )
    vbox2.pack_start( self.progress3 )
    self.startButton = gtk.Button( "Rozpocznij przetwarzanie" )
    self.startButton.connect( "clicked", self.start )
    vbox2.pack_start( self.startButton )
    self.startButton.show()

    self.progress1.show()
    self.progress2.show()
    self.progress3.show()

    vbox2.show()

    vbox3 = gtk.VBox( True, 1 )
    self.window.add( vbox3 )
    vbox3.pack_start( hbox )
    vbox3.pack_start( vbox2 )
    vbox3.show()

    self.window.show()

  def main( self ):
    gtk.main()

if __name__ == "__main__":
  x = crawlerGui()
  x.main()
