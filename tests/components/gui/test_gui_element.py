#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

from funcy import partial
from testing import *

from pyecs import *
from pycompupipe.components import GuiElement


class TestGuiElement():
    def test_usage(self):
        e = Entity()
        g = e.add_component(GuiElement())
        e.fire_callbacks("awake")
        assert g.position == (0,0)
        assert g.size == (0,0)
        assert g.anchor == (0,0)
        assert g.rect() == (0,0,0,0)

    def test_anchor1(self):
        e = Entity()
        g = e.add_component(GuiElement((0,0),(100,50),(0,0)))
        e.fire_callbacks("awake")

        assert g.position == (0,0)
        assert g.size == (100,50)
        assert g.anchor == (0,0)
        assert g.rect() == (0,0,100,50)

    def test_anchor2(self):
        e = Entity()
        g = e.add_component(GuiElement((0,0),(100,50),(0.5,0.5)))
        e.fire_callbacks("awake")

        assert g.position == (0,0)
        assert g.size == (100,50)
        assert g.anchor == (0.5,0.5)
        assert g.rect() == (-50,-25,100,50)

    def test_anchor3(self):
        e = Entity()
        g = e.add_component(GuiElement((0,0),(100,50),(1,1)))
        e.fire_callbacks("awake")

        assert g.position == (0,0)
        assert g.size == (100,50)
        assert g.anchor == (1,1)
        assert g.rect() == (-100,-50,100,50)
    def test_anchor4(self):
        e = Entity()
        g = e.add_component(GuiElement((0,0),(100,50),(0,1)))
        e.fire_callbacks("awake")

        assert g.position == (0,0)
        assert g.size == (100,50)
        assert g.anchor == (0,1)
        assert g.rect() == (0,-50,100,50)

    def test_relative_pos1(self):
        e = Entity()
        g = e.add_component(GuiElement((50,20),(100,50),(0,0)))

        e2 = Entity()
        g2 = e2.add_component(GuiElement((10,10),(5,5),(0,0),relative_position=True))
        e2.fire_callbacks("awake")
        e.add_entity(e2)

        e.fire_callbacks("awake")

        assert g2.rect() == (60,30,5,5)

    def test_relative_pos2(self):
        e = Entity()
        g = e.add_component(GuiElement((50,20),(100,50),(0.5,0.5)))

        e2 = Entity()
        g2 = e2.add_component(GuiElement((10,10),(5,5),(0,0),relative_position=True))
        e2.fire_callbacks("awake")
        e.add_entity(e2)

        e.fire_callbacks("awake")

        assert g.rect() == (0,-5,100,50)
        assert g2.rect() == (10,5,5,5)

    def test_relative_pos3(self):
        e = Entity()
        g = e.add_component(GuiElement((50,20),(100,50),(0.5,0.5)))

        e2 = Entity()
        g2 = e2.add_component(GuiElement((10,10),(5,5),(1,1),relative_position=True))
        e2.fire_callbacks("awake")
        e.add_entity(e2)

        e.fire_callbacks("awake")

        assert g.rect() == (0,-5,100,50)
        assert g2.rect() == (5,0,5,5)


    @forEach("x",partial(generateRandomNormals,0,1),5)
    @forEach("y",partial(generateRandomNormals,0,1),5)
    @forEach("w",partial(generateUniformRandoms,0,1),5)
    @forEach("h",partial(generateUniformRandoms,0,1),5)
    @forEach("i",partial(generateUniformRandoms,-1,2),5)
    @forEach("j",partial(generateUniformRandoms,-1,2),5)
    def test_is_in(self,x,y,w,h,i,j):
        g = GuiElement((x,y),(w,h),(0,0))
        if 0 <= i and i <= 1 and 0 <= j and j <= 1:
            assert g.is_in((x+i*w,y+j*h)) == True
        else:
            assert g.is_in((x+i*w,y+j*h)) == False


    def test_snap_to_grid1(self):
        g = GuiElement((0,0),(16,16),(0,0),snap_to_grid=16)
        assert g.rect() == (0,0,16,16)

    def test_snap_to_grid2(self):
        g = GuiElement((10,10),(16,16),(0,0),snap_to_grid=16)
        assert g.rect() == (0,0,16,16)

    def test_snap_to_grid3(self):
        g = GuiElement((16,16),(16,16),(0,0),snap_to_grid=16)
        assert g.rect() == (16,16,16,16)

    def test_snap_to_grid4(self):
        g = GuiElement((16,16),(20,20),(0,0),snap_to_grid=16)
        assert g.rect() == (16,16,16,16)

    def test_snap_to_grid5(self):
        g = GuiElement((16,16),(24,24),(0,0),snap_to_grid=16)
        assert g.rect() == (16,16,32,32)

    def test_snap_to_grid6(self):
        g = GuiElement((16,16),(32,32),(0,0),snap_to_grid=16)
        assert g.rect() == (16,16,32,32)

    @forEach("x",partial(generateRandomNormals,0,1),10)
    @forEach("y",partial(generateRandomNormals,0,1),10)
    def test_position_pipeline(self,x,y):
        e = Entity()
        g = GuiElement((x,y),(0,0),(0,0))
        e.add_component(g)
        assert e.fire_callbacks_pipeline("position") == (x,y)

    @forEach("x",partial(generateRandomNormals,0,1),10)
    @forEach("y",partial(generateRandomNormals,0,1),10)
    def test_position_pipeline_inner_anchor(self,x,y):
        e = Entity()
        g = GuiElement((x,y),(20,10),(0.5,0.5))
        # anchor (0.5,0.5) means (x,y) is position of center of GuiElement

        e.add_component(g)

        # no inner anchor means we want top-left of gui-element
        np.testing.assert_almost_equal(
            e.fire_callbacks_pipeline("position"),
            (x-10,y-5))

        # explicitely request top-left of gui-element
        np.testing.assert_almost_equal(
            e.fire_callbacks_pipeline("position",(0,0)),
            (x-10,y-5))

        # explicitely request center-left of gui-element
        np.testing.assert_almost_equal(
            e.fire_callbacks_pipeline("position",(0,0.5)),
            (x-10,y))

        # explicitely request bottom-left of gui-element
        np.testing.assert_almost_equal(
            e.fire_callbacks_pipeline("position",(0,1)),
            (x-10,y+5))

        # explicitely request top-center of gui-element
        np.testing.assert_almost_equal(
            e.fire_callbacks_pipeline("position",(0.5,0)),
            (x,y-5))

        # explicitely request center of gui-element
        np.testing.assert_almost_equal(
            e.fire_callbacks_pipeline("position",(0.5,0.5)),
            (x,y))

        # explicitely request bottom-center of gui-element
        np.testing.assert_almost_equal(
            e.fire_callbacks_pipeline("position",(0.5,1)),
            (x,y+5))

        # explicitely request top-right of gui-element
        np.testing.assert_almost_equal(
            e.fire_callbacks_pipeline("position",(1,0)),
            (x+10,y-5))

        # explicitely request center-right of gui-element
        np.testing.assert_almost_equal(
            e.fire_callbacks_pipeline("position",(1,0.5)),
            (x+10,y))

        # explicitely request bottom-right of gui-element
        np.testing.assert_almost_equal(
            e.fire_callbacks_pipeline("position",(1,1)),
            (x+10,y+5))

