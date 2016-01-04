#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

import math
from funcy import partial
from testing import *

from pyecs import *
from pycompupipe.components import GuiElement,GuiManager,Selectable, FetchMouseCallbacksWhileSelected

import pytest
import mock

from collections import namedtuple

class TestFetchMouseCallbacksWhileSelected():
    def test(self):
        e0 = Entity()
        gui_manager = e0.add_component(GuiManager())
        e1 = e0.add_entity(Entity())
        gui_element = e1.add_component(GuiElement((0,0),(0,0)))
        s = e1.add_component(Selectable())
        f = e1.add_component(FetchMouseCallbacksWhileSelected())
        e0.fire_callbacks("awake")

        PosEvent = namedtuple("Event",["pos"])

        # note: position outside of guielement
        argss = [("mousebuttonup",PosEvent((50,50))),
                 ("mousemotion",PosEvent((50,50))),
                 ("mousebuttondown",PosEvent((50,50)))]
        for args in argss:
            mocked = mock.MagicMock()
            e1.register_callback(args[0],mocked)

            mocked.reset_mock()
            s.select()
            e0.fire_callbacks(*args)
            mocked.assert_called_once_with(*args[1:])

            mocked.reset_mock()
            s.deselect()
            e0.fire_callbacks(*args)
            mocked.assert_not_called()



