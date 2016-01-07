#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
from __future__ import absolute_import

import pygame

from pyecs import *
# from pyecs.components import *
# from components import *

class ColorFill(Component):
    """docstring for ColorFill"""
    def __init__(self, draw_event_name, color = (0,0,0), *args,**kwargs):
        super(ColorFill, self).__init__(*args,**kwargs)
        self.draw_event_name = draw_event_name
        self.color = color

    @component_callback
    def component_attached(self):
        self.entity.register_callback(self.draw_event_name, self.draw)

    def draw(self, screen):
        screen.fill(self.color)
