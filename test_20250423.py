#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2025/4/23 14:25
# @File    : test_20250423.py

import os
import json
import maya.cmds as mc

def switch_crd_rigging():
    sel = mc.ls(sl=True)
    for e_chr in sel:
        ref_node = mc.referenceQuery(e_chr, rfn=True)
        path = mc.referenceQuery(e_chr, f=True)
        normalPath = path.split("{")[0]
        chr_name = normalPath.rsplit("/", 1)[-1].split(".")[0]
        crd_path = normalPath.replace(chr_name, "{}_crd".format(chr_name)).replace("asset/chr/", "asset/crd/")

        if not os.path.isfile(crd_path):
            mc.confirmDialog(title=u'提示', message=u"群集绑定不存在，请确认绑定是否已经提交。")
            continue
        mc.file(crd_path, loadReference=ref_node, options="v=0")



