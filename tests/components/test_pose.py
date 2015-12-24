#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division

import math
from funcy import partial
from testing import *

from pyecs import *
from pycompupipe.components import Pose



class TestPose():
    def test_usage(self):
        # specify x and y
        p = Pose(1,2)
        assert p.x == 1
        assert p.y == 2
        assert p.angle == 0 # default value if not specified

        # specify x, y and angle
        p = Pose(1,2,3)
        assert p.x == 1
        assert p.y == 2
        assert p.angle == 3

    @forEach("x",partial(generateRandomNormals,0,1),5)
    @forEach("y",partial(generateRandomNormals,0,1),5)
    @forEach("d",partial(generateUniformRandoms,0,1),5)
    @forEach("angle",partial(generateUniformRandoms,0,2*math.pi),5)
    def test_distance_to(self,x,y,d,angle):
        cs,sn = math.cos(angle),math.sin(angle)
        p1 = Pose(x,y)
        p2 = Pose(x+cs*d,y+sn*d)
        assert abs(p1.distance_to(p2) - d) < 1e-5

    @forEach("x",partial(generateRandomNormals,0,1),5)
    @forEach("y",partial(generateRandomNormals,0,1),5)
    @forEach("d",partial(generateUniformRandoms,0,1),5)
    @forEach("angle",partial(generateUniformRandoms,0,2*math.pi),5)
    def test_distance_to_xy(self,x,y,d,angle):
        cs,sn = math.cos(angle),math.sin(angle)
        p1 = Pose(x,y)
        x2,y2 = x+cs*d,y+sn*d
        assert abs(p1.distance_to_xy(x2,y2) - d) < 1e-5

    @forEach("x",partial(generateRandomNormals,0,1),5)
    @forEach("y",partial(generateRandomNormals,0,1),5)
    @forEach("dx",partial(generateRandomNormals,0,1),5)
    @forEach("dy",partial(generateRandomNormals,0,1),5)
    def test_vector_to(self,x,y,dx,dy):
        p1 = Pose(x,y)
        p2 = Pose(x+dx,y+dy)
        res = p1.vector_to(p2)
        assert abs(res[0] - dx) < 1e-5
        assert abs(res[1] - dy) < 1e-5

    @forEach("x",partial(generateRandomNormals,0,1),5)
    @forEach("y",partial(generateRandomNormals,0,1),5)
    @forEach("dx",partial(generateRandomNormals,0,1),5)
    @forEach("dy",partial(generateRandomNormals,0,1),5)
    def test_vector_to_xy(self,x,y,dx,dy):
        p1 = Pose(x,y)
        res = p1.vector_to_xy(x+dx,y+dy)
        assert abs(res[0] - dx) < 1e-5
        assert abs(res[1] - dy) < 1e-5
