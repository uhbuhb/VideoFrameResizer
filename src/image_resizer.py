import os, sys
import PIL.Image

OUTPUT_SIZE = 128,128


def resize(image_path):
    im = PIL.Image.open(image_path)
    im.thumbnail(OUTPUT_SIZE)
    im.save(f"{image_path}.thumbnail.jpg")

resize("1.jpg")

    