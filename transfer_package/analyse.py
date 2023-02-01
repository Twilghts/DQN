import numpy as np

data = [25.48402, 28.62619, 29.03593, 27.00042, 24.64746, 23.55302, 26.45152, 25.9581, 23.47726, 23.59067]

if len(data) != 10:
    print('数据量异常，请仔细检查。')

print(f'最小值:{min(data)}')
print(f'最大值:{max(data)}')
print(f'平均数:{np.mean(data)}')
print(f'总体方差:{np.var(data)}')
print(f'样本方差:{np.var(data, ddof=1)}')
print(f'总体标准差:{np.std(data)}')
print(f'样本标准差:{np.std(data, ddof=1)}')
