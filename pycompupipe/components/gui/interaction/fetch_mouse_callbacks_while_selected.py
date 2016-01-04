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
        self.guielement = None

    @component_callback
    @with_components(required=[GuiElement])
    def component_attached(self, guielement):
        self.guielement = guielement

    @callback    
    def selected(self, selectable):
        self.guielement.always_fetch_mouse = True          
    
    @callback
    def deselected(self, selectable):
        self.guielement.always_fetch_mouse = False
