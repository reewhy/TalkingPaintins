import math
import time
import cv2
import mediapipe as mp

class face_detector():
    def __init__(self,
                 mode = False,
                 max_faces = 2,
                 model_complexity = 1,
                 detection_con = 0.5,
                 tracking_con = 0.5):
        self.mode = mode
        self.max_faces = max_faces
        self.model_complexity = model_complexity
        self.detection_con = detection_con
        self.tracking_con = tracking_con

        self.facedt = mp.solutions.face_detection
        self.mpdraw = mp.solutions.drawing_utils

    def find_faces(self, img, draw=True):
        with self.facedt.FaceDetection(self.detection_con):
            results = face_detection.process