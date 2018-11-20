import pickle
import os, time
import cv2, argparse
import rpyc
from threading import Thread

from src.image_resizer import resize



def export_resized_video_frames(filename, outfolder):
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
        cv2.imwrite(f"{outfolder}/frame{count}.jpg", resized_image)
        count += 1
        success, image = vidcap.read()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("inVideoFullPath")
    parser.add_argument("NInstances")
    parser.add_argument("MElapsedSeconds")
    args = parser.parse_args()
    in_filename = args.inVideoFullPath
    threads = []
    for i in range(int(args.NInstances)):
        thread = Thread(target=export_resized_video_frames, args=(in_filename, f"instance{i}"))
        print(f"starting thread{i}")
        thread.start()
        time.sleep(int(args.MElapsedSeconds))
        threads.append(thread)

    for thread in threads:
        thread.join()



