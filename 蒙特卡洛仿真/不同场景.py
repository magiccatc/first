import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle
from shapely.geometry import Point
from shapely.ops import unary_union

plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False


class Grid:
    def __init__(self):
        self.grid_size = 100  # 总空间大小 (100x100)
        self.num_cells = 5  # 网格数量 (5x5)
        self.cell_size = self.grid_size // self.num_cells  # 每个网格单元的大小 (20x20)
        self.data_x = []
        self.data_y = []

    # 生成随机点并记录在网格中的位置
    def generate_random_points(self):
        self.data_x = []
        self.data_y = []
        for i in range(self.num_cells):
            for j in range(self.num_cells):
                # 在每个网格单元内随机生成一个点
                x = np.random.randint(i * self.cell_size, (i + 1) * self.cell_size)
                y = np.random.randint(j * self.cell_size, (j + 1) * self.cell_size)
                self.data_x.append(x)
                self.data_y.append(y)

        self.data_x = np.array(self.data_x)
        self.data_y = np.array(self.data_y)

    # 计算四分之一圆的面积
    def quarter_circle_area(self, radius):
        return 0.25 * np.pi * radius ** 2

    # 使用 unary_union 计算两个圆的并集面积
    def calculate_union_area(self, radius1, radius2, center1, center2):
        # 创建Shapely的圆形对象
        circle1 = Point(center1).buffer(radius1)
        circle2 = Point(center2).buffer(radius2)

        # 计算并集面积
        union_area = unary_union([circle1, circle2]).area
        return union_area

    # 检查点是否在四分之一圆中
    def is_in_quarter_circle(self, x, y, radius):
        return x >= 0 and y >= 0 and (x ** 2 + y ** 2 <= radius ** 2)

    # 检查点是否在指定圆中
    def is_in_circle(self, x, y, center, radius):
        return (x - center[0]) ** 2 + (y - center[1]) ** 2 <= radius ** 2

    # 绘制四分之一圆和第二个圆
    def plot_circles(self, ax, data_x, data_y):
        # 以原点为中心的四分之一圆，半径为60
        quarter_circle = Arc((0, 0), 120, 120, theta1=0, theta2=90, color='blue', label="四分之一圆")
        ax.add_patch(quarter_circle)

        # 以第3x3个方块的中心为圆心，半径为36
        index_3x3 = 2 * self.num_cells + 2  # 第3x3个方块对应的索引
        center2 = (float(data_x[index_3x3]), float(data_y[index_3x3]))
        circle2 = Circle(center2, 36, color='green', fill=False, label="第3x3方块的圆")
        ax.add_patch(circle2)

        # 绘制网格
        for i in range(0, 101, 20):
            ax.vlines(i, 0, 100, colors='black', linestyles='dotted')
            ax.hlines(i, 0, 100, colors='black', linestyles='dotted')

        # 设置坐标轴范围和标签
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.set_aspect('equal')
        ax.set_xlabel("X轴")
        ax.set_ylabel("Y轴")
        ax.legend()


# 主函数
if __name__ == "__main__":
    grid = Grid()

    radius1 = 60
    radius2 = 36
    center1 = (0, 0)  # 原点

    num_trials = 100
    union_areas = []
    points_in_quarter_circle = []
    points_in_union = []

    # 运行100次实验
    for trial in range(num_trials):
        grid.generate_random_points()  # 生成随机点

        # 第3x3个方块的中心
        index_2x2 = 2 * grid.num_cells + 2
        center2 = (float(grid.data_x[index_2x2]), float(grid.data_y[index_2x2]))

        # 计算两个圆的并集面积
        union_area = grid.calculate_union_area(radius1, radius2, center1, center2)
        union_areas.append(union_area)

        # 记录落入四分之一圆的点的数量
        count_in_quarter_circle = 0
        count_in_union = 0
        for x, y in zip(grid.data_x, grid.data_y):
            if grid.is_in_quarter_circle(x, y, radius1):
                count_in_quarter_circle += 1
            # 记录落入并集的点（即在四分之一圆或第二个圆中）
            if grid.is_in_quarter_circle(x, y, radius1) or grid.is_in_circle(x, y, center2, radius2):
                count_in_union += 1

        points_in_quarter_circle.append(count_in_quarter_circle)
        points_in_union.append(count_in_union)

        # 绘制第1次实验的图像
        if trial == 0:
            fig, ax = plt.subplots()
            grid.plot_circles(ax, grid.data_x, grid.data_y)
            plt.title("第一次实验中的四分之一圆与圆形并集")
            plt.show()

    # 计算100次实验的并集面积平均值
    avg_union_area = np.mean(union_areas)

    # 计算平均落入四分之一圆和并集的点的数量
    avg_points_in_quarter_circle = np.mean(points_in_quarter_circle)
    avg_points_in_union = np.mean(points_in_union)

    # 输出结果
    print(f"100次实验的并集面积平均值: {avg_union_area:.2f}")
    print(f"落入四分之一圆的平均点数: {avg_points_in_quarter_circle:.2f}")
    print(f"落入四分之一圆和并集的平均点数: {avg_points_in_union:.2f}")
