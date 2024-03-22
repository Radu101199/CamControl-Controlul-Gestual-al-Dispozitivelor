from mediapipe.python.solutions import face_mesh
import numpy as np
import cv2
import pyautogui
from .app_utils import *
from scipy import signal

NK_DWELL_MOVE_THRESH = 10
# anuleaza inchiderea aplicatiei cand coltul din stanga sus este atins
pyautogui.FAILSAFE = False
# mareste viteza
pyautogui.PAUSE = 0
class FaceModule:
    def __init__(self, move, speedX, speedY, filter, filterX, filterY):
        self.face_mesh = face_mesh.FaceMesh(refine_landmarks=True)

        # initializare variabile
        # miscare cursor
        self.cX_prev = 0
        self.cY_prev = 0
        # variabila pentru prima miscare a cursorului
        self.first_data = 0
        # filtrarea datelor privind miscarea cursorului
        self.filter_cursor_X = np.zeros(100)
        self.filter_cursor_Y = np.zeros(100)

        # reducerea miscarii cursorului pentru miscari mici
        self.fine_control_X = np.zeros(2)
        self.fine_control_Y = np.zeros(2)
        #  self.fine_control_X = np.zeros(4)
        #  self.fine_control_Y = np.zeros(4)

        self.move = move
        self.speedX = speedX
        self.speedY = speedY
        self.filter = filter
        self.filterX = filterX
        self.filterY = filterY

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

                x = (bounding_box[0][0] + bounding_box[1][0]) / 2
                y = (bounding_box[0][1] + bounding_box[1][1]) / 2
                self.move_cursor(self.move, x, y)


        else:
            frame_markers = frame
        return frame_markers

        # misca cursor
    def move_cursor(self, move, cX, cY):
        # valori din GUI
        # filter_move = self.filterSliderBox.value()
         # = self.speedSpinBox_X.value()
        # speed_Y = self.speedSpinBox_Y.value()

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
            return move_X, move_Y

        # la miscare mai semnficiativa se face diferenta pentru filtru folosit
        if (abs(delta_X) > abs(noise_X)):
            move_X = -(delta_X - noise_X)

        if (abs(delta_Y) > abs(noise_Y)):
            move_Y = delta_Y - noise_Y

        # daca este bifata realizarea miscarii
        if (move == 1):
            # misca cursorul pe axa x
            move_X_final, move_x = self.digital_filter_cursor_X(move_X, self.speedX)
            pyautogui.moveRel(int(round(move_X_final)), 0)

            # misca cursorul pe axa y
            move_Y_final, move_y = self.digital_filter_cursor_Y(move_Y, self.speedY)
            pyautogui.moveRel(0, int(round(move_Y_final)))

            # detectare miscare pentru dwell click
            if move_x or move_y:
                self.move_detected = 1

        # returneaza miscarea pe x si y
        return move_X, move_Y

    # filtru pentru miscarea cursorului pe x
    def digital_filter_cursor_X(self, dx, speed):
        # numtaps = self.filterSpinBox_X.value()
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

        # scalarea pentru o analiza mai usoara
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

        # scalarea pentru o analiza mai usoara
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

