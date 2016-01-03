#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from pyecs import *
from pycompupipe.components import DrawGrid

import mock
import pygame
import re
import os.path

from testing import *

class TestDrawGrid():

    @mock.patch("pycompupipe.components.drawing.draw_grid.DrawGrid.draw")
    def test_event(self, mocked_draw):
        e = Entity()
        d = DrawGrid("draw",10)
        e.add_component(d)
        screen = mock.NonCallableMock()
        e.fire_callbacks("draw", screen)
        mocked_draw.assert_called_once_with(screen)

    @forFiles("fn","characterization/draw_grid_*.png",os.path.dirname(__file__))
    def test_draw(self, fn):
        reference = pygame.image.load(fn)
        m = re.match(r"draw_grid_(\d+)\.png", os.path.basename(fn))
        resolution = int(m.group(1))
        size = reference.get_size()

        d = DrawGrid("draw",resolution,(0,0,0))
        screen = pygame.Surface(size)
        screen.fill((255,255,255))
        d.draw(screen)

        np.testing.assert_almost_equal(
            pygame.surfarray.pixels3d(screen), 
            pygame.surfarray.pixels3d(reference)
            )

    @forEach("resolution",lambda:iter([5,10,16]))
    def _characterize(self,resolution):
        size = (100,100)
        d = DrawGrid("draw",resolution,(0,0,0))
        screen = pygame.Surface(size)
        screen.fill((255,255,255))
        d.draw(screen)
        pygame.image.save(screen, os.path.dirname(__file__) + "/characterization/draw_grid_%d.png" % resolution)

def main(module_name):
    if module_name == "__main__":
        t = TestDrawGrid()
        import sys
        if sys.argv[-1] == "characterize":
            t._characterize()

main(__name__)

