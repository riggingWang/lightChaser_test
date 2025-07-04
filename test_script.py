#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2025/1/8 15:49
# @File    : test_script.py

# update: v02---2024.12.20  µ÷ÕûtargetÃüÃû,ÓÅ»¯copy

import maya.cmds as cmds
import maya.mel as mel


class OceanCopyBS_Window(object):
    def __init__(self):
        pass

    def UI(self):
        if cmds.window("CopyBS_window", exists=True):
            cmds.deleteUI("CopyBS_window")

        self.window = cmds.window("CopyBS_window", title="RBF°ü¹ü´«µÝBS¹¤¾ß v1.0")
        # ÉèÖÃUIÕûÌå²¼¾Ö
        self.layout_main = cmds.columnLayout(adj=True, columnAttach=('both', 5), rowSpacing=5)
        cmds.text(label='', h=2, parent=self.layout_main)  # ¶¥²¿Ô¤Áô¿Õ¼ä
        # -------------------------------µÚÒ»²¿·ÖUI--------------------------------------
        # µÚÒ»ÐÐUI
        cmds.rowLayout(numberOfColumns=3, columnWidth3=(60, 100, 35), adjustableColumn=2, columnAlign=(1, 'right'),
                       columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)], parent=self.layout_main)
        self.text_source = cmds.text(label=u"Ô´RBFÄ£ÐÍ:", w=70, h=25, font="fixedWidthFont")
        self.textField_source = cmds.textField("source_mod", tx=u"", w=100, h=25, placeholderText="¼ÓÔØÓÐRBFµÄÄ£ÐÍ...")
        self.button_source = cmds.button(label=u"ÔØÈë", w=35, h=25, command=self.SourceMod_load)
        # µÚ¶þÐÐUI
        cmds.rowLayout(numberOfColumns=3, columnWidth3=(60, 100, 35), adjustableColumn=2, columnAlign=(1, 'right'),
                       columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)], parent=self.layout_main)
        self.text_base = cmds.text(label=u"»ù´¡Ä£ÐÍ:", w=70, h=25, font="fixedWidthFont")
        self.textField_base = cmds.textField("base_mod", tx=u"", w=100, h=25, placeholderText="¼ÓÔØ´ý´«µÝµÄ»ù´¡Ä£ÐÍ...")
        self.button_base = cmds.button(label=u"ÔØÈë", w=35, h=25, command=self.BaseMod_load)
        cmds.separator(height=5, style='in', parent=self.layout_main)
        cmds.setParent('..')
        # -------------------------------µÚ¶þ²¿·ÖUI--------------------------------------
        layout_wrap = cmds.rowLayout(parent=self.layout_main, numberOfColumns=2, columnWidth2=(150, 150),
                                     adjustableColumn=2, columnAttach=[(2, 'both', 0)])
        self.checkBox_exclusiveBind = cmds.checkBox(label='exclusiveBind', value=True)
        # self.checkBox_invert = cmds.checkBox(label=u"·´Ëã", enable=False)
        cmds.separator(height=5, style='in', parent=self.layout_main)
        cmds.setParent('..')
        # -------------------------------µÚÈý²¿·ÖUI--------------------------------------
        form_layout = cmds.formLayout(parent=self.layout_main)
        self.button_medium = cmds.button(label=u'½éÖÊ', w=90, h=25, command=self.Medium)
        self.button_wrap = cmds.button(label=u'°ü¹ü', w=90, h=25, command=self.Wrap)
        self.button_transfer = cmds.button(label=u'´«µÝ', w=90, h=25, command=self.Transfer)
        # ÉèÖÃ°´Å¥Î»ÖÃºÍ×ÔÊÊÓ¦
        cmds.formLayout(form_layout, edit=True,
                        attachForm=[
                            (self.button_medium, 'top', 0), (self.button_medium, 'left', 0),
                            (self.button_transfer, 'top', 0), (self.button_transfer, 'right', 0),
                            (self.button_wrap, 'top', 0)
                        ],
                        attachControl=[
                            (self.button_medium, 'right', 5, self.button_wrap),
                            (self.button_transfer, 'left', 5, self.button_wrap)
                        ],
                        attachPosition=[
                            (self.button_wrap, 'left', 0, 33), (self.button_wrap, 'right', 0, 66),
                        ])
        cmds.rowLayout(numberOfColumns=1, columnAlign=(1, 'left'), parent=self.layout_main)
        cmds.text(label=u'×¢Òâ£ºRBF½ÚµãÃû³ÆÒªÓëÔ´Ä£ÐÍ¶ÔÓ¦£¬ÇÒÏàÍ¬pose»òÕß±»Ëø¶¨µÄpose»á×Ô¶¯Ìø¹ý', h=20)

        cmds.showWindow(self.window)

    def SourceMod_load(self, *args):
        sel = []
        sel = cmds.ls(sl=True, type='transform')
        if not sel:
            cmds.warning("Ñ¡Ôñ´íÎó!!")
            return 0
        else:
            self.SourceMod = sel[0]
            cmds.textField("source_mod", edit=True, text=self.SourceMod)
        # »ñÈ¡Ä£ÐÍµÄRBF½ÚµãºÍtarget
        mesh_History = cmds.listHistory(sel[0], pdo=True)
        if "RBF_PSD__" + sel[0] in mesh_History:
            self.SourceMod_bsNode = "RBF_PSD__" + sel[0]
            self.SourceMod_targetList = cmds.listAttr(self.SourceMod_bsNode + ".targetWeights", multi=True)
        else:
            cmds.warning("ËùÑ¡ÎïÌåÃ»ÓÐRBF½Úµã or ÃüÃû²»¹æ·¶!!!")

    def BaseMod_load(self, *args):
        sel = []
        sel = cmds.ls(sl=True, type='transform')
        if not sel:
            cmds.warning("Ñ¡Ôñ´íÎó!!!")
            return 0
        else:
            self.BaseMod = sel[0]
            cmds.textField("base_mod", edit=True, text=self.BaseMod)

    def Medium(self, *args):
        mod = cmds.textField("base_mod", query=True, text=True)
        cmds.select(mod, r=1)
        cmds.duplicate()
        self.MediumMod = cmds.rename("MediumMod")
        cmds.select(mod, r=1)
        mel.eval('doHideObjects true')
        cmds.select(self.MediumMod, r=1)
        try:
            mel.eval('performUnparent false')
        except:
            pass

    def Wrap(self, *args):
        self.BaseMod = cmds.textField("base_mod", query=True, text=True)
        self.SourceMod = cmds.textField("source_mod", query=True, text=True)
        cmds.select(cl=1)
        cmds.select(self.MediumMod, r=1)
        cmds.select(self.SourceMod, add=1)
        # self.wrapNode=cmds.deformer(type="wrap")[0]
        # self.wrapNode = mel.eval("deformer -type wrap {};".format(self.MediumMod))[0]
        self.wrapNode = mel.eval("doWrapArgList \"7\"{\"1\", \"0\", \"1\", \"2\", \"1\", \"1\", \"1\", \"0\"};")[0]
        state = cmds.checkBox(self.checkBox_exclusiveBind, query=True, value=True)
        if state:
            cmds.setAttr("{}.exclusiveBind".format(self.wrapNode), 1)
        else:
            cmds.setAttr("{}.exclusiveBind".format(self.wrapNode), 0)

    def Transfer(self, *args):
        self.BaseMod = cmds.textField("base_mod", query=True, text=True)
        self.SourceMod = cmds.textField("source_mod", query=True, text=True)
        mesh_History = cmds.listHistory(self.SourceMod, pdo=True)
        if "RBF_PSD__" + self.SourceMod in mesh_History:
            self.SourceMod_bsNode = "RBF_PSD__" + self.SourceMod
            self.SourceMod_targetList = cmds.listAttr(self.SourceMod_bsNode + ".targetWeights", multi=True)
        else:
            cmds.warning("ËùÑ¡ÎïÌåÃ»ÓÐRBF½Úµã or ÃüÃû²»¹æ·¶!!!")
        targetList = []
        if self.SourceMod_bsNode:
            self.SourceMod_targetList = cmds.listAttr(self.SourceMod_bsNode + ".targetWeights", multi=True)
            for target in self.SourceMod_targetList:
                is_locked = cmds.getAttr(self.SourceMod_bsNode + "." + target, lock=True)
                if is_locked:
                    continue
                else:
                    targetList.append(target)
        else:
            cmds.warning("ËùÑ¡ÎïÌåÃ»ÓÐRBF½Úµã or ÃüÃû²»¹æ·¶!!!")

        if cmds.objExists(self.MediumMod):
            # ÁÐ³öÔ´Ä£ÐÍBSÁ¬½Ó×´Ì¬
            input_connections = []
            for target in targetList:
                connections = cmds.listConnections(self.SourceMod_bsNode + '.' + target, source=True, destination=False,
                                                   connections=True, plugs=True)
                if connections:
                    for temp in connections:
                        input_connections.append(temp)
            # # ¶Ï¿ªÔ´Ä£ÐÍBSÁ¬½Ó
            # if input_connections:
            #     for i in range(0, len(input_connections), 2):
            #         cmds.disconnectAttr(input_connections[i+1],input_connections[i])

            # ¸øÄ¿±êÄ£ÐÍ´´½¨¿ÕBS½Úµã
            cmds.select(self.BaseMod, r=1)
            if '|' in self.BaseMod:
                baseMod = self.BaseMod.split('|')[-1]
            else:
                baseMod = self.BaseMod
            base_mesh_History = cmds.listHistory(self.BaseMod, pdo=True)
            self.BaseMod_bsNode = cmds.ls(base_mesh_History, type='blendShape')
            print(self.BaseMod_bsNode)
            bs_count = 0
            if self.BaseMod_bsNode:
                NewBSNode = self.BaseMod_bsNode[0]
                self.BaseMod_targetList = cmds.listAttr(self.BaseMod_bsNode[0] + '.weight', multi=True)
                bs_count = len(self.BaseMod_targetList)
            else:
                NewBSNode = cmds.blendShape(n=baseMod + "_LcBS", automatic=1)[0]
            # ´«µÝBS
            for i in range(len(targetList)):
                target = targetList[i]
                rbf_pose = target.split("___")[0]
                # Ìø¹ýÒÑÉ¾³ýµÄrbf_poseÊôÐÔ
                if not cmds.objExists(rbf_pose):
                    continue
                # Ìø¹ýÒÑ´«µÝµÄrbf_pose
                if cmds.attributeQuery(rbf_pose, node=NewBSNode, exists=True):
                    continue

                ctrl_name = cmds.getAttr("{}.ctrlName".format(rbf_pose))
                rotation = cmds.getAttr("{}.Rotation".format(rbf_pose))
                cmds.setAttr(ctrl_name + ".rx", rotation[0][0])
                cmds.setAttr(ctrl_name + ".ry", rotation[0][1])
                cmds.setAttr(ctrl_name + ".rz", rotation[0][2])
                # cmds.setAttr(self.SourceMod_bsNode+"."+target,1)
                MediumBSMod = cmds.duplicate(self.MediumMod)[0]
                TargetBSMod = mel.eval('invertShape {0} {1}'.format(self.BaseMod, MediumBSMod))
                # cmds.setAttr(self.SourceMod_bsNode+"."+target,0)
                cmds.blendShape(NewBSNode, edit=True, t=(self.BaseMod, i + bs_count, TargetBSMod, 1.0))
                cmds.delete(MediumBSMod)
                cmds.delete(TargetBSMod)

                cmds.aliasAttr(rbf_pose, "{0}.w[{1}]".format(NewBSNode, i + bs_count))
                cmds.setAttr(ctrl_name + ".rx", 0)
                cmds.setAttr(ctrl_name + ".ry", 0)
                cmds.setAttr(ctrl_name + ".rz", 0)

            cmds.delete(self.MediumMod)
            # Ô´Ä£ÐÍBSÁ¬½Ó
            if input_connections:
                # for i in range(0, len(input_connections), 2):
                #     cmds.connectAttr(input_connections[i+1],input_connections[i])
                # Ä¿±êÄ£ÐÍBSÁ¬½Ó
                for i in range(0, len(input_connections), 2):
                    base_input = input_connections[i].replace(self.SourceMod_bsNode, NewBSNode).split("___")[0]

                    if not cmds.listConnections(base_input):
                        cmds.connectAttr(input_connections[i + 1], base_input)
                    else:
                        pass
                    # cmds.connectAttr(input_connections[i+1],input_connections[i].replace(self.SourceMod_bsNode,NewBSNode))
            cmds.select(self.BaseMod, r=1)
            mel.eval('evalEcho "showHidden -a"')
        else:
            cmds.warning("No Medium Model!")


CopyBS = OceanCopyBS_Window()
CopyBS.UI()