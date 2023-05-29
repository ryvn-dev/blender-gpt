import openai
import re


def SYS_MAIN_PROMPT(language): return f"""
I want you to act as a professional 3D artist who is proficient in writing scripts in Blender, the 3D software.
Here are some rules you have to heed and follow:
- Respond with your answers in markdown (```).
- Preferably import entire modules instead of bits.
- Do not perform destructive operations on the meshes.
- Do not use cap_ends. Do not do more than what is asked (setting up render settings, adding cameras, etc)
- Do not respond with anything that is not Python code.
- Please write comments in {language}.
"""


EX_1_USER = """create 10 cubes in random locations from -1 to 1"""

EX_1_ASSISTANT = """```
import bpy
import random
bpy.ops.mesh.primitive_cube_add()

count = 10

for _ in range(count):
    x = random.randint(-1,1)
    y = random.randint(-1,1)
    z = random.randint(-1,1)
    bpy.ops.mesh.primitive_cube_add(location=(x,y,z))
```"""

EX_2_USER = """delete all mesh objects in the scene and create a 5x5x5 ball in the scence"""

EX_2_ASSISTANT = """```
import bpy

bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0), radius=2.5)
```"""


def post_process(final_txt):
    final_txt = re.findall(
        r'```(.*?)```', final_txt, re.DOTALL)[0]

    final_txt = re.sub(
        r'^python', '', final_txt, flags=re.MULTILINE)

    return final_txt


def chatgpt(context):
    scene = context.scene
    lan = int(scene.lan)

    languages = ['traditional chinese', 'simplified chinese', 'english']
    models = [scene.model_0, scene.model_1, scene.model_2]
    prompts = [scene.prompt_input_0,
               scene.prompt_input_1, scene.prompt_input_2]
    temperatures = [scene.t_0,
                    scene.t_1, scene.t_2]

    # sys data preparation
    messages = [{"role": "system", "content": SYS_MAIN_PROMPT(languages[lan])}]
    messages.append(
        {"role": "system", "name": "example_user", "content": EX_1_USER})
    messages.append(
        {"role": "system", "name": "example_assistant", "content": EX_1_ASSISTANT})
    messages.append(
        {"role": "system", "name": "example_user", "content": EX_2_USER})
    messages.append(
        {"role": "system", "name": "example_assistant", "content": EX_2_ASSISTANT})

    # add previous messages
    for msg in scene.history[-8:]:
        if msg.type == "GPT":
            messages.append(
                {"role": "assistant", "content": "```\n" + msg.content + "\n```"})
        else:
            messages.append({"role": "user",
                            "content": msg.content})

    if messages[-1]["role"] != "user":
        # add the current user message
        messages.append({"role": "user", "content": "Please provide me with Blender (3D software) code regarding the following task: " +
                        prompts[lan] + ". \n. Do not respond with anything that is not Python code. Do not provide explanations. " + f"Wite code comment in {languages[lan]}."})

    response = openai.ChatCompletion.create(
        model=models[lan],
        messages=messages,
        temperature=temperatures[lan],
        # stream=True,
        max_tokens=2000,
    )

    try:
        # events = []
        # final_txt = ''

        # # becuase stream = true so use delta to concatentate
        # for e in response:
        #     if len(e['choices'][0]['delta']) == 0:
        #         continue

        #     if 'role' in e['choices'][0]['delta']:
        #         continue

        #     events.append(e)
        #     event_text = e['choices'][0]['delta']['content']
        #     final_txt += event_text
        #     print(final_txt, flush=True, end='\r')

        # return post_process(final_txt)

        final_txt = response['choices'][0]['message']['content']

        return post_process(final_txt)

    except IndexError:
        return None
