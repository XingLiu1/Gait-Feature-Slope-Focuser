import numpy as np
from matplotlib import pyplot as plt

import data_processing as dp
import event_detection as ed
import evaluation as ev
import visualization as viz
from Evaluation.matchNcompare import find_index_ranges_by_act, enhanced_match_and_compare_peaks

# Load data
# 加载数据
df = dp.load_data('./Dataset/selected_data2.csv')

# Data filtering
# 数据过滤
values1 = ['帕金森', '弯曲僵硬', '画圈', '膝过伸', '跷脚']
df1 = dp.filter_data(df, values1)

# Event detection and processing
# 事件识别和处理
GFSF = ed.GFSF.Gait_Feature_Slope_Focuser(ini_state=104, watch_length=30, nzone=40, pzone=30)
HS, TO = ed.cal_HS_TO(np.array(df.Euler_X_adjusted), GFSF)

# Evaluation
# 评估
# Define tolerance
# 定义容忍度
tolerance = 5

# Load ground truth peak data
# 加载地面真实值峰值数据
gt_hs_peaks = ev.load_peak_data("dfHSGT.csv")
gt_to_peaks = ev.load_peak_data("dfTOGT.csv")
to_peaks = [i for i in TO[0]]
hs_peaks = [i for i in HS[0]]

# Identify index ranges for each 'act'
# 为每个“动作”标识索引范围
act_index_ranges = find_index_ranges_by_act(df['act'])

# Generate performance data
# 生成性能数据
df_hs_metrics, df_to_metrics = ev.generate_performance_data(
    act_index_ranges, hs_peaks, gt_hs_peaks, to_peaks, gt_to_peaks, tolerance
)

# Print results
# 打印结果
print("HS Metrics:")
print(df_hs_metrics)
print("\nTO Metrics:")
print(df_to_metrics)

acts_to_view = ['启动停止+正常行走', '帕金森', '弯曲僵硬', '快速启停+转弯', '快速启动+停止（3步一次）', '拖地',
       '正常行走+转弯', '正常走', '画圈', '站立', '膝过伸', '跷脚']
plt.figure(figsize=(12, 6))
# Visualization
# 可视化
viz.plot_peaks(np.array(df.Euler_X_adjusted), act_index_ranges,to_peaks, gt_to_peaks,acts_to_view)
viz.plot_peaks(np.array(df.Euler_X_adjusted), act_index_ranges,hs_peaks, gt_hs_peaks,acts_to_view)
viz.plot_stop_data(np.array(df.Euler_X_adjusted), act_index_ranges,GFSF, acts_to_view)
viz.plot_signal_subplots(np.array(df.Euler_X_adjusted), GFSF,0,len(np.array(df.Euler_X_adjusted)))
plt.show(block=1)

# Extract data and index range for example
# 提取数据和索引范围，用作示例
datal = np.array(df.Euler_X_adjusted)
start_index = 104240  # Example start index 示例起始索引
end_index = 105025    # Example end index 示例结束索引

# Plot signal subplots
# 绘制信号子图
viz.plot_signal_subplots(datal, GFSF, start_index, end_index)

# Prepare data for histogram plotting
# 准备绘制直方图的数据
# For overall results (not split by act)
# 对整体结果（不区分活动）
overall_metrics_hs = enhanced_match_and_compare_peaks(hs_peaks, gt_hs_peaks, tolerance)
overall_metrics_to = enhanced_match_and_compare_peaks(to_peaks, gt_to_peaks, tolerance)
matched_differences = overall_metrics_hs['matched_differences'].copy()
matched_differences.extend(overall_metrics_to['matched_differences'])
non_zero_differences = [diff for diff in matched_differences if diff != 0]

# Plot histogram with normal distribution fit
# 绘制直方图并拟合正态分布
viz.plot_histogram_with_normal_fit(non_zero_differences, (0, 8, 1), (0, 10))
