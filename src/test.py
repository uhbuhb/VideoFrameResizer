import cv2
from src.image_resizer import resize



def export_video_frames(filename):
    vidcap = cv2.VideoCapture(filename)
    count = 0
    success, image = vidcap.read()
    while success:
        resized_image = resize(image)
        cv2.imwrite(f"frames/frame{count}.jpg", resized_image)
        count+=1
        success, image = vidcap.read()








if __name__ == '__main__':
    #args = parser.parse_args()
    #out = read_frame_as_jpeg(args.in_filename, args.frame_num)
    #sys.stdout.buffer.write(out)

    #resize("1.jpg")

    in_filename = "/Users/orihab/Documents/interview projects/anyvision/src/momoVideo.mp4"
    export_video_frames(in_filename)
