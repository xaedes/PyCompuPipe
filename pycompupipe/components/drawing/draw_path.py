#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
import math

import numpy as np
from pyecs import *
from pycompupipe.other import MathUtils
from pycompupipe.components import GuiElement
import pygame

class DrawPath(Component):
    """docstring for DrawPath"""
    def __init__(self, draw_event_name, arrow=0, color=(0,0,0), *args,**kwargs):
        super(DrawPath, self).__init__(*args,**kwargs)
        self.draw_event_name = draw_event_name
        self.arrow = arrow
        self.color = color

    @component_callback
    def component_attached(self):
        self.entity.register_callback(self.draw_event_name, self.draw)

    def draw(self, screen):
        points = []

        # build path from support points
        for support in self.entity.find_entities(lambda e: e.has_tag("support_point")):
            gui = support.get_component(GuiElement)
            x,y = gui.entity.fire_callbacks_pipeline("position")

            points.append((x,y))

        # draw path
        pygame.draw.aalines(screen, self.color, False, points)

        if self.arrow > 0:
            # define arrow points
            above = -0.4*self.arrow, -0.4*self.arrow
            below = -0.4*self.arrow, +0.4*self.arrow
            points_arrow = np.array([above,(0,0),below])

            # calculate angle of arrow
            dx, dy = np.diff(points[-2:],axis=0)[0]
            angle = math.atan2(float(dy),float(dx))

            # rotate and position arrow points
            points_arrow = MathUtils.rotate(points_arrow, angle)
            points_arrow += points[-1]

            # draw arrow            
            pygame.draw.aalines(screen, self.color, False, points_arrow)
