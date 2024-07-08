import numpy as np
import cv2
import json
from PyQt5.QtCore import QSettings

# HeadModule function
def calculate_bounding_box(frame, landmarks):
    # initializarea variabilelor
    min_x, min_y, max_x, max_y = float('inf'), float('inf'), 0, 0
    for landmark in landmarks.landmark:
        # transformarea in coordonate pixeli
        x, y, _ = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0]), int(
            landmark.z * frame.shape[1])
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    # returneaza coltul stanga sus si dreapta jos


    return (min_x, min_y), (max_x, max_y)

#distanta Euclidiana
def calculate_distance(landmark1, landmark2):
    #calcule vectorizate
    x1 = landmark1.x
    y1 = landmark1.y

    x2 = landmark2.x
    y2 = landmark2.y

    v = np.array([x1, y1]) - \
        np.array([x2, y2])
    #norma euclidiana a unui vector ce da distanta dintre 2 puncte in plan 2D
    distance = np.linalg.norm(v)
    return distance

def head_tilt(face_landmarks, frame_markers, scroll: False):
    face_2d = []
    face_3d = []
    for idx, lm in enumerate(face_landmarks.landmark):
        if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
            x, y = int(lm.x * 1920), int(lm.y * 1080)

            # coordonate 2d
            face_2d.append([x, y])

            # coordonate 3d
            face_3d.append([x, y, lm.z])
    face_2d = np.array(face_2d, dtype=np.float64)
    face_3d = np.array(face_3d, dtype=np.float64)
    # matricea camerei
    focal_length = 1920

    cam_matrix = np.array([[focal_length, 0, 1080 / 2],
                           [0, focal_length, 1920 / 2],
                           [0, 0, 1]])

    # matricea de distorsiune
    dist_matrix = np.zeros((4, 1), dtype=np.float64)

    # permite transformarea punctelor 3d in proiectii 2d
    success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

    # obtine matricea de rotatie
    rmat, jac = cv2.Rodrigues(rot_vec)

    # se folloseste de aceasta pentru extragerea unghiurilor
    angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

    # unghiurile sunt convertite apoi din radiani in grade
    x = angles[0] * 360
    y = angles[1] * 360
    z = angles[2] * 360
    # Add the text on the image
    # cv2.putText(image, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
    cv2.putText(frame_markers, "x: " + str(np.round(x, 2)), (500, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame_markers, "y: " + str(np.round(y, 2)), (500, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame_markers, "z: " + str(np.round(z, 2)), (500, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    if scroll is True:

        if y < -2 or y > 2:
            return True
        return False
    if x < 4 and x > -2 and y > -2.5 and y < 2.5:
        return True
    return False

def hand_position(hand_landmarks, label):
    distance = hand_landmarks.landmark[17].x - hand_landmarks.landmark[4].x
    if label == 'Right' and distance > 0:
        return True
    elif label == 'Left' and distance < 0:
        return True
    return False

def save_calibration_to_settings(dictionary):
    settings = QSettings("Licenta", "CamControl")

    existing_dict = load_dictionary_from_settings()

    existing_dict.update(dictionary)

    json_data = json.dumps(existing_dict)

    settings.setValue("mean_calibrations", json_data)




def load_dictionary_from_settings():
    settings = QSettings("Licenta", "CamControl")
    json_data = settings.value("mean_calibrations")
    if json_data is not None:
        return json.loads(json_data)
    else:
        return {}