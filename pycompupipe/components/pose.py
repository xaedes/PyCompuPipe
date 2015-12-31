#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
import math

from pyecs import *

class Pose(Component):
    """docstring for Pose"""
    def __init__(self, x, y, angle=None, *args,**kwargs):
        super(Pose, self).__init__(*args,**kwargs)
        self.x = x
        self.y = y
        self.angle = angle # in degree

    def distance_to(self, pose):
        dx,dy = self.vector_to(pose)
        return math.sqrt(dx*dx+dy*dy)

    def distance_to_xy(self, x, y):
        dx,dy = self.vector_to_xy(x, y)
        return math.sqrt(dx*dx+dy*dy)

    def vector_to(self, pose):
        dx = pose.x - self.x
        dy = pose.y - self.y
        return (dx,dy)
    
    def vector_to_xy(self, x, y):
        dx = x - self.x
        dy = y - self.y
        return (dx,dy)
        
    @callback
    def position(self, accum):
        return self.x, self.y

    def __str__(self):
        params = [self.x,self.y]
        if self.angle is not None:
            params.append(self.angle)
        return "%s(%s)" % (
                super(type(self),self).__str__(), 
                ",".join(map(str,params))
                )
