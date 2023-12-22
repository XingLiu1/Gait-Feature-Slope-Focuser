class Gait_Feature_Slope_Focuser:
    """
    Gait Feature Slope Focuser，用于处理信号并检测HS（Heel Strike）和TO（Toe Off）事件。
    """
    def __init__(self, ini_state=104, watch_length=30, nzone=30, pzone=30):
        """
        初始化Gait Feature Slope Focuser。

        :param ini_state: 初始状态的阈值。
        :param watch_length: 观察窗口长度。
        :param nzone: 负区域长度。
        :param pzone: 正区域长度。
        """
        self.watch_zone = [0] * watch_length
        self.firstdiff1 = [0] * (pzone - 1)
        self.firstdiff2 = [0] * (nzone - 1)

        self.HS_state = 0
        self.HSsleepcount_list = [50, 50, 50]
        self.HSsleepcount = 50

        self.TO_state = 0
        self.HSsleepcount_list = [50, 50, 50]
        self.TOsleepcount = 50

        self.ini_state = 1
        self.ini_count = []
        self.ini_place = 0

        self.TO_threshold_list = [5,5,5]
        self.TO_threshold = 5

        self.HS_threshold_list = [5,5,5]
        self.HS_threshold = 5

        self.posout = []
        self.negout = []

        self.HS = [[0, 42], [0, 0]]
        self.TO = [[0, 70], [0, 0]]

        self.ST = [[0, 0], [0, 0]]
        self.ED = [[0, 0], [0, 0]]

        self.stopcount = 0

    def update(self, input):
        """
        更新函数，用于处理输入信号。

        :param input: 输入信号值。
        """
        # 处理初始状态
        if self.ini_state:
            self.ini_count.append(input)
            if len(self.ini_count) == 50:
                self.ini_state = 0
                self.ini_count.sort()
                self.ini_place = sum(self.ini_count[10:40]) / len(self.ini_count[10:40])

        input = input - self.ini_place
        # 更新一阶差分
        self.firstdiff1[0:-1] = self.firstdiff1[1::]
        self.firstdiff1[-1] = input - self.watch_zone[-1]
        self.firstdiff2[0:-1] = self.firstdiff2[1::]
        self.firstdiff2[-1] = input - self.watch_zone[-1]
        # 更新观察窗
        self.watch_zone[0:-1] = self.watch_zone[1::]
        self.watch_zone[-1] = input

    def posGFSF(self):
        """
        计算正Gait Feature Slope Focuser。

        :return: 正Gait Feature Slope Focuser值。
        """
        GFSF = 0
        for i in self.firstdiff1:
            if i > 0:
                GFSF += i
        return GFSF

    def negGFSF(self):
        """
        计算负Gait Feature Slope Focuser。

        :return: 负Gait Feature Slope Focuser值。
        """
        GFSF = 0
        for i in self.firstdiff2:
            if i < 0:
                GFSF += i
        return GFSF

    # def HS_detect(self, negout):
    #     if negout[-1] - negout[-2] != 0 and (negout[-2] - negout[-3]) / (negout[-1] - negout[-2]) > 2 and (
    #             negout[-2] - negout[-3]) < 0 and self.HSsleepcount <= 0 and self.watch_zone[-1] < 5:
    #         self.HSsleepcount = 75
    #         return True
    #     elif negout[-1] - negout[-2] >= 0 and negout[-2] - negout[-3] < 0 and self.HSsleepcount <= 0 and \
    #             self.watch_zone[-1] < 5:
    #         # print((negout[-3] - negout[-4]) / (negout[-2] - negout[-3]))
    #         self.HSsleepcount = 75
    #         return True
    #     else:
    #         self.HSsleepcount -= 1

    # def TO_detect(self, HS):
    #     threshold = -HS

    #     if self.watch_zone[-1] > threshold \
    #             and self.watch_zone[-1] - self.watch_zone[-2] <= 0 \
    #             and self.watch_zone[-2] - self.watch_zone[-3] >= 0 \
    #             and self.TOsleepcount <= 0 \
    #             and self.watch_zone[-1] > 10:
    #         self.TOsleepcount = 50
    #         return True
    #     else:
    #         self.TOsleepcount -= 1
            
    def HS_detect_new(self, negout):
        """
        新的HS检测方法。

        :param negout: 负Feature Slope输出。
        :return: 是否检测到HS。
        """
        if self.watch_zone[-1] - self.watch_zone[-2] >= 0 and \
           self.watch_zone[-2] - self.watch_zone[-3] <= 0 and \
           self.HSsleepcount < 0 and \
           negout[-1] < -7 :
            self.HSsleepcount = 40
            return True
        else:
            self.HSsleepcount -= 1

    # def HS_detect_new(self, negout):
    #     if self.watch_zone[-1] - self.watch_zone[-2] >= 0 & self.watch_zone[-2] - self.watch_zone[-3] <= 0 and \ #出现谷值
    #     self.HSsleepcount < 0 and \ # 不再睡眠
    #     negout[-1] > 7: #上升了一段时间
    #         self.HSsleepcount = 75
    #         return True
    #     else:
    #         self.HSsleepcount -= 1

    def TO_detect_new(self, posout):
        """
        新的TO检测方法。

        :param posout: 正Feature Slope输出。
        :return: 是否检测到TO。
        """
        if self.watch_zone[-1] - self.watch_zone[-2] <= 0 and \
           self.watch_zone[-2] - self.watch_zone[-3] >= 0 and \
           self.TOsleepcount < 0 and \
           posout[-1] > 7 and self.watch_zone[-1] > 5:
            self.TOsleepcount = 40
            return True
        else:
            self.TOsleepcount -= 1


#     def TO_detect_new(self, posout):
#         if self.watch_zone[-1] - self.watch_zone[-2] <= 0 & self.watch_zone[-2] - self.watch_zone[-3] >= 0 and \ #出现峰值
#         self.TOsleepcount < 0 and \# 不再睡眠
#         posout[-1] < -7: #上升了一段时间
#             self.HSsleepcount = 75
#             return True
#         else:
#             self.TOsleepcount -= 1

######### CHANGE IN 5 5 ##########
    def STOP_detect(self, negout, posout):
        """
        检测停止状态。

        :param negout: 负Feature Slope输出。
        :param posout: 正Feature Slope输出。
        """
        if (self.watch_zone[-1] < 10) and \
        (self.watch_zone[-1] > -5)  and \
        (negout[-1] > -2) and \
        (posout[-1] < 2):
            self.stopcount += 1
            if self.stopcount > 20:
                self.stopcount = 20
        else:
            self.stopcount -= 1
            if self.stopcount < 0:
                self.stopcount = 0

    def GFSF_update_new(self,n, input):
        """
        新的更新方法，处理输入信号并更新HS和TO状态。

        :param n: 当前索引。
        :param input: 输入信号值。
        """

        self.update(input)
        self.posout.append(self.posGFSF())
        self.negout.append(self.negGFSF())

        self.STOP_detect(self.negout, self.posout)
        if self.stopcount > 10:
            self.ED[0].append(n)
            self.ED[1].append(input)

        elif self.stopcount == 10:
            self.ST[0].append(n)
            self.ST[1].append(input)

        if self.ini_state == 0 and self.HS_detect_new(self.negout):

            self.HS[0].append(n)
            self.HS[1].append(input)

        if self.ini_state == 0 and self.HS[1] and self.TO_detect_new(self.posout):
            self.TO[0].append(n)
            self.TO[1].append(input)
            
        
