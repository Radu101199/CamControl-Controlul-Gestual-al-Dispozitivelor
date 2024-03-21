
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