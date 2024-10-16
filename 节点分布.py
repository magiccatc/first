import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题
# 设置随机种子以便重现结果
np.random.seed(0)

# 读取指定的图片
marker_image = mpimg.imread('潜艇部队.png')

# 第一张图：随机生成25个节点
plt.figure(figsize=(10, 5))

# 随机生成25个节点
x_random = np.random.uniform(0, 100, 25)
y_random = np.random.uniform(0, 100, 25)

plt.subplot(1, 2, 1)
for x, y in zip(x_random, y_random):
    plt.imshow(marker_image, extent=(x-2, x+2, y-2, y+2))

plt.xlim(0, 100)
plt.ylim(0, 100)
plt.title('随机节点')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# 第二张图：5x5格子生成节点
plt.subplot(1, 2, 2)

# 生成网格
grid_size = 5
x_grid = np.linspace(10, 90, grid_size)
y_grid = np.linspace(10, 90, grid_size)

for i in range(grid_size):
    for j in range(grid_size):
        # 在每个格子中随机生成一个节点位置
        x = np.random.uniform(x_grid[i] - 8, x_grid[i] + 8)
        y = np.random.uniform(y_grid[j] - 8, y_grid[j] + 8)
        # 在指定位置显示图片
        plt.imshow(marker_image, extent=(x-2, x+2, y-2, y+2))

# 绘制网格线
for i in range(grid_size + 1):
    plt.axvline(x=20 * i, color='gray', linestyle='--')
    plt.axhline(y=20 * i, color='gray', linestyle='--')

plt.xlim(0, 100)
plt.ylim(0, 100)
plt.title('栅格化节点')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

plt.tight_layout()
plt.show()
