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
    return (min_x, min_y), (max_x, max_y)

#calculeaza miscarea medie a unui reper intr un anumit timp
def calculate_moving_average(landmark, ran, LiT):
    #LiT este lista ce stocheaza datele din timp pentru a calcula media
    #daca lista nu contine un numar de elemente, atunci acesteia continua sa i se atribuie
    while len(LiT) < ran:
        LiT.append(landmark)
    LiT.append(landmark)
    #daca contine mai multe atunci cel mai vechi este scos din lista
    if len(LiT) > ran:
        LiT.pop(0)
    #returneaza media listei intr un interval de timp
    return sum(LiT)/ran

#distanta Euclidiana
def calculate_distance(lankdmark1, landmark2):
    #calcule vectorizate
    v = np.array([lankdmark1[0], lankdmark1[1]]) - \
        np.array([landmark2[0], landmark2[1]])
    #norma euclidiana a unui vector ce da distanta dintre 2 puncte in plan 2D
    distance = np.linalg.norm(v)
    return distance