import numpy as np
import GFSF.GFSF_60hz_dynamic as GFSF

def cal_HS_TO(datal, GFSF):
    """
    计算HS和TO的位置，并将数据转换为相应的相位。
    Calculate the positions of HS (Heel Strike) and TO (Toe Off),
    and convert the data into corresponding phases.

    :param datal: 输入的数据列表。List of input data.
    :param GFSF: Gait Feature Slope Focuser的实例。Instance of the slope sum function.
    :return: HS和TO的位置。Positions of HS and TO.
    """

    def event2phase(n, HS, TO):
        """
        将事件转换为相位。
        Convert events into phases.

        :param n: 当前索引。Current index.
        :param HS: Heel Strike位置列表。List of Heel Strike positions.
        :param TO: Toe Off位置列表。List of Toe Off positions.
        :return: 相位值。Phase value.
        """
        if HS[0][-1] < TO[0][-1] and HS[0][-1] > TO[0][-2]:
            # 计算相位转换因子。Calculate phase conversion factor.
            k = 40 / (HS[0][-1] - TO[0][-2])
            K.append(k)
            phase = (n - TO[0][-1]) * k + 63
            if phase >= 100:
                phase = 100
            return phase
        elif HS[0][-1] >= TO[0][-1] and HS[0][-2] < TO[0][-1]:
            k = 63 / (TO[0][-1] - HS[0][-2])
            K.append(k)
            phase = (n - HS[0][-1]) * k
            if phase >= 63:
                phase = 63
            return phase
        else:
            return 0

    n = 0  # 初始化索引。Initialize index.
    phase = []  # 相位列表。List for phases.
    K = []  # 相位转换因子列表。List for phase conversion factors.
    avg = 0  # 平均值。Average value.

    a = 0  # 初始索引。Initial index.

    for i in datal:
        if n < a:
            avg = (avg * n + i) / (n + 1)
        else:
            avg = 92
            GFSF.GFSF_update_new(n, i)  # 更新GFSF。
            phase.append(event2phase(n, GFSF.HS, GFSF.TO))

        n += 1  # 增加索引。Increment index.

    return GFSF.HS, GFSF.TO  # 返回HS和TO的位置。Return positions of HS and TO.
