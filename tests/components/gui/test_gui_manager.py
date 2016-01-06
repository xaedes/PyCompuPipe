#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

from testing import *

from pyecs import *
from pycompupipe.other import Event
from pycompupipe.components import GuiManager, GuiElement

import mock


class TestGuiManager():

    def test_register_manager(self):
        Entity._reset_global()
        Component._reset_global()
        e = Entity()
        gui_manager = e.add_component(GuiManager())
        
        e2 = Entity()
        gui_element = e2.add_component(GuiElement(position=(0,0),size=(100,50),anchor=(0,0)))
        e.add_entity(e2)

        e.fire_callbacks("awake")

        assert gui_element.manager == gui_manager
        
    def test_query1(self):
        Entity._reset_global()
        Component._reset_global()
        e = Entity()
        gui_manager = e.add_component(GuiManager())
        
        e2 = Entity()
        gui_element = e2.add_component(GuiElement(position=(0,0),size=(100,50),anchor=(0,0)))
        e.add_entity(e2)

        e.fire_callbacks("awake")

        assert gui_manager.query1(0,0) == gui_element
        assert gui_manager.query1(50,25) == gui_element
        assert gui_manager.query1(100,0) == gui_element
        assert gui_manager.query1(150,0) == None

    @forEach("callback_name",lambda:iter(["mousemotion","mousebuttonup","mousebuttondown"]))
    def test_event_propagation(self, callback_name):
        Entity._reset_global()
        Component._reset_global()
        e = Entity()
        e.add_component(GuiManager())

        callback2 = mock.MagicMock()
        callback3 = mock.MagicMock()
        
        e2 = Entity()
        e2.add_component(GuiElement(position=(0,0),size=(100,50),anchor=(0,0)))
        e2.register_callback(callback_name, callback2)
        e.add_entity(e2)

        e3 = Entity()
        e3.add_component(GuiElement(position=(0,25),size=(100,50),anchor=(0,0)))
        e3.register_callback(callback_name, callback3)
        e.add_entity(e3)
        e.fire_callbacks("awake")


        # note: e2 and e3 overlap from (0,25) to (100,50)

        event_inside_e2 = Event(pos=(50,10))  
        event_inside_e2e3 = Event(pos=(50,30))
        event_inside_e3 = Event(pos=(50,60))


        e.fire_callbacks(callback_name, event_inside_e2)
        callback2.assert_called_once_with(event_inside_e2)
        callback3.assert_not_called()

        callback2.reset_mock()
        callback3.reset_mock()
        e.fire_callbacks(callback_name, event_inside_e2e3)
        callback2.assert_called_once_with(event_inside_e2e3)
        callback3.assert_called_once_with(event_inside_e2e3)

        callback2.reset_mock()
        callback3.reset_mock()
        e.fire_callbacks(callback_name, event_inside_e3)
        callback2.assert_not_called()
        callback3.assert_called_once_with(event_inside_e3)

    def test_fetch_mouse(self):
        e0 = Entity()
        e1 = e0.add_entity(Entity())
        manager = e0.add_component(GuiManager())
        element = e1.add_component(GuiElement((0,0),(10,10)))
        e0.fire_callbacks("awake")
        assert element.always_fetch_mouse == False

        mocked_mousemotion = mock.MagicMock()
        e1.register_callback("mousemotion", mocked_mousemotion)

        event_inside = Event(pos=(5,5))
        event_outside = Event(pos=(15,5))

        mocked_mousemotion.reset_mock()
        element.always_fetch_mouse = False
        e0.fire_callbacks("mousemotion",event_inside)
        mocked_mousemotion.assert_called_once_with(event_inside)
        
        mocked_mousemotion.reset_mock()
        element.always_fetch_mouse = False
        e0.fire_callbacks("mousemotion",event_outside)
        mocked_mousemotion.assert_not_called()

        mocked_mousemotion.reset_mock()
        element.always_fetch_mouse = True
        e0.fire_callbacks("mousemotion",event_inside)
        mocked_mousemotion.assert_called_once_with(event_inside)
        
        mocked_mousemotion.reset_mock()
        element.always_fetch_mouse = True
        e0.fire_callbacks("mousemotion",event_outside)
        mocked_mousemotion.assert_called_once_with(event_outside)
