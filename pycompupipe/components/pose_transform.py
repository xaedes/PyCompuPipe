#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
import math

from pyecs import *
from . import Pose

class PoseTransform(Component):
    """docstring for PoseTransform"""
    def __init__(self, *args,**kwargs):
        super(PoseTransform, self).__init__(*args,**kwargs)
        self.parent_pose_entity = None

    def _find_parent_xy(self):
        parent = self.parent_pose_entity or self.entity.find_parent_entity_with_component(Pose)
        if parent is None: return None
        return parent.fire_callbacks_pipeline("position")

    @callback
    def position(self, accum):
        x,y = accum
        parent_xy = self._find_parent_xy()
        if parent_xy is not None:
            x,y = parent_xy[0] + x, parent_xy[1] + y
        return x,y

