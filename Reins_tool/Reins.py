#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/29 14:53
# @File    : Reins.py

import sys
# sys.path.append(r"D:\program\lightChaser_test\Reins_tool")
import maya.cmds as mc
import maya.OpenMaya as om
import control_shape as con
reload(con)


class reins():
    def __init__(self):
        self.guide_array = ["ReinsMain_M_1_guide",
                            "ReinsMain_M_2_guide",
                            "ReinsMain_M_3_guide",
                            "ReinsMain_M_4_guide"]

    def main(self):
        self.get_guide_info()
        self.create_global_ctrl()
        self.create_main_fk_control()
        self.create_center_ik_ctrl()

    def get_guide_info(self):
        """
        # get all fk guide

        self.main_fk_guide
        self.main_ik_guide
        self.main_ik_sec_guide

        :return:
        """
        result = []
        result.append(self.guide_array[0])
        chlid = mc.listRelatives("Reins_front_guide_grp", c=True)
        for i in chlid:
            result.append(i)
        result.append(self.guide_array[1])
        result.append(self.guide_array[2])
        chlid = mc.listRelatives("Reins_back_guide_grp", c=True)
        for i in chlid:
            result.append(i)
        result.append(self.guide_array[3])
        self.main_fk_guide = result

        # get all ik guide
        result = []
        result.append(self.guide_array[0])
        chlid = mc.listRelatives("Reins_front_guide_grp", c=True)
        for i in chlid:
            result.append(i)
        result.append(self.guide_array[1])
        chlid = mc.listRelatives("Reins_center_guide_grp", c=True)
        for i in chlid:
            result.append(i)
        result.append(self.guide_array[2])
        chlid = mc.listRelatives("Reins_back_guide_grp", c=True)
        for i in chlid:
            result.append(i)
        result.append(self.guide_array[3])
        self.main_ik_guide = result

        # get all ik sec guide
        self.main_ik_sec_guide = {}
        for ig in range(len(self.main_ik_guide)):
            chlid = mc.listRelatives(self.main_ik_guide[ig], c=True, type="joint")
            chlid_f = []
            for i in chlid:
                if "_L" in str(i):
                    chlid_f.append(i)
            for i in chlid:
                if "_R" in str(i):
                    chlid_f.append(i)

            self.main_ik_sec_guide.update({self.main_ik_guide[ig]: chlid_f})

        # for i in self.main_ik_sec_guide:
        #      i, self.main_ik_sec_guide[i]

    def control_on_surface(self, parameterV, prefix):
        surfaceShape = mc.listRelatives(self.surface_main, s=True)[0]
        pointOnSurface = mc.createNode("pointOnSurfaceInfo")
        aimConstraint = mc.createNode("aimConstraint")
        control_grp = mc.createNode("transform", n="{}_ik_grp".format(prefix))
        ctrl = con.create_ctrl("diamond", prefix + "_ik")
        mc.parent(ctrl[0], control_grp)
        mc.connectAttr("{}.worldSpace[0]".format(surfaceShape), "{}.inputSurface".format(pointOnSurface))
        mc.connectAttr("{}.result.normal".format(pointOnSurface), "{}.worldUpVector".format(aimConstraint))
        mc.connectAttr("{}.result.tangentV".format(pointOnSurface),
                       "{}.target[0].targetTranslate".format(aimConstraint))
        mc.connectAttr("{}.position".format(pointOnSurface), "{}.t".format(control_grp))
        mc.connectAttr("{}.constraintRotate".format(aimConstraint), "{}.r".format(control_grp))
        mc.setAttr("{}.parameterU".format(pointOnSurface), 0.5)
        mc.setAttr("{}.parameterV".format(pointOnSurface), parameterV)
        mc.setAttr("{}.turnOnPercentage".format(pointOnSurface), 0)
        mc.parent(aimConstraint, control_grp)


    def create_center_ik_ctrl(self):
        for i in range(len(self.main_ik_guide)):
            guide_pos = mc.xform(self.main_ik_guide[i], q=True, ws=True, t=True)
            uv = self.getClosestPoint(self.surface_main, guide_pos[0], guide_pos[1], guide_pos[2])
            perfix = self.main_ik_guide[i].replace("_guide", "")
            self.control_on_surface(uv[1], perfix)


    def create_global_ctrl(self):
        """
        创建global控制器
        :return: global_ctrl
        """
        self.global_ctrl = con.create_ctrl("circle", "global")
        return self.global_ctrl


    def create_main_fk_control(self):
        """
        创建主fk控制器
        :return:
        """
        jnt_array = []
        ofs_array = []
        for i in range(len(self.main_fk_guide)):
            prefix = self.main_fk_guide[i].replace("_guide", "_fk")
            ctrls = con.create_ctrl("plane", "{}".format(prefix))
            jnt_array.append(ctrls[1])
            groups = con.create_con_grp(prefix)
            ofs_array.append(groups["ctrl_ofs"])
            t = mc.xform(self.main_fk_guide[i], q=True, ws=True, t=True)
            ro = mc.xform(self.main_fk_guide[i], q=True, ws=True, ro=True)
            mc.xform(groups["ctrl_ofs"], ws=True, t=t)
            mc.xform(groups["ctrl_ofs"], ws=True, ro=ro)

        for i in range(len(jnt_array)):
            if not i == 0:
                mc.parent(ofs_array[i], jnt_array[i - 1])

        self.surface_main = self.createSurface()

        mc.skinCluster(jnt_array, self.surface_main, tsb=1, n="surfaceSkin", mi=1)

    def getClosestPoint(self, obj, x, y, z):
        sel = om.MSelectionList()
        path = om.MDagPath()
        point = om.MPoint(x, y, z)
        om.MGlobal.getSelectionListByName(obj, sel)
        sel.getDagPath(0, path)
        om.MGlobal.displayInfo(path.fullPathName())
        UUtil = om.MScriptUtil()
        VUtil = om.MScriptUtil()
        UPtr = UUtil.asDoublePtr()
        VPtr = VUtil.asDoublePtr()
        surfFn = om.MFnNurbsSurface(path)
        surfFn.closestPoint(point, UPtr, VPtr, False, 1.0e-6, om.MSpace.kWorld)
        u = om.MScriptUtil.getDouble(UPtr)
        v = om.MScriptUtil.getDouble(VPtr)
        return u, v

    def createSurface(self):
        cv_array = []
        for i in self.main_fk_guide:
            sec_guide = self.main_ik_sec_guide[i]
            pos_a = mc.xform(sec_guide[0], q=True, ws=True, t=True)
            pos_b = mc.xform(sec_guide[1], q=True, ws=True, t=True)

            cv = mc.curve(p=[pos_b, pos_a], k=[0, 1], d=1, n="{}_curve".format(i))
            cv_array.append(cv)

        new_cv_array = []
        for i in range(len(cv_array)):
            mc.parent(cv_array[i], self.main_fk_guide[i])

            if i == 0 or i == len(cv_array) - 1:
                new_cv_array.append(cv_array[i])
                mc.parent(cv_array[i], w=True)

            else:
                end_curve = mc.duplicate(cv_array[i])[0]
                start_cv = mc.getAttr("{}.tx".format(cv_array[i]))
                end_cv = mc.getAttr("{}.tx".format(end_curve))
                mc.setAttr("{}.tx".format(cv_array[i]), start_cv - 0.1)
                mc.setAttr("{}.tx".format(end_curve), end_cv + 0.1)
                new_cv_array.append(cv_array[i])
                new_cv_array.append(end_curve)
                mc.parent(cv_array[i], w=True)
                mc.parent(end_curve, w=True)

        surface = mc.loft(new_cv_array, c=0, ch=0, d=1, ss=1, rsn=True, ar=1, u=1, rn=0, po=0)[0]
        mc.delete(new_cv_array)
        return surface



if __name__ == '__main__':
    cls = reins()
    cls.main()





