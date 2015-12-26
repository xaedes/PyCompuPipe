#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
from numbers import Number
import math

from pyecs import *
from . import BoundingBox


class OccupyingBoundingBox(Component):
    """docstring for OccupyingBoundingBox"""
    def __init__(self, *args,**kwargs):
        super(OccupyingBoundingBox, self).__init__(*args,**kwargs)
        self.bbox = None

    @component_callback
    @with_components(required=[BoundingBox])
    def component_attached(self, boundingbox):
        self.bbox = boundingbox
        
    @callback
    def update_occupancy(self, grid):
        grid.occupy_block(self.bbox.rect())
