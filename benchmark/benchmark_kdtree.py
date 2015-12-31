#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division    # Standardmäßig float division - Ganzzahldivision kann man explizit mit '//' durchführen
import math

import numpy as np
from scipy.spatial import cKDTree,KDTree

from time import time

from pprint import pprint

size = 100

def benchmark_construction(constructor,data):
    start_time = time()

    n = 0
    while True:
        tree = constructor(data)

        n += 1
        # check every 10 operations: abort if running for at least 5 seconsd
        if n % 10 == 0 and time() - start_time > 5: 
            break
        if n >= 1000:
            break

    end_time = time()

    time_per = (end_time-start_time) / n
    op_per_sec = 1/time_per
    # print "%s, constructions per second: %.2f" % (constructor.__name__, op_per_sec)
    return op_per_sec

def benchmark_query(constructor,data,r,p,num_queries=1000):
    tree = constructor(data)

    queries = np.random.uniform(0,size,(num_queries,2))

    start_time = time()

    n = 0
    while True:
        x,y = queries[n]
        # rect
        xy_list = tree.query_ball_point((x,y),r,p)
        n += 1
        # check every 10 operations: abort if running for at least 5 seconsd
        if n % 10 == 0 and time() - start_time > 5: 
            break
        if n >= queries.shape[0]:
            break

    end_time = time()

    time_per = (end_time-start_time) / n
    op_per_sec = 1/time_per
    # print "%s, operations per second: %.2f" % (constructor.__name__, op_per_sec)
    return op_per_sec

def benchmark(constructor,data):
    result = {
        "construction":benchmark_construction(constructor,data),
        "query_rect":benchmark_query(constructor,data,10,np.inf),
        "query_circle":benchmark_query(constructor,data,10,2),
    }
    return result

def main(module_name):
    if module_name == '__main__':
        results = {}
        for num_points in [0,10,100,1000,10000,100000]:
            data = np.random.uniform(0,size,(100,2))
            results[num_points] = (benchmark(KDTree, data), benchmark(cKDTree, data))

        pprint(results)

main(__name__)