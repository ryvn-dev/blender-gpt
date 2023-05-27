
import bpy
from .gptzh_pnl import BLENDERGPT_PT_PANEL
from .gptzh_prf import BLENDERGPT_AddonPreferences
from .gptzh_opt import BLENDERGPT_OT_DEL_ALL_MSG, BLENDERGPT_OT_DEL_MSG, BLENDERGPT_OT_GPT_CODE, BLENDERGPT_OT_SEND_MSG


bl_info = {
    "name": "Blender GPT (ZH) 中文用戶專屬",
    "author": "Ryvn (@hc-psy) (@@hao-chenglo2049)",
    "description": "",
    "blender": (2, 82, 0),
    "version": (0, 0, 1),
    "location": "3D View (三維視圖) > UI (使用者介面) > BlenderGptZH",
    "warning": "",
    "category": "Object"
}

system_prompt = """You are an assistant made for the purposes of helping the user with Blender, the 3D software. 
- Respond with your answers in markdown (```). 
- Preferably import entire modules instead of bits. 
- Do not perform destructive operations on the meshes. 
- Do not use cap_ends. Do not do more than what is asked (setting up render settings, adding cameras, etc)
- Do not respond with anything that is not Python code.

Example:

user: create 10 cubes in random locations from -10 to 10
assistant:
```
import bpy
import random
bpy.ops.mesh.primitive_cube_add()

#how many cubes you want to add
count = 10

for c in range(0,count):
    x = random.randint(-10,10)
    y = random.randint(-10,10)
    z = random.randint(-10,10)
    bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
```"""


Classes = (BLENDERGPT_PT_PANEL, BLENDERGPT_OT_DEL_ALL_MSG, BLENDERGPT_OT_DEL_MSG,
           BLENDERGPT_OT_GPT_CODE, BLENDERGPT_OT_SEND_MSG, BLENDERGPT_AddonPreferences)


def init_props():
    bpy.types.Scene.history = bpy.props.CollectionProperty(
        type=bpy.types.PropertyGroup)

    bpy.types.Scene.model = bpy.props.EnumProperty(
        name="GPT模型",
        description="請選擇欲使用的Chat-GPT模型",
        items=[
            ("gpt3.5", "GPT-3.5 (便宜但較容易出錯)", "使用 GPT-3.5 (便宜但較容易出錯)"),
            ("gpt4", "GPT-4 (昂貴但較詳細準確)", "使用 GPT-4 (昂貴但較詳細準確)"),
        ],
        default="gpt3.5",
    )

    bpy.types.Scene.lan = bpy.props.EnumProperty(
        name="語言",
        description="請選擇Chat-GPT所回饋的語言",
        items=[
            ("traditional", "繁體中文", "繁體中文"),
            ("simplified", "简体中文", "简体中文"),
            ("english", "English", "英文"),
        ],
        default="traditional",
    )

    bpy.types.Scene.prompt_input = bpy.props.StringProperty(
        name="指令",
        description="請輸入你的指令",
        default="",
    )

    bpy.types.Scene.on_finish = bpy.props.BoolProperty(default=False)
    bpy.types.PropertyGroup.type = bpy.props.StringProperty()
    bpy.types.PropertyGroup.content = bpy.props.StringProperty()


def get_api_key(context, addon_name):
    preferences = context.preferences
    addon_prefs = preferences.addons[addon_name].preferences
    return addon_prefs.api_key


def clear_props():
    del bpy.types.Scene.history
    del bpy.types.Scene.model
    del bpy.types.Scene.prompt_input
    del bpy.types.Scene.on_finish


def register():
    for cls in Classes:
        bpy.utils.register_class(cls)

    init_props()


def unregister():
    for cls in Classes:
        bpy.utils.unregister_class(cls)

    clear_props()
