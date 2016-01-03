#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
# from pyecs.components import *
from .. import GuiElement

from funcy import partial

class FetchMouseCallbacksWhileSelected(Component):
    """docstring for FetchMouseCallbacksWhileSelected"""
    def __init__(self, *args,**kwargs):
        super(FetchMouseCallbacksWhileSelected, self).__init__(*args,**kwargs)
        self.mouse_callbacks = []
        self.mouse_callbacks.append(("mousemotion",partial(self.mouse_callback, "mousemotion")))
        self.mouse_callbacks.append(("mousebuttonup",partial(self.mouse_callback, "mousebuttonup")))
        self.mouse_callbacks.append(("mousebuttondown",partial(self.mouse_callback, "mousebuttondown")))
        self.guielement = None

    @callback
    @with_components(required=[GuiElement])
    def awake(self, guielement):
        self.guielement = guielement

    @callback    
    def selected(self, selectable):
        for key,callback in self.mouse_callbacks:        
            self.guielement.manager.entity.register_callback(key,callback)
    
    @callback
    def deselected(self, selectable):
        for key,callback in self.mouse_callbacks:        
            self.guielement.manager.entity.remove_callback(key,callback)


    def mouse_callback(self, key, event):
        self.entity.fire_callbacks(key, event)
