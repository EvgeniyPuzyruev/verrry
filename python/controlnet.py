import gradio as gr
import json
from datetime import datetime
from websockets_api import get_one_image
from pathlib import Path
from settings import PROJECT_FOLDER
from PIL import Image


def save_input_image(img):
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    temp_img = Path(PROJECT_FOLDER)/'input/controlnet/temp.jpg'
    input_img = Path(PROJECT_FOLDER)/f'input/controlnet/img_{timestamp}.jpg'
    pillow_image = Image.fromarray(img)
    pillow_image.save(input_img)
    pillow_image.save(temp_img)


def process_controlnet(img, positive, strength):
    workflow_json = Path(PROJECT_FOLDER)/'json/controlnet.json'
    with open(workflow_json, 'r', encoding='utf-8') as f:
        workflow = json.load(f)
    workflow['29']['inputs']['text'] = positive
    workflow['54']['inputs']['number'] = 1 - strength
    save_input_image(img)
    image = get_one_image(workflow)
    return image


controlnet_interface = gr.Interface(
    fn=process_controlnet,
    inputs=[gr.Image(label='''Загружайте сюда исходное изображение.
                     Оно будет обрезано до квадрата.
                     Это вынужденная оптимизация, извините.''',),
            gr.Textbox(label='Промпт(понимает только английский)',
                       info='''Тут описываем необходмиые изменения.
                       Например: "Starry night" погрузит происходящее
                       в звёздную ночь,
                       а "Snowy mountain on background" дорисует
                       заснеженные горы на фоне'''),
            gr.Slider(label='Fantasy', info='''
                       Чем выше значение данного слайдера
                      тем больше вероятность получить то,
                      что написано в промпте,
                      но и расхождения и источником будут выше.
                      Соответственно, чем значения ниже, тем картинку будет
                      больше похожа на источник,
                      но и места изменениям будет меньше.
                      Экспериментируйте!''',
                      minimum=0.1, maximum=0.9, value=0.7, step=0.05)],
    outputs=[gr.Image(label='Изменённое изображение')],
)
