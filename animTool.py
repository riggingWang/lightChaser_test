#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/28 11:07
# @File    : animtool.py


from __builtin__ import long
import pymel.core as pm
import maya.cmds as mc
import maya.OpenMayaUI as omui
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import shiboken2
import webbrowser
import functools
import traceback

_Win = "fk_dynamic_rig_tool"
mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = shiboken2.wrapInstance(long(mayaMainWindowPtr), QWidget)


def undo(func):
    @functools.wraps(func)
    def _undofunc(*args, **kwargs):
        try:
            mc.undoInfo(ock=True)
            return func(*args, **kwargs)
        except:
            traceback.print_exc()
        finally:
            mc.undoInfo(cck=True)
    return _undofunc


class anim_hair_tool:
    def __init__(self):
        self.sel = []

    def get_selected_fkCtrl(self):
        self.sel = mc.ls(sl=True)
        self.sel_parent = []
        for i in self.sel:
            sel_p = pm.listRelatives(i, p=True)[0]
            self.sel_parent.append(sel_p)

    @undo
    def main_create_dynamic_rig(self):
        self.get_selected_fkCtrl()
        self.init_scenes()
        self.get_all_ctrl_pos()  # 查询所有的控制器位置与旋转
        self.create_main_ctrl(self.name)  # 创建主控制器

        self.const_jnt = self.create_joint("_constJnt")  # 创建控制约束的骨骼链
        self.bake_const_jnt(self.const_jnt)  # bake骨骼动画

        self.create_spline_Ik()  # 创建 线性ik
        self.dyn_curve_data = self.create_dyn_sys()  # 创建动力学节点
        pm.blendShape(self.dyn_curve, self.splineIk_cur, w=[(0, 1)])
        pm.skinCluster(self.const_jnt, self.dynCtrl_curveShape)
        self.minus_jnt = self.create_joint("_MinusIk")  # 创建反减骨骼链
        self.connect_jnt(self.const_jnt, self.spline_jnt, self.minus_jnt)  # 链接骨骼 链接控制器父级组
        self.sys_info_records()
        pm.select(self.main_ctrl)

    def sys_info_records(self):
        pm.setAttr("{}.pointLock".format(self.follicle_node), 1)
        pm.setAttr("{}.startCurveAttract".format(self.hairSystem), 0.2)
        pm.setAttr("{}.attractionScale[1].attractionScale_FloatValue".format(self.hairSystem), 0.5)
        pm.setAttr("{}.drag".format(self.hairSystem), 0.97)
        pm.setAttr("{}.motionDrag".format(self.hairSystem), 0.1)

        self.add_label("follicle_tr", str(self.follicle_tr))
        self.add_label("follicle_node", str(self.follicle_node))
        self.add_label("follicle_parent", str(self.follicle_parent))
        self.add_label("dynCtrl_curveShape", str(self.dynCtrl_curveShape))
        self.add_label("dyn_curve", str(self.dyn_curve))
        self.add_label("dyn_curve_parent", str(self.dyn_curve_parent))
        self.add_label("hairSystem", str(self.hairSystem))
        self.add_label("nucleus", str(self.nucleus))

        self.add_label("sel_ctrl", self.list_to_str(self.sel))
        self.add_label("sel_parent_ctrl", self.list_to_str(self.sel_parent))

        self.add_label("const_joints", self.list_to_str(self.const_jnt))
        self.add_label("spline_joints", self.list_to_str(self.spline_jnt))
        self.add_label("minus_joints", self.list_to_str(self.minus_jnt))
        self.add_label("dyn_each_grp", str(self.dyn_each_grp))

        pm.setAttr("{}.overrideEnabled".format(self.const_jnt[0]), True)
        pm.setAttr("{}.overrideColor".format(self.const_jnt[0]), 17)

        pm.setAttr("{}.overrideEnabled".format(self.spline_jnt[0]), True)
        pm.setAttr("{}.overrideColor".format(self.spline_jnt[0]), 14)

        # pm.addAttr(self.main_ctrl, ln="stretchResistance", max=200, dv=10, at='double', min=0, keyable=True)
        # pm.connectAttr("{}.stretchResistance".format(self.main_ctrl), "{}.stretchResistance".format(self.hairSystem))

        # pm.addAttr(self.main_ctrl, ln="compressionResistance", max=200, dv=10, at='double', min=0, keyable=True)
        # pm.connectAttr("{}.compressionResistance".format(self.main_ctrl),
        #                "{}.compressionResistance".format(self.hairSystem))

        pm.addAttr(self.main_ctrl, ln="bendResistance", max=200, dv=1, at='double', min=0, keyable=True)
        pm.connectAttr("{}.bendResistance".format(self.main_ctrl), "{}.bendResistance".format(self.hairSystem))

        # pm.addAttr(self.main_ctrl, ln="startCurveAttract", max=5, dv=0.1, at='double', min=0, keyable=True)
        # pm.connectAttr("{}.startCurveAttract".format(self.main_ctrl), "{}.startCurveAttract".format(self.hairSystem))

        pm.addAttr(self.main_ctrl, ln="damp", max=1, dv=0.1, at='double', min=0, keyable=True)
        pm.connectAttr("{}.damp".format(self.main_ctrl), "{}.damp".format(self.hairSystem))

        # pm.addAttr(self.main_ctrl, ln="motionDrag", max=1, dv=0.01, at='double', min=0, keyable=True)
        # pm.connectAttr("{}.motionDrag".format(self.main_ctrl), "{}.motionDrag".format(self.hairSystem))

    def add_label(self, attr, label_str):
        info = self.hair_sys_info
        pm.addAttr(info, ln=attr, dt="string")
        pm.setAttr('{}.{}'.format(info, attr), str(label_str), type="string")
        pm.setAttr("{}.{}".format(info, attr), l=True)

    def list_to_str(self, list_v):
        result = ''
        for i in list_v:
            if not list_v.index(i) == 0:
                result += ","
            result += i
        return result

    def bake_const_jnt(self, const_jnt):
        constrain_array = []
        for i in range(len(self.sel)):
            cons = pm.parentConstraint(self.sel[i], const_jnt[i])
            constrain_array.append(cons)
        self.bakeResults(const_jnt, self.min_time, self.max_time)
        pm.delete(constrain_array)

    def create_spline_Ik(self):
        self.spline_jnt = self.create_joint("_splineIk")  # 创建线性IK骨骼链
        self.splineIk_cur = self.create_curve("{}_blendCurve".format(self.name))  # 创建线性IK曲线
        ikh = pm.ikHandle(sj=self.spline_jnt[0], ee=self.spline_jnt[-1], roc=True, c=self.splineIk_cur,
                          sol='ikSplineSolver',
                          ccv=False,
                          rootOnCurve=False, n='{}_IKH'.format(self.name))[0]  # 创建线性IK
        pm.parent(ikh, self.dyn_each_deform_grp)

    def connected_anim(self):  # pass
        time_array = [self.min_time + i for i in range(self.all_time)]
        direction = ["x", "y", "z"]

        #
        rotate_array = []
        for each_time in time_array:
            pm.currentTime(each_time)
            all_jnt_rotate_Array = []
            for j in range(len(self.sel_parent)):
                r = mc.getAttr("{}.r".format(self.minus_jnt[j]))[0]
                all_jnt_rotate_Array.append(r)
            rotate_array.append(all_jnt_rotate_Array)

        #
        for ctrl_index in range(len(self.sel_parent)):
            for each_dir in range(len(direction)):
                animCurve = pm.createNode("animCurveTA", n="{}_r{}".format(self.sel_parent[ctrl_index], each_dir))
                for each_time in range(len(time_array)):
                    value = rotate_array[each_time][ctrl_index][each_dir]
                    pm.setKeyframe(animCurve, t=time_array[each_time], v=value)
                pm.connectAttr("{}.output".format(animCurve),
                               "{}.r{}".format(self.sel_parent[ctrl_index], direction[each_dir]))

    def connect_jnt(self, jntArrayA, jntArrayB, jntArrayC):

        for i in range(len(self.sel_parent)):
            multMatrix = pm.createNode("multMatrix")
            decomposeMatrix = pm.createNode("decomposeMatrix")
            pm.connectAttr("{}.matrix".format(jntArrayB[i]), "{}.matrixIn[0]".format(multMatrix))
            pm.connectAttr("{}.inverseMatrix".format(jntArrayA[i]), "{}.matrixIn[1]".format(multMatrix))
            pm.connectAttr("{}.matrixSum".format(multMatrix), "{}.inputMatrix".format(decomposeMatrix))

            blendColors = pm.createNode("blendColors")
            pm.setAttr("{}.color1".format(blendColors), 0, 0, 0, type='double3')
            pm.setAttr("{}.color2".format(blendColors), 0, 0, 0, type='double3')
            pm.connectAttr("{}.dyn_blend".format(self.hair_sys_info), "{}.blender".format(blendColors))

            pm.connectAttr("{}.outputRotateX".format(decomposeMatrix), "{}.color1R".format(blendColors))
            pm.connectAttr("{}.outputRotateY".format(decomposeMatrix), "{}.color1G".format(blendColors))
            pm.connectAttr("{}.outputRotateZ".format(decomposeMatrix), "{}.color1B".format(blendColors))

            pm.connectAttr("{}.outputR".format(blendColors), "{}.rx".format(jntArrayC[i]))
            pm.connectAttr("{}.outputG".format(blendColors), "{}.ry".format(jntArrayC[i]))
            pm.connectAttr("{}.outputB".format(blendColors), "{}.rz".format(jntArrayC[i]))

        for i in range(len(self.sel_parent)):
            pm.connectAttr("{}.rx".format(self.minus_jnt[i]), "{}.rx".format(self.sel_parent[i]), f=True)
            pm.connectAttr("{}.ry".format(self.minus_jnt[i]), "{}.ry".format(self.sel_parent[i]), f=True)
            pm.connectAttr("{}.rz".format(self.minus_jnt[i]), "{}.rz".format(self.sel_parent[i]), f=True)

    def get_all_ctrl_pos(self):
        self.pos_array = []
        self.rotate_array = []
        for i in self.sel:
            t = pm.xform(i, q=True, ws=True, piv=True)[:-3]
            ro = pm.xform(i, q=True, ws=True, ro=True)
            self.pos_array.append(t)
            self.rotate_array.append(ro)
        endPos = self.getCenterPoint(self.pos_array[-2], self.pos_array[-1], 1.5)
        self.pos_array.append(endPos)
        return self.pos_array

    def create_joint(self, suffix):
        jnt_array = []
        pos_count = len(self.pos_array)

        for i in range(len(self.pos_array)):
            if not i == pos_count - 1:
                jnt = mc.createNode("joint", n="{}{}".format(self.sel[i].replace(":", "__"), suffix))
                jnt_array.append(jnt)
                pm.xform(jnt, ws=True, t=self.pos_array[i])
                pm.xform(jnt, ws=True, ro=self.rotate_array[i])
            else:
                jnt = mc.createNode("joint", n="{}End{}".format(self.sel[-1].replace(":", "__"), suffix))
                jnt_array.append(jnt)
                pm.xform(jnt, ws=True, t=self.pos_array[i])
                pm.xform(jnt, ws=True, ro=self.rotate_array[-1])

        for i in range(len(jnt_array)):
            if not i == pos_count - 1:
                pm.parent(jnt_array[i + 1], jnt_array[i])

        pm.makeIdentity(jnt_array[0], n=0, s=1, r=1, t=1, apply=True, pn=1)
        pm.parent(jnt_array[0], self.dyn_each_deform_grp)
        return jnt_array

    def getCenterPoint(self, PosA, PosB, Value):
        x = PosA[0] * (1 - Value) + PosB[0] * Value
        y = PosA[1] * (1 - Value) + PosB[1] * Value
        z = PosA[2] * (1 - Value) + PosB[2] * Value
        return [x, y, z]

    def create_main_ctrl(self, name):
        self.main_ctrl = self.control_shapes(name="{}_dynSys_ctrl".format(name))
        selShape = pm.listRelatives(self.sel[-1], s=True)[0]
        boundingBox_val = pm.getAttr("{}.boundingBox".format(selShape))[-1]
        length_v = boundingBox_val.length()
        self.main_ctrl.s.set(length_v, length_v, length_v)
        pm.makeIdentity(self.main_ctrl, n=0, s=1, r=1, t=1, apply=True, pn=1)
        self.main_ctrl_grp = pm.createNode("transform", n="{}_dynSys_grp".format(name))
        pm.parent(self.main_ctrl, self.main_ctrl_grp)
        self.main_ctrl_grp.t.set(self.pos_array[-1])
        pm.parent(self.main_ctrl_grp, self.dyn_each_grp)
        pm.parentConstraint(self.sel[-1], self.main_ctrl_grp, mo=True, sr=["x", "y", "z"])
        pm.setAttr("{}.tx".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)
        pm.setAttr("{}.ty".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)
        pm.setAttr("{}.tz".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)
        pm.setAttr("{}.rx".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)
        pm.setAttr("{}.ry".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)
        pm.setAttr("{}.rz".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)
        pm.setAttr("{}.sx".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)
        pm.setAttr("{}.sy".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)
        pm.setAttr("{}.sz".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)
        pm.setAttr("{}.v".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)

        pm.addAttr(self.main_ctrl, ln="rig_info", dt="string")
        pm.setAttr('{}.rig_info'.format(self.main_ctrl), self.hair_sys_info, type="string")

        pm.addAttr(self.main_ctrl, ln="envelope", max=10, dv=10, at='double', min=0, keyable=True)

        # floatMath = pm.createNode("floatMath")
        # floatMath.operation.set(3)
        # floatMath.floatB.set(10)
        # pm.connectAttr("{}.envelope".format(self.main_ctrl), "{}.floatA".format(floatMath))
        # pm.connectAttr("{}.outFloat".format(floatMath), "{}.dyn_blend".format(self.hair_sys_info))

        floatMath = pm.createNode("multiplyDivide")
        pm.setAttr("{}.operation".format(floatMath), 2)
        pm.setAttr("{}.input2X".format(floatMath), 10)
        pm.connectAttr("{}.envelope".format(self.main_ctrl), "{}.input1X".format(floatMath))
        pm.connectAttr("{}.outputX".format(floatMath), "{}.dyn_blend".format(self.hair_sys_info))

        return name

    def create_curve(self, name):
        curve = pm.curve(p=self.pos_array, d=1, n=name)
        return curve

    def create_dyn_sys(self):
        pm.currentTime(1)
        pm.refresh()
        curve = self.create_curve("{}_dynCurve".format(self.name))  # 创建动力学结算曲线
        pm.select(curve)
        pm.mel.makeCurvesDynamic(2, ["1", "0", "1", "1", "0"])

        self.follicle_tr = pm.listRelatives(curve, p=True)[0]
        self.follicle_node = pm.listRelatives(self.follicle_tr, s=True)[0]
        self.follicle_parent = pm.listRelatives(self.follicle_tr, p=True)[0]
        self.dynCtrl_curveShape = pm.listRelatives(curve, s=True)[0]
        self.dyn_curve = pm.listConnections("{}.outCurve".format(self.follicle_node))[0]
        self.dyn_curve_parent = pm.listRelatives(self.dyn_curve, p=True)[0]
        self.hairSystem = pm.listConnections("{}.outHair".format(self.follicle_node))[0]
        self.nucleus = pm.listConnections("{}.currentState".format(self.hairSystem))[0]
        pm.setAttr("{}.intermediateObject".format(self.dynCtrl_curveShape), 0)

        main_grp = pm.createNode("transform", n="{}_hairSys".format(curve))
        pm.parent(self.follicle_parent, main_grp)
        pm.parent(self.dyn_curve_parent, main_grp)
        pm.parent(self.hairSystem, self.dyn_each_grp)

        pm.parent(main_grp, self.dyn_each_deform_grp)
        pm.parent(self.nucleus, self.dyn_main_grp)

        return locals()

    def init_scenes(self):
        self.min_time = int(pm.playbackOptions(q=True, min=True))
        self.max_time = int(pm.playbackOptions(q=True, max=True))
        self.all_time = int(self.max_time - self.min_time + 1)
        self.dyn_main_grp = "FK_Dynamic_RIG_GRP"
        if not pm.objExists(self.dyn_main_grp):
            pm.createNode("transform", n="FK_Dynamic_RIG_GRP")
        self.set_parent_zero()
        self.name = self.sel[0].split("_ctrl")[0].replace(":", "__")
        self.dyn_each_grp = "{}_mainRig_grp".format(self.name)
        if pm.objExists(self.dyn_each_grp):
            pm.delete(self.dyn_each_grp)
        self.dyn_each_grp = pm.createNode("transform", n="{}_mainRig_grp".format(self.name))
        pm.parent(self.dyn_each_grp, self.dyn_main_grp)

        self.hair_sys_info = pm.createNode("transform", n="{}_hairSysInfo".format(self.name))
        pm.parent(self.hair_sys_info, self.dyn_each_grp)

        self.dyn_each_deform_grp = pm.createNode("transform", n="{}_deform_grp".format(self.name))
        pm.parent(self.dyn_each_deform_grp, self.dyn_each_grp)
        self.dyn_each_deform_grp.v.set(0)

        pm.addAttr(self.hair_sys_info, ln="dyn_blend", max=1, dv=1, at='double', min=0, keyable=True)

        value = "{},{}".format(self.min_time, self.max_time)
        pm.addAttr(self.hair_sys_info, ln="time_data", dt="string")
        pm.setAttr('{}.time_data'.format(self.hair_sys_info), value, type="string")

    def bakeResults(self, objArray, min_time, max_time, only_rotate=False, sample_by=1):
        if only_rotate:
            pm.bakeResults(objArray,
                           sparseAnimCurveBake=False, minimizeRotation=True, removeBakedAttributeFromLayer=False,
                           removeBakedAnimFromLayer=False, oversamplingRate=1, bakeOnOverrideLayer=False,
                           preserveOutsideKeys=True, simulation=True, sampleBy=1, shape=True,
                           t="{}:{}".format(min_time, max_time), disableImplicitControl=True,
                           controlPoints=False, at=["rx", "ry", "rz"])
        else:
            pm.bakeResults(objArray,
                           sparseAnimCurveBake=False, minimizeRotation=True, removeBakedAttributeFromLayer=False,
                           removeBakedAnimFromLayer=False, oversamplingRate=1, bakeOnOverrideLayer=False,
                           preserveOutsideKeys=True, simulation=True, sampleBy=1, shape=True,
                           t="{}:{}".format(min_time, max_time), disableImplicitControl=True,
                           controlPoints=False)
        pm.filterCurve(objArray, kernel='gaussian2', period=sample_by, f='resample')
        return True

    def control_shapes(self, name):
        cur = pm.curve(p=[[-0.24, 0.716, 0.0],
                          [-0.214, 0.817, 0.0],
                          [-0.219, 0.841, 0.0],
                          [-0.241, 0.859, 0.0],
                          [-0.268, 0.857, 0.0],
                          [-0.289, 0.842, 0.0],
                          [-0.81, -0.75, 0.0],
                          [-0.811, -0.778, 0.0],
                          [-0.792, -0.798, 0.0],
                          [-0.765, -0.794, 0.0],
                          [-0.749, -0.768, 0.0],
                          [-0.24, 0.716, 0.0],
                          [-0.164, 0.733, 0.0],
                          [-0.086, 0.744, 0.0],
                          [-0.008, 0.747, 0.0],
                          [0.074, 0.736, 0.0],
                          [0.159, 0.713, 0.0],
                          [0.247, 0.661, 0.0],
                          [0.313, 0.599, 0.0],
                          [0.375, 0.539, 0.0],
                          [0.433, 0.492, 0.0],
                          [0.518, 0.45, 0.0],
                          [0.598, 0.432, 0.0],
                          [0.666, 0.43, 0.0],
                          [0.735, 0.435, 0.0],
                          [0.842, 0.459, 0.0],
                          [0.656, -0.081, 0.0],
                          [0.575, -0.098, 0.0],
                          [0.489, -0.107, 0.0],
                          [0.425, -0.106, 0.0],
                          [0.365, -0.096, 0.0],
                          [0.293, -0.071, 0.0],
                          [0.234, -0.035, 0.0],
                          [0.188, 0.002, 0.0],
                          [0.147, 0.041, 0.0],
                          [0.088, 0.098, 0.0],
                          [0.028, 0.144, 0.0],
                          [-0.038, 0.18, 0.0],
                          [-0.109, 0.2, 0.0],
                          [-0.189, 0.209, 0.0],
                          [-0.268, 0.208, 0.0],
                          [-0.344, 0.196, 0.0],
                          [-0.425, 0.178, 0.0]], d=1, n=name)
        curve_shape = pm.listRelatives(cur, s=True)[0]
        curve_shape.overrideEnabled.set(True)
        curve_shape.overrideColor.set(9)

        return cur

    def set_parent_zero(self):
        for i in self.sel_parent:
            mc.setAttr("{}.r".format(i), 0,0,0)

    def update_anim(self):
        sel = self.get_selected()
        if not sel: return

        all_sel_ctrl = []
        all_sel_parent = []
        all_minus_joints = []
        all_const_joints = []
        all_time_data = []

        for each_sel in sel:
            pm.setAttr("{}.envelope".format(each_sel), 0)

            const_joints = self.get_label(each_sel, "const_joints")
            const_joints_array = const_joints.split(",")
            const_joints_array.remove(const_joints_array[-1])
            all_const_joints += const_joints_array

            sel_ctrl = self.get_label(each_sel, "sel_ctrl")
            sel_ctrl_array = sel_ctrl.split(",")
            all_sel_ctrl += sel_ctrl_array

            sel_parent_ctrl = self.get_label(each_sel, "sel_parent_ctrl")
            sel_parent_ctrl_array = sel_parent_ctrl.split(",")
            all_sel_parent += sel_parent_ctrl_array

            minus_joints = self.get_label(each_sel, "minus_joints")
            minus_joints_array = minus_joints.split(",")
            minus_joints_array.remove(minus_joints_array[-1])
            all_minus_joints += minus_joints_array

            time_data = self.get_label(each_sel, "time_data")
            time_data_array = time_data.split(",")
            all_time_data += time_data_array

        for i in all_sel_parent:  # disconnect
            pm.disconnectAttr("{}.rx".format(i))
            pm.disconnectAttr("{}.ry".format(i))
            pm.disconnectAttr("{}.rz".format(i))

        consNode_array = []
        for i in range(len(all_sel_ctrl)):
            consNode = pm.parentConstraint(all_sel_ctrl[i], all_const_joints[i])
            consNode_array.append(consNode)
        self.bakeResults(all_const_joints, all_time_data[0], all_time_data[1])
        pm.delete(consNode_array)

        for i in range(len(all_sel_parent)):  # connect
            pm.connectAttr("{}.rx".format(all_minus_joints[i]), "{}.rx".format(all_sel_parent[i]))
            pm.connectAttr("{}.ry".format(all_minus_joints[i]), "{}.ry".format(all_sel_parent[i]))
            pm.connectAttr("{}.rz".format(all_minus_joints[i]), "{}.rz".format(all_sel_parent[i]))

        for each_sel in sel:
            pm.setAttr("{}.envelope".format(each_sel), 10)

    def get_label(self, ctrl, attr):
        info = pm.getAttr("{}.rig_info".format(ctrl))
        data = pm.getAttr("{}.{}".format(info, attr))
        return data

    def clear_scene(self):
        main_grp = "FK_Dynamic_RIG_GRP"
        children = pm.listRelatives(main_grp, c=True)
        children = [i for i in children if pm.nodeType(i) == "transform"]
        if len(children) == 0:
            pm.delete(main_grp)

    def bake_all_ctrl_parent(self, sample_by):
        sel = self.get_selected()
        if not sel: return

        all_sel_parent = []
        all_time_data = []
        for each_sel in sel:
            sel_parent_ctrl = self.get_label(each_sel, "sel_parent_ctrl")
            sel_parent_ctrl_array = sel_parent_ctrl.split(",")
            all_sel_parent += sel_parent_ctrl_array

            time_data = self.get_label(each_sel, "time_data")
            time_data_array = time_data.split(",")
            all_time_data += time_data_array

        self.bakeResults(all_sel_parent, all_time_data[0], all_time_data[1], True, sample_by)

    def edit_sys(self):
        sel = self.get_selected()
        if not sel: return
        for each_sel in sel:
            pm.setAttr("{}.envelope".format(each_sel), 0)
            sel_parent_ctrl = self.get_label(each_sel, "sel_parent_ctrl")
            sel_parent_ctrl_array = sel_parent_ctrl.split(",")
            minus_joints = self.get_label(each_sel, "minus_joints")
            minus_joints_array = minus_joints.split(",")

            for i in range(len(sel_parent_ctrl_array)):
                pm.connectAttr("{}.rx".format(minus_joints_array[i]), "{}.rx".format(sel_parent_ctrl_array[i]), f=True)
                pm.connectAttr("{}.ry".format(minus_joints_array[i]), "{}.ry".format(sel_parent_ctrl_array[i]), f=True)
                pm.connectAttr("{}.rz".format(minus_joints_array[i]), "{}.rz".format(sel_parent_ctrl_array[i]), f=True)

    def selected_hair_ctrl(self):
        sel = pm.ls(sl=True)
        a = pm.getAttr("{}.boundingBox".format(self.sel[-1]))[-1]
        length_v = a.length()

    def delete_rig(self):
        sel = self.get_selected()
        if not sel: return

        for each_sel in sel:
            dyn_each_grp = self.get_label(each_sel, "dyn_each_grp")
            dyn_each_grp_array = dyn_each_grp.split(",")
            pm.delete(dyn_each_grp_array)
            self.clear_scene()

    def get_selected(self):
        sel = pm.ls(sl=True)
        if len(sel) == 0:
            pm.warning("not selected!!!")
            return False

        for i in sel:
            if not str("dynSys_ctrl") in str(i):
                pm.warning("not selected dyn ctrl!!!")

                return False
        return sel

    def lrs_createRig(self):
        currentTime = pm.playbackOptions(q=True, min=True)
        LR="L"
        pm.select("lhgz_lianhuagongzhu*:antenna_{}_pri_fk_1_ctrl".format(LR),
                  "lhgz_lianhuagongzhu*:antenna_{}_pri_fk_2_ctrl".format(LR),
                  "lhgz_lianhuagongzhu*:antenna_{}_pri_fk_3_ctrl".format(LR),
                  "lhgz_lianhuagongzhu*:antenna_{}_pri_fk_4_ctrl".format(LR),
                  "lhgz_lianhuagongzhu*:antenna_{}_pri_fk_5_ctrl".format(LR), )
        self.main_create_dynamic_rig()
        pm.currentTime(currentTime)
        LR="R"
        pm.select("lhgz_lianhuagongzhu*:antenna_{}_pri_fk_1_ctrl".format(LR),
                  "lhgz_lianhuagongzhu*:antenna_{}_pri_fk_2_ctrl".format(LR),
                  "lhgz_lianhuagongzhu*:antenna_{}_pri_fk_3_ctrl".format(LR),
                  "lhgz_lianhuagongzhu*:antenna_{}_pri_fk_4_ctrl".format(LR),
                  "lhgz_lianhuagongzhu*:antenna_{}_pri_fk_5_ctrl".format(LR), )
        self.main_create_dynamic_rig()

    def lrs_selectedDyn(self):
        pm.select("lhgz_lianhuagongzhu*__antenna_*_pri_fk_*_dynSys_ctrl")



class anim_ui(QMainWindow):
    def __init__(self, parent=mayaMainWindow):
        super(anim_ui, self).__init__(parent)
        self.setObjectName(_Win)
        self.setMinimumWidth(300)
        self.cls = anim_hair_tool()
        self.setupUi(self)

    def setupUi(self, MainWindows):
        MainWindows.resize(381, 317)
        self.centralwidget = QWidget(MainWindows)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QRect(9, 9, 361, 262))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_create_rig = QPushButton(self.verticalLayoutWidget)
        self.btn_create_rig.setMinimumSize(QSize(0, 40))
        self.btn_create_rig.setBaseSize(QSize(0, 0))
        self.btn_create_rig.setObjectName("btn_create_rig")
        self.verticalLayout.addWidget(self.btn_create_rig)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_edit = QPushButton(self.verticalLayoutWidget)
        self.btn_edit.setMinimumSize(QSize(0, 40))
        self.btn_edit.setObjectName("btn_edit")
        self.horizontalLayout.addWidget(self.btn_edit)
        self.btn_update = QPushButton(self.verticalLayoutWidget)
        self.btn_update.setMinimumSize(QSize(0, 40))
        self.btn_update.setObjectName("btn_update")
        self.horizontalLayout.addWidget(self.btn_update)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_bake = QPushButton(self.verticalLayoutWidget)
        self.btn_bake.setMinimumSize(QSize(176, 40))
        self.btn_bake.setObjectName("btn_bake")
        self.horizontalLayout_3.addWidget(self.btn_bake)
        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.sampleBy_line = QLineEdit(self.verticalLayoutWidget)
        self.sampleBy_line.setMinimumSize(QSize(0, 30))
        self.sampleBy_line.setObjectName("sampleBy_line")
        self.horizontalLayout_3.addWidget(self.sampleBy_line)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.btn_delete = QPushButton(self.verticalLayoutWidget)
        self.btn_delete.setMinimumSize(QSize(0, 40))
        self.btn_delete.setObjectName("btn_delete")
        self.verticalLayout.addWidget(self.btn_delete)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setMinimumSize(QSize(120, 40))
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.startTime_line = QLineEdit(self.verticalLayoutWidget)
        self.startTime_line.setMinimumSize(QSize(0, 30))
        self.startTime_line.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.startTime_line)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.lianhua_QHBoxLayout = QHBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.addLayout(self.lianhua_QHBoxLayout)


        self.btn_lianhua_createRig = QPushButton(self.verticalLayoutWidget)
        self.btn_lianhua_createRig.setMinimumSize(QSize(0, 40))
        self.btn_lianhua_createRig.setObjectName("btn_delete")
        self.lianhua_QHBoxLayout.addWidget(self.btn_lianhua_createRig)

        self.btn_lianhua_selectedDyn = QPushButton(self.verticalLayoutWidget)
        self.btn_lianhua_selectedDyn.setMinimumSize(QSize(0, 40))
        self.btn_lianhua_selectedDyn.setObjectName("btn_delete")
        self.lianhua_QHBoxLayout.addWidget(self.btn_lianhua_selectedDyn)


        MainWindows.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindows)
        self.menubar.setGeometry(QRect(0, 0, 381, 23))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindows.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindows)
        self.statusbar.setObjectName("statusbar")
        MainWindows.setStatusBar(self.statusbar)
        self.actionWiki = QAction(MainWindows)
        self.actionWiki.setObjectName("actionWiki")
        self.menuHelp.addAction(self.actionWiki)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindows)
        QMetaObject.connectSlotsByName(MainWindows)


    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QApplication.translate("MainWindows", "自动解算Fk动画工具", None, -1))
        self.btn_create_rig.setText(QApplication.translate("MainWindows", "创建动力学绑定", None, -1))
        self.btn_edit.setText(QApplication.translate("MainWindows", "编辑", None, -1))
        self.btn_update.setText(QApplication.translate("MainWindows", "更新", None, -1))
        self.btn_bake.setText(QApplication.translate("MainWindows", "烘培", None, -1))
        self.label_2.setText(QApplication.translate("MainWindows", "烘培帧间隔:", None, -1))
        self.btn_delete.setText(QApplication.translate("MainWindows", "删除", None, -1))
        self.label.setText(QApplication.translate("MainWindows", "开始时间：", None, -1))
        self.menuHelp.setTitle(QApplication.translate("MainWindows", "help", None, -1))
        self.actionWiki.setText(QApplication.translate("MainWindows", "wiki", None, -1))
        self.btn_lianhua_createRig.setText(QApplication.translate("MainWindows", "莲花绑定创建", None, -1))
        self.btn_lianhua_selectedDyn.setText(QApplication.translate("MainWindows", "选择控制器", None, -1))

        self.btn_create_rig.clicked.connect(lambda: self.cls.main_create_dynamic_rig())
        self.btn_edit.clicked.connect(lambda: self.cls.edit_sys())
        self.btn_update.clicked.connect(lambda: self.cls.update_anim())
        self.btn_bake.clicked.connect(lambda: self.cls.bake_all_ctrl_parent(self.get_sample_by()))
        self.btn_delete.clicked.connect(lambda: self.cls.delete_rig())
        self.btn_lianhua_createRig.clicked.connect(lambda: self.cls.lrs_createRig())
        self.btn_lianhua_selectedDyn.clicked.connect(lambda: self.cls.lrs_selectedDyn())

        self.btn_create_rig.setStyleSheet("background-color:rgb(120,150,120,255)")
        self.btn_edit.setStyleSheet("background-color:rgb(120,120,150,255)")
        self.btn_update.setStyleSheet("background-color:rgb(120,120,150,255)")
        self.btn_bake.setStyleSheet("background-color:rgb(150,150,120,255)")
        self.btn_delete.setStyleSheet("background-color:rgb(150,120,120,255)")
        self.btn_lianhua_createRig.setStyleSheet("background-color:rgb(150,120,150,255)")
        self.btn_lianhua_selectedDyn.setStyleSheet("background-color:rgb(150,120,150,255)")

        self.actionWiki.triggered.connect(self.open_web)
        self.startTime_line.setValidator(QIntValidator())
        self.startTime_line.setText("{}".format(self.get_start_time()))
        self.startTime_line.returnPressed.connect(self.set_start_time)
        self.startTime_line.editingFinished.connect(self.set_start_time)
        self.sampleBy_line.setValidator(QIntValidator())
        self.sampleBy_line.setText("{}".format(1))

        font = QFont(u"楷体")
        font.setPointSize(15)
        font.setBold(True)
        self.btn_create_rig.setFont(font)
        self.btn_edit.setFont(font)
        self.btn_update.setFont(font)
        self.btn_bake.setFont(font)
        self.btn_delete.setFont(font)
        self.label.setFont(font)
        self.label_2.setFont(font)
        self.actionWiki.setFont(font)
        self.btn_lianhua_createRig.setFont(font)
        self.btn_lianhua_selectedDyn.setFont(font)

    def get_sample_by(self):
        return float(self.sampleBy_line.text())

    def open_web(self):
        webbrowser.open("http://wiki.zhuiguang.com/display/RIG/hair_system_rig")

    def set_start_time(self):
        if pm.objExists("FK_Dynamic_RIG_GRP"):
            child = pm.listRelatives("FK_Dynamic_RIG_GRP", c=True)
            for i in child:
                if pm.nodeType(i) == "nucleus":
                    value = int(self.startTime_line.text())
                    pm.setAttr("{}.startFrame".format(i), value)
        else:
            pm.warning("nucleus not exists")

    def get_start_time(self):
        if pm.objExists("FK_Dynamic_RIG_GRP"):
            child = pm.listRelatives("FK_Dynamic_RIG_GRP", c=True)
            for i in child:
                if pm.nodeType(i) == "nucleus":
                    value = pm.getAttr("{}.startFrame".format(i))
                    return int(value)
        else:
            return int(pm.playbackOptions(q=True, min=True))


def main():
    if pm.window(_Win, ex=True):
        pm.deleteUI(_Win)
    win = anim_ui()
    win.show()


if __name__ == '__main__':
    main()



