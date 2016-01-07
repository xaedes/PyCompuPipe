#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
from __future__ import absolute_import

import math
from pyecs import *
# from . import Size

from funcy import partial

class GuiElement(Component):
    """docstring for GuiElement"""
    def __init__(self, position=(0,0), size=(0,0), anchor=(0,0), relative_position = False, snap_to_grid = None, *args,**kwargs):
        super(GuiElement, self).__init__(*args,**kwargs)
        self.position = position
        self.relative_position = relative_position
        self.size = size
        self.anchor = anchor
        self.snap_to_grid = snap_to_grid
        self.manager = None
        self.parent_gui_element = None
        self._always_fetch_mouse = False
        self.mouse_callbacks = []
        self.mouse_callbacks.append(("mousemotion",partial(self.mouse_callback, "mousemotion")))
        self.mouse_callbacks.append(("mousebuttonup",partial(self.mouse_callback, "mousebuttonup")))
        self.mouse_callbacks.append(("mousebuttondown",partial(self.mouse_callback, "mousebuttondown")))

    @property
    def always_fetch_mouse(self):
        return self._always_fetch_mouse

    @always_fetch_mouse.setter
    def always_fetch_mouse(self, value):
        self._always_fetch_mouse = value
        if self._always_fetch_mouse:
            for key,callback in self.mouse_callbacks:        
                self.manager.entity.register_callback(key,callback)
        else:
            for key,callback in self.mouse_callbacks:        
                self.manager.entity.remove_callback(key,callback)

    def mouse_callback(self, key, event):
        self.entity.fire_callbacks(key, event)

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
    def position_pipeline(self, inner_anchor):
        if inner_anchor is None:
            inner_anchor = (0,0)
        
        x,y,w,h = self.rect()

        return (x+inner_anchor[0]*w,y+inner_anchor[1]*h)

    @callback
    def is_in(self, pos):
        i,j = pos
        x,y,w,h = self.rect()
        result = i >= x and i <= x+w and j >= y and j <= y+h
        return result

    @component_callback
    def register_manager(self, manager):
        self.manager = manager
