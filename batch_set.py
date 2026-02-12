#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2025/7/2 14:56
# @File    : batch_set.py

"""

C:\Program Files\Autodesk\Maya2019\bin\mayapy.exe D:\program\lightChaser_test\batch_set.py

"""



import maya.standalone

try:
    maya.standalone.initialize(name='python')
except RuntimeError:
    pass

import os
import maya.cmds as mc
import pymel.core as pm
import shutil

chrList = os.listdir(r"Z:\projects\sgl\asset\chr")
chrList = ["youxia_a"]

dir_array = []
for i in chrList:
    layout_file = r"Z:\projects\sgl\asset\chr\{0}\rig\publish\{0}.rig.rigging_layout\{0}.mb".format(i)
    ani_file = r"Z:\projects\sgl\asset\chr\{0}\rig\publish\{0}.rig.rigging\{0}.mb".format(i)

    if os.path.isfile(layout_file) and os.path.isfile(ani_file):
        dir_array.append([ani_file, layout_file, i])

print len(dir_array)

def export_info(*args):
    fileName = "batch_info.txt"
    filePath = r"W:\shome\wangqi2\info"
    longPath = os.path.join(filePath, fileName)

    if not os.path.isfile(longPath):
        with open(longPath, 'w'):
            pass

    with open(longPath, 'r') as file:
        content = file.read()

    for i in args:
        content+=str(i)+"\n"

    modified_content = content

    with open(longPath, 'w') as file:
        file.write(modified_content)



print dir_array


for ani_file, layout_file, chr_name in dir_array[:1]:
    print "+-"*100

    print "Open the Maya file >>>>>>>>>>>>>>>>>>>> {}".format(ani_file)

    try:

        mc.file(ani_file, ignoreVersion=1, typ="mayaBinary", options="v=0;", o=1, f=1)

        ani_lookPass_str = mc.addAttr("visibility_ctrl.lookPass", q=True, en=True)

        ani_lookPass_list = ani_lookPass_str.split(":")

        print ani_lookPass_list

        mc.file(layout_file, ignoreVersion=1, typ="mayaBinary", options="v=0;", o=1, f=1)

        if not mc.objExists("visibility_ctrl.lookPass"):

            mc.addAttr("visibility_ctrl", ln="lookPass", at="enum", en="Green:Blue:", k=True)

        layout_lookPass_str = mc.addAttr("visibility_ctrl.lookPass", q=True, en=True)

        layout_lookPass_list = layout_lookPass_str.split(":")

        print layout_lookPass_list

        mc.addAttr("visibility_ctrl.lookPass", enumName=ani_lookPass_str, e=1)

        str_a = ani_file.replace(".rig.rigging",".rig.rigging\\batch_backup")

        moreThan = []
        for i in ani_lookPass_list:
            if not i in layout_lookPass_list:
                moreThan.append(i)

        if len(moreThan) == 0:
            export_info("+" * 150,
                        layout_file,
                        "Animation lookPath：{}".format(ani_lookPass_list),
                        "Layout lookPath：{}".format(layout_lookPass_list),
                        "continue!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

            continue

        backupPath = r"Z:\projects\sgl\asset\chr\{0}\rig\publish\{0}.rig.rigging_layout\batch_backup".format(chr_name)

        if not os.path.isdir(backupPath):
            os.makedirs(backupPath)

        if not os.path.isfile(os.path.join(backupPath, "{}.mb".format(chr_name))):
            shutil.copy2(layout_file, os.path.join(backupPath))


        export_info("+" * 150,
                    layout_file,
                    "Animation lookPath：{}".format(ani_lookPass_list),
                    "Layout lookPath：{}".format(layout_lookPass_list),
                    "More than: {}".format(moreThan))



    except RuntimeError as e:

        export_info("+" * 150,
                    layout_file,
                    "Error!!!!!!!!!!!!!!!!!!  \n{}".format(e))

    print "+-"*100
















