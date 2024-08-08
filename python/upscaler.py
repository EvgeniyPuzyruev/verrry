import gradio as gr
import json
from datetime import datetime
from websockets_api import get_one_image
from pathlib import Path
from settings import PROJECT_FOLDER
from PIL import Image


def save_input_image(img):
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    temp_img = Path(PROJECT_FOLDER)/'input/upscale/temp.jpg'
    input_img = Path(PROJECT_FOLDER)/f'input/upscale/img_{timestamp}.jpg'
    pillow_image = Image.fromarray(img)
    pillow_image.save(input_img)
    pillow_image.save(temp_img)


def process_upscale(img, upscale, denoising):
    if upscale == '4x':
        workflow_json = Path(PROJECT_FOLDER)/'json/4x.json'
    else:
        workflow_json = Path(PROJECT_FOLDER)/'json/16x.json'
    with open(workflow_json, 'r', encoding='utf-8') as f:
        workflow = json.load(f)
    workflow['24']['inputs']['number'] = denoising

    save_input_image(img)
    image = get_one_image(workflow)
    return image


upscaler_interface = gr.Interface(
    fn=process_upscale,
    inputs=[
        gr.Image(label='image'),
        gr.Radio(info='', choices=[
            '4x', '16x'
            ],
            value='4x'),
        gr.Slider(label='fantasy',
                  minimum=0.1, maximum=0.5, value=0.2, step=0.05,
                  info='''Модели придётся "фантазировать",
                  дорисовывая изображения.
                  Слайдер отвечает за этот параметр.
                  Соответственно, при уменьшении значения,
                  полученное изображение будет больше походить на исходное.
                  При увеличении – качество апскейла будет выше.
                  Результат зависит от исходного изображения и прогнозируется
                  слабо(всё-таки это AI, а не интерполяция пикселей).
                  Значение по умолчанию – подходит чаще всего.
                  Экспериментируйте!''')
        ],
    outputs=['image'],
    description='''Не рекомендуется апскейлить изначально большие изображения,
                   так как время ожидания может быть долгим.
                   Максимальный размер стороны – 8192 пикселей.'''
)
