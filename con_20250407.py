#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2025/4/7 16:36
# @File    : con_20250407.py

import maya.cmds as mc

class createFollow():
    def __init__(self):
        self.root_m = "root_ctrl"
        self.hand_l = "arm_L_wrist_1_bind"
        self.hand_r = "arm_R_wrist_1_bind"
        self.base_grp = "prop_follow_loc_grp"
        self.sword_root_ik_ctrl = "sword_root_ik_ctrl"
        self.root_m_follow_grp = "{}_follow_grp".format(self.root_m)
        self.hand_l_follow_grp = "{}_follow_grp".format(self.hand_l)
        self.hand_r_follow_grp = "{}_follow_grp".format(self.hand_r)

        self.switch_attr = "follow"
        self.follow_grp_array = [self.root_m_follow_grp, self.hand_l_follow_grp, self.hand_r_follow_grp]

    def main(self):
        sel = mc.ls(sl=True)
        self.createFollowBaseGrp()
        for i in sel:
            self.create(i)
        mc.select(sel)

    def createFollowBaseGrp(self):
        if mc.objExists(self.base_grp):
            return
        root_m_follow_grp = mc.createNode("transform", n=self.root_m_follow_grp)
        mc.parentConstraint(self.root_m, root_m_follow_grp)
        hand_l_follow_grp = mc.createNode("transform", n=self.hand_l_follow_grp)
        mc.parentConstraint(self.hand_l, hand_l_follow_grp)
        hand_r_follow_grp = mc.createNode("transform", n=self.hand_r_follow_grp)
        mc.parentConstraint(self.hand_r, hand_r_follow_grp)
        base_grp = mc.createNode("transform", n=self.base_grp)
        mc.parent(self.follow_grp_array, base_grp)
        if mc.objExists("anim_modules_grp"):
            mc.parent(base_grp, "anim_modules_grp")

    def create(self, control):
        prefix = control.split("_ctrl")[0]
        ctrl_con = prefix + "_ctrl_con"
        loc_array = []
        animCurve_array = []
        mc.addAttr(control, ln=self.switch_attr, en="World:Left_Hand:Right_Hand:", at="enum", k=True)

        for i, item in enumerate(self.follow_grp_array):
            loc = mc.spaceLocator(n="{}_{}".format(prefix, item.replace("_grp", "_loc")))[0]
            loc_array.append(loc)
            mc.parent(loc, item)
            mc.setAttr("{}.t".format(loc), 0, 0, 0)
            mc.setAttr("{}.r".format(loc), 0, 0, 0)
            mc.setAttr("{}.s".format(loc), 1, 1, 1)

            animCurveUU = mc.createNode("animCurveUU", n="{}__{}__{}_ANIMUU".format(control, ctrl_con, i))
            animCurve_array.append(animCurveUU)
            mc.connectAttr(control + "." + self.switch_attr, "{}.input".format(animCurveUU))

            for index in range(len(self.follow_grp_array)):
                if index == i:
                    mc.setKeyframe(animCurveUU, f=index, v=1)
                else:
                    mc.setKeyframe(animCurveUU, f=index, v=0)

        mc.delete(mc.ls(mc.listRelatives(ctrl_con, c=True), type="constraint"))
        cons_node = mc.parentConstraint(loc_array, ctrl_con)[0]
        mc.setAttr("{}.interpType".format(cons_node), 2)
        for i, item in enumerate(loc_array):
            mc.connectAttr("{}.output".format(animCurve_array[i]), "{}.{}W{}".format(cons_node, item, i))



if __name__ == '__main__':
    cls = createFollow()
    cls.main()


