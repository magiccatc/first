import copy
import heapq
import sys
import warnings
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QGraphicsScene
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import networkx as nx
from sklearn.cluster import KMeans

from dialog import Ui_Dialog  # 确保这是由 Qt Designer 生成的 UI 类

warnings.filterwarnings("ignore", category=DeprecationWarning)
from control_windows import ControlWindow
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


class Dialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)

        self.fig = Figure(figsize=(10, 10), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.scene = QGraphicsScene()
        self.scene.addWidget(self.canvas)
        self.graphicsView.setScene(self.scene)

        self.ax = self.fig.add_subplot(111)

        self.data_x = np.array([])
        self.data_y = np.array([])

        self.kmeans = None
        self.animation = None
        self.farthest_indices = []
        self.graph = None
        self.shortest_paths = []  # 存储最短路径
        self.max_distance = 35  # 最大距离假设为10

        self.pushButton_2.clicked.connect(self.start_process)


    def start_process(self):
        self.contol_window = ControlWindow()
        self.contol_window.show()








if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec_())