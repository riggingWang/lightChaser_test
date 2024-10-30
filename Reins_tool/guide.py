#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/2 17:30
# @File    : guide.py


import maya.cmds as mc




def set_control_count(surface, count, place):
    sel = mc.ls(sl=True)
    guide_grp = "Reins_{}_guide_grp".format(place)
    child = mc.listRelatives(guide_grp,c=True)
    mc.delete(child)
    iter_v = 1.0 / (count + 1)
    for i in range(count):
        v = (i + 1) * iter_v
        guide_on_surface(v, i, surface, place)
    mc.select(sel)


def guide_on_surface(parameterV, index, surface, place):
    guide_grp = "Reins_{}_guide_grp".format(place)

    surfaceShape = mc.listRelatives(surface, s=True)[0]
    pointOnSurface = mc.createNode("pointOnSurfaceInfo")
    aimConstraint = mc.createNode("aimConstraint")
    joint_M = mc.createNode("joint", n="ReinsMain_M_{}{}_guide".format(place,index))
    joint_L = mc.createNode("joint", n="ReinsMain_L_{}{}_guide".format(place,index))
    joint_R = mc.createNode("joint", n="ReinsMain_R_{}{}_guide".format(place,index))
    mc.setAttr("{}.segmentScaleCompensate".format(joint_M), 0)
    mc.setAttr("{}.segmentScaleCompensate".format(joint_L), 0)
    mc.setAttr("{}.segmentScaleCompensate".format(joint_R), 0)
    mc.setAttr("{}.displayLocalAxis".format(joint_M), 1)
    mc.setAttr("{}.displayLocalAxis".format(joint_L), 1)
    mc.setAttr("{}.displayLocalAxis".format(joint_R), 1)
    mc.setAttr("{}.tz".format(joint_L), 3)
    mc.setAttr("{}.tz".format(joint_R), -3)
    mc.parent(joint_L,joint_R, joint_M)
    mc.connectAttr("{}.worldSpace[0]".format(surfaceShape), "{}.inputSurface".format(pointOnSurface))
    mc.connectAttr("{}.result.normal".format(pointOnSurface), "{}.worldUpVector".format(aimConstraint))
    mc.connectAttr("{}.result.tangentV".format(pointOnSurface), "{}.target[0].targetTranslate".format(aimConstraint))
    mc.connectAttr("{}.position".format(pointOnSurface), "{}.t".format(joint_M))
    mc.connectAttr("{}.constraintRotate".format(aimConstraint), "{}.r".format(joint_M))
    mc.setAttr("{}.parameterU".format(pointOnSurface), 0.5)
    mc.setAttr("{}.parameterV".format(pointOnSurface), parameterV)
    mc.setAttr("{}.turnOnPercentage".format(pointOnSurface), 1)
    mc.parent(aimConstraint, joint_M)
    mc.parent( joint_M, guide_grp)
    mc.scaleConstraint("Reins_guide", joint_M)




if __name__ == '__main__':
    # set_control_count(5)
    set_control_count("Reins_front_surf",1, "front")
    set_control_count("Reins_center_surf",2, "center")
    set_control_count("Reins_back_surf",1, "back")