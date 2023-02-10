import random
import time

import numpy
from 模拟网络.data import Data

choose_list = [i for i in range(11)]
data_number = 1000000

start_time = time.perf_counter()
data_set = [Data(x, y, True) for x, y in
            zip(numpy.random.choice(choose_list, data_number),
                numpy.random.choice(choose_list, data_number))]
print(time.perf_counter() - start_time)

start_time = time.perf_counter()
data_set_2 = []
while len(data_set_2) < data_number:
    pair = random.sample(choose_list, 2)
    data_set_2.append(Data(pair[0], pair[1], True))
print(time.perf_counter() - start_time)
"""第一种方式生成数据的速度是第二种的一半左右"""