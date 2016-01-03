#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
from numbers import Number
import math

from pyecs import *
import pygame

class DrawLine(Component):
    """docstring for DrawLine"""
    def __init__(self, draw_event_name, line, arrow=False, color=(0,0,0), *args,**kwargs):
        super(DrawLine, self).__init__(*args,**kwargs)
        self.draw_event_name = draw_event_name
        self.line = line
        self.arrow = arrow
        self.color = color

    @component_callback
    def component_attached(self):
        self.entity.register_callback(self.draw_event_name, self.draw)

    def draw(self, screen):
        x,y = self.entity.fire_callbacks_pipeline("position")

        p0, p1 = self.line

        p0 = x+p0[0], y+p0[1]
        p1 = x+p1[0], y+p1[1]
        # print pygame.draw.line,x,y,p0,p1
        pygame.draw.line(screen, self.color, p0, p1, 1)

        if self.arrow:
            p0_ = p1[0]

            dx = p0[0]-p1[0]
            dy = p0[1]-p1[1]
            d = math.sqrt(dx*dx+dy*dy)

            p0_above = p1[0]-0.4*d, p1[1]-0.4*d
            p0_below = p1[0]-0.4*d, p1[1]+0.4*d
            pygame.draw.line(screen, self.color, p0_above, p1, 1)
            pygame.draw.line(screen, self.color, p0_below, p1, 1)
