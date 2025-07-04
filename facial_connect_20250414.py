#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2025/4/14 16:18
# @File    : facial_connect_20250414.py

import maya.cmds as mc

class facial_connect():
    def __init__(self):
        self.prefix = "crd_"
        self.crd_control_grp = "crd_facial_controls_grp"
        self.shot_namespace = ''
        self.chr_namespace = ''

    def main(self):
        self.bake_control = []
        self.match_array = self.get_rig_array()
        for crd_nameSpace, ani_nameSpace  in self.match_array:
            if not mc.objExists(crd_nameSpace + ":" + self.crd_control_grp):
                mc.warning(u" {}  >>>--->>>--->>>  角色 crd rig不存在".format(crd_nameSpace))
                continue

            child = self.find_child(crd_nameSpace + ":" + self.crd_control_grp)
            self.control_array = []
            for i in child:
                if i.endswith("_ctrl") and not "_sec_ctrl" in i and not "_pri_ctrl" in i:
                    self.control_array.append(i)
            mc.select(self.control_array)
            self.filter_attr = self.check_attr(self.control_array, ani_nameSpace)
            self.connect_attr(self.filter_attr)
        return

    def bake_anim(self):
        self.st = 1
        self.et = 100
        mc.bakeResults(self.bake_control, sparseAnimCurveBake=False, minimizeRotation=True,
                       removeBakedAttributeFromLayer=False, removeBakedAnimFromLayer=False, oversamplingRate=1,
                       bakeOnOverrideLayer=False, preserveOutsideKeys=True, simulation=True, sampleBy=1, shape=True,
                       t=(self.st, self.et), disableImplicitControl=True, controlPoints=False)


    def connect_attr(self,filter_attr):
        for i in filter_attr:
            crd_attr =  i.split(":")[1] + ":" + self.prefix +  i.rsplit(":", 1)[1]
            mc.connectAttr(i, crd_attr, f=True)


    def check_attr(self, control_array, ani_namespace):
        result = []
        for each_crd_ctrl in control_array:
            self.abs_name = each_crd_ctrl.split(self.prefix)[-1]
            self.actual_name = ani_namespace + ":" + self.abs_name
            if not mc.objExists(self.actual_name):
                print u"{}   不存在".format(self.actual_name)
            else:
                self.bake_control.append(each_crd_ctrl)
                attr_array = mc.listAttr(each_crd_ctrl, k=True)
                for attr_i in attr_array:
                    attr = self.actual_name + "." + attr_i
                    if not mc.objExists(attr):
                        print u"{}   属性不存在".format(attr)
                    else:
                        result.append(attr)
        return result


    def find_child(self, obj):
        result = mc.ls(mc.listRelatives(obj, c=True), type="transform")
        if result == []:
            return result
        return result + self.find_child(result)


    def get_rig_array(self):
        allTransform = mc.ls(type="transform")
        rig_array = []
        for i in allTransform:
            if i.endswith(":rig"):
                attr = "{}.char_type".format(i)
                if mc.objExists(attr):
                    if mc.getAttr(attr) == "Biped":
                        rig_array.append(i)
        match_array = []
        for i in rig_array:
            split_name = i.split(":", 1)[-1]
            if split_name in rig_array:
                match_array.append([split_name.split(":rig")[0], i.split(":rig")[0]])

        return match_array


    def get_child_namespace(self, nameSpace):
        all = mc.ls(type="transform")
        chr_array = []
        for i in all:
            if nameSpace + ":" in i:
                name_array = i.split(":")
                if not name_array[1] in chr_array:
                    chr_array.append(name_array[1])
        print chr_array

        return chr_array


if __name__ == '__main__':
    cls = facial_connect()
    cls.main()
    # cls.bake_anim()
    # cls.get_rig_array()












