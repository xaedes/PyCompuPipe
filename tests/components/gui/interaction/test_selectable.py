#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

from testing import *

from pyecs import *
from pycompupipe.components import Selectable

import mock

class TestSelectable():
    def test(self):
        Selectable._reset_global()
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
        assert Selectable.selected_component == s0
        assert s0.selected == True
        assert s1.selected == False
        assert s2.selected == False

        s1.select()
        assert Selectable.selected_component == s1
        assert s0.selected == False
        assert s1.selected == True
        assert s2.selected == False

        s2.select()
        assert Selectable.selected_component == s2
        assert s0.selected == False
        assert s1.selected == False
        assert s2.selected == True

        s2.deselect()
        assert Selectable.selected_component == None
        assert s0.selected == False
        assert s1.selected == False
        assert s2.selected == False
    
        s0.deselect()        
        s1.deselect()        
        assert Selectable.selected_component == None
        assert s0.selected == False
        assert s1.selected == False
        assert s2.selected == False

    def test_events(self):
        Selectable._reset_global()
        e = Entity()
        selectable = e.add_component(Selectable())
        mocked_selected = mock.MagicMock()
        mocked_deselected = mock.MagicMock()
        e.register_callback("selected",mocked_selected)
        e.register_callback("deselected",mocked_deselected)

        mocked_selected.assert_not_called()
        mocked_deselected.assert_not_called()

        mocked_selected.reset_mock()
        mocked_deselected.reset_mock()
        selectable.select()
        mocked_selected.assert_called_once_with(selectable)
        mocked_deselected.assert_not_called()

        mocked_selected.reset_mock()
        mocked_deselected.reset_mock()
        selectable.select()
        mocked_selected.assert_not_called()
        mocked_deselected.assert_not_called()

        mocked_selected.reset_mock()
        mocked_deselected.reset_mock()
        selectable.deselect()
        mocked_selected.assert_not_called()
        mocked_deselected.assert_called_once_with(selectable)

        mocked_selected.reset_mock()
        mocked_deselected.reset_mock()
        selectable.deselect()
        mocked_selected.assert_not_called()
        mocked_deselected.assert_not_called()

    def test_selected_property(self):
        Selectable._reset_global()
        e = Entity()
        selectable = e.add_component(Selectable())
        mocked_selected = mock.MagicMock()
        mocked_deselected = mock.MagicMock()
        e.register_callback("selected",mocked_selected)
        e.register_callback("deselected",mocked_deselected)

        mocked_selected.reset_mock()
        mocked_deselected.reset_mock()
        selectable.selected = True
        mocked_selected.assert_called_once_with(selectable)
        mocked_deselected.assert_not_called()
        
        mocked_selected.reset_mock()
        mocked_deselected.reset_mock()
        selectable.selected = True
        mocked_selected.assert_not_called()
        mocked_deselected.assert_not_called()
        
        mocked_selected.reset_mock()
        mocked_deselected.reset_mock()
        selectable.selected = False
        mocked_selected.assert_not_called()
        mocked_deselected.assert_called_once_with(selectable)

        mocked_selected.reset_mock()
        mocked_deselected.reset_mock()
        selectable.selected = False
        mocked_selected.assert_not_called()
        mocked_deselected.assert_not_called()
