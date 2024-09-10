import copy
import heapq
import math
import sys
import warnings
import numpy as np
from PIL.Image import Image
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QGraphicsScene
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from sklearn.cluster import KMeans

from dialog import Ui_Dialog  # 确保这是由 Qt Designer 生成的 UI 类

warnings.filterwarnings("ignore", category=DeprecationWarning)

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题
def add_image_to_scatter(ax, img_path, x, y, zoom=0.1):
    """在指定的ax上，将图片放置在(x, y)坐标处"""
    image = plt.imread(img_path)
    im = OffsetImage(image, zoom=zoom)
    ab = AnnotationBbox(im, (x, y), frameon=False)
    ax.add_artist(ab)

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
       # 监听模式切换
        pi=np.pi
    def start_process(self):
        try:
            num_points = int(self.lineEdit.text())
            self.num_points = num_points
            if num_points < 1 or num_points > 100:
                raise ValueError("点的数量必须在 1 到 100 之间")
        except ValueError as e:
            QtWidgets.QMessageBox.warning(self, "输入错误", str(e))
            return

        # 根据 comboBox_3 的选择更新显示模式
        # self.data_x = (np.random.rand(num_points) * 101).astype(int)
        # self.data_y = (np.random.rand(num_points) * 101).astype(int)
        sqrt_points = int(np.sqrt(num_points))
        self.cell_size_x = 101 // sqrt_points
        self.cell_size_y = 101 // sqrt_points

        self.data_x = []
        self.data_y = []

        for i in range(sqrt_points):
            for j in range(sqrt_points):
                # 在每个网格单元内随机生成一个点
                x = np.random.randint(i * self.cell_size_x, (i + 1) * self.cell_size_x)
                y = np.random.randint(j * self.cell_size_y, (j + 1) * self.cell_size_y)
                self.data_x.append(x)
                self.data_y.append(y)

        self.data_x = np.array(self.data_x)
        self.data_y = np.array(self.data_y)


        mode = self.comboBox_3.currentText()
        if mode == "通信":
            self.ax.clear()
            #self.ax.scatter(self.data_x, self.data_y, color='black', label='随机点')
           # self.ax.scatter(0, 0, color='red', label='原点')
            add_image_to_scatter(self.ax, "指挥中心.png", 0, 0, zoom=0.5)
            for (x, y) in zip(self.data_x, self.data_y):
                add_image_to_scatter(self.ax, "舰艇.png", x, y, zoom=0.1)
            self.ax.set_xlim(0, 100)
            self.ax.set_ylim(0, 100)
           # self.ax.set_facecolor((0.7, 0.7, 1, 0.5))  # 使用RGBA值设置浅蓝色背景
            self.ax.legend()
            self.canvas.draw()

            self.kmeans = None
            self.graph = None  # 重置图形
            self.shortest_paths = []  # 重置最短路径

            self.update_animation_function()  # 更新动画函数
            self.start_animation()
        elif mode == "成功率":
            self.update_success_rate_function()  # 处理成功率模式



    def update_animation_function(self):


        control_type = self.comboBox_2.currentText()
        print(f"当前选中的控制类型: {control_type}")  # 打印下拉框选项
        if control_type == "分级指控":
            self.update_function = self.hierarchical_control
        elif control_type == "集中指控":
            self.update_function = self.concentrated_control
        elif control_type == "mesh指控（贪婪路由）":
            self.update_function = self.shortest_path_control # Assuming this is your correct function
        elif control_type == "mesh指控（冗余路由）":
            self.update_function = self.shortest_path_two_control # Assuming this is your correct function
        else:
            self.update_function = None

    def update_success_rate_function(self):
        # 在这里添加关于“成功率”模式的处理逻辑
        if self.animation is not None:
            self.animation.event_source.stop()


        # 清除之前的图形
        self.ax.clear()
        self.hierarchical_caculate()
        # 绘制折线图
        data1=np.array(self.allpoints_distances)
        data2=np.array(self.all_hierarchical_distances)
        print("data1",data2)

        #results1 = np.vectorize(self.success_rate_conclusion)(data1)
        results1 = [self.success_rate_conclusion(element) for element in data1]
        print("results1",results1)
        results2 = [[self.success_rate_conclusion(item) for item in sublist] for sublist in data2]
        results1=np.mean(results1)*100
        print("results1",results1)
        results2=np.mean(results2)*100
        self._initialize_graph()
        self._calculate_farthest_indices()
        #print("1",self.distance_array1)

        data3=self.distance_array1
        print("data3",len(data3))
        #print("data3",data3)
        data4=self.distance_array2
        data3=[[self.success_rate_conclusion(item) for item in sublist] for sublist in data3]
        data4=[[self.success_rate_conclusion(item) for item in sublist] for sublist in data4]
        #print("data3",data3)
        results3= [sum(sublist) / len(sublist) for sublist in data3]
        results4= [sum(sublist) / len(sublist) for sublist in data4]
        results4 = [1 - (1 - a) * (1 - b) for a, b in zip(results3, results4)]
        #print("results4",results4)
        results3=sum(results3)/len(results3)*100
        #print("results3",results3)
        results4=sum(results4)/len(results4)*100
        #print("results4",results4)
        self.plot_bar_chart([results1, results2, results3, results4])

    def plot_bar_chart(self, data):
        # X轴标签
        # 清除Figure中的所有轴
        self.ax.clear()
        labels = ['集中指控', '分级指控', 'mesh指控（贪婪转发）', 'mesh指控（冗余路由）']


        colors = ['skyblue', 'lightcoral', 'lightgreen', 'lightsalmon']  # 设置柱形颜色

        bar_width = 0.4  # 设置柱形宽度
        bar_positions = range(len(labels))  # 设置柱形的位置

        for i, (label, value) in enumerate(zip(labels, data)):
            self.ax.bar(i, value, color=colors[i], width=bar_width, edgecolor='black', linewidth=1.5, alpha=0.7)

        self.ax.set_xticks(range(len(labels)))
        self.ax.set_xticklabels(labels)
        self.ax.set_xlim(-0.5, len(labels) - 0.5)  # 设置x轴范围，使得柱形居中
        self.ax.set_ylim(0, 100)
        self.ax.set_title('Success Rate by Group', fontsize=14, fontweight='bold')  # 设置标题样式
        self.ax.set_xlabel('指控模式', fontsize=12)
        self.ax.set_ylabel('消息到达率', fontsize=12)
        self.ax.grid(axis='y', linestyle='--', alpha=0.5)

        self.canvas.draw()






    def success_rate_conclusion(self,length): #关于功率的计算

        if 0<=length<=36:
            return 1-length*np.sqrt(length)/(np.pi*36*6)
        else:
            return 0

    def hierarchical_control(self, frame):
        # 在这里添加关于“分级指控”模式的处理逻辑
        self.hierarchical_caculate()
        # 每次绘制之前清除所有之前的连线
        #data1=np.array(self.f)
        self.ax.clear()
        #self.ax.scatter(self.data_x, self.data_y, color='blue', label='随机点')
        #self.ax.scatter(0, 0, color='red', label='原点')
        #add_image_to_scatter(self.ax, "指挥中心.svg", 0, 0, zoom=0.1)
        add_image_to_scatter(self.ax, "指挥中心.png", 0, 0, zoom=0.5)
        for (x, y) in zip(self.data_x, self.data_y):
            add_image_to_scatter(self.ax, "舰艇.png", x, y, zoom=0.1)
        #self.ax.scatter(np.array(self.closest_data_points)[:, 0], np.array(self.closest_data_points)[:, 1], c='yellow',
                        #label='实际簇中心')
        # 绘制网格线
        for i in range(1, int(np.sqrt(self.num_points))):
            self.ax.vlines(i * self.cell_size_x, 0, 100, colors='black', linestyles='dotted')
            self.ax.hlines(i * self.cell_size_y, 0, 100, colors='black', linestyles='dotted')
        num_farthest_points = len(self.farthest_indices)

        # 确定当前绘制的点
        point_index = frame // 2
        if point_index < num_farthest_points:
            farthest_index, closest_center = self.closest_cluster_centers[point_index]
            farthest_point = (self.data_x[farthest_index], self.data_y[farthest_index])

            if frame % 2 == 0:
                # 偶数帧：绘制从原点到簇中心的连线和从簇中心到最远点的连线
                self.ax.plot([0, closest_center[0]], [0, closest_center[1]], 'g--', linewidth=2)  # 从原点到簇中心的虚线
            else:
                # 奇数帧：绘制从簇中心到最远点的连线
                self.ax.plot([0, closest_center[0]], [0, closest_center[1]], 'g--', linewidth=2)  # 从原点到簇中心的虚线
                self.ax.plot([closest_center[0], farthest_point[0]], [closest_center[1], farthest_point[1]], 'b-',
                             linewidth=2)  # 从簇中心到最远点的连线

        self.ax.legend()
        #self.ax.set_title(f"分级指控动画 - 帧 {frame + 1}")
        self.canvas.draw()

    def hierarchical_caculate(self):
        if self.kmeans is None:
            self.kmeans = KMeans(n_clusters=4)
            self.kmeans.fit(np.vstack((self.data_x, self.data_y)).T)
            self.cluster_centers = self.kmeans.cluster_centers_

            self.closest_data_points = []
            for center in self.cluster_centers:
                distances = np.sqrt((self.data_x - center[0]) ** 2 + (self.data_y - center[1]) ** 2)
                closest_point_index = np.argmin(distances)
                self.closest_data_points.append((self.data_x[closest_point_index], self.data_y[closest_point_index]))
            #print(self.closest_data_points)
            # 计算距离并选择最远的五个点
            distances = np.sqrt((self.data_x - 0) ** 2 + (self.data_y - 0) ** 2)
            self.allpoints = np.argsort(-distances)
            self.allpoints_distances=distances[self.allpoints]
            self.farthest_indices = np.argsort(-distances)[:5]  # 取前五个最远的点
            self.farthest_distances = distances[self.farthest_indices]
            #print("最远点的索引:", self.farthest_indices)

            # 为每个最远点找到最近的簇中心
            self.closest_cluster_centers = []
            self.allpoints_centers = []
            for index in self.farthest_indices:
                point = np.array([self.data_x[index], self.data_y[index]])
                distances_to_centers = np.sqrt(np.sum((np.array(self.closest_data_points) - point) ** 2, axis=1))
                closest_center_index = np.argmin(distances_to_centers)
                self.closest_cluster_centers.append((index, self.closest_data_points[closest_center_index]))
            for index in self.allpoints:
                point = np.array([self.data_x[index], self.data_y[index]])
                distances_to_centers = np.sqrt(np.sum((np.array(self.closest_data_points) - point) ** 2, axis=1))
                closest_center_index = np.argmin(distances_to_centers)
                self.allpoints_centers.append((index, self.closest_data_points[closest_center_index]))

                # 计算并存储距离
            self.hierarchical_distances = []
            self.all_hierarchical_distances = []
            for index, (x, y) in self.closest_cluster_centers:
                    point = np.array([self.data_x[index], self.data_y[index]])
                    distance_from_origin_to_center =np.sqrt(x**2+y**2)
                    distance_from_center_to_point = np.sqrt(
                        (point[0] - x) ** 2 + (point[1] - y) ** 2)
                # 存储距离
                    self.hierarchical_distances.append([distance_from_origin_to_center, distance_from_center_to_point])
            for index, (x, y) in self.allpoints_centers:
                    point = np.array([self.data_x[index], self.data_y[index]])
                    distance_from_origin_to_center =np.sqrt(x**2+y**2)
                    distance_from_center_to_point = np.sqrt(
                        (point[0] - x) ** 2 + (point[1] - y) ** 2)
                # 存储距离
                    self.all_hierarchical_distances.append([distance_from_origin_to_center, distance_from_center_to_point])


            print(self.closest_cluster_centers)
            print(self.hierarchical_distances)
    def concentrated_control(self, frame):
        self.ax.clear()

        # 绘制点和原点
        #self.ax.scatter(self.data_x, self.data_y, color='blue', label='随机点')

        #self.ax.scatter(0, 0, color='red', label='原点')
        add_image_to_scatter(self.ax, "指挥中心.png", 0, 0, zoom=0.5)
        for (x, y) in zip(self.data_x, self.data_y):
            add_image_to_scatter(self.ax, "舰艇.png", x, y, zoom=0.1)
        if frame == 0:
            # 计算距离并选择最远的五个点
            distances = np.sqrt((self.data_x - 0) ** 2 + (self.data_y - 0) ** 2)
            self.farthest_indices = np.argsort(-distances)[:5]  # 取前五个最远的点

        # 逐个连接
        if frame < len(self.farthest_indices):
            index = self.farthest_indices[frame]
            farthest_point = (self.data_x[index], self.data_y[index])
            self.ax.plot([0, farthest_point[0]], [0, farthest_point[1]], 'g-', linewidth=2)  # 连线

        #self.ax.set_title(f"集中指控动画 - 帧 {frame + 1}")
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        # 绘制网格线
        for i in range(1, int(np.sqrt(self.num_points))):
            self.ax.vlines(i * self.cell_size_x, 0, 100, colors='black', linestyles='dotted')
            self.ax.hlines(i * self.cell_size_y, 0, 100, colors='black', linestyles='dotted')
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
        #self.ax.scatter(self.data_x, self.data_y, color='blue', label='随机点')
        #self.ax.scatter(0, 0, color='red', label='原点')
        add_image_to_scatter(self.ax, "指挥中心.png", 0, 0, zoom=0.5)
        for (x, y) in zip(self.data_x, self.data_y):
            add_image_to_scatter(self.ax, "舰艇.png", x, y, zoom=0.1)

        # 绘制最短路径
        if frame < len(self.shortest_paths):
            path = self.shortest_paths[frame]
            for i in range(len(path) - 1):
                x_coords = [self.graph.nodes[path[i]]['pos'][0], self.graph.nodes[path[i + 1]]['pos'][0]]
                y_coords = [self.graph.nodes[path[i]]['pos'][1], self.graph.nodes[path[i + 1]]['pos'][1]]
                self.ax.plot(x_coords, y_coords, 'g-', linewidth=2)
                print(f"帧 {frame + 1}: 路径 {path[i]} 到 {path[i + 1]} 的坐标: {x_coords}, {y_coords}")

        #self.ax.set_title(f"mesh指控 - 帧 {frame + 1}")
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        # 绘制网格线
        for i in range(1, int(np.sqrt(self.num_points))):
            self.ax.vlines(i * self.cell_size_x, 0, 100, colors='black', linestyles='dotted')
            self.ax.hlines(i * self.cell_size_y, 0, 100, colors='black', linestyles='dotted')
        self.ax.legend()
        self.canvas.draw()

    def shortest_path_two_control(self, frame):
        if self.graph is None:
            self._initialize_graph()
            self._calculate_farthest_indices()

        self.ax.clear()
        self._plot_points()

        if frame < len(self.shortest_paths):
            self._plot_paths(frame)

        self.ax.set_title(f"最短路径与替代路径指控动画 - 帧 {frame + 1}")
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 100)
        # 绘制网格线
        # 绘制网格线
        for i in range(1, int(np.sqrt(self.num_points))):
            self.ax.vlines(i * self.cell_size_x, 0, 100, colors='black', linestyles='dotted')
            self.ax.hlines(i * self.cell_size_y, 0, 100, colors='black', linestyles='dotted')
        self.ax.legend()
        self.canvas.draw()

    def _initialize_graph(self):
        self.graph = nx.Graph()
        origin = np.array([[0, 0]])
        points = np.vstack((origin, np.column_stack((self.data_x, self.data_y))))

        for i, (x, y) in enumerate(points):
            self.graph.add_node(i, pos=(x, y))

        edges = [(i, j, np.linalg.norm(points[i] - points[j]))
                 for i in range(len(points)) for j in range(i + 1, len(points))
                 if np.linalg.norm(points[i] - points[j]) <= self.max_distance]

        self.graph.add_weighted_edges_from(edges)

    def _calculate_farthest_indices(self):
        origin = np.array([[0, 0]])
        points = np.vstack((origin, np.column_stack((self.data_x, self.data_y))))

        distances = np.linalg.norm(points[1:] - origin, axis=1)
        self.farthest_indices = np.argsort(distances)[-5:][::-1]
        self.farthest_indices1 = np.argsort(distances)
        self.sorted_indices = np.argsort(distances)
        self.shortest_paths = []
        self.alternate_paths = []
        self.shortest_paths1 = []
        self.alternate_paths1 = []
        print("shortest_paths:", self.shortest_paths)
        print("alternate_paths:", self.alternate_paths)
        for idx in self.farthest_indices:
            self._find_paths(idx)
        for idx in self.farthest_indices1:
            self._find_paths(idx)

        for path in self.shortest_paths1:
            path_distances = []
            #print("path")
            distances_array1 = []
            self.distance_array1=distances_array1
            # 遍历每个路径
            for path in self.shortest_paths:
                # 初始化路径上的节点对
                path_distances = []
                # 遍历路径中的每对相邻节点
                for i in range(len(path) - 1):
                    node1, node2 = path[i], path[i + 1]
                    # 计算欧几里得距离
                    distance = np.linalg.norm(points[node2] - points[node1])
                    # 将距离和节点对存储在路径距离列表中
                    path_distances.append(distance)
                # 将路径上的所有节点对距离存储在二维数组中
                distances_array1.append(path_distances)

            distances_array2 = []
            self.distance_array2 = distances_array2
            # 遍历每个路径
            for path in self.alternate_paths1:
                # 初始化路径上的节点对
                #print("path")
                path_distances = []
                # 遍历路径中的每对相邻节点
                for i in range(len(path) - 1):
                    node1, node2 = path[i], path[i + 1]
                    # 计算欧几里得距离
                    distance = np.linalg.norm(points[node2] - points[node1])
                    # 将距离和节点对存储在路径距离列表中
                    path_distances.append(distance)
                # 将路径上的所有节点对距离存储在二维数组中
                distances_array2.append(path_distances)

    def _find_paths(self, idx):
        try:
            shortest_path = nx.shortest_path(self.graph, source=0, target=idx + 1, weight='weight')
            self.shortest_paths.append(shortest_path)
            shortest_path1 = nx.shortest_path(self.graph, source=0, target=idx + 1, weight='weight')
            self.shortest_paths1.append(shortest_path1)

            print(f"节点 {idx + 1} 的最短路径为: {shortest_path1}")
            alternate_paths = self._find_alternate_paths(0, idx + 1, shortest_path)
            self.alternate_paths.append(alternate_paths)
            alternate_paths1 = self._find_alternate_paths(0, idx + 1, shortest_path1)
            self.alternate_paths1.append(alternate_paths1)
            print(f"节点 {idx + 1} 的替代路径为: {alternate_paths}")
        except nx.NetworkXNoPath:
            print(f"没有从原点到节点 {idx + 1} 的路径")

    def _find_alternate_paths(self, source, target, shortest_path):
        def path_weight(path):
            return sum(self.graph[u][v]['weight'] for u, v in zip(path[:-1], path[1:]))

        alternate_paths = []

        # 创建图的副本以进行修改
       # print("base graph number",self.graph)
        graph_copy = copy.deepcopy(self.graph)
       # print("copy graph number",graph_copy)
        # 遍历最短路径中的每一条边，逐步移除它们
        for i in range(len(shortest_path) - 1):
            u, v = shortest_path[i], shortest_path[i + 1]

            # 从副本中移除当前边
            graph_copy.remove_edge(u, v)
           # print(" new graph copy number",graph_copy)
            # 尝试找到新的最短路径

            new_path = nx.shortest_path(graph_copy, source=source, target=target, weight='weight')


              

            # 将边重新添加回图的副本
        graph_copy.add_edge(u, v, weight=self.graph[u][v]['weight'])

        return new_path

    def _plot_points(self):
        self.ax.scatter(self.data_x, self.data_y, color='blue', label='随机点')
        self.ax.scatter(0, 0, color='red', label='原点')


    def _plot_paths(self, frame):
        shortest_path = self.shortest_paths[frame]
        alternate_path = self.alternate_paths[frame]

        for i in range(len(shortest_path) - 1):
            x_coords = [self.graph.nodes[shortest_path[i]]['pos'][0],
                        self.graph.nodes[shortest_path[i + 1]]['pos'][0]]
            y_coords = [self.graph.nodes[shortest_path[i]]['pos'][1],
                        self.graph.nodes[shortest_path[i + 1]]['pos'][1]]
            self.ax.plot(x_coords, y_coords, 'g-', linewidth=2, label='最短路径' if i == 0 else "")

        if alternate_path:
            for i in range(len(alternate_path) - 1):
                x_coords = [self.graph.nodes[alternate_path[i]]['pos'][0],
                            self.graph.nodes[alternate_path[i + 1]]['pos'][0]]
                y_coords = [self.graph.nodes[alternate_path[i]]['pos'][1],
                            self.graph.nodes[alternate_path[i + 1]]['pos'][1]]
                self.ax.plot(x_coords, y_coords, 'b--', linewidth=2, label='替代路径' if i == 0 else "")

    def update_animation(self, frame):
        if self.update_function:
            self.update_function(frame)

    def start_animation(self):
        if self.animation is not None:
            self.animation.event_source.stop()
        self.animation = FuncAnimation(self.fig, self.update_animation,
                                       frames=range(6),  # 根据具体的动画帧数调整
                                       interval=1500,  # 动画的时间间隔（毫秒）
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