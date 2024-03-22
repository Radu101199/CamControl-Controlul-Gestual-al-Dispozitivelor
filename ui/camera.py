import cv2
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer
from PyQt5 import QtGui
from .ui_modules import *
from src.face_module import *
from src.hand_module import *


class Camera:
    def __init__(self, main_window, part, camera_id: int = 0):
        self.main_window = main_window
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(camera_id)
        self.part = part
        if self.cap is None or not self.cap.isOpened():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Unable to open Camera!")
            print("Unable to open Camera!")
            msg.exec_()

        if self.part == 'Face':
            move = self.main_window.ui.moveCursorCheckBox.isChecked()
            speedX = self.main_window.ui.speedSlider_X.value()
            speedY = self.main_window.ui.speedSlider_Y.value()
            filter = self.main_window.ui.filterSlider.value()
            filterX = self.main_window.ui.filterSlider_X.value()
            filterY = self.main_window.ui.filterSlider_Y.value()
            self.mod = FaceModule(move, speedX, speedY, filter, filterX, filterY)
        else:
            self.mod = HandModule()

    def select_camera(self, id):
        camera = id
        self.cap = cv2.VideoCapture(int(camera))
        return self.cap

    def close(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.cap = None

    def get_frame(self):
        # daca camera nu este disponibila returneaza eroare
        if self.cap is None or not self.cap.isOpened():
            return -1

        _, frame = self.cap.read()

        # detectare modul
        image = self.mod.detect(frame)
        if image is not None:
            frame_to_show = cv2.flip(frame, 1)
            image = cv2.cvtColor(frame_to_show, cv2.COLOR_BGR2RGB)

        # Qt asteapta un format de culoare RGB
        qimage = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format_RGB888)

        self.display_image(qimage)

    def display_image(self, qimage):
        if self.part == 'Face':
            self.main_window.ui.imageFrameFace.setPixmap(QtGui.QPixmap.fromImage(qimage))
            self.main_window.ui.imageFrameFace.setScaledContents(True)
        else:
            self.main_window.ui.imageFrameHands.setPixmap(QtGui.QPixmap.fromImage(qimage))
            self.main_window.ui.imageFrameHands.setScaledContents(True)

    def is_opened(self):
        return self.cap and self.cap.isOpened()
