from .main_window import *
from PyQt5.QtCore import QSettings
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

        # Load the values of five sliders
        slider_values = settings.value("slider_values", type=list)
        self.ui.speedSlider_X.setValue(slider_values[0])
        self.ui.speedSlider_Y.setValue(slider_values[1])
        self.ui.filterSlider_X.setValue(slider_values[2])
        self.ui.filterSlider_Y.setValue(slider_values[3])
        self.ui.filterSlider.setValue(slider_values[4])

        hands_speed = settings.value("speedHandsCursor", type=float)
        self.ui.speedHandsSlider.setValue(hands_speed)


    def save_settings(self):
        settings = QSettings("Licenta", "CamControl")

        # Save the state of the checkbox
        checkbox_state = self.ui.moveFaceCursorCheckBox.isChecked()
        settings.setValue("moveFaceCursorCheckBox", checkbox_state)

        # Save the state of the checkbox
        checkbox_state = self.ui.moveHandsCursorCheckBox.isChecked()
        settings.setValue("moveHandsCursorCheckBox", checkbox_state)


        # Save the values of five sliders
        slider_values = [
            self.ui.speedSlider_X.value(),
            self.ui.speedSlider_Y.value(),
            self.ui.filterSlider_X.value(),
            self.ui.filterSlider_Y.value(),
            self.ui.filterSlider.value()
        ]
        settings.setValue("slider_values", slider_values)

        hands_speed = self.ui.speedHandsSlider.value()
        settings.setValue("speedHandsCursor", hands_speed)

        image_width = self.ui.imageFrameHands.frameGeometry().width()
        settings.setValue("image_width", image_width)
        print(image_width)
        image_height = self.ui.imageFrameHands.frameGeometry().height()
        settings.setValue("image_height", image_height)