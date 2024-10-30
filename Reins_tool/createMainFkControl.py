#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2024/10/15 16:57
# @File    : createMainFkControl.py


import sys

sys.path.append(r"D:\program\lightChaser_test\Reins_tool")
import maya.cmds as mc
import control_shape as con
import createSplineIkControl

reload(createSplineIkControl)
reload(con)


class reins():
    def __init__(self):
        self.guide_array = ["reins_M_1_guide",
                            "reins_M_2_guide",
                            "reins_M_3_guide",
                            "reins_M_4_guide"]

        self.guide_L_array = ["reins_L_1_guide",
                              "reins_L_2_guide",
                              "reins_L_3_guide",
                              "reins_L_4_guide"]

        self.guide_R_array = ["reins_R_1_guide",
                              "reins_R_2_guide",
                              "reins_R_3_guide",
                              "reins_R_4_guide"]

        self.spline_ik_cls = createSplineIkControl.create_spline_ik_control()

    def main(self, number=7, sec_number=13):
        self.create_main_fk_control()
        surface = self.create_all_surface()
        self.create_sec_ctrl(surface, number, sec_number)
        self.global_ctrl = self.create_main_ctrl("reins_M_global")
        self.clear_up()

    def clear_up(self):
        reins_rig_grp = mc.createNode("transform", n="reins_rig_grp")

        layer1_L_grp = mc.group(self.layer1_L_ofs_array, n="reins_layer1_L_grp")
        layer1_R_grp = mc.group(self.layer1_R_ofs_array, n="reins_layer1_R_grp")
        layer2_L_grp = mc.group(self.layer2_L_ofs_array, n="reins_layer2_L_grp")
        layer2_R_grp = mc.group(self.layer2_R_ofs_array, n="reins_layer2_R_grp")
        layer2_M_grp = mc.group(self.m_sec_ctrl[1], n="reins_layer2_M_grp")

        mc.parent(self.ofs_array[0], reins_rig_grp)
        reins_splineIk_grp = mc.group(layer1_L_grp, layer1_R_grp, layer2_L_grp, layer2_R_grp, layer2_M_grp,
                                      self.m_ctrl[1]["ctrl_ofs"], n="reins_splineIk_grp")
        mc.parent(reins_splineIk_grp, reins_rig_grp)

        surface_array = [self.surface_L_main, self.surface_R_main, self.surface_M_main, self.m_surface,
                         self.layer2_L_surface, self.layer2_R_surface]
        surface_grp = mc.group(surface_array, n="reins_surface_grp")
        mc.setAttr("{}.v".format(surface_grp), False)
        mc.parent(surface_grp, reins_rig_grp)
        mc.parent(self.global_ctrl[1]["ctrl_ofs"], reins_rig_grp)

        mc.parent(self.follow_world_loc, reins_rig_grp)
        mc.parent(self.follow_head_loc, self.jnt_array[0])

        mc.parentConstraint(self.global_ctrl[0][1], self.ofs_array[0])
        mc.scaleConstraint(self.global_ctrl[0][1], self.ofs_array[0])

        mc.delete(self.m_sec_ctrl[1][0], self.m_sec_ctrl[1][-1])

        self.connect_vis([layer1_L_grp, layer1_R_grp], [layer2_L_grp, layer2_R_grp, layer2_M_grp, self.m_ctrl[1]["ctrl_ofs"]])



    def connect_vis(self, main, sec):
        main_attr = "main_ctrl_vis"
        sec_attr = "sec_ctrl_vis"
        followAttrName = "reins_follow_head"

        mc.addAttr(self.ctrl_array[-1], ln=main_attr, at='bool', keyable=True)
        mc.addAttr(self.ctrl_array[-1], ln=sec_attr, at='bool', keyable=True)


        mc.setAttr("{}.{}".format(self.ctrl_array[-1], main_attr), 1)
        mc.setAttr("{}.{}".format(self.ctrl_array[-1], sec_attr), 1)

        mc.addAttr(self.ctrl_array[-1], ln=followAttrName, max=1, dv=0, at='double', min=0, k=True)

        mc.setAttr("{}.{}".format(self.ctrl_array[-1], main_attr), l=False, keyable=False, channelBox=True)
        mc.setAttr("{}.{}".format(self.ctrl_array[-1], sec_attr), l=False, keyable=False, channelBox=True)

        for i in main:
            mc.connectAttr("{}.{}".format(self.ctrl_array[-1], main_attr), "{}.v".format(i))

        for i in sec:
            mc.connectAttr("{}.{}".format(self.ctrl_array[-1], sec_attr), "{}.v".format(i))


        mc.connectAttr("{}.{}".format(self.ctrl_array[-1], followAttrName),
                       "{}.{}".format(self.global_ctrl[0][0], followAttrName))



        mc.setAttr("{}.v".format(self.follow_world_loc), 0)
        mc.setAttr("{}.v".format(self.follow_head_loc), 0)

    def create_main_ctrl(self, prefix):
        ctrl = con.create_ctrl("circle", prefix)
        groups = con.create_con_grp(prefix)
        pos = self.getTransform(self.guide_array[0])
        self.setTransform(groups["ctrl_ofs"], pos)

        self.follow_world_loc = mc.spaceLocator(n="{}_follow_world_locator".format(prefix))[0]
        self.follow_head_loc = mc.spaceLocator(n="{}_follow_head_locator".format(prefix))[0]

        constNode = \
            mc.orientConstraint(self.follow_world_loc, self.follow_head_loc, self.groups_array[1]["ctrl_con"],
                                mo=True)[0]

        attrName = "reins_follow_head"
        mc.addAttr(ctrl[0], ln=attrName, max=1, dv=0, at='double', min=0, k=False)

        reverse = mc.createNode("reverse")
        mc.connectAttr("{}.{}".format(ctrl[0], attrName), "{}.inputX".format(reverse))

        mc.connectAttr("{}.outputX".format(reverse), "{}.{}W0".format(constNode, self.follow_world_loc))
        mc.connectAttr("{}.{}".format(ctrl[0], attrName), "{}.{}W1".format(constNode, self.follow_head_loc))
        return ctrl, groups

    def create_sec_ctrl(self, surface, number, sec_number):
        self.spline_ik_cls.number = number
        self.spline_ik_cls.sec_number = sec_number

        self.spline_ik_cls.prefix = "reins_L"
        self.spline_ik_cls.surface_main = surface[0]
        self.spline_ik_cls.main()

        self.layer1_L_jnt_array = self.spline_ik_cls.layer1_data[0]
        self.layer2_L_jnt_array = self.spline_ik_cls.layer2_data[0]
        self.layer1_L_ofs_array = self.spline_ik_cls.layer1_data[1]
        self.layer2_L_ofs_array = self.spline_ik_cls.layer2_data[1]
        self.layer2_L_surface = self.spline_ik_cls.surface

        self.spline_ik_cls.prefix = "reins_R"
        self.spline_ik_cls.surface_main = surface[1]
        self.spline_ik_cls.main()

        self.layer1_R_jnt_array = self.spline_ik_cls.layer1_data[0]
        self.layer2_R_jnt_array = self.spline_ik_cls.layer2_data[0]
        self.layer1_R_ofs_array = self.spline_ik_cls.layer1_data[1]
        self.layer2_R_ofs_array = self.spline_ik_cls.layer2_data[1]
        self.layer2_R_surface = self.spline_ik_cls.surface

        self.m_ctrl = self.spline_ik_cls.create_control_on_surface(surface[2], 0.5, "reins_M_main")
        mc.skinCluster([self.layer1_L_jnt_array[-1], self.layer1_R_jnt_array[-1]], surface[2], tsb=1, n="surfaceSkin_1",
                       mi=1)

        self.m_surface = self.spline_ik_cls.create_surface_on_jnt_array(
            [self.layer1_L_jnt_array[-1], self.m_ctrl[0][1], self.layer1_R_jnt_array[-1]], "reins_M")

        skinNode = \
            mc.skinCluster([self.layer2_L_jnt_array[-1], self.m_ctrl[0][1], self.layer2_R_jnt_array[-1]],
                           self.m_surface,
                           tsb=1,
                           n="surfaceSkin_2", mi=1)[0]

        self.spline_ik_cls.set_skinWeights(self.m_surface, skinNode, [self.layer2_L_jnt_array[-1], self.m_ctrl[0][1],
                                                                      self.layer2_R_jnt_array[-1]])

        self.m_sec_ctrl = self.spline_ik_cls.create_layer2_ctrl(self.m_surface, 5, "reinsSec_M")

        return

    def create_main_fk_control(self):
        """
        创建主fk控制器
        :return:
        """

        self.prefix_array = []
        self.jnt_array = []
        self.ctrl_array = []
        self.ofs_array = []
        self.bind_array = []
        self.bind_grp_array = []
        self.groups_array = []

        # create control
        for i in range(len(self.guide_array)):
            prefix = self.guide_array[i].replace("_guide", "_fk")
            self.prefix_array.append(prefix)
            ctrls = con.create_ctrl("plane", "{}".format(prefix))
            self.ctrl_array.append(ctrls[0])
            self.jnt_array.append(ctrls[1])
            groups = con.create_con_grp(prefix)
            self.ofs_array.append(groups["ctrl_ofs"])
            self.groups_array.append(groups)

        # parent fk
        mc.parent(self.ofs_array[1], self.jnt_array[0])
        mc.parent(self.ofs_array[2], self.jnt_array[1])
        mc.parent(self.ofs_array[3], self.jnt_array[1])

        # create bind joint
        for i in range(len(self.jnt_array)):
            transform = mc.createNode("transform", n="{}_con".format(self.prefix_array[i]))
            joint = mc.createNode("joint", n="{}_bind".format(self.prefix_array[i]))
            self.bind_grp_array.append(transform)
            self.bind_array.append(joint)
            mc.parent(joint, transform)
            mc.parent(transform, self.jnt_array[i])

        # set transform
        for i in range(len(self.jnt_array)):
            t_r = self.getTransform(self.guide_array[i])
            self.setTransform(self.ofs_array[i], t_r)

        orientConstraint = mc.orientConstraint(self.jnt_array[1], self.jnt_array[0], self.bind_grp_array[1], mo=True)[0]
        mc.setAttr("{}.interpType".format(orientConstraint), 2)
        return

    def create_all_surface(self):
        self.surface_L_main = self.createSurface(self.guide_L_array, "reins_L_main", startEndLoft=False)
        mc.skinCluster(self.bind_array, self.surface_L_main, tsb=1, n="reins_L_main_surfaceSkin", mi=1)

        self.surface_R_main = self.createSurface(self.guide_R_array, "reins_R_main", startEndLoft=False)
        mc.skinCluster(self.bind_array, self.surface_R_main, tsb=1, n="reins_R_main_surfaceSkin", mi=1)

        center = [self.guide_L_array[-1], self.guide_R_array[-1]]
        self.surface_M_main = self.createSurface(center, "reins_M_main")

        return self.surface_L_main, self.surface_R_main, self.surface_M_main

    def createSurface(self, bind_array, prefix, startEndLoft=True):
        cv_array = []
        t_r_array = []
        for i in range(len(bind_array)):
            cv = mc.curve(p=[[0, -0.1, 0], [0, 0.1, 0]], k=[0, 1], d=1, n="{}_curve".format(i))
            cv_array.append(cv)
            t_r = self.getTransform(bind_array[i])
            t_r_array.append(t_r)

        loft_curves = []
        temp = []
        if startEndLoft:
            for i in range(len(cv_array)):
                if i == 0 or i == len(cv_array) - 1:
                    loft_curves.append(cv_array[i])
                    temp.append(cv_array[i])
                    self.setTransform(cv_array[i], t_r_array[i])
                else:
                    end_curve = mc.duplicate(cv_array[i])[0]
                    start_cv_value = mc.getAttr("{}.tx".format(cv_array[i]))
                    end_cv_value = mc.getAttr("{}.tx".format(end_curve))
                    grp = mc.group(cv_array[i], end_curve)
                    self.setTransform(grp, t_r_array[i])
                    temp.append(grp)
                    mc.setAttr("{}.tx".format(cv_array[i]), start_cv_value - 0.01)
                    mc.setAttr("{}.tx".format(end_curve), end_cv_value + 0.01)
                    loft_curves.append(cv_array[i])
                    loft_curves.append(end_curve)

        else:
            for i in range(len(cv_array)):
                end_curve = mc.duplicate(cv_array[i])[0]
                start_cv_value = mc.getAttr("{}.tx".format(cv_array[i]))
                end_cv_value = mc.getAttr("{}.tx".format(end_curve))
                grp = mc.group(cv_array[i], end_curve)
                self.setTransform(grp, t_r_array[i])
                temp.append(grp)
                mc.setAttr("{}.tx".format(cv_array[i]), start_cv_value - 0.01)
                mc.setAttr("{}.tx".format(end_curve), end_cv_value + 0.01)
                loft_curves.append(cv_array[i])
                loft_curves.append(end_curve)


        surface = \
            mc.loft(loft_curves, c=0, ch=0, d=1, ss=1, rsn=True, ar=1, u=1, rn=0, po=0,
                    n="{}_surface".format(prefix))[0]
        mc.delete(temp)
        return surface

    def getTransform(self, obj):
        data = []
        t = mc.xform(obj, q=True, ws=True, t=True)
        r = mc.xform(obj, q=True, ws=True, ro=True)
        data.append(t)
        data.append(r)
        return data

    def setTransform(self, obj, data):
        mc.xform(obj, ws=True, t=data[0])
        mc.xform(obj, ws=True, ro=data[1])


if __name__ == '__main__':
    cls = reins()
    cls.main(7, 13)
