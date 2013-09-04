#!/usr/bin/python

'''
from websocket import create_connection
ws = create_connection("ws://localhost:8888/ws")
print "Sending 'Hello, World'..."
ws.send("Hello, World")
print "Sent"
print "Reeiving..."
result =  ws.recv()
print "Received '%s'" % result
ws.close()
'''

import time
from websocket import create_connection
from position import *
from messageHandler import CommMessage
from gpx_parser import GPXParser


class BusSideClient(object):
    def __init__(self, host):
        
        self.running = False

        self.client = create_connection(host)
        
        gpxParser = GPXParser('route.gpx')
        self.route = gpxParser.getRouteList()
        
        self.currentLocationIdx = 0

        
    def run(self):
        try:
            self.running = True
            
            while self.running:
                
                nextRouteIdx = lambda idx : ( idx + 1 ) % len(self.route)
                
                currentLocation = self.route[self.currentLocationIdx] 
                self.currentLocationIdx = nextRouteIdx (self.currentLocationIdx)
                
                position = ([float(currentLocation['lat']), float(currentLocation['lon'])])
                
                print 'Current Position', currentLocation
                
                positionMessage = '%.15f;%.15f' % (position[0], position[1])
                message = CommMessage('BUS', "0", 'Position', positionMessage)
                
                self.client.send(message.toString())

                time.sleep(3)
                
        finally:
            self.terminate()
            
            
    def terminate(self):
        self.running = False


if __name__ == '__main__':
    aps = BusSideClient(host='ws://localhost:8888/ws')
    try:
        aps.run()
    except KeyboardInterrupt:
        aps.terminate()