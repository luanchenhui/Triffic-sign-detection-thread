# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QFileDialog

from qt_predict import Predicter


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1050, 600)
        MainWindow.setStyleSheet("#MainWindow{border-image:url(./image/bk.jpg);}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.close_btn = QtWidgets.QPushButton(self.centralwidget)
        self.close_btn.setGeometry(QtCore.QRect(950, 525, 100, 50))
        self.close_btn.setObjectName("close_btn")
        self.select_image_btn = QtWidgets.QPushButton(self.centralwidget)
        self.select_image_btn.setGeometry(QtCore.QRect(130, 525, 100, 50))
        self.select_image_btn.setObjectName("select_image_btn")
        self.normal_image = QtWidgets.QLabel(self.centralwidget)
        self.normal_image.setGeometry(QtCore.QRect(50, 50, 460, 400))
        self.normal_image.setAlignment(QtCore.Qt.AlignCenter)
        self.normal_image.setIndent(-1)
        self.normal_image.setObjectName("normal_image")
        self.min_image = QtWidgets.QLabel(self.centralwidget)
        self.min_image.setGeometry(QtCore.QRect(600, 50, 360, 300))
        self.min_image.setAlignment(QtCore.Qt.AlignCenter)
        self.min_image.setObjectName("min_image")
        self.show_predict = QtWidgets.QLabel(self.centralwidget)
        self.show_predict.setGeometry(QtCore.QRect(690, 350, 200, 200))
        self.show_predict.setObjectName("show_predict")
        self.show_predict.setAlignment(QtCore.Qt.AlignLeft)
        self.start_predict = QtWidgets.QPushButton(self.centralwidget)
        self.start_predict.setGeometry(QtCore.QRect(300, 525, 100, 50))
        self.start_predict.setObjectName("start_predict")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1047, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # 创建新线程，将自定义信号sinOut连接到slotAdd()槽函数
        self.thread = Predicter()
        self.thread.sinOut.connect(self.slot_flash_ui)

        self.retranslateUi(MainWindow)
        self.close_btn.clicked.connect(MainWindow.close)
        self.select_image_btn.clicked.connect(self.open_image)

        # 链接点击事件和slot处理函数
        self.start_predict.clicked.connect(self.slot_start)

        # 使得开始预测按钮默认不可用
        self.start_predict.setEnabled(False)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # 开始按钮按下后使其不可用，启动线程
    def slot_start(self):
        self.start_predict.setEnabled(False)
        print('start detection')
        self.thread.start()

    # 刷新UI
    def slot_flash_ui(self, message_of_predict):
        split_message = message_of_predict.split(":")
        flag = split_message[0]
        real_data = split_message[1]
        if flag == 'R':
            font = QtGui.QFont()
            font.setPointSize(16)
            self.show_predict.setFont(font)
            self.show_predict.setText(real_data)
        if flag == 'P':
            font = QtGui.QFont()
            font.setPointSize(24)
            self.show_predict.setFont(font)
            self.show_predict.setText(real_data)
        if flag == 'I':
            image = QtGui.QPixmap(real_data).scaled(self.min_image.width(), self.min_image.height())
            self.min_image.setPixmap(image)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.close_btn.setText(_translate("MainWindow", "退出"))
        self.select_image_btn.setText(_translate("MainWindow", "选择图片"))
        self.normal_image.setText(_translate("MainWindow", "请选择图片"))
        self.min_image.setText(_translate("MainWindow", "此处为缩略图"))
        self.show_predict.setText(_translate("MainWindow", "尚未开始测试"))
        self.start_predict.setText(_translate("MainWindow", "开始预测"))

        self.normal_image.setAutoFillBackground(True)
        self.min_image.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Window, Qt.gray)
        self.normal_image.setPalette(palette)
        self.min_image.setPalette(palette)

    def open_image(self):
        image_name, _ = QFileDialog.getOpenFileName(self.centralwidget)
        print(image_name)
        image = QtGui.QPixmap(image_name).scaled(self.normal_image.width(), self.normal_image.height())
        self.normal_image.setPixmap(image)
        image = QtGui.QPixmap(image_name).scaled(self.min_image.width(), self.min_image.height())
        self.min_image.setPixmap(image)
        print('Using thread')
        self.thread.image_path = image_name
        self.start_predict.setEnabled(True)
