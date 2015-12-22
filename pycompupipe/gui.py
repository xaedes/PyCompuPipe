#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import numpy as np

from pyecs import *
from pyecs.components import *
from components import *

from gui_application import GuiApplication

from common import Utils

import pygame

class Gui(GuiApplication):
    """docstring for Experiment"""
    def __init__(self):
        self.width = 640
        self.height = 480

        super(Gui, self).__init__()

    def setup_main_entity(self):
        super(Gui, self).setup_main_entity()

        self.entity.add_component(Pygame(
            size=(self.width,self.height),
            caption="PyCompuPipe",
            flags=pygame.DOUBLEBUF | pygame.RESIZABLE))
        self.entity.add_component(ColorFill(color=(255,255,255)))
        # def print_args(*args):
        #     print args
        # self.entity.register_callback("videoresize",print_args)
        # self.entity.add_entity(self.create_entity())
        self.entity.fire_callbacks("awake")

    def create_entity(self):
        e = Entity()
        e.add_component(Pose(20,10))
        e.add_component(Size(20,10))
        e.add_component(DrawSizeAsRectangle((128,128,128)))
        e.add_component(Draggable())
        e.fire_callbacks("awake")
        return e

def main(module_name):
    if module_name == "__main__":
        Gui()

main(__name__)
