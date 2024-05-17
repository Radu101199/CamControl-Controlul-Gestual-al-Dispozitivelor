from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import QSettings, QSize

from .ui_functions import UIFunctions
from .ui_modules import *
from .camera import *
import time
import platform
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)
        ## PRINT ==> SYSTEM
        print('System: ' + platform.system())
        print('Version: ' + platform.release())
        ## Generare UI
        UIFunctions.removeTitleBar(True)

        self.setWindowTitle('CamControl')
        UIFunctions.labelTitle(self, 'CamControl')
        UIFunctions.labelDescription(self, 'Set text')

        startSize = QSize(1000, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)

        # TOGGLE MENU
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))
        # END

        # Adauga butoanele
        self.ui.stackedWidget.setMinimumWidth(20)
        UIFunctions.addNewMenu(self, "Home", "btn_home", "", True)
        UIFunctions.addNewMenu(self, "Face", "btn_face", "", True)
        UIFunctions.addNewMenu(self, "Hands", "btn_hands", "", True)
        UIFunctions.addNewMenu(self, "Keyboard", "btn_keyboard", "", False)
        UIFunctions.addNewMenu(self, "Voice", "btn_voice", "", False)
        UIFunctions.addNewMenu(self, "Settings", "btn_settings", "", False)


        UIFunctions.selectStandardMenu(self, "btn_home")
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunctions.returnStatus(self) == 1:
                UIFunctions.maximize_restore(self)

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()

        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow

        UIFunctions.uiDefinitions(self)
        #####

        UIFunctions.load_settings(self)
        # UIFunctions.clickBtnCon(self,'btn_home')
        # UIFunctions.clickBtnCon(self, 'btn_face')
        # UIFunctions.clickBtnCon(self, 'btn_hands')
        # UIFunctions.clickBtnCon(self, 'btn_settings')
        # UIFunctions.clickBtnCon(self, 'btn_keyboard')
        # UIFunctions.clickBtnCon(self, 'btn_voice')
        UIFunctions.clickBtnCon(self, 'btn_save')
        UIFunctions.clickBtnCon(self, 'btn_recalibrate')


        self.camera = None
        UIFunctions.first_time(self)



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

        # KEYBOARD BTN
        if btn_widget.objectName() == "btn_keyboard":
            self.launch_feature('btn_keyboard')

        # VOICE BTN
        if btn_widget.objectName() == "btn_voice":
            self.launch_feature('btn_voice')

        if btn_widget.objectName() == "btn_recalibrate":

            UIFunctions.launch_calibration(self)


    def launch_feature(self, btn_name):
        if self.camera is not None:
            self.camera = Camera(self, self.camera.part)
            self.frame_timer()
        if btn_name == 'btn_voice':
            UIFunctions.launch_siri()
        else:
            UIFunctions.launch_keyboard()

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

    def reset_dwell_timer(self):
        self.timer_dwell.start(1800)

    def close_window(self):
        self.close()

    ## EVENT ==> MOUSE DOUBLE CLICK
    ########################################################################
    def eventFilter(self, watched, event):
        if watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())
    ## ==> END ##

    ## EVENT ==> MOUSE CLICK
    ########################################################################
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
        if event.buttons() == Qt.MidButton:
            print('Mouse click: MIDDLE BUTTON')
    ## ==> END ##

    ## EVENT ==> KEY PRESSED
    ########################################################################
    def keyPressEvent(self, event):
        print('Key: ' + str(event.key()) + ' | Text Press: ' + str(event.text()))
    ## ==> END ##

    ## EVENT ==> RESIZE EVENT
    ########################################################################
    def resizeEvent(self, event):
        self.resizeFunction()
        return super(MainWindow, self).resizeEvent(event)

    def resizeFunction(self):
        print('Height: ' + str(self.height()) + ' | Width: ' + str(self.width()))
    ## ==> END ##

