#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

import math
from funcy import partial
from testing import *

from pyecs import *
from pycompupipe.components import Process

import pytest


class TestProcess():
    def test(self):
        p = Process(2,3)
        assert p.num_inputs == 2
        assert p.num_outputs == 3
