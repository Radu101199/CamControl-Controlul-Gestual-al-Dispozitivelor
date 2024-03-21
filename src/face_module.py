from mediapipe.python.solutions import face_mesh
import numpy as np
import cv2
from .app_utils import *


class FaceModule:
    def __init__(self):
        self.face_mesh = face_mesh.FaceMesh(refine_landmarks=True)

        # initializare variabile
        # miscare cursor
        self.cX_prev = 0
        self.cY_prev = 0
        self.move_detected = 0
        # variabila pentru prima miscare a cursorului
        self.first_data = 0
        # filtrarea datelor privind miscarea cursorului
        self.filter_cursor_X = np.zeros(100)
        self.filter_cursor_Y = np.zeros(100)

        # reducerea miscarii cursorului pentru miscari mici
        self.fine_control_X = np.zeros(2)
        self.fine_control_Y = np.zeros(2)

    def detect(self, frame):
        # converteste imaginea din BGR in RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # procesarea imaginii cu landmark urile fetei
        results = self.face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # desenarea unui dreptunghi in jurul fetei
                bounding_box = calculate_bounding_box(rgb_frame, face_landmarks)
                frame_markers = cv2.rectangle(frame, bounding_box[0], bounding_box[1], (0, 255, 0), 3)
                print(frame_markers)
        else:
            frame_markers = frame
        return frame_markers
