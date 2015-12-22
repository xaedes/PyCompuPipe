#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
# from pyecs.components import *
from components import Pose, Size, Pygame

from time import time

class Draggable(Component):
    num_selected = 0
    """docstring for Draggable"""
    def __init__(self, move_every = 1/60, *args,**kwargs):
        super(Draggable, self).__init__(*args,**kwargs)
        self.dragging = False
        self.last_move = time()
        
        # specify how much time shall elapse between two Pose updates
        self.move_every = move_every

        # print "Draggable()"
        self.last_pos = None

    @callback    
    def selected(self, selectable):
        if not self.dragging:
            self.dragging = True
            self.entity.fire_callbacks("drag", self)

    @callback    
    def mousebuttondown(self, event):
        if self.dragging:
            self.last_pos = event.pos
                    
    @callback    
    @with_components(required=[Pose])
    def mousemotion(self, event, pose):
        if self.dragging:
            # print "mousemotion", event
            if time() - self.last_move > self.move_every:
                self.last_move = time()
                pose.x += event.pos[0] - self.last_pos[0]
                pose.y += event.pos[1] - self.last_pos[1]
                self.last_pos = event.pos
                self.entity.fire_callbacks("dragging", self)
    
    @callback
    def deselected(self, selectable):
        # deselect
        if self.dragging:
            # print "mousebuttonup", event
            self.dragging = False
            self.entity.fire_callbacks("drop", self)


