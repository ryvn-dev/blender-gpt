import bpy

from bpy.types import Panel
from .gpt_cst import UI


class BLENDERGPT_PT_PANEL(Panel):
    bl_label = 'Blender GPT'
    bl_idname = 'GPT_PT_PANEL'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blender GPT'

    def draw(self, context):
        addon_prefs = context.preferences.addons['blender-gpt'].preferences
        lan = addon_prefs.language

        layout = self.layout

        column = layout.column(align=True)

        # language youre using
        column.label(text=UI['label_language'][lan])

        column.separator()

        # model of chat gpt
        column.label(text=UI['label_model'][lan])
        column.prop(context.scene, "model", text="")

        column.separator()

        # creativity
        column.label(text=UI['creativity'][lan])
        column.prop(context.scene, "creativity", text="")

        column.separator()

        # history of chat
        if len(context.scene.history) > 0:
            column.label(text=UI['label_history'][lan])
            box = column.box()
            for index, message in enumerate(context.scene.history):
                if message.type == 'GPT':
                    row = box.row()
                    row.label(text="GPT>")

                    code_op = row.operator(
                        "gpt.gpt_code", text="", icon="TEXT", emboss=False)
                    code_op.code = message.content

                    if index == len(context.scene.history) - 1:
                        del_msg_op = row.operator(
                            'gpt.del_msg', text="", icon='TRASH', emboss=False)
                        del_msg_op.msg_idx = index

                else:
                    row = box.row()
                    row.label(
                        text=f"{UI['label_user'][lan]}{message.content}")

                    if index == len(context.scene.history) - 2:
                        del_msg_op = row.operator(
                            'gpt.del_msg', text="", icon='TRASH', emboss=False)
                        del_msg_op.msg_idx = index

        column.separator()

        # input of chat
        if len(context.scene.history) == 0 or (len(context.scene.history) > 0 and context.scene.history[-1].type != 'USER'):
            column.label(text=UI['command'][lan])
            column.prop(context.scene, "prompt_input", text="")

        # send message
        if len(context.scene.history) > 0 and context.scene.history[-1].type == 'USER':
            button_label = UI['button_send'][lan] if context.scene.on_finish else UI['button_regenerate'][lan]
        else:
            button_label = UI['button_send'][lan] if context.scene.on_finish else UI['button_submit'][lan]

        column.operator("gpt.send_msg", text=button_label, icon="PLAY")

        column.separator()
        column.operator("gpt.del_all_msg",
                        text=UI['button_delete_all'][lan], icon="TRASH")


def model_props_generator():
    addon_prefs = bpy.context.preferences.addons['blender-gpt'].preferences
    lan = addon_prefs.language

    return bpy.props.EnumProperty(
        name=UI['label_model'][lan],
        description=UI['label_model_description'][lan],
        items=[
            ("gpt-3.5-turbo", UI['model_options']['gpt3.5']
             [lan], UI['model_options']['gpt3.5'][lan]),
            ("gpt-4", UI['model_options']['gpt4']
             [lan], UI['model_options']['gpt4'][lan]),
        ],
        default="gpt-3.5-turbo",
    )


def prompt_input_generator():
    addon_prefs = bpy.context.preferences.addons['blender-gpt'].preferences
    lan = addon_prefs.language

    return bpy.props.StringProperty(
        name=UI['command'][lan],
        description=UI['command_instruction'][lan],
        default="",
    )


def temperature_generator():
    addon_prefs = bpy.context.preferences.addons['blender-gpt'].preferences
    lan = addon_prefs.language

    return bpy.props.FloatProperty(
        name=UI['creativity'][lan],
        description=UI['creativity'][lan],
        default=0,
        min=0,
        max=1,
    )


def props_initialization():
    bpy.types.Scene.history = bpy.props.CollectionProperty(
        type=bpy.types.PropertyGroup)

    bpy.types.Scene.model = model_props_generator()
    bpy.types.Scene.prompt_input = prompt_input_generator()
    bpy.types.Scene.creativity = temperature_generator()
    bpy.types.Scene.on_finish = bpy.props.BoolProperty(default=False)

    bpy.types.PropertyGroup.type = bpy.props.StringProperty()
    bpy.types.PropertyGroup.content = bpy.props.StringProperty()


def props_clear():
    del bpy.types.Scene.history
    del bpy.types.Scene.model
    del bpy.types.Scene.prompt_input
    del bpy.types.Scene.creativity
    del bpy.types.Scene.on_finish
