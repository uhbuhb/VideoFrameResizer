import pickle
import os, time
import cv2, argparse
import rpyc
from threading import Thread


def export_resized_video_frames(filename, outfolder, thread_number):
    start = time.time()
    remote_connection = rpyc.connect("localhost", 8081)
    t = time.time()
    connection_time = t-start
    vidcap = cv2.VideoCapture(filename)
    vidcap_time = time.time() - t
    t = time.time()
    count = 0
    tot_resize_time = 0
    success, image = vidcap.read()
    try:
        os.mkdir(outfolder)
    except FileExistsError as e:
        pass
    print(f"{thread_number}: connection_time: {connection_time*1000}")
    while success:
        binary_image = pickle.dumps(image)
        resized_image_binary = remote_connection.root.exposed_resize(binary_image)
        resized_image = pickle.loads(resized_image_binary)
        cv2.imwrite(f"/tmp/{outfolder}/Frame{count}.jpg", resized_image)
        count += 1
        resize_time = time.time() - t
        t = time.time()
        tot_resize_time += resize_time
        avg_resize_time = tot_resize_time/count
        #print (f"{thread_number}: single frame resize_time: {resize_time*1000}, running_avg_frame_resize_time: {avg_resize_time*1000}")
        success, image = vidcap.read()
    print(
        f"{thread_number}: overall frame resize avg: {avg_resize_time*1000} fps")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("InVideoFullPath")
    parser.add_argument("NInstances")
    parser.add_argument("MDiffSeconds")
    args = parser.parse_args()
    in_filename = args.InVideoFullPath
    threads = []
    for i in range(int(args.NInstances)):
        thread = Thread(target=export_resized_video_frames, args=(in_filename, f"vid-instance{i}", i))
        print(f"starting thread{i}")
        thread.start()
        time.sleep(int(args.MDiffSeconds))
        threads.append(thread)

    for thread in threads:
        thread.join()

