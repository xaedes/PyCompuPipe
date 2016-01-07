#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from pyecs import *
from pycompupipe.components import DrawPath, GuiElement

import mock
import pygame
import re
import os.path

from testing import *

class TestDrawPath():
    def _support_point(self,x,y):
        e = Entity()
        e.add_component(GuiElement((x,y)))
        e.add_tag("support_point")
        return e

    @mock.patch("pycompupipe.components.drawing.draw_path.DrawPath.draw")
    def test_event(self, mocked_draw):
        e = Entity()
        d = DrawPath("draw",10)
        e.add_component(d)
        screen = mock.NonCallableMock()
        e.fire_callbacks("draw", screen)
        mocked_draw.assert_called_once_with(screen)

    @forFiles("fn","characterization/draw_path_*.png",os.path.dirname(__file__))
    def test_draw(self, fn):
        reference = pygame.image.load(fn)
        m = re.match(r"^draw_path_(.+)_(\w+)\.png$", os.path.basename(fn))
        xys = m.group(1)
        xys = [[float(v) for v in xy.split(",")] for xy in xys.split("_")]

        arrow = int(m.group(2))

        size = reference.get_size()

        e = Entity()
        # e.add_component(GuiElement())
        d = e.add_component(DrawPath("draw",arrow))
        for xy in xys:
            e.add_entity(self._support_point(*xy))


        screen = pygame.Surface(size)
        screen.fill((255,255,255,255))
        d.draw(screen)

        pxls = pygame.surfarray.pixels3d(screen)
        pxls_ref = pygame.surfarray.pixels3d(reference)

        np.testing.assert_almost_equal(
            pygame.surfarray.pixels3d(screen), 
            pygame.surfarray.pixels3d(reference)
            )


    @forEach("n",lambda:iter(range(4,7)))
    @useParameters("xys",["n"],lambda n:10*np.round(np.random.uniform(1,9,(n,2))))
    @forEach("arrow",lambda:iter([0,5,10]))
    def _characterize(self, xys, arrow):
        size = (100,100)

        e = Entity()
        e.add_component(GuiElement())
        d = e.add_component(DrawPath("draw",arrow))
        for xy in xys:
            e.add_entity(self._support_point(*xy))

        screen = pygame.Surface(size)
        screen.fill((255,255,255))
        d.draw(screen)
        pygame.image.save(screen, os.path.dirname(__file__) + 
            "/characterization/draw_path_%s_%s.png" % 
                (
                    "_".join((",".join(map(str,xy))) for xy in xys),
                    str(arrow))
                )

def main(module_name):
    if module_name == "__main__":
        t = TestDrawPath()
        import sys
        if sys.argv[-1] == "characterize":
            t._characterize()

main(__name__)

