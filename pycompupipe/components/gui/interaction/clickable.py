#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
from pycompupipe.other import Event
# from pyecs.components import *
from .. import GuiElement

from time import time

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
    