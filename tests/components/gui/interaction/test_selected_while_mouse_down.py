#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

from pyecs import *
from pycompupipe.other import Event
from pycompupipe.components import Selectable, SelectedWhileMouseDown

import mock

class TestSelectedWhileMouseDown():
    @mock.patch("pycompupipe.components.gui.interaction.selected_while_mouse_down.Selectable.select")
    @mock.patch("pycompupipe.components.gui.interaction.selected_while_mouse_down.Selectable.deselect")
    def test(self, mocked_deselect, mocked_select):
        Selectable.selected = None
        e = Entity()
        s = e.add_component(Selectable())
        c = e.add_component(SelectedWhileMouseDown())

        mocked_select.reset_mock()
        mocked_deselect.reset_mock()
        e.fire_callbacks("mousebuttondown",Event(button=1))
        mocked_select.assert_called_once_with()
        mocked_deselect.assert_not_called()
        s.selected = True

        mocked_select.reset_mock()
        mocked_deselect.reset_mock()
        e.fire_callbacks("mousebuttonup",Event())
        mocked_select.assert_not_called()
        mocked_deselect.assert_called_once_with()

