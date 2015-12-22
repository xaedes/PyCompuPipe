#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
# from pyecs.components import *
from components import Pygame

import pygame

class BlockingPygameEventPump(Component):
    """docstring for BlockingPygameEventPump"""
    def __init__(self, *args,**kwargs):
        super(BlockingPygameEventPump, self).__init__(*args,**kwargs)
        self.done = False

    @callback
    def awake(self):
        self.pygame = self.get_component(Pygame)

    @callback
    def quit(self, event):
        self.done = True

    def pump(self):
        while not self.done:
            event = pygame.event.wait()
            if event.type in self.pygame.pygame_mappings:
                self.entity.fire_callbacks(self.pygame.pygame_mappings[event.type], event)

