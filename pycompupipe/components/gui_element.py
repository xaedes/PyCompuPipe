#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

import math
from pyecs import *
# from . import Size

class GuiElement(Component):
    """docstring for GuiElement"""
    def __init__(self, position, size, anchor, relative_position = False, snap_to_grid = None, *args,**kwargs):
        super(GuiElement, self).__init__(*args,**kwargs)
        self.position = position
        self.relative_position = relative_position
        self.size = size
        self.anchor = anchor
        self.snap_to_grid = snap_to_grid
        self.manager = None
        self.parent_gui_element = None

    @callback
    def entity_added(self, parent, entity):
        if entity != self.entity: return

        if self.relative_position:
            self.parent_gui_element = self.parent_gui_element or self.entity.find_parent_entity_with_component(GuiElement).get_component(GuiElement)

    def rect(self):
        x,y = self.position

        w,h = self.size
        ax,ay = self.anchor

        if self.relative_position:
            px,py,pw,ph = self.parent_gui_element.rect()
        else:
            px, py = 0,0
        
        i,j = x-ax*w+px, y-ay*h+py

        if self.snap_to_grid is not None:
            i, j = math.floor(i/self.snap_to_grid)*self.snap_to_grid, math.floor(j/self.snap_to_grid)*self.snap_to_grid
            w, h = int(0.5+w/self.snap_to_grid)*self.snap_to_grid, int(0.5+h/self.snap_to_grid)*self.snap_to_grid

        return (i, j, w, h)

    @callback("position")
    def position_pipeline(self, accum):
        x,y,w,h = self.rect()
        return (x,y)

    @callback
    def is_in(self, pos):
        i,j = pos
        x,y,w,h = self.rect()
        result = i >= x and i <= x+w and j >= y and j <= y+h
        return result

    @component_callback
    def register_manager(self, manager):
        self.manager = manager
