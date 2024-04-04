import cv2
import numpy as np

from .app_utils import *
from mediapipe.python.solutions import hands as mp_hands
from mediapipe.python.solutions import drawing_utils as mp_drawing
import pyautogui
from PyQt5.QtCore import QSettings, QTimer
import time
from scipy import signal

# anuleaza inchiderea aplicatiei cand coltul din stanga sus este atins
pyautogui.FAILSAFE = False
# mareste viteza
pyautogui.PAUSE = 0

NK_DWELL_MOVE_THRESH = 10
class HandModule:
    def __init__(self):

        self.hands = mp_hands.Hands(min_detection_confidence=0.8,
        min_tracking_confidence=0.8,
        max_num_hands=1
    )

        settings = QSettings("Licenta", "CamControl")
        self.move = settings.value("moveHandsCursorCheckBox", type=bool)
        self.speedCursor = settings.value("speedHandsCursor", type=float)

        slider_values = settings.value("slider_values_hands", type=list)
        self.speed = slider_values[0]
        self.filter = slider_values[3]
        self.filterX = slider_values[1]
        self.filterY = slider_values[2]

        # Initializare variabile
        self.distance_click = 0.7
        self.cX_prev, self.cY_prev = 0, 0
        self.move_detected = 0
        self.first_data = 0

        self.before_right_click, self.after_right_click = 0, 0  # de schimbat denumire
        self.start, self.c_start = float('inf'), float('inf')

        # variabile click
        self.nowRightClick, self.nowLeftClick = 0, 0
        self.previousRightClick, self.previousLeftClick = 0, 0
        self.doubleClick = 0

        # variabile pentru viitoare desenare
        self.x = 0
        self.y = 0

        # filtrarea datelor privind miscarea cursorului
        self.filter_cursor_X = np.zeros(100)
        self.filter_cursor_Y = np.zeros(100)

        # reducerea miscarii cursorului pentru miscari mici
        self.fine_control_X = np.zeros(2)
        self.fine_control_Y = np.zeros(2)
        #  self.fine_control_X = np.zeros(4)
        #  self.fine_control_Y = np.zeros(4)

        # apel functie pentru verificarea miscarii
        self.check_move_timer()
        self.timer_move_detected = None

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
                # coordonatele x si y ale degetului aratator
                x = hand_landmarks.landmark[8].x * frame.shape[1]
                y = hand_landmarks.landmark[8].y * frame.shape[0]
                self.move_cursor(x, y)
                self.click_functionality(hand_landmarks)
                self.recenter_cursor(hand_landmarks)
        else:
            frame_markers = frame
        return frame_markers

        # procesarea reperelor si apelarea diferitor actiuni

    def check_move_timer(self):
        self.timer_dwell = QTimer()
        self.timer_dwell.timeout.connect(self.check_move)
        self.timer_dwell.start(1800)

    def check_move(self):
        if self.move and (self.move_detected == 0):
            #  print("mouse click")
            self.timer_dwell.start(1600)
        self.move_detected = 0

    def move_cursor(self, cX, cY):
        filter_move = self.filter
        # variabile pentru reducerea miscarilor mici
        noise_X = filter_move
        noise_Y = filter_move

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

        # la miscare mai semnificativa se face diferenta pentru filtru folosit
        if (abs(delta_X) > abs(noise_X)):
            move_X = -(delta_X - noise_X)

        if (abs(delta_Y) > abs(noise_Y)):
            move_Y = -(delta_Y - noise_Y)

        # print(self.moveCursorCheckBox.checkState())
        # daca este bifata realizarea miscarii
        if self.move:
            sensitivity = self.speedCursor / 100
            # misca cursorul pe axa x
            move_X_final, move_x = self.digital_filter_cursor_X(move_X, sensitivity)
            # pyautogui.moveRel(int(round(-move_X_final)), 0)

            # misca cursorul pe axa y
            move_Y_final, move_y = self.digital_filter_cursor_Y(move_Y, sensitivity)
            # pyautogui.moveRel(0, int(round(move_Y_final)))
            # rezolvare diagonala
            pyautogui.moveRel(int(round(-move_X_final)), int(round(-move_Y_final)))
            # print(move_Y_final, move_X_final)
            # detectare miscare pentru dwell click
            if move_x or move_y:
                self.move_detected = 1

        # returneaza miscarea pe x si y
        return move_X, move_Y

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
            print(c)
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
        speed_final = speed * abs(sum_X) / (2 * 200)
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
        if (numtaps == 0):
            y_out = dy
        # filtru Finite Impulse Response pentru a reduce din zgomot
        else:
            # frecventa de taiere, atenueaza semnalul
            f = 0.1
            # coeficientii filtrului
            c = signal.firwin(numtaps, f)
            print(c)
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
        if (abs(y_out) > NK_DWELL_MOVE_THRESH):
            move = 1

        return y_out, move

    def recenter_cursor(self, hand_landmarks):
        distance_index_finger = calculate_distance(hand_landmarks.landmark[8], hand_landmarks.landmark[5])
        distance_average = np.average([calculate_distance(hand_landmarks.landmark[11], hand_landmarks.landmark[10]),
                                       calculate_distance(hand_landmarks.landmark[15], hand_landmarks.landmark[14]),
                                       calculate_distance(hand_landmarks.landmark[19], hand_landmarks.landmark[18])])
        threshold = distance_average/distance_index_finger
        if threshold <= 0.08 and self.move_detected is 0:
            if self.timer_move_detected is None:
                    self.timer_move_detected = time.time()
            elif time.time() - self.timer_move_detected >= 3:
                    # print('a trecut de timp')
                    screen_width, screen_height = pyautogui.size()
                    center_x = screen_width // 2
                    center_y = screen_height // 2

                    pyautogui.moveTo(center_x, center_y)
                    pyautogui.sleep(1)

                    self.timer_move_detected = None
        else:
                # Reset head returned time if head is not in initial position
            self.timer_move_detected = None


    def click_functionality(self, hand_landmarks):
        # calculeaza distante intre puncte specifice pentru miscarea mainii sau click
        absStandard = calculate_distance(hand_landmarks.landmark[0], hand_landmarks.landmark[1]) #distanta dintre baza mainii si inceputul degetului mare
        absClick = calculate_distance(hand_landmarks.landmark[4], hand_landmarks.landmark[6]) / absStandard # distanta dintre varful degetului mare si mijlocul degetului aratator

        #apelarea actiunilor pentru mouse
        self.click(absClick)

        #print('Nu a  intrat in if', self.nowLeftClick, self.previousLeftClick)
        if self.nowLeftClick == 1 and self.nowLeftClick != self.previousLeftClick:
            #print('A intrat in if', self.nowLeftClick, self.previousLeftClick)
            self.leftClick()

        if self.nowLeftClick == 0 and self.nowLeftClick != self.previousLeftClick:
            self.leftClickRelease()

        # print(self.nowRightClick)
        if self.nowRightClick == 1 and self.nowRightClick != self.previousRightClick:
            self.rightClick()

        #daca degetul aratator este strans

        if hand_landmarks.landmark[8].y - hand_landmarks.landmark[5].y > -0.06:
            # print(hand_landmarks.landmark[8].y - hand_landmarks.landmark[5].y)
            self.move = False
            self.Scroll(hand_landmarks.landmark[5].y - hand_landmarks.landmark[4].y)
        else:
            self.move = True

        #actualizare click flag
        self.previousLeftClick = self.nowLeftClick
        self.previousRightClick = self.nowRightClick

    def click(self, absClick):
        #click stanga
        if absClick < self.distance_click:
            self.nowLeftClick = 1

        elif absClick >= self.distance_click:
            self.nowLeftClick = 0

        if self.move_detected:  # miscarea mainii
            self.before_right_click = 0

        #daca se identifica leftclick si miscarea e minimala ceea ce indica ca, k = 0 atunci porneste un timer
        if self.nowLeftClick == 1 and self.move_detected == 0:
            if self.before_right_click == 0:
                self.start = time.perf_counter()
                self.before_right_click += 1
            end = time.perf_counter()
            #daca timer ul dureaza mai mult de 1.5 secunde se face click dreapta
            if end - self.start > 1.5:
                self.nowRightClick = 1
        else:
            self.nowRightClick = 0

    # click stanga

    def leftClick(self):
        if self.after_right_click == 1:
            self.after_right_click = 0
        pyautogui.mouseDown()

    # eliberare click stanga

    def leftClickRelease(self):
        pyautogui.mouseUp()
        # resetare k
        self.before_right_click = 0

        # verificarea unui potential dublu click
        if self.doubleClick == 0:
            self.c_start = time.perf_counter()
            self.doubleClick += 1
        c_end = time.perf_counter()
        # verifica daca se ramane in pozitia respectiva pentru mai mult de 1 secunda
        if 10 * (c_end - self.c_start) > 10 and self.doubleClick == 1:
            # self.mouse.click(Button.left, 2)
            print('double click')
            pyautogui.doubleClick()
            self.doubleClick = 0

    # click dreapta
    def rightClick(self):
        pyautogui.rightClick()
        self.after_right_click = 1

    # scroll pe verticala
    def Scroll(self, dy):
        # print('dy inainte=', dy)

        dy = dy * 1080
        # print('dy dupa * 1080', dy)
        pyautogui.scroll(dy / 50)

        #### asigura ca nu se misca mouse ul in momentul asta



