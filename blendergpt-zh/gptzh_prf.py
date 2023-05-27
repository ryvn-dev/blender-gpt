from bpy import props
from bpy.types import AddonPreferences


class BLENDERGPT_AddonPreferences(AddonPreferences):
    bl_idname = __name__
    print(__name__)
    api_key: props.StringProperty(
        name="API Key",
        description="Enter your OpenAI API Key",
        default="",
        subtype="PASSWORD",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "api_key")
