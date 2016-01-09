#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import

import math
from pyecs import *
from pycompupipe.components import ProcessOutput
from pycompupipe.other import child_support_points
from pycompupipe.components import Selectable, FetchMouseCallbacksWhileSelected, Draggable, SelectedWhileMouseDown
from pycompupipe.components import GuiElement 
# from . import UserDefinesPath
# from pyecs.components import *

# print GuiElement.
# help(GuiElement)

class UserCanDefineConnection(Component):
    """docstring for UserCanDefineConnection"""
    def __init__(self, opposing_connector_type, *args,**kwargs):
        super(UserCanDefineConnection, self).__init__(*args,**kwargs)

        self.active = False
        self.opposing_connector_type = opposing_connector_type
        self.last_point = None
        self.support_points = []

    @component_callback
    def component_attached(self):
        self.gui = self.entity.get_component(GuiElement)
        self.selectable = self.entity.get_component(Selectable)


    @callback
    def start(self):
        self.reset()

    @callback
    def selected(self, selectable):
        self.active = True

        self.reset()
        # self._clear_support_points()
        # self.entity.add_entity(self._support_point(0,0,relative=True))
        x,y = self.entity.fire_callbacks_pipeline("position", (0.5,0.5))

        self.last_point.relative_position = False
        self.last_point.position = (x,y)

        # self.last_point = self.entity.add_entity(self._support_point(x,y)).get_component(GuiElement)
        
        self.gui.manager.exclusive_elements.add(self.gui)

        self._redraw()

    @callback
    def deselected(self, selectable):
        self.active = False
        self.last_point = None
        self._make_draggable()

        self.gui.manager.exclusive_elements.remove(self.gui)

    @callback
    def mouseclick(self, event):
        LEFT, RIGHT = 1, 3 
        if event.button == LEFT:
            if self.active:
                under_cursor = filter(lambda gui:gui!=self.gui and gui!=self.last_point, self.gui.manager.query(*event.pos))

                opposing = filter(lambda gui:gui.entity.has_component(self.opposing_connector_type),under_cursor)
                print opposing
                if len(opposing) > 0:
                    # create connection to opposing connector
                    opposing = opposing[0]
                    self._create_connection(opposing)

                elif len(under_cursor) == 0:
                    # add support point
                    self.last_point = self.entity.add_entity(self._support_point(*event.pos)).get_component(GuiElement)
                else:
                    print under_cursor[0].entity
                self._redraw()
            else:
                # start defining path
                self.selectable.selected = True

        elif event.button == RIGHT:
            supps = child_support_points(self.entity)

            if len(supps) > 2:
                # discard last point
                self._discard_last_point()
            else:
                # abort
                self._abort()

            self._redraw()
            

        # self.entity.find_root().print_structure()

    def _create_connection(self, opposing_connector):
        # set last point to opposing connector
        self.last_point.relative_position = True
        self.last_point.position = (0,0)
        self.last_point.relative_gui_element = opposing_connector

        self.selectable.selected = False

    def _discard_last_point(self):
        self.last_point.entity.remove_from_parent()

        supps = child_support_points(self.entity)
        self.last_point = supps[-1].get_component(GuiElement)

    def _abort(self):
        self.reset()
        self.selectable.selected = False


    @callback
    def mousemotion(self, event):
        if self.active and self.last_point:
            x,y = event.pos
            x = int(0.5+x/self.gui.snap_to_grid)*self.gui.snap_to_grid
            y = int(0.5+y/self.gui.snap_to_grid)*self.gui.snap_to_grid
            self.last_point.position = (x,y)
            self._redraw()
            # self.entity.find_root().print_structure()

    def _redraw(self):
        self.entity.find_root().draw()

    def _clear_support_points(self):
        for support in child_support_points(self.entity):
            self.entity.remove_entity(support)

    def _support_point(self,x,y,relative=False):
        e = Entity()
        size = self.gui.snap_to_grid
        gui = e.add_component(GuiElement((x,y),(size,size),(0.5,0.5),relative))
        gui.register_manager(self.gui.manager)

        e.register_callback("dragging", self.entity.find_root().draw)

        e.add_tag("support_point")
        return e

    def _make_draggable(self):
        for e in child_support_points(self.entity):
            if not e.get_component(GuiElement).relative_position:
                e.add_component(Selectable())
                e.add_component(SelectedWhileMouseDown())
                e.add_component(FetchMouseCallbacksWhileSelected())
                e.add_component(Draggable())
