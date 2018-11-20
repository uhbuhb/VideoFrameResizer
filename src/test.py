import pickle
import os, time
import cv2, argparse
import rpyc
from threading import Thread

from src.image_resizer import resize



def export_video_frames(filename, outfolder):
    remote_connection = rpyc.connect("localhost", 18861)
    vidcap = cv2.VideoCapture(in_filename)
    count = 0
    success, image = vidcap.read()
    try:
        os.mkdir(outfolder)
    except FileExistsError as e:
        pass

    while success:
        binary_image = pickle.dumps(image)
        resized_image_binary = remote_connection.root.exposed_resize(binary_image)
        resized_image = pickle.loads(resized_image_binary)
        cv2.imwrite(f"{outfolder}/frame{count}original.jpg", image)
        cv2.imwrite(f"{outfolder}/frame{count}.jpg", resized_image)
        #print(f"wrote image {count}")
        count += 1
        success, image = vidcap.read()









if __name__ == '__main__':
    in_filename = "/Users/orihab/Documents/interview projects/anyvision/src/momoVideo.mp4"
    thread = Thread(target=export_video_frames, args=(in_filename, "instance1"))
    print("starting thread1")
    thread.start()
    print("started thread1")
    time.sleep(3)
    thread2 = Thread(target=export_video_frames, args=(in_filename, "instance2"))
    print("starting thread2")
    thread2.start()
    print("started thread2")
    print("waiting for threads to finish")
    thread.join()
    print("thread1 finished!")
    thread2.join()
    print("thread2 finished!")




# in_filename = "/Users/orihab/Documents/interview projects/anyvision/src/momoVideo.mp4"
# vidcap = cv2.VideoCapture(in_filename)
# success, image = vidcap.read()
# binary_image = pickle.dumps(image)
# c = rpyc.connect("localhost", 18861)
# resized_image_binary = c.root.exposed_resize(binary_image)
# count = 1
# resized_image = pickle.loads(resized_image_binary)
# cv2.imwrite(f"frames/frame{count}.jpg", resized_image)

