import math
import warnings

import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
warnings.filterwarnings("ignore", category=DeprecationWarning)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

class HistogramPlotter:
    def __init__(self):
        """
        初始化图表、随机点及相关参数
        """
        # 创建绘图对象
        self.fig, self.ax = plt.subplots(figsize=(10, 10), dpi=100)
        self.ax.set_xlim(0, 100)  # 设置x轴范围
        self.ax.set_ylim(0, 100)  # 设置y轴范围

        # 初始化用于存储点的数组
        self.data_x = np.array([])
        self.data_y = np.array([])
        self.kmeans = None
    def init_points(self):
        """
        生成随机点，并将其均匀分布在一个 sqrt(num_points) x sqrt(num_points) 的网格中
        """
        num_points = 25  # 设定生成 25 个点
        self.num_points = num_points

        # 计算网格的行和列（点数量的平方根）
        sqrt_points = int(np.sqrt(num_points))

        # 计算每个网格单元的大小
        self.cell_size_x = 101 // sqrt_points
        self.cell_size_y = 101 // sqrt_points

        # 初始化存储 X 和 Y 坐标的列表
        self.data_x = []
        self.data_y = []

        # 遍历每个网格单元并随机生成点
        for i in range(sqrt_points):
            for j in range(sqrt_points):
                x = np.random.randint(i * self.cell_size_x, (i + 1) * self.cell_size_x)
                y = np.random.randint(j * self.cell_size_y, (j + 1) * self.cell_size_y)
                self.data_x.append(x)
                self.data_y.append(y)
        # # 随机生成 x 和 y 坐标，范围在 [0, 100] 之间
        # self.data_x = np.random.uniform(0, 100, num_points)
        # self.data_y = np.random.uniform(0, 100, num_points)
        # 将 X 和 Y 列表转换为 NumPy 数组
        self.data_x = np.array(self.data_x)
        self.data_y = np.array(self.data_y)

        # 绘制网格线
        for i in range(1, sqrt_points):
            self.ax.vlines(i * self.cell_size_x, 0, 100, colors='black', linestyles='dotted')
            self.ax.hlines(i * self.cell_size_y, 0, 100, colors='black', linestyles='dotted')

        # 绘制随机生成的点和原点
        self.ax.scatter(self.data_x, self.data_y, color='blue', label='随机点')
        self.ax.scatter(0, 0, color='red', label='原点')

        # 设置图例和标题
        self.ax.legend()
        self.ax.set_title('随机点分布')
        self.ax.set_xlabel('X 坐标')
        self.ax.set_ylabel('Y 坐标')

        # 显示图形
        plt.show()
    def success_rate_conclusion(self,length): #关于功率的计算
        M=1
        m=0
        n=1
        psize=8192
        BER=M/(length*np.sqrt(math.log(m+n*length),10))
        if 0<=length<=36:
            return 1-(1-BER)**psize
        else:
            return 0
    def hierarchical_caculate(self):
            #在这里添加关于“分级指控”模式的处理逻辑
        if self.kmeans is None:
            self.kmeans = KMeans(n_clusters=4)
            self.kmeans.fit(np.vstack((self.data_x, self.data_y)).T)
            self.cluster_centers = self.kmeans.cluster_centers_
            self.closest_data_points = []
            for center in self.cluster_centers:
                distances = np.sqrt((self.data_x - center[0]) ** 2 + (self.data_y - center[1]) ** 2)
                closest_point_index = np.argmin(distances)
                self.closest_data_points.append((self.data_x[closest_point_index], self.data_y[closest_point_index]))
            distances = np.sqrt((self.data_x - 0) ** 2 + (self.data_y - 0) ** 2)
            self.allpoints = np.argsort(-distances)
            self.allpoints_distances = distances[self.allpoints] # 所有点到原点的距离,这个是集中指控的

            # 为每个最远点找到最近的簇中心
            self.allpoints_centers = []
            for index in self.allpoints:
                point = np.array([self.data_x[index], self.data_y[index]])
                distances_to_centers = np.sqrt(np.sum((np.array(self.closest_data_points) - point) ** 2, axis=1))
                closest_center_index = np.argmin(distances_to_centers)
                self.allpoints_centers.append((index, self.closest_data_points[closest_center_index]))

            # 计算每个最远点到最近簇中心的距离
            self.all_hierarchical_distances = []
            for index, (x, y) in self.allpoints_centers:
                    point = np.array([self.data_x[index], self.data_y[index]])
                    distance_from_origin_to_center =np.sqrt(x**2+y**2)
                    distance_from_center_to_point = np.sqrt(
                        (point[0] - x) ** 2 + (point[1] - y) ** 2)
                # 存储距离
                    self.all_hierarchical_distances.append([distance_from_origin_to_center, distance_from_center_to_point])
            print(self.allpoints_distances)
            print(self.closest_data_points)
            print(self.all_hierarchical_distances)
plotter = HistogramPlotter()
plotter.init_points()
plotter.hierarchical_caculate()