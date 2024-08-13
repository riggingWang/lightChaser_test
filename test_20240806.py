#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/6 16:26
# @File    : test_20240806.py

import math
import maya.cmds as mc
import pymel.core as pm
import maya.api.OpenMaya as om



def simplifyCurve(curve):
    newCurve = mc.duplicate(curve)[0]
    allCv = mc.ls("{}.cv[*]".format(newCurve), fl=True)
    y_value = mc.xform(allCv[0], q=True, ws=True, t=True)[1]
    for i in allCv:
        t = mc.xform(i, q=True, ws=True, t=True)
        new_t = [t[0], y_value, t[2]]
        mc.xform(i, ws=True, t=new_t)
    allPoint = mc.ls("{}.cv[0:32]".format(newCurve), fl=True)
    result = []
    length = len(allPoint)
    for i in range(1, length):
        if not i % 4 == 0:
            result.append(allPoint[i])
    pm.delete(result)
    pm.rebuildCurve(newCurve, rt=0, ch=1, end=1, d=3, kr=0, s=4, kcp=0, tol=0.01, kt=0, rpo=1, kep=1)
    return newCurve

simplifyCurve("mouth_M_upNatureGuideCrv")

def get_closest_point(pos, mesh):
    sel_array = om.MGlobal.getSelectionListByName(mesh)
    path = sel_array.getDagPath(0)
    mesh_fn = om.MFnMesh(path)
    point = om.MPoint(pos)
    closestPoint = mesh_fn.getClosestPoint(point, space=om.MSpace.kWorld)
    return list(closestPoint[0])[:-1]

def getCurveClosestPointAndNormal(curve, point):
    tolerance = 0.1e-6
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

def convertRotate(vector):
    v = math.atan2(vector[0], vector[2])
    rotate = math.degrees(v)
    return rotate

def match_rotate(test_loc):
    # test_loc = "mouth_R_up_5_secondary_ctrl"
    pos = mc.xform(test_loc, q=True,ws=True,piv=True)[:-3]
    print pos
    simplify_curve = simplifyCurve("mouth_M_upNatureGuideCrv")
    closest_data = getCurveClosestPointAndNormal(simplify_curve, pos)
    normal = closest_data["normal"]

    aimNode = pm.createNode("aimConstraint")
    print normal
    mc.setAttr("{}.target[0].tt.ttx".format(aimNode), normal[0])
    mc.setAttr("{}.target[0].tt.tty".format(aimNode), normal[1])
    mc.setAttr("{}.target[0].tt.ttz".format(aimNode), normal[2])
    mc.setAttr("{}.offsetY".format(aimNode), -90)

    loc = pm.spaceLocator()

    pm.connectAttr('{}.constraintRotate'.format(aimNode), '{}.rotate'.format(loc), f=1)

    rotate = pm.getAttr('{}.constraintRotate'.format(aimNode))
    mc.setAttr("{}.r".format(test_loc),rotate[0],rotate[1],rotate[2])
    pm.delete(simplify_curve)
    pm.delete(aimNode)
    pm.delete(loc)


def set_closest_Position(guide_ofs):
    guide_loc = pm.listRelatives(guide_ofs, c=True)[0]
    loc = mc.spaceLocator()[0]
    pm.parent(loc, guide_ofs)
    pm.setAttr("{}.t".format(loc),0,0,1.0e5)
    pm.setAttr("{}.r".format(loc),0,0,0)

    for i in range(20):
        pos = mc.xform(loc, q=True, ws=True, t=True)
        closest_pos = get_closest_point(pos, "head_geo_meshDrvModel")
        mc.xform(loc, ws=True,t=closest_pos)
        pm.setAttr("{}.tx".format(loc),0)
        pm.setAttr("{}.ty".format(loc),0)
    z = pm.getAttr("{}.tz".format(loc))
    pm.setAttr("{}.tz".format(guide_loc), z)
    pm.delete(loc)


def run():
    guide_ofs = mc.listRelatives("mouth_M_ModuleSecCtrlGuideGrp")
    for i in guide_ofs:
        if not "corner" in str(i):
            print i
            match_rotate(i)
            set_closest_Position(i)





if __name__ == '__main__':
    run()

