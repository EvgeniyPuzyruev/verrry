# Verrry project
** **
[Watch the video](https://github.com/EvgeniyPuzyruev/verrry/blob/master/exp.mp4)
** **
## Using local installed ComfyUI graphic interface for Stable Diffusion, Gradio web-interface for demonstration some skills and opportunities(mine and genertive AI)
**Disclaimer** *This project was created for fun and in order to better understand the interaction of Comfy, gradio and python. I am not programmer, developer or somebody like that so something can break, stop working correctly, and I have no idea how it works under heavy load(more than one user, huh)*
### Description ###
Basically, it works like this:
-  Launch of local installed ComfyUI interface(it automatically opens in browser in http://127.0.0.1:8188/) 
-  Launch of file main.py, it startes gradio interface with sub-interfaces for every tab
(main.py links to .py files like “just_prompt_interface”, “rem_bg_interface” etc)
** **
*Explanation how every interface works on example* 
-  gr.Interface requires 3 arguments: input, output and function which converts first to second.
When we upload image it saves locally to specific subfolder in project folder
(Link to this folder in file settings.py). Image saves twice: with temp name for further interactions and timestamp name for archive.
The most important link in process_ function is .json file. It links comfyui workflow saved as .json with web-interface so we can make input or change workflow’s parameters in gradio(image, textbox, slider, dropdown etc). Then get_prompt_images or get_one_image from websockets.api executes workflow and outputs results. That’s it!
## About each interface in more detail ##
### Just_prompt interface ###
![Alt Text](https://github.com/EvgeniyPuzyruev/verrry/blob/master/screenshots/just_prompt.png)
Creates image using epic_realism checkpoint. If we tick checkbocks high.res, resolution of output will be increased from 512 to 768 on every side.
** **
### Rem_bg interface ###
![Alt Text](https://github.com/EvgeniyPuzyruev/verrry/blob/master/screenshots/rembg.png)
Accepts image in any format(includes webp) and using BRIA_REMBG model separates main object from background. You also receive alpha map for post-production.
** **
### Upscale interface ###
![Alt Text](https://github.com/EvgeniyPuzyruev/verrry/blob/master/screenshots/upscale.png)
Actually there are two similar workflows. SD_upscale method works but in case of 16x it works twice(of course, it takes more time). We use universal 4x-ESRGAN model and able to change denoise factor. If denoise factor is low output will be looks like
input but quality of upscaling will be mediocre too. In case of high denoise factor result of upscailing will be good but you'll see differences between input and output.
** **
### Controlnet interface ###
![Alt Text](https://github.com/EvgeniyPuzyruev/verrry/blob/master/screenshots/controlnet.png)
Uses input image for creating depth map and contour with midas and canny_edge controlnets. Fantasy slider defines how it will limit changes from prompt. For example, if we want to change color or add snow on image little fantasy is correct. If we would like to add some object better to use higher fantasy factor to brake through maps's limitaions.
### Openpose and faceswapper interface ###
![Alt Text](https://github.com/EvgeniyPuzyruev/verrry/blob/master/screenshots/openpose.png)
It's joke but demonstates such powerful instruments as openpose and faceswapper. Basic model is 3d/pixar style and output resolution is 768x768. Dropdown menus are just handy way to add choosen word to prompt. Openpose controlnet defines pose of output charcter. Before output saving ReActor changes face.

