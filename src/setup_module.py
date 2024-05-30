from mediapipe.python.solutions import face_mesh
from mediapipe.python.solutions import hands as mp_hands
from mediapipe.python.solutions import drawing_utils as mpDraw
import numpy as np
import cv2
import time
import math
from .app_utils import *
from ui.ui_functions import UIFunctions

class SetupModule:
    def __init__(self, setup_window, list_calibration):
        self.face_mesh = face_mesh.FaceMesh(refine_landmarks=True)
        self.hands = mp_hands.Hands(min_detection_confidence=0.8,
                                    min_tracking_confidence=0.8,
                                    max_num_hands=1
                                    )
        self.setup_window = setup_window
        if list_calibration is None:
            self.list_calibration = ['face_click_left', 'face_click_right', 'face_smile',
                                'hand_click', 'hand_recenter', 'hand_volume']
        else:
            self.list_calibration = list_calibration

        self.label = ''
        self.calibration = np.zeros(151)
        self.calibration_timer = None
        self.index = None
        self.delay_calibration = None
        self.continue_calibration = True
        self.dictionary_calibrated = {}

    def detect(self, frame):
        # converteste imaginea din BGR in RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.frame_markers = frame
        self.frame_markers = cv2.rectangle(self.frame_markers, (660, 140), (1260, 980), (0, 255, 0), 3)
        self.height, self.width, _ = frame.shape
        # procesarea imaginii cu landmark urile fetei
        results_face = self.face_mesh.process(rgb_frame)
        results_hands = self.hands.process(rgb_frame)
        contains_face = any('face' in s for s in self.list_calibration)
        contains_hand = any('hand' in s for s in self.list_calibration)
        if contains_face:
            list_face = [s for s in self.list_calibration if 'face' in s]
            if results_face.multi_face_landmarks:
                for self.face_landmarks in results_face.multi_face_landmarks:
                    # mpDraw.draw_landmarks(self.frame_markers, self.face_landmarks, face_mesh.FACEMESH_TESSELATION)
                    self.bounding_box = calculate_bounding_box(rgb_frame, self.face_landmarks)
                    part = list_face[0]
                    self.draw_landmarks(part)
                    if self.continue_calibration is True:
                        if self.delay_calibration is None:
                            self.delay_calibration = time.time()
                        if time.time() - self.delay_calibration >= 3:
                            self.start_calibration(part)
                        else:
                            self.delay_gesture(part)
                    elif len(list_face) > 0 or contains_hand is True:
                        self.continue_calibration = True


            else:
                cv2.putText(self.frame_markers, "Camera nu recunoaste o fata in dreptul sau ",
                            (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif contains_hand:
            list_hand = [s for s in self.list_calibration if 'hand' in s]
            if results_hands.multi_hand_landmarks:
                for self.hand_landmarks in results_hands.multi_hand_landmarks:
                    # mpDraw.draw_landmarks(
                    #     frame, self.hand_landmarks, mp_hands.HAND_CONNECTIONS
                    # )

                    self.bounding_box = calculate_bounding_box(rgb_frame, self.hand_landmarks)
                    part = list_hand[0]
                    self.draw_landmarks(part)
                    self.label = results_hands.multi_handedness[0].classification[0].label
                    if self.continue_calibration is True:
                        if self.delay_calibration is None:
                            self.delay_calibration = time.time()
                        if time.time() - self.delay_calibration >= 3:
                            self.start_calibration(part)
                        else:
                            self.delay_gesture(part)
                    elif len(list_hand) > 0:
                        self.continue_calibration = True
            else:
                cv2.putText(self.frame_markers, "Afiseaza mana in fata camerei ",
                            (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        elif contains_face is False and contains_hand is False:
            save_calibration_to_settings(self.dictionary_calibrated)
            print(self.dictionary_calibrated)
            self.setup_window.parent.show()
            self.setup_window.camera.close()
            self.setup_window.destroy()
        return self.frame_markers

    def start_calibration(self, gesture):
        if self.index is None:
            self.index = 0
        if self.calibration_timer is None:
            self.calibration_timer = time.time()
        if self.check_part(gesture) and self.check_bounds(gesture):
            if self.index < 151:
                threshold = self.operations(gesture)
                print(threshold)
                self.calibration[self.index] = threshold
                self.index = self.index + 1
            if (time.time() - self.calibration_timer) > 10:
                self.dictionary_calibrated[gesture] = np.mean(self.calibration)
                self.continue_calibration = False
                self.delay_calibration = None
                self.calibration_timer = None
                self.index = None
                self.list_calibration.pop(0)
        else:
            self.frame_markers = cv2.putText(self.frame_markers, 'Frame the face inside the rectangle',
                                             (660, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
            self.calibration_timer = None
            self.index = None
            self.calibration = np.zeros(151)

    def check_part(self, gesture):
        if 'face' in gesture:
            return (self.bounding_box[0][0] > 660 and self.bounding_box[0][1] > 140 and self.bounding_box[1][0] < 1260 and
                    self.bounding_box[1][1] < 980 and head_tilt(self.face_landmarks, self.frame_markers, False))
        else:
            return (self.bounding_box[0][0] > 660 and self.bounding_box[0][1] > 140 and self.bounding_box[1][
                0] < 1260 and
                    self.bounding_box[1][1] < 980 and hand_position(self.hand_landmarks, self.label))

    def check_bounds(self, gesture):
        if gesture == 'face_click_left':
            if self.operations(gesture) > 1.25:
                cv2.putText(self.frame_markers, "Nu deschide ochiul stang  " + str(
                    np.round(3.00 - (time.time() - self.delay_calibration), 2)),
                            (700, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                return False

        elif gesture == 'face_click_right':
            if self.operations(gesture) > 1.25:
                cv2.putText(self.frame_markers, "Nu deschide ochiul drept " + str(
                    np.round(3.00 - (time.time() - self.delay_calibration), 2)),
                            (700, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                return False
        elif gesture == 'face_smile':
            if self.operations(gesture) < 0.35:
                cv2.putText(self.frame_markers, "Incepe sa zambesti " + str(
                    np.round(3.00 - (time.time() - self.delay_calibration), 2)),
                            (700, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                return False
        elif gesture == 'hand_click':
            if self.operations(gesture) > 1.5:
                cv2.putText(self.frame_markers, "Apropie punctele mai mult " + str(
                    np.round(3.00 - (time.time() - self.delay_calibration), 2)),
                            (700, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                return False
        elif gesture == 'hand_recenter':
            if self.operations(gesture) > 0.15:
                cv2.putText(self.frame_markers, "Apropiete mana mai mult de gest " + str(
                    np.round(3.00 - (time.time() - self.delay_calibration), 2)),
                            (700, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                return False
        else: # < 5
            if self.operations(gesture) < 5:
                cv2.putText(self.frame_markers, "Mareste distanta dintre degete" + str(
                    np.round(3.00 - (time.time() - self.delay_calibration), 2)),
                            (700, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                return False
        return True

    def operations(self, gesture):
        if gesture == 'face_click_left':
                return  ((calculate_distance(self.face_landmarks.landmark[160], self.face_landmarks.landmark[144])
                        + calculate_distance(self.face_landmarks.landmark[158], self.face_landmarks.landmark[153])
                        + calculate_distance(self.face_landmarks.landmark[159], self.face_landmarks.landmark[145]))
                       / (calculate_distance(self.face_landmarks.landmark[33], self.face_landmarks.landmark[133])))

        elif gesture == 'face_click_right':
                return ((calculate_distance(self.face_landmarks.landmark[386], self.face_landmarks.landmark[374])
                        + calculate_distance(self.face_landmarks.landmark[385], self.face_landmarks.landmark[380])
                        + calculate_distance(self.face_landmarks.landmark[387], self.face_landmarks.landmark[373]))
                       / calculate_distance(self.face_landmarks.landmark[362], self.face_landmarks.landmark[263]))

        elif gesture == 'face_smile':
                face_width = abs(self.face_landmarks.landmark[33].x - self.face_landmarks.landmark[263].x)
                lips_width =abs(self.face_landmarks.landmark[61].x - self.face_landmarks.landmark[291].x)
                jaw_width = abs(self.face_landmarks.landmark[132].x - self.face_landmarks.landmark[361].x)
                lips_width_normalized = lips_width / face_width
                jaw_width_normalized = jaw_width / face_width
                return lips_width_normalized / jaw_width_normalized

        elif gesture == 'hand_click':
            absStandard = calculate_distance(self.hand_landmarks.landmark[0], self.hand_landmarks.landmark[
                1])  # distanta dintre baza mainii si inceputul degetului mare
            return calculate_distance(self.hand_landmarks.landmark[4], self.hand_landmarks.landmark[
                6]) / absStandard  # distanta dintre varful degetului mare si mijlocul degetului aratator

        elif gesture == 'hand_recenter':
            distance_index_finger = calculate_distance(self.hand_landmarks.landmark[8], self.hand_landmarks.landmark[5])
            distance_average = np.average([calculate_distance(self.hand_landmarks.landmark[11], self.hand_landmarks.landmark[10]),
                                           calculate_distance(self.hand_landmarks.landmark[15], self.hand_landmarks.landmark[14]),
                                           calculate_distance(self.hand_landmarks.landmark[19],
                                                              self.hand_landmarks.landmark[18])])
            return distance_average / distance_index_finger

        else:
            absStandard = calculate_distance(self.hand_landmarks.landmark[0], self.hand_landmarks.landmark[1])
            return  calculate_distance(self.hand_landmarks.landmark[8], self.hand_landmarks.landmark[4]) / absStandard

    def delay_gesture(self, gesture):
        if gesture == 'face_click_left':
            cv2.putText(self.frame_markers, "Inchide ochiul stang, calibrarea v-a incepe in  " + str(
                np.round(3.00 - (time.time() - self.delay_calibration), 2)),
                        (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        elif gesture == 'face_click_right':
            cv2.putText(self.frame_markers, "Inchide ochiul drept, calibrarea v-a incepe in  " + str(
                            np.round(3.00 - (time.time() - self.delay_calibration), 2)),
                        (500, 50),  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        elif gesture == 'face_smile':
            cv2.putText(self.frame_markers, "Incepe sa zambesti, calibrarea v-a incepe in  " + str(
                np.round(3.00 - (time.time() - self.delay_calibration), 2)),
                        (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255), 2)

        elif gesture == 'hand_click':
            cv2.putText(self.frame_markers, "Afiseaza mana spre camera, si lipeste degetul mare de cel aratator"
                                                  ", calibrarea v-a incepe in  " +
                              str(np.round(3.00-(time.time() - self.delay_calibration), 2)),
                      (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        else :
            cv2.putText(self.frame_markers,"Afiseaza mana spre camera, in pozitia urmatoare"
                              ", calibrarea v-a incepe in  " +
                              str(np.round(3.00 - (time.time() - self.delay_calibration), 2)),
                              (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(0, 0, 255), 2)

    def draw_landmarks(self, gesture):
        if gesture == 'face_click_left':

            for idx, landmark in enumerate(self.face_landmarks.landmark):
                if idx in [159, 145, 33, 133]:  # alege indicii pe care vrei sa ii desenezi

                    cx, cy = int(landmark.x * self.width), int(landmark.y * self.height)
                    cv2.circle(self.frame_markers, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        elif gesture == 'face_click_right':
            for idx, landmark in enumerate(self.face_landmarks.landmark):
                if idx in [386, 374, 362, 263]:  # alege indicii pe care vrei sa ii desenezi
                    cx, cy = int(landmark.x * self.width), int(landmark.y * self.height)
                    cv2.circle(self.frame_markers, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        elif gesture == 'face_smile':
            for idx, landmark in enumerate(self.face_landmarks.landmark):
                if idx in [61, 291]:  # alege indicii pe care vrei sa ii desenezi

                    cx, cy = int(landmark.x * self.width), int(landmark.y * self.height)
                    cv2.circle(self.frame_markers, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        elif gesture == 'hand_click':
            for idx, landmark in enumerate(self.hand_landmarks.landmark):
                if idx in [4, 6]:  # alege indicii pe care vrei sa ii desenezi

                    cx, cy = int(landmark.x * self.width), int(landmark.y * self.height)
                    cv2.circle(self.frame_markers, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        elif gesture == 'hand_recenter':
            for idx, landmark in enumerate(self.hand_landmarks.landmark):
                if idx in [11, 15, 19, 18, 10, 14]:  # alege indicii pe care vrei sa ii desenezi
                    cx, cy = int(landmark.x * self.width), int(landmark.y * self.height)
                    cv2.circle(self.frame_markers, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        else :
            for idx, landmark in enumerate(self.hand_landmarks.landmark):
                if idx in [4, 8]:  # alege indicii pe care vrei sa ii desenezi
                    cx, cy = int(landmark.x * self.width), int(landmark.y * self.height)
                    cv2.circle(self.frame_markers, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
