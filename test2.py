import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.animation import FuncAnimation
import networkx as nx
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget


class AnimationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设定窗口标题和大小
        self.setWindowTitle('Shortest Path Animation')
        self.setGeometry(100, 100, 800, 600)

        # 创建主窗口的中央部件和布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # 创建 Matplotlib 图形和画布
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        # 生成数据和图形
        self.setup_plot()

        # 创建动画
        self.anim = FuncAnimation(self.fig, self.update_frame, frames=len(self.max_path), repeat=False, interval=1000)

    def setup_plot(self):
        np.random.seed(0)
        num_points = 40
        points = np.random.rand(num_points, 2) * 10
        origin = np.array([[0, 0]])
        all_points = np.vstack([origin, points])

        # 创建图
        self.G = nx.Graph()
        distance_limit = 4

        # 添加节点
        for i in range(len(all_points)):
            self.G.add_node(i, pos=all_points[i])

        # 添加边
        for i in range(len(all_points)):
            for j in range(i + 1, len(all_points)):
                distance = np.linalg.norm(all_points[i] - all_points[j])
                if distance <= distance_limit:
                    self.G.add_edge(i, j, weight=distance)

        # 计算最短路径
        lengths = {}
        paths = {}
        for i in range(1, len(all_points)):
            try:
                path = nx.shortest_path(self.G, source=0, target=i, weight='weight')
                lengths[i] = len(path)
                paths[i] = path
            except nx.NetworkXNoPath:
                lengths[i] = float('inf')
                paths[i] = []

        # 找到距离原点最远的点
        farthest_point = max(lengths.items(), key=lambda x: x[1])[0]
        self.max_path = paths[farthest_point]

        # 绘制初始图
        self.ax.clear()
        self.ax.scatter(all_points[:, 0], all_points[:, 1], color='blue')
        self.ax.scatter([origin[0, 0]], [origin[0, 1]], color='red', label='Origin')
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.ax.set_title('Shortest Path Animation')
        self.ax.legend()
        self.ax.grid(True)

    def update_frame(self, frame):
        self.ax.clear()
        self.ax.scatter(self.all_points[:, 0], self.all_points[:, 1], color='blue')
        self.ax.scatter([self.origin[0, 0]], [self.origin[0, 1]], color='red', label='Origin')

        if frame < len(self.max_path) - 1:
            x_coords = [self.all_points[self.max_path[frame]][0], self.all_points[self.max_path[frame + 1]][0]]
            y_coords = [self.all_points[self.max_path[frame]][1], self.all_points[self.max_path[frame + 1]][1]]
            self.ax.plot(x_coords, y_coords, 'k--', lw=2)

        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.ax.set_title(f"Frame {frame + 1}")
        self.ax.legend()
        self.ax.grid(True)
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AnimationWindow()
    window.show()
    sys.exit(app.exec_())
