from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1625, 895)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")

        self.graphicsView = QtWidgets.QGraphicsView(Dialog)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)

        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setMaximumSize(QtCore.QSize(1267, 16777215))
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)

        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setMinimumSize(QtCore.QSize(1603, 0))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)

        self.comboBox_2 = QtWidgets.QComboBox(Dialog)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.verticalLayout.addWidget(self.comboBox_2)

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)

        self.comboBox_3 = QtWidgets.QComboBox(Dialog)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.verticalLayout.addWidget(self.comboBox_3)

        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        # 设置按钮文字居中，并调整边框和大小
        self.pushButton_2.setStyleSheet("text-align: center; padding: 5px; border: 1px solid black;")
        self.verticalLayout.addWidget(self.pushButton_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.comboBox.setItemText(0, _translate("Dialog", "普通消息"))
        self.comboBox.setItemText(1, _translate("Dialog", "重要消息"))
        self.comboBox.setItemText(2, _translate("Dialog", "关键消息"))
        self.label.setText(_translate("Dialog", "消息类型"))
        self.comboBox_2.setItemText(0, _translate("Dialog", "分级指控"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "集中指控"))
        self.comboBox_2.setItemText(2, _translate("Dialog", "mesh指控（贪婪路由）"))
        self.comboBox_2.setItemText(3, _translate("Dialog", "mesh指控（冗余路由）"))
        self.comboBox_2.setItemText(4, _translate("Dialog", "mesh指控（节点移动）"))
        self.comboBox_2.setItemText(5, _translate("Dialog", "全部"))
        self.label_2.setText(_translate("Dialog", "指控模式"))
        self.comboBox_3.setItemText(0, _translate("Dialog", "成功率"))
        self.comboBox_3.setItemText(1, _translate("Dialog", "通信"))
        self.pushButton_2.setText(_translate("Dialog", "开始"))
