#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import

import math
from pyecs import *
# from pycompupipe.components import Selectable
from pycompupipe.other import child_support_points
from . import Selectable, FetchMouseCallbacksWhileSelected, Draggable, SelectedWhileMouseDown
from .. import GuiElement 
# from . import UserDefinesPath
# from pyecs.components import *

# print GuiElement.
# help(GuiElement)

class UserCanDefinePath(Component):
    """docstring for UserCanDefinePath"""
    def __init__(self, *args,**kwargs):
        super(UserCanDefinePath, self).__init__(*args,**kwargs)

        self.active = False
        self.last_point = None

    @component_callback
    def component_attached(self):
        self.gui = self.entity.get_component(GuiElement)
        self.selectable = self.entity.get_component(Selectable)


    @callback
    def selected(self, selectable):
        self.active = True

        self._clear_support_points()
        self.entity.add_entity(self._support_point(0,0,relative=True))
        x,y = self.entity.fire_callbacks_pipeline("position", (0.5,0.5))

        self.last_point = self.entity.add_entity(self._support_point(x,y)).get_component(GuiElement)
        
        self._redraw()

    @callback
    def deselected(self, selectable):
        self.active = False
        self._make_draggable()

        print "i got deselected", self


    @callback
    def mouseclick(self, event):
        LEFT, RIGHT = 1, 3 
        if event.button == LEFT:
            if self.active:
                under_cursor = filter(lambda gui:not(gui.entity), self.gui.manager.query(*event.pos))
                if len(self.gui.manager.query(*event.pos)) <= 1:
                    self.last_point = self.entity.add_entity(self._support_point(*event.pos)).get_component(GuiElement)
                    self._redraw()
            else:
                self.selectable.selected = True

        elif event.button == RIGHT:
            self.last_point.entity.remove_from_parent()

            supps = child_support_points(self.entity)
            if len(supps) > 0:
                self.last_point = supps[-1].get_component(GuiElement)
            else:
                self.last_point = False
                self.selectable.selected = False
            print "self.last_point", self.last_point
            self._redraw()

        self.entity.find_root().print_structure()

    @callback
    def mousemotion(self, event):
        if self.active and self.last_point:
            x,y = event.pos
            x = math.floor(x/self.gui.snap_to_grid)*self.gui.snap_to_grid
            y = math.floor(y/self.gui.snap_to_grid)*self.gui.snap_to_grid
            self.last_point.position = (x,y)
            self._redraw()
            self.entity.find_root().print_structure()

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
            e.add_component(Selectable())
            e.add_component(SelectedWhileMouseDown())
            e.add_component(FetchMouseCallbacksWhileSelected())
            e.add_component(Draggable())
