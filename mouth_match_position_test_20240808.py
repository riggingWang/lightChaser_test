#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/8 10:50
# @File    : mouth_match_position_test_20240808.py


import math
import maya.cmds as mc
import pymel.core as pm
import maya.api.OpenMaya as om

def createNodeArray(surface, point):
    surfaceShape = mc.listRelatives(surface, s=True)[0]
    pntOnSufNode = mc.createNode("pointOnSurfaceInfo")
    aimConstraint = mc.createNode("aimConstraint")
    closestNode = mc.createNode("closestPointOnSurface")
    loc = mc.spaceLocator()[0]
    mc.connectAttr("{}.tangentU".format(pntOnSufNode), "{}.target[0].targetTranslate".format(aimConstraint))
    mc.connectAttr("{}.tangentV".format(pntOnSufNode), "{}.worldUpVector".format(aimConstraint))
    mc.connectAttr("{}.constraintRotate".format(aimConstraint), "{}.rotate".format(loc))
    mc.connectAttr("{}.position".format(pntOnSufNode), "{}.translate".format(loc))
    mc.connectAttr("{}.worldSpace[0]".format(surfaceShape), "{}.inputSurface".format(pntOnSufNode))
    mc.connectAttr("{}.parameterU".format(closestNode), "{}.parameterU".format(pntOnSufNode))
    mc.connectAttr("{}.parameterV".format(closestNode), "{}.parameterV".format(pntOnSufNode))
    mc.connectAttr("{}.worldSpace[0]".format(surfaceShape), "{}.inputSurface".format(closestNode))

    mc.setAttr("{}.offset".format(aimConstraint), 0, 0, 0)

    mc.setAttr("{}.inPosition".format(closestNode), point[0], point[1], point[2])
    t = mc.getAttr("{}.t".format(loc))[0]
    r = mc.getAttr("{}.r".format(loc))[0]
    mc.delete(loc, pntOnSufNode, aimConstraint, closestNode)
    return t, r


def get_closest_point(mesh, pos):
    sel_array = om.MGlobal.getSelectionListByName(mesh)
    path = sel_array.getDagPath(0)
    mesh_fn = om.MFnMesh(path)
    point = om.MPoint(pos)
    closestPoint = mesh_fn.getClosestPoint(point, space=om.MSpace.kWorld)
    return list(closestPoint[0])[:-1]


def set_closest_Position(mesh, guide_ofs):
    guide_loc = pm.listRelatives(guide_ofs, c=True)[0]
    loc = mc.spaceLocator()[0]
    pm.parent(loc, guide_ofs)
    pm.setAttr("{}.t".format(loc), 0, 0, 1.0e5)
    pm.setAttr("{}.r".format(loc), 0, 0, 0)

    for i in range(20):
        pos = mc.xform(loc, q=True, ws=True, t=True)
        closest_pos = get_closest_point(mesh, pos)
        mc.xform(loc, ws=True, t=closest_pos)
        pm.setAttr("{}.tx".format(loc), 0)
        pm.setAttr("{}.ty".format(loc), 0)
    z = pm.getAttr("{}.tz".format(loc))
    pm.setAttr("{}.tz".format(guide_loc), z)
    pm.delete(loc)


def match_rotate(surface, test_loc):
    pos = mc.xform(test_loc, q=True, ws=True, piv=True)[:-3]
    closest_data = createNodeArray(surface, pos)
    rotate = closest_data[1]
    mc.setAttr("{}.r".format(test_loc), rotate[0], rotate[1], rotate[2])


def set_mouth_control_position():
    guide_ofs = mc.listRelatives("mouth_M_ModuleSecCtrlGuideGrp")
    for i in guide_ofs:
        if not "corner" in str(i):
            print i
            match_rotate("mouth_M_ModuleGuideUDSrf", i)
            set_closest_Position("head_geo_meshDrvModel", i)

    # guide_ofs = mc.listRelatives("brow_M_L_PriGuideGrp")
    # for i in guide_ofs:
    #     if "secondary" in str(i):
    #         print i
    #         match_rotate("brow_M_ModuleGuideUDSrf", i)
    #         set_closest_Position("head_geo_meshDrvModel", i)

    # guide_ofs = mc.listRelatives("brow_M_R_PriGuideGrp")
    # for i in guide_ofs:
    #     if "secondary" in str(i):
    #         print i
    #         match_rotate("brow_M_ModuleGuideUDSrf", i)
    #         set_closest_Position("head_geo_meshDrvModel", i)




if __name__ == '__main__':
    set_mouth_control_position()



