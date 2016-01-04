#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

import math
import numpy as np
from funcy import partial
from testing import *

from pyecs import *
from pycompupipe.components import (
                GuiManager,GuiElement,
                Selectable, FetchMouseCallbacksWhileSelected, 
                SelectedWhileMouseDown, Draggable)

import pytest
import mock

from collections import namedtuple

class TestDraggable():
    def test_selected_callbacks(self):
        Component._reset_global()

        e = Entity()
        s = e.add_component(Selectable())
        draggable = e.add_component(Draggable())
        assert draggable.dragging == False

        mocked_drag = mock.MagicMock()
        mocked_drop = mock.MagicMock()
        e.register_callback("drag", mocked_drag)
        e.register_callback("drop", mocked_drop)

        s.select()
        assert draggable.dragging == True
        assert mocked_drag.called

        s.deselect()
        assert draggable.dragging == False
        assert mocked_drop.called

    def test_moving(self):
        Component._reset_global()

        Selectable.selected = None
        e0 = Entity()
        e0.add_component(GuiManager())

        e1 = e0.add_entity(Entity())
        gui = e1.add_component(GuiElement((0,0),(10,10)))
        s = e1.add_component(Selectable())
        e1.add_component(SelectedWhileMouseDown())
        e1.add_component(FetchMouseCallbacksWhileSelected())

        e0.fire_callbacks("awake")

        draggable = e1.add_component(Draggable())

        Event = namedtuple("Event",["pos"])
        ButtonEvent = namedtuple("Event",["pos","button"])
        
        cursor_start = (5,5) # inside of gui element

        # generate random walk
        n = 100
        dxy = np.random.normal(0,5,(n,2))
        xy = np.cumsum(dxy,axis=0) + cursor_start
        xy = np.round(xy)

        # start dragging
        e0.fire_callbacks("mousebuttondown",ButtonEvent(xy[0],1))
        assert draggable.dragging == True
        assert gui.position[0] == xy[i,0] - cursor_start[0]
        assert gui.position[1] == xy[i,1] - cursor_start[1]

        # move around n times with random walk
        # omit first and last pos, as these are for buttondown and buttonup
        for i in xrange(1,n-1):
            e0.fire_callbacks("mousemotion",Event(xy[i]))

            # assert gui element was moved
            assert gui.position[0] == xy[i,0] - cursor_start[0]
            assert gui.position[1] == xy[i,1] - cursor_start[1]

        # end moving
        e.fire_callbacks("mousebuttonup",Event(xy[-1]))
        assert gui.position[0] == xy[-1,0] - cursor_start[0]
        assert gui.position[1] == xy[-1,1] - cursor_start[1]
        assert draggable.dragging == False

t = TestDraggable()
t.test_moving()
