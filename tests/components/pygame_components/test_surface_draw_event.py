#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pyecs import *
from pycompupipe.components import PygameSurface, SurfaceDrawEvent

import mock
import pygame

from testing import *

class TestSurfaceDrawEvent():

    @mock.patch("pycompupipe.components.pygame_components.surface_draw_event.PygameSurface.resize")
    def test_event(self, mocked_resize):
        e = Entity()
        s = e.add_component(PygameSurface((10,10)))
        c = e.add_component(SurfaceDrawEvent("arbitrary_event","draw"))

        s.surface = mock.NonCallableMock()
        mocked_draw = mock.MagicMock()
        
        e.register_callback("draw",mocked_draw)
        e.fire_callbacks("arbitrary_event")
        mocked_draw.assert_called_once_with(s.surface)

    @mock.patch("pycompupipe.components.pygame_components.surface_draw_event.PygameSurface.resize")
    def test_event_root(self, mocked_resize):
        e0 = Entity()
        e1 = e0.add_entity(Entity())
        e2 = e1.add_entity(Entity())
        s = e2.add_component(PygameSurface((10,10)))
        c = e2.add_component(SurfaceDrawEvent("arbitrary_event","draw",fire_at_root=True))

        s.surface = mock.NonCallableMock()
        mocked_draw0 = mock.MagicMock()
        mocked_draw2 = mock.MagicMock()

        e0.register_callback("draw",mocked_draw0)
        e2.register_callback("draw",mocked_draw2)
        e2.fire_callbacks("arbitrary_event")
        mocked_draw0.assert_called_once_with(s.surface)
        mocked_draw2.assert_not_called()

    def test_str(self):
        c = SurfaceDrawEvent("arbitrary_event","draw")
        assert str(c) == "SurfaceDrawEvent(arbitrary_event->draw)"
        c = SurfaceDrawEvent("arbitrary_event","draw",fire_at_root=True)
        assert str(c) == "SurfaceDrawEvent(arbitrary_event->root.draw)"
