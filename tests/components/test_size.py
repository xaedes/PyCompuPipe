#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

from pyecs import *

from pycompupipe.components import Size

class TestSize():
    def test_usage(self):
        # use one number for width and height
        s = Size(10)
        assert s.size == 10

        # use a tuple to specify width and height
        s = Size((20,10))
        assert s.size == (20,10)
