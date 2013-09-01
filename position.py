# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 21:35:45 2013

@author: Itamar

"""
__doc__ = """
Position class
 
"""
class Position:
    def __init__(self, latitude = 0, longitude = 0 ):
        self.latitude = latitude
        self.longitude = longitude
        
    @property
    def Latitude(self):
        return self.latitude
        
    @property 
    def Longitude(self):
        return self.longitude
        