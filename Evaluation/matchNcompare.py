from matplotlib import pyplot as plt

# Function: Find index ranges for each activity in the dataframe
# 函数：在数据框中为每个活动查找索引范围
def find_index_ranges_by_act(acts):
    """
    Calculate the start and end indices for each activity.

    计算每个活动的起始和结束索引。

    :param acts: List of activities. 活动列表。
    :return: Dictionary of start and end indices for each activity. 每个活动的起始和结束索引的字典。
    """

    index_ranges = {}
    current_act = None

    for index, act in enumerate(acts):
        if act != current_act:
            if current_act is not None:
                index_ranges[current_act][1] = index - 1  # 设置前一个活动的结束索引
            current_act = act
            index_ranges[act] = [index, None]  # 设置新活动的起始索引

    # 设置最后一个活动的结束索引
    if current_act is not None:
        index_ranges[current_act][1] = len(acts) - 1

    return index_ranges

# 函数：匹配并比较两组峰值
def enhanced_match_and_compare_peaks(peaks1, peaks2, tolerance):
    """
    Match and compare two sets of peaks, calculate matched peaks, missed detections, etc.

    匹配并比较两组峰值，计算匹配的峰值、错过的检测、错误的检测等。

    :param peaks1: First set of peaks. 第一组峰值。
    :param peaks2: Second set of peaks. 第二组峰值。
    :param tolerance: Tolerance level. 容忍度。
    :return: Dictionary of matching results. 匹配结果的字典。
    """
    # ...
    matched_peaks = []
    missed_detections = []
    false_detections = []

    for peak1 in peaks1:
        if peaks2:
            closest_peak = min(peaks2, key=lambda peak2: abs(peak2 - peak1))
            if abs(closest_peak - peak1) <= tolerance:
                matched_peaks.append(abs(closest_peak - peak1))
            else:
                missed_detections.append(peak1)
        else:
            missed_detections.append(peak1)

    for peak2 in peaks2:
        if not any(abs(peak1 - peak2) <= tolerance for peak1 in peaks1):
            false_detections.append(peak2)

    detection_rate = len(matched_peaks) / len(peaks2) if len(peaks2) > 0 else 0
    average_difference = sum(matched_peaks) / len(matched_peaks) if len(matched_peaks) > 0 else 0

    return {
        "matched_differences": matched_peaks,
        "average_difference": average_difference,# * 16.6,
        "detection_rate": detection_rate,
        "missed_detections": missed_detections,
        "false_detections": false_detections,
        "total_missed": len(missed_detections),
        "total_false": len(false_detections)
    }

# 函数：绘制活动数据和峰值
def plot_act_data_and_peaks(data, act_ranges, peaks, acts_to_view, marker, s):
    """
    Plot data and peaks for selected activities.

    绘制选定活动的数据和峰值。

    :param data: Data list. 数据列表。
    :param act_ranges: Dictionary of index ranges for each activity. 每个活动的索引范围字典。
    :param peaks: List of peaks. 峰值列表。
    :param acts_to_view: List of activities to view. 要查看的活动列表。
    :param marker: Style of peak markers. 峰值标记样式。
    :param s: Label prefix. 标签前缀。
    """
    for act in acts_to_view:
        start_index, end_index = act_ranges[act]
        act_data = data[start_index:end_index + 1]
        act_peaks = [peak for peak in peaks if start_index <= peak <= end_index]

        plt.plot(range(start_index, end_index + 1), act_data, label=s + f"{act} Data")
        plt.scatter(act_peaks, [data[p] for p in act_peaks], label=s + f"{act} Peaks", marker=marker)

    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.title("Data and Peaks for Selected Acts")
    # plt.legend()

def compute_metrics_within_range(peaks1, peaks2, start_index, end_index, tolerance):
    """
    Compute metrics for peak matching within a given range.

    在给定范围内计算峰值匹配的度量标准。

    :param peaks1: First set of peaks. 第一组峰值。
    :param peaks2: Second set of peaks. 第二组峰值。
    :param start_index: Start index. 起始索引。
    :param end_index: End index. 结束索引。
    :param tolerance: Tolerance level. 容忍度。
    :return: Dictionary of matching results. 匹配结果的字典。
    """
    peaks1_in_range = [p for p in peaks1 if start_index <= p <= end_index]
    peaks2_in_range = [p for p in peaks2 if start_index <= p <= end_index]

    return enhanced_match_and_compare_peaks(peaks1_in_range, peaks2_in_range, tolerance)
