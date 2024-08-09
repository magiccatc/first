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

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

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
        self.comboBox_2.currentIndexChanged.connect(self.update_animation_function)

    def start_process(self):
        try:
            num_points = int(self.lineEdit.text())
            self.update_animation_function()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "输入错误", "请输入一个有效的整数")
            return

        if num_points < 1 or num_points > 100:
            QtWidgets.QMessageBox.warning(self, "输入错误", "点的数量必须在 1 到 100 之间")
            return

        self.data_x = (np.random.rand(num_points) * 101).astype(int)
        self.data_y = (np.random.rand(num_points) * 101).astype(int)

        self.ax.clear()
        self.ax.scatter(self.data_x, self.data_y, color='blue', label='随机点')
        self.ax.scatter(0, 0, color='red', label='原点')
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.legend()
        self.canvas.draw()

        self.kmeans = None
        self.graph = None  # 重置图形
        self.shortest_paths = []  # 重置最短路径
        self.start_animation()

    def update_animation_function(self):
        control_type = self.comboBox_2.currentText()
        print(f"当前选中的控制类型: {control_type}")  # 打印下拉框选项
        if control_type == "分级指控":
            self.update_function = self.hierarchical_control
        elif control_type == "集中指控":
            self.update_function = self.concentrated_control
        elif control_type == "mesh指控（贪婪路由）":
            self.update_function = self.shortest_path_two_control
        elif control_type == "mesh指控（冗余路由）":
            self.update_function = self.shortest_path_two_control()
        else:
            self.update_function = None

    def hierarchical_control(self, frame):
        if self.kmeans is None:
            self.kmeans = KMeans(n_clusters=3)
            self.kmeans.fit(np.vstack((self.data_x, self.data_y)).T)
            self.cluster_centers = self.kmeans.cluster_centers_

            # 找到每个计算的簇中心最近的实际数据点
            self.closest_data_points = []
            for center in self.cluster_centers:
                distances = np.sqrt((self.data_x - center[0]) ** 2 + (self.data_y - center[1]) ** 2)
                closest_point_index = np.argmin(distances)
                self.closest_data_points.append((self.data_x[closest_point_index], self.data_y[closest_point_index]))

            # 计算距离并选择最远的五个点
            distances = np.sqrt((self.data_x - 0) ** 2 + (self.data_y - 0) ** 2)
            self.farthest_indices = np.argsort(-distances)[:5]  # 取前五个最远的点

            # 为每个最远点找到最近的簇中心
            self.closest_cluster_centers = []
            for index in self.farthest_indices:
                point = np.array([self.data_x[index], self.data_y[index]])
                distances_to_centers = np.sqrt(np.sum((np.array(self.closest_data_points) - point) ** 2, axis=1))
                closest_center_index = np.argmin(distances_to_centers)
                self.closest_cluster_centers.append((index, self.closest_data_points[closest_center_index]))

        # 每次绘制之前清除所有之前的连线
        self.ax.clear()
        self.ax.scatter(self.data_x, self.data_y, color='blue', label='随机点')
        self.ax.scatter(0, 0, color='red', label='原点')
        self.ax.scatter(np.array(self.closest_data_points)[:, 0], np.array(self.closest_data_points)[:, 1], c='yellow',
                        label='实际簇中心')

        num_farthest_points = len(self.farthest_indices)

        # 确定当前绘制的点
        point_index = frame // 2
        if point_index < num_farthest_points:
            farthest_index, closest_center = self.closest_cluster_centers[point_index]
            farthest_point = (self.data_x[farthest_index], self.data_y[farthest_index])

            if frame % 2 == 0:
                # 偶数帧：绘制从原点到簇中心的连线和从簇中心到最远点的连线
                self.ax.plot([0, closest_center[0]], [0, closest_center[1]], 'g--', linewidth=2)  # 从原点到簇中心的虚线
                self.ax.plot([closest_center[0], farthest_point[0]], [closest_center[1], farthest_point[1]], 'b-',
                             linewidth=2)  # 从簇中心到最远点的连线
            else:
                # 奇数帧：绘制从簇中心到最远点的连线
                self.ax.plot([closest_center[0], farthest_point[0]], [closest_center[1], farthest_point[1]], 'b-',
                             linewidth=2)  # 从簇中心到最远点的连线

        self.ax.legend()
        self.ax.set_title(f"分级指控动画 - 帧 {frame + 1}")
        self.canvas.draw()

    def concentrated_control(self, frame):
        self.ax.clear()

        # 绘制点和原点
        self.ax.scatter(self.data_x, self.data_y, color='blue', label='随机点')
        self.ax.scatter(0, 0, color='red', label='原点')

        if frame == 0:
            # 计算距离并选择最远的五个点
            distances = np.sqrt((self.data_x - 0) ** 2 + (self.data_y - 0) ** 2)
            self.farthest_indices = np.argsort(-distances)[:5]  # 取前五个最远的点

        # 逐个连接
        if frame < len(self.farthest_indices):
            index = self.farthest_indices[frame]
            farthest_point = (self.data_x[index], self.data_y[index])
            self.ax.plot([0, farthest_point[0]], [0, farthest_point[1]], 'g-', linewidth=2)  # 连线

        self.ax.set_title(f"集中指控动画 - 帧 {frame + 1}")
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.legend()
        self.canvas.draw()

        # 打印连接线的坐标
        if frame < len(self.farthest_indices):
            index = self.farthest_indices[frame]
            farthest_point = (self.data_x[index], self.data_y[index])
            print(f"帧 {frame + 1}: 连接线坐标: ({0}, {0}) to ({farthest_point[0]}, {farthest_point[1]})")

    def shortest_path_control(self, frame):
        # 检查 self.graph 是否已初始化，如果没有，则创建图并计算最短路径
        if self.graph is None:
            # 创建图并添加节点
            self.graph = nx.Graph()

            # 将原点和散点数据合并为二维数组
            origin = np.array([[0, 0]])
            points = np.vstack((origin, np.column_stack((self.data_x, self.data_y))))

            # 添加节点
            for i, (x, y) in enumerate(points):
                self.graph.add_node(i, pos=(x, y))
            print(self.graph.nodes)
            # 添加边，边的权重是点之间的距离，且距离不超过 self.max_distance
            for i in range(len(points)):
                for j in range(i + 1, len(points)):
                    distance = np.linalg.norm(points[i] - points[j])
                    if distance <= self.max_distance:
                        self.graph.add_edge(i, j, weight=distance)
                print(self.graph.edges)
            # 计算最远点的索引
            distances = np.linalg.norm(points[1:] - origin, axis=1)
            # 获取距离最远的5个点的索引
            self.farthest_indices = np.argsort(distances)[-5:][::-1]
            # 计算从原点到每个最远点的最短路径
            self.shortest_paths = []
            print(self.farthest_indices)
            for idx in self.farthest_indices:
                try:
                    path = nx.shortest_path(self.graph, source=0, target=idx + 1, weight='weight')
                    self.shortest_paths.append(path)
                except nx.NetworkXNoPath:
                    print(f"没有从原点到节点 {idx + 1} 的路径")

            # 清除之前的图形
        self.ax.clear()
        self.ax.scatter(self.data_x, self.data_y, color='blue', label='随机点')
        self.ax.scatter(0, 0, color='red', label='原点')

        # 绘制最短路径
        if frame < len(self.shortest_paths):
            path = self.shortest_paths[frame]
            for i in range(len(path) - 1):
                x_coords = [self.graph.nodes[path[i]]['pos'][0], self.graph.nodes[path[i + 1]]['pos'][0]]
                y_coords = [self.graph.nodes[path[i]]['pos'][1], self.graph.nodes[path[i + 1]]['pos'][1]]
                self.ax.plot(x_coords, y_coords, 'g-', linewidth=2)
                print(f"帧 {frame + 1}: 路径 {path[i]} 到 {path[i + 1]} 的坐标: {x_coords}, {y_coords}")

        self.ax.set_title(f"最短路径指控动画 - 帧 {frame + 1}")
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.legend()
        self.canvas.draw()

    def shortest_path_two_control(self, frame):
        if self.graph is None:
            self.graph = nx.Graph()
            origin = np.array([[0, 0]])
            points = np.vstack((origin, np.column_stack((self.data_x, self.data_y))))
            for i, (x, y) in enumerate(points):
                self.graph.add_node(i, pos=(x, y))

            for i in range(len(points)):
                for j in range(i + 1, len(points)):
                    distance = np.linalg.norm(points[i] - points[j])
                    if distance <= self.max_distance:
                        self.graph.add_edge(i, j, weight=distance)

            distances = np.linalg.norm(points[1:] - origin, axis=1)
            self.farthest_indices = np.argsort(distances)[-5:][::-1]

            self.shortest_paths = []
            self.alternate_paths = []

            for idx in self.farthest_indices:
                try:
                    shortest_path = nx.shortest_path(self.graph, source=0, target=idx + 1, weight='weight')
                    self.shortest_paths.append(shortest_path)

                    # 查找所有从原点到目标点的路径
                    all_paths = list(nx.all_simple_paths(self.graph, source=0, target=idx + 1))

                    # 计算最短路径的节点集合
                    shortest_path_set = set(shortest_path[1:-1])

                    # 从所有路径中选择与最短路径尽可能不重合且总长度最短的路径
                    min_length = float('inf')
                    best_alternate_path = None

                    for path in all_paths:
                        if not any(node in path for node in shortest_path_set):
                            path_length = sum(self.graph[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))
                            if path_length < min_length:
                                min_length = path_length
                                best_alternate_path = path

                    if best_alternate_path:
                        self.alternate_paths.append(best_alternate_path)
                    else:
                        self.alternate_paths.append([])

                except nx.NetworkXNoPath:
                    print(f"没有从原点到节点 {idx + 1} 的路径")

        self.ax.clear()
        self.ax.scatter(self.data_x, self.data_y, color='blue', label='随机点')
        self.ax.scatter(0, 0, color='red', label='原点')

        if frame < len(self.shortest_paths):
            shortest_path = self.shortest_paths[frame]
            alternate_path = self.alternate_paths[frame]

            # 绘制最短路径
            for i in range(len(shortest_path) - 1):
                x_coords = [self.graph.nodes[shortest_path[i]]['pos'][0],
                            self.graph.nodes[shortest_path[i + 1]]['pos'][0]]
                y_coords = [self.graph.nodes[shortest_path[i]]['pos'][1],
                            self.graph.nodes[shortest_path[i + 1]]['pos'][1]]
                self.ax.plot(x_coords, y_coords, 'g-', linewidth=2, label='最短路径' if i == 0 else "")

            # 绘制替代路径
            if alternate_path:
                for i in range(len(alternate_path) - 1):
                    x_coords = [self.graph.nodes[alternate_path[i]]['pos'][0],
                                self.graph.nodes[alternate_path[i + 1]]['pos'][0]]
                    y_coords = [self.graph.nodes[alternate_path[i]]['pos'][1],
                                self.graph.nodes[alternate_path[i + 1]]['pos'][1]]
                    self.ax.plot(x_coords, y_coords, 'b--', linewidth=2, label='替代路径' if i == 0 else "")

        self.ax.set_title(f"最短路径与替代路径指控动画 - 帧 {frame + 1}")
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.legend()
        self.canvas.draw()

    def update_animation(self, frame):
        if self.update_function:
            self.update_function(frame)

    def start_animation(self):
        if self.animation is not None:
            self.animation.event_source.stop()
        self.animation = FuncAnimation(self.fig, self.update_animation,
                                       frames=range(6),  # 根据具体的动画帧数调整
                                       interval=1000,  # 动画的时间间隔（毫秒）
                                       init_func=self.init_animation,
                                       blit=False)
        self.canvas.draw()

    def init_animation(self):
        self.ax.clear()
        self.ax.scatter(self.data_x, self.data_y, color='blue', label='随机点')
        self.ax.scatter(0, 0, color='red', label='原点')
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        self.ax.legend()
        self.canvas.draw()
        return []

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = Dialog()
    dialog.show()
    sys.exit(app.exec_())