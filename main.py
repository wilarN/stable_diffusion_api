import json
import os.path

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
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    r = response.json()

    for i, img_data in enumerate(r['images']):
        image = Image.open(io.BytesIO(base64.b64decode(img_data.split(",", 1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + img_data
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))

        filename = f"output_{i}.png"
        final_save_location = os.path.join(output_dir, filename)
        image.save(final_save_location, pnginfo=pnginfo)
        print(f"Image saved as {filename}")


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
            "enable_hr": false,
            "denoising_strength": 0,
            "firstphase_width": 0,
            "firstphase_height": 0,
            "hr_scale": 2,
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
            "steps": 50,
            "cfg_scale": 7,
            "width": 512,
            "height": 512,
            "restore_faces": false,
            "tiling": false,
            "do_not_save_samples": false,
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
            "sampler_index": "Euler",
            "script_name": "",
            "send_images": true,
            "save_images": false,
            "alwayson_scripts": {}
        }
    except Exception as e:
        print(e)


if __name__ == '__main__':
    user_initial_selection()
    main()
