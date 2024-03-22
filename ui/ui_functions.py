from .main_window import *
from PyQt5.QtCore import QSettings
class UIFunctions(QMainWindow):
    def clickBtnCon(self, name):
        button = self.findChild(QPushButton, name)
        button.clicked.connect(self.Button)

    def load_settings(self):
        settings = QSettings("Licenta", "CamControl")
        checkbox_state = settings.value("moveCursorCheckBox", defaultValue=True, type=bool)
        checkbox = self.findChild(QCheckBox, 'moveCursorCheckBox')
        checkbox.setChecked(False)

    def save_settings(self):
        settings = QSettings("Licenta", "CamControl")
        checkbox_state = QMainWindow.moveCursorCheckBox.isChecked()
        settings.setValue("moveCursorCheckBox", checkbox_state)