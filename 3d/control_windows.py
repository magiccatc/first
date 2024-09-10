from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtCore import pyqtSignal, QObject
import sys
from control import Ui_MainWindow


class ControlWindow(QMainWindow, Ui_MainWindow):
    value_submitted = pyqtSignal(str)
    def __init__(self):
        super(ControlWindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_button_clicked)

    def on_button_clicked(self):

        # 判断哪个复选框被选中，并执行相应的操作
        if self.checkBox.isChecked():
            value="contralized"
            print(1)
        elif self.checkBox_2.isChecked():
            value="sort"
        elif self.checkBox_3.isChecked():
            value="mesh1"
        elif self.checkBox_4.isChecked():
            value="mesh2"
        self.value_submitted.emit(value)
        self.close()
