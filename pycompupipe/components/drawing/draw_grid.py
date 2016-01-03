#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
from numbers import Number
import math

from pyecs import *

class DrawGrid(Component):
    """docstring for DrawGrid"""
    def __init__(self, draw_event_name, resolution, color=(0,0,0), *args,**kwargs):
        super(DrawGrid, self).__init__(*args,**kwargs)
        self.draw_event_name = draw_event_name
        self.resolution = resolution
        self.color = color

    @component_callback
    def component_attached(self):
        self.entity.register_callback(self.draw_event_name, self.draw)

    def draw(self, screen):
        w = int(math.floor(screen.get_width() / self.resolution))
        h = int(math.floor(screen.get_height() / self.resolution))
        for x in xrange(w):
            for y in xrange(h):
                screen.set_at((x*self.resolution,y*self.resolution),self.color)
                