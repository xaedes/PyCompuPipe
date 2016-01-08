#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
from __future__ import absolute_import

import numpy as np

from pyecs import *
from . import GuiElement

from funcy import partial

class GuiManager(Component):
    """docstring for GuiManager"""
    def __init__(self, *args,**kwargs):
        super(GuiManager, self).__init__(*args,**kwargs)
        self.exclusive_elements = set()

    @callback
    def awake(self):
        for gui_element in Component.__added_components__[GuiElement]:
            gui_element.fire_callbacks("register_manager", self)

        self.entity.register_callback("mousemotion",partial(self.mouse_callback, "mousemotion"))
        self.entity.register_callback("mousebuttonup",partial(self.mouse_callback, "mousebuttonup"))
        self.entity.register_callback("mousebuttondown",partial(self.mouse_callback, "mousebuttondown"))

    def query(self,x,y,limit_num=None):
        result = []
        for gui_element in Component.__added_components__[GuiElement]:
            if gui_element.is_in((x,y)):
                result.append(gui_element)
                if limit_num is not None and len(result) == limit_num:
                    return result

        return result
        
    def query1(self,x,y):
        l = self.query(x,y,1)
        if len(l) == 0:
            return None
        else:
            return l[0]

    def mouse_callback(self, event_type, event):
        gui_elements = self.query(*event.pos)
        for gui_element in gui_elements:
            if len(self.exclusive_elements)==0 or (gui_element in self.exclusive_elements):
                if not gui_element.always_fetch_mouse:
                    gui_element.entity.fire_callbacks(event_type, event)

                    # gui_element.always_fetch_mouse == True:
                    # the gui element has mouse callbacks on manager entity
                    # we don't want to fire events twice for this gui element
                    # so we do nothing here
