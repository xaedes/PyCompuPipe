#!/usr/bin/env python2
# -*- coding: utf-8 -*-

class Event():
    def __init__(self,**kwargs):
        for key,value in kwargs.iteritems():
            setattr(self,key,value)
