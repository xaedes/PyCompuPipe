#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
import pygame

from pyecs import *

class Pygame(Component):
    """docstring for Pygame"""
    def __init__(self, size = (640, 480), caption = "caption", flags=pygame.DOUBLEBUF, *args,**kwargs):
        super(Pygame, self).__init__(*args,**kwargs)
        # Set the width and height of the screen [width, height]
        self.size = size
        self.caption = caption
        self.flags = flags

    @component_callback
    def component_attached(self):
        if pygame.RESIZABLE & self.flags == pygame.RESIZABLE:
            self.entity.register_callback("videoresize", self.onVideoresize)
            self.entity.register_callback("activeevent", self.onActiveEvent)
            self.resizing = None
        self.setup()

    def onVideoresize(self, event):
        self.resizing = event

    def onActiveEvent(self, event):
        if self.resizing is not None:
            if event.state == 2 and event.gain == 1:
                # end of resizing action
                self.resize(self.resizing.size)
                self.resizing = None
        # self.resize(event.resize)

    def resize(self, size):
        self.size = size
        self.screen = pygame.display.set_mode(self.size,self.flags)
        self.entity.fire_callbacks("resized", self)

    @callback
    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size,self.flags)
        pygame.display.set_caption(self.caption)


    @callback
    def quit(self, event):
        pygame.quit()

    def draw(self):
        self.entity.fire_callbacks("draw", self.screen)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

