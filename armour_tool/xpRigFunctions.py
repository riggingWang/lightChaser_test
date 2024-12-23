# -*- coding: utf-8 -*-
#*************************************************************************
#***    External imports.
#*************************************************************************
import maya.cmds as mc
import json
#*************************************************************************
#***    Internal imports.
#*************************************************************************
from assetsystem_sgl.utils.math import maths
from assetsystem_sgl.utils.string import strings
from assetsystem_sgl.utils.maya import curve
from assetsystem_sgl.utils.maya import control_shape
from assetsystem_sgl.utils.maya import utils
from assetsystem_sgl.utils.maya import transform
from assetsystem_sgl.utils.maya import attributes
from assetsystem_sgl.utils.maya import handler
from assetsystem_sgl.utils.maya import component
from assetsystem_sgl.utils.maya import animation
from assetsystem_sgl.modules.config import Config

import xpMathFunctions
reload(xpMathFunctions)

#*************************************************************************


class JointBuilder(object):

    def __init__(self):
        pass
        # self.ikHandle = ikHandle.IkHandle()

    def line_to_joint(self, cvName, jointPrefix, jointSuffix, orientation="xyz", step=1, *args):
        '''
            Usage::
            >>> self.line_to_joint("belly","belly", "jnt", "xyz", 1)
        '''
        mc.select(cl=True)
        # a judgment of curveDegree
        # cvNum = mc.getAttr(cvName + ".spans")
        # cvDegree = mc.getAttr(cvName + ".d")
        # cvNum = cvNum + cvDegree
        cvNum = component.get_component_count(cvName)
        # create joint
        jointList = []
        j = 1
        for i in range(0, cvNum, step):
            cvVertex = cvName + ".cv[" + str(i) + "]"
            jointName = "%s_%s_%s" % (jointPrefix, j, jointSuffix)

            cvJointPos = mc.xform(cvVertex, q=True, ws=True, t=True)
            mc.select(cl=True)
            jointName = mc.joint(p=cvJointPos, n=jointName)
            jointList.append(jointName)
            j += 1

        # set joint orientation
        # set aim and orientation vectors, always yup
        aimDict = {}
        aimDict[orientation[0]] = 1
        aimDict[orientation[1]] = 0
        aimDict[orientation[2]] = 0
        aimVec = (aimDict['x'], aimDict['y'], aimDict['z'])

        orientDict = {}
        orientDict[orientation[0]] = 0
        orientDict[orientation[1]] = 0
        orientDict[orientation[2]] = 1
        orientVec = (orientDict['x'], orientDict['y'], orientDict['z'])

        # orient first joint
        JntAimConstrain = mc.aimConstraint(jointList[1],
                                           jointList[0],
                                           aimVector=aimVec,
                                           upVector=(0, 1, 0),
                                           worldUpType="scene")
        mc.delete(JntAimConstrain)

        rotate = mc.getAttr("%s.rotate" % jointList[0])[0]
        mc.setAttr("%s.jointOrient" %
                   jointList[0], rotate[0], rotate[1], rotate[2], type="float3")
        mc.setAttr("%s.rotate" % jointList[0], 0, 0, 0, type="float3")

        # orient middle joints
        for i in range(1, len(jointList) - 1):
            JntAimConstrain = mc.aimConstraint(jointList[i + 1], jointList[i],
                                               aimVector=aimVec,
                                               upVector=orientVec,
                                               worldUpType="objectrotation",
                                               worldUpVector=orientVec,
                                               worldUpObject=jointList[i - 1])
            mc.delete(JntAimConstrain)
            rotate = mc.getAttr("%s.rotate" % jointList[i])[0]
            mc.setAttr("%s.jointOrient" % jointList[i], rotate[
                0], rotate[1], rotate[2], type="float3")
            mc.setAttr("%s.rotate" % jointList[i], 0, 0, 0, type="float3")

        # parent joints
        for i in range(1, len(jointList)):
            mc.parent(jointList[i], jointList[i - 1], absolute=True)

        # orient last joint
        mc.setAttr("%s.jointOrient" % jointList[-1], 0, 0, 0, type="float3")

        mc.select(jointList[0])
        # print('Successfully created and oriented joint chain. Continuing...')
        return jointList

    def line_to_joint_new(self, cvName, jointPrefix, jointSuffix, aim_vector=[1, 0, 0], up_vector=[0, 1, 0], step=1,
                          *args):
        '''
            Usage::
            >>> self.line_to_joint("belly","belly", "jnt", "xyz", 1)
        '''
        mc.select(cl=True)
        # a judgment of curveDegree
        # cvNum = mc.getAttr(cvName + ".spans")
        # cvDegree = mc.getAttr(cvName + ".d")
        # cvNum = cvNum + cvDegree
        cvNum = component.get_component_count(cvName)
        # create joint
        jointList = []
        j = 1
        for i in range(0, cvNum, step):
            cvVertex = cvName + ".cv[" + str(i) + "]"
            jointName = "%s_%s_%s" % (jointPrefix, j, jointSuffix)

            if not mc.objExists(jointName):
                cvJointPos = mc.xform(cvVertex, q=True, ws=True, t=True)
                mc.select(cl=True)
                jointName = mc.joint(p=cvJointPos, n=jointName)

            jointList.append(jointName)
            j += 1

        # # set joint orientation
        # # set aim and orientation vectors, always yup
        # aimDict = {}
        # aimDict[orientation[0]] = 1
        # aimDict[orientation[1]] = 0
        # aimDict[orientation[2]] = 0
        # aimVec = (aimDict['x'], aimDict['y'], aimDict['z'])

        # orientDict = {}
        # orientDict[orientation[0]] = 0
        # orientDict[orientation[1]] = 0
        # orientDict[orientation[2]] = 1
        # orientVec = (orientDict['x'], orientDict['y'], orientDict['z'])

        # orient first joint
        JntAimConstrain = mc.aimConstraint(jointList[1],
                                           jointList[0],
                                           aimVector=aim_vector,
                                           upVector=up_vector,
                                           worldUpType="scene")
        mc.delete(JntAimConstrain)

        rotate = mc.getAttr("%s.rotate" % jointList[0])[0]
        mc.setAttr("%s.jointOrient" %
                   jointList[0], rotate[0], rotate[1], rotate[2], type="float3")
        mc.setAttr("%s.rotate" % jointList[0], 0, 0, 0, type="float3")

        # orient middle joints
        for i in range(1, len(jointList) - 1):
            JntAimConstrain = mc.aimConstraint(jointList[i + 1], jointList[i],
                                               aimVector=aim_vector,
                                               upVector=up_vector,
                                               worldUpType="objectrotation",
                                               worldUpVector=up_vector,
                                               worldUpObject=jointList[i - 1])
            mc.delete(JntAimConstrain)
            rotate = mc.getAttr("%s.rotate" % jointList[i])[0]
            mc.setAttr("%s.jointOrient" % jointList[i], rotate[
                0], rotate[1], rotate[2], type="float3")
            mc.setAttr("%s.rotate" % jointList[i], 0, 0, 0, type="float3")

        # parent joints
        for i in range(1, len(jointList)):
            # mc.parent(jointList[i], jointList[i - 1], absolute=True)
            transform.parent(jointList[i], jointList[i - 1])

        # orient last joint
        mc.setAttr("%s.jointOrient" % jointList[-1], 0, 0, 0, type="float3")

        mc.select(jointList[0])
        # print('Successfully created and oriented joint chain. Continuing...')
        return jointList

    def list_all_joint(self, start_joint, end_joint=None, *args):
        start_joints = mc.listRelatives(start_joint,
                                        path=True,
                                        allDescendents=True,
                                        type="joint")

        if start_joints:
            start_joints.append(start_joint)
            start_joints.reverse()
        else:
            start_joints = [start_joint]

        if end_joint:
            end_joints = mc.listRelatives(end_joint,
                                          path=True,
                                          allDescendents=True,
                                          type="joint")

            if end_joints:
                for item in end_joints:
                    if item in start_joints:
                        start_joints.remove(item)

        return start_joints

    def locator_to_joint(self, joint, sourceName, targetName):
        mc.select(cl=True)

        jointName = joint.replace(sourceName, targetName)

        if not mc.objExists(jointName):
            jointNode = mc.joint(n=jointName)
        else:
            jointNode = jointName

        try:
            # set joints rotate order
            rotate_order = mc.getAttr("%s.ro" % joint)
            mc.setAttr("%s.ro" % jointNode, rotate_order)

            transform.catch_position(joint, jointNode, 1, 1, 1)
            mc.makeIdentity(jointNode, apply=True, t=0, r=1, s=0)
        except:
            pass

        return jointNode

    def joint_to_joint(self, joints, prefixName, suffixName="jnt", step=1, *args):
        jointList = []
        mc.select(cl=True)
        j = 1
        for i in range(0, len(joints), step):
            # joint name
            jointName = "%s_%s_%s" % (prefixName, j, suffixName)
            if not mc.objExists(jointName):
                jointNode = mc.joint(n=jointName)
            else:
                jointNode = jointName

            # set joints rotate order
            if mc.objExists("%s.ro" % joints[i]):
                rotate_order = mc.getAttr("%s.ro" % joints[i])
                mc.setAttr("%s.ro" % jointNode, rotate_order)

            # catch position
            transform.catch_position(joints[i], jointNode)
            mc.makeIdentity(jointNode, apply=True, t=0, r=1, s=0)

            jointList.append(jointNode)
            j = j + 1

        return jointList

    def duplicate_surface_curves(self, surface, num, brank=True):
        """reference get value
        """
        curves = []
        surface_shape = utils.obj_shape_type(surface, "nurbsSurface")

        max_value = mc.getAttr("%s.minMaxRangeV" % surface_shape)[0][1]

        # get value
        step_value = []
        value = 0
        if num == 1:
            step_value.append(0.5)

        elif brank:
            step = float(max_value) / (num - 1)
            for i in range(0, num):
                step_value.append(value)
                value += step

        else:
            step = float(max_value) / (num + 1)
            for i in range(0, num):
                value += step
                step_value.append(value)

        # set value
        for i in range(0, num):
            nodes = mc.duplicateCurve("%s.v[%s]" % (surface_shape, step_value[i]),
                                      ch=1,
                                      rn=0,
                                      local=0,
                                      name="%s_%s_curve" % (surface, i + 1))
            mc.rename(nodes[1], "%s_%s_curveFromSurfaceIso" % (surface, i))

            curves.append(nodes[0])

        return curves

    def joint_to_num(self, joints, prefix=None, suffix="jnt", count=0):
        """Usage::
            >>> self.joint_to_num(["joint1", "joint2", "joint3", "joint4", "joint5"], count=10)
        """
        joints_dict = {}
        for i, item in enumerate(joints):
            joints_dict[i] = item

        if count == 0:
            count = len(joints)

        # average value
        joints_num = len(joints) - 1
        value = joints_num / float(count - 1)

        start_pos = 0.0
        all_joints = []
        for i in range(0, count):
            start_pos_str = str(start_pos)
            step = int(start_pos_str.split(".")[0])
            offset = float("0.%s" % start_pos_str.split(".")[1])

            start_joint = joints_dict[step]

            # joint name
            joint_name = "%s_%s_%s" % (prefix, i + 1, suffix)
            if not mc.objExists(joint_name):
                # create joint
                mc.select(cl=True)
                joint_node = mc.joint(name=joint_name)
                # mc.delete(mc.parentConstraint(start_joint, joint_node, mo=False))
            else:
                joint_node = joint_name

            # # set joints rotate order
            # if mc.objExists("%s.ro" % start_joint):
            #     rotate_order = mc.getAttr("%s.ro" % start_joint)
            #     mc.setAttr("%s.ro" % joint_node, rotate_order)

            transform.catch_position(start_joint, joint_node)

            if joints_dict.has_key(step + 1):
                end_joint = joints_dict[step + 1]
                axis = self.get_joint_axis(end_joint)
                attr = "t%s" % axis
                joint_length = self.length(start_joint, end_joint)

                # fix 父物体有缩放 2017.11.17
                global_scale = mc.xform(start_joint, q=True, scale=True, ws=True)
                if axis == "x":
                    offset = offset / global_scale[0]
                elif axis == "y":
                    offset = offset / global_scale[1]
                else:
                    offset = offset / global_scale[2]

                if axis:
                    direct = mc.getAttr("%s.%s" % (end_joint, attr))
                    if direct < 0:
                        result = -joint_length * offset
                    else:
                        result = joint_length * offset

                    # 创建临时组，避免父骨骼有缩放值 2017.11.17
                    temp_grp = transform.make_transform("%s_temp_grp" % joint_node)
                    transform.catch_position(joint_node, temp_grp)

                    transform.parent(joint_node, temp_grp)
                    transform.parent(temp_grp, start_joint)
                    # transform.parent(joint_node, start_joint)

                    # set offset
                    mc.setAttr("%s.%s" % (temp_grp, attr), result)
                    mc.parent(joint_node, w=True)
                    mc.delete(temp_grp)

            all_joints.append(joint_node)
            start_pos += value

        # parent all joints
        for i, item in enumerate(all_joints):
            mc.makeIdentity(item, apply=True, t=0, r=1, s=0)
            if i > 0:
                mc.parent(item, all_joints[i - 1])
        return all_joints

    def joint_to_joint_repalce(self, joints, sourceName, targetName, step=1, *args):
        jointList = []
        mc.select(cl=True)
        # j = 1
        for i in range(0, len(joints), step):
            # joint name
            jointName = joints[i].replace(sourceName, targetName)

            if not mc.objExists(jointName):
                jointNode = mc.joint(n=jointName)
            else:
                jointNode = jointName

            try:
                # set joints rotate order
                rotate_order = mc.getAttr("%s.ro" % joints[i])
                mc.setAttr("%s.ro" % jointNode, rotate_order)
                transform.catch_position(joints[i], jointNode)
                mc.makeIdentity(jointNode, apply=True, t=0, r=1, s=0)
            except:
                pass

            jointList.append(jointNode)
            # j = j + 1

        return jointList

    def hide_joint(self, groupName, value=0):
        listJnt = mc.listRelatives(
            groupName, allDescendents=True, type="joint")
        if listJnt != None:
            for item in listJnt:
                if value == 1:
                    mc.setAttr("%s.drawStyle" % item, 0)
                elif value == 0:
                    mc.setAttr("%s.drawStyle" % item, 2)
                else:
                    mc.warning("the value must be off or on")

    def length(self, start_joint, end_joint=None, *args):
        '''
        Get length of specified joint
        @param joint: Joint to query length from
        @type joint: str
        '''
        # Check start_joint
        if not mc.objExists(start_joint):
            raise Exception('Joint "' + start_joint + '" does not exist!')

        # Get child joints
        joints_chain = self.list_all_joint(start_joint, end_joint)

        if not joints_chain:
            return 0.0

        # Get length
        maxLength = 0.0
        for i in range(1, len(joints_chain)):
            pt1 = component.get_position(joints_chain[i - 1])
            pt2 = component.get_position(joints_chain[i])
            # offset = maths.offset_vector(pt1, pt2)
            # length = maths.mag(offset)

            length = maths.distance_between(pt1, pt2)
            maxLength += length

        # float type
        maxLength = float("%.9f" % maxLength)
        # Return result
        return maxLength

    def joint_cube(self, size=0.3):
        mc.select("*_bind")
        list = mc.ls(sl=True)
        for item in list:
            child = self.get_first_child_joint(item)
            axis_vector = (1, 0, 0)
            h = 1

            if child:
                axis = self.get_joint_axis(child)
                if axis == "x":
                    axis_vector = (1, 0, 0)
                elif axis == "y":
                    axis_vector = (0, 1, 0)
                else:
                    axis_vector = (0, 0, 1)
                h = self.length(item)

            cube = mc.polyCube(w=size, h=0.5, d=size, ax=axis_vector)
            transform.catch_position(item, cube[0])
            mc.parent(cube[0], item)

    def get_joint_axis(self, joint):
        '''
        '''
        axis = None
        translate = mc.getAttr("%s.t" % joint)[0]
        tol = 0.0001
        for i in range(0, 3):
            value = translate[i] > tol or translate[i] < (-1 * tol)

            if i == 0 and value:
                axis = "x"
            elif i == 1 and value:
                axis = "y"
            elif i == 2 and value:
                axis = "z"

            # 不可以用默认X轴，否则零距离骨骼不正确
            # else:
            #     mc.warning("The joint joint is too close to the parent joint.\
            #                 Cannot determine the proper axis to segment.")
        return axis

    def get_first_child_joint(self, joint):
        # joints = mc.listRelatives(joint, f=True, c=True, type="joint")
        joints = mc.listRelatives(joint, c=True, type="joint")
        if joints:
            return joints[0]
        else:
            None

    def auto_name(self, prefix, num=1, suffix=None, *args):
        '''auto rename name
        '''
        obj = "%s_%s_%s" % (prefix, num, suffix)
        while mc.objExists(obj):
            obj = "%s_%s_%s" % (prefix, num, suffix)
            num = num + 1
        return obj

    # add volume joint
    # def add_volume_joint(self, driver, driven, axis="x", length=0.1, prefix="", *args):
    def add_volume_joint_drive(self,
                               driver_ctrl,
                               driver,
                               root_joint,
                               attrs=[],
                               *args):
        '''
        # self.add_volume_joint("finA_L_finA_1_bind", [("rotateZ", -60),
        # ("scaleY", 2)],(1,0,0), "")
        '''

        if attrs:
            if not mc.attributeQuery("volume_joints_multi", node=driver, exists=True):
                mc.addAttr(driver,
                           k=False,
                           longName="volume_joints_multi",
                           defaultValue=1,
                           minValue=0,
                           maxValue=2,
                           attributeType="double")

            # set driver key
            for item in attrs:
                # init attributes
                driver_attr = "%s.%s" % (driver_ctrl, item[0][0])
                driver_value = item[0][1]

                mult_node = "%s_drive_multDoubleLinear" % driver
                if not mc.objExists(mult_node):
                    mult_node = mc.createNode("multDoubleLinear",
                                              name=mult_node)

                    mc.connectAttr("%s.volume_joints_multi" % driver,
                                   "%s.input2" % mult_node, f=True)
                    mc.connectAttr(driver_attr,
                                   "%s.input1" % mult_node, f=True)
                driver_attr = "%s.output" % mult_node

                for i in range(1, len(item)):
                    driven_attr = "%s.%s" % (root_joint, item[i][0])
                    driven_value = item[i][1]
                    default_value = mc.attributeQuery(item[i][0],
                                                      node=root_joint,
                                                      listDefault=True)[0]

                    animation.driver_key_obj(driver_attr,
                                             driver_value,
                                             driven_attr,
                                             driven_value)

                    # set default value
                    animation.driver_key_obj(driver_attr,
                                             0,
                                             driven_attr,
                                             default_value)

    def add_volume_joint(self,
                         driver,
                         position=["tx", 0.2],
                         prefix="",
                         *args):
        '''
        # self.add_volume_joint("finA_L_finA_1_bind", [("rotateZ", -60),
        # ("scaleY", 2)],(1,0,0), "")
        '''
        if not prefix:
            prefix = strings.prefix(driver)

        # create start joint
        mc.select(cl=True)
        root_joint = '%s_vol_root_jnt' % prefix
        if mc.objExists(root_joint) == False:
            root_joint = mc.joint(name=root_joint)
            mc.setAttr("%s.drawStyle" % root_joint, 2)
            transform.parent(root_joint, driver)

        # create end joint
        end_joint = '%s_vol_end_jnt' % prefix
        if mc.objExists(end_joint) == False:
            end_joint = mc.joint(name=end_joint)
            transform.parent(end_joint, root_joint)

        # create volumn down joint
        transform.catch_position(driver, root_joint)

        # freeze rotate value
        mc.makeIdentity(root_joint, apply=True, r=1, n=0)

        # set position
        mc.setAttr("%s.%s" % (end_joint, position[0]), position[1])
        # mc.setAttr("%s.segmentScaleCompensate" % root_joint, 0)

        return [root_joint, end_joint]

    def split_joint(self, start_joint, end_joint, prefix_name, suffix_name, num, parent=None, *args):
        '''split joint
        '''
        if not mc.objExists(start_joint):
            raise Exception('Joint ' + start_joint + ' does not exist!')

        if not prefix_name:
            prefix_name = strings.prefix(start_joint)

        # remove number
        prefix_name = strings.prefix(prefix_name)

        joints = []

        # query joint info
        axis = self.get_joint_axis(end_joint)
        attr = "t%s" % axis

        joint_length = self.length(start_joint, end_joint)
        joint_offset = float(joint_length) / (num - 1)

        # create joint
        for i in range(0, num):
            joint_name = "%s_%s_%s" % (prefix_name, i + 1, suffix_name)
            joints.append(joint_name)

            if mc.objExists(joint_name) == False:
                joint_name = mc.duplicate(start_joint,
                                          po=True,
                                          n=joint_name)[0]
                # disconnect message attr
                attributes.dis_connect(joint_name, ["message"])

                # connect rotate order
                mc.connectAttr("%s.ro" % start_joint, "%s.ro" % joint_name, f=True)
            else:
                continue

            # parent chain
            if i > 0:
                transform.parent(joint_name, joints[i - 1])

            value = mc.getAttr("%s.%s" % (end_joint, attr))
            if value > 0:
                mc.setAttr("%s.%s" % (joint_name, attr), joint_offset)
            else:
                mc.setAttr("%s.%s" % (joint_name, attr), -joint_offset)

            # freeze joint
            mc.makeIdentity(joint_name, apply=True, t=0, r=1, s=0)

            # joints.append(joint_name)

        # joints.append(end_joint)

        if parent:
            for item in joints:
                transform.parent(item, parent)
        else:
            transform.parent(end_joint, joints[-1])

        # return joints, start_joint, end_joint
        return joints

    def split_twist_joint(self, start_joint, end_joint, prefix_name, suffix_name, num, parent=None):
        '''split joint
        '''
        if not mc.objExists(start_joint):
            raise Exception('Joint ' + start_joint + ' does not exist!')

        if not prefix_name:
            prefix_name = strings.prefix(start_joint)
        joints = []

        # query joint info
        axis = self.get_joint_axis(end_joint)
        attr = "t%s" % axis

        joint_length = self.length(start_joint, end_joint)
        joint_offset = float(joint_length) / (num - 1)

        # create joint
        joint_pos = 0
        for i in range(1, num + 1):
            joint_name = "%s_%s_%s" % (prefix_name, i, suffix_name)
            if mc.objExists(joint_name) == False:
                joint_name = mc.duplicate(start_joint,
                                          po=True,
                                          n=joint_name)[0]

            # parent chain
            if i == 1:
                transform.parent(joint_name, start_joint)
                mc.setAttr("%s.%s" % (joint_name, attr), 0)
            else:
                transform.parent(joint_name, joints[i - 2])

                value = mc.getAttr("%s.%s" % (end_joint, attr))
                if value > 0:
                    mc.setAttr("%s.%s" % (joint_name, attr), joint_offset)
                else:
                    mc.setAttr("%s.%s" % (joint_name, attr), -joint_offset)

            # mc.setAttr("%s.%s" % (joint_name, attr), joint_offset)
            # freeze joint
            # mc.makeIdentity(joint_name, apply=True, t=0, r=1, s=0)
            joints.append(joint_name)

        if parent:
            for item in joints:
                transform.parent(item, parent)
        # else:
        #     if end_joint:
        #         transform.parent(end_joint, joints[-1])

        return joints


class ControlBuilder(object):

    def __init__(self):
        self.overrideId = {'_L_': 6, '_R_': 13, '_M_': 17}
        self.controls_type = ['box', 'square', 'circle', 'sphere', "circleFlower",
                              "locator", "locatorArrow", "singleArrow", "root", "arrow", "cross",
                              "circle_aim", "circle_roll", "circle_half", "circle_rectangle",
                              "fourArrowOut", "fourArrowIn", "arcArrow", "arcArrowDn",
                              "fourArcArrow", "squareArrow", "coordinatesOrient",
                              "createRawLocalAxesInfo", "half_axis_arow", "half_circle_arow",
                              "two_arrow", "up_two_arrow", "reflect_two_arrow",
                              "createRawSegmentCurve", "createRawOrientation", "rhombus",
                              "snake", "eye", "text", "curve", "settingCtrl_Leg_L", "settingCtrl_Leg_R",
                              "settingCtrl_Arm_L", "settingCtrl_Arm_R", "New_Global_ctrl", "new_Pole_IK_Ctrl",
                              "new_spine_M_root_ctrl", "new_FK_Ctrl_world", "spine_fk_ctrl", "finger_fk_ctrl",
                              "finger_fk01_ctrl"]
        self.control_shape = control_shape

    def create(self, ctrl_type, name, color=0, r=1, aim_vector=[0, 1, 0], text="", *args):
        '''
        self.create(box, "hand_IK_ctrl", 6, 1, [1, 0, 0])
        @param ctrl_type: control type
        @type ctrl_type: string
        @param name: control name
        @type name: string
        @param color: control shape color
        @type color: int
        @param r: the controls radius
        @type r: int
        @param aim_vector: controls axis
        @type aim_vector: list
        @param text: create text curves
        @type text: string
        '''
        # Check name
        nameInd = 1
        origname = name
        while mc.objExists(name):
            name = origname + str(nameInd)
            nameInd += 1

        # Check Control Type
        if not self.controls_type.count(ctrl_type):
            raise Exception(
                'Unsupported control shape type("' + ctrl_type + '")!!')

        # Create Control
        control = ''
        if ctrl_type == 'box':
            control = self.control_shape.box(name)
        elif ctrl_type == 'square':
            control = self.control_shape.square(name)
        elif ctrl_type == 'circle':
            control = self.control_shape.circle(name, axis=aim_vector)
        elif ctrl_type == 'sphere':
            control = self.control_shape.sphere(name)
        elif ctrl_type == 'circleFlower':
            control = self.control_shape.circleFlower(name, axis=aim_vector)
        elif ctrl_type == 'locator':
            control = self.control_shape.locator(name)
        elif ctrl_type == 'cross':
            control = self.control_shape.cross(name)
        elif ctrl_type == 'circle_aim':
            control = self.control_shape.circle_aim(name)
        elif ctrl_type == 'circle_roll':
            control = self.control_shape.circle_roll(name)
        elif ctrl_type == 'circle_rectangle':
            control = self.control_shape.circle_rectangle(name)
        elif ctrl_type == 'circle_half':
            control = self.control_shape.circle_half(name)

        elif ctrl_type == 'locatorArrow':
            control = self.control_shape.locatorArrow(name)
        elif ctrl_type == 'root':
            control = self.control_shape.root(name)
        elif ctrl_type == 'arrow':
            control = self.control_shape.arrow(name)

        elif ctrl_type == 'fourArrowOut':
            control = self.control_shape.fourArrowOut(name)
        elif ctrl_type == 'fourArrowIn':
            control = self.control_shape.fourArrowIn(name)
        elif ctrl_type == 'arcArrow':
            control = self.control_shape.arcArrow(name)
        elif ctrl_type == 'arcArrowDn':
            control = self.control_shape.arcArrowDn(name)

        elif ctrl_type == 'two_arrow':
            control = self.control_shape.two_arrow(name)
        elif ctrl_type == 'up_two_arrow':
            control = self.control_shape.up_two_arrow(name)
        elif ctrl_type == 'reflect_two_arrow':
            control = self.control_shape.reflect_two_arrow(name)

        elif ctrl_type == 'fourArcArrow':
            control = self.control_shape.fourArcArrow(name)
        elif ctrl_type == 'squareArrow':
            control = self.control_shape.squareArrow(name)
        elif ctrl_type == 'singleArrow':
            control = self.control_shape.singleArrow(name)
        elif ctrl_type == 'coordinatesOrient':
            control = self.control_shape.coordinates_orient(name)

        elif ctrl_type == 'createRawOrientation':
            control = self.control_shape.createRawOrientation(name)

        elif ctrl_type == 'createRawLocalAxesInfo':
            control = self.control_shape.createRawLocalAxesInfo(name)

        elif ctrl_type == 'half_axis_arow':
            control = self.control_shape.half_axis_arow(name)

        elif ctrl_type == 'half_circle_arow':
            control = self.control_shape.half_circle_arow(name)

        elif ctrl_type == 'rhombus':
            control = self.control_shape.rhombus(name)

        elif ctrl_type == 'snake':
            control = self.control_shape.snake(name)

        elif ctrl_type == 'text':
            control = self.control_shape.text(name, text, True)
        # cjw
        elif ctrl_type == 'settingCtrl_Leg_L':
            control = self.control_shape.settingCtrl_Leg_L(name)
        elif ctrl_type == 'settingCtrl_Leg_R':
            control = self.control_shape.settingCtrl_Leg_R(name)
        elif ctrl_type == 'settingCtrl_Arm_L':
            control = self.control_shape.settingCtrl_Arm_L(name)
        elif ctrl_type == 'settingCtrl_Arm_R':
            control = self.control_shape.settingCtrl_Arm_R(name)
        elif ctrl_type == 'New_Global_ctrl':
            control = self.control_shape.New_Global_ctrl(name)
        elif ctrl_type == 'new_Pole_IK_Ctrl':
            control = self.control_shape.new_Pole_IK_Ctrl(name)
        elif ctrl_type == 'new_spine_M_root_ctrl':
            control = self.control_shape.new_spine_M_root_ctrl(name, axis=aim_vector)
        elif ctrl_type == 'new_FK_Ctrl_world':
            control = self.control_shape.new_FK_Ctrl_world(name, axis=aim_vector)
        elif ctrl_type == 'spine_fk_ctrl':
            control = self.control_shape.spine_fk_ctrl(name, axis=aim_vector)
        elif ctrl_type == 'finger_fk_ctrl':
            control = self.control_shape.finger_fk_ctrl(name, axis=aim_vector)
        elif ctrl_type == 'finger_fk01_ctrl':
            control = self.control_shape.finger_fk01_ctrl(name, axis=aim_vector)
        else:
            raise Exception(
                'Unsupported control shape type("' + ctrl_type + '")!!')

        # rename curve shape
        utils.rename_shape(control)

        # Color it
        for item in self.overrideId:
            if control.find(item) == 0:
                curve.color_shape(control, self.overrideId[item])
        if color != 0:
            curve.color_shape(control, color)

        curve.scale(control, r, r, r)

        # fix shape axis
        if ctrl_type == "square" or ctrl_type == "rhombus":
            axis = strings.list_to_axis(aim_vector)
            if axis == "x":
                curve.rotate(control, 0, 0, 90)

            elif axis == "y":
                curve.rotate(control, 0, 90, 0)

            elif axis == "z":
                curve.rotate(control, 90, 0, 0)

        # Return result
        # return str(control)
        return control

    def replace_shape(self, ctrl, ctrl_type, r=1):
        shape = utils.obj_shape_type(ctrl, "nurbsCurve")
        color = mc.getAttr("%s.overrideColor" % ctrl)

        if shape:
            color = mc.getAttr("%s.overrideColor" % shape)
            mc.delete(shape)

        ctrl_shape = self.create(ctrl_type,
                                 ctrl)

        curve.add_shapes(ctrl, ctrl_shape)
        utils.rename_shape(ctrl)

        # set control color
        curve.color_shape(ctrl, color)

        curve.scale(ctrl, r, r, r)

    def create_fk(self,
                  object,
                  ctrl_name,
                  ctrl_type,
                  color,
                  type="parent",
                  r=1,
                  axis=(1, 0, 0),
                  *args):
        # ctrl name
        ctrl = self.create(ctrl_type, ctrl_name, color, r, axis)

        rotate_order = mc.getAttr("%s.ro" % object)
        mc.setAttr("%s.ro" % ctrl, rotate_order)

        # catch control postion
        transform.catch_position(object, ctrl)

        transform.make_group_zero(ctrl)

        # parent control
        if type == "parent":
            transform.parent(object, ctrl)

        elif type == "joint":
            ctrl = curve.joint_to_control(ctrl, object)

        elif type == "parentConstraint":
            mc.parentConstraint(ctrl, object, mo=True, weight=1)

        elif type == "pointConstraint":
            mc.pointConstraint(ctrl, object, mo=True, weight=1)

        elif type == "orientConstraint":
            mc.orientConstraint(ctrl, object, mo=True, weight=1)

        else:
            mc.warning("unknow type")

        return ctrl

    def ikfk_chain(self,
                   joints,
                   prefixName,
                   suffixName,
                   ctrl_type="new_FK_Ctrl_world",
                   color=17,
                   type="parent",
                   r=1,
                   aim_vector=(1, 0, 0),
                   *args):
        '''
        self.ikfk_chain([joint1, joint2, joint3], "arm_L", "ctrl")
        @param type:joint, parent, parentConstraint, pointConstraint, orientConstraint
        @type:string
        '''
        joints = strings.convert_list(joints)
        # if isinstance(joints, list):
        ctrls = []
        for i, item in enumerate(joints):
            # ctrl name
            j = i + 1
            ctrl_name = "%s_%s_%s" % (prefixName, j, suffixName)

            # create ctrl
            ctrl = self.create_fk(item,
                                  ctrl_name,
                                  ctrl_type,
                                  color,
                                  type,
                                  r,
                                  aim_vector)

            # parent
            if i > 0:
                ctrl_grp = mc.listRelatives(ctrl, parent=True)
                transform.parent(ctrl_grp, ctrls[i - 1])

            ctrls.append(ctrl)
        return ctrls

    def ikfk_chain_replace(self,
                           joints,
                           search_name,
                           replace_name,
                           ctrl_type="new_FK_Ctrl_world",
                           color=17,
                           type="parent",
                           r=1,
                           aim_vector=(1, 0, 0),
                           *args):
        '''
        确保单轴向位移数值唯一
        self.ikfk_chain([joint1, joint2, joint3], "arm_L", "ctrl")
        @param type:joint, parent, parentConstraint, pointConstraint, orientConstraint
        @type:string
        '''
        joints = strings.convert_list(joints)
        # if isinstance(joints, list):
        ctrls = []
        for i, item in enumerate(joints):
            # ctrl name
            ctrl_name = item.replace(search_name, replace_name)

            # create ctrl
            ctrl = self.create_fk(item,
                                  ctrl_name,
                                  ctrl_type,
                                  color,
                                  type,
                                  r,
                                  aim_vector)

            # parent
            if i > 0:
                ctrl_grp = mc.listRelatives(ctrl, parent=True)
                transform.parent(ctrl_grp, ctrls[i - 1])

            # # make multiply group é˜²æ­¢å±žæ€§è¢«é”ä½
            # self.make_group_multi(ctrl, False)

            ctrls.append(ctrl)
        return ctrls

    def ikfk_chain_joints(self,
                          joints,
                          search_name,
                          replace_name,
                          ctrl_type="new_FK_Ctrl_world",
                          color=17,
                          r=1,
                          axis=(1, 0, 0),
                          *args):
        '''
        self.ikfk_chain_joints([joint1, joint2, joint3], "jnt", "ctrl")
        '''
        joints = strings.convert_list(joints)

        ctrlList = []
        for i, item in enumerate(joints):
            # ctrl name
            ctrl_name = item.replace(search_name, replace_name)

            # create ctrl
            ctrl = self.create(ctrl_type, ctrl_name, color, r, axis)
            ctrl = curve.joint_to_control(ctrl, item)

            # group
            if i == 0:
                transform.make_group_zero(ctrl, orient=1)

            else:
                obj_group = mc.group(n="%s_ofs" % ctrl, em=True)
                transform.parent(obj_group, ctrlList[i - 1])

                # transform.catch_position(ctrl, obj_group, orient=False)
                mc.delete(mc.parentConstraint(ctrl, obj_group))
                # same as parent's rotate
                # mc.setAttr("%s.r" % obj_group, 0, 0, 0, type="double3")
                transform.parent(ctrl, obj_group)

            # make multiply group
            self.make_group_multi_base(ctrl, False)
            ctrlList.append(ctrl)

        return ctrlList

    def make_group_multi_base(self, ctrl, orient=True):
        # get prefix
        prefix = strings.prefix(ctrl)

        # make mult group
        base_group = self.make_group_multi(ctrl, orient)

        # base transform
        base = self.make_base(ctrl)

        return base_group, base

    def make_group_multi(self, ctrl, orient=True):
        prefix = strings.prefix(ctrl)
        suffix = ctrl.split("_")[-1]

        all_parent = ["%s_ofs" % suffix,
                      "%s_con" % suffix,
                      "%s_drv" % suffix,
                      "sec_%s" % suffix,
                      "pri_%s" % suffix]

        base_group = None
        # parent transform
        for item in all_parent:
            name = "%s_%s" % (prefix, item)
            if not mc.objExists(name):
                node = transform.make_group_zero(ctrl, item, orient=orient)
                name = mc.rename(node, name)

                if item.endswith("_ofs") or item.endswith("_con") or item.endswith("_drv"):
                    attributes.lock_hide_attrs(name,
                                               "v",
                                               keyable=False,
                                               lock=True)
                else:
                    attributes.lock_hide_attrs(name,
                                               "s",
                                               "v",
                                               keyable=False,
                                               lock=True)

            if item == all_parent[0]:
                base_group = name
        return base_group

    def make_base(self, ctrl):
        # get prefix
        prefix = strings.prefix(ctrl)

        # base transform
        base = "%s_base" % prefix
        if not mc.objExists(base):
            base = mc.createNode("transform", name=base)
            transform.catch_position(ctrl, base)
            transform.parent(base, ctrl)
            mc.connectAttr("%s.ro" % ctrl, "%s.ro" % base, f=True)
            mc.reorder(base, r=True)

        return base

    def make_pivot(self, ctrl):
        prefix = strings.prefix(ctrl)
        suffix = ctrl.split("_")[-1]

        # povit control
        name = "%s_piv_%s" % (prefix, suffix)
        if not mc.objExists(name):
            mc.addAttr(ctrl,
                       ln="povit_vis",
                       attributeType='long',
                       min=0,
                       max=1,
                       k=False)
            mc.setAttr("%s.povit_vis" % ctrl, cb=True)

            node = self.create("createRawLocalAxesInfo", name)
            transform.catch_position(ctrl, node)
            transform.parent(node, ctrl)

            mc.connectAttr("%s.povit_vis" % ctrl, "%s.v" % node, f=True)

            mc.connectAttr("%s.translate" % node,
                           "%s.rotatePivot" % ctrl, f=True)
            mc.connectAttr("%s.translate" % node,
                           "%s.scalePivot" % ctrl, f=True)

    def adv_aim_constraint(self,
                           prefix_name=None,
                           root_ctrl=None,
                           aim_ctrl=None,
                           parent_aim_ctrl=None,
                           parent_aim_up_ctrl=None,
                           aim_vector=None,
                           up_vector=None,
                           up_value=0.1):
        '''advance aim constraint
        '''
        if root_ctrl == None:
            root_ctrl = "%s_guide" % prefix_name
            if not mc.objExists(root_ctrl):
                root_ctrl = self.create("locator",
                                        root_ctrl,
                                        0,
                                        0.5)
                # root_ctrl = mc.spaceLocator(n="%s_guide" % prefix_name)[0]
                mc.setAttr("%s.displayHandle" % root_ctrl, 1)

        if aim_ctrl == None:
            aim_ctrl = "%s_guide_aim_ctrl" % prefix_name
            if not mc.objExists(aim_ctrl):
                aim_ctrl = self.create("coordinatesOrient",
                                       aim_ctrl,
                                       0,
                                       0.5)
                transform.parent(aim_ctrl, root_ctrl)

        # create aim up locator
        if aim_vector:
            aim_up_ctrl = "%s_guide_up_loc" % prefix_name
            if not mc.objExists(aim_up_ctrl):
                aim_up_ctrl = mc.spaceLocator(n=aim_up_ctrl)[0]
                axis = strings.list_to_axis(up_vector)
                mc.setAttr("%s.t%s" % (aim_up_ctrl, axis), up_value)

                mc.setAttr("%s.template" % aim_up_ctrl, 1)
                mc.setAttr("%s.v" % aim_up_ctrl, 0)

                # to the list of assignments
                transform.parent(aim_up_ctrl, root_ctrl)

            # orient
            if parent_aim_ctrl and parent_aim_up_ctrl:
                # the aim loc is created in order to unify the joint axis

                mc.aimConstraint(aim_ctrl,
                                 parent_aim_ctrl,
                                 aimVector=aim_vector,
                                 upVector=up_vector,
                                 worldUpType="object",
                                 worldUpObject=parent_aim_up_ctrl)

            return root_ctrl, aim_ctrl, aim_up_ctrl

        else:
            return root_ctrl, aim_ctrl

    def aim_constraint(self,
                       prefix_name=None,
                       source_aim_ctrl=None,
                       target_aim_ctrl=None,
                       aim_vector=None,
                       up_vector=None,
                       up_value=0.1):
        '''advance aim constraint
        '''
        if source_aim_ctrl == None:
            source_aim_ctrl = "%s_guide_aim_ctrl" % prefix_name
            if not mc.objExists(source_aim_ctrl):
                source_aim_ctrl = self.create("coordinatesOrient",
                                              source_aim_ctrl,
                                              0,
                                              0.5)

        # create aim up locator
        aim_up_ctrl = "%s_guide_up_loc" % prefix_name
        if not mc.objExists(aim_up_ctrl):
            aim_up_ctrl = mc.spaceLocator(n=aim_up_ctrl)[0]

            mc.setAttr("%s.template" % aim_up_ctrl, 1)
            mc.setAttr("%s.v" % aim_up_ctrl, 0)

            # catch position
            transform.catch_position(target_aim_ctrl, aim_up_ctrl)
            transform.make_group_zero(aim_up_ctrl)

            axis = strings.list_to_axis(up_vector)
            mc.setAttr("%s.t%s" % (aim_up_ctrl, axis), up_value)

        # orient
        mc.aimConstraint(source_aim_ctrl,
                         target_aim_ctrl,
                         aimVector=aim_vector,
                         upVector=up_vector,
                         worldUpType="object",
                         worldUpObject=aim_up_ctrl,
                         mo=True)
        return aim_up_ctrl

    @handler.undo_info
    def connect_proxy_controls(self, main_ctrl, suffix="facial_origin"):
        target_ctrls = mc.duplicate(main_ctrl, rc=True, ic=True)
        for item in target_ctrls:
            # rename
            if mc.objExists(item[0:-1]):
                # delete duplicate bind
                if mc.objExists(item):
                    if item.endswith("_bind1"):
                        mc.delete(item)

                if mc.objExists(item):
                    source = mc.rename(
                        item[0:-1], "%s__%s" % (item[0:-1], suffix))
                    target = mc.rename(item, item[0:-1])

                    # set hide
                    if source.endswith("_ctrl__%s" % suffix):
                        shapes = mc.listRelatives(
                            source, c=True, type="nurbsCurve")
                        if shapes:
                            attributes.dis_connect_source(shapes[0], "v")
                            mc.setAttr("%s.v" % shapes[0], 0)

                    elif target.endswith("_ctrl_ofs") or \
                            target.endswith("_ctrl_con") or \
                            target.endswith("_ctrl_drv"):
                        attributes.connect_attr_mult(
                            target, source, "t", "r", "s")

                    if target.endswith("_ctrl"):
                        attributes.connect_attr_mult(
                            target, source, "t", "r", "s")

                        user_attrs = mc.listAttr(source, ud=True)
                        if user_attrs:
                            for attr in user_attrs:
                                lock = mc.getAttr(
                                    "%s.%s" % (source, attr), lock=True)
                                if lock:
                                    user_attrs.remove(attr)

                                if attr == "lockInfluenceWeights":
                                    user_attrs.remove(attr)

                            attributes.copy_attr_list(source,
                                                      target,
                                                      True,
                                                      False,
                                                      user_attrs)

        # parent
        proxy_grp = "%s__facial_origin" % main_ctrl
        if mc.objExists(proxy_grp):
            mc.setAttr("%s.inheritsTransform" % proxy_grp, 0)

            if main_ctrl.endswith("controls_grp"):
                rig_grp = main_ctrl.replace("controls_grp", "rig_grp")
                if mc.objExists(rig_grp):
                    transform.parent(proxy_grp, rig_grp)

            return proxy_grp

    def connect_proxy_joints(self, joints, object_grp, suffix):
        # proxy
        connect_joints = self.joint_chain.joint_to_joint_repalce(joints,
                                                                 "bind",
                                                                 "connect_jnt",
                                                                 1)
        connect_joints_grp = transform.make_group_zero(connect_joints[0])
        mc.parent(connect_joints_grp, self.rig_grp)

        if self.joint_count > self.fk_controls_count + 1:
            self.ribbon_chain.fk_joints_constraint("%s_surface" % self.prefix_name,
                                                   self.fk_controls,
                                                   connect_joints,
                                                   2)

        else:
            for i, item in enumerate(self.fk_controls):
                mc.parentConstraint(item, connect_joints[i])

        # parent self.module_root_jnt
        if mc.objExists(self.module_root_jnt):
            skin_joints_grp = transform.make_group_zero(self.skin_joints[0][0])
            transform.parent(skin_joints_grp,
                             self.module_root_jnt)

        # add stretch
        self.__lca_add_stretch(self.fk_controls[0],
                               self.fk_controls,
                               connect_joints)

        for i, item in enumerate(connect_joints):
            attributes.connect_attr_mult(
                item, self.skin_joints[0][i], "t", "r", "s", "ro")

        mc.parentConstraint(self.controls_grp,
                            connect_joints_grp,
                            weight=True,
                            mo=True)

        target_ctrls = mc.duplicate(object_grp, rc=True, un=True)
        for item in target_ctrls:

            # rename
            source = mc.rename(item[0:-1], "%s__%s" % (item[0:-1], suffix))
            target = mc.rename(item, item[0:-1])

            # set hide
            if source.endswith("_ctrl__%s" % suffix):
                shapes = mc.listRelatives(source, c=True, type="nurbsCurve")
                if shapes:
                    attributes.dis_connect_source(shapes[0], "v")
                    mc.setAttr("%s.v" % shapes[0], 0)

            # self connections
            attrs = ["t", "tx", 'ty', "tz", "r", "rx", "ry", "rz", "ro"]
            for i_attr in attrs:
                if mc.objExists("%s.%s" % (source, i_attr)):
                    # get lock
                    # lock = mc.getAttr("%s.%s" % (source, i_attr), lock=True)
                    source_attrs = mc.listConnections(
                        "%s.%s" % (source, i_attr), s=True, d=False, p=True)
                    if source_attrs:
                        target_attrs = source_attrs[0].split("__%s." % suffix)
                        # print source_attrs, target_attrs, target
                        # mc.connectAttr("%s.%s" % (target_attrs[0], target_attrs[1]),
                        #                 "%s.%s" % (target, i_attr), f=True)
                        # attributes.connect_attr_mult(target_attrs, source, i_attr)

        # parent
        proxy_grp = "%s__facial_origin" % object_grp
        if mc.objExists(proxy_grp):
            transform.parent(proxy_grp, self.rig_grp)


class BaseSetup(Config):
    def __init__(self, guide_module):
        super(BaseSetup, self).__init__()
        """ Initialize the module class.
        """
        # init module
        self.guide_module = guide_module

        # init args
        self.main_rig = "rig"

        self.main_controls_grp = "anim_controls_grp"
        self.main_skeletons_grp = "anim_skeletons_grp"
        self.main_modules_grp = "anim_modules_grp"
        self.main_guides_grp = "anim_guides_grp"
        self.world_space_grp = "world_space_grp"

        self.global_ctrl = "global_ctrl"
        self.root_ctrl = "root_ctrl"

        # defining variables:
        # self.set_up = True
        self.prefix_name = None
        self.module_type = None
        self.module_name = None
        self.module_side = None
        self.joint_num = None
        self.guide_joints = []
        self.skin_joints = []

        # init
        self.joint_chain = JointBuilder()
        self.control_builder = ControlBuilder()
        self.curve = curve
        self.string = strings
        # get guide info
        # self.get_guide_info()

    def load_guide(self, guide):
        self.guide_module = guide
        self.get_guide_info()

    def get_guide_attributes(self, guide):
        attrs = {}
        user_attrs = mc.listAttr(guide, ud=True)
        if user_attrs == None:
            return attrs

        for item in user_attrs:
            type = mc.getAttr("%s.%s" % (guide, item), type=True)

            if type == "enum":
                value = mc.getAttr("%s.%s" % (guide, item), asString=True)

            elif type == "message":
                continue

            else:
                value = mc.getAttr("%s.%s" % (guide, item))

            attrs[item] = value
        return attrs

    def get_guide_info(self):
        '''
        get guide all info
        '''
        if not mc.objExists(self.guide_module):
            return

        self.attrs = self.get_guide_attributes(self.guide_module)

        self.module_type = self.attrs["module_type"]
        self.module_name = self.attrs["module_name"]
        # self.set_up = self.attrs["setup"]
        # print "attr setup of %s is %s" % (self.module_name, self.set_up)

        if self.attrs.has_key("aim_vector"):
            aim_vector = self.attrs["aim_vector"]
            self.aim_vector = strings.str_to_long3(aim_vector)

        if self.attrs.has_key("up_vector"):
            up_vector = self.attrs["up_vector"]
            self.up_vector = strings.str_to_long3(up_vector)

        if self.attrs.has_key("joint_num"):
            self.joint_num = self.attrs["joint_num"]

        # init self.prefix_name
        self.prefix_name = self.module_name

        if self.attrs.has_key("module_side"):
            self.module_side = self.attrs["module_side"]
            if self.module_side:
                self.prefix_name = "%s_%s" % (
                    self.prefix_name, self.module_side)

        if self.attrs.has_key("module_part"):
            self.module_part = self.attrs["module_part"]
            if self.module_part:
                self.prefix_name = "%s_%s" % (
                    self.prefix_name, self.module_part)

        # get global info
        self.char_name = "char"
        self.global_size = 1

        if mc.objExists("guide_global_ctrl"):
            self.global_size = mc.getAttr("guide_global_ctrl.sx")
            self.char_name = mc.getAttr("guide_global_ctrl.char_name")

        if mc.objExists("%s_guide" % self.prefix_name):
            module_size = mc.getAttr("%s_guide.sx" % self.prefix_name)
            self.global_size = self.global_size * module_size

        if mc.objExists("%s_guide_plane" % self.prefix_name):
            module_size = mc.getAttr("%s_guide_plane.sx" % self.prefix_name)
            self.global_size = self.global_size * module_size

        if self.attrs.has_key("global_size"):
            global_size = mc.getAttr("%s.global_size" % self.guide_module)
            if global_size != 1:
                self.global_size = global_size

        if self.attrs.has_key("global_space"):
            self.global_space = mc.getAttr("%s.global_space" % self.guide_module)

        self.module_root_jnt = "%s_root_bind" % self.prefix_name

        self.__get_guide_joints()
        self.__get_skin_joints()

    def get_guide_value(self, guide, attr, default=1):
        if mc.objExists("%s.%s" % (guide, attr)):
            value = mc.getAttr("%s.%s" % (guide, attr))
        else:
            value = default

        return value

    def __get_guide_joints(self):
        '''
        get guide joints
        '''
        self.guide_joints = []
        guide_joints = []

        if mc.objExists("%s.guide_connection" % self.guide_module):
            guide_joints = mc.listConnections("%s.guide_connection" % self.guide_module,
                                              s=True, d=False)

        if guide_joints:
            for item in guide_joints:
                joints = attributes.get_message(item, "connection")
                self.guide_joints.append(joints)

    def __get_skin_joints(self):
        '''get all joints
        '''
        # get skin joints
        self.skin_joints = []
        skin_joints = []

        if mc.objExists("%s.skin_connection" % self.guide_module):
            skin_joints = mc.listConnections("%s.skin_connection" % self.guide_module,
                                             s=True, d=False)

            if skin_joints:
                for item in skin_joints:
                    joints = attributes.get_message(item, "connection")
                    self.skin_joints.append(joints)

    def get_twist_joints(self, skin_joints):
        '''
        get skin joints
        '''
        self.twist_joints = []
        twist_joints = []
        for item in skin_joints:
            if mc.objExists("%s.twist" % item):
                twist_joints = attributes.get_message(item, "twist")

                if twist_joints:
                    self.twist_joints.append(twist_joints)

        return self.twist_joints

    def __module_setup(self):
        '''
        create module group:
        '''
        self.rig_grp = transform.make_transform("%s_rig_grp" % self.prefix_name,
                                                self.main_modules_grp)

        # create controls group
        self.controls_grp = transform.make_transform("%s_controls_grp" % self.prefix_name,
                                                     self.root_ctrl)
        self.info_grp = transform.make_transform("%s_module_info" % self.prefix_name,
                                                 self.rig_grp)

        # create rig group
        self.deformation_grp = transform.make_transform("%s_deformation_grp" % self.prefix_name,
                                                        self.rig_grp)
        self.components_grp = transform.make_transform("%s_components_grp" % self.prefix_name,
                                                       self.rig_grp)

        if not mc.objExists("%s.global_scale" % self.components_grp):
            mc.addAttr(self.components_grp,
                       ln="global_scale",
                       at="double",
                       min=0.001,
                       dv=1,
                       keyable=False)

        # parent
        transform.parent(self.components_grp, self.controls_grp)
        mc.setAttr("%s.v" % self.components_grp, 0)

        # global scale
        if mc.objExists(self.global_ctrl):
            if mc.attributeQuery("global_scale", node=self.global_ctrl, exists=True):
                attributes.connect_attr("%s.global_scale" % self.global_ctrl,
                                        "%s.global_scale" % self.components_grp)
            else:
                attributes.connect_attr("%s.sx" % self.global_ctrl,
                                        "%s.global_scale" % self.components_grp)
                # constraint
                # mc.parentConstraint(
                #     self.controls_grp, self.components_grp, weight=True, mo=False)
                # mc.scaleConstraint(
                #     self.controls_grp, self.components_grp, weight=True, mo=False)

                # mc.parentConstraint(
                #     self.controls_grp, self.stats_grp, weight=True, mo=True)
                # mc.scaleConstraint(
                #     self.controls_grp, self.stats_grp, weight=True, mo=True)

    def __connect_message(self):
        if self.controls_grp:
            attributes.add_message_attr(self.info_grp,
                                        self.controls_grp, "parent", False)

        if self.skin_joints:
            attributes.add_message_attr(self.info_grp,
                                        self.skin_joints[0][0], "bind", True)
        if self.guide_module:
            attributes.add_message_attr(self.info_grp,
                                        self.guide_module, "module_info", True)

        user_attrs = ["module_name", "module_type", "module_side",
                      "module_part", "aim_vector", "up_vector"]
        # user_attrs = mc.listAttr(self.guide_module, ud=True)
        attributes.copy_attr_list(self.guide_module,
                                  self.info_grp,
                                  False,
                                  False,
                                  self.guide_attrs)

        mc.setAttr("%s.guide_base" % self.guide_module, 1)

        if not mc.attributeQuery("linked", node=self.info_grp, exists=True):
            mc.addAttr(self.info_grp, ln="linked", attributeType="bool", keyable=True)
            mc.setAttr("%s.linked" % self.info_grp, False)
        else:
            mc.setAttr("%s.linked" % self.info_grp, False)

    @handler.undo_info
    def _create_joint(self, components):
        # super(BaseSetup, self).create_main_control()

        # create skin joints
        joints_temp = self.joint_chain.joint_to_joint_repalce(
            components, "guide_jnt", "bind", 1)

        # rename skin joints
        joints = []
        for i, item in enumerate(joints_temp):
            name = mc.getAttr("%s.name" % components[i])
            joint_name = "%s_%s_bind" % (self.prefix_name, name)

            if item != joint_name:
                joint_name = mc.rename(item, joint_name)

            joints.append(joint_name)

            # connect information for joints
            if i > 0:
                attributes.add_message_attr(joints[i - 1],
                                            joints[i],
                                            "connection",
                                            False)

        # connect information for self.guide_module
        attributes.add_message_attr(self.guide_module,
                                    joints[0],
                                    "skin_connection",
                                    True)

        self.skin_joints.append(joints)

    def _create_twist_joints(self, start_joint, end_joint, num):
        twist_joints = self.joint_chain.split_joint(start_joint,
                                                    end_joint,
                                                    "",
                                                    "bind",
                                                    num)
        # twist_joints = self.joint_chain.split_twist_joint(start_joint,
        #                                                   end_joint,
        #                                                   "",
        #                                                   "bind",
        #                                                   num)

        # add message attribute
        for i, item in enumerate(twist_joints):
            if i > 0:
                attributes.add_message_attr(twist_joints[i - 1],
                                            item,
                                            "twist",
                                            False)

        return twist_joints

    @handler.undo_info
    def _create_setup(self):
        self.get_guide_info()
        # super(BaseSetup, self).create_main_control()
        self.__module_setup()
        self.__connect_message()

def createGrp(groupName, parent = ''):
    if not mc.objExists(groupName):
        if parent:
            grpName = mc.group(empty = True, n = groupName, p=parent)
            return grpName
        else:
            grpName = mc.group(empty = True, n = groupName, w=1)
            return grpName
    else:
        if parent:
            transform.parent(groupName, parent)
            return groupName
        else:
            return groupName

def createNode(nodeName, nodeType):
    if not mc.objExists(nodeName):
        ikCurve_info = mc.createNode(nodeType, name=nodeName)
    else:
        ikCurve_info = nodeName
    return ikCurve_info

def writeString(nodeName, attrName, strlist):
    if not mc.attributeQuery(attrName, node=nodeName, exists=True):
        mc.addAttr(nodeName, longName=attrName, dataType="string")
    mc.setAttr("{}.{}".format(nodeName, attrName), json.dumps(strlist), type="string")

def groupIsGenerated(grpName, parent='', attrName='isGenerated', finished=False):
    if not mc.objExists('global_ctrl'):
        mc.error(
            ' ****** - error ! - ******  missing global ctrl, please import character first'.format(
                grpName))
    if not mc.objExists('root_ctrl'):
        mc.error(
            ' ****** - error ! - ******  missing root ctrl, please import character first'.format(
                grpName))
    if finished:
        mc.setAttr(grpName + "." + attrName, 1)
        print(' ****** - note - ******  [  {}  ] generated successfully '.format(grpName))
        return
    if mc.objExists(grpName + "." + attrName):
        generated_value = mc.getAttr(grpName + "." + attrName)
        if generated_value:
            mc.warning(
                ' ****** - error ! - ******  armor_up already generated, please delete   [  {}  ]   before regenerated'.format(
                    grpName))
            return True
        else:
            mc.warning(
                ' ****** - error ! - ******  armor_up generated failed, please delete   [  {}  ]   before regenerated'.format(
                    grpName))
            return True
    else:
        mc.addAttr(grpName, ln=attrName, at='bool')
        mc.setAttr(grpName + "." + attrName, 0)
        if parent:
            transform.parent(grpName, parent)
        return False

def groupAttrAdded(grpName, parent='', attrName='armorPart', finished=False):
    print grpName
    if finished:
        mc.setAttr(grpName + "." + attrName, 1)
        print(' ****** - note - ******  [  {}  ] generated successfully '.format(attrName))
        return
    if mc.objExists(grpName + "." + attrName):
        generated_value = mc.getAttr(grpName + "." + attrName)
        if generated_value:
            mc.warning(
                ' ****** - error ! - ******  [  {}  ] drive already generated, please delete   [  {}  ]   before regenerated'.format(
                    attrName, grpName))
            return True
        else:
            mc.warning(
                ' ****** - error ! - ******  [  {}  ] drive generated failed, please delete   [  {}  ]   before regenerated'.format(
                    attrName, grpName))
            return True
    else:
        mc.addAttr(grpName, ln=attrName, at='bool')
        mc.setAttr(grpName + "." + attrName, 0)
        if parent:
            transform.parent(grpName, parent)
        return False

def getGrpAttrInfo(GrpName, AttrName, defaultAttrName = 'default'):
    if mc.objExists("{}.{}".format(GrpName, AttrName)):
        attrValue = mc.getAttr("{}.{}".format(GrpName, AttrName))
    else:
        attrValue = defaultAttrName
    return attrValue


def has_joint_and_nurbs_curve(parent_node):
    # Get all children recursively
    children = mc.listRelatives(parent_node, ad=True, fullPath=True) or []

    # Initialize flags for joint and nurbsCurve detection
    has_joint = False
    has_nurbs_curve = False

    # Iterate through all children
    for child in children:
        # Check if the child is a joint
        if mc.objectType(child) == "joint":
            has_joint = True
        # Check if the child is a nurbsCurve
        elif mc.objectType(child) == "nurbsCurve":
            has_nurbs_curve = True

        # If both are found, return True
        if has_joint and has_nurbs_curve:
            return True

    # Return False if both types were not found
    return False

def has_double_joint_chain(parent_node):
    # Get all children recursively
    sons = mc.listRelatives(parent_node, c=True, fullPath=True, type = 'joint') or []
    print sons
    if len(sons) == 2:
        return True

    # Return False if both types were not found
    return False


def create_nurbsCurve_from_locators(locatorList, curveName):
    positions = []
    for locator in locatorList:
        pos = mc.xform(locator, query=True, worldSpace=True, translation=True)
        positions.append(pos)
    # genCurve = mc.curve(degree=3, point=positions, name=curveName)
    genCurve = mc.curve(degree=3, ep=positions, name=curveName)
    #shapeNode = mc.listRelatives(genCurve, type=True, fullPath=True)[0]
    #newShapeName = curveName + "Shape"
    utils.rename_shape(genCurve)

    return genCurve

def create_locators(locName, parentObj, positionObj, t=1, r=1, ro=1):
    if not mc.objExists(locName):
        newLoc = mc.spaceLocator(name=locName)[0]
        transform.catch_position(positionObj, newLoc, t, r, ro)
        transform.parent(newLoc, parentObj)
        return newLoc
    else:
        transform.catch_position(positionObj, locName, t, r, ro)
        transform.parent(locName, parentObj)
        return locName


def get_locators_under_group(group_name):
    """
    获取指定组下的所有定位器。

    :param group_name: 组的名称或路径
    :return: 包含所有定位器变换节点的列表
    """
    # 获取组下的所有直接子物体
    children = mc.listRelatives(group_name, ad=True, fullPath=True, type = 'locator') or []
    locators = []
    for child in children:
        trans = mc.listRelatives(child, p=True)[0]
        locators.append(trans)

    return locators

def changeRotateToHorizontal(upObj, tObj, orientObj, aimVector = (1,0,0), upVector = (0,1,0)):
    # 1.将指定轴向指向目标方向
    mc.delete(mc.aimConstraint(upObj, tObj, aimVector = aimVector, upVector = upVector, worldUpType = 'scene', mo=False))
    # 2.方向约束单轴向旋转
    if aimVector == (1, 0, 0):
        skip = ["y", "z"]
    elif aimVector == (0, 1, 0):
        skip = ["x", "z"]
    elif aimVector == (0, 0, 1):
        skip = ["x", "y"]
    else:
        skip = ["y", "z"]
    mc.delete(mc.orientConstraint(orientObj, tObj, mo=False, skip=skip, w=1.0))