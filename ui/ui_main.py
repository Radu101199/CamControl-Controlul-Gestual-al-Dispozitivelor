# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1012, 738)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_main = QtWidgets.QFrame(self.centralwidget)
        self.frame_main.setStyleSheet("/* LINE EDIT */\n"
"QLineEdit {\n"
"    background-color: rgb(27, 29, 35);\n"
"    border-radius: 5px;\n"
"    border: 2px solid rgb(27, 29, 35);\n"
"    padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"    border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* SCROLL BARS */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"    border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(85, 170, 255);\n"
"    min-width: 25px;\n"
"    border-radius: 7px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"    border-top-right-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"    border-top-left-radius: 7px;\n"
"    border-bottom-left-radius: 7px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"    border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {    \n"
"    background: rgb(85, 170, 255);\n"
"    min-height: 25px;\n"
"    border-radius: 7px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"    border-bottom-left-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"    border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* CHECKBOX */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"    border: 3px solid rgb(52, 59, 72);    \n"
"    background-image: url(:/16x16/icons/16x16/cil-check-alt.png);\n"
"}\n"
"\n"
"/* RADIO BUTTON */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"    border: 3px solid rgb(52, 59, 72);    \n"
"}\n"
"\n"
"/* COMBOBOX */\n"
"QComboBox{\n"
"    background-color: rgb(27, 29, 35);\n"
"    border-radius: 5px;\n"
"    border: 2px solid rgb(27, 29, 35);\n"
"    padding: 5px;\n"
"    padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"    border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 25px; \n"
"    border-left-width: 3px;\n"
"    border-left-color: rgba(39, 44, 54, 150);\n"
"    border-left-style: solid;\n"
"    border-top-right-radius: 3px;\n"
"    border-bottom-right-radius: 3px;    \n"
"    background-image: url(:/16x16/icons/16x16/cil-arrow-bottom.png);\n"
"    background-position: center;\n"
"    background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"    color: rgb(85, 170, 255);    \n"
"    background-color: rgb(27, 29, 35);\n"
"    padding: 10px;\n"
"    selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* SLIDERS */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 9px;\n"
"    height: 18px;\n"
"    margin: 0px;\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"    background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(85, 170, 255);\n"
"    border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"    border-radius: 9px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(105, 180, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(65, 130, 195);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 9px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"    background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(85, 170, 255);\n"
"    border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"    border-radius: 9px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(105, 180, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(65, 130, 195);\n"
"}\n"
"\n"
"")
        self.frame_main.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_main.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_main.setObjectName("frame_main")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_main)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_top = QtWidgets.QFrame(self.frame_main)
        self.frame_top.setMinimumSize(QtCore.QSize(0, 65))
        self.frame_top.setStyleSheet("background-color: transparent;")
        self.frame_top.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_top.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top.setObjectName("frame_top")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_top)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.frame_toggle = QtWidgets.QFrame(self.frame_top)
        self.frame_toggle.setMaximumSize(QtCore.QSize(70, 65))
        self.frame_toggle.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_toggle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_toggle.setObjectName("frame_toggle")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_toggle)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btn_toggle_menu = QtWidgets.QPushButton(self.frame_toggle)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_toggle_menu.sizePolicy().hasHeightForWidth())
        self.btn_toggle_menu.setSizePolicy(sizePolicy)
        self.btn_toggle_menu.setMinimumSize(QtCore.QSize(70, 65))
        self.btn_toggle_menu.setStyleSheet("QPushButton {\n"
"    background-image: url();\n"
"    background-position: center;\n"
"    background-repeat: no-reperat;\n"
"    border: none;\n"
"    background-color: rgb(27, 29, 35);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_toggle_menu.setObjectName("btn_toggle_menu")
        self.verticalLayout_3.addWidget(self.btn_toggle_menu)
        self.horizontalLayout_7.addWidget(self.frame_toggle)
        self.frame_top_right = QtWidgets.QFrame(self.frame_top)
        self.frame_top_right.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_top_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top_right.setObjectName("frame_top_right")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_top_right)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_top_btns = QtWidgets.QFrame(self.frame_top_right)
        self.frame_top_btns.setMinimumSize(QtCore.QSize(0, 42))
        self.frame_top_btns.setStyleSheet("background-color: rgba(27, 29, 35, 200)")
        self.frame_top_btns.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_top_btns.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top_btns.setObjectName("frame_top_btns")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_top_btns)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.frame_3 = QtWidgets.QFrame(self.frame_top_btns)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_8.addWidget(self.frame_3)
        self.frame_btns_right = QtWidgets.QFrame(self.frame_top_btns)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_btns_right.sizePolicy().hasHeightForWidth())
        self.frame_btns_right.setSizePolicy(sizePolicy)
        self.frame_btns_right.setMaximumSize(QtCore.QSize(120, 42))
        self.frame_btns_right.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_btns_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_btns_right.setObjectName("frame_btns_right")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_btns_right)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.btnMinimize = QtWidgets.QPushButton(self.frame_btns_right)
        self.btnMinimize.setMinimumSize(QtCore.QSize(40, 42))
        self.btnMinimize.setStyleSheet("QPushButton {    \n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btnMinimize.setObjectName("btnMinimize")
        self.horizontalLayout_9.addWidget(self.btnMinimize)
        self.btnRestore = QtWidgets.QPushButton(self.frame_btns_right)
        self.btnRestore.setMinimumSize(QtCore.QSize(40, 42))
        self.btnRestore.setStyleSheet("QPushButton {    \n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btnRestore.setObjectName("btnRestore")
        self.horizontalLayout_9.addWidget(self.btnRestore)
        self.btnClose = QtWidgets.QPushButton(self.frame_btns_right)
        self.btnClose.setMinimumSize(QtCore.QSize(40, 42))
        self.btnClose.setStyleSheet("QPushButton {    \n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btnClose.setObjectName("btnClose")
        self.horizontalLayout_9.addWidget(self.btnClose)
        self.horizontalLayout_8.addWidget(self.frame_btns_right)
        self.verticalLayout_4.addWidget(self.frame_top_btns)
        self.frame_info = QtWidgets.QFrame(self.frame_top_right)
        self.frame_info.setMinimumSize(QtCore.QSize(0, 23))
        self.frame_info.setStyleSheet("background-color: rgba(27, 29, 35, 200)")
        self.frame_info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_info.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_info.setObjectName("frame_info")
        self.verticalLayout_4.addWidget(self.frame_info)
        self.horizontalLayout_7.addWidget(self.frame_top_right)
        self.verticalLayout.addWidget(self.frame_top, 0, QtCore.Qt.AlignTop)
        self.frame_center = QtWidgets.QFrame(self.frame_main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_center.sizePolicy().hasHeightForWidth())
        self.frame_center.setSizePolicy(sizePolicy)
        self.frame_center.setStyleSheet("background-color: rgb(40, 44, 52);")
        self.frame_center.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_center.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_center.setObjectName("frame_center")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_center)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_left_menu = QtWidgets.QFrame(self.frame_center)
        self.frame_left_menu.setMinimumSize(QtCore.QSize(70, 0))
        self.frame_left_menu.setMaximumSize(QtCore.QSize(70, 16777215))
        self.frame_left_menu.setStyleSheet("background-color: rgb(27, 29, 35);")
        self.frame_left_menu.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_left_menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_left_menu.setObjectName("frame_left_menu")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_left_menu)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame_menu = QtWidgets.QFrame(self.frame_left_menu)
        self.frame_menu.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_menu.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_menu.setObjectName("frame_menu")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_menu)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.btn_home = QtWidgets.QPushButton(self.frame_menu)
        self.btn_home.setMinimumSize(QtCore.QSize(70, 60))
        self.btn_home.setStyleSheet("QPushButton {\n"
"\n"
"    background-position: center;\n"
"    background-repeat: no-reperat;\n"
"    border: none;\n"
"    background-color: rgb(27, 29, 35);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_home.setObjectName("btn_home")
        self.verticalLayout_6.addWidget(self.btn_home)
        self.btn_face = QtWidgets.QPushButton(self.frame_menu)
        self.btn_face.setMinimumSize(QtCore.QSize(70, 60))
        self.btn_face.setStyleSheet("QPushButton {\n"
"\n"
"    background-position: center;\n"
"    background-repeat: no-reperat;\n"
"    border: none;\n"
"    background-color: rgb(27, 29, 35);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_face.setObjectName("btn_face")
        self.verticalLayout_6.addWidget(self.btn_face)
        self.btn_hands = QtWidgets.QPushButton(self.frame_menu)
        self.btn_hands.setMinimumSize(QtCore.QSize(70, 60))
        self.btn_hands.setStyleSheet("QPushButton {\n"
"\n"
"    background-position: center;\n"
"    background-repeat: no-reperat;\n"
"    border: none;\n"
"    background-color: rgb(27, 29, 35);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_hands.setObjectName("btn_hands")
        self.verticalLayout_6.addWidget(self.btn_hands)
        self.verticalLayout_5.addWidget(self.frame_menu, 0, QtCore.Qt.AlignTop)
        self.frame_settings = QtWidgets.QFrame(self.frame_left_menu)
        self.frame_settings.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_settings.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_settings.setObjectName("frame_settings")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_settings)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.btn_settings = QtWidgets.QPushButton(self.frame_settings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_settings.sizePolicy().hasHeightForWidth())
        self.btn_settings.setSizePolicy(sizePolicy)
        self.btn_settings.setMinimumSize(QtCore.QSize(0, 60))
        self.btn_settings.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_settings.setStyleSheet("QPushButton {\n"
"\n"
"    background-position: center;\n"
"    background-repeat: no-reperat;\n"
"    border: none;\n"
"    background-color: rgb(27, 29, 35);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_settings.setObjectName("btn_settings")
        self.verticalLayout_7.addWidget(self.btn_settings)
        self.verticalLayout_5.addWidget(self.frame_settings, 0, QtCore.Qt.AlignBottom)
        self.horizontalLayout_2.addWidget(self.frame_left_menu, 0, QtCore.Qt.AlignLeft)
        self.frame_content_right = QtWidgets.QFrame(self.frame_center)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_content_right.sizePolicy().hasHeightForWidth())
        self.frame_content_right.setSizePolicy(sizePolicy)
        self.frame_content_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_content_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_content_right.setObjectName("frame_content_right")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_content_right)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_content = QtWidgets.QFrame(self.frame_content_right)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_content.sizePolicy().hasHeightForWidth())
        self.frame_content.setSizePolicy(sizePolicy)
        self.frame_content.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_content.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_content.setObjectName("frame_content")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_content)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame_content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setMaximumSize(QtCore.QSize(1000, 1000))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_home = QtWidgets.QWidget()
        self.page_home.setObjectName("page_home")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page_home)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.page_home)
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.page_home)
        font = QtGui.QFont()
        font.setPointSize(35)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.page_home)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.stackedWidget.addWidget(self.page_home)
        self.page_face = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page_face.sizePolicy().hasHeightForWidth())
        self.page_face.setSizePolicy(sizePolicy)
        self.page_face.setObjectName("page_face")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.page_face)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.imageFrameFace = QtWidgets.QLabel(self.page_face)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageFrameFace.sizePolicy().hasHeightForWidth())
        self.imageFrameFace.setSizePolicy(sizePolicy)
        self.imageFrameFace.setMinimumSize(QtCore.QSize(860, 580))
        self.imageFrameFace.setMaximumSize(QtCore.QSize(1000, 1000))
        self.imageFrameFace.setAlignment(QtCore.Qt.AlignCenter)
        self.imageFrameFace.setObjectName("imageFrameFace")
        self.horizontalLayout_5.addWidget(self.imageFrameFace)
        self.stackedWidget.addWidget(self.page_face)
        self.page_hands = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.page_hands.sizePolicy().hasHeightForWidth())
        self.page_hands.setSizePolicy(sizePolicy)
        self.page_hands.setObjectName("page_hands")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.page_hands)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.imageFrameHands = QtWidgets.QLabel(self.page_hands)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageFrameHands.sizePolicy().hasHeightForWidth())
        self.imageFrameHands.setSizePolicy(sizePolicy)
        self.imageFrameHands.setMinimumSize(QtCore.QSize(860, 580))
        self.imageFrameHands.setAlignment(QtCore.Qt.AlignCenter)
        self.imageFrameHands.setObjectName("imageFrameHands")
        self.horizontalLayout_6.addWidget(self.imageFrameHands)
        self.stackedWidget.addWidget(self.page_hands)
        self.page_settings = QtWidgets.QWidget()
        self.page_settings.setObjectName("page_settings")
        self.label_4 = QtWidgets.QLabel(self.page_settings)
        self.label_4.setGeometry(QtCore.QRect(140, 50, 60, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.page_settings)
        self.label_5.setGeometry(QtCore.QRect(490, 50, 60, 16))
        self.label_5.setObjectName("label_5")
        self.moveFaceCursorCheckBox = QtWidgets.QCheckBox(self.page_settings)
        self.moveFaceCursorCheckBox.setGeometry(QtCore.QRect(90, 110, 111, 21))
        self.moveFaceCursorCheckBox.setObjectName("moveFaceCursorCheckBox")
        self.moveHandsCursorCheckBox = QtWidgets.QCheckBox(self.page_settings)
        self.moveHandsCursorCheckBox.setGeometry(QtCore.QRect(450, 110, 111, 21))
        self.moveHandsCursorCheckBox.setObjectName("moveHandsCursorCheckBox")
        self.speedSlider_X = QtWidgets.QSlider(self.page_settings)
        self.speedSlider_X.setGeometry(QtCore.QRect(90, 220, 160, 16))
        self.speedSlider_X.setMaximum(5)
        self.speedSlider_X.setSliderPosition(1)
        self.speedSlider_X.setOrientation(QtCore.Qt.Horizontal)
        self.speedSlider_X.setObjectName("speedSlider_X")
        self.label_6 = QtWidgets.QLabel(self.page_settings)
        self.label_6.setGeometry(QtCore.QRect(20, 220, 60, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.page_settings)
        self.label_7.setGeometry(QtCore.QRect(20, 260, 60, 16))
        self.label_7.setObjectName("label_7")
        self.speedSlider_Y = QtWidgets.QSlider(self.page_settings)
        self.speedSlider_Y.setGeometry(QtCore.QRect(90, 260, 160, 16))
        self.speedSlider_Y.setMaximum(5)
        self.speedSlider_Y.setSliderPosition(1)
        self.speedSlider_Y.setOrientation(QtCore.Qt.Horizontal)
        self.speedSlider_Y.setObjectName("speedSlider_Y")
        self.filterSlider_Y = QtWidgets.QSlider(self.page_settings)
        self.filterSlider_Y.setGeometry(QtCore.QRect(90, 350, 160, 16))
        self.filterSlider_Y.setMaximum(10)
        self.filterSlider_Y.setProperty("value", 6)
        self.filterSlider_Y.setSliderPosition(6)
        self.filterSlider_Y.setOrientation(QtCore.Qt.Horizontal)
        self.filterSlider_Y.setObjectName("filterSlider_Y")
        self.label_15 = QtWidgets.QLabel(self.page_settings)
        self.label_15.setGeometry(QtCore.QRect(20, 350, 60, 16))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.page_settings)
        self.label_16.setGeometry(QtCore.QRect(20, 306, 60, 20))
        self.label_16.setObjectName("label_16")
        self.filterSlider_X = QtWidgets.QSlider(self.page_settings)
        self.filterSlider_X.setGeometry(QtCore.QRect(90, 310, 160, 16))
        self.filterSlider_X.setMaximum(10)
        self.filterSlider_X.setProperty("value", 6)
        self.filterSlider_X.setSliderPosition(6)
        self.filterSlider_X.setOrientation(QtCore.Qt.Horizontal)
        self.filterSlider_X.setObjectName("filterSlider_X")
        self.filterSlider = QtWidgets.QSlider(self.page_settings)
        self.filterSlider.setGeometry(QtCore.QRect(90, 390, 160, 16))
        self.filterSlider.setMaximum(10)
        self.filterSlider.setProperty("value", 0)
        self.filterSlider.setSliderPosition(0)
        self.filterSlider.setOrientation(QtCore.Qt.Horizontal)
        self.filterSlider.setObjectName("filterSlider")
        self.label_17 = QtWidgets.QLabel(self.page_settings)
        self.label_17.setGeometry(QtCore.QRect(20, 390, 60, 16))
        self.label_17.setObjectName("label_17")
        self.btn_save = QtWidgets.QPushButton(self.page_settings)
        self.btn_save.setGeometry(QtCore.QRect(690, 510, 81, 26))
        self.btn_save.setObjectName("btn_save")
        self.label_28 = QtWidgets.QLabel(self.page_settings)
        self.label_28.setGeometry(QtCore.QRect(430, 220, 60, 16))
        self.label_28.setObjectName("label_28")
        self.speedHandsSlider = QtWidgets.QSlider(self.page_settings)
        self.speedHandsSlider.setGeometry(QtCore.QRect(500, 220, 160, 16))
        self.speedHandsSlider.setMinimum(4)
        self.speedHandsSlider.setMaximum(12)
        self.speedHandsSlider.setProperty("value", 5)
        self.speedHandsSlider.setSliderPosition(5)
        self.speedHandsSlider.setOrientation(QtCore.Qt.Horizontal)
        self.speedHandsSlider.setObjectName("speedHandsSlider")
        self.dwellClickCheckBox = QtWidgets.QCheckBox(self.page_settings)
        self.dwellClickCheckBox.setGeometry(QtCore.QRect(100, 450, 111, 21))
        self.dwellClickCheckBox.setObjectName("dwellClickCheckBox")
        self.smileCenterCheckBox = QtWidgets.QCheckBox(self.page_settings)
        self.smileCenterCheckBox.setGeometry(QtCore.QRect(100, 500, 111, 21))
        self.smileCenterCheckBox.setObjectName("smileCenterCheckBox")
        self.stackedWidget.addWidget(self.page_settings)
        self.horizontalLayout_4.addWidget(self.stackedWidget)
        self.horizontalLayout_3.addWidget(self.frame_content)
        self.horizontalLayout_2.addWidget(self.frame_content_right)
        self.verticalLayout.addWidget(self.frame_center)
        self.horizontalLayout.addWidget(self.frame_main)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btn_toggle_menu.setText(_translate("MainWindow", "Toggle"))
        self.btnMinimize.setText(_translate("MainWindow", "-"))
        self.btnRestore.setText(_translate("MainWindow", "#"))
        self.btnClose.setText(_translate("MainWindow", "X"))
        self.btn_home.setText(_translate("MainWindow", "Home"))
        self.btn_face.setText(_translate("MainWindow", "Face"))
        self.btn_hands.setText(_translate("MainWindow", "Hands"))
        self.btn_settings.setText(_translate("MainWindow", "Settings"))
        self.label.setText(_translate("MainWindow", "HOME"))
        self.label_2.setText(_translate("MainWindow", "CamControl"))
        self.label_3.setText(_translate("MainWindow", "Paun Raducu"))
        self.imageFrameFace.setText(_translate("MainWindow", "Camera not availalable!"))
        self.imageFrameHands.setText(_translate("MainWindow", "Camera not availalable!"))
        self.label_4.setText(_translate("MainWindow", "Face"))
        self.label_5.setText(_translate("MainWindow", "Hands"))
        self.moveFaceCursorCheckBox.setText(_translate("MainWindow", "Move Cursor"))
        self.moveHandsCursorCheckBox.setText(_translate("MainWindow", "Move Cursor"))
        self.label_6.setText(_translate("MainWindow", "Speed X"))
        self.label_7.setText(_translate("MainWindow", "Speed Y"))
        self.label_15.setText(_translate("MainWindow", "Filter Y"))
        self.label_16.setText(_translate("MainWindow", "Filter X"))
        self.label_17.setText(_translate("MainWindow", "Filter"))
        self.btn_save.setText(_translate("MainWindow", "Save"))
        self.label_28.setText(_translate("MainWindow", "Speed"))
        self.dwellClickCheckBox.setText(_translate("MainWindow", "Dwell Click"))
        self.smileCenterCheckBox.setText(_translate("MainWindow", "Smile Center"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
