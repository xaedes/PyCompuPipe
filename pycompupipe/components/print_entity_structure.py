#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import

import numpy as np

from pyecs import *
from pyecs.components import *
from . import *

from time import time

class PrintEntityStructure(Component):
    """docstring for PrintEntityStructure"""
    def __init__(self, interval=1., *args,**kwargs):
        super(PrintEntityStructure, self).__init__(*args,**kwargs)
        self.interval = interval # in seconds
        self.last_save = None

    @callback
    def start(self):
        self.last_save = time()

    @callback
    def update(self, dt):
        if self.last_save is None or time() - self.last_save > self.interval:
            self.print_structure()
            self.last_save = time()

    @callback
    def quit(self,evt):
        self.print_structure()

    def print_structure(self):
        pass
        print "---"
        self.entity.find_root().print_structure()