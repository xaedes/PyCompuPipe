#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pyecs import *
from pycompupipe.other import Event

class TestEvent():

    def test(self):
        e = Event(pos=(1,2))
        assert hasattr(e, "pos")
        assert e.pos == (1,2)

    def test2(self):
        e = Event(pos=(1,2),button=1)
        assert hasattr(e, "pos")
        assert e.pos == (1,2)
        assert hasattr(e, "button")
        assert e.button == 1
