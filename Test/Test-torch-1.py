import time
import torch

_n = 1000

a = torch.zeros(_n)
b = torch.zeros(_n)
c = torch.zeros(_n)

start_time = time.perf_counter()
for i in range(_n):
    c[i] = a[i] + b[i]
print(f'消耗时间:{time.perf_counter() - start_time}')

start_time = time.perf_counter()
d = a + b
print(f'消耗时间:{time.perf_counter() - start_time}')
