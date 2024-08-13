#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/31 14:11
# @File    : getClosestPointOnMesh.py


import pymel.core as pm
import maya.api.OpenMaya as om
import maya.cmds as mc

def get_closest_point(pos, mesh):
    sel_array = om.MGlobal.getSelectionListByName(mesh)
    path = sel_array.getDagPath(0)
    mesh_fn = om.MFnMesh(path)
    point = om.MPoint(pos)
    closestPoint = mesh_fn.getClosestPoint(point, space=om.MSpace.kWorld)
    return list(closestPoint[0])[:-1]


sel = pm.ls(sl=True)
mesh = "head_geo_meshDrvModel"

for i in sel:
    pm.setAttr("{}.tz".format(i), 1.0e5)
    pos = pm.xform(i, q=True, ws=True, t=True)
    const_x = pos[0]
    const_y = pos[1]
    iter_value = pos
    for j in range(20):
        closest_pos = get_closest_point(iter_value, mesh)
        iter_value = [const_x, const_y, closest_pos[2]]

    pm.xform(i, ws=True, t=iter_value)





