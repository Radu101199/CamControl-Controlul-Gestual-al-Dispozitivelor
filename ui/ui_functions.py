from .main_window import *
from PyQt5 import QtCore
from PyQt5.QtCore import QSettings, QPropertyAnimation, Qt
from PyQt5.QtGui import QFont, QColor
from .ui_styles import Style
import subprocess
# from .setup_window import *

count = 1
## ==> GLOBALS
GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True

class UIFunctions(QMainWindow):
    ## ==> GLOBALS
    GLOBAL_STATE = 0
    GLOBAL_TITLE_BAR = True

    def clickBtnCon(self, name):
        button = self.findChild(QPushButton, name)
        button.clicked.connect(self.Button)

    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.btn_maximize_restore.setToolTip("Restore")
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u":/16x16/icons/16x16/cil-window-restore.png"))
            self.ui.frame_top_btns.setStyleSheet("background-color: rgb(27, 29, 35)")
            self.ui.frame_size_grip.hide()
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.ui.horizontalLayout.setContentsMargins(10, 10, 10, 10)
            self.ui.btn_maximize_restore.setToolTip("Maximize")
            self.ui.btn_maximize_restore.setIcon(QtGui.QIcon(u":/16x16/icons/16x16/cil-window-maximize.png"))
            self.ui.frame_top_btns.setStyleSheet("background-color: rgba(27, 29, 35, 200)")
            self.ui.frame_size_grip.show()

        ## ==> RETURN STATUS

    def returnStatus(self):
        return GLOBAL_STATE

        ## ==> SET STATUS

    def setStatus(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    def removeTitleBar(status):
        global GLOBAL_TITLE_BAR
        GLOBAL_TITLE_BAR = status

    def labelTitle(self, text):
        self.ui.label_title_bar_top.setText(text)
    def labelDescription(self, text):
        self.ui.label_top_info_1.setText(text)

    def toggleMenu(self, maxWidth, enable):
        if enable:
            # GET WIDTH
            width = self.ui.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 70

            # SET MAX WIDTH
            if width == 70:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    def addNewMenu(self, name, objName, icon, isTopMenu):
        font = QFont()
        font.setFamily(u"Segoe UI")
        button = QPushButton(str(count),self)
        button.setObjectName(objName)
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(sizePolicy3)
        button.setMinimumSize(QSize(0, 70))
        button.setLayoutDirection(Qt.LeftToRight)
        button.setFont(font)
        button.setStyleSheet(Style.style_bt_standard.replace('ICON_REPLACE', icon))
        button.setText(name)
        button.setToolTip(name)
        button.clicked.connect(self.Button)

        if isTopMenu:
            self.ui.layout_menus.addWidget(button)
        else:
            self.ui.layout_menu_bottom.addWidget(button)

    def selectStandardMenu(self, widget):
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(UIFunctions.selectMenu(w.styleSheet()))

    def selectMenu(getStyle):
        select = getStyle + ("QPushButton { border-right: 7px solid rgb(44, 49, 60); }")
        return select

    ## ==> DESELECT
    def deselectMenu(getStyle):
        deselect = getStyle.replace("QPushButton { border-right: 7px solid rgb(44, 49, 60); }", "")
        return deselect

    def uiDefinitions(self):
        def dobleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))

        ## REMOVE ==> STANDARD TITLE BAR
        if GLOBAL_TITLE_BAR:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.ui.frame_label_top_btns.mouseDoubleClickEvent = dobleClickMaximizeRestore
        else:
            self.ui.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.ui.frame_label_top_btns.setContentsMargins(8, 0, 0, 5)
            self.ui.frame_label_top_btns.setMinimumHeight(42)
            self.ui.frame_icon_top_bar.hide()
            self.ui.frame_btns_right.hide()
            self.ui.frame_size_grip.hide()


        ## SHOW ==> DROP SHADOW
        # self.shadow = QGraphicsDropShadowEffect(self)
        # self.shadow.setBlurRadius(17)
        # self.shadow.setXOffset(0)
        # self.shadow.setYOffset(0)
        # self.shadow.setColor(QColor(0, 0, 0, 150))
        # self.ui.frame_main.setGraphicsEffect(self.shadow)

        ## ==> RESIZE WINDOW
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        ### ==> MINIMIZE
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())

        ## ==> MAXIMIZE/RESTORE
        self.ui.btn_maximize_restore.clicked.connect(lambda: UIFunctions.maximize_restore(self))

        ## SHOW ==> CLOSE APPLICATION
        self.ui.btn_close.clicked.connect(lambda: self.close())


    def load_settings(self):
        settings = QSettings("Licenta", "CamControl")
        # Load the state of the checkbox
        checkbox_state = settings.value("moveFaceCursorCheckBox", defaultValue=True, type=bool)
        self.ui.moveFaceCursorCheckBox.setChecked(checkbox_state)
        # Load the state of the checkbox
        checkbox_state = settings.value("moveHandsCursorCheckBox", defaultValue=True, type=bool)
        self.ui.moveHandsCursorCheckBox.setChecked(checkbox_state)

        # Load the state of the checkbox
        checkbox_state = settings.value("smileCenterCheckBox", defaultValue=True, type=bool)
        self.ui.smileCenterCheckBox.setChecked(checkbox_state)
        # Load the state of the checkbox
        checkbox_state = settings.value("dwellClickCheckBox", defaultValue=True, type=bool)
        self.ui.dwellClickCheckBox.setChecked(checkbox_state)

        radiobox_state = settings.value("dwellClickRadioBox", defaultValue=True, type=bool)
        self.ui.dwellClickRadioBox.setChecked(radiobox_state)

        radiobox_state = settings.value("dwellScrollRadioBox", defaultValue=True, type=bool)
        self.ui.dwellScrollRadioBox.setChecked(radiobox_state)

        # Load the values of five sliders face
        slider_values_face = settings.value("slider_values_face", type=list)
        self.ui.speedSlider_X.setValue(slider_values_face[0])
        self.ui.speedSlider_Y.setValue(slider_values_face[1])
        self.ui.filterSlider_X_Face.setValue(slider_values_face[2])
        self.ui.filterSlider_Y_Face.setValue(slider_values_face[3])
        self.ui.filterSlider_Face.setValue(slider_values_face[4])

        # Load the values of sliders hands
        slider_values_hands = settings.value("slider_values_hands", type=list)
        self.ui.speedHandsSlider.setValue(slider_values_hands[0])
        self.ui.filterSlider_X_Hands.setValue(slider_values_hands[1])
        self.ui.filterSlider_Y_Hands.setValue(slider_values_hands[2])
        self.ui.filterSlider_Hands.setValue(slider_values_hands[3])


    def save_settings(self):
        settings = QSettings("Licenta", "CamControl")

        # Save the state of the checkbox
        checkbox_state = self.ui.moveFaceCursorCheckBox.isChecked()
        settings.setValue("moveFaceCursorCheckBox", checkbox_state)

        # Save the state of the checkbox
        checkbox_state = self.ui.moveHandsCursorCheckBox.isChecked()
        settings.setValue("moveHandsCursorCheckBox", checkbox_state)

        # Save the state of the checkbox
        checkbox_state = self.ui.smileCenterCheckBox.isChecked()
        settings.setValue("smileCenterCheckBox", checkbox_state)

        # Save the state of the checkbox
        checkbox_state = self.ui.dwellClickCheckBox.isChecked()
        settings.setValue("dwellClickCheckBox", checkbox_state)

        radiobox_state = self.ui.dwellClickRadioBox.isChecked()
        settings.setValue("dwellClickRadioBox", radiobox_state)

        radiobox_state = self.ui.dwellScrollRadioBox.isChecked()
        settings.setValue("dwellScrollRadioBox", radiobox_state)

        # Save the values of five sliders face
        slider_values_face = [
            self.ui.speedSlider_X.value(),
            self.ui.speedSlider_Y.value(),
            self.ui.filterSlider_X_Face.value(),
            self.ui.filterSlider_Y_Face.value(),
            self.ui.filterSlider_Face.value()
        ]
        settings.setValue("slider_values_face", slider_values_face)

        # Save the values of sliders hands
        slider_values_hands = [
            self.ui.speedHandsSlider.value(),
            self.ui.filterSlider_X_Hands.value(),
            self.ui.filterSlider_Y_Hands.value(),
            self.ui.filterSlider_Hands.value()
        ]
        settings.setValue("slider_values_hands", slider_values_hands)

    def first_time(self):
        settings = QSettings("Licenta", "CamControl")

        first_time = settings.value('isFirstTime')
        if first_time is True or first_time is None:
            from ui import SetupWindow
            self.setup_window = SetupWindow(self)
            self.close()
            settings.setValue('isFirstTime', False)
        else:
            self.show()

    def launch_calibration(self):
        list_calibration = []
        checkboxes = [
            ('face_click_left', self.ui.face_click_left_checkBox.isChecked()),
            ('face_click_right', self.ui.face_click_right_checkBox.isChecked()),
            ('face_smile', self.ui.face_smile_checkBox.isChecked()),
            ('hand_click', self.ui.hand_click_checkBox.isChecked()),
            ('hand_recenter', self.ui.hand_recenter_checkBox.isChecked()),
            ('hand_volume', self.ui.hand_volume_checkBox.isChecked())
        ]

        for checkbox_name, checkbox_state in checkboxes:
            if checkbox_state:
                list_calibration.append(checkbox_name)
        print(list_calibration)
        from ui import SetupWindow
        self.close()
        self.setup_window = SetupWindow(self, list_calibration)

    @staticmethod
    def launch_keyboard():
        applescript_code = '''
        tell application "System Settings"
            if not running then
                run
                delay 1
            end if
            set current pane to pane id "com.apple.Accessibility-Settings.extension"
            delay 1
        end tell
        tell application "System Events"
            tell window 1 of application process "System Settings"
                tell button 2 of group 3 of scroll area 1 of group 1 of list 2 of splitter group 1 of list 1
                    click
                    delay 1
                end tell
            end tell
        end tell

        tell application "System Events"
            tell window 1 of application process "System Settings"
                tell checkbox "Tastatură de accesibilitate" of group 3 of scroll area 1 of group 1 of list 2 of splitter group 1 of list 1
                    click
                    delay 1
                end tell
            end tell
        end tell

        tell application "System Settings"
            quit
        end tell
        '''
        # Run the AppleScript code
        subprocess.run(['osascript', '-e', applescript_code])

    @staticmethod
    def launch_siri():
        subprocess.Popen(
            ["/usr/bin/open", "-W", "-n", "-a", "/System/Applications/Siri.app"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE
        )