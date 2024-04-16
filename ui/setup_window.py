from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import QSettings
from .ui_main import Ui_MainWindow
from . import ui_setup
from .ui_setup import *
from .camera import *
import time
from .main_window import *
import sys
class SetupWindow(QMainWindow):
    def __init__(self, parent=None, list_calibration=None):
        super().__init__(parent)

        self.parent = parent
        self.list_calibration = list_calibration
        self.ui = Ui_SetupWindow()

        self.ui.setupUi(self)


        self.camera = None
        self.show()
        self.start_time = time.time()
        self.setup_timer()

    def setup_timer(self):
        self.setuptimer = QTimer(self)
        self.setuptimer.timeout.connect(self.showCamera)
        self.setuptimer.start(1000)

    def frame_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.camera.get_frame)
        self.timer.start(0.1)


    def showCamera(self):
        current_time = time.time()
        if current_time - self.start_time > 2:
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_calibration)
            print(self.list_calibration)
            self.camera = Camera(self, 'setup',0, self.list_calibration)
            self.frame_timer()
            self.setuptimer.stop()
        else:
            print(1)

    # def close_window(self):
    #     UIFunctions.close(self)
    def setup_complete(self):
        # self.hide()
        self.main_window.show()
        # self.Open.show()
