#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

import math
from funcy import partial
from testing import *

from pyecs import *
from pycompupipe.components import Selectable

import pytest
import mock

class TestSelectable():
    def test(self):
        Selectable.selected = None
        e0 = Entity()
        s0 = e0.add_component(Selectable())
        e1 = Entity()
        s1 = e1.add_component(Selectable())
        e2 = Entity()
        s2 = e2.add_component(Selectable())
        assert s0.selected == False
        assert s1.selected == False
        assert s2.selected == False
        
        s0.select()
        assert Selectable.selected == s0
        assert s0.selected == True
        assert s1.selected == False
        assert s2.selected == False

        s1.select()
        assert Selectable.selected == s1
        assert s0.selected == False
        assert s1.selected == True
        assert s2.selected == False

        s2.select()
        assert Selectable.selected == s2
        assert s0.selected == False
        assert s1.selected == False
        assert s2.selected == True

        s2.deselect()
        assert Selectable.selected == None
        assert s0.selected == False
        assert s1.selected == False
        assert s2.selected == False
    
        s0.deselect()        
        s1.deselect()        
        assert Selectable.selected == None
        assert s0.selected == False
        assert s1.selected == False
        assert s2.selected == False

    def test_events(self):
        e = Entity()
        s = e.add_component(Selectable())
        mocked_selected = mock.MagicMock()
        mocked_deselected = mock.MagicMock()
        e.register_callback("selected",mocked_selected)
        e.register_callback("deselected",mocked_deselected)

        mocked_selected.assert_not_called()
        mocked_deselected.assert_not_called()

        mocked_selected.reset_mock()
        mocked_deselected.reset_mock()
        s.select()
        mocked_selected.assert_called_once_with(s)
        mocked_deselected.assert_not_called()

        mocked_selected.reset_mock()
        mocked_deselected.reset_mock()
        s.select()
        mocked_selected.assert_not_called()
        mocked_deselected.assert_not_called()

        mocked_selected.reset_mock()
        mocked_deselected.reset_mock()
        s.deselect()
        mocked_selected.assert_not_called()
        mocked_deselected.assert_called_once_with(s)

        mocked_selected.reset_mock()
        mocked_deselected.reset_mock()
        s.deselect()
        mocked_selected.assert_not_called()
        mocked_deselected.assert_not_called()

