#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import

from pyecs import *
from pycompupipe.components import ProcessInput, GuiElement
from . import UserCanDefineConnection


class UserCanDefineOutgoingConnection(UserCanDefineConnection):
    """docstring for UserCanDefineOutgoingConnection"""
    def __init__(self, *args,**kwargs):
        super(UserCanDefineOutgoingConnection, self).__init__(ProcessInput, *args,**kwargs)

    def reset(self):
        self._clear_support_points()
        self.entity.add_entity(self._support_point(0,0,relative=True))
        self.last_point = self.entity.add_entity(self._support_point(self.gui.snap_to_grid,0,relative=True))
        self.last_point = self.last_point.get_component(GuiElement)

