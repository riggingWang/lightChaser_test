#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/7 17:12
# @File    : showUi.py


import sys
import os
import json
import webbrowser
sys.path.append(r"D:\program\lca_rig\assetsystem_sgl\tools\body\armour_tool\python\armour_tool")

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import *

import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import maya.cmds as mc
from assetsystem_sgl.ui import common
import production.usage_mongodb
import rigLib.scripts.utils.maya.utility as utility
import shiboken2
import mainWindow
reload(mainWindow)
import create_guide
reload(create_guide)
import armour_common
reload(armour_common)
import armor_generate_functions
reload(armor_generate_functions)

_win = "armour_rig_tool"
mayaMainWindowPtr = omui.MQtUtil.mainWindow()
mayaMainWindow = shiboken2.wrapInstance(long(mayaMainWindowPtr), QWidget)

try:
    dialog_ui = os.path.normpath(os.path.join(os.path.dirname(__file__), 'resources', 'dialog.ui'))
except:
    dialog_ui = r"D:\program\lca_rig\assetsystem_sgl\tools\body\armour_tool\python\armour_tool\resources\dialog.ui"

class armour_rig_ui(QMainWindow):
    def __init__(self, parent=mayaMainWindow):
        super(armour_rig_ui, self).__init__(parent)
        self.setObjectName(_win)
        self.setWindowTitle("Armour Rig Tool")
        self.resize(390, 700)
        self.main_Widget = QWidget(self)
        self.setCentralWidget(self.main_Widget)
        self.loadUiPySide(self.main_Widget,dialog_ui)
        self._ui = self.main_Widget.ui
        QMetaObject.connectSlotsByName(self)

        self.guide = create_guide.guide()
        self.EditMesh_cls = armour_common.EditMesh()
        self.copyBlendShapeCls = armour_common.copyBlendShape()

        self.setupUi()
        self.statusBar().showMessage("v2024.12")

        self._ui.armor_up_img_6.hide()
        self._ui.armorDn2HZcheck.hide()
        self._ui.ArmorDn2Btn.hide()
        self._ui.ArmorUpDrv2Btn.hide()

    def setupUi(self):
        self._language = "cn"
        self._ui.tabWidget.setCurrentIndex(0)
        self._ui.matchCurveProgressBar.hide()
        self._ui.EditMesh_EditOverProgressBar.hide()

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 381, 23))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionWiki = QAction(self)
        self.actionWiki.setObjectName("actionWiki")
        self.menuHelp.addAction(self.actionWiki)
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuHelp.setTitle(QApplication.translate("MainWindows", "help", None, -1))
        self.actionWiki.setText(QApplication.translate("MainWindows", "wiki", None, -1))
        self.actionWiki.triggered.connect(self.open_web)

        self.actionWiki_l = QAction(self)
        self.actionWiki_l.setObjectName("actionWiki")
        self.menuHelp.addAction(self.actionWiki_l)
        self.actionWiki_l.setText(QApplication.translate("MainWindows", "Switch language", None, -1))
        self.actionWiki_l.triggered.connect(self.language)

        self.listWidgetInit()
        self.EditMesh_listWidgetInit()
        self._ui.tabWidget.currentChanged.connect(self.currentChangedCmd)

    def loadUiPySide(self, widget, path=None):
        loader = QUiLoader()
        loader.setWorkingDirectory(os.path.dirname(path))
        f = QFile(path)
        f.open(QFile.ReadOnly)
        widget.ui = loader.load(path, widget)
        f.close()
        layout = QVBoxLayout()
        layout.setObjectName('uiLayout')
        layout.addWidget(widget.ui)
        widget.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setMinimumWidth(widget.ui.minimumWidth())
        widget.setMinimumHeight(widget.ui.minimumHeight())
        widget.setMaximumWidth(widget.ui.maximumWidth())
        widget.setMaximumHeight(widget.ui.maximumHeight())


    def open_web(self):
        webbrowser.open("http://wiki.zhuiguang.com/display/RIG/Armour+Rig+Tool")

    def language(self):
        print u"set language - {}".format(self._language)
        index = 0
        if self._language == "us":
            index = 0
            self._language = "cn"
        elif self._language == "cn":
            index = 1
            self._language = "us"

        json_path = r"D:\program\lca_rig\assetsystem_sgl\tools\body\armour_tool\python\armour_tool\resources\chinese_name.json"
        with open(json_path, "r") as json_file:
            data = json.load(json_file)

        for i in data:
            widget = self._ui.findChild(QWidget, i)
            text = data[i][index]
            try:
                widget.setText(u"{}".format(text))
            except:
                widget.setFormat(text)

        """ 
        
        all = self._ui.findChildren(QWidget)
        aaa = {}
        for i in all:
            try:
                t = i.text()
                o = i.objectName()
                aaa.update({"{}".format(o):["{}".format(t),"{}".format(t)]})
                i.setText(u"哈哈哈哈哈哈哈哈")
            except:
                pass
        print aaa

        with open(r"D:\program\lca_rig\assetsystem_sgl\tools\body\armour_tool\python\armour_tool\resources\chinese_name.json", "w") as json_file:
            json.dump(aaa, json_file, indent=4)
            
        """

    def currentChangedCmd(self):
        self.listUpdateBtnCmd()
        self.EditMesh_updateBtnCmd()

    @Slot()
    def on_CurveLoadingBtn_clicked(self):
        text = ""
        sel = mc.ls(sl=True)
        for i in sel:
            text += str(i)+","
        self._ui.CurveLoadingLineEdit.setText(text)


    @Slot()
    def on_AxialLoadingBtn_clicked(self):
        text = ""
        sel = mc.ls(sl=True)
        for i in sel:
            text += str(i)+","
        self._ui.AxialLoadingLineEdit.setText(text)


    @Slot()
    def on_nurbsGeoLoadingBtn_clicked(self):
        text = ""
        sel = mc.ls(sl=True)
        for i in sel:
            text += str(i)+","
        self._ui.nurbsGeoLoadingLineEdit.setText(text)

    @Slot()
    def on_spansUAddBtn_clicked(self):
        self.guide.setSpans("u", "add")

    @Slot()
    def on_spansUSubBtn_clicked(self):
        self.guide.setSpans("u", "sub")

    @Slot()
    def on_spansVAddBtn_clicked(self):
        self.guide.setSpans("v", "add")

    @Slot()
    def on_spansVSubBtn_clicked(self):
        self.guide.setSpans("v", "sub")


    @Slot()
    def on_ConvertCurveBtn_clicked(self):
        print "on_ConvertCurveBtn_clicked"
        Curve =  self._ui.CurveLoadingLineEdit.text()
        Axial =  self._ui.AxialLoadingLineEdit.text()
        aim = self._ui.aim_buttonGroup.checkedButton().text()
        up = self._ui.up_buttonGroup.checkedButton().text()
        curve_array = filter(None, Curve.split(","))
        axial_array = filter(None, Axial.split(","))
        self.guide.batch_convertCurve(curve_array, axial_array, aim, up)


    @Slot()
    def on_initializeBtn_clicked(self):
        self.guide.initialize_scene()

    @Slot()
    def on_nurbsImportGuideBtn_clicked(self):
        self.guide.importGuide()

    @Slot()
    def on_pickCurveBtn_clicked(self):
        prefix = self._ui.Prefix_LineEdit.text()
        self.guide.pickCurve(prefix + "_PickCurve")

    @Slot()
    def on_renameCurveBtn_clicked(self):
        prefix = self._ui.Prefix_LineEdit.text()
        LR = self._ui.LR_buttonGroup.checkedButton().text()
        self.guide.createCurveGuide(prefix, LR)

    @Slot()
    def on_nurbsMatchCurveBtn_clicked(self):
        progressBar = self._ui.matchCurveProgressBar
        mesh = self._ui.nurbsGeoLoadingLineEdit.text()
        mesh_array = filter(None, mesh.split(","))
        prefix = self._ui.Nurbs_Prefix_LineEdit.text()

        if len(mesh_array) == 0:
            om.MGlobal.displayWarning("No object loaded")
            return

        for i in mesh_array:
            exists = not mc.objExists(i)
            node_type_a = not mc.nodeType(i) == "transform"
            node_type_b = mc.nodeType(mc.listRelatives(i, s=True)) == "nurbsSurface"
            if exists or node_type_a or node_type_b:
                om.MGlobal.displayWarning("No exists or error type.")
                return

        self.guide.match_curve_guide(mesh_array, progressBar, prefix)


    @Slot()
    def on_nurbsCreateGuideBtn_clicked(self):
        prefix = self._ui.Nurbs_Prefix_LineEdit.text()
        checkBox = self._ui.NurbsMirrorcheckBox.isChecked()
        aim = self._ui.nurbs_aim_buttonGroup.checkedButton().text()
        up = self._ui.nurbs_up_buttonGroup.checkedButton().text()
        self.guide.create_nurbs_guide(prefix, checkBox, aim, up)

    @Slot()
    def on_AddPointsToolBtn_clicked(self):
        mc.AddPointsTool()

    @Slot()
    def on_insertKnotToolBtn_clicked(self):
        mc.InsertKnot()

    @Slot()
    def on_ReverseCurveBtn_clicked(self):
        mc.ReverseCurve()


    @Slot()
    def on_relaxCurveBtn_clicked(self):
        self.guide.smoothCurveCv()

    @Slot()
    def on_createShoulderBtn_clicked(self):  # Shoulder
        self.guide.shoulder_guide()

    @Slot()
    def on_createShoulderMirrorBtn_clicked(self):
        self.guide.shoulder_guide_mirror()

    @Slot()
    def on_createPauldronsBtn_clicked(self):  # Pauldrons
        self.guide.pauldrons_guide()

    @Slot()
    def on_createPauldronsMirrorBtn_clicked(self):
        self.guide.pauldrons_guide_mirror()

    @Slot()
    def on_createArmletBtn_clicked(self):  # Armlet
        self.guide.armlet_guide()

    @Slot()
    def on_createArmletMirrorBtn_clicked(self):
        self.guide.armlet_guide_mirror()




    # ----------------------------------------- tab2 ------------------------------------
    #@Slot()
    #def on_ctrlScaleApplyBtn_clicked(self):
    #    scaleValue = self._ui.ctrlScaleTextLineEdit.text()
    #    print scaleValue

    @Slot()
    @armour_common.undo
    def on_ArmorUpBtn_clicked(self):
        print('on_ArmorUpBtn_clicked')
        if self._ui.armorUpHZcheck.isChecked():
            horizontalCtrl=True
        else:
            horizontalCtrl=False
        run = armor_generate_functions.caocao_armor_setup_module('prefix', (1, 0, 0), (1, 0, 0), size=float(self._ui.ctrlScaleTextLineEdit.text()))
        selected = mc.ls(sl=1)
        if selected:
            for each in selected:
                run.create_armor_body_up_setup(each, horizontalCtrl)

        else:
            mc.warning('please select guide group')
        self._ui.ArmorUpBtn.setStyleSheet("background-color: green; color: white;")

    @Slot()
    @armour_common.undo
    def on_ArmorUpDrvBtn_clicked(self):
        print('on_ArmorUpDrvBtn_clicked')
        run = armor_generate_functions.caocao_armor_setup_module('prefix', (1, 0, 0), (1, 0, 0), size=float(self._ui.ctrlScaleTextLineEdit.text()))
        selected = mc.ls(sl=1)
        if selected:
            run.create_armor_body_up_drive(selected[0])
        else:
            mc.warning('please select generated group')
        self._ui.ArmorUpDrvBtn.setStyleSheet("background-color: green; color: white;")

    @Slot()
    @armour_common.undo
    def on_ArmorDnBtn_clicked(self): #new
        print('on_ArmorDnBtn_clicked')
        if self._ui.armorDnHZcheck.isChecked():
            horizontalCtrl=True
        else:
            horizontalCtrl=False
        run = armor_generate_functions.caocao_armor_setup_module('prefix', (1, 0, 0), (1, 0, 0), size=float(self._ui.ctrlScaleTextLineEdit.text()))
        selected = mc.ls(sl=1)
        if selected:
            for each in selected:
                run.create_armor_body_dn_setup(each, horizontalCtrl)
        else:
            mc.warning('please select guide group')
        self._ui.ArmorDnBtn.setStyleSheet("background-color: green; color: white;")

    @Slot()
    @armour_common.undo
    def on_ArmorDnDrvBtn_clicked(self):
        print('on_ArmorDnDrvBtn_clicked')
        run = armor_generate_functions.caocao_armor_setup_module('prefix', (1, 0, 0), (1, 0, 0), size=float(self._ui.ctrlScaleTextLineEdit.text()))
        selected = mc.ls(sl=1)
        if selected:
            run.create_armor_body_dn_drive(selected[0])
        else:
            mc.warning('please select generated group')
        self._ui.ArmorDnDrvBtn.setStyleSheet("background-color: green; color: white;")

    @Slot()
    @armour_common.undo
    def on_ArmorDn2Btn_clicked(self): #new
        print('on_ArmorDn2Btn_clicked')
        if self.armorUpHZcheck.isChecked():
            horizontalCtrl=True
        else:
            horizontalCtrl=False
        run = armor_generate_functions.caocao_armor_setup_module('prefix', (1, 0, 0), (1, 0, 0), size=float(self._ui.ctrlScaleTextLineEdit.text()))
        selected = mc.ls(sl=1)
        if selected:
            run.create_armor_body_dn_2_setUp(selected[0], horizontalCtrl)
        else:
            mc.warning('please select guide group')
        self._ui.ArmorDn2Btn.setStyleSheet("background-color: green; color: white;")

    @Slot()
    @armour_common.undo
    def on_ArmorUpDrv2Btn_clicked(self):
        print('on_ArmorUpDrv2Btn_clicked')
        run = armor_generate_functions.caocao_armor_setup_module('prefix', (1, 0, 0), (1, 0, 0), size=float(self._ui.ctrlScaleTextLineEdit.text()))
        selected = mc.ls(sl=1)
        if selected:
            run.create_armor_body_dn_2_drive(selected[0])
        else:
            mc.warning('please select guide group')
        self._ui.ArmorUpDrv2Btn.setStyleSheet("background-color: green; color: white;")

    @Slot()
    def on_ArmorShoulderBtn_clicked(self): #new
        print('on_ArmorShoulderBtn_clicked')
        run = armor_generate_functions.caocao_armor_setup_module('prefix', (1, 0, 0), (1, 0, 0), size=float(self._ui.ctrlScaleTextLineEdit.text()))
        selected = mc.ls(sl=1)
        if selected:
            for each in selected:
                mc.undoInfo(openChunk=True)
                try:
                    run.create_armor_shoulder_setup(each)
                    mc.undoInfo(closeChunk=True)
                except Exception as e:
                    mc.undoInfo(closeChunk=True)
        else:
            mc.warning('please select guide group')
        self._ui.ArmorShoulderBtn.setStyleSheet("background-color: green; color: white;")

    @Slot()
    def on_ArmorShoulderDrvBtn_clicked(self): #new
        print('on_ArmorShoulderDrvBtn_clicked')
        run = armor_generate_functions.caocao_armor_setup_module('prefix', (1, 0, 0), (1, 0, 0), size=float(self._ui.ctrlScaleTextLineEdit.text()))
        selected = mc.ls(sl=1)
        if selected:
            run.create_armor_shoulder_drive(selected[0])
        else:
            mc.warning('please select generated group')
        self._ui.ArmorShoulderDrvBtn.setStyleSheet("background-color: green; color: white;")

    @Slot()
    @armour_common.undo
    def on_ctrlScaleApplyBtn_clicked(self): #new
        print('on_ctrlScaleApplyBtn_clicked')
        run = armor_generate_functions.caocao_armor_setup_module('prefix', (1, 0, 0), (1, 0, 0), size=float(self._ui.ctrlScaleTextLineEdit.text()))
        run.apply_ctrl_scale_fnc(size=float(self._ui.ctrlScaleTextLineEdit.text()))
    @Slot()
    @armour_common.undo
    def on_angleDriveBtn_clicked(self):
        print('on_angleDriveBtn_clicked')
        selected = mc.ls(sl=1)
        if selected:
            armor_generate_functions.gen_angele_between_node(selected)
        else:
            mc.warning('please select three ctrls')

    @Slot()
    @armour_common.undo
    def on_ArmorPauldronsBtn_clicked(self): #new
        print('on_ArmorPauldronsBtn_clicked')
        run = armor_generate_functions.caocao_armor_setup_module('prefix', (1, 0, 0), (1, 0, 0), size=float(self._ui.ctrlScaleTextLineEdit.text()))
        selected = mc.ls(sl=1)
        if selected:
            run.create_armor_pauldrons_setup(selected[0])
        else:
            mc.warning('please select generated group')
        self._ui.ArmorPauldronsBtn.setStyleSheet("background-color: green; color: white;")

    @Slot()
    def on_ArmorArmletBtn_clicked(self):  # new
        print('on_ArmorArmletBtn_clicked')
        run = armor_generate_functions.caocao_armor_setup_module('prefix', (1, 0, 0), (1, 0, 0),
                                                                 size=float(self._ui.ctrlScaleTextLineEdit.text()))
        selected = mc.ls(sl=1)
        if selected:
            mc.undoInfo(openChunk=True)
            try:
                run.create_armlet_setup(selected[0])
                mc.undoInfo(closeChunk=True)
            except Exception as e:
                mc.undoInfo(closeChunk=True)
        else:
            mc.warning('please select generated group')
        self._ui.ArmorArmletBtn.setStyleSheet("background-color: green; color: white;")

    @Slot()
    def on_ArmorBodyDriveBtn_clicked(self): #new
        print('on_ArmorBodyDrive_clicked')
        run = armor_generate_functions.caocao_armor_setup_module('prefix', (1, 0, 0), (1, 0, 0), size=float(self._ui.ctrlScaleTextLineEdit.text()))
        run.create_body_drive()
        self._ui.ArmorBodyDriveBtn.setStyleSheet("background-color: green; color: white;")

    @Slot()
    def on_DriveConvertToolBtn_clicked(self):
        print('on_DriveConvertToolBtn_clicked')
        sys.path.append('U:/lca_rig/assetsystem_sgl/tools/animation/convert_animCurve/python/convert_animCurve')
        import convert_animCurve_fun as DriveConvertTool
        reload(DriveConvertTool);
        DriveConvertTool.mainCall()

    @Slot()
    def on_DriveIOToolBtn_clicked(self):
        print('on_DriveIOToolBtn_clicked')
        sys.path.append('U:/lca_rig/assetsystem_sgl/tools/animation/AnimCurveIO/python')
        import DrivenCurveIO.showUI as DriveIOTool
        reload(DriveIOTool);
        DriveIOTool.main()
    @Slot()
    def on_sdkMirrorToolBtn_clicked(self):
        print('on_DriveIOToolBtn_clicked')
        sys.path.append('U:/lca_rig/assetsystem_sgl/tools/animation/driver-key/python/driver_key/')
        import mirror_sdk_ui.mani_window as sdkMirrorTool
        reload(sdkMirrorTool);
        sdkMirrorTool.show_ui()

    # ----------------------------------------- tab3 ------------------------------------


    @Slot()
    def on_tool_copyBlendBtn_clicked(self):
        sel = mc.ls(sl=True)
        for i in sel:
            if i == sel[0]:
                continue
            self.copyBlendShapeCls.copy_blendShape(sel[0], i)
        mc.select(sel)

    @Slot()
    def on_tool_copyWeightsBtn_clicked(self):
        armour_common.batchCopyWeights()



    # ----------------------------------------- listWidget set------------------------------------

    @Slot()
    def on_guidelistUpdataBtn_clicked(self):
        self.listUpdateBtnCmd()
        self.listWidgetInit()


    def listWidgetInit(self):
        self._ui.guidelistWidget.itemClicked.connect(self.list_itemClicked_cmd)
        self._ui.guidelistWidget.itemDoubleClicked.connect(self.list_itemDoubleClicked_cmd)
        self.listUpdateBtnCmd()

    def list_itemClicked_cmd(self):
        currentSelect = self._ui.guidelistWidget.currentItem().text()
        mc.select(currentSelect)

    def list_itemDoubleClicked_cmd(self):
        currentSelect = self._ui.guidelistWidget.currentItem().text()
        mc.delete(currentSelect)
        self.listUpdateBtnCmd()

    def listUpdateBtnCmd(self):
        self._ui.guidelistWidget.clear()
        if mc.objExists(self.guide.armour_batchDetail_grp):
            for i in armour_common.getChlidren(self.guide.armour_batchDetail_grp):
                self._ui.guidelistWidget.addItem(i)
        if mc.objExists(self.guide.armourShoulder_grp):
            self._ui.guidelistWidget.addItem(self.guide.armourShoulder_grp)
        if mc.objExists(self.guide.armourPauldrons_grp):
            self._ui.guidelistWidget.addItem(self.guide.armourPauldrons_grp)
        if mc.objExists(self.guide.armourArmlet_grp):
            self._ui.guidelistWidget.addItem(self.guide.armourArmlet_grp)


    # ----------------------------------------- EditMesh listWidget set---------------------------------

    @Slot()
    def on_EditMesh_RefreshBtn_clicked(self):
        print "EditMesh_RefreshBtn"
        self.EditMesh_updateBtnCmd()


    def EditMesh_listWidgetInit(self0):
        pass



    @Slot()
    def on_EditMesh_createMeshBtn_clicked(self):
        currentSelect = self._ui.EditMesh_listWidget.currentItem().text()
        self.EditMesh_cls.createEditMesh(currentSelect)
        self.EditMesh_updateBtnCmd()

    @Slot()
    def on_EditMesh_EditOverBtn_clicked(self):
        ProgressBar = self._ui.EditMesh_EditOverProgressBar
        confirm = mc.confirmDialog(title=u'提示',
                                   message=u'请确认控制器为归零状态\n'
                                           u'编辑模型历史只允许存在三个节点：\n'
                                           u'\n'
                                           u'"skinCluster",\n'
                                           u'"blendShape",\n'
                                           u'"lcPoseDeformer"\n'
                                           u'\n'
                                           u'生效后，编辑模型删除，无法恢复，你确定吗？？',
                                   button=['Confirm', 'Cancel'],
                                   backgroundColor=[0.3, 0.2, 0.2],
                                   defaultButton='Yes', cancelButton='No', dismissString='No')
        if confirm == "Cancel":
            return
        currentSelect = self._ui.EditMesh_listWidget.currentItem().text()
        prefix = currentSelect.split("{}".format(self.EditMesh_cls.splitStr))[0]
        self.EditMesh_cls.deleteEditMesh(prefix, ProgressBar)
        self.EditMesh_updateBtnCmd()



    def EditMesh_updateBtnCmd(self):
        grp_array = mc.ls("*_armor_tri_IkCrv_grp")
        prefix_array = []
        for each_grp in grp_array:
            prefix = each_grp.split("_armor_tri_IkCrv_grp")[0]
            child = armour_common.getChlidren(each_grp)
            if len(child) == 0:
                continue
            prefix_array.append(prefix)

        self._ui.EditMesh_listWidget.clear()
        for prefix in prefix_array:
            string = prefix
            if mc.objExists(self.EditMesh_cls.edit_grp.format(prefix)):
                string = string + "{}EditMesh".format(self.EditMesh_cls.splitStr)

            self._ui.EditMesh_listWidget.addItem(string)


@production.usage_mongodb.Usage('Armour_rig_tool', dept='rig')
def main():
    if mc.window(_win, ex=True):
        mc.deleteUI(_win)
    ui = armour_rig_ui()
    ui.show()

if __name__ == '__main__':
    main()



