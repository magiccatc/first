from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
import sys
from main_windows import Ui_MainWindow
from control_windows import ControlWindow
from PyQt5.QtCore import pyqtSignal
# 导入主窗口UI类
# 导入设置窗口UI类


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.textEdit.setReadOnly(True)

        # 点击按钮时打开设置窗口
        self.pushButton.clicked.connect(self.open_control_settings)
        self.pushButton_2.clicked.connect(self.open_channel_setting)
        self.pushButton_3.clicked.connect(self.open_data_setting)
        self.pushButton_4.clicked.connect(self.commnicate_simulate)
        self.pushButton_4.clicked.connect(self.start)

    def start(self):
        pass
    def open_control_settings(self):
        self.contol_window = ControlWindow()
        self.contol_window.show()
        self.contol_window.value_submitted.connect(self.display_value)


    def display_value(self, value):
        # 槽函数，接收来自子窗口的信号并更新主窗口的标签
        self.value=value
        print(value)
        self.textEdit.append("指控模式已设置"+self.value)
    def open_channel_setting(self):
        pass
    def open_data_setting(self):
        pass
    def commnicate_simulate(self):
        pass

    # 以对话框的形式显示设置窗口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()

    main_win.show()
    sys.exit(app.exec_())
