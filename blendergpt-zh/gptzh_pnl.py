import bpy

from bpy.types import Panel


class BLENDERGPT_PT_PANEL(Panel):
    bl_label = 'Blender GPT ZH'
    bl_idname = 'GPT_PT_PANEL'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Blender GPT ZH'

    def draw(self, context):
        layout = self.layout

        column = layout.column(align=True)

        # language usage
        row = column.row(align=True)
        row.label(text="回饋語言：")
        row.prop(context.scene, "lan", text="")

        column.separator()

        # history of chat
        column.label(text="對話歷史紀錄：")
        box = column.box()
        for index, message in enumerate(context.scene.history):
            if message.type == 'GPT':
                row = box.row()
                row.label(text="GPT: ")
                show_code_op = row.operator(
                    "gpt.gpt_code", text="展示程式碼", icon="TEXT")
                show_code_op.code = message.content
                delete_message_op = row.operator(
                    'gpt.del_msg', text="", icon='TRASH', emboss=False)
                delete_message_op.msg_idx = index
            else:
                row = box.row()
                row.label(text=f"USER: {message.content}")
                delete_message_op = row.operator(
                    'gpt.del_msg', text="", icon='TRASH', emboss=False)
                delete_message_op.msg_idx = index

        column.separator()

        # model of chat gpt
        column.label(text="Chat-GPT 模型：")
        column.prop(context.scene, "model", text="")

        # input of chat
        column.label(text="指令：")
        column.prop(context.scene, "prompt_input", text="")

        button_label = "請稍候，模型正在編寫腳本..." if context.scene.on_finish else "送出指令"

        row = column.row(align=True)
        row.operator("gpt.send_msg", text=button_label)
        row.operator("gpt.del_all_msg", text="Clear Chat")

        column.separator()
