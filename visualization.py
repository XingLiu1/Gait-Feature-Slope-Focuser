import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from Evaluation.matchNcompare import plot_act_data_and_peaks

# Function: Plot data and peaks for different activities
# 函数：绘制不同动作的数据和峰值
def plot_peaks(datal, act_index_ranges, peaks, gt_peaks, acts_to_view):
    """
    Plot data and peaks for specified activities.
    绘制指定动作的数据和峰值。

    :param datal: Data list. 数据列表。
    :param act_index_ranges: Dictionary of activity index ranges. 动作索引范围字典。
    :param peaks: List of peaks. 峰值列表。
    :param gt_peaks: List of ground truth peaks. 真实峰值列表。
    :param acts_to_view: List of activities to view. 要查看的动作列表。
    """
    # Code to plot real and GFSF peaks...
    # 绘制真实峰值和GFSF峰值的代码...
    plot_act_data_and_peaks(datal, act_index_ranges, gt_peaks, acts_to_view, 'o', 'GT')
    plot_act_data_and_peaks(datal, act_index_ranges, peaks, acts_to_view, '*', 'GFSF')

# Function: Plot stop data
# 函数：绘制停止数据
def plot_stop_data(datal, act_index_ranges, GFSF, acts_to_view):
    """
    Plot stop data for specified activities.
    绘制指定动作的停止数据。

    :param datal: Data list. 数据列表。
    :param act_index_ranges: Dictionary of activity index ranges. 动作索引范围字典。
    :param GFSF: Results of GFSF analysis. GFSF分析结果。
    :param acts_to_view: List of activities to view. 要查看的动作列表。
    """
    # 绘制GFSF开始和结束标记
    plot_act_data_and_peaks(datal, act_index_ranges, GFSF.ST[0], acts_to_view, 'v', 'GFSF_start')
    plot_act_data_and_peaks(datal, act_index_ranges, GFSF.ED[0], acts_to_view, 'v', 'GFSF_end')

# Function: Plot signal subplots
# 函数：绘制信号子图
def plot_signal_subplots(datal, GFSF, start, end):
    """
    Plot signal subplots for a specific data range.
    为特定数据范围绘制信号子图。

    :param datal: Data list. 数据列表。
    :param GFSF: Results of GFSF analysis. GFSF分析结果。
    :param start: Start index for subplots. 子图的开始索引。
    :param end: End index for subplots. 子图的结束索引。
    """
    # Code to plot three subplots...
    # 绘制三个子图的代码...
    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    axs[0].plot(datal[start:end], label='Pulse Data', color='black')
    axs[1].plot(GFSF.posout[start:end], label='Positive GSFS', color='black')
    axs[2].plot(GFSF.negout[start:end], label='Negative GSFS', color='black')

    for ax in axs:
        ax.set_title(ax.get_legend_handles_labels()[1][0])
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        ax.legend()
        ax.label_outer()

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show(block = 1)


# Function: Plot histogram with normal distribution fit
# 函数：绘制直方图并拟合正态分布
def plot_histogram_with_normal_fit(data, bins_range, x_range):
    """
    Plot histogram of the data and fit a normal distribution.
    绘制数据的直方图并拟合正态分布。

    :param data: Data list. 数据列表。
    :param bins_range: Range for histogram bins. 直方图bins的范围。
    :param x_range: Range for the x-axis. x轴的范围。
    """
    plt.figure(figsize=(8, 6))
    counts, bins, patches = plt.hist(data, bins=np.arange(*bins_range), color='black', rwidth=0.8, density=True)

    mu, std = norm.fit(data)
    x = np.linspace(*x_range, 100)
    p = norm.pdf(x, mu, std)

    plt.plot(x, p, 'k', linewidth=2)
    plt.fill_between(x, p, alpha=0.1, color='black')

    for i, patch in enumerate(patches):
        plt.text(patch.get_x() + patch.get_width() / 2, patch.get_height(), f'{(counts[i] / sum(counts)) * 100:.1f}%', ha='center', va='bottom')

    plt.title('Matching Events (%) with Normal Distribution', fontsize=14)
    plt.xlabel('Δ t (Frames)', fontsize=12)
    plt.ylabel('Probability Density', fontsize=12)
    plt.xticks(bins[:-1] + 0.5, labels=[str(int(b)) for b in bins[:-1]])
    plt.xlim(x_range)
    plt.tight_layout()
    plt.show(block = 1)
