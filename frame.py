#!/usr/bin/env python3
import os
import random
import time
from io import BytesIO
from os import path

import requests
import schedule
from dotenv import dotenv_values
from inky import auto
from pi_heif import register_heif_opener
from PIL import Image, ImageDraw, ImageOps

inky = auto(ask_user=False, verbose=True)
overlay = False
saturation = 0.5

image_folder = "/home/notedwin/src/images"
overlay = None
current_image = None
original_image = None
previous_image = None

canvas = Image.new("RGB", (inky.width, inky.height), color=(255, 255, 255))
canvas_draw = ImageDraw.Draw(canvas)

register_heif_opener()

c = dotenv_values(".env")


def pull_images():
    url = "http://192.168.0.220:2283"
    apikey = c["immich_api"]
    albumid = "c17bb978-9e6d-413a-8af5-9a41b9465b33"  # copy from url when accessing folder

    headers = {"Accept": "application/json", "x-api-key": apikey}

    # # Get the list of photos from the API using the albumid
    response = requests.get(url + "/api/albums/" + albumid, headers=headers)

    if response.status_code != 200:
        print("Failed to get album")
        exit()

    data = response.json()
    image_urls = data["assets"]
    imgs = []
    print(f"Found {len(image_urls)} images in album {albumid}")

    # Download each image from the URL and save it to the directory
    headers = {"Accept": "application/octet-stream", "x-api-key": apikey}

    # creaate images directory if it doesn't exist
    if not path.exists("images"):
        os.mkdir("images")

    for id in image_urls:
        asseturl = url + "/api/assets/" + str(id["id"]) + "/original"
        response = requests.get(asseturl, headers=headers)

        photo_path = f"images/{id['id']}.jpeg"
        imgs.append(id["id"])

        # Only download file if it doesn't already exist
        if path.exists(photo_path):
            print(f"File {photo_path} already exists")
            continue

        with open(photo_path, "wb") as f:
            # open response with pillow
            img = Image.open(BytesIO(response.content)).convert("RGB")
            img.save(f, format="jpeg")

        print(f"Downloaded {photo_path}")

    for file in os.listdir("images"):
        file = os.path.splitext(file)
        basename = file[0]
        if basename not in imgs:
            # delete the file
            os.remove(f"images/{basename}.jpeg")


def display():
    random_image = random.choice(os.listdir(image_folder))
    img = Image.open(os.path.join(image_folder, random_image)).convert("RGB")
    img = img.rotate(90)
    img = ImageOps.fit(img, (inky.width, inky.height))
    inky.set_border(inky.RED)
    inky.set_image(img, saturation=saturation)
    inky.show()


if __name__ == "__main__":
    schedule.every(60).seconds.do(display)
    schedule.every(60).minutes.do(pull_images)

    while True:
        n = schedule.idle_seconds()
        if n > 0:
            print(f"Sleeping for {n} seconds")
            time.sleep(n)
        schedule.run_pending()
