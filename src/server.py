import pickle
import rpyc
import cv2
import time


RESIZE_FACTOR = .5

class MyService(rpyc.Service):
    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        pass

    def exposed_resize(self, received_image_binary):
        start = time.time()
        received_image = pickle.loads(received_image_binary)
        load_time = time.time()-start
        x,y,z = received_image.shape
        resized_image = cv2.resize(received_image, dsize=(int(y*RESIZE_FACTOR),int(x*RESIZE_FACTOR)), interpolation=cv2.INTER_AREA)
        resize_time = time.time()-load_time-start
        resized_binary = pickle.dumps(resized_image)
        dump_time = time.time()-resize_time-load_time-start
        print (f"load: {load_time*1000}, resize: {resize_time*1000}, dump: {dump_time*1000}")
        return resized_binary


if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    print("starting server")
    t = ThreadedServer(MyService, port=18861)
    t.start()


