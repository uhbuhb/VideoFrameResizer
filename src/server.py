import pickle
import numpy
import PIL
import rpyc
import cv2


OUTPUT_SIZE = 128,128


class MyService(rpyc.Service):
    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        pass

    def exposed_get_answer(self): # this is an exposed method
        return 42

    exposed_the_real_answer_though = 43     # an exposed attribute

    def get_question(self):  # while this method is not exposed
        return "what is the airspeed velocity of an unladen swallow?"

    def exposed_resize(self, received_image_binary):
        received_image = pickle.loads(received_image_binary)
        size = tuple([l/2 for l in received_image.shape])
        resized_image = cv2.resize(received_image, dsize=size, interpolation=cv2.INTER_AREA)
        print(f"received image")
        resized_binary = pickle.dumps(resized_image)
        return resized_binary

    def resize(im):
        image = PIL.Image.fromarray(im)
        image.thumbnail(OUTPUT_SIZE)
        return numpy.asarray(image)

if __name__ == "__main__":
    from rpyc.utils.server import ThreadedServer
    print("starting server")
    t = ThreadedServer(MyService, port=18861)
    t.start()
    print("running...")


