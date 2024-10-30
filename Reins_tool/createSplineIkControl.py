#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/24 14:56
# @File    : createSplineIkControl.py



import maya.cmds as mc
import control_shape as con
reload(con)


class create_spline_ik_control():
    def __init__(self, prefix="null", number=6, sec_number=11):
        self.number = number
        self.sec_number = sec_number
        self.prefix = prefix
        self.surface_main = ""

    def main(self):
        self.layer1_data = self.create_layer1_ctrl(self.surface_main, self.number, self.prefix)
        self.surface = self.create_surface_on_jnt_array(self.layer1_data[0], self.prefix)
        skin_node = mc.skinCluster(self.layer1_data[0], self.surface, tsb=1, n="surfaceSkin", mi=1)[0]
        self.set_skinWeights(self.surface, skin_node, self.layer1_data[0])
        self.layer2_data = self.create_layer2_ctrl(self.surface, self.sec_number, self.prefix)
        return

    def create_surface_on_jnt_array(self, jnt_array, prefix):
        cur_array = []
        for i in jnt_array:
            cur = mc.curve(p=[[0, 0, -1], [0, 0, 1]], k=[0, 1], d=1, n="{}_curve".format(i))
            cur_array.append(cur)
            mc.parent(cur, i)
            mc.xform(cur, t=[0, 0, 0], ro=[0, 0, 0])

        surface = mc.loft(cur_array, c=0, ch=1, d=3, ss=1, rsn=True, ar=1, u=1, rn=0, po=0, n="{}_sec_surface".format(prefix))[0]

        mc.delete(cur_array)
        return surface


    def create_layer2_ctrl(self, surface, number, prefix):
        ctrl_array = []
        ctrl_jnt_array = []
        ctrl_ofs_array = []
        for i in range(number):
            parameter = i / float(number - 1)
            ctrl = self.create_control_on_surface(surface, parameter, "{}_sec_{}".format(prefix, str(i).zfill(3)))
            ctrl_array.append(ctrl[0][0])
            ctrl_jnt_array.append(ctrl[0][1])
            ctrl_ofs_array.append(ctrl[1]["ctrl_ofs"])
        return [ctrl_jnt_array, ctrl_ofs_array]


    def create_layer1_ctrl(self, surface_main, number, prefix):
        ctrl_array = []
        ctrl_jnt_array = []
        ctrl_ofs_array = []
        for i in range(number):
            parameter = i / float(number - 1)
            ctrl = self.create_control_on_surface(surface_main, parameter, "{}_main_{}".format(prefix, str(i).zfill(3)))
            ctrl_array.append(ctrl[0][0])
            ctrl_jnt_array.append(ctrl[0][1])
            ctrl_ofs_array.append(ctrl[1]["ctrl_ofs"])
        return [ctrl_jnt_array, ctrl_ofs_array]


    def set_skinWeights(self, surface, skinNode, jnt_array):
        cv_array = mc.ls("{}.cv[*][*]".format(surface), fl=True)
        v_list = []
        for i in cv_array:
            if ".cv[0]" in str(i):
                v_list.append(i)

        v_str = v_list[-2][-3:]

        for i in cv_array:
            if i.endswith(v_str):
                mc.skinPercent(skinNode, i, tv=(jnt_array[-1], 0.666666))
            elif i.endswith("[1]"):
                mc.skinPercent(skinNode, i, tv=(jnt_array[0], 0.666666))

    def create_control_on_surface(self, surface_main, parameterV, prefix):
        """

        :return:
        ctrl[0]:控制器, ctrl[1]:骨骼
        groups["str"]: 每个组
        """
        surfaceShape = mc.listRelatives(surface_main, s=True)[0]
        pointOnSurface = mc.createNode("pointOnSurfaceInfo", n="{}_pointNode".format(prefix))
        aimConstraint = mc.createNode("aimConstraint", n="{}_aimNode".format(prefix))
        ctrl = con.create_ctrl("diamond3d", prefix)
        groups = con.create_con_grp(prefix)
        mc.connectAttr("{}.worldSpace[0]".format(surfaceShape), "{}.inputSurface".format(pointOnSurface))
        mc.connectAttr("{}.result.normal".format(pointOnSurface), "{}.worldUpVector".format(aimConstraint))
        mc.connectAttr("{}.result.tangentV".format(pointOnSurface),
                       "{}.target[0].targetTranslate".format(aimConstraint))
        mc.connectAttr("{}.position".format(pointOnSurface), "{}.t".format(groups["ctrl_ofs"]))
        mc.connectAttr("{}.constraintRotate".format(aimConstraint), "{}.r".format(groups["ctrl_ofs"]))
        mc.setAttr("{}.parameterU".format(pointOnSurface), 0.5)
        mc.setAttr("{}.parameterV".format(pointOnSurface), parameterV)
        mc.setAttr("{}.turnOnPercentage".format(pointOnSurface), 1)
        mc.parent(aimConstraint, groups["ctrl_ofs"])
        # mc.parent(groups["ctrl_ofs"], self.main_grp)
        return ctrl, groups


if __name__ == '__main__':
    cls = create_spline_ik_control("reins_L", 6, 11)
    cls.main()

    # sel = mc.ls(sl=True)[0]
    # cls.create_layer2_ctrl(sel,3, "dwwd")
    # cls.create_control_on_surface(sel,0.5, "Sec")