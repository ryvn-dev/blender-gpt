import bpy

from bpy.types import Operator
import openai

from .gpt_gpt import chatgpt


class BLENDERGPT_OT_DEL_MSG(Operator):
    bl_idname = "gpt.del_msg"
    bl_label = "delete message"
    bl_description = "delete message"
    bl_options = {"REGISTER", "UNDO"}

    msg_idx: bpy.props.IntProperty(name="訊息索引", default=0)

    def execute(self, context):
        scene = context.scene
        history = scene.history
        history.remove(self.msg_idx)
        return {"FINISHED"}


class BLENDERGPT_OT_DEL_ALL_MSG(Operator):
    bl_idname = "gpt.del_all_msg"
    bl_label = "delete all messages"
    bl_description = "delete all messages"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        history = scene.history
        history.clear()
        return {"FINISHED"}


class BLENDERGPT_OT_GPT_CODE(Operator):
    bl_idname = "gpt.gpt_code"
    bl_label = "show GPT code"
    bl_description = "show GPT code"
    bl_options = {"REGISTER", "UNDO"}

    code: bpy.props.StringProperty(
        name="GPT Code", description="GPT Code", default="")

    def execute(self, context):

        # text area
        if int(context.scene.lan) == 0:
            txt_name = '指令腳本.py'
        elif int(context.scene.lan) == 1:
            txt_name = '指令脚本.py'
        else:
            txt_name = 'prompt_script.py'

        txt = bpy.data.texts.get(txt_name)

        if txt is None:
            txt = bpy.data.texts.new(txt_name)

        txt.clear()
        txt.write(self.code)

        txt_edit_area = None
        for area in bpy.context.screen.areas:
            if area.type == 'TEXT_EDITOR':
                txt_edit_area = area
                break

        if txt_edit_area is None:
            cxt_area = context.area
            for region in cxt_area.regions:
                if region.type == 'WINDOW':
                    bpy.ops.screen.area_split(
                        {'area': cxt_area, 'region': region}, direction='VERTICAL', factor=0.5)
                    break

            new_area = context.screen.areas[-1]
            new_area.type = 'TEXT_EDITOR'
            txt_edit_area = new_area

        txt_edit_area.spaces.active.text = txt

        return {"FINISHED"}


class BLENDERGPT_OT_SEND_MSG(Operator):
    bl_idname = "gpt.send_msg"
    bl_label = "send message"
    bl_description = "send message"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene

        # TODO: connect to GPT
        prf = context.preferences
        openai.api_key = prf.addons["blender-gpt"].preferences.openai_key

        if not openai.api_key:
            if int(context.scene.lan) == 0:
                self.report(
                    {'ERROR'}, "錯誤: 沒有偵測到 OPENAI API Key，請在插件設定中設定 OPENAI API Key")
            elif int(context.scene.lan) == 1:
                self.report(
                    {'ERROR'}, "错误: 没有检测到 OPENAI API Key，请在插件设置中设置 OPENAI API Key")
            else:
                self.report(
                    {'ERROR'}, "Error: No OPENAI API Key detected, please set OPENAI API Key in the add-on preferences")
            return {'CANCELLED'}

        scene.on_finish = True
        # bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

        lan = int(context.scene.lan)
        prompts = [scene.prompt_input_0,
                   scene.prompt_input_1, scene.prompt_input_2]

        if len(scene.history) == 0 or scene.history[-1].type == 'GPT':
            if prompts[lan] == "":
                if lan == 0:
                    self.report({'ERROR'}, f"錯誤: 請輸入指令")
                elif lan == 1:
                    self.report({'ERROR'}, f"错误: 请输入指令")
                else:
                    self.report({'ERROR'}, f"Error: Please enter the prompt")
                scene.on_finish = False
                return {'CANCELLED'}

        try:
            code_exe_blender = chatgpt(context)
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
            scene.on_finish = False
            return {'CANCELLED'}

        if len(scene.history) == 0 or scene.history[-1].type == 'GPT':
            msg = scene.history.add()
            msg.type = 'USER'
            msg.content = prompts[lan]
            scene.prompt_input_0 = ""
            scene.prompt_input_1 = ""
            scene.prompt_input_2 = ""

        if code_exe_blender:
            msg = scene.history.add()
            msg.type = 'GPT'
            msg.content = code_exe_blender

            global_namespace = globals().copy()

        try:
            exec(code_exe_blender, global_namespace)
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
            scene.on_finish = False
            return {'CANCELLED'}

        scene.on_finish = False
        return {"FINISHED"}
