#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
from __future__ import absolute_import

import pygame
from pyecs import *
# from pyecs.components import *

class DrawProcess(Component):
    """docstring for DrawProcess"""
    def __init__(self, draw_event_name, bg_color=(255,255,255), fg_color=(0,0,0), *args,**kwargs):
        super(DrawProcess, self).__init__(*args,**kwargs)
        self.draw_event_name = draw_event_name
        self.bg_color = bg_color
        self.fg_color = fg_color

    @component_callback
    def component_attached(self):
        self.entity.register_callback(self.draw_event_name, self.draw)
    
    def draw(self, screen):
        screen.fill(self.bg_color)
        pygame.draw.rect(screen, self.fg_color, screen.get_rect(), 1)
