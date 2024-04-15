import sys
from PyQt5.QtWidgets import *
from ui import *
from PyQt5.QtCore import QSettings
from ui.setup_window import *

class UIManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        settings = QSettings("Licenta", "CamControl")
        # Load the state of the checkbox
        first_time = settings.value("isFirstTime", defaultValue=True, type=bool)
        if first_time is True:
            window = SetupWindow()
            settings.setValue('isFirstTime', False)
        else:
            window = MainWindow()

        # window.close()
        sys.exit(self.app.exec_())


