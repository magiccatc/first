from scipy.spatial import ConvexHull
from shapely.geometry import Polygon
from shapely.ops import unary_union
import matplotlib.pyplot as plt
import numpy as np

def circle_to_polygon(center, radius, num_segments=100):
    angle = np.linspace(0, 2 * np.pi, num_segments)
    x = center[0] + radius * np.cos(angle)
    y = center[1] + radius * np.sin(angle)
    return Polygon(np.column_stack([x, y]))

# 随机生成点
num_points = 10
points = np.random.rand(num_points, 2)

# 使用 ConvexHull 找到凸包
hull = ConvexHull(points)
polygon_vertices = points[hull.vertices]  # 获取凸包顶点坐标
polygon = Polygon(polygon_vertices)  # 构建多边形

# 定义圆的半径
radius = 0.1

# 创建圆的多边形
circles = [circle_to_polygon(center, radius) for center in polygon_vertices]

# 计算所有圆的并集
circle_union = unary_union(circles)

# 计算圆并集与多边形的并集
combined_union = unary_union([circle_union, polygon])
combined_area = combined_union.area

# 可视化
fig, ax = plt.subplots()
x, y = polygon.exterior.xy
ax.plot(x, y, color='blue', label='Polygon')

# 绘制每个圆
for circle in circles:
    x, y = circle.exterior.xy
    ax.plot(x, y, color='lightblue', alpha=0.5)

# 绘制并集
if not combined_union.is_empty:
    x, y = combined_union.exterior.xy
    ax.fill(x, y, color='red', alpha=0.3, label='Union Area')  # 填充并集区域
    ax.plot(x, y, color='red', label='Union Boundary')

# 绘制原始点
ax.plot(points[:, 0], points[:, 1], 'o', label='Points')

plt.title(f'Union Area: {combined_area:.2f}')
plt.legend()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
