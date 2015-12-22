#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
from pyecs.components import *
import pygame as pygame_module
class DrawOnVideoresize(Component):
    """fires draw callback on videoresize callback"""
    def __init__(self,*args,**kwargs):
        super(DrawOnVideoresize, self).__init__(*args,**kwargs)

    @callback
    @with_components(required=[Pygame])
    def videoresize(self,event,pygame):
        print "draw"
        self.entity.fire_callbacks("draw", pygame.screen)
        print "flip"
        pygame_module.display.flip()