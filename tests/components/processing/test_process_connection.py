#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

import math
from funcy import partial
from testing import *

from pyecs import *
from pycompupipe.components import Process, ProcessConnection

import pytest


class TestProcessConnection():
    def test1(self):
        producer = Process(0,1)
        consumer = Process(1,0)

        conn = ProcessConnection(producer, consumer)

        assert conn.input == producer
        assert conn.output == consumer

    def test2(self):
        consumer = Process(1,0)

        conn = ProcessConnection(input=None, output=consumer)

        assert conn.input == None
        assert conn.output == consumer

    def test3(self):
        producer = Process(0,1)

        conn = ProcessConnection(input=producer, output=None)

        assert conn.input == producer
        assert conn.output == None
