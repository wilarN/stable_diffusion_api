import json
import os.path
import random
import string
import time

import requests
import io
import base64
from PIL import Image, PngImagePlugin

false = False
true = True

global payload


url = "http://127.0.0.1:7860"

output_dir = "./output"


def main():
    all_images_generate = []

    print("Beginning generation... Please wait until it's finished...")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()

    for i, img_data in enumerate(r['images']):
        image = Image.open(io.BytesIO(base64.b64decode(img_data.split(",", 1)[0])))
        png_payload = {"image": "data:image/png;base64," + img_data}
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        filename = f"{random_string}.png"
        final_save_location = os.path.join(output_dir, filename)
        image.save(final_save_location, pnginfo=pnginfo)
        print(f"Image saved as {filename}")
        all_images_generate.append(filename)

    if continue_or_not("Upscale output? (Might take a tiny bit longer to process...)"):
        image_list = []
        for file in all_images_generate:
            with open(("./output/" + file), 'rb') as f:
                image_data = f.read()
                image_data_base64 = base64.b64encode(image_data).decode('utf-8')
                image_list.append({"data": image_data_base64, "name": os.path.basename(file)})
        upscale_payload = {
            "resize_mode": 0,
            "show_extras_results": False,
            "gfpgan_visibility": 0,
            "codeformer_visibility": 0,
            "codeformer_weight": 0,
            "upscaling_resize": 4,
            "upscaling_resize_w": 512,
            "upscaling_resize_h": 768,
            "upscaling_crop": False,
            "upscaler_1": "R-ESRGAN 4x+ Anime6B",
            "upscaler_2": "None",
            "extras_upscaler_2_visibility": 0,
            "upscale_first": False,
            "imageList": image_list
        }
        response = requests.post(url=f'{url}/sdapi/v1/extra-batch-images', json=upscale_payload)
        r = response.json()

        for i, img_data in enumerate(r['images']):
            image_name = os.path.splitext(os.path.basename(all_images_generate[i]))[0]
            image = Image.open(io.BytesIO(base64.b64decode(img_data.split(",", 1)[0])))
            png_payload = {"image": "data:image/png;base64," + img_data}
            response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)
            pnginfo = PngImagePlugin.PngInfo()
            pnginfo.add_text("parameters", response2.json().get("info"))
            # random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            filename = f"{image_name}_upscaled.png"
            final_save_location = os.path.join(output_dir, filename)
            image.save(final_save_location, pnginfo=pnginfo)

    path = os.path.realpath(output_dir)
    os.startfile(path)


def user_initial_selection():
    global payload
    os.system("cls")
    print("""
    #######################################
    #                                     #
    #          1) - Prompt                #
    #          2) - Amount                #
    #                                     #
    #######################################
    """)
    prompt_amount_usr = 1
    try:
        while True:
            prompt_usr = input("1) >> ")
            if len(prompt_usr.strip(" ")) < 5:
                print("Has to be longer than 5 chars.")
                continue

            prompt_amount_usr = input("2) >> ")
            if int(prompt_amount_usr) < 1 :
                print("Has to be more than ONE.")
                continue
            break

        payload = {
            "enable_hr": True,
            "denoising_strength": 0.7,
            "firstphase_width": 0,
            "firstphase_height": 0,
            "hr_scale": 1,
            "hr_upscaler": "Latent",
            "hr_second_pass_steps": 0,
            "hr_resize_x": 0,
            "hr_resize_y": 0,
            "prompt": f"{prompt_usr}",
            "styles": [
                ""
            ],
            "seed": -1,
            "subseed": -1,
            "subseed_strength": 0,
            "seed_resize_from_h": -1,
            "seed_resize_from_w": -1,
            "sampler_name": "DPM++ 2M Karras",
            "batch_size": int(prompt_amount_usr),
            "n_iter": 1,
            "steps": 20,
            "cfg_scale": 7,
            "width": 512,
            "height": 768,
            "restore_faces": true,
            "tiling": false,
            "do_not_save_samples": true,
            "do_not_save_grid": true,
            "negative_prompt": "bad hands, bad face, more fingers, bad legs, two people, multiple legs",
            "eta": 0,
            "s_min_uncond": 0,
            "s_churn": 0,
            "s_tmax": 0,
            "s_tmin": 0,
            "s_noise": 1,
            "override_settings": {},
            "override_settings_restore_afterwards": true,
            "script_args": [],
            "sampler_index": "DPM++ 2M Karras",
            "script_name": "",
            "send_images": true,
            "save_images": false,
            "alwayson_scripts": {}
        }


    except Exception as e:
        print(e)


def continue_or_not(text):
    while True:
        usr_anw = input(text)
        if usr_anw.lower().strip(" ").__contains__("n"):
            return False
        elif usr_anw.lower().strip(" ").__contains__("y"):
            return True
        else:
            pass


def clear():
    os.system("cls")


if __name__ == '__main__':
    while True:
        clear()
        user_initial_selection()
        main()
        if not continue_or_not("Again? (y/n)"):
            break
    bye_text = "Bye bye :) Come back sometime!"
    for i in bye_text:
        print(i, end="")
        time.sleep(0.01)

