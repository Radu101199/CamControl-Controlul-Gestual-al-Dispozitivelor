import numpy as np

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
    # print(frame.shape)
    # print((min_x, min_y),(max_x, max_y))
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

def calculate_distance_z(landmark1, landmark2):
    #calcule vectorizate
    x1 = landmark1.x
    y1 = landmark1.y
    z1 = landmark1.z

    x2 = landmark2.x
    y2 = landmark2.y
    z2 = landmark2.z


    v = np.array([x1, y1, z1]) - \
        np.array([x2, y2, z2])
    #norma euclidiana a unui vector ce da distanta dintre 2 puncte in plan 2D
    distance = np.linalg.norm(v)
    return distance