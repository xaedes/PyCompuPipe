#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import numpy as np

from pyecs import *
from pyecs.components import *
from components import *

from gui_application import GuiApplication

from common import Utils

import pygame

class Gui(GuiApplication):
    """docstring for Experiment"""
    def __init__(self):
        self.width = 640
        self.height = 480
        self.grid_resolution = 16

        super(Gui, self).__init__()

    def setup_main_entity(self):
        super(Gui, self).setup_main_entity()

        self.entity.add_component(Pygame(
            size=(self.width,self.height),
            caption="PyCompuPipe",
            flags=pygame.DOUBLEBUF | pygame.RESIZABLE))
        self.entity.add_component(DrawOnResized())
        self.entity.add_component(OccupancyGrid(self.grid_resolution))
        self.entity.add_component(ColorFill("draw",color=(255,255,255)))
        self.entity.add_component(DrawGrid("draw",self.grid_resolution))
        # def print_args(*args):
        #     print args
        # self.entity.register_callback("videoresize",print_args)

        self.entity.add_entity(self.create_screen_filling_surface((self.width, self.height),"lines"))
        self.entity.add_entity(self.create_screen_filling_surface((self.width, self.height),"blocks"))
        self.entity.add_entity(self.create_screen_filling_surface((self.width, self.height),"debug"))
        for i in range(2,5):
            self.entity.add_entity(self.create_process(i))
        # self.entity.add_entity(self.create_process())
        self.entity.add_component(PropagateCallback([
            "draw","draw_blocks","draw_lines","redraw",
            "mousebuttondown","mousebuttonup","mousemotion",
            "update_occupancy"]))
        self.entity.fire_callbacks("awake")
        self.entity.fire_callbacks("redraw")
        self.entity.fire_callbacks("update_occupancy",self.entity.get_component(OccupancyGrid))
        self.entity.get_component(Pygame).draw()

        self.entity.print_structure()
        # self.entity.add_entity(PrintEntityStructure())

    def create_screen_filling_surface(self, size, name):
        e = Entity()
        e.add_component(PygameSurface(size,pygame.SRCALPHA))
        e.add_component(ResizeEventOnVideoresize("draw"))
        e.add_component(SurfaceDrawEvent("draw","draw_"+name,fire_at_root=True))
        e.add_component(ColorFill("draw_"+name,color=(0,0,0,0)))
        e.add_component(Pose(0,0))
        e.add_component(Size(size))
        e.add_component(Anchor(0))
        e.add_component(BlitSurface("draw"))
        e.fire_callbacks("awake")
        return e

    def create_process(self,i):
        e = Entity()
        process = e.add_component(Process(i,i))
        e.add_component(PropagateCallback([
            "draw","draw_blocks","draw_lines","redraw",
            "mousebuttondown","mousebuttonup","mousemotion",
            "update_occupancy"]))
        e.add_entity(self.create_process_gui((100,100),(100,1+(i+1)*self.grid_resolution),process))
        e.fire_callbacks("awake")
        return e

    def create_process_gui(self,pos,size,process):
        e = Entity()
        e.add_component(Pose(*pos))
        e.add_component(Size(size))
        e.add_component(Anchor(0.5))
        e.add_component(PygameSurface(size))
        draw_event = "draw_%i"%e.uid
        # e.add_component(SurfaceDrawEvent("awake",draw_event))
        e.add_component(SurfaceDrawEvent("redraw",draw_event))
        e.add_component(BoundingBox())
        e.add_component(OccupyingBoundingBox())
        e.add_component(OccupyingProcess())
        e.add_component(Selectable())
        e.add_component(Draggable())
        e.add_component(SnapToGrid(self.grid_resolution))
        e.add_component(PropagateCallback([draw_event,"draw_lines","mousebuttondown","mousebuttonup","mousemotion"]))
        # e.add_component(DrawProcessConnectors("draw_lines",padding=self.grid_resolution))
        def dragging(draggable):
            self.entity.fire_callbacks("update_occupancy",self.entity.get_component(OccupancyGrid))
            self.entity.get_component(Pygame).draw()

        e.register_callback("dragging", dragging)

        e.add_entity(self.create_box(size,draw_event))
        e.add_entity(self.create_process_input_gui(size,process.num_inputs))
        e.add_entity(self.create_process_output_gui(size,process.num_outputs))
        e.add_component(BlitSurface("draw_blocks"))
        e.fire_callbacks("awake")
        return e

    def create_box(self,size,draw_event):
        e = Entity()
        e.add_component(Pose(0,0))
        e.add_component(Size(size))
        e.add_component(Anchor(0))
        # e.add_component(Size((size[0]-1,size[1]-1)))
        e.add_component(BoundingBox())
        e.add_component(ColorFill(draw_event,color=(255,255,255)))
        e.add_component(DrawBoundingBox(draw_event,(0,0,0)))
        e.fire_callbacks("awake")
        return e

    def create_process_input_gui(self, size, num):
        e = Entity()
        e.add_component(PropagateCallback(["draw_lines","mousebuttondown","mousebuttonup","mousemotion"]))
        for i in range(num):
            inp = e.add_entity(self.create_process_input_connector_gui(0,self.grid_resolution * (i+2)))
            inp = inp.get_component(Pose)
        e.fire_callbacks("awake")
        return e

    def create_process_input_connector_gui(self, x, y):
        e = Entity()
        hitbox_height = 5
        e.add_component(Pose(x,y))
        e.add_component(PoseTransform())
        e.add_component(Size((self.grid_resolution,hitbox_height)))
        e.add_component(Anchor((1,0.5)))
        # e.add_component(Size((size[0]-1,size[1]-1)))
        e.add_component(BoundingBox())
        # e.add_component(DrawBoundingBox("draw_lines",(0,0,0)))
        e.add_component(Selectable())
        e.add_component(Draggable())
        e.add_component(SnapToGrid(self.grid_resolution))
        # x,y,w,h = bb.rect()
        e.add_component(DrawLine("draw_lines",[(0,0),(self.grid_resolution,0)],arrow=True))
        def onDragging(draggable):
            e.find_root().get_component(Pygame).draw()
        e.register_callback("dragging",onDragging)
        e.fire_callbacks("awake")
        return e
    def create_process_output_gui(self, size, num):
        e = Entity()
        e.add_component(PropagateCallback(["draw_lines","mousebuttondown","mousebuttonup","mousemotion"]))
        for i in range(num):
            inp = e.add_entity(self.create_process_output_connector_gui(size[0],self.grid_resolution * (i+2)))
            inp = inp.get_component(Pose)
        e.fire_callbacks("awake")
        return e

    def create_process_output_connector_gui(self, x, y):
        e = Entity()
        hitbox_height = 5
        e.add_component(Pose(x,y))
        e.add_component(PoseTransform())
        e.add_component(Size((self.grid_resolution,hitbox_height)))
        e.add_component(Anchor((0,0.5)))
        # e.add_component(Size((size[0]-1,size[1]-1)))
        e.add_component(BoundingBox())
        # e.add_component(DrawBoundingBox("draw_lines",(0,0,0)))
        e.add_component(Selectable())
        e.add_component(Draggable())
        e.add_component(SnapToGrid(self.grid_resolution))
        e.add_component(DrawLine("draw_lines",[(0,0),(self.grid_resolution,0)],arrow=True))
        def onDragging(draggable):
            e.find_root().get_component(Pygame).draw()
        e.register_callback("dragging",onDragging)
        e.fire_callbacks("awake")
        return e

            
    
def main(module_name):
    if module_name == "__main__":
        # profile(Gui)
        Gui()

main(__name__)
