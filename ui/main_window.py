from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import QSettings
from .ui_modules import *
from .camera import *
import time
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)
        UIFunctions.load_settings(self)
        UIFunctions.clickBtnCon(self,'btn_home')
        UIFunctions.clickBtnCon(self, 'btn_face')
        UIFunctions.clickBtnCon(self, 'btn_hands')
        UIFunctions.clickBtnCon(self, 'btn_settings')
        UIFunctions.clickBtnCon(self, 'btn_save')



        self.camera = None
        self.show()

    def Button(self):
        btn_widget = self.sender()

        # PAGE HOME
        if btn_widget.objectName() == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        if self.camera is not None:
            if self.camera.is_opened():
                self.camera.close()

        # PAGE FACE
        if btn_widget.objectName() == "btn_face":
            if self.camera is not None:
                if self.camera.is_opened():
                    self.camera.close()
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_face)
            self.camera = Camera(self, 'Face')
            self.frame_timer()


        # PAGE HANDS
        if btn_widget.objectName() == "btn_hands":
            if self.camera is not None:
                if self.camera.is_opened():
                    self.camera.close()
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_hands)
            self.camera = Camera(self, 'Hands')
            self.frame_timer()

        # PAGE SETTINGS
        if btn_widget.objectName() == "btn_settings":
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_settings)
            if self.camera is not None:
                if self.camera.is_opened():
                    self.camera.close()

        # SAVE BTN
        if btn_widget.objectName() == "btn_save":
            UIFunctions.save_settings(self)
            self.repaint()
            UIFunctions.load_settings(self)


    def display_image(self, qimage, part):
        if part == 'Face':
            self.ui.imageFrameFace.setPixmap(QtGui.QPixmap.fromImage(qimage))
            self.ui.imageFrameFace.setScaledContents(True)
        else:
            self.ui.imageFrameHands.setPixmap(QtGui.QPixmap.fromImage(qimage))
            self.ui.imageFrameHands.setScaledContents(True)

    def frame_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.camera.get_frame)
        self.timer.start(0.1)
