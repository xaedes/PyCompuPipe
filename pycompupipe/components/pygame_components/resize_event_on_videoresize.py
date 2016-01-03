#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

import pygame

from pyecs import *
# from pyecs.components import *
# from . import *

class ResizeEventOnVideoresize(Component):
    """docstring for ResizeEventOnVideoresize"""
    def __init__(self, *args,**kwargs):
        super(ResizeEventOnVideoresize, self).__init__(*args,**kwargs)

    @callback
    def videoresize(self, event):
        self.entity.fire_callbacks("resize", event.size)
