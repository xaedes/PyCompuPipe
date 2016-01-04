#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
# from pyecs.components import *
from . import Selectable

class SelectedWhileMouseDown(Component):
    selected = None
    """docstring for SelectedWhileMouseDown"""
    def __init__(self, *args,**kwargs):
        super(SelectedWhileMouseDown, self).__init__(*args,**kwargs)
        self.selectable = False

    @component_callback
    @with_components(required=[Selectable])
    def component_attached(self, selectable):
        self.selectable = selectable
        
    @callback    
    def mousebuttondown(self, event):
        # select if left mouse button is down
        if event.button == 1:
            self.selectable.select()

    @callback
    def mousebuttonup(self, event):
        # deselect
        if self.selectable.selected:
            self.selectable.deselect()
