import os
import random
import time
from datetime import datetime

from gpiozero import Button
from inky import auto
from PIL import Image, ImageDraw, ImageFont

inky = auto(ask_user=False, verbose=True)
overlay = False
saturation = 0.5

image_folder = "/home/notedwin/Pictures"
overlay = None
current_image = None
original_image = None
previous_image = None

rotate = True

OVERLAY_BUTTON = Button(5)
NEXT_BUTTON = Button(6)
PREV_BUTTON = Button(16)  # find actual pin
STOP_BUTTON = Button(24)


def handle_overlay():
    global overlay, current_image, original_image
    overlay = not overlay
    print(f"Overlay Enabled: {overlay}")

    if overlay:
        original_image = current_image.copy()  # Save a copy of the original image
        current_time = datetime.now().strftime("%H:%M:%S")
        draw = ImageDraw.Draw(current_image)
        font = ImageFont.load_default()
        draw.rectangle(
            [inky.width / 4, inky.height / 4, 3 * inky.width / 4, 3 * inky.height / 4],
            inky.BLUE,
        )
        # write "Hello, World!" in the middle of the screen
        draw.text(
            (inky.width / 2, inky.height / 2),
            "Hello, World!" + current_time,
            inky.BLUE,
            font,
        )
        # write 4 "<-- Overlay" on the 20 pixels from left side of the screen and every 20 pixels from the top
        for i in range(4):
            draw.text((5, 110 * i + 50), "<-- Overlay", inky.WHITE, font)
            # draw a small rectangle around the text
            draw.rectangle(
                [0, 110 * i + 25, 25, 110 * i + 50 + 25],
                inky.WHITE,
            )
    else:
        if original_image is not None:
            current_image = (
                original_image
            )  # Replace the current image with the original one

    inky.set_border(inky.RED)
    inky.set_image(current_image, saturation=saturation)
    inky.show()


def custom_sleep(x):
    start_time = time.time()
    while True:
        if time.time() - start_time >= x:
            break  # If yes, exit the loop

        if OVERLAY_BUTTON.is_pressed:
            handle_overlay()
        if NEXT_BUTTON.is_pressed:
            break
        if PREV_BUTTON.is_pressed:
            break
        if STOP_BUTTON.is_pressed:
            global rotate
            rotate = not rotate  # Toggle the rotation
            print(f"Rotation {'Enabled' if rotate else 'Disabled'}")

        time.sleep(0.002)

    print(f"Slept for {x} seconds. Exiting custom_sleep function.")


def display_random_image():
    global current_image, previous_image
    # keep track of previous image
    if current_image is not None:
        previous_image = current_image

    random_image = random.choice(os.listdir(image_folder))
    img = Image.open(os.path.join(image_folder, random_image)).convert("RGB")
    img = img.rotate(90)
    current_image = img.resize((inky.width, inky.height))
    inky.set_border(inky.RED)
    inky.set_image(current_image, saturation=saturation)
    inky.show()


# untested
# def display_random_image(img=None):
# global current_image, previous_image
# # keep track of previous image
# if current_image is not None:
#     previous_image = current_image
# if not img:
#     random_image = random.choice(os.listdir(image_folder))
#     img = Image.open(os.path.join(image_folder, random_image)).convert("RGB")
#     img = img.rotate(90).resize((inky.width, inky.height))
# current_image = img
# inky.set_border(inky.RED)
# inky.set_image(current_image, saturation=saturation)
# inky.show()

if __name__ == "__main__":
    display_random_image()

    while True:
        if rotate:
            custom_sleep(75)
            display_random_image()
        else:
            custom_sleep(100)
