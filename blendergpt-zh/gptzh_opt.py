import bpy

from bpy.types import Operator


class BLENDERGPT_OT_DEL_MSG(Operator):
    bl_idname = "gpt.del_msg"
    bl_label = "刪除訊息"
    bl_description = "刪除訊息"
    bl_options = {"REGISTER", "UNDO"}

    msg_idx: bpy.props.IntProperty(name="訊息索引", default=0)

    def execute(self, context):
        scene = context.scene
        history = scene.history
        history.remove(self.msg_idx)
        return {"FINISHED"}


class BLENDERGPT_OT_DEL_ALL_MSG(Operator):
    bl_idname = "gpt.del_all_msg"
    bl_label = "刪除所有訊息"
    bl_description = "刪除所有訊息"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        history = scene.history
        history.clear()
        return {"FINISHED"}


class BLENDERGPT_OT_GPT_CODE(Operator):
    bl_idname = "gpt.gpt_code"
    bl_label = "展示GPT程式碼"
    bl_description = "展示GPT程式碼"
    bl_options = {"REGISTER", "UNDO"}

    code: bpy.props.StringProperty(
        name="GPT程式碼", description="GPT所產生的程式碼", default="")

    def execute(self, context):
        # text area
        txt_name = '指令腳本.py'
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

        cxt_area = context.area
        for region in cxt_area.regions:
            if region.type == 'WINDOW':
                override = {'area': cxt_area, 'region': region}
                bpy.ops.screen.area_split(
                    override, direction='VERTICAL', factor=0.5)
                break

        new_area = context.screen.areas[-1]
        new_area.type = 'TEXT_EDITOR'

        if txt_edit_area is None:
            txt_edit_area = new_area

        txt_edit_area.spaces.active.text = txt

        return {"FINISHED"}


class BLENDERGPT_OT_SEND_MSG(Operator):
    bl_idname = "gpt.send_msg"
    bl_label = "送出訊息"
    bl_description = "送出訊息"
    bl_options = {"REGISTER", "UNDO"}

    prompt_input: bpy.props.StringProperty(
        name="指令", description="指令", default="")

    def execute(self, context):
        # TODO: connect to GPT

        scene = context.scene

        scene.on_finish = True
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

        blender_code = "print('Hello World')"  # TODO: get from GPT

        msg = scene.history.add()
        msg.type = 'USER'
        msg.content = scene.prompt_input

        # clear prompt input
        scene.prompt_input = ""

        if blender_code:
            msg = scene.history.add()
            msg.type = 'GPT'
            msg.content = blender_code

            global_namespace = globals().copy()

        try:
            exec(blender_code, global_namespace)
        except Exception as e:
            self.report({'ERROR'}, f"Error: {e}")
            scene.on_finish = False
            return {'CANCELLED'}

        scene.on_finish = False
        return {"FINISHED"}
