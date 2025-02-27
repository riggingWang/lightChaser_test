#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/28 10:42
# @File    : armour_common.py

import maya.cmds as mc
import pymel.core as pm
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
import maya.mel as mel
import traceback
import functools


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


def wrap(control, target):
    mc.select(target, control)
    mel.eval('doWrapArgList "7" { "1","0","1", "2", "1", "1", "0", "0" };')
    history = mc.listHistory(target, pdo=1)
    wrap_array = []
    for i in history:
        if mc.nodeType(i) == "wrap":
            wrap_array.append(i)
    wrap = wrap_array[0]
    baseGeo = mc.listConnections("{}.basePoints[0]".format(wrap))[0]
    return wrap, baseGeo


def curveFormEdge(control, targets):
    cv_count = 0
    for target_index, target in enumerate(targets):
        cv_array =  mc.ls("{}.cv[*]".format(target), fl=True)
        if target_index == 0:
            cv_count = len(cv_array)
            continue
        if not cv_count == len(cv_array):
            print "Different quantities"
            return


    curve_count = len(targets)
    print cv_count
    print curve_count
    total_count = cv_count * curve_count

    index_data = []
    for i in range(curve_count):
        it = i
        each_curve_index_array = [i]
        for j in range(cv_count):
            it = it + curve_count
            each_curve_index_array.append(it)
        each_curve_index_array.remove(each_curve_index_array[-1])
        index_data.append(each_curve_index_array)

    for i in index_data[:3]:
        mc.select(d=True)
        for j in i:
            print j

            mc.select("{}.vtx[{}]".format(control, j), tgl=True)
            mc.refresh()

        mc.ConvertSelectionToContainedEdges()

    return



if __name__ == '__main__':
    curveFormEdge("body_up_editMesh", [u'body_up_M_0_curveGuide_splineIK_crv_EditCurve',
                                                   u'body_up_L_1_curveGuide_splineIK_crv_EditCurve',
                                                   u'body_up_L_2_curveGuide_splineIK_crv_EditCurve',
                                                   u'body_up_L_3_curveGuide_splineIK_crv_EditCurve',
                                                   u'body_up_L_4_curveGuide_splineIK_crv_EditCurve',
                                                   u'body_up_L_5_curveGuide_splineIK_crv_EditCurve',
                                                   u'body_up_M_6_curveGuide_splineIK_crv_EditCurve',
                                                   u'body_up_R_5_curveGuide_splineIK_crv_EditCurve',
                                                   u'body_up_R_4_curveGuide_splineIK_crv_EditCurve',
                                                   u'body_up_R_3_curveGuide_splineIK_crv_EditCurve',
                                                   u'body_up_R_2_curveGuide_splineIK_crv_EditCurve',
                                                   u'body_up_R_1_curveGuide_splineIK_crv_EditCurve'])



def batchCopyWeights():
    selGeo = pm.ls(sl=True, fl=True)
    infJoint = pm.skinCluster(selGeo[0], q=True, inf=True)
    for i in selGeo:
        if i == selGeo[0]:
            continue
        aimSkinNode = pm.listHistory(i, pdo=True, type="skinCluster")
        if len(aimSkinNode) == 0:
            pm.skinCluster(infJoint, i, tsb=True)
        pm.copySkinWeights(selGeo[0], i, surfaceAssociation='closestPoint', influenceAssociation='closestJoint',
                           noMirror=1)
    pm.select(selGeo)


def listHistory(obj):
    result = mc.listHistory(obj, pdo=True)
    if result == None:
        result = []
    return result


def find_skinNode(obj):
    targetSkin = listHistory(obj)
    targetSkin = [i for i in targetSkin if mc.nodeType(i) == "skinCluster"]
    return targetSkin


def get_blend_node(object):
    array = mc.listHistory(object, pdo=True)
    if array == None:
        array = []
    blend = []
    for i in array:
        if mc.nodeType(i) == "blendShape":
            blend.append(i)
    return blend

def get_MObject(obj):
    MObj = om.MObject()
    MSel = om.MSelectionList()
    MSel.add(obj)
    MSel.getDependNode(0, MObj)
    return MObj


def copyWeights(object, target):
    try:
        infJoint = mc.skinCluster(object, q=True, inf=True)
    except:
        return
    targetSkin = listHistory(target)
    targetSkin = [i for i in targetSkin if mc.nodeType(i) == "skinCluster"]
    mc.delete(targetSkin)
    mc.skinCluster(infJoint, target, tsb=True)
    mc.copySkinWeights(object, target, surfaceAssociation='closestPoint', influenceAssociation='closestJoint',
                       noMirror=1)


def getChlidren(obj):
    result = mc.listRelatives(obj, c=True)
    if result == None:
        result = []
    return result


def mirror_joint(joint):
    result = []
    for i in joint:
        if "_L_" in i:
            re = mc.mirrorJoint(i, mirrorBehavior=1, mirrorYZ=1, searchReplace=("_L_", "_R_"))
            result.append(re)
        elif "_R_" in i:
            re = mc.mirrorJoint(i, mirrorBehavior=1, mirrorYZ=1, searchReplace=("_R_", "_L_"))
            result.append(re)
    return result


def mirror_guide_joint(guideGrp):
    child = mc.listRelatives(guideGrp, c=True)
    if len(child) == 1:
        if "_L_" in child[0]:
            new_name = child[0].replace("_L_", "_R_")
            new_grp = mc.createNode("transform", n=new_name)
            mc.parent(new_grp, guideGrp)
            joint_array = mc.listRelatives("{}".format(child[0]), c=True)
            new_joints = mirror_joint(joint_array)
            for i in new_joints:
                mc.parent(i[0], new_grp)


def addAttribute(obj, type="str", attr_name="attr", value=None):
    if type == "str":
        if not mc.attributeQuery(attr_name, node=obj, ex=True):
            mc.addAttr(obj, ln=attr_name, dt="string", keyable=True)
        mc.setAttr("{}.{}".format(obj, attr_name), value, type="string")

def create_polyFacet(curve, skin=True):
    cvArray = mc.ls("{}.cv[*]".format(curve), fl=True)
    posArray = []
    for i in cvArray:
        pos = mc.xform(i, q=True, ws=True, t=True)
        posArray.append(pos)
    temp_poly = mc.polyCreateFacet(p=posArray, s=1, ch=False, tx=1, n="{}_poly".format(curve))[0]
    polyArray = mc.ls("{}.vtx[*]".format(temp_poly), fl=True)

    if skin:
        infJoint = mc.skinCluster(curve, q=True, inf=True)
        curve_skin = find_skinNode(curve)[0]
        temp_poly_skin = mc.skinCluster(infJoint, temp_poly, tsb=True)[0]
        for i in range(len(cvArray)):
            weights = mc.skinPercent(curve_skin, cvArray[i], query=True, value=True)
            mc.skinPercent(temp_poly_skin, polyArray[i], tv=zip(infJoint, weights))
    return temp_poly

def get_lcPoseDeformer(object):
    array = mc.listHistory(object, pdo=True)
    if array == None:
        array = []
    blend = []
    for i in array:
        if mc.nodeType(i) == "lcPoseDeformer":
            blend.append(i)
    return blend

def find_lcPoseDeformer_targetWeights(node):
    MSel = om.MSelectionList()
    MSel.add(node)
    MObj = om.MObject()
    MSel.getDependNode(0, MObj)
    depNodeFn = om.MFnDependencyNode(MObj)  # main node
    weightPlug = depNodeFn.findPlug("targetWeights", False)
    indexArray = []
    nameArray = []
    weights = []
    for i in range(weightPlug.numElements()):
        elementPlug = weightPlug.elementByPhysicalIndex(i)
        indexArray.append(i)
        nameArray.append(elementPlug.name())
        weights.append(elementPlug.asDouble())
    return zip(indexArray, nameArray, weights)


def polyToCurve(mesh):
    point_array = mc.ls("{}.vtx[*]".format(mesh), fl=True)
    pos_array = []
    for i in point_array:
        pos = mc.xform(i, q=True, ws=True, t=True)
        pos_array.append(pos)
    curve = mc.curve(p=pos_array, d=3, n="{}_lcaPoseDeform".format(mesh.split("_EditCurve")[0]))
    curveShape = mc.listRelatives(curve, s=True)[0]
    mc.delete(mesh)
    mc.rename(curveShape, "{}Shape".format(curve))
    return curve



def orderAddBlendShapeTarget(target, object):
    targetShape = mc.listRelatives(target, s=True)[0]
    objectShape = mc.listRelatives(object, s=True)[0]
    target_MObj = get_MObject(targetShape)
    object_MObj = get_MObject(objectShape)
    blend_array = get_blend_node(objectShape)
    if len(blend_array) == 0:
        blend_array = mc.blendShape(object, frontOfChain=True)
    blendShapeMFn = oma.MFnBlendShapeDeformer(get_MObject(blend_array[0]))
    indexList = om.MIntArray()
    blendShapeMFn.weightIndexList(indexList)
    if len(indexList) == 0:
        endIndex = 0
    else:
        endIndex = indexList[-1] + 1
    blendShapeMFn.addTarget(object_MObj, endIndex, target_MObj, 1)
    return "{}.w[{}]".format(blend_array[0], endIndex)




class copyBlendShape():
    def __init__(self):
        pass

    def getBlendTargets(self, blendShape):
        sel = om.MSelectionList()
        sel.add(blendShape)
        MObject = om.MObject()
        sel.getDependNode(0, MObject)
        blendFn = oma.MFnBlendShapeDeformer(MObject)
        MIntArray = om.MIntArray()
        blendFn.weightIndexList(MIntArray)
        index_array = []
        alias_array = []
        for i in MIntArray:
            name = mel.eval('aliasAttr("-q", "{}.w[{}]")'.format(blendShape, i))
            index_array.append(i)
            alias_array.append(name)
        return zip(index_array, alias_array)

    def copy_blendShape(self, mesh, curve):
        meshShape = mc.listRelatives(mesh, s=True)[0]
        blend_array = get_blend_node(meshShape)
        if len(blend_array) == 0:
            return
        blendNode = blend_array[0]
        bsTargets = self.getBlendTargets(blendNode)

        curveShape = mc.listRelatives(curve, s=True)[0]
        mc.delete(get_blend_node(curveShape))

        for index, alias in bsTargets:
            connect_attr = mc.listConnections("{}.w[{}]".format(blendNode, index), plugs=True)
            if connect_attr:
                mc.disconnectAttr(connect_attr[0], "{}.w[{}]".format(blendNode, index))

            mc.setAttr("{}.w[{}]".format(blendNode, index), 0)
            dup_curve = self.duplicate(curve, n="{}".format(alias))
            wrap_data = wrap(mesh, dup_curve)
            mc.setAttr("{}.w[{}]".format(blendNode, index), 1)
            mc.delete(dup_curve, ch=True)
            mc.delete(wrap_data[1])
            mc.setAttr("{}.w[{}]".format(blendNode, index), 0)
            bs = self.addBlendTargets(dup_curve, curve, index)
            mc.delete(dup_curve)

            if connect_attr:
                mc.connectAttr(connect_attr[0], "{}.w[{}]".format(blendNode, index))
                mc.connectAttr(connect_attr[0], "{}.w[{}]".format(bs, index), f=True)


    def duplicate(self, obj, n):
        dup = mc.duplicate(obj, n="{}".format(n))[0]
        shape = mc.listRelatives(dup, s=True, f=True)[0]
        mc.rename(shape, "{}Shape".format(dup))
        return dup


    def get_MDagPath(self, obj):
        mSel = om.MSelectionList()
        om.MGlobal.getSelectionListByName(obj, mSel)
        path = om.MDagPath()
        mSel.getDagPath(0, path)
        return path

    def addBlendTargets(self, target, object, index):
        targetShape = mc.listRelatives(target, s=True)[0]
        objectShape = mc.listRelatives(object, s=True)[0]
        target_MObj = get_MObject(targetShape)
        object_MObj = get_MObject(objectShape)
        blend_array = get_blend_node(object)
        if len(blend_array) == 0:
            blend_array = mc.blendShape(object, frontOfChain=True)
        bsFn = oma.MFnBlendShapeDeformer(get_MObject(blend_array[0]))
        bsFn.removeTarget(object_MObj, index, target_MObj, 1)
        bsFn.addTarget(object_MObj, index, target_MObj, 1)
        bsFn.setWeight(index, 0)
        return bsFn.name()



class EditMesh():
    def __init__(self):
        self.edit_grp = "TEMP_{}_edit_grp"
        self.curveEdit_grp = "TEMP_{}_curveEdit_grp"
        self.splitStr = "   -->   "
        self.copy_blend = copyBlendShape()

    @undo
    def createEditMesh(self, prefix):
        self.crv_grp = "{}_armor_tri_IkCrv_grp".format(prefix)

        child = getChlidren(self.crv_grp)
        if len(child) == 0:
            return
        TEMP_edit_grp = mc.createNode("transform", n="TEMP_{}_edit_grp".format(prefix))
        TEMP_curve_edit_grp = mc.createNode("transform", n="TEMP_{}_curveEdit_grp".format(prefix))
        mc.parent(TEMP_curve_edit_grp, TEMP_edit_grp)

        child_sort = self.curve_array_sort(child)
        new_curve_array = []
        for i in child_sort:
            curve, pos_array = self.curveEpToCv(i)
            new_curve_array.append(curve)
            mc.parent(curve, TEMP_curve_edit_grp)

        mesh = self.custom_loft(new_curve_array, prefix)

        mc.addAttr(mesh, ln="switch", max=1, dv=1, at='double', min=0, keyable=True)
        wrap_node = wrap(mesh, new_curve_array)
        mc.parent(mesh, wrap_node[1], TEMP_edit_grp)
        mc.setAttr("{}.hio".format(wrap_node[1]), True)

        for i in range(len(new_curve_array[:-1])):
            blendNode = mc.blendShape(new_curve_array[i], child_sort[i], w=[(0, 1)], before=True,
                                      n="{}_bs".format(new_curve_array[i]))[0]
            addAttribute(new_curve_array[i], type="str", attr_name="blend_node", value=blendNode)
            addAttribute(new_curve_array[i], type="str", attr_name="blend_object", value=child_sort[i])
            mc.connectAttr("{}.switch".format(mesh), "{}.w[0]".format(blendNode))
        mc.delete(new_curve_array[-1])
        mc.select(mesh)

    @undo
    def deleteEditMesh(self, prefix, progressBar):
        self.progressBar = progressBar
        self.progressBar.setFormat("copy weights and blendShape :    %p%")
        self.progressBar.show()
        self.progressBar.setProperty("value", 1)

        editMesh = "{}_editMesh".format(prefix)
        curveEdit_grp = self.curveEdit_grp.format(prefix)
        mc.setAttr("{}.switch".format(editMesh), 0)

        editCurve_array = mc.listRelatives(curveEdit_grp)
        blend_node_array = []
        blend_object_array = []
        for i in editCurve_array:
            blend_node = mc.getAttr("{}.blend_node".format(i))
            blend_node_array.append(blend_node)

            blend_object = mc.getAttr("{}.blend_object".format(i))
            blend_object_array.append(blend_object)
        mc.delete(blend_node_array)

        percent = 100.0 / len(blend_object_array)
        iter = 0
        for i in blend_object_array:
            copyWeights(editMesh, i)
            self.copy_blend.copy_blendShape(editMesh, i)
            iter += percent
            mc.setAttr("{}.inheritsTransform".format(i), False)
            self.progressBar.setProperty("value", iter)

        #  -------------copy lcPoseDeformer-------------
        meshShape = mc.listRelatives(editMesh, s=True)[0]  # 找到Shape
        lcPoseDeformerArray = get_lcPoseDeformer(meshShape)
        if len(lcPoseDeformerArray) == 0:
            return
        lcPoseDeformerNode = lcPoseDeformerArray[0]  # 找到lcDeform 节点
        lcPoseDfmWeights = find_lcPoseDeformer_targetWeights(lcPoseDeformerNode)  # 所有target

        self.progressBar.setFormat("copy lcPoseDeformer :    %p%")
        percent = 100.0 / len(lcPoseDfmWeights)
        iter = 0

        bridge_Mesh_array = []
        for i in blend_object_array:
            bridge_Mesh = create_polyFacet(i)  # 1.在初始pose绑定poly。  “bridge_Mesh“
            bridge_Mesh_array.append(bridge_Mesh)

        blendArray = get_blend_node(meshShape)
        if not len(blendArray) == 0:
            mc.setAttr("{}.envelope".format(blendArray[0]), 0)

        for index, alias, value in lcPoseDfmWeights:  # 索引,名称,初始值.(each targets)  遍历28个姿势
            print index, alias, value
            rbfPoseNurbs = alias.split(".")[-1].split("___")[0]  # pose_*
            ctrl = mc.getAttr("{}.ctrlName".format(rbfPoseNurbs))  # 控制器
            rotate = mc.getAttr("{}.Rotation".format(rbfPoseNurbs))[0]  # 旋转值
            mc.setAttr("{}.r".format(ctrl), rotate[0], rotate[1], rotate[2], type="double3")  # 2.设置pose。
            for i in lcPoseDfmWeights:  # 关掉其余目标
                if alias == i[1]:
                    mc.setAttr(i[1], 1)
                else:
                    mc.setAttr(i[1], 0)
            for index, curve in enumerate(blend_object_array):  # 遍历12根曲线
                pose_mesh = create_polyFacet("{}_EditCurve".format(curve), skin=False)  # 4.查询 "TEMP_*_curveEdit_grp" 每个点的位置，并且按照每个点位置生成poly。(有pose poly)
                inverstShape = mc.invertShape(bridge_Mesh_array[index], pose_mesh)  # 5.第一步和的第四步创建出来的poly，反减模型.
                mc.delete(pose_mesh)
                inverstCurve = polyToCurve(inverstShape)  # 6.按模型创建curve
                inverstTarget = mc.rename(inverstCurve, "{}__{}_lcPD".format(curve, rbfPoseNurbs))
                poseTarget = orderAddBlendShapeTarget(inverstTarget, curve)
                output = mc.listConnections(alias, p=True)[0]
                mc.connectAttr(output, poseTarget)
                mc.delete(inverstTarget)

            mc.setAttr("{}.r".format(ctrl), 0, 0, 0, type="double3")  # 2.设置pose   0。

            iter += percent
            self.progressBar.setProperty("value", iter)

        mc.delete(self.edit_grp.format(prefix))
        mc.delete(bridge_Mesh_array)
        self.progressBar.hide()

    def curve_array_sort(self, curve_array):
        new_array = []
        R_array = []
        for i in curve_array:
            if not "_R_" in str(i):
                new_array.append(i)
            else:
                R_array.append(i)
        R_array.sort(reverse=True)
        new_array = new_array + R_array + [new_array[0]]
        return new_array

    def curveEpToCv(self, curve):
        cv_array = mc.ls("{}.cv[*]".format(curve), fl=True)
        pos_array = []
        for i in cv_array:
            pos = mc.xform(i, q=True, ws=True, t=True)
            pos_array.append(pos)
        name = "{}_EditCurve".format(curve)

        if mc.objExists(name):
            name = name + "_ring"
        new_curve = mc.curve(p=pos_array, d=3, n=name)
        return new_curve, pos_array

    def custom_loft(self, curve_array, prefix):
        editMesh, loft = mc.loft(curve_array, c=0, ch=True, d=1, ss=1, rsn=True, ar=1, u=1, rn=0, po=1,
                                 n="{}_editMesh".format(prefix))
        nurbsTessellate_Attr = mc.listConnections("{}.outputSurface".format(loft), p=1)
        nurbsTessellate = nurbsTessellate_Attr[0].split(".")[0]
        pm.setAttr("{}.format".format(nurbsTessellate), 3)
        mc.delete(editMesh, ch=True)
        mc.polyNormal(ch=False, normalMode=4)
        mc.polyMergeVertex(editMesh, ch=False, am=1, d=0.01)
        return editMesh


if __name__ == '__main__':
    pass
