import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import GFSF.GFSF_60hz as GFSF
import pandas as pd

from matchNcompare import *

#########报告二数据

df1 = df = pd.read_csv('../Dataset/selected_data2.csv')
datal = np.array(df1.Euler_X_adjusted)


from scipy import signal
from scipy.signal import find_peaks
b, a = signal.butter(8, 0.4, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
filtedData = signal.filtfilt(b, a, datal)  # data为要过滤的信号
# 定义一个函数来绘制特定 act 的数据和峰值


from scipy.signal import find_peaks

# 定义不同的 act 类别及其对应的参数
act_parameters = {
    '启动停止+正常行走': {'distance': 30, 'height': 5},
    '帕金森':  {'distance': 30, 'height': 0},
    '弯曲僵硬': {'distance': 30, 'height': 6},
    '快速启停+转弯': {'distance': 60, 'height': 4},
    '快速启动+停止（3步一次）':  {'distance': 30, 'height': 10},
    '拖地': {'distance': 90, 'height': 5},
    '正常行走+转弯': {'distance': 60, 'height': 10},
    '正常走': {'distance': 20, 'height': 4},
    '画圈': {'distance': 20, 'height': 5},
    '站立': {'distance': 20, 'height': 20},
    '膝过伸': {'distance': 70, 'height': 7},
    '跷脚': {'distance': 100, 'height': 4},
    # 添加其他 act 类别和参数
}

# # 定义不同的 act 类别及其对应的参数
# act_parameters = {
#     '启动停止+正常行走': {'distance': 30, 'height': 5},
#     '帕金森':  {'distance': 30, 'height': 0},
#     '弯曲僵硬': {'distance': 30, 'height': 6},
#     '快速启停+转弯': {'distance': 60, 'height': 4},
#     '快速启动+停止（3步一次）':  {'distance': 30, 'height': 10},
#     '拖地': {'distance': 90, 'height': 5},
#     '正常行走+转弯': {'distance': 30, 'height': 4},
#     '正常走': {'distance': 20, 'height': 4},
#     '画圈': {'distance': 20, 'height': 5},
#     '站立': {'distance': 20, 'height': 20},
#     '膝过伸': {'distance': 70, 'height': 7},
#     '跷脚': {'distance': 100, 'height': 4},
#     # 添加其他 act 类别和参数
# }

# 获取每个 act 类别的索引范围
act_index_ranges = find_index_ranges_by_act(df1['act'])

# 用于存储所有 act 类别的峰值
all_peaks = []

for act, params in act_parameters.items():
    # 获取特定 act 类别的索引范围
    start_index, end_index = act_index_ranges[act]

    # 获取特定 act 类别的数据
    act_data = datal[start_index:end_index + 1]

    # 使用特定参数查找峰值
    peaks, _ = find_peaks(act_data, distance=params['distance'], height=params['height'])

    # 调整峰值索引以匹配原始数据的索引
    adjusted_peaks = [peak + start_index for peak in peaks]

    # 将峰值添加到总列表中
    all_peaks.extend(adjusted_peaks)

# 对峰值进行排序，以便后续分析
peaks3 = sorted(all_peaks)

# 您想查看的 act 列表
acts_to_view = ['启动停止+正常行走',
 '帕金森',
 '弯曲僵硬',
 '快速启停+转弯',
 '快速启动+停止（3步一次）',
 '拖地',
 '正常行走+转弯',
 '正常走',
 '画圈',
 '站立',
 '膝过伸',
 '跷脚']

acts_to_view = [
 '帕金森',
 '弯曲僵硬',

 '拖地',
 '跷脚']

# acts_to_view = ['拖地',]
# 绘制只包含特定 act 范围内的数据和对应峰值的图像
plt.figure(figsize=(12, 6))
# 调用函数绘制图像
plot_act_data_and_peaks(datal, act_index_ranges, peaks3, acts_to_view,'.','GT')
plt.show(block = 1)


dfGT = pd.DataFrame(peaks3)
dfGT.to_csv("../dfTOGT.csv", index=False)
