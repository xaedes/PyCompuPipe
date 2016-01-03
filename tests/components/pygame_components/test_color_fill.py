#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from pyecs import *
from pycompupipe.components import ColorFill

import mock
import pygame
import re
import os.path

from testing import *

class TestColorFill():

    @mock.patch("pycompupipe.components.pygame_components.color_fill.ColorFill.draw")
    def test_event(self, mocked_draw):
        e = Entity()
        d = e.add_component(ColorFill("draw",(255,0,0)))
        screen = mock.NonCallableMock()
        e.fire_callbacks("draw", screen)
        mocked_draw.assert_called_once_with(screen)

    def test_draw(self):
        size = (100,100)
        
        screen = pygame.Surface(size)

        screen.fill((0,0,0))
        c = ColorFill("draw",(255,0,0))
        c.draw(screen)

        assert (pygame.surfarray.pixels3d(screen) == (255,0,0)).all()
