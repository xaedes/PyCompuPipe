#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen

from pyecs import *
# from pyecs.components import *

from time import time

class Selectable(Component):
    selected_component = None
    @classmethod
    def _reset_global(CLS):
        Selectable.selected_component = None

    """docstring for Selectable"""
    def __init__(self, *args,**kwargs):
        super(Selectable, self).__init__(*args,**kwargs)
        self._selected = False

    @property
    def selected(self):
        return self._selected
    
    @selected.setter
    def selected(self, value):
        if value and not self._selected:
            self._selected = value
            self._select()

        elif self._selected and not value:
            self._selected = value
            self._deselect()

    def select(self):
        self.selected = True
    def deselect(self):
        self.selected = False

    def _select(self):
        # if not self.selected:
        if Selectable.selected_component is not None:
            Selectable.selected_component.deselect()

        Selectable.selected_component = self
        self.entity.fire_callbacks("selected", self)

    def _deselect(self):
        # if self.selected:
        Selectable.selected_component = None
        self.entity.fire_callbacks("deselected", self)

