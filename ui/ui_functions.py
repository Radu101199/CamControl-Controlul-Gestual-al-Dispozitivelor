from .main_window import *
from PyQt5.QtCore import QSettings
import subprocess
# from .setup_window import *

class UIFunctions(QMainWindow):
    def clickBtnCon(self, name):
        button = self.findChild(QPushButton, name)
        button.clicked.connect(self.Button)

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