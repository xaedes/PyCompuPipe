#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

import pygame

from pyecs import *
# from pyecs.components import *
# from components import *

class PygameSurface(Component):
    """docstring for PygameSurface"""
    def __init__(self, size, *args,**kwargs):
        super(PygameSurface, self).__init__()
        self._surface_args = args
        self._surface_kwargs = kwargs
        self.size = None
        self.surface = None
        self.resize(size)

    @callback
    def resize(self, size):
        self.size = size
        self.surface = pygame.Surface(self.size, *self._surface_args, **self._surface_kwargs)

