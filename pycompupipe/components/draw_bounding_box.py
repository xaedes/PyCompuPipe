#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
import pygame
from pyecs import *
# from pyecs.components import *
from components import BoundingBox

class DrawBoundingBox(Component):
    """docstring for DrawBoundingBox"""
    def __init__(self, color=(255,255,255), *args,**kwargs):
        super(DrawBoundingBox, self).__init__(*args,**kwargs)
        self.color = color

    @callback
    @with_components(required=[BoundingBox])
    def draw(self, screen, boundingbox):
        bbox = boundingbox.rect()
        pygame.draw.rect(screen, self.color, bbox, 1)
