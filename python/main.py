import gradio as gr
from just_prompt import just_prompt_interface
from rem_bg import rem_bg_interface
from upscaler import upscaler_interface
from controlnet import controlnet_interface
from openpose import openpose_interface


demo = gr.TabbedInterface(
    interface_list=[
        just_prompt_interface, rem_bg_interface, upscaler_interface,
        controlnet_interface, openpose_interface
        ],
    tab_names=[
        'just_prompt', 'rem_bg', 'upscale', 'controlnet', 'openpose'
        ]
)


demo.queue()
demo.launch(share=True)
