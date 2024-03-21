from .main_window import *

class UIFunctions(QMainWindow):
    def clickBtnCon(self, name):
        button = self.findChild(QPushButton, name)
        button.clicked.connect(self.Button)