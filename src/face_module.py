from mediapipe.python.solutions import face_mesh
from mediapipe.python.solutions import drawing_utils
import numpy as np
import cv2
import pyautogui
from .app_utils import *
from scipy import signal
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QTimer
import time
mpDraw = drawing_utils

NK_DWELL_MOVE_THRESH = 10
# anuleaza inchiderea aplicatiei cand coltul din stanga sus este atins
pyautogui.FAILSAFE = False
# mareste viteza
pyautogui.PAUSE = 0

class FaceModule:
    def __init__(self):
        self.face_mesh = face_mesh.FaceMesh(refine_landmarks=True)

        self.settings = QSettings("Licenta", "CamControl")
        self.move = self.settings.value("moveFaceCursorCheckBox", type=bool)

        self.dwellClick = self.settings.value("dwellClickRadioBox", type=bool)
        self.dwellScroll = self.settings.value("dwellScrollRadioBox", type=bool)
        self.smileCenter = self.settings.value("smileCenterCheckBox", type=bool)

        slider_values = self.settings.value("slider_values_face", type=list)
        self.speedX = slider_values[0]/20
        self.speedY = slider_values[1]/20
        self.filter = slider_values[4]
        self.filterX = slider_values[2]
        self.filterY = slider_values[3]

        # initializare variabile

        # miscare cursor
        self.cX_prev = 0
        self.cY_prev = 0
        self.move_detected = 0
        self.x, self.y = 0, 0
        # variabila pentru prima miscare a cursorului
        self.first_data = 0

        # variabile click
        self.nowRightClick, self.nowLeftClick = 0, 0
        self.previousRightClick, self.previousLeftClick = 0, 0
        self.nowScroll = 0
        self.doubleClick = 0
        self.c_start_left, self.c_start_right = None, None
        self.click_count_left, self.click_count_right = 0, 0
        self.mouse_down = False
        self.double_click_timer = 0

        # filtrarea datelor privind miscarea cursorului
        self.filter_cursor_X = np.zeros(100)
        self.filter_cursor_Y = np.zeros(100)

        # reducerea miscarii cursorului pentru miscari mici
        self.fine_control_X = np.zeros(2)
        self.fine_control_Y = np.zeros(2)
        #  self.fine_control_X = np.zeros(4)
        #  self.fine_control_Y = np.zeros(4)

        if self.dwellClick or self.dwellScroll:
            # conectare Dwell click checkbox si timer
            self.dwell_timer()

        # instantiere constanta zambet si variabila de timp
        self.smile_duration_threshold = 5
        self.smile_start_time = None

        self.initial_distance = None
        self.head_returned_time = None

        thresholds = load_dictionary_from_settings()
        self.threshold_left_eye = thresholds.get('face_click_left') + 0.1
        self.threshold_right_eye = thresholds.get('face_click_right') + 0.1
        self.threshold_smile = thresholds.get('face_smile')


    def detect(self, frame):
        # converteste imaginea din BGR in RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # procesarea imaginii cu landmark urile fetei
        results = self.face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # desenarea unui dreptunghi in jurul fetei
                bounding_box = calculate_bounding_box(rgb_frame, face_landmarks)
                self.frame_markers = cv2.rectangle(frame, bounding_box[0], bounding_box[1], (0, 255, 0), 3)
                for idx, landmark in enumerate(face_landmarks.landmark):
                    if idx in [33, 263, 1 , 61 , 291 , 199]:  # alege indicii pe care vrei sa ii desenezi
                        height, width, _ = frame.shape
                        cx, cy = int(landmark.x * width), int(landmark.y * height)
                        cv2.circle(self.frame_markers, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

                self.x = (bounding_box[0][0] + bounding_box[1][0]) / 2
                self.y = (bounding_box[0][1] + bounding_box[1][1]) / 2
                self.move_cursor(self.x, self.y)
                if self.smileCenter:
                    self.detect_smile(face_landmarks)

                if head_tilt(face_landmarks, self.frame_markers, False):
                    self.click_functionality(face_landmarks)
                if self.dwellScroll:
                    self.initiate_Scroll(face_landmarks)

        else:
            self.frame_markers = frame
        return self.frame_markers

    # timer dwell
    def dwell_timer(self):
        self.timer_dwell = QTimer()
        self.timer_dwell.timeout.connect(self.check_move)
        self.timer_dwell.start(5000)

    def check_move(self):
        checkbox_check = (self.move and self.dwellClick) or (self.move and self.dwellScroll)
        if checkbox_check and (self.move_detected == 0):

            if self.dwellClick:

                pyautogui.click()  # click
            elif self.dwellScroll:

                self.nowScroll = 1
                self.timer_dwell.stop()
        else:
            self.nowScroll = 0
            self.move_detected = 0

    def detect_smile(self, landmarks):

        # Extrage landmark-uri relevante ale fetei
        smile_landmarks = [
            landmarks.landmark[361],  # jaw
            landmarks.landmark[132],
            landmarks.landmark[61],  # lips
            landmarks.landmark[291]
        ]
        outer_eye_corners = [
            landmarks.landmark[33],
            landmarks.landmark[263],
        ]

        face_width = abs(outer_eye_corners[0].x - outer_eye_corners[1].x)

        # Calculeaza lungimea buzelor si a maxilarului
        lips_width = abs(smile_landmarks[2].x - smile_landmarks[3].x)
        jaw_width = abs(smile_landmarks[1].x - smile_landmarks[0].x)

        # normalizeaza acestei valori pentru o valoare mai generala
        lips_width_normalized = lips_width / face_width
        jaw_width_normalized = jaw_width / face_width

        ratio = lips_width_normalized / jaw_width_normalized
        ratioBar = ratio
        ratioBar = np.interp(ratioBar, [0.41, 0.52], [400, 150])
        cv2.rectangle(self.frame_markers, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(self.frame_markers, (50, int(ratioBar)), (85, 400), (0, 255, 0), cv2.FILLED)

        if ratio > self.threshold_smile:
            # Incepe timerul daca zembetul este detectat
            if self.smile_start_time is None:
                self.smile_start_time = time.time()
            else:
                cv2.putText(self.frame_markers, "Zambet in detectare!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                # Daca zambetul continua mai mult de 5 secunda muta cursorul in centru
                if time.time() - self.smile_start_time >= self.smile_duration_threshold:
                    # Lungimea si latimea ecranului
                    screen_width, screen_height = pyautogui.size()
                    # Coordonatele centrale
                    center_x = screen_width // 2
                    center_y = screen_height // 2
                    # Misca cursorul in centru
                    pyautogui.moveTo(center_x, center_y)
                    pyautogui.sleep(1)
                    self.smile_start_time = None
        else:
            # Daca zambetul scade sub rata, reseteaza inceputul acestuia
            self.smile_start_time = None

        # misca cursor
    def move_cursor(self, cX, cY):
        # variabile pentru reducerea miscarilor mici
        noise_X = self.filter
        noise_Y = self.filter

        # calculeaza delta x si y(diferenta dintre coordonatele actualore si cele anterioare)
        delta_X = cX - self.cX_prev
        delta_Y = cY - self.cY_prev

        # salvarea coordonatelor pentru urmatoarea iteratie
        self.cX_prev = cX
        self.cY_prev = cY

        move_X = 0
        move_Y = 0

        # pentru primul set de date se returneaza 0(nu exista date anterioare)
        if (self.first_data == 0):
            self.first_data = 1
            # preluare marime ecran
            screen_width, screen_height = pyautogui.size()
            # coordonate centrale
            center_x = screen_width // 2
            center_y = screen_height // 2

            pyautogui.moveTo(center_x, center_y)

            # pauza o secunda
            time.sleep(1)
            return move_X, move_Y

        # la miscare mai semnficiativa se face diferenta pentru filtru folosit
        if (abs(delta_X) > abs(noise_X)):
            move_X = delta_X - noise_X

        if (abs(delta_Y) > abs(noise_Y)):
            move_Y = delta_Y - noise_Y

        # daca este bifata realizarea miscarii
        if self.move is True:
            # misca cursorul pe axa x
            move_X_final, move_x = self.digital_filter_cursor_X(move_X, self.speedX)
            # misca cursorul pe axa y
            move_Y_final, move_y = self.digital_filter_cursor_Y(move_Y, self.speedY)
            pyautogui.moveRel(int(round(move_X_final)), int(round(move_Y_final)))
            print(move_X_final, move_Y_final)
            # detectare miscare pentru dwell click
            if move_x or move_y:
                self.move_detected = 1

        # returneaza miscarea pe x si y
        return move_X, move_Y

    # filtru pentru miscarea cursorului pe x
    def digital_filter_cursor_X(self, dx, speed):
        numtaps = self.filterX
        # fara filtru
        if (numtaps == 0):
            x_out = dx
        # filtru Finite Impulse Response pentru a reduce din zgomot
        else:
            # frecventa de taiere, atenueaza semnalul
            f = 0.1
            # coeficientii filtrului
            c = signal.firwin(numtaps, f)
            # numarul de coeficienti
            filter_size = len(c)
            # se adauga valoarea curenta dx
            self.filter_cursor_X = np.append([dx], self.filter_cursor_X)
            # se sterge ultimul element
            self.filter_cursor_X = self.filter_cursor_X[:-1]

            # calcularea valorii de iesire prin multiplicare acumulata(inmulturea coeficientilor si adunarea lor)
            x_out = 0
            for i in range(0, filter_size):
                x_out = x_out + self.filter_cursor_X[i] * c[i]

        # scalarea pentru calcularea vitezei finale

        x_out = x_out * 1000

        # adaugarea valorii absolute ale lui x curent
        self.fine_control_X = np.append([abs(x_out)], self.fine_control_X)
        # stergerea ultimului element
        self.fine_control_X = self.fine_control_X[:-1]
        # suma valorilor pentru control
        sum_X = sum(self.fine_control_X)

        # viteza finala bazata pe viteza curenta si suma in urma filtrarii impartita la un factor constant
        speed_final = speed * abs(sum_X) / 400
        # valoarea de iesire filtrata
        x_out = speed_final * x_out / 1000

        # verifica daca miscarea calculata trece de pragul de stationare
        move = 0
        if (abs(x_out) > NK_DWELL_MOVE_THRESH):
            move = 1

        return x_out, move

    # filtru pentru miscarea cursorului pe y
    def digital_filter_cursor_Y(self, dy, speed):

        numtaps = self.filterY
        # fara filtru
        if numtaps == 0:
            y_out = dy
        # filtru Finite Impulse Response pentru a reduce din zgomot
        else:
            # frecventa de taiere, atenueaza semnalul
            f = 0.1
            # coeficientii filtrului
            c = signal.firwin(numtaps, f)
            # numarul de coeficienti
            filter_size = len(c)

            # se adauga valoarea curenta dy
            self.filter_cursor_Y = np.append([dy], self.filter_cursor_Y)
            # sterge ultimul element
            self.filter_cursor_Y = self.filter_cursor_Y[:-1]

            # calcularea valorii de iesire prin multiplicare acumulata(inmulturea coeficientilor si adunarea lor)
            y_out = 0
            for i in range(0, filter_size):
                y_out = y_out + self.filter_cursor_Y[i] * c[i]

        # scalarea pentru calcularea vitezei finale
        y_out = y_out * 1000

        # adaugarea valorii absolute ale lui y curent
        self.fine_control_Y = np.append([abs(y_out)], self.fine_control_Y)
        # sterge ultimul element
        self.fine_control_Y = self.fine_control_Y[:-1]
        # suma valorilor pentru control
        sum_Y = sum(self.fine_control_Y)

        # viteza finala bazata pe viteza curenta si suma in urma filtrarii impartita la un factor constant
        speed_final = speed * abs(sum_Y) / (2 * 200)
        # valoarea de iesire filtrata
        y_out = speed_final * y_out / 1000

        # verifica daca miscarea calculata trece de pragul de stationare
        move = 0
        if abs(y_out) > NK_DWELL_MOVE_THRESH:
            move = 1

        return y_out, move

    def click_functionality(self, face_landmarks):
        self.click(face_landmarks)
        #functionalitate dublu click
        if self.nowLeftClick == 1 and self.nowLeftClick != self.previousLeftClick:
            if time.time() - self.double_click_timer < 3:
                self.double_click()

        #functionalitate left click
        if self.nowLeftClick == 1:
            if self.c_start_left is None:
                self.c_start_left = time.time()
            elif time.time() - self.c_start_left >= 2 and self.mouse_down is False:
                self.leftClick()
                self.double_click_timer = time.time()

        # functionalitate mouse up
        if self.nowLeftClick == 0 and self.nowLeftClick != self.previousLeftClick:
            self.c_start_left = None
            self.leftClickRelease()

        if self.nowRightClick == 0:
            self.c_start_right = None

        # functionalitate right click
        if self.nowRightClick == 1:
            if self.c_start_right is None:
                self.c_start_right = time.time()
            elif time.time() - self.c_start_right >= 2:
                self.rightClick()
                self.c_start_right = None

        # actualizare click flag
        self.previousLeftClick = self.nowLeftClick
        self.previousRightClick = self.nowRightClick

    def click(self, face_landmarks):

        ear_opt_left_eye = ((calculate_distance(face_landmarks.landmark[160], face_landmarks.landmark[144])
                    + calculate_distance(face_landmarks.landmark[158], face_landmarks.landmark[153])
                    + calculate_distance(face_landmarks.landmark[159], face_landmarks.landmark[145]))
                    /  calculate_distance(face_landmarks.landmark[33], face_landmarks.landmark[133]))

        ear_opt_right_eye = ((calculate_distance(face_landmarks.landmark[386], face_landmarks.landmark[374])
                    + calculate_distance(face_landmarks.landmark[385], face_landmarks.landmark[380])
                    + calculate_distance(face_landmarks.landmark[387], face_landmarks.landmark[373]))
                    /  calculate_distance(face_landmarks.landmark[362], face_landmarks.landmark[263]))

        if ear_opt_left_eye < self.threshold_left_eye:
            self.nowLeftClick = 1
        else:
            self.nowLeftClick = 0

        if ear_opt_right_eye < self.threshold_right_eye:
            self.nowRightClick = 1
        else:
            self.nowRightClick = 0

    def leftClick(self):
        pyautogui.mouseDown()
        self.mouse_down = True

    # eliberare click stanga
    def leftClickRelease(self):
        self.mouse_down = False
        pyautogui.mouseUp()
    def double_click(self):
        # print('double click')
        pyautogui.doubleClick()
        self.double_click_timer = 0

    # click dreapta
    def rightClick(self):
        pyautogui.rightClick()

    def initiate_Scroll(self, face_landmarks):
        # functionalitate scroll
        if self.nowScroll == 1:
            if self.initial_distance is None:
                self.initial_distance = calculate_distance(face_landmarks.landmark[152], face_landmarks.landmark[1])
            self.move = False
            self.Scroll(face_landmarks)
        else:
            self.move = self.settings.value("moveFaceCursorCheckBox", type=bool)
            self.initial_distance = None

    def Scroll(self, face_landmarks):
        current_distance = calculate_distance(face_landmarks.landmark[152], face_landmarks.landmark[1])
        dy = face_landmarks.landmark[195].y - self.y/1080
        dy = dy * 1080
        pyautogui.scroll(-dy/50)
        if self.head_returned(current_distance) or head_tilt(face_landmarks, self.frame_markers, True):
            self.timer_dwell.start()
            self.nowScroll = 0

    def head_returned(self, current_distance, tolerance=0.02, return_duration=5):
        # Define the lower and upper bounds of the interval
        lower_bound = self.initial_distance - tolerance
        upper_bound = self.initial_distance + tolerance
        # Check if the current distance is within the interval
        if lower_bound <= current_distance <= upper_bound:
            if self.head_returned_time is None:
                # Start counting the time when head returns to initial position
                self.head_returned_time = time.time()
            elif time.time() - self.head_returned_time >= return_duration:
                # Head has remained in initial position for return_duration seconds
                self.head_returned_time = None
                return True
        else:
            # Reset head returned time if head is not in initial position
            self.head_returned_time = None
        return False



