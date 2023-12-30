SYSTEMPROMPTS = [
    """
    I am acting as a professional 3D artist skilled in scripting within Blender, the 3D software. My expertise lies in understanding the relationship between conceptual 3D models, animation ideas, and their corresponding Python scripts in Blender.
    Here are the guidelines for our interaction:
    - I will only respond with Python code relevant to Blender scripting, enclosed in markdown code blocks (```).
    - My responses will focus on importing complete modules rather than individual components for scripting.
    - I'll ensure to avoid destructive operations on meshes in my code suggestions.
    - My responses will strictly adhere to the task at hand. I won't include additional setup like render settings or camera additions unless explicitly requested.
    - My replies will consist solely of Python code without any additional explanations or comments.
    - The input provided might be in English, Traditional Chinese and Simplified Chinese, and I will respond accordingly.
    This setup is designed for a tailor-made Blender GPT to assist with 3D modeling and animation scripting in Python.
    """,
    """
    Here are a few examples to illustrate how I can assist:
    1. Task: Create 10 Cubes in Random Locations
    - User Prompt Content: "Create 10 cubes in random locations from -1 to 1"
    - Assistant Response Content:
        ```python
        import bpy
        import random

        count = 10
        for _ in range(count):
            x = random.uniform(-1, 1)
            y = random.uniform(-1, 1)
            z = random.uniform(-1, 1)
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        ```

    2. Task: Delete All Mesh Objects and Create a Sphere
    - User Prompt Content: Delete all mesh objects in the scene and create a 5x5x5 ball in the scene
    - Assistant Response Content:
        ```python
        import bpy

        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='MESH')
        bpy.ops.object.delete()

        bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0), radius=2.5)
        ```

    3. Task: Create a Rigid Body Simulation with a Tower of Cubes
    - User Prompt Content: "Create a rigid body sim with 10 1x1x1 cubes stacked as a tower that falls down onto a 20x20 plane"
    - Assistant Response Content:
        ```python
        import bpy

        for i in range(10):
            bpy.ops.mesh.primitive_cube_add(location=(0, 0, 1 + i))
            bpy.ops.rigidbody.object_add()
            bpy.context.object.scale = (1, 1, 1)

        bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0))
        bpy.ops.rigidbody.object_add()
        bpy.context.object.rigid_body.type = 'PASSIVE'
        bpy.context.object.scale = (20, 20, 1)

        bpy.context.scene.frame_end = 200
        ```
    """
]

UI = {
    'language': {
        'zh': '繁體中文',
        'cn': '简体中文',
        'en': 'English',
        'es': 'Español',
        'fr': 'Français',
    },
    'label_language': {
        'zh': '語言',
        'cn': '语言',
        'en': 'Language',
        'es': 'Idioma',
        'fr': 'Langue',
    },
    'label_model': {
        'zh': 'GPT 模型',
        'cn': 'GPT 模型',
        'en': 'GPT Model',
        'es': 'Modelo GPT',
        'fr': 'Modèle GPT',
    },
    'label_model_description': {
        'zh': '請選擇欲使用的GPT模型',
        'cn': '请选择要使用的GPT模型',
        'en': 'Please select the GPT model',
        'es': 'Por favor seleccione el modelo GPT',
        'fr': 'Veuillez sélectionner le modèle GPT',
    },
    'model_options': {
        'zh': {
            'gpt3.5': 'GPT-3.5 (便宜但較容易出錯)',
            'gpt4': 'GPT-4 (昂貴但較詳細準確)',
        },
        'cn': {
            'gpt3.5': 'GPT-3.5 (便宜但較容易出错)',
            'gpt4': 'GPT-4 (昂贵但较详细准确)',
        },
        'en': {
            'gpt3.5': 'GPT-3.5 (Affordable but less accurate)',
            'gpt4': 'GPT-4 (Expensive but more accurate)',
        },
        'es': {
            'gpt3.5': 'GPT-3.5 (Asequible pero menos preciso)',
            'gpt4': 'GPT-4 (Caro pero más preciso)',
        },
        'fr': {
            'gpt3.5': 'GPT-3.5 (Abordable mais moins précis)',
            'gpt4': 'GPT-4 (Coûteux mais plus précis)',
        },
    },
    'label_history': {
        'zh': '對話歷史紀錄',
        'cn': '对话历史纪录',
        'en': 'Chat History',
        'es': 'Historial de chat',
        'fr': 'Historique du chat',
    },
    'label_show_code': {
        'zh': '顯示程式碼',
        'cn': '显示代码',
        'en': 'Show Code',
        'es': 'Mostrar código',
        'fr': 'Afficher le code',
    },
    'label_user': {
        'zh': '指令>',
        'cn': '指令>',
        'en': 'Prompt>',
        'es': 'Indicación>',
        'fr': 'Indication>',
    },
    'button_send': {
        'zh': '請稍候，模型正在編寫腳本...',
        'cn': '请稍候，模型正在编写脚本...',
        'en': 'Please wait, the model is writing the script...',
        'es': 'Por favor espere, el modelo está escribiendo el script...',
        'fr': 'Veuillez patienter, le modèle écrit le script...',
    },
    'button_submit': {
        'zh': '送出指令',
        'cn': '提交指令',
        'en': 'Submit Prompt',
        'es': 'Enviar indicación',
        'fr': 'Soumettre l\'indication',
    },
    'button_regenerate': {
        'zh': '重新生成',
        'cn': '重新生成',
        'en': 'Regenerate Response',
        'es': 'Regenerar respuesta',
        'fr': 'Régénérer la réponse',
    },
    'command': {
        'zh': '指令',
        'cn': '指令',
        'en': 'Prompt',
        'es': 'Indicación',
        'fr': 'Indication',
    },
    'command_instruction': {
        'zh': '請輸入指令',
        'cn': '请输入指令',
        'en': 'Please enter the command',
        'es': 'Por favor ingrese la indicación',
        'fr': 'Veuillez entrer l\'indication',
    },
    'button_delete_all': {
        'zh': '刪除所有對話',
        'cn': '删除所有对话',
        'en': 'Delete History',
        'es': 'Eliminar historial',
        'fr': 'Supprimer l\'historique',
    },
    'button_delete': {
        'zh': '刪除此回答',
        'cn': '删除此回答',
        'en': 'Delete This Response',
        'es': 'Eliminar esta respuesta',
        'fr': 'Supprimer cette réponse',
    },
    'creativity': {
        'zh': '創意度',
        'cn': '创意度',
        'en': 'Creativity',
        'es': 'Creatividad',
        'fr': 'Créativité',
    },
    'no_openai_key_error': {
        'zh': '錯誤: 沒有偵測到 OPENAI API Key，請在插件設定中設定 OPENAI API Key',
        'cn': '错误: 没有检测到 OPENAI API Key，请在插件设置中设置 OPENAI API Key',
        'en': 'Error: No OPENAI API Key detected, please set OPENAI API Key in the add-on preferences',
        'es': 'Error: No se detectó ninguna clave de API de OPENAI, configure la clave de API de OPENAI en las preferencias del complemento',
        'fr': 'Erreur: aucune clé API OPENAI détectée, veuillez définir la clé API OPENAI dans les préférences du module complémentaire',
    },
    'no_prompt_error': {
        'zh': '錯誤: 請輸入指令',
        'cn': '错误: 请输入指令',
        'en': 'Error: Please enter the prompt',
        'es': 'Error: Por favor ingrese la indicación',
        'fr': 'Erreur: Veuillez entrer l\'indication',
    },
}
