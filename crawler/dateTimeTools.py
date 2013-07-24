'''
Created on 17-07-2012

@author: pogoma
'''

import datetime

def dayToString( _date ):
  dayS = str( _date.day )
  if dayS.__len__() == 1:
    dayS = '0' + dayS
  return dayS

def monthToString( _date ):
  monthS = str( _date.month )
  if monthS.__len__() == 1:
    monthS = '0' + monthS
  return monthS

def yearToString( _date ):
  yearS = str( _date.year )
  return yearS

def getYahooDate( _date ):
  year = yearToString( _date )
  month = monthToString( _date )
  day = dayToString( _date )
  d = year + '-' + month + '-' + day
  return d
