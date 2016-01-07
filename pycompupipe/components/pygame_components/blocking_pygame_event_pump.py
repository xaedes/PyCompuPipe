#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
from __future__ import absolute_import

from pyecs import *
# from pyecs.components import *

import pygame

class BlockingPygameEventPump(Component):
    """docstring for BlockingPygameEventPump"""

    
    event_mappings = dict({
        pygame.QUIT: "quit",
        pygame.ACTIVEEVENT: "activeevent",
        pygame.KEYDOWN: "keydown",
        pygame.KEYUP: "keyup",
        pygame.MOUSEMOTION: "mousemotion",
        pygame.MOUSEBUTTONUP: "mousebuttonup",
        pygame.MOUSEBUTTONDOWN: "mousebuttondown",
        pygame.JOYAXISMOTION: "joyaxismotion",
        pygame.JOYBALLMOTION: "joyballmotion",
        pygame.JOYHATMOTION: "joyhatmotion",
        pygame.JOYBUTTONUP: "joybuttonup",
        pygame.JOYBUTTONDOWN: "joybuttondown",
        pygame.VIDEORESIZE: "videoresize",
        pygame.VIDEOEXPOSE: "videoexpose",
        pygame.USEREVENT: "userevent"
        })

    def __init__(self, *args,**kwargs):
        super(BlockingPygameEventPump, self).__init__(*args,**kwargs)
        self.done = False

    @callback
    def quit(self, event):
        self.done = True

    def pump(self):
        while not self.done:
            event = pygame.event.wait()
            if event.type in self.event_mappings:
                self.entity.fire_callbacks(self.event_mappings[event.type], event)

