#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

import math
from funcy import partial
from testing import *

from pyecs import *
from pycompupipe.components import Pose,SnapToGrid

import pytest


class TestSnapToGrid():

    @forEach("x",lambda:iter(range(5)))
    @forEach("y",lambda:iter(range(5)))
    @forEach("dx",partial(generateUniformRandoms,0,9.9),5)
    @forEach("dy",partial(generateUniformRandoms,0,9.9),5)
    def test_pipeline(self,x,y,dx,dy):
        e = Entity()
        assert e.fire_callbacks_pipeline("position") == None

        e.add_component(Pose(10*x+dx,10*y+dy))
        assert e.fire_callbacks_pipeline("position") == (10*x+dx,10*y+dy)

        e.add_component(SnapToGrid(10))
        assert e.fire_callbacks_pipeline("position") == (10*x,10*y)

