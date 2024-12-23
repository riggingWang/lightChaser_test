# -*- coding: utf-8 -*-
#*************************************************************************
#***    External imports.
#*************************************************************************
import os
import sys
import fnmatch
import maya.cmds as mc

#*************************************************************************
#***    Internal imports.

from assetsystem_sgl.utils.maya import utils
#*************************************************************************
# Get the directory of the current script
from assetsystem_sgl.utils.maya import transform

import xpRigFunctions
reload(xpRigFunctions)
import xpMathFunctions
reload(xpMathFunctions)

class caocao_armor_setup_module(object):
    """docstring for shoulder armor"""
    def __init__(self, prefix, aim_vector, up_vector, size):
        super(caocao_armor_setup_module, self).__init__()
        self.prefix = prefix
        self.global_size = size
        self.up_vector = up_vector
        self.ControlBuilder = xpRigFunctions.ControlBuilder()
        self.JointBuilder = xpRigFunctions.JointBuilder()

        self.main_rig = "rig"

        self.main_controls_grp = "anim_controls_grp"
        self.main_skeletons_grp = "anim_skeletons_grp"
        self.main_modules_grp = "anim_modules_grp"
        self.main_guides_grp = "anim_guides_grp"
        self.world_space_grp = "world_space_grp"

        self.global_ctrl = "global_ctrl"
        self.root_ctrl = "root_ctrl"
        self.body_geo = 'body_geo'

        # guide_group_name
        self.guideGrpSuffix = "*_guideGrp" # 获取每根曲线上的分组
        self.guideInfoGrp = "*_batchGuide_grp" # 获模块总组上的信息
        self._grp_Suffix = "*_grp"
        self.localGrpSuffix = "*_loc_grp"
        self.guideGrp = "*_batchGuide_grp"
        self.guideLocGrp = "*_guideGrp_loc_grp"
        self.guideCrvGrp = "*_guideGrp_curve_grp"
        self.prefixAttr = 'prefix'
        self.sideAttr = 'side'

        # armor_rig module
        self.armorRigMainGrp = 'armor_main_grp'
        self.armorRigSecGrp = '_armor_sec_grp'
        self.armorRigTriIKCrvGrp = '_armor_tri_IkCrv_grp'
        self.armorRigTriDisCrvGrp = '_armor_tri_DisCrv_grp'
        self.bindJntListAttr = 'bindJnt'

        # body_up module
        self.armor_body_up_root_grp = 'armor_up_setup_grp'
        self.armor_body_up_loc_grp = 'armour_guide_grp'
        self.armor_body_up_root_loc = mc.ls('armor_up_root_*_loc')
        self.armor_body_up_root_loc = mc.ls('armor_up_root_*_loc')
        self.body_up_bind_list = [[u'spine_M_spine_5_bind', u'spine_M_spine_4_bind', u'shoulder_L_shoulder_1_bind', u'spine_M_spine_1_bind', u'hip_L_hip_1_bind', u'shoulder_R_shoulder_1_bind', u'neck_M_neck_1_bind', u'hip_L_hip_1_front_bind', u'hip_R_hip_1_front_bind', u'hip_R_hip_1_bind', u'leg_L_leg_1_front_bind', u'neck_M_neck_2_bind', u'arm_R_arm_1_bind', u'leg_R_leg_1_front_bind', u'head_M_head_1_bind', u'arm_L_arm_1_bind', u'spine_M_spine_2_bind', u'spine_M_spine_3_bind']]

        # body_dn module
        self.armor_body_dn_root_grp = 'armor_dn_setup_grp'
        self.armor_body_dn_loc_grp = 'armour_guide_grp'
        self.armor_body_dn_root_loc = mc.ls('armor_dn_root_*_loc')
        self.armor_body_dn_root_loc = mc.ls('armor_dn_root_*_loc')
        self.body_up_bind_list = [[u'spine_M_spine_5_bind', u'spine_M_spine_4_bind', u'shoulder_L_shoulder_1_bind', u'spine_M_spine_1_bind', u'hip_L_hip_1_bind', u'shoulder_R_shoulder_1_bind', u'neck_M_neck_1_bind', u'hip_L_hip_1_front_bind', u'hip_R_hip_1_front_bind', u'hip_R_hip_1_bind', u'leg_L_leg_1_front_bind', u'neck_M_neck_2_bind', u'arm_R_arm_1_bind', u'leg_R_leg_1_front_bind', u'head_M_head_1_bind', u'arm_L_arm_1_bind', u'spine_M_spine_2_bind', u'spine_M_spine_3_bind']]

        # shoulder module
        self.armor_shoulder_L_root_grp = 'shoulder_L_shoulder_1_bind'
        self.armor_shoulder_R_root_grp = 'shoulder_R_shoulder_1_bind'
        self.armor_shoulder_L_root_loc = mc.ls('armor_shoulder_L_root_*_loc')
        self.armor_shoulder_R_root_loc = mc.ls('armor_shoulder_R_root_*_loc')

    # todo ------ 用disCurve驱动IKCrv的问题，；也就是bs曲线的问题需要讨论一下 ------
    def create_armor_body_up_setup(self, guideMainGrp, horizontalCtrl=True): # 线性IK链条
        # read guide and create group
        bind_joint_list = []
        armor_ctrl_list = []

        guide_grp_keys = mc.listRelatives(guideMainGrp, ad=True, type='transform')
        guide_grp_keys.append(guideMainGrp)
        guideSecGrps = fnmatch.filter(guide_grp_keys, self.guideGrpSuffix)
        try:
            guideInfoGrps = fnmatch.filter(guide_grp_keys, self.guideInfoGrp)[0]
            prefix = mc.getAttr(
                str(guideInfoGrps) + ".prefix")  # xpRigFunctions.getGrpAttrInfo(guideMainGrp, self.prefixAttr, defaultAttrName=guideSecGrps[0].split('_')[0])
        except:
            mc.warning(' ****** - guide error ! - ******  please select guide group')
            return
        aimDirection = mc.getAttr(str(guideInfoGrps) + ".aim")
        aimVec = (1, 0, 0)
        upDirection = mc.getAttr(str(guideInfoGrps) + ".up")
        upVec = (0, 1, 0)
        ForwardAxis = 0
        upAxis = 0

        if aimDirection == 'X':
            aimVec = (1, 0, 0)
            ForwardAxis = 0
            if upDirection == 'y':
                upVec = (0, 1, 0)
                upAxis = 0
            elif upDirection == 'Z':
                upVec = (0, 0, 1)
                upAxis = 3
        elif aimDirection == 'Y':
            aimVec = (0, 1, 0)
            ForwardAxis = 2
            if upDirection == 'X':
                upVec = (1, 0, 0)
                upAxis = 6
            elif upDirection == 'Z':
                upVec = (0, 0, 1)
                upAxis = 3
        elif aimDirection == 'Z':
            aimVec = (0, 0, 1)
            ForwardAxis = 4
            if upDirection == 'X':
                upVec = (1, 0, 0)
                upAxis = 6
            elif upDirection == 'Y':
                upVec = (0, 1, 0)
                upAxis = 0


        if not xpRigFunctions.has_joint_and_nurbs_curve(guideMainGrp):
            mc.warning(' ****** - guide error ! - ******  your group miss either joint or nurbsCurve')
            return

        armorRigSecGrp = xpRigFunctions.createGrp(prefix + self.armorRigSecGrp)
        ikh_loc_grp = xpRigFunctions.createGrp(prefix + '_ikh_loc_grp', parent=armorRigSecGrp)
        generateInfo = xpRigFunctions.groupIsGenerated(armorRigSecGrp, parent = 'root_ctrl')
        if generateInfo:
            return
        splineIK_crv_grp = xpRigFunctions.createGrp(prefix + self.armorRigTriIKCrvGrp, parent=armorRigSecGrp)
        mc.addAttr(splineIK_crv_grp, ln='stretch', at="long", min=0, max=1, dv=1)
        mc.setAttr(splineIK_crv_grp + '.stretch', e=1, k=1)
        splineIK_handle_grp = xpRigFunctions.createGrp(prefix + '_ikHandleGrp', parent=armorRigSecGrp)
        splineIK_ctrl_grp = xpRigFunctions.createGrp(prefix + '_ikCtrlGrp', parent=armorRigSecGrp)
        mc.setAttr(splineIK_crv_grp + ".inheritsTransform", 0)
        disCrv_grp = xpRigFunctions.createGrp(prefix + self.armorRigTriDisCrvGrp, parent=armorRigSecGrp)
        mc.setAttr(disCrv_grp + ".inheritsTransform", 0)
        #mc.addAttr(disCrv_grp, ln='stretchRatio', at="double", min=0, dv=1)


        # create curves and joints
        for eachGrp in guideSecGrps: # prefix_0_loc_grp
            guideLocs = mc.listRelatives(eachGrp, ad=True, type='joint')
            guideCrvShape = mc.listRelatives(eachGrp, ad=True, type='nurbsCurve', f=True)[0]
            guideCrv = mc.listRelatives(guideCrvShape, p=True, f=False)[0]
            # splineIkCrv = mc.duplicate(guideCrv, n=guideCrv + '_splineIK_crv')[0]
            #mc.rebuildCurve(splineIkCrv,
            #                  degree=3,  # Set the curve to cubic (degree = 3)
            #                  spans=len(guideLocs),  # Adjust the number of spans (change as needed)
            #                  keepRange=1)  # Normalize the parameter range (0 to 1)
            splineIkCrv = xpRigFunctions.create_nurbsCurve_from_locators(guideLocs, guideCrv + '_splineIK_crv')
            transform.parent(splineIkCrv, splineIK_crv_grp)

            # 创建 ik spline joint chain
            jnt_list = self.JointBuilder.joint_to_joint_repalce(guideLocs,
                                                               '_guide',
                                                               '_splineIk_jnt',
                                                               step=1)
            for each in jnt_list:
                mc.setAttr(each + '.drawStyle', 2)
            transform.parent(jnt_list[0], armorRigSecGrp)

            # 创建 ik spline handle
            start_object = 'spine_M_spine_1_bind'
            end_object = 'spine_M_spine_5_bind'
            start_locator = mc.spaceLocator(name=eachGrp.replace('_guideGrp','') + "_spline_1_loc")[0]
            end_locator = mc.spaceLocator(name=eachGrp.replace('_guideGrp','') + "_spline_5_loc")[0]
            #mc.addAttr(armorRigSecGrp, longName='ikhLoc1', dataType="string")
            #mc.setAttr("{}.{}".format(armorRigSecGrp, 'ikhLoc1'), str(start_locator), type="string")
            #mc.addAttr(armorRigSecGrp, longName='ikhLoc2', dataType="string")
            #mc.setAttr("{}.{}".format(armorRigSecGrp, 'ikhLoc2'), str(end_locator), type="string")

            transform.parent(start_locator, ikh_loc_grp)
            transform.parent(end_locator, ikh_loc_grp)
            if start_object and end_object:
                mc.delete(mc.parentConstraint(start_object, start_locator, mo=False))
                mc.delete(mc.parentConstraint(end_object, end_locator, mo=False))
            self.ControlBuilder.make_group_multi(start_locator)
            self.ControlBuilder.make_group_multi(end_locator)

            new_ik_handle = \
            mc.ikHandle(startJoint=jnt_list[0], endEffector=jnt_list[-1], sol="ikSplineSolver", ccv=False, snc=False,
                          pcv=False, curve=splineIkCrv, name=splineIkCrv.replace('_curve','') + "_ikHandle")[0]
            transform.parent(new_ik_handle, splineIK_handle_grp)
            transform.parent(jnt_list[0], splineIK_ctrl_grp)

            mc.setAttr(str(new_ik_handle) + ".dTwistControlEnable", 1)
            mc.setAttr(str(new_ik_handle) + ".dWorldUpType", 4)
            mc.setAttr(str(new_ik_handle) + ".dForwardAxis", ForwardAxis)
            mc.setAttr(str(new_ik_handle) + ".dWorldUpAxis", upAxis)

            mc.setAttr(str(new_ik_handle) + ".dWorldUpVectorX", 0)
            mc.setAttr(str(new_ik_handle) + ".dWorldUpVectorY", 0)
            mc.setAttr(str(new_ik_handle) + ".dWorldUpVectorZ", 1)

            mc.setAttr(str(new_ik_handle) + ".dWorldUpVectorEndX", 0)
            mc.setAttr(str(new_ik_handle) + ".dWorldUpVectorEndY", 0)
            mc.setAttr(str(new_ik_handle) + ".dWorldUpVectorEndZ", 1)
            mc.connectAttr("{}.worldMatrix[0]".format(start_locator), "{}.dWorldUpMatrix".format(new_ik_handle),force=True)
            mc.connectAttr("{}.worldMatrix[0]".format(end_locator), "{}.dWorldUpMatrixEnd".format(new_ik_handle),force=True)

            # disCrv 驱动暂时不加，单独分出来加
            pos1 = mc.xform(guideLocs[0], query=True, worldSpace=True, translation=True)
            pos2 = mc.xform(guideLocs[-1], query=True, worldSpace=True, translation=True)
            disCrv = mc.curve(d=1, p=[pos1, pos2], n=guideCrv + '_disCrv')
            utils.rename_shape(disCrv)
            transform.parent(disCrv, disCrv_grp)
            mc.addAttr(disCrv_grp, ln='{}_ratio'.format(disCrv.replace('_curveGuide','')), at="double", min=0, dv=1)
            mc.setAttr(disCrv_grp + '.{}_ratio'.format(disCrv).replace('_curveGuide',''), e=1, k=1)
            # disCrv 计算拉伸和整体缩放
            disCrvInfo = xpRigFunctions.createNode(disCrv + '_curveInfo', "curveInfo")
            disCrv_info_fm = xpRigFunctions.createNode(disCrv + '_curveInfo_fm', "floatMath")
            disCrv_info_md = xpRigFunctions.createNode(disCrv + '_curveInfo_md', "multiplyDivide")
            mc.setAttr(disCrv_info_md + ".operation", 2)
            mc.setAttr(disCrv_info_fm + ".operation", 3)
            mc.connectAttr(disCrv + ".worldSpace[0]", disCrvInfo + ".inputCurve", force=True)
            mc.connectAttr(disCrvInfo + ".arcLength", disCrv_info_fm + ".floatA", force=True)
            mc.setAttr(disCrv_info_fm + ".floatB", mc.getAttr(disCrvInfo + ".arcLength"))
            mc.connectAttr(disCrv_info_fm + ".outFloat", disCrv_info_md + ".input1X", force=True)
            mc.connectAttr("global_ctrl.global_scale", disCrv_info_md + ".input2X", force=True)
            mc.connectAttr(disCrv_info_md + ".outputX", disCrv_grp + ".{}_ratio".format(disCrv.replace('_curveGuide','')), force=True)

            # ikCrv 计算拉伸和整体缩放
            ikCurve_info = xpRigFunctions.createNode(splineIkCrv + '_curveInfo', "curveInfo")
            ikCurve_info_fm = xpRigFunctions.createNode(splineIkCrv + '_curveInfo_fm', "floatMath")
            ikCurve_info_cd = xpRigFunctions.createNode(splineIkCrv + '_curveInfo_cd', "condition")
            ikCurve_info_md = xpRigFunctions.createNode(splineIkCrv + '_curveInfo_md', "multiplyDivide")

            mc.connectAttr(splineIkCrv + ".worldSpace[0]", ikCurve_info + ".inputCurve", force=True)
            mc.connectAttr(ikCurve_info + ".arcLength", ikCurve_info_fm + ".floatA", force=True)
            mc.setAttr(ikCurve_info_fm + ".floatB", mc.getAttr(ikCurve_info + ".arcLength"))
            mc.setAttr(ikCurve_info_fm + ".operation", 3)
            mc.setAttr(ikCurve_info_md + ".operation", 2)
            mc.connectAttr(ikCurve_info_fm + ".outFloat", ikCurve_info_cd + ".colorIfTrueR", force=True)
            mc.connectAttr(splineIK_crv_grp + ".stretch", ikCurve_info_cd + ".firstTerm", force=True)
            mc.connectAttr("global_ctrl.global_scale", ikCurve_info_cd + ".colorIfFalseR", force=True)
            #mc.setAttr(ikCurve_info_cd + ".colorIfFalseR", 1)
            mc.setAttr(ikCurve_info_cd + ".secondTerm", 1)

            mc.connectAttr( ikCurve_info_cd + ".outColorR", ikCurve_info_md + ".input1X", force=True)
            mc.connectAttr("global_ctrl.global_scale", ikCurve_info_md + ".input2X", force=True)
            aimDirection = xpRigFunctions.getGrpAttrInfo(eachGrp, 'aimDirection', defaultAttrName='X')
            for eachJnt in jnt_list:
                # todo ------ scaleX replace with the attribute of across axies in attr ------
                mc.connectAttr(ikCurve_info_md + ".outputX", eachJnt + ".scale" + aimDirection, force=True)

            # 创建 控制器 和 权重骨骼
            #chainSide = xpRigFunctions.getGrpAttrInfo(eachGrp, self.sideAttr, defaultAttrName='M')
            if '_L_' in eachGrp:
                chainSide = 'L'
                side_color = 6
                side_sec_color = 15
            elif '_R_' in eachGrp:
                chainSide = 'R'
                side_color = 13
                side_sec_color = 12
            elif '_M_' in eachGrp:
                chainSide = 'M'
                side_color = 17
                side_sec_color = 21
            else:
                chainSide = 'M'
                side_color = 17
                side_sec_color = 21

            for i, eachJnt in enumerate(jnt_list):
                if mc.getAttr(guideLocs[i] + '.visibility') != 0:
                    eachJnt = self.JointBuilder.locator_to_joint(eachJnt,
                                                                '_jnt',
                                                                '_bind')
                    newCtrl = self.ControlBuilder.create("box",
                                                         eachJnt.replace('_bind', '_ctrl'),
                                                         color = side_color,
                                                         r = self.global_size,
                                                         aim_vector = aimVec
                                                         )

                    if horizontalCtrl:
                        upLoc = xpRigFunctions.create_locators(newCtrl + "_hz_locator", armorRigSecGrp, guideLocs[i], 1, 0, 0)
                        mc.setAttr(upLoc + '.translateY', 100)
                        orientLoc = xpRigFunctions.create_locators(newCtrl + "_orient_locator", armorRigSecGrp, guideLocs[i], 1, 1, 0)
                        transform.catch_position(guideLocs[i], newCtrl, 1, 1, 1)
                        xpRigFunctions.changeRotateToHorizontal(upLoc, newCtrl, orientLoc, aimVector = (1,0,0), upVector = (0,1,0))
                        mc.delete(upLoc, orientLoc)
                    else:
                        transform.catch_position(guideLocs[i], newCtrl, 1, 1, 1)

                    transform.parent(newCtrl, eachJnt.replace('_bind', '_jnt'))
                    self.ControlBuilder.make_group_multi(newCtrl)
                    transform.parent(eachJnt, newCtrl)
                    bind_joint_list.append(eachJnt)
                    armor_ctrl_list.append(newCtrl)
            #xpRigFunctions.writeString(armorRigSecGrp, self.bindJntListAttr, bind_joint_list)

        if bind_joint_list:
            bindJntsSet = mc.sets(name=prefix + "_bindJnts", empty=True)
            mc.sets(bind_joint_list, add=bindJntsSet)
        if armor_ctrl_list:
            armorCtrlSet = mc.sets(name=prefix + "_armorCtrl", empty=True)
            mc.sets(armor_ctrl_list, add=armorCtrlSet)

        xpRigFunctions.groupIsGenerated(armorRigSecGrp, finished=True)
        mc.select(armorRigSecGrp ,r=1)
        return armorRigSecGrp, guideMainGrp

    def create_armor_body_up_drive(self, guideMainGrp):

        if xpRigFunctions.groupAttrAdded(guideMainGrp, parent='', attrName='armorUpDrive', finished=False):
            return

        ikCrvs = mc.listRelatives(guideMainGrp.replace('_armor_sec_grp','_armor_tri_IkCrv_grp'), c=True)
        disCrvs = mc.listRelatives(guideMainGrp.replace('_armor_sec_grp', '_armor_tri_DisCrv_grp'), c=True)
        allCrvs = ikCrvs + disCrvs
        prefixName = guideMainGrp.split('_')[0]

        start_object = 'spine_M_spine_1_bind'
        end_object = 'spine_M_spine_5_bind'

        allLocs = xpRigFunctions.get_locators_under_group(guideMainGrp)
        print allLocs
        spine_1_bind_locs = fnmatch.filter(allLocs, '*_spine_M_spine_1_bind_lo*')
        spine_5_bind_locs = fnmatch.filter(allLocs, '*_spine_M_spine_5_bind_lo*')
        for each in spine_1_bind_locs:
            mc.parentConstraint(start_object, each, mo=0)
        for each in spine_5_bind_locs:
            mc.parentConstraint(end_object, each, mo=0)
        #ikLoc1 = mc.getAttr(guideMainGrp + '.ikhLoc1')
        #ikLoc2 = mc.getAttr(guideMainGrp + '.ikhLoc2')

        # body权重 -> 曲线权重 这部分不在这里加，单独驱动模块
        bind_list = [u'spine_M_spine_3_bind', u'shoulder_L_shoulder_1_bind', u'neck_M_neck_1_bind', u'spine_M_spine_4_bind', u'shoulder_R_shoulder_1_bind', u'spine_M_spine_1_bind', u'head_M_head_1_bind', u'neck_M_neck_2_bind', u'spine_M_spine_2_bind', u'spine_M_spine_5_bind', 
        u'hip_L_hip_1_bind', u'hip_R_hip_1_bind', u'hip_R_hip_1_front_bind', u'leg_L_leg_1_front_bind', u'leg_R_leg_1_front_bind', u'hip_L_hip_1_front_bind', u'arm_R_arm_1_bind', u'arm_L_arm_1_bind', u'hip_R_hip_1_back_bind', u'leg_R_leg_1_back_bind', u'hip_L_hip_1_back_bind', u'leg_L_leg_1_back_bind', u'leg_R_leg_4_bind', u'leg_R_leg_1_bind', u'leg_R_knee_2_bind', u'leg_R_leg_3_bind', u'leg_L_knee_1_volume_bind', u'leg_L_leg_1_bind', u'leg_L_leg_3_bind', u'leg_L_knee_1_bind', u'leg_L_leg_2_bind', u'leg_R_knee_1_volume_bind', u'leg_R_leg_5_bind', u'leg_L_leg_4_bind', u'leg_L_knee_2_bind', u'leg_L_knee_3_bind', u'leg_R_knee_1_bind', u'leg_L_leg_5_bind', u'leg_R_leg_2_bind', u'leg_R_knee_3_bind']
        existing_bind_list = [obj for obj in bind_list if mc.objExists(obj)]
        for eachCrv in allCrvs:
            try:
                mc.skinCluster(existing_bind_list, eachCrv, toSelectedBones=True, maximumInfluences=2, dropoffRate=4,
                                removeUnusedInfluence=False)
                # The two surfaces have different numbers of influences (148 and 34) . Weight transfer may be problematic near the missing influences. #
                #mc.copySkinWeights(self.body_geo, eachCrv, noMirror=1, surfaceAssociation='closestPoint',
                #                   influenceAssociation='oneToOne')
            except:
                print  "copy skin Error, jump copy"

        #mc.addAttr(guideMainGrp, longName='part', dataType="string")
        #mc.setAttr("{}.{}".format(guideMainGrp, 'part'), 'ArmorUp', type="string")
        #ikHandleList = mc.listRelatives(guideMainGrp, ad=True, type='ikHandle', f=True)

        xpRigFunctions.groupAttrAdded(guideMainGrp, parent='', attrName='armorUpDrive', finished=True)
        mc.select(guideMainGrp, r=1)

    def create_armor_body_dn_setup(self, guideMainGrp, horizontalCtrl=False): # FK链带动的IK链

        # read guide and create group
        bind_joint_list = []
        armor_ctrl_list = []
        guide_grp_keys = mc.listRelatives(guideMainGrp, ad=True, type='transform')
        guide_grp_keys.append(guideMainGrp)
        guideSecGrps = fnmatch.filter(guide_grp_keys, self.guideGrpSuffix)
        try:
            guideInfoGrps = fnmatch.filter(guide_grp_keys, self.guideInfoGrp)[0]
            prefix = mc.getAttr(str(guideInfoGrps) + ".prefix") # xpRigFunctions.getGrpAttrInfo(guideMainGrp, self.prefixAttr, defaultAttrName=guideSecGrps[0].split('_')[0])
        except:
            mc.warning(' ****** - guide error ! - ******  please select guide group')
            return

        aimDirection = mc.getAttr(str(guideInfoGrps) + ".aim")
        aimVec = (1, 0, 0)
        upDirection = mc.getAttr(str(guideInfoGrps) + ".up")
        upVec = (0, 1, 0)
        ForwardAxis = 0
        upAxis = 0
        if aimDirection == 'X':
            aimVec = (1, 0, 0)
            ForwardAxis = 0
            if upDirection == 'y':
                upVec = (0, 1, 0)
                upAxis = 0
            elif upDirection == 'Z':
                upVec = (0, 0, 1)
                upAxis = 3
        elif aimDirection == 'Y':
            aimVec = (0, 1, 0)
            ForwardAxis = 2
            if upDirection == 'X':
                upVec = (1, 0, 0)
                upAxis = 6
            elif upDirection == 'Z':
                upVec = (0, 0, 1)
                upAxis = 3
        elif aimDirection == 'Z':
            aimVec = (0, 0, 1)
            ForwardAxis = 4
            if upDirection == 'X':
                upVec = (1, 0, 0)
                upAxis = 6
            elif upDirection == 'Y':
                upVec = (0, 1, 0)
                upAxis = 0
        if not xpRigFunctions.has_joint_and_nurbs_curve(guideMainGrp):
            mc.warning(' ****** - guide error ! - ******  your group miss either joint or nurbsCurve')
            return

        armorRigSecGrp = xpRigFunctions.createGrp(prefix + self.armorRigSecGrp)
        generateInfo = xpRigFunctions.groupIsGenerated(armorRigSecGrp, parent = 'root_ctrl')
        if generateInfo:
            return
        armorRigSecSetGrp = xpRigFunctions.createGrp(prefix + self.armorRigSecGrp + "_set", armorRigSecGrp)
        #splineIK_crv_grp = xpRigFunctions.createGrp(prefix + self.armorRigTriIKCrvGrp, parent=armorRigSecGrp)
        #mc.setAttr(splineIK_crv_grp + ".inheritsTransform", 0)
        #disCrv_grp = xpRigFunctions.createGrp(prefix + self.armorRigTriDisCrvGrp, parent=armorRigSecGrp)
        #mc.setAttr(disCrv_grp + ".inheritsTransform", 0)

        # create curves and joints
        for eachGrp in guideSecGrps:
            if mc.objExists(str(eachGrp) + ".side"):
                frontBackSide = mc.getAttr(str(eachGrp) + ".side")
            else:
                frontBackSide = "center"
            guideLocs = mc.listRelatives(eachGrp, ad=True, type='joint')
            guideCrvShape = mc.listRelatives(eachGrp, ad=True, type='nurbsCurve', f=True)[0]
            guideCrv = mc.listRelatives(guideCrvShape, p=True, f=False)[0]
            #guideCurve = mc.duplicate(guideCrv, n=guideCrv + '_crv')[0]
            #mc.rebuildCurve(guideCurve,
            #                  degree=3,  # Set the curve to cubic (degree = 3)
            #                  spans=len(guideLocs),  # Adjust the number of spans (change as needed)
            #                  keepRange=1)  # Normalize the parameter range (0 to 1)
            # guideCurve = xpRigFunctions.create_nurbsCurve_from_locators(guideLocs, guideCrv + '_splineIK_crv')
            # transform.parent(guideCurve, splineIK_crv_grp)
            # chainSide = xpRigFunctions.getGrpAttrInfo(eachGrp, self.sideAttr, defaultAttrName='M')
            if '_L_' in eachGrp:
                chainSide = 'L'
                side_color = 6
                side_sec_color = 15
            elif '_R_' in eachGrp:
                chainSide = 'R'
                side_color = 13
                side_sec_color = 12
            elif '_M_' in eachGrp:
                chainSide = 'M'
                side_color = 17
                side_sec_color = 21
            else:
                chainSide = 'M'
                side_color = 17
                side_sec_color = 21

            # 创建 FK IK ctrl chain
            FK_ctrl_list = []
            IK_ctrl_list = []
            for i, eachLoc in enumerate(guideLocs):
                newFkCtrlName = eachLoc.replace('_guide', '_Fk_ctrl')
                newFkCtrl = self.ControlBuilder.create("circle",
                                                     newFkCtrlName,
                                                     color=side_color,
                                                     r=self.global_size * 1.25,
                                                     aim_vector=[1, 0, 0]
                                                     )

                if horizontalCtrl:
                    upLoc = xpRigFunctions.create_locators(newFkCtrl + "_hz_locator", armorRigSecGrp, eachLoc, 1, 0,
                                                           0)
                    mc.setAttr(upLoc + '.translateY', -100)
                    orientLoc = xpRigFunctions.create_locators(newFkCtrl + "_orient_locator", armorRigSecGrp,
                                                               eachLoc, 1, 1, 0)
                    transform.catch_position(eachLoc, newFkCtrl, 1, 1, 1)
                    xpRigFunctions.changeRotateToHorizontal(upLoc, newFkCtrl, orientLoc, aimVector=(1, 0, 0),
                                                            upVector=(0, 1, 0))
                    mc.delete(upLoc, orientLoc)
                else:
                    transform.catch_position(eachLoc, newFkCtrl, 1, 1, 1)

                FK_ctrl_list.append(newFkCtrl)
                armor_ctrl_list.append(newFkCtrl)
                if i == 0:
                    transform.parent(newFkCtrl, armorRigSecGrp)
                else:
                    transform.parent(newFkCtrl, FK_ctrl_list[i-1])

                newIkCtrlName = eachLoc.replace('_guide', '_Ik_ctrl')
                newIkCtrl = self.ControlBuilder.create("box",
                                                     newIkCtrlName,
                                                     color=side_sec_color,
                                                     r=self.global_size * 0.75
                                                     )
                if horizontalCtrl:
                    upLoc = xpRigFunctions.create_locators(newIkCtrl + "_hz_locator", armorRigSecGrp, eachLoc, 1, 0,
                                                           0)
                    mc.setAttr(upLoc + '.translateY', -100)
                    orientLoc = xpRigFunctions.create_locators(newIkCtrl + "_orient_locator", armorRigSecGrp,
                                                               eachLoc, 1, 1, 0)
                    transform.catch_position(eachLoc, newIkCtrl, 1, 1, 1)
                    xpRigFunctions.changeRotateToHorizontal(upLoc, newIkCtrl, orientLoc, aimVector=(1, 0, 0),
                                                            upVector=(0, -1, 0))
                    mc.delete(upLoc, orientLoc)
                else:
                    transform.catch_position(eachLoc, newIkCtrl, 1, 1, 1)

                IK_ctrl_list.append(newIkCtrl)
                armor_ctrl_list.append(newIkCtrl)
                transform.parent(newIkCtrl, newFkCtrl)
                eachJnt = self.JointBuilder.locator_to_joint(eachLoc, '_guide', '_bind'.format(str(i)))
                transform.parent(eachJnt, newIkCtrl)
                bind_joint_list.append(eachJnt)
                self.ControlBuilder.make_group_multi(newFkCtrl)
                self.ControlBuilder.make_group_multi(newIkCtrl)

            # aim constraint
            armorRigSecSetOfs = xpRigFunctions.createGrp(newFkCtrl + '_aim_ofs', armorRigSecSetGrp)
            mc.delete(mc.parentConstraint(newFkCtrl, armorRigSecSetOfs, mo=False))
            armorRigSecSetCon = xpRigFunctions.createGrp(newFkCtrl + '_aim_con', armorRigSecSetOfs)
            mc.delete(mc.parentConstraint(newFkCtrl, armorRigSecSetCon, mo=False))
            mc.addAttr(armorRigSecSetCon, longName='side', dataType="string")
            mc.setAttr(armorRigSecSetCon + '.side', frontBackSide, type="string")
            armorRigSecSetAimObj = xpRigFunctions.createGrp(newFkCtrl + '_aim_grp', armorRigSecSetCon)
            mc.delete(mc.parentConstraint(newFkCtrl, armorRigSecSetAimObj, mo=False))
            mc.setAttr(armorRigSecSetAimObj + ".translateX", 10) # todo 这里需要从祖上读取轴向和方向
            mc.aimConstraint(armorRigSecSetAimObj, FK_ctrl_list[0]+'_con', weight=1, upVector=(1, 0, 0), mo=1,
                             worldUpObject=armorRigSecSetAimObj, worldUpType="object", aimVector=(0, -1, 0))
            # body权重 -> 曲线权重
            try:
                pass
            except:
                print  "copy Error, jump copy"

        if bind_joint_list:
            bindJntsSet = mc.sets(name=prefix + "_bindJnts", empty=True)
            mc.sets(bind_joint_list, add=bindJntsSet)
        if armor_ctrl_list:
            armorCtrlSet = mc.sets(name=prefix + "_armorCtrl", empty=True)
            mc.sets(armor_ctrl_list, add=armorCtrlSet)
        xpRigFunctions.groupIsGenerated(armorRigSecGrp, finished=True)
        mc.select(armorRigSecGrp, r=1)

    def create_armor_body_dn_drive(self, guideMainGrp):
        if xpRigFunctions.groupAttrAdded(guideMainGrp, parent='', attrName='armorDnDrive', finished=False):
            return

        back_cons_jnt_list = ['leg_L_leg_1_back_bind', 'leg_R_leg_1_back_bind']
        front_cons_jnt_list = ['leg_R_leg_1_front_bind', 'leg_L_leg_1_front_bind']
        guide_grp_keys = mc.listRelatives(guideMainGrp, ad=True, type='transform')
        guide_grp_keys.append(guideMainGrp)
        guideInfoGrps = fnmatch.filter(guide_grp_keys, '*_sec_grp_set')[0]
        ofs_side_grps = mc.listRelatives(guideInfoGrps, c=True, type='transform')
        for eachGrp in ofs_side_grps:
            conGrp = eachGrp.replace('_ofs', '_con')
            frontBackSide = mc.getAttr(str(conGrp) + '.side')
            if frontBackSide == 'front':
                mc.parentConstraint(front_cons_jnt_list[0], front_cons_jnt_list[1], conGrp, mo=True)

            elif frontBackSide == 'back':
                mc.parentConstraint(back_cons_jnt_list[0], back_cons_jnt_list[1], conGrp, mo=True)

            else:
                pass
                #mc.parentConstraint(front_cons_jnt_list[0], front_cons_jnt_list[1], back_cons_jnt_list[0], back_cons_jnt_list[1], eachGrp, mo=True)


        xpRigFunctions.groupAttrAdded(guideMainGrp, parent='', attrName='armorDnDrive', finished=True)

    def create_armor_body_dn_2_setUp(self, guideMainGrp, horizontalCtrl=False):
        armorRigSecGrp, guideMainGrp = self.create_armor_body_up_setup(guideMainGrp, horizontalCtrl)
        allDecs = mc.listRelatives(armorRigSecGrp, ad=True, type='transform')
        allDecs.append(armorRigSecGrp)

        bind_joint_list = []
        armor_ctrl_list = []
        guide_grp_keys = mc.listRelatives(guideMainGrp, ad=True, type='transform')
        guide_grp_keys.append(guideMainGrp)
        guideSecGrps = fnmatch.filter(guide_grp_keys, self.guideGrpSuffix)
        try:
            guideInfoGrps = fnmatch.filter(guide_grp_keys, self.guideInfoGrp)[0]
            prefix = mc.getAttr(str(guideInfoGrps) + ".prefix") # xpRigFunctions.getGrpAttrInfo(guideMainGrp, self.prefixAttr, defaultAttrName=guideSecGrps[0].split('_')[0])
        except:
            mc.warning(' ****** - guide error ! - ******  please select guide group')
            return

        fkik_ctrl_grp = xpRigFunctions.createGrp(prefix + '_fkik_ctrl_grp', parent=armorRigSecGrp)

        # 1.获取ikSpline骨骼链
        # 2.删除所有*_ctrl组，然后把ofs组层级拼起来，用ikSpline骨骼约束
        ctrlGrps = fnmatch.filter(allDecs, '*_ctrl')
        ctrlDrvGrps = fnmatch.filter(allDecs, '*_ctrl_drv')
        ikCtrlGrp = fnmatch.filter(allDecs, '*_ikCtrlGrp')[0]
        mc.delete(ctrlGrps)
        mc.delete(ctrlDrvGrps)
        IK_ofs_grps = mc.listRelatives(ikCtrlGrp, c=True, type='transform')
        IK_ofs_grps.sort()
        for each in IK_ofs_grps:
            eachIKGrps = mc.listRelatives(each, ad=True, type='transform')
            offsetGrps = fnmatch.filter(eachIKGrps, '*_ctrl_ofs')
            offsetGrps.sort()
            for i, eachOfs in enumerate(offsetGrps):
                if i == 0:
                    transform.parent(offsetGrps[i], ikCtrlGrp)
                elif i > 0:
                    transform.parent(offsetGrps[i], offsetGrps[i-1].replace('_ofs', '_con'))
                mc.parentConstraint(eachOfs.replace('_ctrl_ofs','_jnt'), eachOfs.replace('_ofs','_con'),mo=0)

        locator1s = fnmatch.filter(allDecs, '*_spline_1_*')
        locator5s = fnmatch.filter(allDecs, '*_spline_5_*')
        for each in locator1s:
            mc.rename(each, each.replace('_spline_1_', '_startPoint_'))
        for each in locator5s:
            mc.rename(each, each.replace('_spline_5_', '_endPoint_'))

        #3.创建FKIK链条，和之前的body_dn一样，再把con组的旋转给到fkIK链条上的fk组
        aimDirection = mc.getAttr(str(guideInfoGrps) + ".aim")
        aimVec = (1, 0, 0)
        upDirection = mc.getAttr(str(guideInfoGrps) + ".up")
        upVec = (0, 1, 0)
        ForwardAxis = 0
        upAxis = 0
        if aimDirection == 'X':
            aimVec = (1, 0, 0)
            ForwardAxis = 0
            if upDirection == 'y':
                upVec = (0, 1, 0)
                upAxis = 0
            elif upDirection == 'Z':
                upVec = (0, 0, 1)
                upAxis = 3
        elif aimDirection == 'Y':
            aimVec = (0, 1, 0)
            ForwardAxis = 2
            if upDirection == 'X':
                upVec = (1, 0, 0)
                upAxis = 6
            elif upDirection == 'Z':
                upVec = (0, 0, 1)
                upAxis = 3
        elif aimDirection == 'Z':
            aimVec = (0, 0, 1)
            ForwardAxis = 4
            if upDirection == 'X':
                upVec = (1, 0, 0)
                upAxis = 6
            elif upDirection == 'Y':
                upVec = (0, 1, 0)
                upAxis = 0
        for eachGrp in guideSecGrps:
            if mc.objExists(str(eachGrp) + ".side"):
                frontBackSide = mc.getAttr(str(eachGrp) + ".side")
            else:
                frontBackSide = "center"
            guideLocs = mc.listRelatives(eachGrp, ad=True, type='joint')
            guideCrvShape = mc.listRelatives(eachGrp, ad=True, type='nurbsCurve', f=True)[0]
            guideCrv = mc.listRelatives(guideCrvShape, p=True, f=False)[0]
            # guideCurve = mc.duplicate(guideCrv, n=guideCrv + '_crv')[0]
            # mc.rebuildCurve(guideCurve,
            #                  degree=3,  # Set the curve to cubic (degree = 3)
            #                  spans=len(guideLocs),  # Adjust the number of spans (change as needed)
            #                  keepRange=1)  # Normalize the parameter range (0 to 1)
            # guideCurve = xpRigFunctions.create_nurbsCurve_from_locators(guideLocs, guideCrv + '_splineIK_crv')
            # transform.parent(guideCurve, splineIK_crv_grp)
            # chainSide = xpRigFunctions.getGrpAttrInfo(eachGrp, self.sideAttr, defaultAttrName='M')
            if '_L_' in eachGrp:
                chainSide = 'L'
                side_color = 6
                side_sec_color = 15
            elif '_R_' in eachGrp:
                chainSide = 'R'
                side_color = 13
                side_sec_color = 12
            elif '_M_' in eachGrp:
                chainSide = 'M'
                side_color = 17
                side_sec_color = 21
            else:
                chainSide = 'M'
                side_color = 17
                side_sec_color = 21

            # 创建 FK IK ctrl chain
            FK_ctrl_list = []
            IK_ctrl_list = []
            for i, eachLoc in enumerate(guideLocs):
                newFkCtrlName = eachLoc.replace('_guide', '_Fk_ctrl')
                newFkCtrl = self.ControlBuilder.create("circle",
                                                       newFkCtrlName,
                                                       color=side_color,
                                                       r=self.global_size * 1.25,
                                                       aim_vector=[1, 0, 0]
                                                       )
                transform.catch_position(eachLoc, newFkCtrl, 1, 1, 1)
                FK_ctrl_list.append(newFkCtrl)
                armor_ctrl_list.append(newFkCtrl)
                if i == 0:
                    transform.parent(newFkCtrl, fkik_ctrl_grp)
                else:
                    transform.parent(newFkCtrl, FK_ctrl_list[i - 1])

                newIkCtrlName = eachLoc.replace('_guide', '_Ik_ctrl')
                newIkCtrl = self.ControlBuilder.create("box",
                                                       newIkCtrlName,
                                                       color=side_sec_color,
                                                       r=self.global_size * 0.75
                                                       )
                IK_ctrl_list.append(newIkCtrl)
                armor_ctrl_list.append(newIkCtrl)
                transform.catch_position(eachLoc, newIkCtrl, 1, 1, 1)
                transform.parent(newIkCtrl, newFkCtrl)
                eachJnt = self.JointBuilder.locator_to_joint(eachLoc, '_guide', '_bind'.format(str(i)))
                transform.parent(eachJnt, newIkCtrl)
                bind_joint_list.append(eachJnt)
                self.ControlBuilder.make_group_multi(newFkCtrl)
                self.ControlBuilder.make_group_multi(newIkCtrl)

                mc.connectAttr(newFkCtrl.replace('_Fk_ctrl', '_splineIk_ctrl_con') + '.t', newFkCtrl + '_con.t')
                mc.connectAttr(newFkCtrl.replace('_Fk_ctrl', '_splineIk_ctrl_con') + '.r', newFkCtrl + '_con.r')




            # body权重 -> 曲线权重
            try:
                pass
            except:
                print  "copy Error, jump copy"

        if bind_joint_list:
            bindJntsSet = mc.sets(name=prefix + "_bindJnts", empty=True)
            mc.sets(bind_joint_list, add=bindJntsSet)
        if armor_ctrl_list:
            armorCtrlSet = mc.sets(name=prefix + "_armorCtrl", empty=True)
            mc.sets(armor_ctrl_list, add=armorCtrlSet)
        mc.select(armorRigSecGrp, r=1)

    def create_armor_body_dn_2_drive(self, guideMainGrp):
        pass
    # TODO:  在 anim_modules_grp 下创建一个组，内有一个info组，两个字段，左边和右边所有bind_jnt的名字
    def create_armor_shoulder_setup(self, guideMainGrp): # 双向FK控制器链条套骨骼

        # create joint
        root_ctrl_list = []
        bind_joint_list = []

        # read guide and create group
        bind_joint_list = []
        armor_ctrl_list = []

        guide_grp_keys = mc.listRelatives(guideMainGrp, ad=True, type='transform')
        guide_grp_keys.append(guideMainGrp)
        guideSecGrps = fnmatch.filter(guide_grp_keys, self._grp_Suffix)
        try:
            guideInfoGrps = fnmatch.filter(guide_grp_keys, self._grp_Suffix)[0]
            prefix = xpRigFunctions.getGrpAttrInfo(guideInfoGrps, 'prefix')
        except:
            mc.warning(' ****** - guide error ! - ******  please select guide group')
            return

        localSecGrps = fnmatch.filter(guide_grp_keys, self.guideGrpSuffix)
        #armorRigMainGrp = xpRigFunctions.createGrp(self.armorRigMainGrp)
        armorRigSecGrp = xpRigFunctions.createGrp(prefix + self.armorRigSecGrp)
        generateInfo = xpRigFunctions.groupIsGenerated(armorRigSecGrp)
        if generateInfo:
            return

        """
        if side=='L':
            armor_shoulder_side_root_loc = self.armor_shoulder_L_root_loc
            armor_shoulder_root_grp = self.armor_shoulder_L_root_grp
            side_color = 6
        elif side=='R':
            armor_shoulder_side_root_loc = self.armor_shoulder_R_root_loc
            armor_shoulder_root_grp = self.armor_shoulder_R_root_grp
            side_color = 13
        """

        # create root ctrl
        # create curves and joints
        for lrGrp in localSecGrps:
            rootJoints = mc.listRelatives(lrGrp, c=True, type='joint')
            # for eachGuideRoot in rootJoints: # prefix_0_loc_grp
            # guideLocs = mc.listRelatives(eachGuideRoot, ad=True, type='joint')

            if '_L_' in lrGrp:
                chainSide = 'L' # xpRigFunctions.getGrpAttrInfo(eachGrp, self.sideAttr, defaultAttrName='M')
            elif '_R_' in lrGrp:
                chainSide = 'R'
            else:
                chainSide = 'M'

            if 'L' == chainSide:
                side_color = 6
                side_sec_color = 15
            elif 'R' == chainSide:
                side_color = 13
                side_sec_color = 12
            elif 'M' == chainSide:
                side_color = 17
                side_sec_color = 21
            else:
                chainSide = 'M'
                side_color = 17
                side_sec_color = 21

            for eachRootLoc in rootJoints:
                if not xpRigFunctions.has_double_joint_chain(eachRootLoc):
                    mc.warning(' ****** - guide error ! - ******  need double single joint chains')
                    return
                eachRootJnt = self.JointBuilder.locator_to_joint(eachRootLoc, '_guide', '_bind')
                newRootCtrl = self.ControlBuilder.create("box",
                                                     eachRootJnt.replace('_bind', '_ctrl'),
                                                     color=side_color,
                                                     r=self.global_size
                                                     )
                transform.catch_position(eachRootJnt, newRootCtrl, 1, 1, 1)
                transform.parent(eachRootJnt, newRootCtrl)
                transform.parent(newRootCtrl, armorRigSecGrp)
                self.ControlBuilder.make_group_multi(newRootCtrl)
                bind_joint_list.append(eachRootJnt)
                armor_ctrl_list.append(newRootCtrl)

                # root下面的loc,因该是最多a，b两条fk链条，需要重新命名
                children = mc.listRelatives(eachRootLoc, children=True, type='transform')
                FK_loc_chain_A = []
                FK_loc_chain_B = []
                if children:
                    FK_loc_chain_A.append(children[0])
                    FK_loc_chain_A_childern = mc.listRelatives(children[0], allDescendents=True, type='transform')
                    if FK_loc_chain_A_childern:
                        FK_loc_chain_A.extend(FK_loc_chain_A_childern)
                    for eachLoc in FK_loc_chain_A:
                        loopIndex = FK_loc_chain_A.index(eachLoc)
                        newLoc = mc.rename(eachLoc, '{}_A_{}_loc'.format(eachRootLoc.replace('_loc',''), loopIndex))
                        eachJnt = self.JointBuilder.locator_to_joint(newLoc, '_loc', '_bind')
                        newCtrl = self.ControlBuilder.create("box",
                                                             eachJnt.replace('_bind', '_ctrl'),
                                                             color=side_sec_color,
                                                             r=self.global_size
                                                             )
                        transform.catch_position(newLoc, newCtrl, 1, 1, 1)
                        armor_ctrl_list.append(newCtrl)
                        if loopIndex == 0:
                            transform.parent(newCtrl, newRootCtrl)
                        else:
                            transform.parent(newCtrl, '{}_A_{}_ctrl'.format(eachRootLoc.replace('_loc',''), loopIndex-1))
                        self.ControlBuilder.make_group_multi(newCtrl)
                        transform.parent(eachJnt, newCtrl)
                        bind_joint_list.append(eachJnt)
                    if len(children) == 2:
                        FK_loc_chain_B.append(children[1])
                        FK_loc_chain_B_childern = mc.listRelatives(children[1], allDescendents=True, type='transform')
                        if FK_loc_chain_B_childern:
                            FK_loc_chain_B.extend(FK_loc_chain_B_childern)
                        for eachLoc in FK_loc_chain_B:
                            loopIndex = FK_loc_chain_B.index(eachLoc)
                            newLoc = mc.rename(eachLoc, '{}_B_{}_loc'.format(eachRootLoc.replace('_loc',''), loopIndex))
                            eachJnt = self.JointBuilder.locator_to_joint(newLoc, '_loc', '_bind')
                            newCtrl = self.ControlBuilder.create("box",
                                                                 eachJnt.replace('_bind', '_ctrl'),
                                                                 color=side_sec_color,
                                                                 r=self.global_size
                                                                 )
                            transform.catch_position(newLoc, newCtrl, 1, 1, 1)
                            armor_ctrl_list.append(newCtrl)
                            if loopIndex == 0:
                                transform.parent(newCtrl, newRootCtrl)
                            else:
                                transform.parent(newCtrl, '{}_B_{}_ctrl'.format(eachRootLoc.replace('_loc',''), loopIndex-1))
                            self.ControlBuilder.make_group_multi(newCtrl)
                            transform.parent(eachJnt, newCtrl)
                            bind_joint_list.append(eachJnt)
                    elif len(children) > 2:
                        mc.warning('current shoulder loc chain only support two chains, please check yourself')
                        continue

        # build a, b joint chain
        if bind_joint_list:
            bindJntsSet = mc.sets(name=prefix + "_bindJnts", empty=True)
            mc.sets(bind_joint_list, add=bindJntsSet)
        if armor_ctrl_list:
            armorCtrlSet = mc.sets(name=prefix + "_armorCtrl", empty=True)
            mc.sets(armor_ctrl_list, add=armorCtrlSet)
        xpRigFunctions.groupIsGenerated(armorRigSecGrp, finished=True)
        mc.select(armorRigSecGrp, r=1)
        print('build successfully')
        #return bind_joint_list

    def create_armor_shoulder_drive(self, guideMainGrp):
        if xpRigFunctions.groupAttrAdded(guideMainGrp, parent='', attrName='armorShoulderDrive', finished=False):
            return
        armorRigTriGrps = mc.listRelatives(guideMainGrp, ch=1)
        for eachGrp in armorRigTriGrps:
            if '_L_' in eachGrp:
                transform.parent(eachGrp, 'shoulder_L_shoulder_1_bind')
            elif '_R_' in eachGrp:
                transform.parent(eachGrp, 'shoulder_R_shoulder_1_bind')

        xpRigFunctions.groupAttrAdded(guideMainGrp, parent='', attrName='armorShoulderDrive', finished=True)

    # TODO:  骨骼设置好层级，一次性生成
    def create_armor_pauldrons_setup(self, guideMainGrp):

        # read guide and create group
        bind_joint_list = []
        armor_ctrl_list = []

        guide_grp_keys = mc.listRelatives(guideMainGrp, ad=True, type='transform')
        guide_grp_keys.append(guideMainGrp)
        guideSecGrps = fnmatch.filter(guide_grp_keys, self.guideGrpSuffix)
        try:
            guideInfoGrps = fnmatch.filter(guide_grp_keys, self._grp_Suffix)[0]
            prefix = mc.getAttr(
                str(guideInfoGrps) + ".prefix")  # xpRigFunctions.getGrpAttrInfo(guideMainGrp, self.prefixAttr, defaultAttrName=guideSecGrps[0].split('_')[0])
        except:
            mc.warning(' ****** - guide error ! - ******  please select guide group')
            return

        try:
            aimDirection = mc.getAttr(str(guideInfoGrps) + ".aim")
            upDirection = mc.getAttr(str(guideInfoGrps) + ".up")
        except:
            aimDirection = 'X'
            upDirection = 'Y'
            # prefix = guideSecGrps[0].split('_')[0]
        aimVec = (1, 0, 0)
        upVec = (0, 1, 0)
        ForwardAxis = 0
        upAxis = 0
        if aimDirection == 'X':
            aimVec = (1, 0, 0)
            ForwardAxis = 0
            if upDirection == 'y':
                upVec = (0, 1, 0)
                upAxis = 0
            elif upDirection == 'Z':
                upVec = (0, 0, 1)
                upAxis = 3
        elif aimDirection == 'Y':
            aimVec = (0, 1, 0)
            ForwardAxis = 2
            if upDirection == 'X':
                upVec = (1, 0, 0)
                upAxis = 6
            elif upDirection == 'Z':
                upVec = (0, 0, 1)
                upAxis = 3
        elif aimDirection == 'Z':
            aimVec = (0, 0, 1)
            ForwardAxis = 4
            if upDirection == 'X':
                upVec = (1, 0, 0)
                upAxis = 6
            elif upDirection == 'Y':
                upVec = (0, 1, 0)
                upAxis = 0

        armorRigSecGrp = xpRigFunctions.createGrp(prefix + self.armorRigSecGrp)
        generateInfo = xpRigFunctions.groupIsGenerated(armorRigSecGrp)
        if generateInfo:
            return
        #armorRigSecSetGrp = xpRigFunctions.createGrp(prefix + self.armorRigSecGrp + "_set", armorRigSecGrp)
        #splineIK_crv_grp = xpRigFunctions.createGrp(prefix + self.armorRigTriIKCrvGrp, parent=armorRigSecGrp)
        #mc.setAttr(splineIK_crv_grp + ".inheritsTransform", 0)
        #disCrv_grp = xpRigFunctions.createGrp(prefix + self.armorRigTriDisCrvGrp, parent=armorRigSecGrp)
        #mc.setAttr(disCrv_grp + ".inheritsTransform", 0)

        # create curves and joints
        for eachGrp in guideSecGrps: # left and right
            #整体结构是 大fk链条套小fkik链条

            #guideCrvShape = mc.listRelatives(eachGrp, ad=True, type='nurbsCurve', f=True)[0]
            #guideCrv = mc.listRelatives(guideCrvShape, p=True, f=False)[0]

            #guideCurve = xpRigFunctions.create_nurbsCurve_from_locators(guideLocs, guideCrv + '_splineIK_crv')
            #transform.parent(guideCurve, splineIK_crv_grp)

            if '_L_' in eachGrp:
                chainSide = 'L'
                side_color = 6
                side_sec_color = 15
            elif '_R_' in eachGrp:
                chainSide = 'R'
                side_color = 13
                side_sec_color = 12
            elif '_M_' in eachGrp:
                chainSide = 'M'
                side_color = 17
                side_sec_color = 21
            else:
                chainSide = 'M'
                side_color = 17
                side_sec_color = 21

            # 创建 主 FK ctrl chain ：pauldrons_L_1_ctrl
            FK_ctrl_list = []
            IK_ctrl_list = []
            FK_f_sec_ctrl_list = []
            FK_b_sec_ctrl_list = []
            # get main fk chain guide locators
            allGuideLocs = mc.listRelatives(eachGrp, ad=True, type='joint') # main fk chain
            mainGuideLocs1 = fnmatch.filter(allGuideLocs, '*_main_*')
            mainGuideLocs = sorted(mainGuideLocs1)

            # 创建主FK链条
            fk_main_jnt_list = self.JointBuilder.joint_to_joint_repalce(mainGuideLocs,
                                                               '_guide',
                                                               '_main_ctrl',
                                                               step=1)
            transform.parent(fk_main_jnt_list[0], armorRigSecGrp)

            for eachCtrl in fk_main_jnt_list:
                newRef = self.ControlBuilder.create("circle",
                                                    eachCtrl.replace('_ctrl', '__main_ctrl'),
                                                    color=18,
                                                    r=self.global_size * 3.5,
                                                    aim_vector=aimVec
                                                    )
                refShape = mc.listRelatives(newRef, c=True, type='nurbsCurve')[0]
                mc.parent(refShape, eachCtrl, r=1, s=1)
                mc.delete(newRef)
                self.ControlBuilder.make_group_multi(eachCtrl)
                armor_ctrl_list.append(eachCtrl)

            # 创建FKIK链条
            print '735', mainGuideLocs
            for eachMainGuide in mainGuideLocs:
                # 每根主骨骼下面有两根次级骨骼, 前后两条fk链条
                secGuideRootLocs = mc.listRelatives(eachMainGuide, c=True, type='joint')
                for eachRootLoc in secGuideRootLocs:
                    if eachRootLoc in mainGuideLocs:
                        secGuideRootLocs.remove(eachRootLoc)
                print '738', secGuideRootLocs # [u'pauldrons_1_f1_guide', u'pauldrons_1_b1_guide']


                secGuideListA1 = mc.listRelatives(secGuideRootLocs[0], ad=True, type='joint')
                secGuideListA1.insert(0, secGuideRootLocs[0])
                secGuideListA = sorted(secGuideListA1)
                print '739', secGuideListA
                A_fk_ctrl_list = self.JointBuilder.joint_to_joint_repalce(secGuideListA,
                                                                            '_guide',
                                                                            '_fk_ctrl',
                                                                            step=1)
                transform.parent(A_fk_ctrl_list[0], eachMainGuide.replace('_guide', '_main_ctrl'))

                # 创建FK控制器以及IK控制器，骨骼
                for eachCtrl in A_fk_ctrl_list:
                    armor_ctrl_list.append(eachCtrl)
                    newRef = self.ControlBuilder.create("circle",
                                                         eachCtrl.replace('_ctrl', '_ref'),
                                                         color = side_color,
                                                         r = self.global_size * 1.5,
                                                         aim_vector = aimVec
                                                         )
                    transform.catch_position(eachCtrl, newRef, 1, 1, 1)
                    refShape = mc.listRelatives(newRef, c=True, type='nurbsCurve')[0]
                    mc.parent(refShape, eachCtrl, r=1, s=1)
                    mc.delete(newRef)

                    newIkCtrl = self.ControlBuilder.create("box",
                                                         eachCtrl.replace('_fk_ctrl', '_ik_ctrl'),
                                                         color=side_sec_color,
                                                         r=self.global_size * 0.75
                                                         )
                    transform.catch_position(eachCtrl, newIkCtrl, 1, 1, 1)
                    transform.parent(newIkCtrl, eachCtrl)
                    eachJnt = self.JointBuilder.locator_to_joint(eachCtrl, '_fk_ctrl', '_bind')
                    armor_ctrl_list.append(newIkCtrl)
                    bind_joint_list.append(eachJnt)

                    transform.catch_position(newIkCtrl, eachJnt, 1, 1, 1)
                    try:
                        transform.parent(eachJnt, newIkCtrl)
                    except:
                        pass

                    self.ControlBuilder.make_group_multi(eachCtrl)
                    self.ControlBuilder.make_group_multi(newIkCtrl)
                    bind_joint_list.append(eachJnt)
                    armor_ctrl_list.append(eachCtrl)
                    armor_ctrl_list.append(newIkCtrl)

                secGuideListB1 = mc.listRelatives(secGuideRootLocs[1], ad=True, type='joint')
                secGuideListB1.insert(0, secGuideRootLocs[1])
                secGuideListB = sorted(secGuideListB1)
                B_fk_jnt_list = self.JointBuilder.joint_to_joint_repalce(secGuideListB,
                                                                            '_guide',
                                                                            '_fk_ctrl',
                                                                            step=1)
                transform.parent(B_fk_jnt_list[0], eachMainGuide.replace('_guide', '_main_ctrl'))
                # 创建FK控制器以及IK控制器，骨骼
                for eachCtrl in B_fk_jnt_list:
                    armor_ctrl_list.append(eachCtrl)
                    newRef = self.ControlBuilder.create("circle",
                                                        eachCtrl.replace('_ctrl', '_ref'),
                                                        color=side_color,
                                                        r=self.global_size * 1.5,
                                                        aim_vector=aimVec
                                                        )
                    transform.catch_position(eachCtrl, newRef, 1, 1, 1)
                    refShape = mc.listRelatives(newRef, c=True, type='nurbsCurve')[0]
                    mc.parent(refShape, eachCtrl, r=1, s=1)
                    mc.delete(newRef)

                    newIkCtrl = self.ControlBuilder.create("box",
                                                         eachCtrl.replace('_fk_ctrl', '_ik_ctrl'),
                                                         color=side_sec_color,
                                                         r=self.global_size * 0.75
                                                         )
                    transform.catch_position(eachCtrl, newIkCtrl, 1, 1, 1)
                    transform.parent(newIkCtrl, eachCtrl)
                    eachJnt = self.JointBuilder.locator_to_joint(eachCtrl, '_fk_ctrl', '_bind')
                    armor_ctrl_list.append(newIkCtrl)
                    bind_joint_list.append(eachJnt)

                    transform.catch_position(newIkCtrl, eachJnt, 1, 1, 1)
                    try:
                        transform.parent(eachJnt, newIkCtrl)
                    except:
                        pass

                    self.ControlBuilder.make_group_multi(eachCtrl)
                    self.ControlBuilder.make_group_multi(newIkCtrl)


            # body权重 -> 曲线权重
            try:
                pass
            except:
                print  "copy Error, jump copy"

        if bind_joint_list:
            bindJntsSet = mc.sets(name=prefix + "_bindJnts", empty=True)
            mc.sets(bind_joint_list, add=bindJntsSet)
        if armor_ctrl_list:
            armorCtrlSet = mc.sets(name=prefix + "_armorCtrl", empty=True)
            mc.sets(armor_ctrl_list, add=armorCtrlSet)
        xpRigFunctions.groupIsGenerated(armorRigSecGrp, finished=True)
        mc.select(armorRigSecGrp, r=1)

    def apply_ctrl_scale_fnc(self, size):
        print(size)

        # 定义缩放参数
        relative = True  # 相对缩放

        # 获取当前选择对象
        selected_objects = mc.ls(selection=True, type='transform')

        if selected_objects:
            for each in selected_objects:
                shapes = mc.listRelatives(each, children=True, shapes=True, type='nurbsCurve', fullPath=True)
                if not shapes:
                    continue
                crvShape = shapes[0]
                spans = mc.getAttr(crvShape + '.spans')
                degree = mc.getAttr(crvShape + '.degree')
                num_cvs = spans + degree

                # 创建控制点列表
                control_points = ['{}.cv[{}]'.format(crvShape, i) for i in range(num_cvs)]
                pivot = mc.xform(each, query=True, ws=True, rp=True)
                mc.scale(size, size, size,
                           control_points,
                           pivot=pivot,
                           relative=relative)
        else:
            print("No objects selected.")

    def scale_ctrl(self, ctrl_list, scale_size):
        for eachCtrl in ctrl_list:
            mc.scale(scale_size, scale_size, scale_size, ctrl_list, absolute=True)

    def create_body_drive(self):
        #armorRigMainGrp = xpRigFunctions.createGrp(self.armorRigMainGrp)
        hip_R_1_fk_ctrl_body_drv_grp = xpRigFunctions.createGrp('hip_R_1_fk_ctrl_body_drv_grp',
                                                                parent='hip_R_1_fk_ctrl')
        transform.catch_position('hip_R_1_fk_ctrl', hip_R_1_fk_ctrl_body_drv_grp, 1, 1, 1)
        if xpRigFunctions.groupAttrAdded(hip_R_1_fk_ctrl_body_drv_grp, parent='', attrName='body_drive_setup', finished=False):
            return
        # generate hip_R_hip_1_front_bind

        loc_R_List = ['hip_R_hip_1_bind', 'hip_R_hip_2_bind']
        if not mc.objExists('hip_R_hip_1_bind'):
            mc.warning(' ****** - error ! - ******  please import or reference character without nameSpace first')
            return
        hip_R_1_fk_ctrl_body_drv_grp = xpRigFunctions.createGrp('hip_R_1_fk_ctrl_body_drv_grp', parent='hip_R_1_fk_ctrl')

        # create _R_ locators under spine_M_spine_1_bind:
        hip_R_hip_1_limit_locator_ofs = xpRigFunctions.create_locators("hip_R_hip_1_limit_locator_ofs", 'spine_M_spine_1_bind', 'hip_R_1_fk_ctrl', 1, 1, 1)
        hip_R_1_fk_ctrl_sb_translation = mc.xform('hip_R_1_fk_ctrl', query=True, translation=True, worldSpace=True)
        leg_R_knee_fk_ctrl_sb_translation = mc.xform('leg_R_knee_fk_ctrl', query=True, translation=True, worldSpace=True)
        y_dis = -(abs(hip_R_1_fk_ctrl_sb_translation[1]) - abs(leg_R_knee_fk_ctrl_sb_translation[1]))
        mc.setAttr(hip_R_hip_1_limit_locator_ofs + '.ty', y_dis)

        hip_R_hip_1_local_locator = xpRigFunctions.create_locators("hip_R_hip_1_local_locator", hip_R_1_fk_ctrl_body_drv_grp, hip_R_hip_1_limit_locator_ofs, 1, 1, 1)
        leg_R_leg_1_local_locator = xpRigFunctions.create_locators("leg_R_leg_1_local_locator", hip_R_1_fk_ctrl_body_drv_grp, 'hip_R_1_fk_ctrl', 1, 1, 1)
        mc.parentConstraint('leg_R_leg_1_bind', leg_R_leg_1_local_locator, mo=0)

        hip_R_hip_1_front_limit_locator = xpRigFunctions.create_locators("hip_R_hip_1_front_limit_locator", hip_R_hip_1_limit_locator_ofs, hip_R_hip_1_limit_locator_ofs, 1, 1, 1)
        hip_R_hip_1_back_limit_locator = xpRigFunctions.create_locators("hip_R_hip_1_back_limit_locator", hip_R_hip_1_limit_locator_ofs, hip_R_hip_1_limit_locator_ofs, 1, 1, 1)
        hip_R_hip_1_free_limit_locator = xpRigFunctions.create_locators("hip_R_hip_1_free_limit_locator", hip_R_hip_1_limit_locator_ofs, hip_R_hip_1_limit_locator_ofs, 1, 1, 1)

        mc.pointConstraint(hip_R_hip_1_local_locator, hip_R_hip_1_front_limit_locator, mo=0)
        mc.pointConstraint(hip_R_hip_1_local_locator, hip_R_hip_1_back_limit_locator, mo=0)
        mc.pointConstraint(hip_R_hip_1_local_locator, hip_R_hip_1_free_limit_locator, mo=0)

        # hip_R_hip_1_front_bind =======================================================================================
        bind_R_jnt_list = self.JointBuilder.joint_to_joint_repalce(loc_R_List,
                                                           '_bind',
                                                           '_front_bind',
                                                           step=1)

        secBindJnt = bind_R_jnt_list[1].replace('hip', 'leg').replace('_2_', '_1_')
        mc.rename(bind_R_jnt_list[1], secBindJnt)
        bind_R_jnt_list.append(secBindJnt)
        bind_R_jnt_list.pop(1)
        transform.parent(bind_R_jnt_list[0], hip_R_1_fk_ctrl_body_drv_grp)

        local_R_jnt_list_new = self.JointBuilder.joint_to_joint_repalce(loc_R_List,
                                                           '_bind',
                                                           '_front_local',
                                                           step=1)
        local_R_jnt_list = []
        for each in local_R_jnt_list_new:
            mc.rename(each, each.replace('hip', 'leg'))
            local_R_jnt_list.append(each.replace('hip', 'leg'))
        transform.parent(local_R_jnt_list[0], bind_R_jnt_list[0])
        #transform.catch_position(bind_R_jnt_list[1], local_R_jnt_list[0], 1, 1, 1)
        #transform.catch_position('leg_R_knee_fk_ctrl', local_R_jnt_list[1], 1, 1, 1)
        mc.connectAttr(leg_R_leg_1_local_locator + '.translate', local_R_jnt_list[0] + '.translate')
        mc.connectAttr(leg_R_leg_1_local_locator + '.rotate', local_R_jnt_list[0] + '.rotate')
        mc.delete(mc.pointConstraint('leg_R_knee_fk_ctrl', local_R_jnt_list[1], mo=0))
        print('855', local_R_jnt_list[0], local_R_jnt_list[1])

        mc.aimConstraint(hip_R_hip_1_front_limit_locator, bind_R_jnt_list[0], weight=1, upVector=(1, 0, 0), mo=0,
                         worldUpObject='spine_M_spine_1_bind', worldUpType=2, aimVector=(0, 1, 0))

        leg_R_leg_1_front_limit_locator_ofs = xpRigFunctions.create_locators("leg_R_leg_1_front_limit_locator_ofs",
                                                                         bind_R_jnt_list[0],
                                                                         'leg_R_knee_fk_ctrl', 1, 1, 1)
        leg_R_leg_1_front_limit_locator = xpRigFunctions.create_locators("leg_R_leg_1_front_limit_locator",
                                                                         leg_R_leg_1_front_limit_locator_ofs,
                                                                         'leg_R_knee_fk_ctrl', 1, 1, 1)
        leg_R_leg_1_front_free_locator = xpRigFunctions.create_locators("leg_R_leg_1_front_free_locator",
                                                                         leg_R_leg_1_front_limit_locator_ofs,
                                                                         'leg_R_knee_fk_ctrl', 1, 1, 1)
        mc.pointConstraint(local_R_jnt_list[1], leg_R_leg_1_front_limit_locator, mo=0)
        mc.pointConstraint(local_R_jnt_list[1], leg_R_leg_1_front_free_locator, mo=0)

        mc.aimConstraint(leg_R_leg_1_front_limit_locator, bind_R_jnt_list[1], weight=1, upVector=(1, 0, 0), mo=0,
                         worldUpObject=local_R_jnt_list[0], worldUpType=2, aimVector=(0, 1, 0))

        # hip_R_hip_1_back_bind =======================================================================================
        bind_R_jnt_list = self.JointBuilder.joint_to_joint_repalce(loc_R_List,
                                                           '_bind',
                                                           '_back_bind',
                                                           step=1)
        secBindJnt = bind_R_jnt_list[1].replace('hip', 'leg').replace('_2_', '_1_')
        mc.rename(bind_R_jnt_list[1], secBindJnt)
        bind_R_jnt_list.append(secBindJnt)
        bind_R_jnt_list.pop(1)
        transform.parent(bind_R_jnt_list[0], hip_R_1_fk_ctrl_body_drv_grp)

        local_R_jnt_list_new = self.JointBuilder.joint_to_joint_repalce(loc_R_List,
                                                           '_bind',
                                                           '_back_local',
                                                           step=1)
        local_R_jnt_list = []
        for each in local_R_jnt_list_new:
            mc.rename(each, each.replace('hip', 'leg'))
            local_R_jnt_list.append(each.replace('hip', 'leg'))
        transform.parent(local_R_jnt_list[0], bind_R_jnt_list[0])
        #transform.catch_position(bind_R_jnt_list[1], local_R_jnt_list[0], 1, 1, 1)
        #transform.catch_position('leg_R_knee_fk_ctrl', local_R_jnt_list[1], 1, 1, 1)
        mc.delete(mc.parentConstraint('hip_R_1_fk_ctrl', local_R_jnt_list[0], mo=0))
        mc.delete(mc.parentConstraint('leg_R_knee_fk_ctrl', local_R_jnt_list[1], mo=0))

        mc.aimConstraint(hip_R_hip_1_back_limit_locator, bind_R_jnt_list[0], weight=1, upVector=(1, 0, 0), mo=0,
                         worldUpObject='spine_M_spine_1_bind', worldUpType=2, aimVector=(0, 1, 0))

        leg_R_leg_1_back_limit_locator_ofs = xpRigFunctions.create_locators("leg_R_leg_1_back_limit_locator_ofs",
                                                                         bind_R_jnt_list[0],
                                                                         'leg_R_knee_fk_ctrl', 1, 1, 1)
        leg_R_leg_1_back_limit_locator = xpRigFunctions.create_locators("leg_R_leg_1_back_limit_locator",
                                                                         leg_R_leg_1_back_limit_locator_ofs,
                                                                         'leg_R_knee_fk_ctrl', 1, 1, 1)
        leg_R_leg_1_back_free_locator = xpRigFunctions.create_locators("leg_R_leg_1_back_free_locator",
                                                                         leg_R_leg_1_back_limit_locator_ofs,
                                                                         'leg_R_knee_fk_ctrl', 1, 1, 1)
        mc.pointConstraint(local_R_jnt_list[1], leg_R_leg_1_back_limit_locator, mo=0)
        mc.pointConstraint(local_R_jnt_list[1], leg_R_leg_1_back_free_locator, mo=0)

        mc.aimConstraint(leg_R_leg_1_back_limit_locator, bind_R_jnt_list[1], weight=1, upVector=(1, 0, 0), mo=0,
                         worldUpObject=local_R_jnt_list[0], worldUpType=2, aimVector=(0, 1, 0))

        xpRigFunctions.groupAttrAdded(hip_R_1_fk_ctrl_body_drv_grp, parent='', attrName='body_drive_setup', finished=True)

        hip_L_1_fk_ctrl_body_drv_grp = xpRigFunctions.createGrp('hip_L_1_fk_ctrl_body_drv_grp',
                                                                parent='hip_L_1_fk_ctrl')
        transform.catch_position('hip_L_1_fk_ctrl', hip_L_1_fk_ctrl_body_drv_grp, 1, 1, 1)
        if xpRigFunctions.groupAttrAdded(hip_L_1_fk_ctrl_body_drv_grp, parent='', attrName='body_drive_setup', finished=False):
            return
        # generate hip_L_hip_1_front_bind

        loc_L_List = ['hip_L_hip_1_bind', 'hip_L_hip_2_bind']
        if not mc.objExists('hip_L_hip_1_bind'):
            mc.warning(' ****** - error ! - ******  please import or reference character without nameSpace first')
            return


        hip_L_1_fk_ctrl_body_drv_grp = xpRigFunctions.createGrp('hip_L_1_fk_ctrl_body_drv_grp', parent='hip_L_1_fk_ctrl')

        # create _L_ locators under spine_M_spine_1_bind:
        hip_L_hip_1_limit_locator_ofs = xpRigFunctions.create_locators("hip_L_hip_1_limit_locator_ofs", 'spine_M_spine_1_bind', 'hip_L_1_fk_ctrl', 1, 1, 1)
        hip_L_1_fk_ctrl_sb_translation = mc.xform('hip_L_1_fk_ctrl', query=True, translation=True, worldSpace=True)
        leg_L_knee_fk_ctrl_sb_translation = mc.xform('leg_L_knee_fk_ctrl', query=True, translation=True,worldSpace=True)
        y_dis = -(abs(hip_L_1_fk_ctrl_sb_translation[1]) - abs(leg_L_knee_fk_ctrl_sb_translation[1]))
        mc.setAttr(hip_L_hip_1_limit_locator_ofs + '.ty', y_dis)

        hip_L_hip_1_local_locator = xpRigFunctions.create_locators("hip_L_hip_1_local_locator", hip_L_1_fk_ctrl_body_drv_grp, hip_L_hip_1_limit_locator_ofs, 1, 1, 1)
        leg_L_leg_1_local_locator = xpRigFunctions.create_locators("leg_L_leg_1_local_locator", hip_L_1_fk_ctrl_body_drv_grp, 'hip_L_1_fk_ctrl', 1, 1, 1)
        mc.parentConstraint('leg_L_leg_1_bind', leg_L_leg_1_local_locator, mo=0)

        hip_L_hip_1_front_limit_locator = xpRigFunctions.create_locators("hip_L_hip_1_front_limit_locator", hip_L_hip_1_limit_locator_ofs, hip_L_hip_1_limit_locator_ofs, 1, 1, 1)
        hip_L_hip_1_back_limit_locator = xpRigFunctions.create_locators("hip_L_hip_1_back_limit_locator", hip_L_hip_1_limit_locator_ofs, hip_L_hip_1_limit_locator_ofs, 1, 1, 1)
        hip_L_hip_1_free_limit_locator = xpRigFunctions.create_locators("hip_L_hip_1_free_limit_locator", hip_L_hip_1_limit_locator_ofs, hip_L_hip_1_limit_locator_ofs, 1, 1, 1)

        mc.pointConstraint(hip_L_hip_1_local_locator, hip_L_hip_1_front_limit_locator, mo=0)
        mc.pointConstraint(hip_L_hip_1_local_locator, hip_L_hip_1_back_limit_locator, mo=0)
        mc.pointConstraint(hip_L_hip_1_local_locator, hip_L_hip_1_free_limit_locator, mo=0)

        # hip_L_hip_1_front_bind =======================================================================================
        bind_L_jnt_list = self.JointBuilder.joint_to_joint_repalce(loc_L_List,
                                                           '_bind',
                                                           '_front_bind',
                                                           step=1)
        secBindJnt = bind_L_jnt_list[1].replace('hip', 'leg').replace('_2_', '_1_')
        mc.rename(bind_L_jnt_list[1], secBindJnt)
        bind_L_jnt_list.append(secBindJnt)
        bind_L_jnt_list.pop(1)
        transform.parent(bind_L_jnt_list[0], hip_L_1_fk_ctrl_body_drv_grp)

        local_L_jnt_list_new  = self.JointBuilder.joint_to_joint_repalce(loc_L_List,
                                                           '_bind',
                                                           '_front_local',
                                                           step=1)
        local_L_jnt_list = []
        for each in local_L_jnt_list_new:
            mc.rename(each, each.replace('hip', 'leg'))
            local_L_jnt_list.append(each.replace('hip', 'leg'))
        transform.parent(local_L_jnt_list[0], bind_L_jnt_list[0])
        #transform.catch_position(bind_L_jnt_list[1], local_L_jnt_list[0], 1, 1, 1)
        #transform.catch_position('leg_L_knee_fk_ctrl', local_L_jnt_list[1], 1, 1, 1)
        mc.delete(mc.parentConstraint('hip_L_1_fk_ctrl', local_L_jnt_list[0], mo=0))
        mc.delete(mc.parentConstraint('leg_L_knee_fk_ctrl', local_L_jnt_list[1], mo=0))

        mc.aimConstraint(hip_L_hip_1_front_limit_locator, bind_L_jnt_list[0], weight=1, upVector=(1, 0, 0), mo=0,
                         worldUpObject='spine_M_spine_1_bind', worldUpType=2, aimVector=(0, 1, 0))

        leg_L_leg_1_front_limit_locator_ofs = xpRigFunctions.create_locators("leg_L_leg_1_front_limit_locator_ofs",
                                                                         bind_L_jnt_list[0],
                                                                         'leg_L_knee_fk_ctrl', 1, 1, 1)
        leg_L_leg_1_front_limit_locator = xpRigFunctions.create_locators("leg_L_leg_1_front_limit_locator",
                                                                         leg_L_leg_1_front_limit_locator_ofs,
                                                                         'leg_L_knee_fk_ctrl', 1, 1, 1)
        leg_L_leg_1_front_free_locator = xpRigFunctions.create_locators("leg_L_leg_1_front_free_locator",
                                                                         leg_L_leg_1_front_limit_locator_ofs,
                                                                         'leg_L_knee_fk_ctrl', 1, 1, 1)
        mc.pointConstraint(local_L_jnt_list[1], leg_L_leg_1_front_limit_locator, mo=0)
        mc.pointConstraint(local_L_jnt_list[1], leg_L_leg_1_front_free_locator, mo=0)

        mc.aimConstraint(leg_L_leg_1_front_limit_locator, bind_L_jnt_list[1], weight=1, upVector=(1, 0, 0), mo=0,
                         worldUpObject=local_L_jnt_list[0], worldUpType=2, aimVector=(0, 1, 0))

        # hip_L_hip_1_back_bind =======================================================================================
        bind_L_jnt_list = self.JointBuilder.joint_to_joint_repalce(loc_L_List,
                                                           '_bind',
                                                           '_back_bind',
                                                           step=1)
        secBindJnt = bind_L_jnt_list[1].replace('hip', 'leg').replace('_2_', '_1_')
        mc.rename(bind_L_jnt_list[1], secBindJnt)
        bind_L_jnt_list.append(secBindJnt)
        bind_L_jnt_list.pop(1)
        transform.parent(bind_L_jnt_list[0], hip_L_1_fk_ctrl_body_drv_grp)

        local_L_jnt_list_new = self.JointBuilder.joint_to_joint_repalce(loc_L_List,
                                                           '_bind',
                                                           '_back_local',
                                                           step=1)
        local_L_jnt_list = []
        for each in local_L_jnt_list_new:
            mc.rename(each, each.replace('hip', 'leg'))
            local_L_jnt_list.append(each.replace('hip', 'leg'))
        transform.parent(local_L_jnt_list[0], bind_L_jnt_list[0])
        #transform.catch_position(bind_L_jnt_list[1], local_L_jnt_list[0], 1, 1, 1)
        #transform.catch_position('leg_L_knee_fk_ctrl', local_L_jnt_list[1], 1, 1, 1)
        mc.delete(mc.parentConstraint('hip_L_1_fk_ctrl', local_L_jnt_list[0], mo=0))
        mc.delete(mc.parentConstraint('leg_L_knee_fk_ctrl', local_L_jnt_list[1], mo=0))

        mc.aimConstraint(hip_L_hip_1_back_limit_locator, bind_L_jnt_list[0], weight=1, upVector=(1, 0, 0), mo=0,
                         worldUpObject='spine_M_spine_1_bind', worldUpType=2, aimVector=(0, 1, 0))

        leg_L_leg_1_back_limit_locator_ofs = xpRigFunctions.create_locators("leg_L_leg_1_back_limit_locator_ofs",
                                                                         bind_L_jnt_list[0],
                                                                         'leg_L_knee_fk_ctrl', 1, 1, 1)
        leg_L_leg_1_back_limit_locator = xpRigFunctions.create_locators("leg_L_leg_1_back_limit_locator",
                                                                         leg_L_leg_1_back_limit_locator_ofs,
                                                                         'leg_L_knee_fk_ctrl', 1, 1, 1)
        leg_L_leg_1_back_free_locator = xpRigFunctions.create_locators("leg_L_leg_1_back_free_locator",
                                                                         leg_L_leg_1_back_limit_locator_ofs,
                                                                         'leg_L_knee_fk_ctrl', 1, 1, 1)
        mc.pointConstraint(local_L_jnt_list[1], leg_L_leg_1_back_limit_locator, mo=0)
        mc.pointConstraint(local_L_jnt_list[1], leg_L_leg_1_back_free_locator, mo=0)

        mc.aimConstraint(leg_L_leg_1_back_limit_locator, bind_L_jnt_list[1], weight=1, upVector=(1, 0, 0), mo=0,
                         worldUpObject=local_L_jnt_list[0], worldUpType=2, aimVector=(0, 1, 0))

        hip_L_1_fk_ctrl_body_drv_grp = xpRigFunctions.createGrp('hip_L_1_fk_ctrl_body_drv_grp', parent='hip_L_1_fk_ctrl')


        xpRigFunctions.groupAttrAdded(hip_L_1_fk_ctrl_body_drv_grp, parent='', attrName='body_drive_setup', finished=True)


    def create_armlet_setup(self, guideMainGrp):

        # read guide and create group
        bind_joint_list = []
        armor_ctrl_list = []

        guide_grp_keys = mc.listRelatives(guideMainGrp, ad=True, type='transform')
        guide_grp_keys.append(guideMainGrp)
        guideSecGrps = fnmatch.filter(guide_grp_keys, self.guideGrpSuffix)
        try:
            guideInfoGrps = fnmatch.filter(guide_grp_keys, self._grp_Suffix)[0]
            prefix = mc.getAttr(
                str(guideInfoGrps) + ".prefix")  # xpRigFunctions.getGrpAttrInfo(guideMainGrp, self.prefixAttr, defaultAttrName=guideSecGrps[0].split('_')[0])
        except:
            mc.warning(' ****** - guide error ! - ******  please select guide group')
            return
        try:
            aimDirection = mc.getAttr(str(guideInfoGrps) + ".aim")
            upDirection = mc.getAttr(str(guideInfoGrps) + ".up")
        except:
            aimDirection = 'X'
            upDirection = 'Y'
            # prefix = guideSecGrps[0].split('_')[0]
        aimVec = (1, 0, 0)
        upVec = (0, 1, 0)
        ForwardAxis = 0
        upAxis = 0
        if aimDirection == 'X':
            aimVec = (1, 0, 0)
            ForwardAxis = 0
            if upDirection == 'y':
                upVec = (0, 1, 0)
                upAxis = 0
            elif upDirection == 'Z':
                upVec = (0, 0, 1)
                upAxis = 3
        elif aimDirection == 'Y':
            aimVec = (0, 1, 0)
            ForwardAxis = 2
            if upDirection == 'X':
                upVec = (1, 0, 0)
                upAxis = 6
            elif upDirection == 'Z':
                upVec = (0, 0, 1)
                upAxis = 3
        elif aimDirection == 'Z':
            aimVec = (0, 0, 1)
            ForwardAxis = 4
            if upDirection == 'X':
                upVec = (1, 0, 0)
                upAxis = 6
            elif upDirection == 'Y':
                upVec = (0, 1, 0)
                upAxis = 0

        armorRigSecGrp = xpRigFunctions.createGrp(prefix + self.armorRigSecGrp)
        generateInfo = xpRigFunctions.groupIsGenerated(armorRigSecGrp)
        if generateInfo:
            return
        # armorRigSecSetGrp = xpRigFunctions.createGrp(prefix + self.armorRigSecGrp + "_set", armorRigSecGrp)
        # splineIK_crv_grp = xpRigFunctions.createGrp(prefix + self.armorRigTriIKCrvGrp, parent=armorRigSecGrp)
        # mc.setAttr(splineIK_crv_grp + ".inheritsTransform", 0)
        # disCrv_grp = xpRigFunctions.createGrp(prefix + self.armorRigTriDisCrvGrp, parent=armorRigSecGrp)
        # mc.setAttr(disCrv_grp + ".inheritsTransform", 0)

        # create curves and joints
        for eachGrp in guideSecGrps:  # left and right
            # 整体结构是 几条独立fk链条

            # guideCrvShape = mc.listRelatives(eachGrp, ad=True, type='nurbsCurve', f=True)[0]
            # guideCrv = mc.listRelatives(guideCrvShape, p=True, f=False)[0]

            # guideCurve = xpRigFunctions.create_nurbsCurve_from_locators(guideLocs, guideCrv + '_splineIK_crv')
            # transform.parent(guideCurve, splineIK_crv_grp)

            if '_L_' in eachGrp:
                chainSide = 'L'
                side_color = 6
                side_sec_color = 15
            elif '_R_' in eachGrp:
                chainSide = 'R'
                side_color = 13
                side_sec_color = 12
            elif '_M_' in eachGrp:
                chainSide = 'M'
                side_color = 17
                side_sec_color = 21
            else:
                chainSide = 'M'
                side_color = 17
                side_sec_color = 21

            # 创建 主 FK ctrl chain ：pauldrons_L_1_ctrl
            FK_ctrl_list = []
            IK_ctrl_list = []
            FK_f_sec_ctrl_list = []
            FK_b_sec_ctrl_list = []
            # get main fk chain guide locators
            allGuideLocs = mc.listRelatives(eachGrp, ad=True, type='joint')  # main fk chain
            mainGuideLocs1 = fnmatch.filter(allGuideLocs, '*_main_*')
            mainGuideLocs = sorted(mainGuideLocs1)

            # 创建主FK链条
            fk_main_jnt_list = self.JointBuilder.joint_to_joint_repalce(mainGuideLocs,
                                                                        '_guide',
                                                                        '_main_ctrl',
                                                                        step=1)
            transform.parent(fk_main_jnt_list[0], armorRigSecGrp)
            for eachCtrl in fk_main_jnt_list:
                newRef = self.ControlBuilder.create("circle_rectangle",
                                                    eachCtrl.replace('_ctrl', '__main_ctrl'),
                                                    color=18,
                                                    r=self.global_size * 1.2,
                                                    aim_vector=aimVec
                                                    )
                refShape = mc.listRelatives(newRef, c=True, type='nurbsCurve')[0]
                mc.parent(refShape, eachCtrl, r=1, s=1)
                mc.delete(newRef)
                self.ControlBuilder.make_group_multi(eachCtrl)
                armor_ctrl_list.append(eachCtrl)

            mainRootJnt = self.JointBuilder.locator_to_joint(fk_main_jnt_list[0], '_ctrl', '_bind')
            transform.parent(mainRootJnt, armorRigSecGrp)
            bind_joint_list.append(mainRootJnt)

            # 创建其他FK链条
            secRootLocList = []
            secRootLocList1 = mc.listRelatives(mainGuideLocs[0], c=True, type='joint')
            for each in secRootLocList1:
                if each not in mainGuideLocs:
                    secRootLocList.append(each)
            for SecRootLoc in secRootLocList:
                secRootLocList = mc.listRelatives(SecRootLoc, ad=True, type='joint')
                secRootLocList.insert(0, SecRootLoc)
                secRootLocList1 = sorted(secRootLocList)

                fk_jnt_list = self.JointBuilder.joint_to_joint_repalce(secRootLocList1,
                                                                            '_guide',
                                                                            '_fk_ctrl',
                                                                            step=1)
                transform.parent(fk_jnt_list[0], armorRigSecGrp)
                for index, eachCtrl in enumerate(fk_jnt_list):
                    newRef = self.ControlBuilder.create("circle",
                                                        eachCtrl.replace('_ctrl', '__main_ctrl'),
                                                        color=21,
                                                        r=self.global_size * 0.7,
                                                        aim_vector=aimVec
                                                        )
                    refShape = mc.listRelatives(newRef, c=True, type='nurbsCurve')[0]
                    mc.parent(refShape, eachCtrl, r=1, s=1)
                    mc.delete(newRef)
                    eachJnt = self.JointBuilder.locator_to_joint(eachCtrl, '_ctrl', '_bind')
                    transform.parent(eachJnt, eachCtrl)
                    self.ControlBuilder.make_group_multi(eachCtrl)

                    mc.connectAttr(fk_main_jnt_list[index] + '.rotate', eachCtrl + '_drv.rotate')
                    bind_joint_list.append(eachJnt)
                    armor_ctrl_list.append(eachCtrl)

                # body权重 -> 曲线权重
            try:
                pass
            except:
                print  "copy Error, jump copy"

        if bind_joint_list:
            bindJntsSet = mc.sets(name=prefix + "_bindJnts", empty=True)
            mc.sets(bind_joint_list, add=bindJntsSet)
        if armor_ctrl_list:
            armorCtrlSet = mc.sets(name=prefix + "_armorCtrl", empty=True)
            mc.sets(armor_ctrl_list, add=armorCtrlSet)
        xpRigFunctions.groupIsGenerated(armorRigSecGrp, finished=True)
        mc.select(armorRigSecGrp, r=1)

def gen_angele_between_node(selected_locators):
    if len(selected_locators) != 3:
        mc.warning("Please select three ik ctrls as two vectors.")
        return

    tra1 = selected_locators[0]  # Assuming this corresponds to Locator1
    tra2 = selected_locators[1]  # Assuming this corresponds to Locator2
    tra3 = selected_locators[2]  # Assuming this corresponds to Locator2

    prefixA = (str(tra2) + '_bt_' + str(tra1) + '_vt_' + str(tra3)).replace('_splineIk_ctrl','').replace('_Ik_ctrl','')
    prefix1 = (str(tra1) +  '_vt_' + str(tra2)).replace('_splineIk_ctrl','').replace('_Ik_ctrl','')
    prefix2 = (str(tra2) +  '_vt_' + str(tra3)).replace('_splineIk_ctrl','').replace('_Ik_ctrl','')

    locator1 = xpRigFunctions.create_locators('poLc_' + tra1.replace('_splineIk_ctrl','').replace('_Ik_ctrl',''), tra1.replace('_Ik_ctrl', '_splineIk_jnt').replace('_ctrl', '_jnt'), tra1, t=1, r=0, ro=1)
    locator2 = xpRigFunctions.create_locators('poLc_' + tra2.replace('_splineIk_ctrl','').replace('_Ik_ctrl',''), tra2.replace('_Ik_ctrl', '_splineIk_jnt').replace('_ctrl', '_jnt'), tra2, t=1, r=0, ro=1)
    locator3 = xpRigFunctions.create_locators('poLc_' + tra3.replace('_splineIk_ctrl','').replace('_Ik_ctrl',''), tra3.replace('_Ik_ctrl', '_splineIk_jnt').replace('_ctrl', '_jnt'), tra3, t=1, r=0, ro=1)

    if mc.objExists(locator2 + '.' + prefixA):
        mc.select(locator2, r=1)
        return

    pm_a1 = mc.createNode('plusMinusAverage', name='pmA_' + prefix1)
    mc.setAttr(pm_a1 + '.operation', 2)
    mc.connectAttr(locator1 + '.worldPosition[0]', pm_a1 + '.input3D[0]', force=True)
    mc.connectAttr(locator2 + '.worldPosition[0]', pm_a1 + '.input3D[1]', force=True)

    pm_a2 = mc.createNode('plusMinusAverage', name='pmA_' + prefix2)
    mc.setAttr(pm_a2 + '.operation', 2)
    mc.connectAttr(locator2 + '.worldPosition[0]', pm_a2 + '.input3D[0]', force=True)
    mc.connectAttr(locator3 + '.worldPosition[0]', pm_a2 + '.input3D[1]', force=True)

    # Create an angleBetween node to calculate the angle
    angle_node = mc.createNode('angleBetween', name='agB_' + prefixA)
    mc.connectAttr(pm_a1 + '.output3D', angle_node + '.vector1', force=True)
    mc.connectAttr(pm_a2 + '.output3D', angle_node + '.vector2', force=True)

    # Output angle
    mc.addAttr(locator2, ln=prefixA, at="double", dv=0)
    mc.setAttr(locator2 + '.' + prefixA, e=True, keyable=True)
    mc.connectAttr(angle_node + '.angle', locator2 + '.' + prefixA, force=True)

    mc.select(locator2, r=1)

    # Call the function to create and connect nodes

if __name__ == '__main__':
    import os
    import sys
    import maya.cmds as mc
    # Get the directory of the current Maya file (if saved)
    current_file = mc.file(q=True, sn=True)
    current_dir = 'D:/program/lca_rig/assetsystem_sgl/tools/body/armour_tool/python/armour_tool'
    # Add the directory to the system path
    if current_dir and current_dir not in sys.path:
        sys.path.append(current_dir)

    # Now import the rigfnc module
    import armor_generate_functions
    reload(armor_generate_functions)

    run = armor_generate_functions.caocao_armor_setup_module('prefix', (1, 0, 0), (1, 0, 0), size=0.2)
    selected = mc.ls(sl=1)
    if selected:
        for each in selected:
            run.create_armor_shoulder_setup(each)
    else:
        mc.warning('please select the main group of a group of locators')

    #run.create_armor_shoulder_setup('L')
