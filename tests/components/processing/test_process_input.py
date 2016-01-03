#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

import math
from funcy import partial
from testing import *

from pyecs import *
from pycompupipe.components import Process, ProcessInput

import pytest


class TestProcessInput():
    def test1(self):
        process = Process(1,0)
        input = ProcessInput(process)

        assert input.process == process

