from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QGraphicsScene
import sys

from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure

from main_windows import Ui_MainWindow
from control_windows import ControlWindow
from  nodes_init_windows import NodesWindow
from PyQt5.QtCore import pyqtSignal
# 导入主窗口UI类
# 导入设置窗口UI类


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        #self.textEdit.setReadOnly(True)
        self.resize(1200, 1500)
        self.setStyleSheet("background-color: lightblue;")
        # 点击按钮时打开设置窗口

        # 点击按钮时打开设置窗口
       # self.fig = Figure(figsize=(10, 10), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.scene = QGraphicsScene()
        self.scene.addWidget(self.canvas)
        self.graphicsView.setScene(self.scene)

        #self.ax = self.fig.add_subplot(111)



        self.pushButton.clicked.connect(self.open_control_settings)
        self.pushButton_2.clicked.connect(self.open_channel_setting)
        self.pushButton_3.clicked.connect(self.open_data_setting)
        self.pushButton_4.clicked.connect(self.commnicate_simulate)
        self.pushButton_4.clicked.connect(self.start)

    def start(self):
        pass

    def display_nodes_value(self, value):
        # 槽函数，接收来自子窗口的信号并更新主窗口的标签
        self.nodes_value=value
        print(value)
        #self.textEdit.append("调度配置已设置"+self.nodes_value)
    def open_channel_setting(self):
        pass
    def open_data_setting(self):
        self.nodes_window = NodesWindow()
        self.nodes_window.show()
        self.nodes_window.value_submitted.connect(self.display_nodes_value)
    def commnicate_simulate(self):
        pass

    def open_control_settings(self):
        self.contol_window = ControlWindow()
        self.contol_window.show()
        self.contol_window.value_submitted.connect(self.display_control_value)

    def display_control_value(self, value):
        # 槽函数，接收来自子窗口的信号并更新主窗口的标签
        self.control_value = value
        print(value)
        #self.textEdit.append("指控模式已设置" + self.control_value)

    # 以对话框的形式显示设置窗口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()

    main_win.show()
    sys.exit(app.exec_())
