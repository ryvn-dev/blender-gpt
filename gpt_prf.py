from bpy import props
from bpy.types import AddonPreferences


class BLENDERGPT_AddonPreferences(AddonPreferences):
    bl_idname = "blender-gpt"

    openai_key: props.StringProperty(
        name="OPENAI API Key",
        description="Enter your OpenAI API Key",
        default="",
        subtype="PASSWORD",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "openai_key")
