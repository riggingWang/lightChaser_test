#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2025/7/4 17:39
# @File    : deadline_batch.py



# import maya.standalone
#
# try:
#     maya.standalone.initialize(name='python')
# except RuntimeError:
#     pass

import os
import sys

import maya.cmds as mc
import pymel.core as pm
import shutil




def export_info(*args):
    fileName = "batch_info.txt"
    filePath = r"W:/shome/wangqi2/info"
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


def main(chr_name):
    layout_file = r"Z:\projects\sgl\asset\chr\{0}\rig\publish\{0}.rig.rigging_layout\{0}.mb".format(chr_name)
    ani_file = r"Z:\projects\sgl\asset\chr\{0}\rig\publish\{0}.rig.rigging\{0}.mb".format(chr_name)

    if not (os.path.isfile(layout_file) and os.path.isfile(ani_file)):
        export_info("+" * 150,
                    layout_file,
                    "Missing files   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return

    mc.file(ani_file, ignoreVersion=1, typ="mayaBinary", options="v=0;", o=1, f=1)

    ani_lookPass_str = mc.addAttr("visibility_ctrl.lookPass", q=True, en=True)

    ani_lookPass_list = ani_lookPass_str.split(":")

    mc.file(layout_file, ignoreVersion=1, typ="mayaBinary", options="v=0;", o=1, f=1)

    if mc.objExists("visibility_ctrl.lookPass"):

        layout_lookPass_str = mc.addAttr("visibility_ctrl.lookPass", q=True, en=True)

        layout_lookPass_list = layout_lookPass_str.split(":")

    else:

        mc.addAttr("visibility_ctrl", ln="lookPass", at="enum", en="default", k=True)

        layout_lookPass_list = []


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
        return


    backupPath = r"Z:\projects\sgl\asset\chr\{0}\rig\publish\{0}.rig.rigging_layout\batch_backup".format(chr_name)

    if not os.path.isdir(backupPath):
        os.makedirs(backupPath)

    if not os.path.isfile(os.path.join(backupPath, "{}.mb".format(chr_name))):
        shutil.copy2(layout_file, os.path.join(backupPath))

    mc.addAttr("visibility_ctrl.lookPass", enumName=ani_lookPass_str, e=1)

    export_info("+" * 150,
                layout_file,
                "Animation lookPath：{}".format(ani_lookPass_list),
                "Layout lookPath：{}".format(layout_lookPass_list),
                "More than: {}".format(moreThan))

    mc.file(save=1, force=1, options="v=0")




if __name__ == '__main__':
    # argv = sys.argv[1]
    # main(argv)

    main("yuanshao_zhongjun_armor")
