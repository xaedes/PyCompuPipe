#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from pyecs import *
from pycompupipe.components import DrawProcess

import mock
import pygame
import re
import os.path

from testing import *

class TestDrawProcess():

    @mock.patch("pycompupipe.components.drawing.draw_process.DrawProcess.draw")
    def test_event(self, mocked_draw):
        e = Entity()
        d = DrawProcess("draw",10)
        e.add_component(d)
        screen = mock.NonCallableMock()
        e.fire_callbacks("draw", screen)
        mocked_draw.assert_called_once_with(screen)

    @forFiles("fn","characterization/draw_process_*.png",os.path.dirname(__file__))
    def test_draw(self, fn):
        reference = pygame.image.load(fn)
        size = reference.get_size()

        d = DrawProcess("draw")
        screen = pygame.Surface(size)
        d.draw(screen)

        np.testing.assert_almost_equal(
            pygame.surfarray.pixels3d(screen), 
            pygame.surfarray.pixels3d(reference)
            )

    @forEach("w",lambda:iter([10,20,100]))
    @forEach("h",lambda:iter([10,20,100]))
    def _characterize(self,w,h):
        size = (w,h)
        d = DrawProcess("draw")
        screen = pygame.Surface(size)
        d.draw(screen)
        pygame.image.save(screen, os.path.dirname(__file__) + 
            "/characterization/draw_process_%d_%d.png" % size)

def main(module_name):
    if module_name == "__main__":
        t = TestDrawProcess()
        import sys
        if sys.argv[-1] == "characterize":
            t._characterize()

main(__name__)

