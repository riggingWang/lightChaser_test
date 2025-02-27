#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/7 17:09
# @File    : create_guide.py

import os
import copy
import math
import re
import maya.cmds as mc
import pymel.core as pm
import maya.api.OpenMaya as om2
import maya.OpenMaya as om
import rigLib.scripts.utils.maya.utility as utility
import armour_common
reload(armour_common)


class guide:
    def __init__(self):
        self.armour_rig_grp = "armour_rig_grp"      # 总组

        self.armour_customGuide_grp = "armour_customGuide_grp"      # guide组   pass
        self.armour_guide_info = "armour_guide_info"        # guide 信息  pass
        self.armour_batchBase_grp = "armour_batchBase_grp"    # 批量生成总模块

        self.armour_batchDetail_grp = "armour_batchDetail_grp"   # 批量生成后的所有guide 存放位置

        self.armour_nurbsGuide_grp = "armour_nurbsGuide_grp"         # nurbs guide 批量生成引导片
        self.armour_nurbs_guide = "armour_nurbs_guide"              #  主要nurbs guide
        self.armour_nurbs_center = "armour_nurbs_center"            #  用于确定向量nurbs guide
        self.armour_nurbs_normal = "armour_nurbs_normal"            #  用于确定法线nurbs guide

        self.temp_guide_grp = "TEMP_guide_grp"

        self.armourShoulder_grp = "armourShoulder_grp"
        self.armourPauldrons_grp = "armourPauldrons_grp"
        self.armourArmlet_grp = "armourArmlet_grp"


    @armour_common.undo
    def initialize_scene(self):
        if not mc.objExists(self.armour_rig_grp):
            mc.createNode("transform", n=self.armour_rig_grp)

        # if not mc.objExists(self.armour_guide_info):
        #     mc.createNode("transform", n=self.armour_guide_info)
        #     mc.parent(self.armour_guide_info, self.armour_rig_grp)

        # if not mc.objExists(self.armour_customGuide_grp):
        #     mc.createNode("transform", n=self.armour_customGuide_grp)
        #     mc.parent(self.armour_customGuide_grp, self.armour_rig_grp)

        if not mc.objExists(self.armour_batchBase_grp):
            mc.createNode("transform", n=self.armour_batchBase_grp)
            mc.parent(self.armour_batchBase_grp, self.armour_rig_grp)

        if not mc.objExists(self.armour_batchDetail_grp):
            mc.createNode("transform", n=self.armour_batchDetail_grp)
            mc.parent(self.armour_batchDetail_grp, self.armour_batchBase_grp)

    @armour_common.undo
    def createCurveGuide(self, prefix, LR):   # renameCurveBtn
        sel = mc.ls(sl=True)
        iter_v = 0
        suffix = "curveGuide"
        for i in range(len(sel)):
            name = "{}_{}_{}_{}".format(prefix, LR, 0, suffix)
            while mc.objExists(name):
                iter_v += 1
                name = "{}_{}_{}_{}".format(prefix, LR, iter_v, suffix)
            mc.rename(sel[i], name)
            self.addAttribute(name, type="str", attr_name="prefix", valus=prefix)

    @armour_common.undo
    def importGuide(self):
        self.initialize_scene()
        try:
            path = os.path.normpath(os.path.join(os.path.dirname(__file__), "resources", "maya", "armour_guide.ma"))
        except:
            path = r"D:/program/lca_rig/assetsystem_sgl/tools/body/armour_tool/python/armour_tool/resources/maya/armour_guide.ma"

        if not mc.objExists(self.armour_nurbs_guide) and mc.objExists(self.armour_nurbsGuide_grp):
            mc.delete(self.armour_nurbsGuide_grp)

        if mc.objExists(self.armour_nurbsGuide_grp):
            mc.setAttr("{}.v".format(self.armour_nurbsGuide_grp), True)
            return


        mc.file(path, i=1, type="mayaAscii")
        mc.parent(self.armour_nurbsGuide_grp, self.armour_batchBase_grp)
        mc.select(d=True)


    @armour_common.undo
    def batch_convertCurve(self, curve_array, axial_array, aim="X", up="Y"):
        for i in curve_array:
            if not mc.attributeQuery("prefix", node=i, ex=True):
                mc.warning("{} is not guide curve!!!!".format(i))
                return

        sel = mc.ls(sl=True)
        self.parent_world(curve_array)
        new_axial_array = mc.duplicate(axial_array,  n="temp_obj") # duplicate temp obj
        self.parent_world(new_axial_array)

        guide_grp = self.convertCurve(curve_array, new_axial_array, aim=aim, up=up)  # Batch: 批量转换曲线guide
        for i in range(len(guide_grp)):
            prefix = mc.getAttr("{}.prefix".format(curve_array[i]))
            batch_grp = "{}_batchGuide_grp".format(prefix)
            if not mc.objExists(batch_grp):
                batch_grp = mc.createNode("transform", n=batch_grp)
                mc.parent(batch_grp, self.armour_batchDetail_grp)
            mc.parent(guide_grp[i], batch_grp)
            self.addAttribute(batch_grp, type="str", attr_name="prefix", valus=prefix)
            self.addAttribute(batch_grp, type="str", attr_name="aim", valus=aim)
            self.addAttribute(batch_grp, type="str", attr_name="up", valus=up)
            self.addAttribute(guide_grp[i], type="str", attr_name="side", valus="center") # 默认设置为center

        mc.delete(new_axial_array)
        mc.select(sel)


    def convertCurve(self, curve_array, axial_array,  aim="X", up="Y"):
        self.initialize_scene()
        self.grp_array = []
        self.grp_loc_array = []
        self.grp_curve_array = []

        for curve_index in curve_array:
            groups = self.createGroup("{}_guideGrp".format(curve_index))
            self.grp_array.append(groups[0])
            self.grp_loc_array.append(groups[1])
            self.grp_curve_array.append(groups[2])

        guide_loc_all_array = []
        for curve_index in range(len(curve_array)):
            cv_array = mc.ls("{}.cv[*]".format(curve_array[curve_index]), fl=True)
            guide_loc_array = []
            curvePrefix = curve_array[curve_index].split("_curveGuide")[0]
            for cv_index in range(len(cv_array)):
                guide_loc = mc.createNode("joint", n="{}_cv{}_guide".format(curvePrefix, cv_index))
                mc.setAttr("{}.displayLocalAxis".format(guide_loc), 1)
                guide_loc_array.append(guide_loc)
                mc.parent(guide_loc, self.grp_loc_array[curve_index])
                pos = mc.xform(cv_array[cv_index], q=True, ws=True, t=True)
                mc.xform(guide_loc, ws=True, t=pos)
            guide_loc_all_array.append(guide_loc_array)
            mc.parent(curve_array[curve_index], self.grp_curve_array[curve_index])

        for curve_i in range(len(guide_loc_all_array)):
            for cv_i in  range(len(guide_loc_all_array[curve_i])):
                if cv_i == len(guide_loc_all_array[curve_i])-1:
                    ro = mc.getAttr("{}.r".format(guide_loc_all_array[curve_i][cv_i-1]))[0]
                    mc.setAttr("{}.r".format(guide_loc_all_array[curve_i][cv_i]), ro[0],ro[1],ro[2], type="double3")
                    continue
                if len(axial_array) == len(curve_array):
                    self.match_rotate(guide_loc_all_array[curve_i][cv_i+1], guide_loc_all_array[curve_i][cv_i], axial_array[curve_i], aim, up)
                else:
                    self.match_rotate(guide_loc_all_array[curve_i][cv_i+1], guide_loc_all_array[curve_i][cv_i], axial_array[0], aim, up)
        mc.select(d=True)
        return self.grp_array


    def match_rotate(self, target, object, up, aimAxle="X", upAxle="Y"):
        if aimAxle == "X": aimVector = (1, 0, 0)
        elif aimAxle == "Y": aimVector = (0, 1, 0)
        elif aimAxle == "Z": aimVector = (0, 0, 1)
        else: aimVector = (1, 0, 0)

        if upAxle == "X": upVector = (1, 0, 0)
        elif upAxle == "Y": upVector = (0, 1, 0)
        elif upAxle == "Z": upVector = (0, 0, 1)
        else: upVector = (0, 1, 0)

        node = mc.aimConstraint(target, object, weight=1, upVector=upVector, worldUpObject=up,
                                worldUpType="objectrotation", offset=(0, 0, 0), aimVector=aimVector,
                                worldUpVector=(0, 1, 0))

        mc.delete(node)


    def createGroup(self, name):
        perfix = name.split("_curve")[0]
        guide_grp = "{}_guideGrp".format(perfix)
        guide_loc_grp = "{}_loc_grp".format(perfix)
        guide_curve_grp = "{}_curve_grp".format(perfix)

        if mc.objExists(guide_grp):
            mc.delete(guide_grp)
        mc.createNode("transform", n=guide_grp)

        if mc.objExists(guide_loc_grp):
            mc.delete(guide_loc_grp)
        mc.createNode("transform", n=guide_loc_grp)
        mc.parent(guide_loc_grp, guide_grp)

        if mc.objExists(guide_curve_grp):
            mc.delete(guide_curve_grp)
        mc.createNode("transform", n=guide_curve_grp)
        mc.parent(guide_curve_grp, guide_grp)

        return guide_grp, guide_loc_grp, guide_curve_grp


    def pickCurve(self, prefix):
        curve = mc.polyToCurve(conformToSmoothMeshPreview=1, degree=1, form=2, ch=False, n=prefix)[0]
        return curve


    def get_surface_cv_array(self):
        # get all cv.
        cv_array = mc.ls("{}.cv[*][*]".format(self.armour_nurbs_guide), fl=True)
        # set array length.
        iter_u = 0
        iter_v = 0
        for i in range(len(cv_array)):
            string = cv_array[i].split("[")
            u, v = int(string[1].split("]")[0]), int(string[2].split("]")[0])
            if iter_u < u:
                iter_u = u
            if iter_v < v:
                iter_v = v
        iter_u = iter_u + 1
        iter_v = iter_v + 1
        data = []
        for i in range(iter_v):
            temp_list = []
            for j in range(iter_u):
                temp_list.append(None)
            data.append(temp_list)

        for i in range(len(cv_array)):
            string = cv_array[i].split("[")
            u, v = int(string[1].split("]")[0]), int(string[2].split("]")[0])
            data[v][u] = cv_array[i]
        return data


    def createCurve(self, p=None, n=""):
        cur = mc.curve(p=p, d=1, n=n)
        curShape = mc.listRelatives(cur, s=True)[0]
        mc.rename(curShape, "{}Shape".format(n))
        self.setColors(cur, 13)
        mc.ToggleCVs()
        return cur

    @armour_common.undo
    def match_curve_guide(self, mesh_array, progressBar, prefix):  # on_matchCurveBtn_clicked
        self.batch_grp = "{}_batchGuide_grp".format(prefix)
        if mc.objExists(self.batch_grp):
            om.MGlobal.displayWarning("prefix : {}  is Exists!!!".format(prefix))
            return
        if mc.objExists(self.temp_guide_grp):
            om.MGlobal.displayWarning("TEMP_guide_grp is Exists!!!".format(prefix))
            return

        cv_array =  self.get_surface_cv_array()  # 获取所有cv点的列表
        center_array = self.convert_center_array(cv_array)  # 获取所有中心cv点的列表

        count = len(cv_array) * len(cv_array[0]) # 初始化进度条
        percent = 100.0/count
        iter = 0
        progressBar.show()

        self.curve_array = []  # 所有曲线
        self.curvePos_array = []  # 所有点的计算后位置
        for i in range(len(cv_array)):  # 遍历所有列
            array = []  # 列中每个点的计算后位置
            for j in range(len(cv_array[i])):    # 遍历列中所有cv点
                pos = self.calculate_point(cv_array[i][j], center_array[i][j], mesh_array[0])  # 计算
                array.append(pos)
                iter += percent
                progressBar.setProperty("value", iter)
            self.curvePos_array.append(array)
            if i == 0 or i == len(cv_array)-1: # 判断方向
                side = "M"
            else:
                side = "L"
            cur = self.createCurve(p=array, n="{}_{}_{}_curveGuide".format(prefix, side,i))
            self.addAttribute(cur, type="str", attr_name="prefix", valus=prefix)
            self.curve_array.append(cur)
            # mc.refresh()
        progressBar.hide()
        # 到这里所有cv曲线创建结束

        # 创建 确定向上轴向的loc
        self.loc_array = []
        for i in range(len(self.curvePos_array)):
            center_index = len(self.curvePos_array[i]) / 2  # 只求每条线第一个点的位置  在此位置对应曲面上最近的点，求出 位移和旋转
            T_R = self.get_normal(self.curvePos_array[i][center_index])
            loc = mc.spaceLocator(n="{}".format(self.curve_array[i].replace("_curveGuide", "_upLocGuide")))[0]
            self.loc_array.append(loc)
            pos = self.curvePos_array[i][center_index]
            mc.setAttr("{}.t".format(loc), pos[0], pos[1], pos[2], type="double3")
            mc.setAttr("{}.r".format(loc), T_R[1][0], T_R[1][1], T_R[1][2], type="double3")
            self.setColors(loc, 17)


        # 将第一个和最后一个 loc的旋转指向正Z方向
        mc.setAttr("{}.r".format(self.loc_array[0]), -90, 0, 90)
        mc.setAttr("{}.r".format(self.loc_array[-1]), 90, 0, 90)

        if not mc.objExists(self.temp_guide_grp):
            self.temp_guide_grp = mc.createNode("transform", n=self.temp_guide_grp)
            mc.parent(self.temp_guide_grp, self.armour_rig_grp)

        for i in range(len(cv_array)):
            mc.parent(self.curve_array[i], self.temp_guide_grp)
            mc.parent(self.loc_array[i], self.temp_guide_grp)

        mc.setAttr("{}.v".format(self.armour_nurbsGuide_grp), False)


    @armour_common.undo
    def create_nurbs_guide(self, prefix, mirror, aim, up):
        if not mc.objExists(self.temp_guide_grp):
            om.MGlobal.displayWarning("Please first create guide.")
            return

        self.batch_grp = "{}_batchGuide_grp".format(prefix)
        self.curve_array = []
        self.loc_array = []
        for i in mc.listRelatives(self.temp_guide_grp, c=True):
            if i.endswith("_curveGuide"):
                self.curve_array.append(i)

        for i in mc.listRelatives(self.temp_guide_grp, c=True):
            if i.endswith("_upLocGuide"):
                self.loc_array.append(i)


        # 是否需要镜像曲线
        curve_array = self.curve_array
        loc_array = self.loc_array
        if mirror:
            mirror_curves = []
            mirror_axis = []
            for i in range(len(self.curve_array)):
                if "L" in str(self.curve_array[i]):
                    mirrorCurve = self.mirrorObj(self.curve_array[i])
                    mirror_curves.append(mirrorCurve)
                    mirrorloc = self.mirrorObj(self.loc_array[i])
                    mirror_axis.append(mirrorloc)

            curve_array = self.curve_array + mirror_curves
            loc_array = self.loc_array + mirror_axis

        self.batch_grp = mc.createNode("transform", n=self.batch_grp)

        guide_grp = self.convertCurve(curve_array, loc_array, aim=aim, up=up)   # Nurbs: 将曲线和 up axis转换Guide
        self.add_front_back_label(guide_grp)

        mc.parent(guide_grp, self.batch_grp)
        mc.parent(self.batch_grp, self.armour_batchDetail_grp)

        self.addAttribute(self.batch_grp, type="str", attr_name="prefix", valus=prefix)
        self.addAttribute(self.batch_grp, type="str", attr_name="aim", valus=aim)
        self.addAttribute(self.batch_grp, type="str", attr_name="up", valus=up)

        mc.delete(loc_array)
        mc.delete(self.temp_guide_grp)


    def convert_center_array(self, array):
        center_array = copy.deepcopy(array)
        for i in range(len(center_array)):
            for j in range(len(center_array[i])):
                center_array[i][j] = center_array[i][j].replace(self.armour_nurbs_guide, self.armour_nurbs_center)

        return center_array

    def add_front_back_label(self, array):
        L_M_array = []
        R_array = []
        for i in array:
            if not "_R_" in str(i):
                L_M_array.append(i)
            else:
                R_array.append(i)
        def addAttr(array):
            count = len(array)
            for i in range(len(array)):
                if i + 1 <= count / 2:
                    self.addAttribute(array[i], type="str", attr_name="side", valus="back")
                elif count % 2 == 1 and i + 1 == count / 2 + 1:
                    self.addAttribute(array[i], type="str", attr_name="side", valus="center")
                else:
                    self.addAttribute(array[i], type="str", attr_name="side", valus="front")
            return
        addAttr(L_M_array)
        addAttr(R_array)
        return

    def calculate_point(self, p1, p2, mesh):
        _split = re.split(r"[\[;\]]", p1)
        u = _split[-4]
        v = _split[-2]
        target_t = mc.createNode("transform", n="crv{}_cv{}_target".format(u, v))
        # mc.setAttr("{}.displayLocalAxis".format(target_t), 1)
        base_t = mc.createNode("transform", n="crv{}_cv{}_base".format(u, v))
        # mc.setAttr("{}.displayLocalAxis".format(base_t), 1)
        pos = mc.xform(p1, q=True, ws=True, t=True)
        mc.xform(target_t, ws=True, t=pos)
        pos = mc.xform(p2, q=True, ws=True, t=True)
        mc.xform(base_t, ws=True, t=pos)
        self.match_rotate(target_t, base_t, target_t)
        point = self.set_closest_Position(mesh, base_t, 5000)
        mc.delete(target_t, base_t)
        return point


    def get_closest_point(self, mesh, pos):
        sel = om.MSelectionList()
        om.MGlobal.getSelectionListByName(mesh, sel)
        path = om.MDagPath()
        sel.getDagPath(0, path)
        mesh_fn = om.MFnMesh(path)
        point = om.MPoint(pos[0], pos[1], pos[2])
        out_point = om.MPoint()
        mesh_fn.getClosestPoint(point, out_point, om.MSpace.kWorld)
        return out_point.x, out_point.y, out_point.z


    def set_closest_Position(self, mesh, guide_ofs, iterations):
        loc = mc.createNode("transform", n="{}".format(guide_ofs.replace("_base", "_it")))
        # mc.setAttr("{}.displayLocalAxis".format(loc), 1)
        mc.parent(loc, guide_ofs)
        mc.setAttr("{}.t".format(loc), 1.0e5, 0, 0)
        mc.setAttr("{}.r".format(loc), 0, 0, 0)
        iter = 1.0e6
        for i in range(iterations):
            pos = mc.xform(loc, q=True, ws=True, t=True)
            closest_pos = self.get_closest_point(mesh, pos)
            length = self.getLength(pos, closest_pos)
            value = abs(length - iter)
            # print value
            iter = length
            mc.xform(loc, ws=True, t=closest_pos)
            mc.setAttr("{}.tz".format(loc), 0)
            mc.setAttr("{}.ty".format(loc), 0)
            if value < 1.0e-6 or i == iterations - 1:
                print("{}, itCount:{: 4}, Error: {:.6f}, break: {:.6f}".format(loc.split("_it")[0], i, iter, value))
                break

        pos = mc.xform(loc, q=True,ws=True,t=True)
        # mc.delete(loc)
        return pos


    def getLength(self, array_a, array_b):
        return math.sqrt(pow(array_a[0]-array_b[0], 2) + pow(array_a[1]-array_b[1], 2) + pow(array_a[2]-array_b[2], 2))


    def get_normal(self, pos):
        paramUV = self.getPointOnSurfaceParam(self.armour_nurbs_normal, pos)
        closest_point_transform =  self.surfaceParamTransform(paramUV[0], paramUV[1], self.armour_nurbs_normal)
        return closest_point_transform

    def getPointOnSurfaceParam(self, surface, pos):
        sel = om.MSelectionList()
        om.MGlobal.getSelectionListByName(surface, sel)
        MPoint = om.MPoint(pos[0], pos[1], pos[2])
        path = om.MDagPath()
        sel.getDagPath(0, path)
        surfaceFn = om.MFnNurbsSurface(path)
        scriptUtil_u = om.MScriptUtil()
        Double_u = scriptUtil_u.asDoublePtr()
        scriptUtil_v = om.MScriptUtil()
        Double_v = scriptUtil_v.asDoublePtr()
        surfaceFn.closestPoint(MPoint, Double_u, Double_v, False, 0.0001, om.MSpace.kWorld)
        u = om.MScriptUtil.getDouble(Double_u)
        v = om.MScriptUtil.getDouble(Double_v)
        return u, v

    def surfaceParamTransform(self, Param_u, Param_v, surface):
        pointOnSurface = mc.createNode("pointOnSurfaceInfo")
        mc.connectAttr("{}.worldSpace[0]".format(surface), "{}.inputSurface".format(pointOnSurface))
        mc.setAttr("{}.parameterU".format(pointOnSurface), Param_u)
        mc.setAttr("{}.parameterV".format(pointOnSurface), Param_v)
        mc.setAttr("{}.turnOnPercentage".format(pointOnSurface), False)

        aimConstraint = mc.createNode("aimConstraint")

        mc.connectAttr("{}.result.normal".format(pointOnSurface), "{}.worldUpVector".format(aimConstraint))
        mc.connectAttr("{}.result.tangentU".format(pointOnSurface), "{}.target[0].targetTranslate".format(aimConstraint))

        translate = mc.getAttr("{}.position".format(pointOnSurface))[0]
        rotate = mc.getAttr("{}.constraintRotate".format(aimConstraint))[0]
        mc.delete(pointOnSurface)
        return translate, rotate


    def setSpans(self, side, modify):
        if side == "u" and modify == "add":
            value = mc.getAttr("{}.spans_u".format(self.armour_nurbs_guide))
            if value + 1 > 20:
                mc.warning("It is already the maximum value")
                return
            mc.setAttr("{}.spans_u".format(self.armour_nurbs_guide), value + 1)

        if side == "u" and modify == "sub":
            value = mc.getAttr("{}.spans_u".format(self.armour_nurbs_guide))
            if value - 1 < 1:
                mc.warning("It is already the minimum value")
                return
            mc.setAttr("{}.spans_u".format(self.armour_nurbs_guide), value - 1)

        if side == "v" and modify == "add":
            value = mc.getAttr("{}.spans_v".format(self.armour_nurbs_guide))
            if value + 1 > 20:
                mc.warning("It is already the maximum value")
                return
            mc.setAttr("{}.spans_v".format(self.armour_nurbs_guide), value + 1)

        if side == "v" and modify == "sub":
            value = mc.getAttr("{}.spans_v".format(self.armour_nurbs_guide))
            if value - 1 < 3:
                mc.warning("It is already the minimum value")
                return
            mc.setAttr("{}.spans_v".format(self.armour_nurbs_guide), value - 1)


    def addAttribute(self, obj, type="str", attr_name="attr", valus=None):
        if type == "str":
            if not mc.attributeQuery( attr_name, node=obj, ex=True):
                mc.addAttr(obj, ln=attr_name, dt="string", keyable=True)
            mc.setAttr("{}.{}".format(obj, attr_name), valus, type="string")

    def mirrorObj(self, obj):
        mirrorName = obj.replace("_L_", "_R_")
        mirrorObj = mc.duplicate(obj, n=mirrorName)[0]
        grp = mc.createNode("transform")
        mc.parent(mirrorObj, grp)
        mc.setAttr("{}.sx".format(grp), -1)
        mc.parent(mirrorObj, w=True)
        mc.delete(grp)
        return mirrorObj

    def setColors(self, obj, index):
        mc.setAttr("{}.overrideEnabled".format(obj), True)
        mc.setAttr("{}.overrideColor".format(obj), index)
        return

    def parent_world(self, obj):
        try:
            mc.parent(obj, w=True)
        except:
            pass


    def getCenterPoint(self, curve_a,  curve_b):
        def center_pos(pos_a, pos_b, v):
            x = pos_a[0] * (1 - v) + pos_b[0] * v
            y = pos_a[1] * (1 - v) + pos_b[1] * v
            z = pos_a[2] * (1 - v) + pos_b[2] * v
            return x,y,z

        cv_array_a = mc.ls("{}.cv[*]".format(curve_a), fl=True)
        cv_array_b = mc.ls("{}.cv[*]".format(curve_b), fl=True)
        pos_a_start = mc.xform(cv_array_a[0], q=True,ws=True,t=True)
        pos_a_end = mc.xform(cv_array_a[-1], q=True,ws=True,t=True)
        pos_b_start = mc.xform(cv_array_b[0], q=True,ws=True,t=True)
        pos_b_end = mc.xform(cv_array_b[-1], q=True,ws=True,t=True)

        start_centerPos = center_pos(pos_a_start, pos_b_start, 0.5)
        end_centerPos =  center_pos(pos_a_end, pos_b_end, 0.5)

        return start_centerPos, end_centerPos


    @armour_common.undo
    def smoothCurveCv(self):
        sel = mc.ls(sl=True)
        for each_curve in sel:
            shape = mc.listRelatives(each_curve, s=True)[0]
            spans = len(mc.ls("{}.cv[*]".format(each_curve), fl=True)) -1
            mc.rebuildCurve(each_curve, rt=0, ch=1, end=1, d=1, kr=0, s=spans, kcp=0, tol=0.01, kt=0, rpo=1, kep=1)
        mc.select(sel)



    @armour_common.undo
    def shoulder_guide(self, shoudlerGuideNum):
        self.initialize_scene()
        try:
            path = os.path.normpath(os.path.join(os.path.dirname(__file__), "resources", "maya", "armourShoulder_guide.ma"))
        except:
            path = r"/assetsystem_sgl/tools/body/armour_tool/python/armour_tool/resources/maya/armourShoulder_guide.ma"

        if mc.objExists(self.armourShoulder_grp):
            return
        mc.file(path, i=1, type="mayaAscii")
        mc.parent(self.armourShoulder_grp, self.armour_rig_grp)
        if shoudlerGuideNum < 11 and shoudlerGuideNum > 0:
            for i in range(11):
                if i > 0:
                    if i > shoudlerGuideNum:
                        mc.delete('armourSdr_L_main_{}_guide'.format(i))

        mc.select(d=True)


    @armour_common.undo
    def pauldrons_guide(self):
        self.initialize_scene()
        try:
            path = os.path.normpath(os.path.join(os.path.dirname(__file__), "resources", "maya", "armourPauldrons_guide.ma"))
        except:
            path = r"/assetsystem_sgl/tools/body/armour_tool/python/armour_tool/resources/maya/armourPauldrons_guide.ma"

        if mc.objExists(self.armourPauldrons_grp):
            return
        mc.file(path, i=1, type="mayaAscii")
        mc.parent(self.armourPauldrons_grp, self.armour_rig_grp)
        mc.select(d=True)

        #if mc.objExists("arm_L_elbow_1_bind"):
        #    mc.parentConstraint("arm_L_elbow_1_bind", "armourPds_L_iKSpline_2_guide")

    @armour_common.undo
    def armlet_guide(self):
        self.initialize_scene()
        try:
            path = os.path.normpath(os.path.join(os.path.dirname(__file__), "resources", "maya", "armourArmlet_guide.ma"))
        except:
            path = r"/assetsystem_sgl/tools/body/armour_tool/python/armour_tool/resources/maya/armourArmlet_guide.ma"

        if mc.objExists(self.armourArmlet_grp):
            return
        mc.file(path, i=1, type="mayaAscii")
        mc.parent(self.armourArmlet_grp, self.armour_rig_grp)
        mc.select(d=True)


    @armour_common.undo
    def shoulder_guide_mirror(self):
        armour_common.mirror_guide_joint(self.armourShoulder_grp)

    @armour_common.undo
    def pauldrons_guide_mirror(self):
        armour_common.mirror_guide_joint(self.armourPauldrons_grp)

    @armour_common.undo
    def armlet_guide_mirror(self):
        armour_common.mirror_guide_joint(self.armourArmlet_grp)




if __name__ == '__main__':
    cls = guide()
    cls.smoothCurveCv()

