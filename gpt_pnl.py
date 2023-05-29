import bpy

from bpy.types import Panel


UI_lan = {
    'language': ['繁體中文', '简体中文', 'English'],
    'label_language': ['語言', '语言', 'Language'],
    'label_model': ['Chat-GPT 模型', 'Chat-GPT 模型', 'Chat-GPT Model'],
    'label_model_description': ['請選擇欲使用的Chat-GPT模型', '请选择要使用的Chat-GPT模型', 'Please select the Chat-GPT model'],
    'model_options': {
        'gpt3.5': ['GPT-3.5 (便宜但較容易出錯)', 'GPT-3.5 (便宜但較容易出错)', 'GPT-3.5 (Affordable but less accurate)'],
        'gpt4': ['GPT-4 (昂貴但較詳細準確)', 'GPT-4 (昂贵但较详细准确)', 'GPT-4 (Expensive but more accurate)'],
    },
    'label_history': ['對話歷史紀錄', '对话历史纪录', 'Chat History'],
    'label_show_code': ['顯示程式碼', '显示代码', 'Show Code'],
    'label_user': ['指令>', '指令>', 'Prompt>'],
    'button_send': ['請稍候，模型正在編寫腳本...', '请稍候，模型正在编写脚本...', 'Please wait, the model is writing the script...'],
    'button_submit': ['送出指令', '提交指令', 'Submit Prompt'],
    'button_regenerate': ['重新生成', '重新生成', 'Regenerate Response'],
    'command': ['指令', '指令', 'Prompt'],
    'command_instruction': ['請輸入指令', '请输入指令', 'Please enter the command'],
    'button_delete_all': ['刪除所有對話', '删除所有对话', 'Delete History'],
    'button_delete': ['刪除此回答', '删除此回答', 'Delete This Response'],
    'creativity': ['創意度', '创意度', 'Creativity'],
}


class BLENDERGPT_PT_PANEL(Panel):
    bl_label = 'Blender GPT'
    bl_idname = 'GPT_PT_PANEL'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blender GPT'

    def draw(self, context):
        layout = self.layout

        lan_idx = int(context.scene.lan)

        column = layout.column(align=True)

        # language usage
        row = column.row(align=True)
        row.label(text=UI_lan['label_language'][lan_idx])
        row.prop(context.scene, "lan", text="")

        column.separator()

        # model of chat gpt
        column.label(text=UI_lan['label_model'][lan_idx])
        if lan_idx == 0:
            column.prop(context.scene, "model_0", text="")
        elif lan_idx == 1:
            column.prop(context.scene, "model_1", text="")
        else:
            column.prop(context.scene, "model_2", text="")

        column.separator()

        # creativity
        column.label(text=UI_lan['creativity'][lan_idx])
        if lan_idx == 0:
            column.prop(context.scene, "t_0", text="")
        elif lan_idx == 1:
            column.prop(context.scene, "t_1", text="")
        else:
            column.prop(context.scene, "t_2", text="")

        column.separator()
        # history of chat
        if len(context.scene.history) > 0:
            column.label(text=UI_lan['label_history'][lan_idx])
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
                        text=f"{UI_lan['label_user'][lan_idx]}{message.content}")

                    if index == len(context.scene.history) - 2:
                        del_msg_op = row.operator(
                            'gpt.del_msg', text="", icon='TRASH', emboss=False)
                        del_msg_op.msg_idx = index

        column.separator()

        # input of chat
        if len(context.scene.history) == 0 or (len(context.scene.history) > 0 and context.scene.history[-1].type != 'USER'):
            column.label(text=UI_lan['command'][lan_idx])
            if lan_idx == 0:
                column.prop(context.scene, "prompt_input_0", text="")
            elif lan_idx == 1:
                column.prop(context.scene, "prompt_input_1", text="")
            else:
                column.prop(context.scene, "prompt_input_2", text="")

        # send message
        if len(context.scene.history) > 0 and context.scene.history[-1].type == 'USER':
            button_label = UI_lan['button_send'][lan_idx] if context.scene.on_finish else UI_lan['button_regenerate'][lan_idx]
        else:
            button_label = UI_lan['button_send'][lan_idx] if context.scene.on_finish else UI_lan['button_submit'][lan_idx]

        column.operator("gpt.send_msg", text=button_label, icon="PLAY")

        column.separator()
        column.operator("gpt.del_all_msg",
                        text=UI_lan['button_delete_all'][lan_idx], icon="TRASH")


def model_props_generator(idx):
    return bpy.props.EnumProperty(
        name=UI_lan['label_model'][idx],
        description=UI_lan['label_model_description'][idx],
        items=[
            ("gpt-3.5-turbo", UI_lan['model_options']['gpt3.5']
             [idx], UI_lan['model_options']['gpt3.5'][idx]),
            ("gpt-4", UI_lan['model_options']['gpt4']
             [idx], UI_lan['model_options']['gpt4'][idx]),
        ],
        default="gpt-3.5-turbo",
    )


def prompt_input_generator(idx):
    return bpy.props.StringProperty(
        name=UI_lan['command'][idx],
        description=UI_lan['command_instruction'][idx],
        default="",
    )


bpy.props.StringProperty(
    name="a",
    description="a",
    default="",
)


def temperature_generator(idx):
    return bpy.props.FloatProperty(
        name=UI_lan['creativity'][idx],
        description=UI_lan['creativity'][idx],
        default=0,
        min=0,
        max=1,
    )


def props_initialization():

    bpy.types.Scene.history = bpy.props.CollectionProperty(
        type=bpy.types.PropertyGroup)

    bpy.types.Scene.lan = bpy.props.EnumProperty(
        name="語言",
        description="請選擇語言",
        items=[
            ("0", "繁體中文", "繁體中文"),
            ("1", "简体中文", "简体中文"),
            ("2", "English", "英文"),
        ],
        default="0",
    )

    bpy.types.Scene.model_0 = model_props_generator(0)
    bpy.types.Scene.model_1 = model_props_generator(1)
    bpy.types.Scene.model_2 = model_props_generator(2)

    bpy.types.Scene.prompt_input_0 = prompt_input_generator(0)
    bpy.types.Scene.prompt_input_1 = prompt_input_generator(1)
    bpy.types.Scene.prompt_input_2 = prompt_input_generator(2)

    bpy.types.Scene.t_0 = temperature_generator(0)
    bpy.types.Scene.t_1 = temperature_generator(1)
    bpy.types.Scene.t_2 = temperature_generator(2)

    bpy.types.Scene.on_finish = bpy.props.BoolProperty(default=False)

    bpy.types.PropertyGroup.type = bpy.props.StringProperty()
    bpy.types.PropertyGroup.content = bpy.props.StringProperty()


def props_clear():
    del bpy.types.Scene.history
    del bpy.types.Scene.lan
    del bpy.types.Scene.model_0
    del bpy.types.Scene.model_1
    del bpy.types.Scene.model_2
    del bpy.types.Scene.prompt_input_0
    del bpy.types.Scene.prompt_input_1
    del bpy.types.Scene.prompt_input_2
    del bpy.types.Scene.t_0
    del bpy.types.Scene.t_1
    del bpy.types.Scene.t_2
    del bpy.types.Scene.on_finish
