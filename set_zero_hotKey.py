
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
    set_zero(i, "tx", 0)
    set_zero(i, "ty", 0)
    set_zero(i, "tz", 0)
    set_zero(i, "rx", 0)
    set_zero(i, "ry", 0)
    set_zero(i, "rz", 0)
    set_zero(i, "sx", 1)
    set_zero(i, "sy", 1)
    set_zero(i, "sz", 1)



"""mesh unlock"""

import pymel.core as pm
mesh = pm.ls(type="mesh")
for i in mesh:
    pm.setAttr("{}.overrideEnabled".format(i), l=False)
    pm.setAttr("{}.overrideEnabled".format(i), 0)

joints = pm.ls(type="joint")
for i in joints:
    pm.setAttr("{}.drawStyle".format(i), 0)





