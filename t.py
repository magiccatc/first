import numpy as np

# 创建示例二维数组
array_2d = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

# 遍历每行的第一个元素
for i in range(array_2d.shape[0]):  # 遍历行数
    first_element = array_2d[i, 0]  # 获取每行的第一个元素
    print(f"第 {i+1} 行的第一个元素是: {first_element}")
