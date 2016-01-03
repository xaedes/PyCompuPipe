#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from pyecs import *
from pycompupipe.components import DrawLine, GuiElement

import mock
import pygame
import re
import os.path

from testing import *

class TestDrawLine():

    @mock.patch("pycompupipe.components.drawing.draw_line.DrawLine.draw")
    def test_event(self, mocked_draw):
        e = Entity()
        d = DrawLine("draw",10)
        e.add_component(d)
        screen = mock.NonCallableMock()
        e.fire_callbacks("draw", screen)
        mocked_draw.assert_called_once_with(screen)

    @forFiles("fn","characterization/draw_line_*.png",os.path.dirname(__file__))
    def test_draw(self, fn):
        reference = pygame.image.load(fn)
        m = re.match(r"draw_line_(\d+),(\d+)_(\d+)_(\w+)\.png", os.path.basename(fn))
        p0 = (int(m.group(1)),int(m.group(2)))
        length = int(m.group(3))
        p1 = p0[0] + length, p0[1]
        arrow = True if m.group(4) == "True" else False
        size = reference.get_size()

        e = Entity()
        e.add_component(GuiElement())
        d = e.add_component(DrawLine("draw",[p0,p1],arrow))
        screen = pygame.Surface(size)
        screen.fill((255,255,255))
        d.draw(screen)

        np.testing.assert_almost_equal(
            pygame.surfarray.pixels3d(screen), 
            pygame.surfarray.pixels3d(reference)
            )

    @forEach("pos",lambda:iter([(0,0),(10,10),(20,10),(10,20)]))
    @forEach("length",lambda:iter([10,20]))
    @forEach("arrow",lambda:iter([False,True]))
    def _characterize(self, pos, length, arrow):
        size = (100,100)
        p0 = pos
        p1 = p0[0] + length, p0[1]
        e = Entity()
        e.add_component(GuiElement())
        d = e.add_component(DrawLine("draw",[p0,p1],arrow))
        screen = pygame.Surface(size)
        screen.fill((255,255,255))
        d.draw(screen)
        pygame.image.save(screen, os.path.dirname(__file__) + 
            "/characterization/draw_line_%d,%d_%d_%s.png" % 
                (p0[0],p0[1],length,str(arrow)))

def main(module_name):
    if module_name == "__main__":
        t = TestDrawLine()
        import sys
        if sys.argv[-1] == "characterize":
            t._characterize()

main(__name__)

