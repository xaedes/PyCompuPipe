#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
from __future__ import absolute_import

import pygame

from pyecs import *
# from pyecs.components import *
# from components import *

class ProcessConnection(Component):
    """docstring for ProcessConnection"""
    def __init__(self, input=None, output=None, *args,**kwargs):
        super(ProcessConnection, self).__init__(*args,**kwargs)
        self.input = input
        self.output = output
    
