#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import math
import numpy as np

class MathUtils():
    @classmethod
    def rotation_matrix(cls, radians):
        cs, sn = math.cos(radians),math.sin(radians)
        return np.array([[cs,-sn],[sn,cs]])

    @classmethod
    def rotate(cls, points, radians):
        rot = cls.rotation_matrix(radians)
        return points.dot(rot.T)

