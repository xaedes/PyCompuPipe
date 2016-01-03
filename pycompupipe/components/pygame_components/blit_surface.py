#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

import pygame

from pyecs import *
# from pyecs.components import *
from . import PygameSurface

class BlitSurface(Component):
    """docstring for BlitSurface"""
    def __init__(self, draw_event_name, blit_flags=0, *args,**kwargs):
        super(BlitSurface, self).__init__(*args,**kwargs)
        self.draw_event_name = draw_event_name
        self.blit_flags = blit_flags
        self.surface = None


    @callback
    @with_components(required=[PygameSurface])
    def awake(self, pygamesurface):
        self.surface = pygamesurface
        
    @component_callback
    def component_attached(self):
        self.entity.register_callback(self.draw_event_name, self.draw)

    def draw(self, surface):
        xy = self.entity.fire_callbacks_pipeline("position")
        if xy is None:
            x,y = 0,0
        else:
            x,y = xy
        # print "blit", self.surface.surface, "at", (x,y), "to", self.draw_event_name
        surface.blit(self.surface.surface,(x,y),None,self.blit_flags)

    def __str__(self):
        return "%s(%s)" % (
                super(type(self),self).__str__(), 
                self.draw_event_name, 
                )
