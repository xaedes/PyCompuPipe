#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

import pygame

from pyecs import *
# from pyecs.components import *
# from components import *

class ProcessInput(Component):
    """docstring for ProcessInput"""
    def __init__(self, process, *args,**kwargs):
        super(ProcessInput, self).__init__(*args,**kwargs)
        self.process = process
    
