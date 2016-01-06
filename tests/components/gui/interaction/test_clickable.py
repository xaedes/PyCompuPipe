#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pyecs import *
from pycompupipe.other import Event
from pycompupipe.components import Clickable

import mock

class TestClickable():

    def test(self):
        e = Entity()
        c = e.add_component(Clickable())

        mocked_click = mock.MagicMock()

        e.register_callback("mouseclick", mocked_click)

        ev = Event(pos=(10,10), button=1)

        e.fire_callbacks("mousebuttondown", ev)
        mocked_click.assert_not_called()

        e.fire_callbacks("mousebuttonup", ev)
        mocked_click.assert_called_once_with(ev)
        