# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 22:29:04 2013

@author: Itamar
"""
import xml.etree.ElementTree as ET
#import ElementTree as ET


class GPXParser:
    def __init__(self, gpx_filename):
        self._filename = gpx_filename
        self._routeList = []
        
        try:
            # Parse
            tree = ET.parse(open(gpx_filename, "r"))            
            root = tree.getroot()
            gpx = root[0]
            
            for item in gpx:
                if (item.tag == "{http://www.topografix.com/GPX/1/1}rtept"):
                    self._routeList.append(item.attrib)
                
            
        except Exception as inst:
            print inst
            raise
        
        
    def getRouteList(self):
        return self._routeList
        
        
        
if __name__ == "__main__":
    gpxParser = GPXParser('route.gpx')
    for item in gpxParser.getRouteList():
        print item
    
        