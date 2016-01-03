#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
# from pyecs.components import *
from . import Pygame

class DrawOnResized(Component):
    """fires draw callback on videoresize callback"""
    def __init__(self,*args,**kwargs):
        super(DrawOnResized, self).__init__(*args,**kwargs)

    @callback
    def awake(self):
        self.pygame = self.get_component(Pygame)
    
    @callback
    def resized(self, pygame):
        self.pygame.draw()