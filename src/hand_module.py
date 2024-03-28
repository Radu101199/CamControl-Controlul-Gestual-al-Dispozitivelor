import cv2

from .app_utils import *
from mediapipe.python.solutions import hands as mp_hands
from mediapipe.python.solutions import drawing_utils as mp_drawing
import pyautogui
from PyQt5.QtCore import QSettings
import time

# anuleaza inchiderea aplicatiei cand coltul din stanga sus este atins
pyautogui.FAILSAFE = False
# mareste viteza
pyautogui.PAUSE = 0
THRESHOLD = 3.5
class HandModule:
    def __init__(self, camera):
        self.camera = camera

        self.hands = mp_hands.Hands(min_detection_confidence=0.8,
        min_tracking_confidence=0.8,
        max_num_hands=1
    )

        settings = QSettings("Licenta", "CamControl")
        self.move = settings.value("moveHandsCursorCheckBox", type=bool)
        self.speedCursor = settings.value("speedHandsCursor", type=float)
        self.image_width = settings.value("image_width", type=float)
        self.image_height = settings.value("image_height", type=float)

        # Initializare variabile
        self.cfps = int(camera.get_fps())# implementare functie in caemra
        # maximul dintre 1 si o zecime din numarul de frame uri pe secunda
        self.smoothingFactor = max(int(self.cfps / 10), 1)
        self.distance = 0.7
        self.previousX, self.previousY = 0, 0
        self.i, self.k, self.h = 0, 0, 0
        self.listX, self.listY, self.list0x, self.list0y, self.list1x, self.list1y, self.list4x, self.list4y, self.list6x, self.list6y, self.list8x, self.list8y, self.list12x, self.list12y = [
        ], [], [], [], [], [], [], [], [], [], [], [], [], []
        self.keyPressed = 0
        self.nowRightClick, self.nowLeftClick = 0, 0
        self.previousRightClick, self.previousLeftClick = 0, 0
        self.doubleClick = 0
        self.x = 0
        self.y = 0

        self.threshold = 3.5


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
                if self.move is True:
                    self.nowMovement = 1
                    # initializarea primelor date
                    if self.i == 0:
                        # preluare marime ecran
                        screen_width, screen_height = pyautogui.size()
                        # coordonate centrale
                        center_x = screen_width // 2
                        center_y = screen_height // 2

                        pyautogui.moveTo(center_x, center_y)

                        # pauza o secunda
                        time.sleep(1)

                        self.previousX = hand_landmarks.landmark[8].x
                        self.previousY = hand_landmarks.landmark[8].y
                        self.i += 1

                    self.preparation(hand_landmarks)
        else:
            self.nowMovement = 0
            frame_markers = frame
        return frame_markers

        # procesarea reperelor si apelarea diferitor actiuni

    def preparation(self, hand_landmarks):

        # calculeaza miscarea medie pentru coordonatele x si y a mai multor repere
        landmark0 = [calculate_moving_average(hand_landmarks.landmark[0].x, self.smoothingFactor, self.list0x),
                     calculate_moving_average(
                         hand_landmarks.landmark[0].y, self.smoothingFactor, self.list0y)]
        landmark1 = [calculate_moving_average(hand_landmarks.landmark[1].x, self.smoothingFactor, self.list1x),
                     calculate_moving_average(
                         hand_landmarks.landmark[1].y, self.smoothingFactor, self.list1y)]
        landmark4 = [calculate_moving_average(hand_landmarks.landmark[4].x, self.smoothingFactor, self.list4x),
                     calculate_moving_average(
                         hand_landmarks.landmark[4].y, self.smoothingFactor, self.list4y)]
        landmark6 = [calculate_moving_average(hand_landmarks.landmark[6].x, self.smoothingFactor, self.list6x),
                     calculate_moving_average(
                         hand_landmarks.landmark[6].y, self.smoothingFactor, self.list6y)]
        landmark8 = [calculate_moving_average(hand_landmarks.landmark[8].x, self.smoothingFactor, self.list8x),
                     calculate_moving_average(
                         hand_landmarks.landmark[8].y, self.smoothingFactor, self.list8y)]
        landmark12 = [calculate_moving_average(hand_landmarks.landmark[12].x, self.smoothingFactor, self.list12x),
                      calculate_moving_average(
                          hand_landmarks.landmark[12].y, self.smoothingFactor, self.list12y)]

        # calculeaza distante intre puncte specifice pentru miscarea mainii sau click
        absStandard = calculate_distance(landmark0,
                                         landmark1)  # distanta dintre baza mainii si inceputul degetului mare
        absMovement = calculate_distance(landmark8,
                                         landmark12) / absStandard  # distanta dintre varfurile degetelor aratatoare si mijlocii, impartita la absStandard pentru a mentine o valoare relativ constanta
        absClick = calculate_distance(landmark4,
                                      landmark6) / absStandard  # distanta dintre varful degetului mare si mijlocul degetului aratator

        # positionX, positionY = self.mouse.position

        # coordonatele curente x si y
        nowX = calculate_moving_average(
            hand_landmarks.landmark[8].x, self.smoothingFactor, self.listX)
        nowY = calculate_moving_average(
            hand_landmarks.landmark[8].y, self.smoothingFactor, self.listY)

        speed = self.speedCursor
        normalized_speed = speed / self.threshold
        # transpunerea acestora in imagine
        dx = normalized_speed * (nowX - self.previousX) * self.image_width
        dy = normalized_speed * (nowY - self.previousY) * self.image_height

        self.previousX = nowX
        self.previousY = nowY

        self.click(absClick, hand_landmarks, dx, dy)

        if absMovement >= self.distance and self.nowMovement == 1:
            self.move_cursor(dx, dy, hand_landmarks)

        # print('Nu a  intrat in if', self.nowLeftClick, self.previousLeftClick)
        if self.nowLeftClick == 1 and self.nowLeftClick != self.previousLeftClick:
            # print('A intrat in if', self.nowLeftClick, self.previousLeftClick)
            self.leftClick()

        # print(self.nowLeftClick, self.previousLeftClick)
        if self.nowLeftClick == 0 and self.nowLeftClick != self.previousLeftClick:
            # print('A intrat in if', self.nowLeftClick, self.previousLeftClick)
            self.leftClickRelease()
        # print(self.nowRightClick, self.previousRightClick)
        if self.nowRightClick == 1 and self.nowRightClick != self.previousRightClick:
            self.rightClick()

        # daca degetul aratator este strans
        if hand_landmarks.landmark[8].y - hand_landmarks.landmark[5].y > -0.06:
            self.Scroll(hand_landmarks, dx, dy)
        else:
            self.nowMovement = 1

        # actualizare click flag
        self.previousLeftClick = self.nowLeftClick
        self.previousRightClick = self.nowRightClick

    def click(self, absClick, hand_landmarks, dx, dy):
        # click stanga
        if absClick < self.distance:
            self.nowLeftClick = 1
            # draw_circle(self.qimage, hand_landmarks.landmark[8].x * self.image_width,
            #             hand_landmarks.landmark[8].y * self.image_height, 20, (0, 250, 250))

        elif absClick >= self.distance:
            self.nowLeftClick = 0

        if np.abs(dx) > 7 and np.abs(dy) > 7:  # miscarea mainii
            self.k = 0
        # print(absClick, self.distance)

        # daca se identifica leftclick si miscarea e minimala ceea ce indica ca k = 0 atunci porneste un timer
        if self.nowLeftClick == 1 and np.abs(dx) < 7 and np.abs(dy) < 7:
            if self.k == 0:
                self.start = time.perf_counter()
                self.k += 1
            end = time.perf_counter()
            # daca timer ul dureaza mai mult de 1.5 secunde se face click dreapta
            if end - self.start > 1.5:
                self.nowRightClick = 1
        else:
            self.nowRightClick = 0

            # click stanga

    def leftClick(self):
        print(self.h)
        if self.h == 1:
            self.h = 0
            # elif self.h == 0:
        pyautogui.mouseDown()
        # self.mouse.press(Button.left)

        # eliberare click stanga

    def leftClickRelease(self):
        pyautogui.mouseUp()
        # resetare k
        self.k = 0

        # verificarea unui potential dublu click
        if self.doubleClick == 0:
            self.c_start = time.perf_counter()
            self.doubleClick += 1
        c_end = time.perf_counter()
        # verifica daca se ramane in pozitia respectiva pentru mai mult de 1 secunda
        if 10 * (c_end - self.c_start) > 10 and self.doubleClick == 1:  # 0.5秒以内にもう一回クリックしたらダブルクリック
            # self.mouse.click(Button.left, 2)
            pyautogui.doubleClick()
            self.doubleClick = 0
        # click dreapta

    def rightClick(self):
        pyautogui.rightClick()
        self.h = 1

    def Scroll(self, hand_landmarks, dx, dy):
        # scroll pe verticala
        pyautogui.scroll(-dy / 50)

        # asigura ca nu se misca mouse ul in momentul asta
        self.nowMovement = 0

    def move_cursor(self, dx, dy, hand_landmarks):
        if abs(dx) > THRESHOLD or abs(dy) > THRESHOLD:
            pyautogui.move(dx, dy)

        self.x = hand_landmarks.landmark[8].x * self.image_width
        self.y = hand_landmarks.landmark[8].y * self.image_height
