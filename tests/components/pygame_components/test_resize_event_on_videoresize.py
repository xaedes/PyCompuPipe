#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pyecs import *
from pycompupipe.components import ResizeEventOnVideoresize

import mock

class TestResizeEventOnVideoresize():

    def test(self):
        e = Entity()
        d = e.add_component(ResizeEventOnVideoresize())

        mocked_resize = mock.MagicMock()
        mocked_event = mock.NonCallableMock()
        e.register_callback("resize", mocked_resize)

        e.fire_callbacks("videoresize", mocked_event)

        mocked_resize.assert_called_once_with(mocked_event.size)
