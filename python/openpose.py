import gradio as gr
import json
from datetime import datetime
from websockets_api import get_prompt_images
from pathlib import Path
from settings import PROJECT_FOLDER
from PIL import Image


def save_input_image(pose_img, face_img):
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    temp_pose = Path(PROJECT_FOLDER)/'input/openpose/temp_pose.jpg'
    input_pose = Path(PROJECT_FOLDER)/f'''input/openpose/pose_
                                          {timestamp}.jpg'''
    temp_face = Path(PROJECT_FOLDER)/'input/openpose/temp_face.jpg'
    input_face = Path(PROJECT_FOLDER)/f'''input/openpose/
                                          face_{timestamp}.jpg'''
    pillow_pose = Image.fromarray(pose_img)
    pillow_face = Image.fromarray(face_img)
    pillow_pose.save(input_pose)
    pillow_pose.save(temp_pose)
    pillow_face.save(input_face)
    pillow_face.save(temp_face)


def process_openpose(who, how_old, where, time, season, clothes, pose, face):
    workflow_json = Path(PROJECT_FOLDER)/'json/openpose_and_faceswapper.json'
    with open(workflow_json, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    if where == 'Mars':
        where = 'on a Mars planet'
    elif where == 'forest':
        where = 'in the forest'
    elif where == 'futuristic city':
        where = 'in the futuristic city'
    else:
        where = 'random place on background'

    positive = f'''{who}, {how_old}, {time}, {season}, {where},
                   (dressed in {clothes}):1.3'''
    workflow['6']['inputs']['text'] = positive
    save_input_image(pose, face)
    images = get_prompt_images(workflow)
    return images


openpose_interface = gr.Interface(
    title='Экспериментальная вкладка для генерации людей.',
    description='''Начнём с того,
                   что полученный результат будет в мультяшном 3D стиле,
                   похожем на Pixar. В меню выбирайте подходящие опции,
                   Во вкладке "pose" грузите любое изображение человека,
                   полученный персонаж примет именно эту позу.
                   Из вкладки "face" будет позаимствовано лицо.''',
    fn=process_openpose,
    inputs=[
        gr.Dropdown(label='who', choices=['man', 'woman'], value='man'),
        gr.Dropdown(label='how old', choices=['young', 'middle-aged', 'old'],
                    value='middle-aged'),
        gr.Dropdown(label='where',
                    choices=['Mars', 'forest', 'futuristic city', 'random'],
                    value='random'),
        gr.Dropdown(label='when',
                    choices=['early morning', 'sunny day',
                             'beautiful sunset', 'dark night'],
                    value='sunny day'),
        gr.Dropdown(label='season', 
                    choices=['spring', 'summer', 'autumn', 'winter'],
                    value='winter'),
        gr.Dropdown(label='clothes',
                    choices=['luxury suit', 'medieval armor',
                             'jack sparrow outfit', 'spider-man costume',
                             'naked'], value='luxury suit'),
        gr.Image(label='pose', sources='upload'),
        gr.Image(label='face', sources='upload'),],
    outputs=[
        gr.Gallery(label='output')],
)
