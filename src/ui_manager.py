import sys
from PyQt5.QtWidgets import *
from ui import *
from PyQt5.QtCore import QSettings
class UIManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        window = MainWindow()
        sys.exit(self.app.exec_())
        # settings = QSettings("Licenta", "CamControl")


        # Load the state of the checkbox
    #     first_time = settings.value('isFirstTime')
    #     print(first_time)
    #     first_time = True ####
    #     if first_time is True:
    #         self.launch_setup()
    #         settings.setValue('isFirstTime', False)
    #     else:
    #         self.launch_main()
    #
    #     # window.close()
    #     sys.exit(self.app.exec_())
    #
    # def launch_main(self):
    #     self.window = MainWindow()
    #
    # def launch_setup(self):
    #     self.window = SetupWindow()


