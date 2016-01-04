#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
# from pyecs.components import *

from time import time

class Selectable(Component):
    selected = None
    """docstring for Selectable"""
    def __init__(self, *args,**kwargs):
        super(Selectable, self).__init__(*args,**kwargs)
        self.selected = False

    def select(self):
        if not self.selected:
            if Selectable.selected is not None:
                Selectable.selected.deselect()

            self.selected = True
            Selectable.selected = self
            self.entity.fire_callbacks("selected", self)

    def deselect(self):
        if self.selected:
            self.selected = False
            Selectable.selected = None
            self.entity.fire_callbacks("deselected", self)

