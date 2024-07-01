import sys
from PyQt5.QtWidgets import *
from ui import *
from PyQt5.QtCore import QSettings
class UIManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        window = MainWindow()
        sys.exit(self.app.exec_())



