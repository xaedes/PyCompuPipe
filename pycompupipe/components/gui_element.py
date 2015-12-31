#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
# from . import Size

class GuiElement(Component):
    """docstring for GuiElement"""
    def __init__(self, position, size, anchor, *args,**kwargs):
        super(GuiElement, self).__init__(*args,**kwargs)
        self.position = position
        self.size = size
        self.anchor = anchor
        self.manager = None

    def rect(self):
        x,y = self.position
        w,h = self.size
        return (x, y, w, h)

    def is_in(self, pos):
        i,j = pos
        x,y,w,h = self.rect()
        result = i >= x and i <= x+w and j >= y and j <= y+h
        return result

    @component_callback
    def register_manager(self, manager):
        self.manager = manager
