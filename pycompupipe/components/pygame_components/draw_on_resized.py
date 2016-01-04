#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
# from pyecs.components import *

class DrawOnResized(Component):
    """fires draw callback on 'resized' callback"""
    def __init__(self,*args,**kwargs):
        super(DrawOnResized, self).__init__(*args,**kwargs)

    @callback
    def resized(self, pygame):
        pygame.draw()
