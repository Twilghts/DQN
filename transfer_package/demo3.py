import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from torch import nn

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # 让图像可以正常生成

data = pd.read_csv('Income1.csv.csv')
data.info()
plt.scatter(data.Education, data.Income)

plt.xlabel('数据大小')  # 改横坐标

plt.show()  # 输出

X = torch.from_numpy(data.Education.values.reshape(-1, 1).astype(np.float32))
Y = torch.from_numpy(data.Income.values.reshape(-1, 1).astype(np.float32))  # 数据预处理

model = nn.Linear(1, 1)  # w*input + b  等价于model(input)
loss_fn = nn.MSELoss()  # 损失函数
opt = torch.optim.SGD(model.parameters(), lr=0.0001)

for epoch in range(2000):
    for x, y in zip(X, Y):
        y_pred = model(x)  # 使用模型预测
        loss = loss_fn(y, y_pred)  # 根据预测结果计算损失
        opt.zero_grad()  # 把变量梯度清零
        loss.backward()  # 求解梯度
        opt.step()  # 优化模型参数

print(model.weight)
print(model.bias)  # 优化后的权重与偏置常数
