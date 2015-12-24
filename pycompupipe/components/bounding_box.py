#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
from numbers import Number

import pygame

from pyecs import *
# from pyecs.components import *
from . import Pose,Size

class BoundingBox(Component):
    """docstring for BoundingBox"""
    def __init__(self, *args,**kwargs):
        super(BoundingBox, self).__init__(*args,**kwargs)
        # self.pose = None
        # self.size = None

    @callback
    @with_components(required=[Pose,Size])
    def awake(self,pose,size):
        self.pose = pose
        self.size = size

    def rect(self):
        x,y = self.entity.fire_callbacks_pipeline("position")
        return (x, y, self.size.size[0], self.size.size[1])

    @callback
    def is_in(self, pos):
        i,j = pos
        x,y,w,h = self.rect()
        result = i >= x and i <= x+w and j >= y and j <= y+h
        return result
