#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

from pyecs import *
from pycompupipe.components import Process, ProcessOutput

class TestProcessOutput():
    def test1(self):
        process = Process(1,0)
        output = ProcessOutput(process)

        assert output.process == process

