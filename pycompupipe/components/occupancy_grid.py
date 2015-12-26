#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
from numbers import Number
import math

from pyecs import *
from . import Pygame

import numpy as np
import pygame

from collections import defaultdict

class OccupancyGrid(Component):
    """docstring for OccupancyGrid"""
    def __init__(self, resolution, *args,**kwargs):
        super(OccupancyGrid, self).__init__(*args,**kwargs)
        self.resolution = resolution
        self.size = None
        self.occupied = defaultdict(lambda:False)
        self.blocked = defaultdict(list) # contains list of x,y tuples

    @component_callback
    @with_components(required=[Pygame])
    def component_attached(self, pygame):
        self.resized(pygame)

    @callback
    def resized(self, pygame):
        self.size = tuple(map(lambda i:int(math.ceil(i / self.resolution)),iter(pygame.size)))
        

    def occupy_block(self, rect):
        x,y,w,h = rect
        x2,y2 = x+w+1,y+h+1
        x,y,x2,y2 = map(lambda i:int(math.floor(i / self.resolution)),[x,y,x2,y2])
        w,h=x2-x,y2-y
        for i in xrange(x,x+w+1):
            self.blocked[(i,y)].append((0,1)) # block south
            self.blocked[(i,y+h)].append((0,-1)) # block north
            for j in xrange(y,y+h+1):
                self.blocked[(x,j)].append((1,0)) # block west
                self.blocked[(x+w,j)].append((-1,0)) # block east
                self.occupied[(i,j)] = True

    def clear(self):
        self.occupied.clear()
        self.blocked.clear()

    @callback
    def draw_debug(self, screen):
        screen.fill((0,0,0,0))
        for x in xrange(self.size[0]):
            for y in xrange(self.size[1]):
                if self.occupied[(x,y)]:
                    color = (255,0,0)
                else:
                    color = (0,200,0)
                self._draw_dot(screen, (x,y), color)
                neighbors = [(-1,0),(1,0),(0,-1),(0,1)]
                color = (255,0,0)
                k = 0.5
                for n in neighbors:
                    if n in self.blocked[(x,y)]:
                        self._draw_line(screen, (x,y), (x+k*n[0],y+k*n[1]), color)

    def _draw_line(self, screen, p0, p1, color):
        p0 = (p0[0]*self.resolution,p0[1]*self.resolution)
        p1 = (p1[0]*self.resolution,p1[1]*self.resolution)
        pygame.draw.line(screen, color, p0, p1, 1)

    def _draw_dot(self, screen, pos, color):
        x,y = pos
        pos = (x*self.resolution,y*self.resolution)
        # screen.set_at((x*self.resolution,y*self.resolution),color)
        pygame.draw.circle(screen, color, pos, 2, 0)
        # screen.
        # screen.set_at((x*self.resolution+1,y*self.resolution),color)
        # screen.set_at((x*self.resolution,y*self.resolution+1),color)
        # screen.set_at((x*self.resolution-1,y*self.resolution),color)
        # screen.set_at((x*self.resolution,y*self.resolution-1),color)


    @callback
    def update_occupancy(self, grid):
        grid.clear()
