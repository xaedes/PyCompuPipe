#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from pyecs import *
from pycompupipe.components import Pygame, BlockingPygameEventPump

import mock
from testing import *
from funcy import partial

class Event(object):
    """docstring for Event"""
    def __init__(self, type):
        super(Event, self).__init__()
        self.type = type
        

def generateEvents():
    # first all events that are not "quit"
    for event_type, name in BlockingPygameEventPump.event_mappings.iteritems():
        if name != "quit":
            yield Event(event_type)

    # now "quit" events
    for event_type, name in BlockingPygameEventPump.event_mappings.iteritems():
        if name == "quit":
            yield Event(event_type)

        

class TestBlockingPygameEventPump():
    @mock.patch("pycompupipe.components.pygame_components.pygame_component.Pygame.setup")
    @mock.patch("pygame.event.wait",new_callable=lambda:partial(lambda it:it.next(),generateEvents()))
    def test(self, mocked_event_wait, mocked_setup):
        e = Entity()
        pump = BlockingPygameEventPump()
        e.add_component(pump)

        callbacks = {}
        for callback_key in BlockingPygameEventPump.event_mappings.itervalues():
            callbacks[callback_key] = mock.MagicMock()

            e.register_callback(callback_key, callbacks[callback_key])

        assert pump.done == False
        pump.pump()

        # quit callback from BlockingPygameEventPump sets done to True
        assert pump.done == True 

        for key,callback in callbacks.iteritems():
            print key
            assert callback.called

