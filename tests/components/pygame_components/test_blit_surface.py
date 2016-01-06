#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from pyecs import *
from pycompupipe.components import PygameSurface, BlitSurface, GuiElement

import mock
import pygame

from testing import *

class TestBlitSurface():

    @mock.patch("pycompupipe.components.pygame_components.blit_surface.BlitSurface.draw")
    def test_event(self, mocked_draw):
        e = Entity()
        s = e.add_component(PygameSurface((10,10)))
        d = e.add_component(BlitSurface("draw",10))
        screen = mock.NonCallableMock()
        e.fire_callbacks("draw", screen)
        mocked_draw.assert_called_once_with(screen)

    def test_draw(self):
        size = (100,100)
        size2 = (100,50)
        
        screen = pygame.Surface(size)

        screen.fill((0,0,0))

        e = Entity()
        s = e.add_component(PygameSurface(size2))
        d = e.add_component(BlitSurface("draw"))

        s.surface.fill((255,255,255))
        d.draw(screen)

        assert (pygame.surfarray.pixels3d(screen)[:size2[0],:size2[1]] == (255,255,255)).all()
        assert (pygame.surfarray.pixels3d(screen)[:size2[0],size2[1]:] == (0,0,0)).all()

    
    @forEach("x",lambda:iter([0,50,80]))
    @forEach("y",lambda:iter([0,50,80]))
    def test_draw_xy(self, x, y):
        size = (100,100)
        size2 = (1,1)
        
        screen = pygame.Surface(size)

        screen.fill((0,0,0))

        e = Entity()
        s = e.add_component(PygameSurface(size2))
        g = e.add_component(GuiElement((x,y)))
        d = e.add_component(BlitSurface("draw"))

        s.surface.fill((255,255,255))
        d.draw(screen)

        assert (pygame.surfarray.pixels3d(screen)[x,y] == (255,255,255)).all()

    def test_str(self):
        d = BlitSurface("draw")
        assert str(d) == "BlitSurface(draw)"
        