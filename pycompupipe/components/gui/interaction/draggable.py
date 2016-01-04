#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
# from pyecs.components import *
from .. import GuiElement

from time import time

class Draggable(Component):
    """docstring for Draggable"""
    def __init__(self, move_every = 1/60, *args,**kwargs):
        super(Draggable, self).__init__(*args,**kwargs)
        self.dragging = False
        self.last_move = time()
        
        # specify how much time shall elapse between two Pose updates
        self.move_every = move_every

        self.last_pos = None
        self.guielement = None

    @component_callback
    @with_components(required=[GuiElement])
    def component_attached(self, guielement):
        self.guielement = guielement

    @callback    
    def selected(self, selectable):
        if not self.dragging:
            self.dragging = True
            self.entity.fire_callbacks("drag", self)

    @callback    
    def mousebuttondown(self, event):
        self.new_pos(event.pos)
                    
    @callback    
    def mousemotion(self, event):
        self.new_pos(event.pos)
    
    @callback    
    def mousebuttonup(self, event):
        self.new_pos(event.pos)
    
    def new_pos(self, pos):
        if not self.dragging:
            return 

        if self.last_pos is None:
            self.last_pos = pos

        elif time() - self.last_move > self.move_every:
            self.last_move = time()
            self.guielement.position = self.guielement.position[0] + pos[0] - self.last_pos[0], self.guielement.position[1] + pos[1] - self.last_pos[1]
            self.last_pos = pos
            self.entity.fire_callbacks("dragging", self)

    @callback
    def deselected(self, selectable):
        # deselect
        if self.dragging:
            self.dragging = False
            self.last_pos = None
            self.entity.fire_callbacks("drop", self)

