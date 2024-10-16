from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtCore import pyqtSignal, QObject
import sys
from nodes_init import Ui_MainWindow


class NodesWindow(QMainWindow, Ui_MainWindow):
    value_submitted = pyqtSignal(str)
    def __init__(self):
        super(NodesWindow, self).__init__()
        self.setupUi(self)
        self.setStyleSheet("background-color: lightblue;")
        self.pushButton.clicked.connect(self.on_button_clicked)
    def on_button_clicked(self):

        # 判断哪个复选框被选中，并执行相应的操作
        if self.checkBox.isChecked():
            value="栅格模式"
            print(1)
        elif self.checkBox_2.isChecked():
            value="随机模式"
        self.value_submitted.emit(value)
        self.close()

