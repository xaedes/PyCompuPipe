#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from pyecs import *
from pycompupipe.components import DrawOnResized

import mock
import pygame

from testing import *

class TestDrawOnResized():

    def test(self):
        e = Entity()
        d = e.add_component(DrawOnResized())

        mocked = mock.NonCallableMock()

        e.fire_callbacks("resized", mocked)

        mocked.draw.assert_called_once_with()
