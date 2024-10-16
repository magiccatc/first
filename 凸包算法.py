import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

# 生成随机点
num_points = 10
points = np.random.rand(num_points, 2)

# 使用 ConvexHull 找到凸包
hull = ConvexHull(points)
print(hull.simplices)
# 计算凸包面积
hull_area = hull.volume

# 可视化
plt.plot(points[:,0], points[:,1], 'o')  # 画出所有点
for simplex in hull.simplices:
    plt.plot(points[simplex, 0], points[simplex, 1], 'k-')  # 画出凸包边界

plt.fill(points[hull.vertices, 0], points[hull.vertices, 1], 'lightgray', alpha=0.5)  # 填充凸包区域
plt.title(f'Convex Hull Area: {hull_area:.2f}')
plt.show()
