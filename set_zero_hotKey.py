
"""set_zero"""

import pymel.core as pm
import maya.cmds as mc

sel = pm.ls(sl=True)
def set_zero(obj, attr, v):
    try:
        pm.setAttr("{}.{}".format(obj, attr), v)
    except:
        pass


for i in sel:
    for j in ["tx", "ty", "tz", "rx", "ry", "rz", ]:
        set_zero(i, j, 0)
    for j in ["sx", "sy", "sz" ]:
        set_zero(i, j, 1)




"""mesh unlock"""

import pymel.core as pm
mesh = pm.ls(type="mesh")
for i in mesh:
    pm.setAttr("{}.overrideEnabled".format(i), l=False)
    pm.setAttr("{}.overrideEnabled".format(i), 0)

joints = pm.ls(type="joint")
for i in joints:
    pm.setAttr("{}.drawStyle".format(i), 0)





