#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

import numpy as np
from scipy.spatial import cKDTree

from pyecs import *
from . import GuiElement

from funcy import partial

class GuiManager(Component):
    """docstring for GuiManager"""
    def __init__(self, *args,**kwargs):
        super(GuiManager, self).__init__(*args,**kwargs)
        self.tree = None

    @callback
    def awake(self):
        for gui_element in Component.__added_components__[GuiElement]:
            gui_element.fire_callbacks("register_manager", self)

        self._build_tree()
        self.entity.register_callback("mousemotion",partial(self.mouse_callback, "mousemotion"))
        self.entity.register_callback("mousebuttonup",partial(self.mouse_callback, "mousebuttonup"))
        self.entity.register_callback("mousebuttondown",partial(self.mouse_callback, "mousebuttondown"))

    def _build_tree(self):
        n = 4 * len(Component.__added_components__[GuiElement])
        data = np.zeros(shape=(n,2))
        for k,gui_element in enumerate(Component.__added_components__[GuiElement]):
            x,y,w,h = gui_element.rect()
            data[k*4]   = (x,y)
            data[k*4+1] = (x+w,y)
            data[k*4+2] = (x,y+h)
            data[k*4+3] = (x+w,y+h)

        self.tree = cKDTree(data)

    def query(self,x,y):
        if self.tree is None: return None
        
        d,i = self.tree.query((x,y))
        
        if i == self.tree.n: return None

        k = i // 4
        gui_element = Component.__added_components__[GuiElement][k]
        if gui_element.is_in((x,y)):
            return gui_element
        else:
            return None

    def mouse_callback(self, event_type, event):
        print event.pos
        gui_element = self.query(*event.pos)
        if gui_element is None: return

        gui_element.entity.fire_callbacks(event_type, event)
