#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

import math
from funcy import partial
from testing import *

from pyecs import *
from pycompupipe.components import Pose,Size,Anchor

import pytest


class TestAnchor():
    def test_usage(self):
        # specify x and y with one number
        a = Anchor(0.5)
        assert a.x == 0.5
        assert a.y == 0.5
        assert str(a) == "Anchor(0.5,0.5)"

        # specify x and y
        a = Anchor((0.5,1))
        assert a.x == 0.5
        assert a.y == 1
        assert str(a) == "Anchor(0.5,1)"

        with pytest.raises(NotImplementedError):
            a = Anchor("this-is-not-supported")

    def test_pipeline(self):
        e = Entity()
        assert e.fire_callbacks_pipeline("position") == None

        e.add_component(Pose(100,50))
        assert e.fire_callbacks_pipeline("position") == (100,50)

        e.add_component(Size((40,30)))
        e.add_component(Anchor(0.5))
        assert e.fire_callbacks_pipeline("position") == (80,35)

