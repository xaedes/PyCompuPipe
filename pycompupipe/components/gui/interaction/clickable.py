#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import

from pyecs import *
# from pyecs.components import *

class Clickable(Component):
    """docstring for Clickable"""
    def __init__(self, *args,**kwargs):
        super(Clickable, self).__init__(*args,**kwargs)
        self.clicking = False

    @callback    
    def mousebuttondown(self, event):
        self.clicking = True

    @callback    
    def mousebuttonup(self, event):
        if self.clicking:
            self.clicking = False
            self.entity.fire_callbacks("mouseclick", event)
    