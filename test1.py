import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# 生成20个随机点
np.random.seed(0)  # 为了结果可重复
num_points = 40
points = np.random.rand(num_points, 2) * 10  # 生成在[0, 10]范围内的点

# 添加原点
origin = np.array([[0, 0]])
all_points = np.vstack([origin, points])

# 创建图
G = nx.Graph()

# 设置距离限制
distance_limit = 4 # 设置距离限制，例如5.0

# 添加节点
for i in range(len(all_points)):
    G.add_node(i, pos=all_points[i])

# 添加边，计算所有节点之间的距离，并根据距离限制添加边
for i in range(len(all_points)):
    for j in range(i + 1, len(all_points)):
        distance = np.linalg.norm(all_points[i] - all_points[j])
        if distance <= distance_limit:
            G.add_edge(i, j, weight=distance)

# 计算最短路径（从原点到所有其他点的最短路径）
lengths = {}
paths = {}
for i in range(1, len(all_points)):
    try:
        length, path = nx.single_source_dijkstra(G, 0, target=i, weight='weight')
        lengths[i] = length
        paths[i] = path
    except nx.NetworkXNoPath:
        # 如果没有路径，跳过该点
        lengths[i] = float('inf')
        paths[i] = []

# 找到距离原点最远的点
farthest_point = max(lengths.items(), key=lambda x: x[1])[0]
max_distance = lengths[farthest_point]
max_path = paths[farthest_point]

# 绘制图
pos = {i: (all_points[i][0], all_points[i][1]) for i in range(len(all_points))}
plt.figure(figsize=(10, 10))

# 绘制点
plt.scatter(all_points[:, 0], all_points[:, 1], color='blue')

# 绘制原点
plt.scatter([origin[0, 0]], [origin[0, 1]], color='red', label='Origin')

# 绘制最短路径
if max_path:
    for i in range(len(max_path) - 1):
        plt.plot([all_points[max_path[i]][0], all_points[max_path[i + 1]][0]],
                 [all_points[max_path[i]][1], all_points[max_path[i + 1]][1]],
                 'k--', lw=2)

plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Shortest Path from Origin to Farthest Point with Distance Limit')
plt.grid(True)
plt.show()
