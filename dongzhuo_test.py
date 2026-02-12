#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2025/2/27 10:06
# @File    : dongzhuo_test.py

import maya.cmds as mc
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma

print "2026.0212"




def listRelatives(obj, parent=True):
    if parent:
        result = mc.listRelatives(obj, p=True)
    else:
        result = mc.listRelatives(obj, c=True)

    if result == None:
        result = []
    return result

def findParent(obj):
    parent = listRelatives(obj)
    if parent == []:
        return parent
    return parent + findParent(parent)

def findChild(obj):
    parent = listRelatives(obj,  parent=False)
    if parent == []:
        return parent
    return parent + findChild(parent)




def getTransform(obj):
    node_type = mc.nodeType(obj)
    joint_t = mc.getAttr("{}.t".format(obj))[0]
    joint_r = mc.getAttr("{}.r".format(obj))[0]
    joint_s = mc.getAttr("{}.s".format(obj))[0]
    joint_o = []
    if mc.nodeType(obj) == "joint":
        joint_o = mc.getAttr("{}.jo".format(obj))[0]
    return joint_t, joint_r, joint_s, joint_o, node_type

def setTransform(obj, transform):
    mc.setAttr("{}.t".format(obj), transform[0][0], transform[0][1], transform[0][2], type="double3")
    mc.setAttr("{}.r".format(obj), transform[1][0], transform[1][1], transform[1][2], type="double3")
    mc.setAttr("{}.s".format(obj), transform[2][0], transform[2][1], transform[2][2], type="double3")
    if mc.nodeType(obj) == "joint":
        mc.setAttr("{}.jo".format(obj), transform[3][0], transform[3][1], transform[3][2], type="double3")


def getDeformNode(obj, type):
    all_history = mc.ls(mc.listHistory(obj), type=type)[0]
    return all_history


def rebuildSkeletalChain(geo, suffix):


    inf_joint = mc.skinCluster(geo, q=True, inf=True)
    parent_data = []
    transform_data = []

    for eachJnt in inf_joint:
        parent_array = [eachJnt] + findParent(eachJnt)
        array_length = len(parent_array)
        for i, item in enumerate(parent_array):
            new_name = item + suffix
            if mc.objExists(new_name):
                continue

            itemType = mc.nodeType(item)
            new_node = mc.createNode(itemType, n=new_name)
            transform_data.append(getTransform(item))
            if not i+1 == array_length:
                parent_data.append([new_node, parent_array[i + 1] + suffix])
            else:
                parent_data.append([new_node])

    for i, item in enumerate(transform_data):
        if not len(parent_data[i]) == 1:
            mc.parent(parent_data[i][0], parent_data[i][1])

    for i, item in enumerate(transform_data):
        setTransform(parent_data[i][0], item)





def getMObject(obj):
    MObj = om.MObject()
    MSel = om.MSelectionList()
    MSel.add(obj)
    MSel.getDependNode(0, MObj)
    return MObj

def getDagPath(obj):
    MPath = om.MDagPath()
    MSel = om.MSelectionList()
    MSel.add(obj)
    MSel.getDagPath(0, MPath)
    return MPath

def replaceSkinJoint(obj, suffix):
    vtx_array = mc.ls("{}.vtx[*]".format(obj), fl=True)
    shape = mc.listRelatives(obj, s=True)[0]
    skinCluster = getDeformNode(shape, "skinCluster")
    inf_joint = mc.skinCluster(skinCluster, q=True, inf=True)

    weights_data = []
    for i in range(len(vtx_array)):
        vtx = i
        component = om.MFnSingleIndexedComponent().create(om.MFn.kMeshVertComponent)
        om.MFnSingleIndexedComponent(component).addElement(vtx)

        s = om.MScriptUtil()
        UintPtr = s.asUintPtr()
        # om.MScriptUtil.setUint(UintPtr, 43)
        # print om.MScriptUtil.getUint(IntPtr)
        skinFn = oma.MFnSkinCluster(getMObject(skinCluster))
        doubleArray = om.MDoubleArray()
        skinFn.getWeights(getDagPath(obj), component, doubleArray, UintPtr)
        weights_data.append(doubleArray)
        # print doubleArray

    bindPreMatrix_array = []
    for i, item in enumerate(inf_joint):
        matrix = mc.getAttr("{}.bindPreMatrix[{}]".format(skinCluster, i))
        bindPreMatrix_array.append(matrix)


    new_joints = []
    IntArray = om.MIntArray()
    for i, item in enumerate(inf_joint):
        new_joints.append(item + suffix)
        IntArray.append(i)



    dup = mc.duplicate(obj, n="{}_temp".format(obj))[0]
    mc.parent(dup,w=True)
    print obj, dup


    mc.skinCluster(new_joints, dup)
    mc.copySkinWeights(obj, dup, surfaceAssociation='closestPoint', influenceAssociation='closestJoint',
                       noMirror=1)

    mc.delete(skinCluster)


    newSkinNode = mc.skinCluster(new_joints, obj)[0]

    mc.copySkinWeights(dup, obj, surfaceAssociation='closestPoint', influenceAssociation='closestJoint',
                       noMirror=1)

    mc.delete(dup)

    return

    # for i in range(len(vtx_array)):
    #     if i%1000 == 0:
    #         print i
    #     component = om.MFnSingleIndexedComponent().create(om.MFn.kMeshVertComponent)
    #     om.MFnSingleIndexedComponent(component).addElement(i)
    #     newSkinNodeFn.setWeights(getDagPath(obj), component, IntArray, weights_data[i], 1)

    # for i, item in enumerate(bindPreMatrix_array):
    #
    #     mc.setAttr("{}.bindPreMatrix[{}]".format(newSkinNode, i), item, type="matrix")
    #



def list_inf_joint(args):
    all_joint = []
    for i in args:
        shape = mc.listRelatives(i, s=True)[0]
        skinCluster = getDeformNode(shape, "skinCluster")
        inf_joint = mc.skinCluster(skinCluster, q=True, inf=True)

        for j in inf_joint:
            if not j in all_joint:
                all_joint.append(j)
    mc.select(all_joint)
    return all_joint




def delete_redundant():
    selNode = mc.ls(sl=True)
    allNode =  findChild("armor_up_armor_sec_grp")

    inf_joint = list_inf_joint(selNode)
    # for j in inf_joint:
    #     parents = findParent(j) + [j]
    #     for i in parents:
    #         try:
    #             allNode.remove(i)
    #         except:
    #             pass
    #             print "not exitex"


    result = []
    for i in inf_joint:
        if i in allNode:
            print i
            result.append(i)


    mc.select(result)










if __name__ == '__main__':
    pass
    # delete_redundant()
    # for i in mc.ls(sl=True):
    #     rebuildSkeletalChain(i, "_CLOTH")
    #     replaceSkinJoint(i, "_CLOTH")

    # list_inf_joint(mc.ls(sl=True))


    # head_ctrl = "dongzhuo_test_newCtrl:head_M_ctrl"
    # facial_CtrlGrp = "dongzhuo_armor_test_b_rig_rigging_facial:facial_CtrlGrp"
    # multMatrix = mc.createNode("multMatrix", n="multMatrix")
    # decomposeMatrix = mc.createNode("decomposeMatrix", n="decomposeMatrix")
    # mc.connectAttr("{}.parentInverseMatrix[0]".format(head_ctrl), "{}.matrixIn[0]".format(multMatrix))
    # mc.connectAttr("{}.worldMatrix[0]".format(head_ctrl), "{}.matrixIn[1]".format(multMatrix))
    # mc.connectAttr("{}.matrixSum".format(multMatrix), "{}.inputMatrix".format(decomposeMatrix))
    # mc.connectAttr("{}.outputTranslate".format(decomposeMatrix), "{}.translate".format(facial_CtrlGrp))
    # mc.connectAttr("{}.outputRotate".format(decomposeMatrix), "{}.rotate".format(facial_CtrlGrp))



import maya.cmds as mc

def connect_joint(prefix, ctrlNameSpace, connect=True):
    allJoint = mc.ls("*:{}*".format(prefix))
    for i in allJoint:
        absJoint = i.split(":")[-1].split(prefix)[-1]
        controlName = ctrlNameSpace + ":" + absJoint
        for attr in ["tx", "ty", "tz", "rx", "ry", "rz"]:

            try:
                if connect:
                    mc.connectAttr("{}.{}".format(controlName, attr), "{}.{}".format(i, attr))
                else:
                    mc.disconnectAttr("{}.{}".format(controlName, attr), "{}.{}".format(i, attr))
                print "Success: {}".format(i)
            except:
                print "Error: {}".format(i)

def connect_facial():
    head_ctrl = "dongzhuo_test_newCtrl:head_M_ctrl"
    facial_CtrlGrp = "dongzhuo_armor_test_b_rig_rigging_facial:facial_CtrlGrp"
    facial_model_grp = "dongzhuo_armor_test_b_rig_rigging_facial:facial_model_grp"
    bodyNameShape =  "dongzhuo_test_newBody"
    node = mc.parentConstraint(head_ctrl, facial_CtrlGrp, n="head_M_ctrl_connectNode")[0]
    mc.setAttr("{}.target[0].targetOffsetTranslateY".format(node), -16.217)
    mc.setAttr("{}.target[0].targetOffsetTranslateZ".format(node), -0.010)

    allTransform = mc.listRelatives("dongzhuo_armor_test_b_rig_rigging_facial:facial_model_grp", allDescendents=True,
                                    type="transform")
    allTransform_filter = []

    for i in allTransform:
        r = mc.listRelatives(i, s=True)
        if not r == None:
            allTransform_filter.append(i)

    mc.select(allTransform_filter)

    for i in allTransform_filter:
        bsNode = mc.ls(mc.findDeformers(i), type="blendShape")[0]  # bs jiedian
        targetMesh =  mc.blendShape(bsNode, q=True, t=True)[0]
        target = bodyNameShape + ":" + i.split(":facial_")[-1]
        mc.blendShape("dongzhuo_armor_test_b_rig_rigging_facial:facial_head_geo", "dongzhuo_test_newBody:body_old_geo", w=(0, 1),tc=0, frontOfChain=True, n="temp_connect")
        try:
            mc.blendShape(targetMesh, target, w=(0,1),tc=0, frontOfChain=True ,n="temp_connect")
        except:
            print "{} ------ is ont exists!".format(target)

def disconnect_facial():
    head_ctrl = "dongzhuo_test_newCtrl:head_M_ctrl"
    facial_CtrlGrp = "dongzhuo_armor_test_b_rig_rigging_facial:facial_CtrlGrp"
    mc.delete("head_M_ctrl_connectNode")
    mc.setAttr("{}.t".format(facial_CtrlGrp), 0,0,0)
    mc.setAttr("{}.r".format(facial_CtrlGrp), 0,0,0)
    mc.delete("temp_connect*")

mc.window(title="Connect")
mc.rowColumnLayout(numberOfRows=2, rowHeight=[(1, 60), (2, 60)])
c_body = mc.button(u"连接 body", command='connect_joint("BODY_", "dongzhuo_test_newCtrl", connect=1)')
d_body = mc.button(u"断开 body", command='connect_joint("BODY_", "dongzhuo_test_newCtrl", connect=0)')
c_cloth = mc.button(u"连接 cloth", command='connect_joint("CLOTH_", "dongzhuo_test_newCtrl", connect=1)')
d_cloth = mc.button(u"断开 cloth", command='connect_joint("CLOTH_", "dongzhuo_test_newCtrl", connect=0)')
c_armor = mc.button(u"连接 armor", command='connect_joint("ARMOR_", "dongzhuo_test_newCtrl", connect=1)')
d_armor = mc.button(u"断开 armor", command='connect_joint("ARMOR_", "dongzhuo_test_newCtrl", connect=0)')
c_facial = mc.button(u"连接 facial", command='connect_facial()')
d_facial = mc.button(u"断开 facial", command='disconnect_facial()')
mc.showWindow()









for i, item in enumerate(mc.ls(sl=True)):
    mc.setAttr("{}.tx".format(item), -i * 25)

for i in range(60):
    mc.file(
        r"Z:\projects\sgl\asset\chr\horse_caocao\rig\publish\horse_caocao.rig.rigging_lite_muggle_B\horse_caocao.mb",
        ignoreVersion=1, namespace="private_soldier_a_{}".format(i), r=1, gl=1,
        mergeNamespacesOnClash=False, options="v=0;")


for i in range(60):
    mc.file(
        r"Z:\projects\sgl\asset\chr\private_soldier_a\rig\publish\private_soldier_a.rig.rigging_lite_muggle_B\private_soldier_a.mb",
        ignoreVersion=1, namespace="horse_caocao_{}".format(i), r=1, gl=1,
        mergeNamespacesOnClash=False, options="v=0;")



"""

W:\shome\PLETEMP\TD_PLE\SGL_d90_test\hs\qibing_anim_muggle.mb




"""


