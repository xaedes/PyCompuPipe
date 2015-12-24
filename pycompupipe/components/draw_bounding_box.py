#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
import pygame
from pyecs import *
# from pyecs.components import *
from . import BoundingBox

class DrawBoundingBox(Component):
    """docstring for DrawBoundingBox"""
    def __init__(self, draw_event_name, color=(255,255,255), *args,**kwargs):
        super(DrawBoundingBox, self).__init__(*args,**kwargs)
        self.draw_event_name = draw_event_name
        self.color = color


    @component_callback
    def component_attached(self):
        self.entity.register_callback(self.draw_event_name, self.draw)
    
    @with_components(required=[BoundingBox])
    def draw(self, screen, boundingbox):
        bbox = boundingbox.rect()
        print "DrawBoundingBox.draw", screen, bbox
        pygame.draw.rect(screen, self.color, bbox, 1)

    def __str__(self):
        return "%s(%s, %s)" % (
                super(type(self),self).__str__(), 
                self.draw_event_name, 
                str(self.color)
                )
