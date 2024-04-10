import numpy as np

# 原始向量
vec = np.array([1, 2, 3])

# 扩充倍数
n = 2

# 使用 np.repeat() 进行重复操作
expanded_vec = np.repeat(vec, n)

print(expanded_vec)