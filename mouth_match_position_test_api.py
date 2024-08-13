#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/7 10:04
# @File    : mouth_match_position_test_api.py

import math
import maya.cmds as mc
import maya.api.OpenMaya as om


def getCurveClosestPointAndNormal(curve, point):
    tolerance = 0.1e-20
    sel = om.MSelectionList()
    sel.add(curve)
    path = sel.getDagPath(0)
    curve_fn = om.MFnNurbsCurve(path)
    point = om.MPoint(point[0], point[1], point[2])
    closestPointData = curve_fn.closestPoint(point, tolerance, om.MSpace.kWorld)
    normal_vector = curve_fn.normal(closestPointData[1])
    # normal_vector[0] = normal_vector[0] *-1
    # normal_vector[1] = normal_vector[1] *-1
    # normal_vector[2] = normal_vector[2] *-1
    closestPoint = closestPointData[0]
    return {"closestPoint": closestPoint, "normal": normal_vector}


def vector_to_euler(vector):
    mvector = om.MVector(vector[0], vector[1], vector[2])
    angles = (math.atan2(mvector.y, mvector.x),math.atan2(mvector.z, math.sqrt(mvector.x * mvector.x + mvector.y * mvector.y)),0.0)
    angles_degrees = tuple(math.degrees(angle) for angle in angles)
    return angles_degrees


def convertRotate(vector):
    v = math.atan2(vector[0], vector[2])
    rotate = math.degrees(v)
    result = 180 - rotate
    if result < 0:
        result = 360-result
    return result

#
# sel = mc.ls(sl=True)
#
#
# for i in sel:
#     data =  getCurveClosestPointAndNormal("nurbsCircle1", mc.getAttr("{}.t".format(i))[0])
#     loc = mc.spaceLocator()[0]
#     locN = mc.spaceLocator()[0]
#     cube = mc.polyCube()[0]
#     mc.parent(locN, loc)
#     mc.parent(cube, loc)
#     mc.setAttr("{}.t".format(loc), data["closestPoint"][0],data["closestPoint"][1],data["closestPoint"][2])
#     mc.setAttr("{}.t".format(locN), data["normal"][0],data["normal"][1],data["normal"][2])
#     vector = (data["normal"][0],data["normal"][1],data["normal"][2])
#     euler_angles = vector_to_euler(vector)
#     print euler_angles
#     mc.setAttr("{}.r".format(cube), euler_angles[0], euler_angles[1], euler_angles[2])
#



aimNode = mc.createNode("aimConstraint")

mc.setAttr("{}.target.targetTranslate.targetTranslateX".format(aimNode), )



