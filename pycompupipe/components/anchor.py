#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
from numbers import Number
import math

from pyecs import *
from . import Size

class Anchor(Component):
    """docstring for Anchor"""
    def __init__(self, xy, *args,**kwargs):
        super(Anchor, self).__init__(*args,**kwargs)
        self.x = None
        self.y = None
        self.size = None
        self.set(xy)

    def set(self, xy):
        if isinstance(xy, Number):
            self.x = xy
            self.y = xy
        elif type(xy) == tuple:
            self.x, self.y = xy
        else:
            raise NotImplementedError()

    @component_callback
    @with_components(required=[Size])
    def component_attached(self, size):
        self.size = size

    @callback
    def position(self, accum):
        # if self.size is None: return accum
        x,y = accum
        w,h = self.size.size
        return x - self.x * w, y - self.y * h

    def __str__(self):
        return "%s(%s,%s)" % (
                super(type(self),self).__str__(), 
                self.x, 
                self.y, 
                )
