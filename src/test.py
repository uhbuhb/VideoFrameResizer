import pickle

import cv2, argparse
import rpyc

from src.image_resizer import resize



def export_video_frames(filename):
    remote_connection = rpyc.connect("localhost", 18861)
    vidcap = cv2.VideoCapture(in_filename)
    count = 0
    success, image = vidcap.read()
    while success:
        binary_image = pickle.dumps(image)
        resized_image_binary = remote_connection.root.exposed_resize(binary_image)
        resized_image = pickle.loads(resized_image_binary)
        cv2.imwrite(f"frames/frame{count}original.jpg", image)
        cv2.imwrite(f"frames/frame{count}.jpg", resized_image)
        print(f"wrote image {count}")
        count += 1
        success, image = vidcap.read()









if __name__ == '__main__':
    in_filename = "/Users/orihab/Documents/interview projects/anyvision/src/momoVideo.mp4"
    export_video_frames(in_filename)


# in_filename = "/Users/orihab/Documents/interview projects/anyvision/src/momoVideo.mp4"
# vidcap = cv2.VideoCapture(in_filename)
# success, image = vidcap.read()
# binary_image = pickle.dumps(image)
# c = rpyc.connect("localhost", 18861)
# resized_image_binary = c.root.exposed_resize(binary_image)
# count = 1
# resized_image = pickle.loads(resized_image_binary)
# cv2.imwrite(f"frames/frame{count}.jpg", resized_image)

