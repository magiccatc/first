import sys
import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QGraphicsScene
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
from sklearn.cluster import KMeans

from dialog import Ui_Dialog  # 假设这是由Qt Designer设计的UI类


class Dialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)

        self.fig = Figure(figsize=(10, 10), dpi=100)
        self.canvas = FigureCanvas(self.fig)
        self.scene = QGraphicsScene()
        self.scene.addWidget(self.canvas)
        self.graphicsView.setScene(self.scene)
        self.setStyleSheet("background-color: lightblue;")
        #self.ax = self.fig.add_subplot(111)
        self.data_x = np.array([])
        self.data_y = np.array([])
        self.farthest_lines = []  # 用于存储动画中的线对象

        self.kmeans = None
        self.animation = None

        self.pushButton_2.clicked.connect(self.start_process)

    def start_process(self):
        try:
            num_points = int(self.lineEdit.text())
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "输入错误", "请输入一个有效的整数")
            return

        if num_points < 1 or num_points > 100:
            QtWidgets.QMessageBox.warning(self, "输入错误", "点的数量必须在1到100之间")
            return

        self.data_x = np.random.rand(num_points) * 100
        self.data_y = np.random.rand(num_points) * 100

        self.ax.clear()
        self.ax.scatter(self.data_x, self.data_y, color='blue', label='随机点')
        self.ax.scatter(0, 0, color='red', label='原点')
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.legend()

        self.canvas.draw()

        # 根据下拉框选项设置动画函数
        control_type = self.comboBox.currentText()
        if control_type == "分级指控":
            self.update_function = self.hierarchical_control
        elif control_type == "集中指控":
            self.update_function = self.concentrated_control

        self.start_animation()

    def init_animation(self):
        self.ax.clear()
        self.ax.scatter(self.data_x, self.data_y, color='blue', label='随机点')
        self.ax.scatter(0, 0, color='red', label='原点')
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.legend()
        self.canvas.draw()
        self.farthest_lines.clear()

    def hierarchical_control(self, frame):
        if self.kmeans is None:
            self.kmeans = KMeans(n_clusters=3)
            self.kmeans.fit(np.vstack((self.data_x, self.data_y)).T)
            self.cluster_centers = self.kmeans.cluster_centers_

        self.ax.clear()
        self.ax.scatter(self.data_x, self.data_y, color='blue', label='随机点')
        self.ax.scatter(self.cluster_centers[:, 0], self.cluster_centers[:, 1], c='yellow', label='聚类中心')
        self.ax.set_title(f"分级指控动画 - 帧 {frame + 1}")
        self.canvas.draw()

    def concentrated_control(self, frame):
        # 清除之前的线
        for line in self.farthest_lines:
            line.remove()
        self.farthest_lines.clear()

        # 找到距离原点最远的点
        distances = np.sqrt((self.data_x - 0) ** 2 + (self.data_y - 0) ** 2)
        farthest_index = np.argsort(-distances)[0]  # 获取最远点的索引
        farthest_point = (self.data_x[farthest_index], self.data_y[farthest_index])

        # 绘制原点到最远点的线
        line, = self.ax.plot([0, farthest_point[0]], [0, farthest_point[1]], 'g-')
        self.farthest_lines.append(line)

        self.ax.set_title("集中指控动画 - 连接到最远点")
        self.canvas.draw()

    def update_animation(self, frame):
        print(f"Updating frame {frame}")  # 添加调试输出
        if self.update_function:
            self.update_function(frame)

    def start_animation(self):
        if self.animation is not None:
            self.animation.event_source.stop()
        self.animation = FuncAnimation(self.fig, self.update_animation,
                                       frames=range(10),  # 增加帧数以显示动画效果
                                       interval=500,  # 每帧间隔0.5秒
                                       init_func=self.init_animation,
                                       blit=False)  # 设置blit为False以确保更新


# 主程序
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec_())
