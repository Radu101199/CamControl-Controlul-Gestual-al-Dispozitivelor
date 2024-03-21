import cv2
from .app_utils import *
from mediapipe.python.solutions import hands as mp_hands
from mediapipe.python.solutions import drawing_utils as mp_drawing
class HandModule:
    def __init__(self):
        self.hands = mp_hands.Hands(min_detection_confidence=0.8,
        min_tracking_confidence=0.8,
        max_num_hands=1
    )

    def detect(self, frame):
        # converteste imaginea din BGR in RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # procesarea imaginii cu landmark urile mainii
        results = self.hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # desenare landmark mana 
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )
                frame_markers = frame
        else:
            frame_markers = frame
        return frame_markers
