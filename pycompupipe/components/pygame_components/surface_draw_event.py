#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
from __future__ import absolute_import

import pygame

from pyecs import *
# from pyecs.components import *
from . import PygameSurface

class SurfaceDrawEvent(Component):
    """docstring for SurfaceDrawEvent"""
    def __init__(self, on_event, event_name, fire_at_root = False, *args,**kwargs):
        super(SurfaceDrawEvent, self).__init__(*args,**kwargs)
        self.on_event = on_event
        self.event_name = event_name
        self.fire_at_root = fire_at_root
        self.fire_at = None
        self.surface = None

    @component_callback
    @with_components(required=[PygameSurface])
    def component_attached(self, pygamesurface):
        self.surface = pygamesurface
        self.entity.register_callback(self.on_event, self.event)
        
    def _fire_at(self):
        if self.fire_at_root and self.entity:
            return self.entity.find_root()

        if not self.fire_at_root:
            return self.entity

    def event(self, *args, **kwargs):
        # print self.event_name

        self.fire_at = self.fire_at or self._fire_at()

        if self.fire_at and self.surface:
            self.fire_at.fire_callbacks(self.event_name, self.surface.surface)

    def __str__(self):
        return "%s(%s->%s%s)" % (
                super(type(self),self).__str__(), 
                self.on_event, 
                "root." if self.fire_at_root else "",
                self.event_name, 
                )
