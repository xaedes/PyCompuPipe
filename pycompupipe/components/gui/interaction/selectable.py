#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
# from pyecs.components import *

from time import time

class Selectable(Component):
    selected = None
    """docstring for Selectable"""
    def __init__(self, move_every = 1/60, *args,**kwargs):
        super(Selectable, self).__init__(*args,**kwargs)
        self.selected = False
        self.last_move = time()
        
        # specify how much time shall elapse between two Pose updates
        self.move_every = move_every

        # print "Selectable()"
        self.last_pos = None

    def select(self):
        self.selected = True
        Selectable.selected = self
        self.entity.fire_callbacks("selected", self)

    def deselect(self):
        self.selected = False
        Selectable.selected = None
        self.entity.fire_callbacks("deselected", self)

    @callback    
    def mousebuttondown(self, event):
        # select if left mouse button is down
        if event.button == 1 and self.entity.fire_callbacks_pipeline("is_in",event.pos):
            if Selectable.selected is not None:
                Selectable.selected.deselect()
            self.select()

    @callback
    def mousebuttonup(self, event):
        # deselect
        if self.selected:
            # print "mousebuttonup", event
            self.deselect()
