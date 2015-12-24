#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
from numbers import Number
import math

from pyecs import *

class SnapToGrid(Component):
    """docstring for SnapToGrid"""
    def __init__(self, grid_size, *args,**kwargs):
        super(SnapToGrid, self).__init__(*args,**kwargs)
        self.grid_size = grid_size

    @callback
    def position(self, accum):
        x,y = accum
        x = int(math.floor(x / self.grid_size))*self.grid_size
        y = int(math.floor(y / self.grid_size))*self.grid_size
        return x,y                