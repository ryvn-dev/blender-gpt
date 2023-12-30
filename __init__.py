
import bpy
from .gpt_pkg import *
from .gpt_pnl import BLENDERGPT_PT_PANEL, props_initialization, props_clear
from .gpt_prf import BLENDERGPT_AddonPreferences
from .gpt_opt import BLENDERGPT_OT_DEL_ALL_MSG, BLENDERGPT_OT_DEL_MSG, BLENDERGPT_OT_GPT_CODE, BLENDERGPT_OT_SEND_MSG


bl_info = {
    "name": "Blender GPT",
    "author": "Ryvn (@hc-psy) (@@hao-chenglo2049)",
    "description": "",
    "blender": (2, 82, 0),
    "version": (0, 0, 2),
    "warning": "",
    "category": "Object"
}


Classes = (BLENDERGPT_PT_PANEL, BLENDERGPT_OT_DEL_ALL_MSG, BLENDERGPT_OT_DEL_MSG,
           BLENDERGPT_OT_GPT_CODE, BLENDERGPT_OT_SEND_MSG, BLENDERGPT_AddonPreferences)


def register():
    for cls in Classes:
        if cls.__name__ not in bpy.types.__dict__:
            bpy.utils.register_class(cls)

    props_initialization()


def unregister():
    for cls in Classes:
        if cls.__name__ in bpy.types.__dict__:
            bpy.utils.unregister_class(cls)

    props_clear()
