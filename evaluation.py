import pandas as pd
from Evaluation.matchNcompare import enhanced_match_and_compare_peaks, compute_metrics_within_range, find_index_ranges_by_act

# Function: Load peak data from a file
# 函数：从文件中加载峰值数据
def load_peak_data(file_path):
    """
    Load peak data from a specified file path.
    从指定的文件路径加载峰值数据。

    :param file_path: Path to the peak data file. 峰值数据文件的路径。
    :return: List of peak data. 峰值数据列表。
    """
    return [i[0] for i in pd.read_csv(file_path).to_numpy()]

# Function: Compute performance metrics
# 函数：计算性能指标
def compute_performance_metrics(matched_differences, total_missed, false_detections, total_true):
    """
    Compute performance metrics based on the peak matching results.
    根据峰值匹配结果计算性能指标。

    :param matched_differences: Differences in matched peaks. 匹配峰值的差异。
    :param total_missed: Total number of missed peaks. 总错过的峰值数量。
    :param false_detections: Number of false detections. 错误检测的数量。
    :param total_true: Total number of true peaks. 真实峰值的总数。
    :return: Sensitivity, Positive Predictive Value (PPV), and detection rate.
             灵敏度、阳性预测值 (PPV) 和检测率。
    """
    TP = len(matched_differences)
    FN = total_missed
    FP = false_detections
    sensitivity = (TP / (TP + FN)) * 100 if (TP + FN) > 0 else 0
    PPV = (TP / (TP + FP)) * 100 if (TP + FP) > 0 else 0
    detection_rate = (TP / total_true) * 100 if total_true > 0 else 0
    return sensitivity, PPV, detection_rate

# Function: Generate performance data
# 函数：生成性能数据
def generate_performance_data(act_index_ranges, hs_peaks, gt_hs_peaks, to_peaks, gt_to_peaks, tolerance):
    """
    Generate performance data for HS and TO based on the provided peak data and tolerance.
    根据提供的峰值数据和容忍度，生成HS和TO的性能数据。

    :param act_index_ranges: Index ranges for each activity. 每个活动的索引范围。
    :param hs_peaks: List of HS peaks. HS峰值列表。
    :param gt_hs_peaks: List of ground truth HS peaks. HS真实峰值列表。
    :param to_peaks: List of TO peaks. TO峰值列表。
    :param gt_to_peaks: List of ground truth TO peaks. TO真实峰值列表。
    :param tolerance: Tolerance for peak matching. 峰值匹配的容忍度。
    :return: DataFrames containing performance data for HS and TO.
             包含HS和TO性能数据的DataFrames。
    """
    data_to_for_df = []
    data_hs_for_df = []

    # Compute metrics for each activity
    # 为每个活动计算指标
    for act, (start_index, end_index) in act_index_ranges.items():
        metrics_hs = compute_metrics_within_range(hs_peaks, gt_hs_peaks, start_index, end_index, tolerance)
        metrics_to = compute_metrics_within_range(to_peaks, gt_to_peaks, start_index, end_index, tolerance)

        append_act_metrics(data_hs_for_df, act, metrics_hs, gt_hs_peaks, start_index, end_index)
        append_act_metrics(data_to_for_df, act, metrics_to, gt_to_peaks, start_index, end_index)

    # Compute overall metrics
    # 计算整体指标
    overall_metrics_hs = enhanced_match_and_compare_peaks(hs_peaks, gt_hs_peaks, tolerance)
    overall_metrics_to = enhanced_match_and_compare_peaks(to_peaks, gt_to_peaks, tolerance)

    append_overall_metrics(data_hs_for_df, overall_metrics_hs, gt_hs_peaks, "Overall")
    append_overall_metrics(data_to_for_df, overall_metrics_to, gt_to_peaks, "Overall")

    # Create DataFrames
    # 创建DataFrame
    df_hs_metrics = pd.DataFrame(data_hs_for_df)
    df_to_metrics = pd.DataFrame(data_to_for_df)

    return df_hs_metrics, df_to_metrics

# Function: Append metrics for a specific activity
# 函数：为特定活动追加指标数据
def append_act_metrics(data_for_df, act, metrics, gt_peaks, start_index, end_index):
    """
    Append metrics for a specific activity to the data list.

    为特定活动向数据列表中追加指标。

    :param data_for_df: Data list. 数据列表。
    :param act: Name of the activity. 活动名称。
    :param metrics: Calculated metrics. 计算得到的指标。
    :param gt_peaks: List of ground truth peaks. 真实峰值列表。
    :param start_index: Start index of the activity. 活动的起始索引。
    :param end_index: End index of the activity. 活动的结束索引。
    """
    TP = len(metrics['matched_differences'])
    FN = metrics['total_missed']
    FP = len(metrics['false_detections'])
    true_number = len([p for p in gt_peaks if start_index <= p <= end_index])

    sensitivity = (TP / (TP + FN)) * 100 if (TP + FN) > 0 else 0
    PPV = (TP / (TP + FP)) * 100 if (TP + FP) > 0 else 0

    data_for_df.append({
        "Act": act,
        "检出数目": TP,
        "真实数目": true_number,
        "检出率": metrics['detection_rate'],
        "平均偏差": metrics['average_difference'],
        "PPV": PPV,
        "sensitivity": sensitivity
    })

# 函数：追加整体指标数据
def append_overall_metrics(data_for_df, overall_metrics, gt_peaks, label):
    """
    Append overall metrics data to the data list.

    向数据列表中追加整体指标数据。

    :param data_for_df: Data list. 数据列表。
    :param overall_metrics: Calculated overall metrics. 计算得到的整体指标。
    :param gt_peaks: List of ground truth peaks. 真实峰值列表。
    :param label: Label (e.g., "Overall"). 标签（例如："Overall"）。
    """
    # Code for appending overall metrics...
    # 追加整体指标的代码...
    TP = len(overall_metrics['matched_differences'])
    FN = overall_metrics['total_missed']
    FP = len(overall_metrics['false_detections'])
    true_number = len(gt_peaks)

    sensitivity = (TP / (TP + FN)) * 100 if (TP + FN) > 0 else 0
    PPV = (TP / (TP + FP)) * 100 if (TP + FP) > 0 else 0

    data_for_df.append({
        "Act": label,
        "检出数目": TP,
        "真实数目": true_number,
        "检出率": overall_metrics['detection_rate'],
        "平均偏差": overall_metrics['average_difference'],
        "PPV": PPV,
        "sensitivity": sensitivity
    })

# 函数：评估峰值
def evaluate_peaks(df_used, hs_peaks, to_peaks, gt_hs_peaks, gt_to_peaks, tolerance):
    """
    Evaluate the peaks for HS and TO.

    评估HS和TO的峰值。

    :param df_used: DataFrame being used. 使用的DataFrame。
    :param hs_peaks: List of HS peaks. HS峰值列表。
    :param to_peaks: List of TO peaks. TO峰值列表。
    :param gt_hs_peaks: List of ground truth HS peaks. HS真实峰值列表。
    :param gt_to_peaks: List of ground truth TO peaks. TO真实峰值列表。
    :param tolerance: Tolerance for peak matching. 峰值匹配的容忍度。
    :return: Dictionary of evaluation results. 评估结果的字典。
    """
    comparison_results_hs = enhanced_match_and_compare_peaks(hs_peaks, gt_hs_peaks, tolerance)
    comparison_results_to = enhanced_match_and_compare_peaks(to_peaks, gt_to_peaks, tolerance)

    act_index_ranges = find_index_ranges_by_act(df_used['act'])

    sensitivity_hs, PPV_hs, detection_rate_hs = compute_performance_metrics(
        comparison_results_hs['matched_differences'],
        comparison_results_hs['total_missed'],
        len(comparison_results_hs['false_detections']),
        len(gt_hs_peaks)
    )

    sensitivity_to, PPV_to, detection_rate_to = compute_performance_metrics(
        comparison_results_to['matched_differences'],
        comparison_results_to['total_missed'],
        len(comparison_results_to['false_detections']),
        len(gt_to_peaks)
    )

    return {
        "HS": {"sensitivity": sensitivity_hs, "PPV": PPV_hs, "detection_rate": detection_rate_hs},
        "TO": {"sensitivity": sensitivity_to, "PPV": PPV_to, "detection_rate": detection_rate_to}
    }
