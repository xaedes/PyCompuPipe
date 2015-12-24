#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
import math

from pyecs import *
# from pyecs.components import *
from . import Pose

class Size(Component):
    """docstring for Size"""
    def __init__(self, size, *args,**kwargs):
        super(Size, self).__init__(*args,**kwargs)
        self.size = size

    # def bounding_radius(self):
    #     ((mx,my),r) = self.bounding_circle()
    #     return r

    # def bounding_circle(self):
    #     # get bounding box
    #     bbox = self.bounding_box()
    #     x,y,w,h = bbox
    #     w2,h2 = w/2,h/2
    #     # center of bounding box
    #     mx,my = x+w2,y+h2
    #     # radius of enclosing circle is distance from
    #      # center to any of the corner points of the bbox
    #     r = math.sqrt(w2*w2+h2*h2)
        
    #     return ((mx,my),r)

    def __str__(self):
        return "%s(%s)" % (
                super(type(self),self).__str__(), 
                self.size, 
                )
