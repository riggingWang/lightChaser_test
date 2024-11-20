#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/2 11:22
# @File    : control_shape.py

import maya.cmds as mc


def create_ctrl(shape, prefix):
    colorId = 17
    if "_sec_" in str(prefix):
        scale = 0.6
        colorR =1
        colorG =0.165
        colorB =0.456
        if "_L_" in str(prefix):
            colorId = 4
        elif "_R_" in str(prefix):
            colorId = 18
        elif "_M_" in str(prefix):
            colorId = 25

    else:
        scale = 1
        colorR =1
        colorG =0.333
        colorB =0.125
        if "_L_" in str(prefix):
            colorId = 13
        elif "_R_" in str(prefix):
            colorId = 6
        elif "_M_" in str(prefix):
            colorId = 17

    shape = con_shape(shape, scale)
    ctrl = mc.rename(shape, "{}_ctrl".format(prefix))
    shape = mc.listRelatives(ctrl, s=True)[0]
    mc.setAttr("{}.overrideEnabled".format(shape), True)
    # mc.setAttr("{}.overrideRGBColors".format(shape), 1)
    # mc.setAttr("{}.overrideColorRGB".format(shape), colorR, colorG, colorB)
    mc.setAttr("{}.overrideColor".format(shape), colorId)
    jnt = mc.joint(n="{}_jnt".format(prefix))
    # mc.refresh()
    return ctrl, jnt


def create_bind_joint(control_jnt):
    prefix = control_jnt.split("_jnt")[0]
    trans = mc.createNode("transform",n ='{}_bind_grp'.format(prefix))
    jnt = mc.createNode("joint", n ='{}_bind'.format(prefix))
    mc.parent(jnt, trans)
    mc.parent(trans, control_jnt)

    return jnt, trans


def con_shape(shape, scale):
    if shape == "plane":
        cv = mc.curve(p=[(0, 1, 3), (0, 1, -3), (0, -1, -3), (0, -1, 3), (0, 1, 3)], k=[0, 1, 2, 3, 4], d=1)

    elif shape == "box":
        cv = mc.curve(
            p=[(0.5, 0.5, 0.5), (-0.5, 0.5, 0.5), (-0.5, 0.5, -0.5), (0.5, 0.5, -0.5), (0.5, 0.5, 0.5),
               (0.5, -0.5, 0.5),
               (-0.5, -0.5, 0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, -0.5, 0.5), (0.5, 0.5, 0.5),
               (0.5, 0.5, -0.5), (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5),
               (-0.5, -0.5, 0.5)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16], d=1)

    elif shape == "diamond":
        cv = mc.curve(p=[(0, 1, 0), (0, 0, 3), (0, -1, 0), (0, 0, -3), (0, 1, 0), (0, -1, 0), (0, 0, 3), (0, 0, -3)],
                      k=[0, 1, 2, 3, 4, 5, 6, 7], d=1)

    elif shape == "circle":
        cv = mc.circle(c=(0, 0, 0), ch=0, d=3, ut=0, sw=360, s=8, r=5, tol=0.01, nr=(0, 1, 0))[0]

    elif shape == "diamond3d":
        cv = mc.curve(
            p=[(0, 0.863792, 0), (-0.866025, 0, -7.57103e-08), (0, -0.863792, 0), (0.866025, 0, 0), (0, 0.863792, 0),
               (1.13566e-07, 0, -0.866025), (0, -0.863792, 0), (-3.78552e-08, 0, 0.866025), (0, 0.863792, 0),
               (-0.866025, 0, -7.57103e-08), (-3.78552e-08, 0, 0.866025), (0.866025, 0, 0), (1.13566e-07, 0, -0.866025),
               (-0.866025, 0, -7.57103e-08)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], d=1)

    else:
        cv = None

    mc.setAttr("{}.s".format(cv), scale, scale, scale)
    mc.setAttr("{}.ry".format(cv), 0)
    mc.makeIdentity(cv, n=0, s=1, r=1, t=1, apply=True, pn=1)
    return cv


def create_con_grp(prefix):

    pri_ctrl = mc.group("{}_ctrl".format(prefix), n="{}_pri_ctrl".format(prefix))
    sec_ctrl = mc.group(pri_ctrl, n="{}_sec_ctrl".format(prefix))
    ctrl_drv = mc.group(sec_ctrl, n="{}_ctrl_drv".format(prefix))
    ctrl_con = mc.group(ctrl_drv, n="{}_ctrl_con".format(prefix))
    ctrl_ofs = mc.group(ctrl_con, n="{}_ctrl_ofs".format(prefix))

    if "_R_main_" in prefix:
        mc.setAttr("{}.sy".format(ctrl_ofs), -1)

    return locals()


if __name__ == '__main__':
    # sel = mc.ls(sl=True)[0]
    # create_con_grp(sel)
    create_bind_joint("ReinsMain_M_back1_fk_jnt")
