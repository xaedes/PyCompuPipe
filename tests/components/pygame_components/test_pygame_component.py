#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from pyecs import *
from pycompupipe.components import Pygame

import mock
from testing import *
from collections import namedtuple

import pygame

class TestPygame():
    def test_init_default(self):
        c = Pygame()
        assert c.size == (640, 480)
        assert c.caption == "caption"
        assert c.flags == pygame.DOUBLEBUF

    def test_init(self):
        c = Pygame((1,2),"text",pygame.DOUBLEBUF | pygame.RESIZABLE)
        assert c.size == (1,2)
        assert c.caption == "text"
        assert c.flags == pygame.DOUBLEBUF | pygame.RESIZABLE

    @mock.patch('pycompupipe.components.pygame_components.pygame_component.Pygame.setup')
    @mock.patch('pygame.display.set_mode')
    def test_resizable_videoresize_callback(self, mocked_pygame_display_set_mode, mocked_setup):
        mocked_setup = callback(mocked_setup)

        e = Entity()
        c = Pygame(size=(1,1),flags=pygame.RESIZABLE)
        e.add_component(c)
        SizeEvent = namedtuple("Event",["size"])
        ActiveEvent = namedtuple("Event",["gain","state"])
        assert c.size != (5,5)
        e.fire_callbacks("videoresize",SizeEvent((5,5)))

        # we don't want to react to every videoresize, but wait for the user to finish resizing
        assert c.size == (1,1)
        assert mocked_pygame_display_set_mode.not_called

        mocked_pygame_display_set_mode.reset_mock()
        mocked_resized = mock.MagicMock()
        e.register_callback("resized", mocked_resized)

        # this event is generated after user is not holding the mouse down anymore to resize
        e.fire_callbacks("activeevent",ActiveEvent(1,2)) 
        assert c.size == (5,5)
        mocked_resized.assert_called_once_with(c)
        mocked_pygame_display_set_mode.assert_called_once_with(c.size, c.flags)
        assert c.screen == mocked_pygame_display_set_mode.return_value

    @mock.patch('pygame.init')
    @mock.patch('pygame.display.set_mode')
    @mock.patch('pygame.display.set_caption')
    def test_setup(self, mocked_pygame_display_set_caption, mocked_pygame_display_set_mode, mocked_pygame_init):
        c = Pygame()
        c.caption = "Foo"
        assert hasattr(c,"screen") == False

        c.setup()
        assert hasattr(c,"screen") == True
        assert mocked_pygame_init.called
        mocked_pygame_display_set_mode.assert_called_once_with(c.size,c.flags)
        mocked_pygame_display_set_caption.assert_called_once_with(c.caption)

    @mock.patch('pycompupipe.components.pygame_components.pygame_component.Pygame.setup')
    def test_setup_when_component_added(self, mocked_setup):
        mocked_setup = callback(mocked_setup)
        e = Entity()
        c = Pygame()

        # setup is called when component is added to entity
        mocked_setup.reset_mock()
        e.add_component(c)
        assert mocked_setup.called   

    @mock.patch('pycompupipe.components.pygame_components.pygame_component.Pygame.setup')
    def test_setup_callback(self, mocked_setup):
        mocked_setup = callback(mocked_setup)
        e = Entity()
        c = Pygame()
        e.add_component(c)
  
        # test callback
        mocked_setup.reset_mock()
        e.fire_callbacks("setup")
        assert mocked_setup.called 

    @mock.patch('pygame.quit')
    def test_quit(self, mocked_pygame_quit):
        c = Pygame()
        mocked_pygame_quit.reset_mock()
        c.quit(None)
        assert mocked_pygame_quit.called

    @mock.patch('pycompupipe.components.pygame_components.pygame_component.Pygame.setup')
    @mock.patch('pygame.display.flip')
    def test_draw(self, mocked_flip, mocked_setup):
        mocked_setup = callback(mocked_setup)

        e = Entity()
        c = e.add_component(Pygame())

        c.screen = mock.NonCallableMock()
        draw = mock.MagicMock()

        e.register_callback("draw", draw)

        c.draw()

        draw.assert_called_once_with(c.screen)
        mocked_flip.assert_called_once_with()
