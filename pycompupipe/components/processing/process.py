#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
from __future__ import absolute_import

import pygame

from pyecs import *
# from pyecs.components import *
# from components import *

class Process(Component):
    """docstring for Process"""
    def __init__(self, num_inputs, num_outputs, *args,**kwargs):
        '''
        @summary: 
        @param num_inputs:
        @param num_outputs:
        @param *args:
        @param **kwargs:
        @result: 
        '''
        super(Process, self).__init__(*args,**kwargs)
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs

