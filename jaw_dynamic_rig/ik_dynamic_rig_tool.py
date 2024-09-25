#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/9 11:56
# @File    : add_ik_hairSystem_rig.py


import maya.OpenMaya as om
import maya.mel as mel

from __builtin__ import long
import maya.cmds as mc
import maya.OpenMayaUI as omui
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import shiboken2
import webbrowser
import functools
import traceback
import production.usage_mongodb

_Win = "ik_dynamic_rig_tool"
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


class jaw_dynamic_rig():
    def __init__(self):
        self.dyn_main_grp = "ik_dynamic_rig_grp"

    @undo
    def main(self):
        self.joint_array = []
        self.sel = []
        self.sel_pri_ctrl = []
        self.sel_sec_ctrl = []
        self.sel_count = 0
        self.bridge_loc_array = []
        self.rivet_loc_array = []
        self.blend_attr_array = []

        self.getSelectedCtrl()  # get select
        self.init_scenes()
        self.get_all_ctrl_pos(extend=True)  # 查询所有的控制器位置与旋转
        self.create_dyn_sys()  # 创建动力学主体
        self.rig_dynamic_curve()  # 绑定动力学
        self.create_main_ctrl(self.name)
        self.sys_info_records()

    def rig_dynamic_curve(self):
        for i in range(len(self.sel_sec_ctrl)):
            jnt = mc.createNode("joint", n="{}_{}_jnt".format(self.name, i))
            self.joint_array.append(jnt)

            rivet_loc = mc.spaceLocator(n="{}_{}_rivet_loc".format(self.name, i))[0]
            self.rivet_loc_array.append(rivet_loc)

            bridge_loc = mc.spaceLocator(n="{}_{}_bridge_loc".format(self.name, i))[0]
            self.bridge_loc_array.append(bridge_loc)

            self.sec_connect_joint(self.sel_sec_ctrl[i], self.joint_array[i], i)
            param = self.get_obj_on_curve_param(jnt, self.dyn_curve)
            self.create_control_loc(param, rivet_loc, i)
            self.loc_connect_pri(self.rivet_loc_array[i], self.bridge_loc_array[i], self.sel_pri_ctrl[i], i)

        mc.skinCluster(self.joint_array, self.dynCtrl_curveShape)

        jnt_grp = mc.createNode("transform", n="{}_jnt_grp".format(self.name))
        mc.parent(self.joint_array, jnt_grp)

        rivet_loc_grp = mc.createNode("transform", n="{}_rivet_grp".format(self.name))
        mc.parent(self.rivet_loc_array, rivet_loc_grp)
        mc.setAttr("{}.v".format(rivet_loc_grp), 0)

        bridge_loc_grp = mc.createNode("transform", n="{}_bridge_grp".format(self.name))
        mc.parent(self.bridge_loc_array, bridge_loc_grp)
        mc.setAttr("{}.v".format(bridge_loc_grp), 0)

        mc.parent(jnt_grp, self.dyn_each_grp)
        mc.parent(rivet_loc_grp, self.dyn_each_grp)
        mc.parent(bridge_loc_grp, self.dyn_each_grp)

    def create_control_loc(self, param, bridge_loc, index):
        pointOnCurve = mc.createNode("pointOnCurveInfo")
        mc.setAttr("{}.parameter".format(pointOnCurve), param)
        mc.connectAttr("{}.worldSpace".format(self.dyn_curve), "{}.inputCurve".format(pointOnCurve))
        mc.connectAttr("{}.position".format(pointOnCurve), "{}.t".format(bridge_loc))

    def loc_connect_pri(self, birdgeLoc, loc, pri, index):
        multMatrix = mc.createNode("multMatrix")
        decomposeMatrix = mc.createNode("decomposeMatrix")
        blendColors = mc.createNode("blendColors")
        mc.setAttr("{}.color2".format(blendColors), 0, 0, 0)
        mc.setAttr("{}.blender".format(blendColors), 1)
        mc.connectAttr("{}.worldMatrix".format(birdgeLoc), "{}.matrixIn[0]".format(multMatrix))
        mc.connectAttr("{}.matrixSum".format(multMatrix), "{}.inputMatrix".format(decomposeMatrix))
        mc.connectAttr("{}.outputTranslate".format(decomposeMatrix), "{}.color1".format(blendColors))
        mc.connectAttr("{}.output".format(blendColors), "{}.t".format(loc))
        mc.connectAttr("{}.tx".format(loc), "{}.tx".format(pri), f=True)
        mc.connectAttr("{}.ty".format(loc), "{}.ty".format(pri), f=True)
        mc.connectAttr("{}.tz".format(loc), "{}.tz".format(pri), f=True)

        mc.connectAttr("{}.parentInverseMatrix[0]".format(pri), "{}.matrixIn[1]".format(multMatrix))

        attrString = "control_{}_weight".format(index)
        mc.addAttr(self.hair_sys_info, ln=attrString, max=10, dv=1, at='double', min=0, keyable=True)
        mc.connectAttr("{}.{}".format(self.hair_sys_info, attrString), "{}.blender".format(blendColors))

        self.blend_attr_array.append(attrString)

    def sys_info_records(self):
        mc.setAttr("{}.solverDisplay".format(self.hairSystem), 1)
        mc.setAttr("{}.selfCollide".format(self.hairSystem), True)
        mc.setAttr("{}.subSteps".format(self.nucleus), 9)
        mc.setAttr("{}.maxCollisionIterations".format(self.nucleus), 12)

        self.add_label("follicle_tr", str(self.follicle_tr))
        self.add_label("follicle_node", str(self.follicle_node))
        self.add_label("follicle_parent", str(self.follicle_parent))
        self.add_label("dynCtrl_curveShape", str(self.dynCtrl_curveShape))
        self.add_label("dyn_curve", str(self.dyn_curve))
        self.add_label("dyn_curve_parent", str(self.dyn_curve_parent))
        self.add_label("hairSystem", str(self.hairSystem))
        self.add_label("hairSystemShape", str(self.hairSystemShape))
        self.add_label("nucleus", str(self.nucleus))

        self.add_label("sel_ctrl", self.list_to_str(self.sel))
        self.add_label("sel_pri_ctrl", self.list_to_str(self.sel_pri_ctrl))
        self.add_label("sel_sec_ctrl", self.list_to_str(self.sel_sec_ctrl))
        self.add_label("dyn_each_grp", str(self.dyn_each_grp))

    def sec_connect_joint(self, obj, jnt, index):

        decomposeMatrix = mc.createNode("decomposeMatrix")
        mc.connectAttr("{}.worldMatrix[0]".format(obj), "{}.inputMatrix".format(decomposeMatrix))
        mc.connectAttr("{}.outputTranslateX".format(decomposeMatrix), "{}.tx".format(jnt))
        mc.connectAttr("{}.outputTranslateY".format(decomposeMatrix), "{}.ty".format(jnt))
        mc.connectAttr("{}.outputTranslateZ".format(decomposeMatrix), "{}.tz".format(jnt))
        mc.connectAttr("{}.outputRotateX".format(decomposeMatrix), "{}.rx".format(jnt))
        mc.connectAttr("{}.outputRotateY".format(decomposeMatrix), "{}.ry".format(jnt))
        mc.connectAttr("{}.outputRotateZ".format(decomposeMatrix), "{}.rz".format(jnt))

    def get_obj_on_curve_param(self, obj, curve):
        paramUtil = om.MScriptUtil()
        paramPtr = paramUtil.asDoublePtr()
        t = mc.xform(obj, q=True, ws=True, t=True)
        point = om.MPoint(t[0], t[1], t[2])
        sel = om.MSelectionList()
        om.MGlobal.getSelectionListByName(curve, sel)
        path = om.MDagPath()
        sel.getDagPath(0, path)
        curveFn = om.MFnNurbsCurve(path)
        curveFn.closestPoint(point, paramPtr, 0.1e-6, om.MSpace.kWorld)
        result = om.MScriptUtil.getDouble(paramPtr)
        return result

    def getSelectedCtrl(self):
        self.sel = mc.ls(sl=True)
        self.sel_pri_ctrl = []
        self.sel_sec_ctrl = []
        self.sel_count = len(self.sel)
        for i in self.sel:
            p = mc.listRelatives(i, p=True)[0]
            self.sel_pri_ctrl.append(p)

        for i in self.sel_pri_ctrl:
            p = mc.listRelatives(i, p=True)[0]
            self.sel_sec_ctrl.append(p)

    def create_dyn_sys(self):
        mc.currentTime(1)
        mc.refresh()
        curve = self.create_curve("{}_dynCurve".format(self.name))  # 创建动力学结算曲线
        mc.select(curve)
        mel.eval('makeCurvesDynamic 2 { "1", "0", "1", "1", "0"};')

        self.follicle_tr = mc.listRelatives(curve, p=True)[0]
        self.follicle_node = mc.listRelatives(self.follicle_tr, s=True)[0]
        self.follicle_parent = mc.listRelatives(self.follicle_tr, p=True)[0]
        self.dynCtrl_curveShape = mc.listRelatives(curve, s=True)[0]
        self.dyn_curve = mc.listConnections("{}.outCurve".format(self.follicle_node))[0]
        self.dyn_curve_parent = mc.listRelatives(self.dyn_curve, p=True)[0]
        self.hairSystem = mc.listConnections("{}.outHair".format(self.follicle_node))[0]
        self.hairSystemShape = mc.listRelatives(self.hairSystem, s=True)[0]
        self.nucleus = mc.listConnections("{}.currentState".format(self.hairSystem))[0]
        mc.setAttr("{}.intermediateObject".format(self.dynCtrl_curveShape), 0)

        if mc.listRelatives(self.nucleus, p=True) == None:
            mc.parent(self.nucleus, self.dyn_main_grp)

        main_grp = mc.createNode("transform", n="{}_hairSys".format(curve))
        mc.parent(self.follicle_parent, main_grp)
        mc.parent(self.dyn_curve_parent, main_grp)
        mc.parent(self.hairSystem, self.dyn_each_grp)
        mc.parent(main_grp, self.dyn_each_DynamicRig_grp)

        return locals()

    def create_main_ctrl(self, name):
        self.main_ctrl = self.control_shapes(name="{}_dynSys_ctrl".format(name))
        selShape = mc.listRelatives(self.sel[-1], s=True)[0]

        # boundingBox_val = mc.getAttr("{}.boundingBox".format(selShape))[-1]
        # length_v = boundingBox_val.length()
        length_v = 0.2

        mc.setAttr("{}.s".format(self.main_ctrl), length_v, length_v, length_v)
        mc.makeIdentity(self.main_ctrl, n=0, s=1, r=1, t=1, apply=True, pn=1)
        self.main_ctrl_grp = mc.createNode("transform", n="{}_dynSys_grp".format(name))
        mc.parent(self.main_ctrl, self.main_ctrl_grp)

        mc.setAttr("{}.t".format(self.main_ctrl_grp),
                   self.pos_array[self.sel_count / 2 + 1][0],
                   self.pos_array[self.sel_count / 2 + 1][1],
                   self.pos_array[self.sel_count / 2 + 1][2])
        mc.parent(self.main_ctrl_grp, self.dyn_each_grp)
        mc.parentConstraint(self.sel[self.sel_count / 2], self.main_ctrl_grp, mo=True, sr=["x", "y", "z"])
        mc.setAttr("{}.tx".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)
        mc.setAttr("{}.ty".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)
        mc.setAttr("{}.tz".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)
        mc.setAttr("{}.rx".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)
        mc.setAttr("{}.ry".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)
        mc.setAttr("{}.rz".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)
        mc.setAttr("{}.sx".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)
        mc.setAttr("{}.sy".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)
        mc.setAttr("{}.sz".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)
        mc.setAttr("{}.v".format(self.main_ctrl), lock=True, channelBox=False, keyable=False)

        mc.addAttr(self.main_ctrl, ln="rig_info", dt="string")
        mc.setAttr('{}.rig_info'.format(self.main_ctrl), self.hair_sys_info, type="string")

        # mc.addAttr(self.main_ctrl, ln="envelope", max=10, dv=10, at='double', min=0, keyable=True)

        floatMath = mc.createNode("multiplyDivide")
        mc.setAttr("{}.operation".format(floatMath), 2)
        mc.setAttr("{}.input2X".format(floatMath), 10)
        # mc.connectAttr("{}.envelope".format(self.main_ctrl), "{}.input1X".format(floatMath))
        mc.connectAttr("{}.outputX".format(floatMath), "{}.dyn_blend".format(self.hair_sys_info))

        mc.addAttr('{}'.format(self.main_ctrl), ln="____________________", en="Control_Weights:", at="enum",
                   keyable=True)
        mc.setAttr("{}.____________________".format(self.main_ctrl), lock=True)

        for i in self.blend_attr_array:
            self.auto_connect_Attr(self.hair_sys_info, self.main_ctrl, 1, i)

        mc.addAttr('{}'.format(self.main_ctrl), ln="_____________________", en="Collide_Attribute:", at="enum",
                   keyable=True)
        mc.setAttr("{}._____________________".format(self.main_ctrl), lock=True)

        self.auto_connect_Attr(self.hairSystemShape, self.main_ctrl, 0.04, "collideWidthOffset")
        self.auto_connect_Attr(self.hairSystemShape, self.main_ctrl, 0.2, "bounce")
        self.auto_connect_Attr(self.hairSystemShape, self.main_ctrl, 0.1, "friction")
        self.auto_connect_Attr(self.hairSystemShape, self.main_ctrl, 0.0, "stickiness")

        mc.addAttr('{}'.format(self.main_ctrl), ln="______________________", en="Solver_Attribute:", at="enum",
                   keyable=True)
        mc.setAttr("{}.______________________".format(self.main_ctrl), lock=True)

        self.auto_connect_Attr(self.hairSystemShape, self.main_ctrl, 20.0, "stretchResistance")
        self.auto_connect_Attr(self.hairSystemShape, self.main_ctrl, 10.0, "compressionResistance")
        self.auto_connect_Attr(self.hairSystemShape, self.main_ctrl, 1.0, "bendResistance")
        self.auto_connect_Attr(self.hairSystemShape, self.main_ctrl, 1.0, "startCurveAttract")
        self.auto_connect_Attr(self.hairSystemShape, self.main_ctrl, 1.0, "mass")
        self.auto_connect_Attr(self.hairSystemShape, self.main_ctrl, 0.05, "drag")
        self.auto_connect_Attr(self.hairSystemShape, self.main_ctrl, 0.20, "damp")

        return name

    def control_shapes(self, name):
        cur = mc.curve(p=[[-0.24, 0.716, 0.0],
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
        curve_shape = mc.listRelatives(cur, s=True)[0]

        mc.setAttr("{}.overrideEnabled".format(curve_shape), True)
        mc.setAttr("{}.overrideColor".format(curve_shape), 9)
        return cur

    def auto_connect_Attr(self, dynamicSys, control, preValue, attr):

        attr_type = mc.getAttr("{}.{}".format(dynamicSys, attr), type=True)

        mc.addAttr(control, ln=attr, dv=preValue, at=attr_type, keyable=True)

        if mc.attributeQuery(attr, n=dynamicSys, maxExists=True):
            print True
            value = mc.attributeQuery(attr, n=dynamicSys, max=True)[0]
            mc.addAttr("{}.{}".format(control, attr), e=True, max=value)

        if mc.attributeQuery(attr, n=dynamicSys, minExists=True):
            value = mc.attributeQuery(attr, n=dynamicSys, min=True)[0]
            mc.addAttr("{}.{}".format(control, attr), e=True, min=value)

        mc.connectAttr("{}.{}".format(control, attr), "{}.{}".format(dynamicSys, attr))

    def get_all_ctrl_pos(self, extend=True):
        self.pos_array = []
        self.rotate_array = []

        for i in self.sel:
            t = mc.xform(i, q=True, ws=True, piv=True)[:-3]
            ro = mc.xform(i, q=True, ws=True, ro=True)
            self.pos_array.append(t)
            self.rotate_array.append(ro)

        if extend:
            endPos = self.getCenterPoint(self.pos_array[-2], self.pos_array[-1], 1.5)
            self.pos_array.append(endPos)
            endPos = self.getCenterPoint(self.pos_array[1], self.pos_array[0], 1.5)
            self.pos_array.insert(0, endPos)

        return self.pos_array

    def bakeResults(self, objArray, min_time, max_time, only_rotate=False, sample_by=1):
        print min_time, max_time
        if only_rotate:
            mc.bakeResults(objArray,
                           sparseAnimCurveBake=False, minimizeRotation=True, removeBakedAttributeFromLayer=False,
                           removeBakedAnimFromLayer=False, oversamplingRate=1, bakeOnOverrideLayer=False,
                           preserveOutsideKeys=True, simulation=True, sampleBy=1, shape=True,
                           t=(min_time, max_time), disableImplicitControl=True,
                           controlPoints=False, at=["rx", "ry", "rz"])
        else:
            mc.bakeResults(objArray,
                           sparseAnimCurveBake=False, minimizeRotation=True, removeBakedAttributeFromLayer=False,
                           removeBakedAnimFromLayer=False, oversamplingRate=1, bakeOnOverrideLayer=False,
                           preserveOutsideKeys=True, simulation=True, sampleBy=1, shape=True,
                           t=(min_time, max_time), disableImplicitControl=True,
                           controlPoints=False)
        mc.filterCurve(objArray, kernel='gaussian2', period=sample_by, f='resample')
        return True

    def getCenterPoint(self, PosA, PosB, Value):
        x = PosA[0] * (1 - Value) + PosB[0] * Value
        y = PosA[1] * (1 - Value) + PosB[1] * Value
        z = PosA[2] * (1 - Value) + PosB[2] * Value
        return [x, y, z]

    def init_scenes(self):
        self.min_time = int(mc.playbackOptions(q=True, min=True))
        self.max_time = int(mc.playbackOptions(q=True, max=True))
        self.all_time = int(self.max_time - self.min_time + 1)

        if not mc.objExists(self.dyn_main_grp):
            mc.createNode("transform", n=self.dyn_main_grp)

        self.name = self.sel[0].split("_ctrl")[0].replace(":", "__")
        self.dyn_each_grp = "{}_MainRig_grp".format(self.name)
        if mc.objExists(self.dyn_each_grp):
            mc.delete(self.dyn_each_grp)

        self.dyn_each_grp = mc.createNode("transform", n="{}_MainRig_grp".format(self.name))
        mc.parent(self.dyn_each_grp, self.dyn_main_grp)

        self.hair_sys_info = mc.createNode("transform", n="{}_DynamicInfo".format(self.name))
        mc.parent(self.hair_sys_info, self.dyn_each_grp)

        self.dyn_each_DynamicRig_grp = mc.createNode("transform", n="{}_DynamicRig_grp".format(self.name))
        mc.parent(self.dyn_each_DynamicRig_grp, self.dyn_each_grp)
        # self.dyn_each_DynamicRig_grp.v.set(0)

        mc.addAttr(self.hair_sys_info, ln="dyn_blend", max=1, dv=1, at='double', min=0, keyable=True)

        value = "{},{}".format(self.min_time, self.max_time)
        mc.addAttr(self.hair_sys_info, ln="time_data", dt="string")
        mc.setAttr('{}.time_data'.format(self.hair_sys_info), value, type="string")

    def add_label(self, attr, label_str):
        info = self.hair_sys_info
        mc.addAttr(info, ln=attr, dt="string")
        mc.setAttr('{}.{}'.format(info, attr), str(label_str), type="string")
        mc.setAttr("{}.{}".format(info, attr), l=True)

    def list_to_str(self, list_v):
        result = ''
        for i in list_v:
            if not list_v.index(i) == 0:
                result += ","
            result += i
        return result

    def create_curve(self, name):
        curve = mc.curve(p=self.pos_array, d=1, n=name)
        return curve

    @undo
    def bake_all_ctrl_parent(self, sample_by):
        sel = self.get_selected()
        if not sel: return

        all_sel_parent = []
        all_time_data = []
        for each_sel in sel:
            sel_parent_ctrl = self.get_label(each_sel, "sel_pri_ctrl")
            sel_parent_ctrl_array = sel_parent_ctrl.split(",")
            all_sel_parent += sel_parent_ctrl_array

            time_data = self.get_label(each_sel, "time_data")
            time_data_array = time_data.split(",")
            all_time_data += time_data_array
        self.bakeResults(all_sel_parent, all_time_data[0], all_time_data[1], False, sample_by)

    def get_selected(self):
        sel = mc.ls(sl=True)
        if len(sel) == 0:
            mc.warning("not selected!!!")
            return False

        for i in sel:
            if not str("dynSys_ctrl") in str(i):
                mc.warning("not selected dyn ctrl!!!")
                return False
        return sel

    def get_label(self, ctrl, attr):
        info = mc.getAttr("{}.rig_info".format(ctrl))
        data = mc.getAttr("{}.{}".format(info, attr))
        return data

    @undo
    def createCollide(self):
        sel = mc.ls(sl=True)
        mel.eval("makeCollideNCloth;")

    def clear_scene(self):
        children = mc.listRelatives(self.dyn_main_grp, c=True)
        main_rig = []
        for i in children:
            if mc.nodeType(i) == "transform":
                main_rig.append(i)

        if len(main_rig) == 0:
            mc.delete(self.dyn_main_grp)

    @undo
    def delete_rig(self):
        sel = self.get_selected()
        if not sel: return

        for each_sel in sel:
            dyn_each_grp = self.get_label(each_sel, "dyn_each_grp")
            dyn_each_grp_array = dyn_each_grp.split(",")
            mc.delete(dyn_each_grp_array)
            self.clear_scene()


class anim_ui(QMainWindow):
    def __init__(self, parent=mayaMainWindow):
        super(anim_ui, self).__init__(parent)
        self.setObjectName(_Win)
        self.setMinimumWidth(300)
        self.cls = jaw_dynamic_rig()
        self.setupUi(self)

    def setupUi(self, MainWindows):
        MainWindows.resize(381, 320)
        self.centralwidget = QWidget(MainWindows)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QRect(9, 9, 361, 260))
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
        # self.btn_edit = QPushButton(self.verticalLayoutWidget)
        # self.btn_edit.setMinimumSize(QSize(0, 40))
        # self.btn_edit.setObjectName("btn_edit")
        # self.horizontalLayout.addWidget(self.btn_edit)
        # self.btn_update = QPushButton(self.verticalLayoutWidget)
        # self.btn_update.setMinimumSize(QSize(0, 40))
        # self.btn_update.setObjectName("btn_update")
        # self.horizontalLayout.addWidget(self.btn_update)
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

        self.horizontalLayout_startTime = QHBoxLayout()
        self.horizontalLayout_startTime.setObjectName("horizontalLayout_2")
        self.label_startTime = QLabel(self.verticalLayoutWidget)
        self.label_startTime.setMinimumSize(QSize(120, 40))
        self.label_startTime.setObjectName("label")
        self.horizontalLayout_startTime.addWidget(self.label_startTime)
        self.startTime_line = QLineEdit(self.verticalLayoutWidget)
        self.startTime_line.setMinimumSize(QSize(0, 30))
        self.startTime_line.setObjectName("lineEdit")
        self.horizontalLayout_startTime.addWidget(self.startTime_line)
        self.verticalLayout.addLayout(self.horizontalLayout_startTime)

        self.horizontalLayout_gravity = QHBoxLayout()
        self.horizontalLayout_gravity.setObjectName("horizontalLayout_gravity")
        self.label_gravity = QLabel(self.verticalLayoutWidget)
        self.label_gravity.setMinimumSize(QSize(120, 40))
        self.label_gravity.setObjectName("label")
        self.horizontalLayout_gravity.addWidget(self.label_gravity)
        self.gravity_line = QLineEdit(self.verticalLayoutWidget)
        self.gravity_line.setMinimumSize(QSize(0, 30))
        self.gravity_line.setObjectName("lineEdit")
        self.horizontalLayout_gravity.addWidget(self.gravity_line)
        self.verticalLayout.addLayout(self.horizontalLayout_gravity)

        self.lianhua_QHBoxLayout = QHBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.addLayout(self.lianhua_QHBoxLayout)

        self.btn_createCollide = QPushButton(self.verticalLayoutWidget)
        self.btn_createCollide.setMinimumSize(QSize(0, 40))
        self.btn_createCollide.setObjectName("btn_createCollide")
        self.lianhua_QHBoxLayout.addWidget(self.btn_createCollide)

        # self.btn_lianhua_createRig = QPushButton(self.verticalLayoutWidget)
        # self.btn_lianhua_createRig.setMinimumSize(QSize(0, 40))
        # self.btn_lianhua_createRig.setObjectName("btn_delete")
        # self.lianhua_QHBoxLayout.addWidget(self.btn_lianhua_createRig)

        # self.btn_lianhua_selectedDyn = QPushButton(self.verticalLayoutWidget)
        # self.btn_lianhua_selectedDyn.setMinimumSize(QSize(0, 40))
        # self.btn_lianhua_selectedDyn.setObjectName("btn_delete")
        # self.lianhua_QHBoxLayout.addWidget(self.btn_lianhua_selectedDyn)

        # self.btn_lianhua_createRig.setVisible(False)
        # self.btn_lianhua_selectedDyn.setVisible(False)
        # self.btn_edit.setVisible(False)
        # self.btn_update.setVisible(False)

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
        MainWindow.setWindowTitle(QApplication.translate("MainWindows", "自动解算Ik动画工具（TEST）", None, -1))
        self.btn_create_rig.setText(QApplication.translate("MainWindows", "创建动力学绑定", None, -1))
        self.btn_bake.setText(QApplication.translate("MainWindows", "烘培", None, -1))
        self.label_2.setText(QApplication.translate("MainWindows", "烘培帧间隔:", None, -1))
        self.btn_delete.setText(QApplication.translate("MainWindows", "删除", None, -1))
        self.label_startTime.setText(QApplication.translate("MainWindows", "开始时间：", None, -1))
        self.label_gravity.setText(QApplication.translate("MainWindows", "重力：", None, -1))
        self.menuHelp.setTitle(QApplication.translate("MainWindows", "help", None, -1))
        self.actionWiki.setText(QApplication.translate("MainWindows", "wiki", None, -1))
        self.btn_createCollide.setText(QApplication.translate("MainWindows", "创建碰撞体", None, -1))

        self.btn_create_rig.clicked.connect(lambda: self.cls.main())
        self.btn_bake.clicked.connect(lambda: self.cls.bake_all_ctrl_parent(self.get_sample_by()))
        self.btn_delete.clicked.connect(lambda: self.cls.delete_rig())
        self.btn_createCollide.clicked.connect(lambda: self.cls.createCollide())

        self.btn_create_rig.setStyleSheet("background-color:rgb(120,150,120,255)")
        self.btn_bake.setStyleSheet("background-color:rgb(150,150,120,255)")
        self.btn_delete.setStyleSheet("background-color:rgb(150,120,120,255)")
        self.btn_createCollide.setStyleSheet("background-color:rgb(150,120,150,255)")

        self.actionWiki.triggered.connect(self.open_web)
        self.startTime_line.setValidator(QIntValidator())
        self.startTime_line.setText("{}".format(self.get_start_time()))
        self.startTime_line.returnPressed.connect(self.set_start_time)
        self.startTime_line.editingFinished.connect(self.set_start_time)

        self.gravity_line.setValidator(QDoubleValidator())
        self.gravity_line.setText("{}".format(self.get_gravity()))
        self.gravity_line.returnPressed.connect(self.set_gravity)
        self.gravity_line.editingFinished.connect(self.set_gravity)

        self.sampleBy_line.setValidator(QIntValidator())
        self.sampleBy_line.setText("{}".format(1))

        font = QFont(u"楷体")
        font.setPointSize(15)
        font.setBold(True)
        self.btn_create_rig.setFont(font)
        self.btn_bake.setFont(font)
        self.btn_delete.setFont(font)
        self.label_startTime.setFont(font)
        self.label_gravity.setFont(font)
        self.label_2.setFont(font)
        self.actionWiki.setFont(font)
        self.btn_createCollide.setFont(font)

    def get_sample_by(self):
        return float(self.sampleBy_line.text())

    def open_web(self):
        webbrowser.open("http://wiki.zhuiguang.com/display/RIG/ik_hairSystem_rig")

    def set_start_time(self):
        if mc.objExists(self.cls.dyn_main_grp):
            child = mc.listRelatives(self.cls.dyn_main_grp, c=True)
            for i in child:
                if mc.nodeType(i) == "nucleus":
                    value = int(self.startTime_line.text())
                    mc.setAttr("{}.startFrame".format(i), value)
        else:
            om.MGlobal.displayWarning("nucleus not exists")

    def get_start_time(self):
        if mc.objExists(self.cls.dyn_main_grp):
            child = mc.listRelatives(self.cls.dyn_main_grp, c=True)
            for i in child:
                if mc.nodeType(i) == "nucleus":
                    value = mc.getAttr("{}.startFrame".format(i))
                    return int(value)
        else:
            return int(mc.playbackOptions(q=True, min=True))

    def set_gravity(self):
        if mc.objExists(self.cls.dyn_main_grp):
            child = mc.listRelatives(self.cls.dyn_main_grp, c=True)
            for i in child:
                if mc.nodeType(i) == "nucleus":
                    value = float(self.gravity_line.text())
                    mc.setAttr("{}.gravity".format(i), value)
        else:
            om.MGlobal.displayWarning("nucleus not exists")

    def get_gravity(self):
        if mc.objExists(self.cls.dyn_main_grp):
            child = mc.listRelatives(self.cls.dyn_main_grp, c=True)
            for i in child:
                if mc.nodeType(i) == "nucleus":
                    value = mc.getAttr("{}.gravity".format(i))
                    return round(value, 3)
        else:
            return 9.8


@production.usage_mongodb.Usage('ik_hairSystem_rig', dept='ani')
def main():
    if mc.window(_Win, ex=True):
        mc.deleteUI(_Win)
    win = anim_ui()
    win.show()


if __name__ == '__main__':
    main()
    # cls = jaw_dynamic_rig()
    # cls.main()  # 创建动力写rig
    # cls.bake_all_ctrl_parent(1)  # bake控制器动画
    # cls.createCollide()  # 创建碰撞体
    # cls.delete_rig()  # 删除动力学rig

    # cls.auto_connect_Attr("hairSystemShape1", "wb_lingchanshangren__rourou_10_bind_secondary_dynSys_ctrl", "opacity")
    # print cls.loc_connect_pri("locator6","wb_lingchanshangren:rourou_6_bind_secondary_pri_ctrl")
