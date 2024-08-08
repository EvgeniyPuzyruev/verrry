import gradio as gr
import json
import random
from websockets_api import get_one_image
from pathlib import Path
from settings import PROJECT_FOLDER


def process_just_prompt(positive, high_res, style):
    workflow_json = Path(PROJECT_FOLDER)/'json/just_prompt.json'
    with open(workflow_json, 'r', encoding='utf-8') as f:
        workflow = json.load(f)
    workflow['6']['inputs']['text'] = positive
    workflow['3']['inputs']['seed'] = random.randint(1, 99999999999999)
    if high_res:
        workflow['5']['inputs']['width'] = 768
        workflow['5']['inputs']['height'] = 768
    if style == 'realism':
        style_model = 'epicrealism_pureEvolutionV5.safetensors'
    elif style == 'cartoon':
        style_model = 'toonyou_beta6.safetensors'
    elif style == 'magic':
        style_model = 'dreamshaper_8.safetensors'
    elif style == 'anime':
        style_model = 'counterfeitV30_v30.safetensors'
    elif style == '3D':
        style_model = 'disneyPixarCartoon_v10.safetensors'

    workflow['4']['inputs']['ckpt_name'] = style_model

    images = get_one_image(workflow)
    return images


just_prompt_interface = gr.Interface(
    fn=process_just_prompt,
    inputs=[
        gr.Textbox(label='Промпт(понимает только английский)',
                   info='''Просто пишите то что хотите получить,
                   разделяя тэги запятыми.
                   Например: tiger, early morning, middle-shot,
                   looking at camera, desert on background.'''),
        gr.Checkbox(label='high.res(wait_longer)'),
        gr.Dropdown(choices=['realism', 'cartoon', 'magic', 'anime', '3D'],
                    value='realism')
    ],
    outputs=['image']
)
