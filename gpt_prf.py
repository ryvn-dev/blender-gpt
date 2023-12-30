import bpy
from bpy import props
from bpy.types import AddonPreferences
from .gpt_cst import UI


class BLENDERGPT_AddonPreferences(AddonPreferences):
    bl_idname = "blender-gpt"

    openai_key: props.StringProperty(
        name="OPENAI API Key",
        description="Enter your OpenAI API Key",
        default="",
        subtype="PASSWORD",
    )

    languages = [
        ('en', "English", ""),
        ('es', "Español", ""),
        ('zh', "繁體中文", ""),
        ('cn', "简体中文", ""),
        ('fr', "Français", ""),
    ]
    language: props.EnumProperty(
        name="Language",
        items=languages,
        default='en',
        description="Select your preferred language",
        update=lambda self, context: self.update_language(context)
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "openai_key")
        layout.prop(self, "language", text="Language")

    def update_language(self, context):
        prefs = context.preferences.addons['blender-gpt'].preferences
        lan = prefs.language

        # model
        current_model = getattr(context.scene, "model", "gpt-3.5-turbo")

        bpy.types.Scene.model = bpy.props.EnumProperty(
            name=UI['label_model'][lan],
            description=UI['label_model_description'][lan],
            items=[
                ("gpt-3.5-turbo", UI['model_options'][lan]
                 ['gpt3.5'], UI['model_options'][lan]['gpt3.5']),
                ("gpt-4", UI['model_options'][lan]['gpt4'],
                 UI['model_options'][lan]['gpt4']),
            ],
            default=current_model,
        )
        setattr(context.scene, "model", current_model)

        # prompt_input
        current_prompt_input = getattr(context.scene, "prompt_input", "")

        bpy.types.Scene.prompt_input = bpy.props.StringProperty(
            name=UI['command'][lan],
            description=UI['command_instruction'][lan],
            default=current_prompt_input,
        )

        setattr(context.scene, "prompt_input", current_prompt_input)

        # creativity
        current_creativity = getattr(context.scene, "creativity", 0)

        bpy.types.Scene.creativity = bpy.props.FloatProperty(
            name=UI['creativity'][lan],
            description=UI['creativity'][lan],
            default=current_creativity,
            min=0,
            max=1,
        )

        setattr(context.scene, "creativity", current_creativity)
