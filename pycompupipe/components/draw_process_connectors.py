#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
import pygame
from pyecs import *
# from pyecs.components import *
from . import Process, BoundingBox

class DrawProcessConnectors(Component):
    """docstring for DrawProcessConnectors"""
    def __init__(self, draw_event_name, color=(0,0,0), padding=10, *args,**kwargs):
        super(DrawProcessConnectors, self).__init__(*args,**kwargs)
        self.draw_event_name = draw_event_name
        self.color = color
        self.padding = padding


    @component_callback
    @with_components(required=[BoundingBox])
    def component_attached(self, boundingbox):
        self.boundingbox = boundingbox
        self.entity.register_callback(self.draw_event_name, self.draw)

    @callback    
    def entity_added(self, parent, entity):
        if entity == self.entity:
            self.process = self.entity.find_parent_entity_with_component(Process).get_component(Process)

    def draw(self, screen):
        x,y,w,h = self.boundingbox.rect()

        for i in range(self.process.num_inputs):
            p0 = x-self.padding, y+(i+1)*self.padding
            p1 = x, y+(i+1)*self.padding
            pygame.draw.line(screen, self.color, p0, p1, 1)

            p0 = x-0.4*self.padding, y+(i+1-0.4)*self.padding
            p1 = x, y+(i+1)*self.padding
            pygame.draw.line(screen, self.color, p0, p1, 1)

            p0 = x-0.4*self.padding, y+(i+1+0.4)*self.padding
            p1 = x, y+(i+1)*self.padding
            pygame.draw.line(screen, self.color, p0, p1, 1)

        for i in range(self.process.num_outputs):
            p0 = x+w+self.padding, y+(i+1)*self.padding
            p1 = x+w, y+(i+1)*self.padding
            pygame.draw.line(screen, self.color, p0, p1, 1)

    def __str__(self):
        return "%s(%s, %s)" % (
                super(type(self),self).__str__(), 
                self.draw_event_name, 
                str(self.color)
                )
