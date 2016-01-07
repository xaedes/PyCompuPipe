#!/usr/bin/env python2
# -*- coding: utf-8 -*-


def is_support_point(entity):
    from pycompupipe.components import GuiElement
    return (entity.has_tag("support_point") and
            entity.has_component(GuiElement))

def child_support_points(entity):
    return filter(is_support_point,entity.children)
    