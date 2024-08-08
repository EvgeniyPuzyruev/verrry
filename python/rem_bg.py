import gradio as gr
import json
from datetime import datetime
from websockets_api import get_prompt_images
from pathlib import Path
from settings import PROJECT_FOLDER
from PIL import Image


def save_input_image(img):
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    temp = f'{Path(PROJECT_FOLDER)}/input/rembg/temp.jpg'
    ts = f'{Path(PROJECT_FOLDER)}/input/rembg/img_{timestamp}.jpg'
    pillow_image = Image.fromarray(img)
    pillow_image.save(temp)
    pillow_image.save(ts)


def process_rem_bg(input_image):
    workflow_json = Path(PROJECT_FOLDER)/'json/rembg.json'
    with open(workflow_json, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    save_input_image(input_image)
    images = get_prompt_images(workflow)
    return images


rem_bg_interface = gr.Interface(
    fn=process_rem_bg,
    inputs=gr.Image(label='image', sources='upload'),
    outputs=[
        gr.Gallery(label='Вырезанное изображение и маска'),
            ],
    description='''Здесь можно вырезать картинку.
                   AI это не магия, поэтому если при взгляде на картинку
                   человеку не очевидно, что является главным объектом,
                   то и модель скорее всего не "догадается".'''
)
