import cv2

class VideoPlayer():
    def __init__(self, path):
        self.path = path
        self.playing = False

    def show(self):
        video = cv2.VideoCapture(self.path)

        if video.isOpened():
            print('video opened')
        else:
            print('error')

        scale = 0

        window = 'Video'
        cv2.namedWindow(window)

        while True:
            ret, frame = video.read()

            if not ret:
                print('error in frame')
                cv2.destroyWindow(window)
                break

            rescaled_frame = frame

            for i in range(scale - 1):
                rescaled_frame = cv2.pyrDown(rescaled_frame)

            cv2.imshow(window, rescaled_frame)

            waitkey = (cv2.waitKey(1) and 0xFF)
            if waitkey == ord("q"):
                cv2.destroyWindow(window)
                video.release()
                break