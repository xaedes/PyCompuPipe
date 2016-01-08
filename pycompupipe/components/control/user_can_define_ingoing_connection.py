#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import

from pyecs import *
from pycompupipe.components import ProcessOutput, GuiElement
from . import UserCanDefineConnection

class UserCanDefineIngoingConnection(UserCanDefineConnection):
    """docstring for UserCanDefineIngoingConnection"""
    def __init__(self, *args,**kwargs):
        super(UserCanDefineIngoingConnection, self).__init__(ProcessOutput, *args,**kwargs)

    def reset(self):
        self._clear_support_points()
        self.last_point = self.entity.add_entity(self._support_point(0,0,relative=True))
        self.last_point = self.last_point.get_component(GuiElement)
        self.entity.add_entity(self._support_point(self.gui.snap_to_grid,0,relative=True))

