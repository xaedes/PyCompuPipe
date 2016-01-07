#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import math
import numpy as np

from pycompupipe.other import MathUtils

from testing import *
from funcy import partial

class TestMathUtils():

    @forEach("radians", partial(generateRandomNormals,0,1), 10)
    @forEach("n_2pi", lambda:iter(range(0,10)))
    def test_rotation_matrix_equivalence(self, radians, n_2pi):
        np.testing.assert_almost_equal(
            MathUtils.rotation_matrix(radians),
            MathUtils.rotation_matrix(radians+n_2pi*math.pi*2)
            )

    def test_rotation_matrix_trivial(self):
        np.testing.assert_almost_equal(
            MathUtils.rotation_matrix(0),
            np.eye(2)
            )
        np.testing.assert_almost_equal(
            MathUtils.rotation_matrix(math.pi / 2),
            np.array([[0,-1],[1,0]])
            )
        np.testing.assert_almost_equal(
            MathUtils.rotation_matrix(math.pi),
            np.array([[-1,0],[0,-1]])
            )
        np.testing.assert_almost_equal(
            MathUtils.rotation_matrix(3*math.pi/2),
            np.array([[0,1],[-1,0]])
            )
        
    @forEach("n",lambda:iter(range(2,3)))
    @useParameters("points",["n"],lambda n:10*np.round(np.random.uniform(1,9,(n,2))))
    @forEach("radians", partial(generateRandomNormals,0,1), 10)
    def test_rotate(self, points, radians):
        np.testing.assert_almost_equal(
            MathUtils.rotate(MathUtils.rotate(points, radians), -radians),
            points
            )

    def test_rotate_trivial(self):
        np.testing.assert_almost_equal(
            MathUtils.rotate(np.array([[1,0]]),0),
            np.array([[1,0]])
            )
        np.testing.assert_almost_equal(
            MathUtils.rotate(np.array([[1,0]]),math.pi / 2),
            np.array([[0,1]])
            )
        np.testing.assert_almost_equal(
            MathUtils.rotate(np.array([[1,0]]),2 * math.pi / 2),
            np.array([[-1,0]])
            )
        np.testing.assert_almost_equal(
            MathUtils.rotate(np.array([[1,0]]),3 * math.pi / 2),
            np.array([[0,-1]])
            )
