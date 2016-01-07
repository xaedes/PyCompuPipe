#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np

from pyecs import *
from pycompupipe.other import Event
from pycompupipe.components import GuiElement, UserCanDefinePath

import mock

class TestUserCanDefinePath():

    def test(self):
        e = Entity()
        e.add_component(GuiElement())
        comp = e.add_component(UserCanDefinePath())
        e.draw = mock.MagicMock()

        LEFT, RIGHT = 1, 3 
        e.fire_callbacks("mouseclick", Event(pos=(0,0), button=1))

        assert comp.active == True
        assert len(e.children) == 2
        assert e.children[0].has_tag("support_point")
        assert e.children[1].has_tag("support_point")
        assert e.children[0].has_component(GuiElement)
        assert e.children[1].has_component(GuiElement)

        e.draw.assert_called_once_with()

        e.draw.reset_mock()
        e.fire_callbacks("mousemotion", Event(pos=(10,0)))
        assert comp.active == True
        assert len(e.children) == 2
        np.testing.assert_almost_equal(
            e.children[1].get_component(GuiElement).fire_callbacks_pipeline("position",(0.5,0.5)),
            (10,0))
        e.draw.assert_called_once_with()
        
        e.draw.reset_mock()
        e.fire_callbacks("mousemotion", Event(pos=(20,10)))
        assert comp.active == True
        assert len(e.children) == 2
        np.testing.assert_almost_equal(
            e.children[1].get_component(GuiElement).fire_callbacks_pipeline("position",(0.5,0.5)),
            (20,10))
        e.draw.assert_called_once_with()

        # e.draw.reset_mock()
        # e.fire_callbacks("mouseclick", Event(pos=(20,10), button=1))
        # assert comp.active == True
        # assert len(e.children) == 2
        # np.testing.assert_almost_equal(
        #     e.children[1].get_component(GuiElement).fire_callbacks_pipeline("position",(0.5,0.5)),
        #     (20,10))
        # e.draw.assert_called_once_with()

