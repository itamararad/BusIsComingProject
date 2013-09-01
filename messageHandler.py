# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 21:28:23 2013

@author: Itamar
"""
from position import Position

class CommMessage(object):
    
    def __init__(self, src, commandType, commandData):
        self._src = src
        self._commandType = commandType
        self._commandData = commandData

    @property
    def Source(self):
        return self._src
    
    @property
    def CommandType(self):
        return self._commandType
        
    @property
    def CommandData(self):
        return self._commandData
        
    #def parse(self, message):
    #    self._src, self._commandType, self._commandData = message.split('#')
        
    @classmethod
    def parse(cls, message):
        src, commandType, commandData = message.split('#')
        return cls(src, commandType, commandData)
        
    def toString(self):
        return "%s#%s#%s" % (self._src, self._commandType, self._commandData)
                
        
    
class MessageHandler:
    @classmethod
    def invoke(cls, message):
        commMsg = CommMessage.parse(message)
        
        print "commMsg", commMsg.toString()
        if commMsg.Source.lower() is "bus":
            handler = BusHandler()
            handler.handle(commMsg)
            return handler
            
        
        
        
class BusHandler():
    def __init__(self):
        self._currentPosition = Position()
        
    def handle(self, commMessage):
        print "Handling bus message"        
        
        if commMessage.CommandType.lower() is 'position':
            print "Postion change demand"
            lati, longi = commMessage.CommandData.split(';')
            self._currentPosition = Position(lati, longi)
    
    @property    
    def Position(self):
        return self.currentPosition
    
 