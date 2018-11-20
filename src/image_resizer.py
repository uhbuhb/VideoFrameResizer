import os, sys
import PIL.Image
import ffmpeg
import argparse
import cv2
import numpy

OUTPUT_SIZE = 128,128


def resize(im):
    #im = PIL.Image.open(image_path)
    image = PIL.Image.fromarray(im)
    image.thumbnail(OUTPUT_SIZE)
    return numpy.asarray(image)

