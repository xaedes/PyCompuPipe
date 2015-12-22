#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import math
import os
import numpy as np

from pyecs import *
from pyecs.components import *
from components import *

class GuiApplication(Application):
    """
    Doesn't have a main update loop, but waits for pygame events.
    """
    def __init__(self):
        super(GuiApplication, self).__init__()

    def setup_main_entity(self):
        super(GuiApplication, self).setup_main_entity()
        self.entity.add_component(BlockingPygameEventPump())
        self.entity.add_component(DrawOnVideoresize())
        self.entity.add_component(PropagateCallback(["draw"]))
        self.entity.fire_callbacks("awake")

    def spin(self):
        self.entity.get_component(BlockingPygameEventPump).pump()
        
def main(module_name):
    if module_name == "__main__":
        print "this file is not meant to be executed directly"

main(__name__)
