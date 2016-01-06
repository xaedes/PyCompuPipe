#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

from pyecs import *
from pycompupipe.components import Process, ProcessInput

class TestProcessInput():
    def test1(self):
        process = Process(1,0)
        input = ProcessInput(process)

        assert input.process == process

