import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core import base_options

class HandTracker:
    def __init__(self):
        options = vision.HandLandmarkerOptions(
            base_options=base_options.BaseOptions(
                model_asset_path="assets/models/hand_landmarker.task"
            ),
            num_hands=1
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        return self.detector.detect(mp_image)
