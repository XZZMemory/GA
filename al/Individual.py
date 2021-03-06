import random
import copy
import math
import numpy as np


class Individual:
    # 定义高斯白噪声，查查怎么写？？
    BW = 1e-7
    '''包丢失率的阈值 9.56db'''
    dBTi = 9.56
    Ti = 10 ** (dBTi / 10)  # 9.036494737223016
    '''分贝毫瓦,可用作电压或功率单位'''
    averagePower_dbm = 40
    '''单位：瓦'''
    averagePower = 10 ** ((averagePower_dbm - 30) / 10)
    '''ei、fi包大小相关的约束，计算PER使用'''
    ei = 1
    fi = 1
    bias = 1000  # 计算误码率时的偏移量
    population = []
    # 高斯噪声
    BW = 1e7
    __N0_dbm = -174 + 10 * np.log10(BW)
    __N0 = (10 ** ((__N0_dbm - 30) / 10)) * 10
    # perFileName = "./data/picture/20190528-VQD5-2-picture.txt"

    '''个体中需要用到的：1.C、P的初始化 
                        2.个体的适应值计算
                        3.交叉 child1.crossover(child2)  return ([child1,child2])
                        4.变异 child.mutate return copyChild
                        修改:需要在初始化的时候，基站有剩余的存储容量，要存储多的视频，多存几遍视频'''
    '''初始化的时候加上population.方便传输参数'''

    def __init__(self, tau, videoBase, sumOfBase, sumOfUser, sumOfVideo,
                 sumOfChannels, powerOfBase, baseRadius, Alpha, VN,
                 basevisitedUE, distanceUserToBase, VNTimes):
        self.tau = tau
        self.sumOfBase = sumOfBase
        self.sumOfUser = sumOfUser
        self.sumOfVideo = sumOfVideo
        self.sumOfChannels = sumOfChannels
        self.VN = VN
        self.VNTimes = VNTimes
        ''' 每个基站的访问用户，在个体初始化C、P时使用'''
        self.basevisitedUE = basevisitedUE
        self.videoBase = videoBase  # 每个视频描述的存储地点
        self.powerOfBase = powerOfBase
        self.baseRadius = baseRadius
        self.Alpha = Alpha  # 计算Noise噪声参数
        self.N0 = 11
        self.Bias = 1000000  # 防止干扰和噪声过小设置的偏移值，在计算SINR之后会约掉 10^6
        self.Qmax = 1  # 实数功率等级，所以最大功率等级是1
        self.powerLimit = 0.00001  # 功率等级小于这个数就直接认为是0并且释放信道
        self.sumOfDescription = 10
        '''信道分配矩阵'''
        self.C = []
        '''功率分配矩阵'''
        self.P = []

        self.initialOfCandP()
        '''用户与基站之间的距离，用于计算SINR'''
        self.distanceUserToBase = distanceUserToBase
        self.SINR = []

    '''用户与基站之间的距离，用户计算SINR'''
    '''1.信道和功率的初始化，需要改改，2018.6.11，信道和功率的分配需要考虑实际情况，
         只有用户访问基站时，在初始化时，才会分配信道，用户不访问基站时，不分配信道
             信道初始化已完成
       2.在交叉和变异的过程中，会发生变化，不满足这个条件，需要进行修正，参考洪庭贺毕设
         中关于修正的部分，后续需要进行修正，2019.3.2不用修正了，因为适应值不好，在GA演变中会自动淘汰
    '''
    '''
    其中宏基站的最大功率设为43dBm（合20000mW），
    即P1,max = 43dbm，微微基站的最大功率设为30dBm（合1000mW），即P2,max = P3,max = … = PK,max = 30dbm。
    pn,s为基站n的信道s的功率等级，其取值为0≤pn,s≤1的实数，表示基站n的信道s占用基站最大功率的百分比。
    '''

    def initialOfCandP(self):
        cnum = 0
        for base in range(self.sumOfBase):  # 计算信道总数
            cnum = cnum + self.sumOfChannels

        p = self.sumOfUser / (cnum * self.sumOfBase)  # 依概率决定是否分配信道，概率为用户数/信道数
        for base in range(self.sumOfBase):
            chan = []  # 当前基站的信道分配
            powe = []  # 当前基站的功率分配
            wholePower = self.Qmax  # 总功率设置为Qmax功率等级
            for j in range(self.sumOfChannels):  # 循环当前基站信道个数次
                if (random.random() > p) and (len(self.basevisitedUE[base]) > 0):
                    # 如果随机数大于P,并且可选用户列表不为空，则为当前信道分配用户
                    try:
                        user = random.choice(self.basevisitedUE[base])
                        chan.append(user)  # 随机在可选用户群中选取一个用户分配给当前信道
                        wp = random.random() * (wholePower / (self.sumOfChannels - j))
                        powe.append(wp)  # 将这个功率值分配给这个信道
                        if wp == 0:
                            chan[j] = -1
                        else:
                            wholePower = wholePower - wp  # 可用功率值减少
                    except IndexError:
                        print('user序号:' + str(user))
                        if self.basevisitedUE[base] == None:
                            print("self.basevisitedUE[base]为空！")
                        else:
                            print('basevisitedUE列表:' + str(self.basevisitedUE[base]) + "length: " + str(
                                len(self.basevisitedUE[base])))
                        print('错误，列表溢出，程序终止')
                        exit(0)
                else:
                    chan.append(-1)  # 如果不分配信道，设置为-1
                    powe.append(0)  # 不用的信道功率设置为0
            self.C.append(chan)  # 当前基站的信道分配加入基因中
            self.P.append(powe)  # 当前基站的功率分配加入基因中

    '''2.交叉   从种群中随机选择两个个体，从基站1到S循环，每层产生一个随机数，随机值后的基因为交叉，对应位置交换位置，即交换两个个体的值'''

    def crossover(self, individual2):
        '''这是随机选择一个位置交换深复制，浅复制，浅复制'''
        child1 = copy.deepcopy(self)
        child2 = copy.deepcopy(individual2)
        '''交叉两个个体的功率和信道分配；对每一个基站，随机产生一个变异位（随机产生一个信道），对该信道进行交叉'''
        for base in range(self.sumOfBase):
            channel = random.randint(0, self.sumOfChannels - 1)
            for i in range(channel, self.sumOfChannels - 1):
                self.C[base][channel] = child2.C[base][channel]
                self.P[base][channel] = child2.P[base][channel]
                individual2.P[base][channel] = child1.P[base][channel]
                individual2.C[base][channel] = child1.C[base][channel]
        self.revise()
        individual2.revise()
        return [self, individual2]

    '''3.变异种群中选择一个个体，从基站1到S循环i，每层产生一个随机数j,信道j，有对应值删除，无对应值随机分配信道'''

    def mutate(self):
        '''变异，随机选择一个位置进行变异'''
        for base in range(self.sumOfBase):
            if (len(self.basevisitedUE[base]) > 0):
                channel = random.randint(0, self.sumOfChannels - 1)
                '''信道处于闲置状态，没有分配给任何用户，则随机产生一个用户，将该基站base的信道channel分配给用户usernum'''
                if (self.C[base][channel] == -1):
                    ''' random.sample()从指定的序列中随机截取指定长度的片段，不作原地修改，返回的仍是列表，不是一个单独数字'''
                    user = random.choice(self.basevisitedUE[base])
                    self.C[base][channel] = user  # 把信道随机分配给一个用户
                    if self.Qmax - sum(self.P[base]) < self.powerLimit * 100:
                        self.revisePower(base)  # 功率超了修复
                    self.P[base][channel] = random.random() * (self.Qmax - sum(self.P[base]))
                    if self.P[base][channel] == 0:
                        self.C[base][channel] = -1
                else:
                    '''非闲置状态,产生一个随机概率，概率p小于0.5，该信道置空；概率p大于0.5，随机选择一个用户，将信道、功率分配给该用户'''
                    p = random.random()
                    if (p < 0.5):
                        self.C[base][channel] = -1
                        self.P[base][channel] = 0
                    else:
                        user = random.choice(self.basevisitedUE[base])
                        self.C[base][channel] = user  # 把信道随机分配给一个用户
                        if self.Qmax - sum(self.P[base]) < self.powerLimit * 100:
                            self.revisePower(base)  # 功率超了修复
                        self.P[base][channel] = random.random() * (self.Qmax - sum(self.P[base]))
                        if self.P[base][channel] == 0:
                            self.C[base][channel] = -1

    def revisePower(self, base):
        for channel in range(len(self.P[base])):
            # 如果功率非常非常小(小于最低限度)，则直接置为0
            if self.P[base][channel] != 0 and (self.P[base][channel] / self.Qmax < self.powerLimit):
                self.C[base][channel] = -1  # 信道标注为空闲
                self.P[base][channel] = 0  # 功率标注为0
        a = sum(self.P[base])  # 该基站当前功率的总数，应该小于Qmax才对
        if a >= self.Qmax:  # 如果a超过Qmax
            for channel in range(len(self.P[base])):
                if self.P[base][channel] != 0:
                    self.P[base][channel] *= self.Qmax / a  # 按照比例减少

    def revise(self):
        for base in range(self.sumOfBase):  # 先修复一次功率,以免出现溢出
            self.revisePower(base)

    def getFitnessOfMatching(self):
        self.getPERofBaseChannelWithIntegral()  # self.asm_array 得到每个基站信道的可靠性
        self.getAns()  # self.ans 得到每个用户访问某基站的可靠性
        PER = []
        #
        for video in range(len(self.VN)):  # 视频i
            PER.append([])
            for user in range(len(self.VN[video])):
                PER[video].append(self.getUserVisitVideoDescriptionReliability(user, video) ** self.sumOfDescription)

        '''个体适应值,可靠性，越高越好'''
        fitness = 0
        for video in range(len(PER)):
            for user in range(len(PER[video])):
                fitness += PER[video][user]
        return fitness / self.VNTimes

    # 获取某一用户访问某视频描述的可靠性
    def getUserVisitVideoDescriptionReliability(self, user, video):
        userUtiltyList = [0]  # 存储该视频的基站提供的可靠性，访问可靠性最大的基站
        if self.VN[video][user] == 1:
            for storedBase in self.videoBase[video]:
                # 获取这个基站为用户提供的的可靠性
                userUtiltyList.append(self.ansArray[user][storedBase])
        return max(userUtiltyList)  # 多个基站为同一提供可靠性，选择可靠性最大的那个

    def getAns(self):
        # 得到用户与每个基站进行通信时的链路可靠性，根据每个信道的可靠性，self.C
        self.ansArray = []
        for user in range(self.sumOfUser):
            self.ansArray.append([])
            ans = 1
            for base in range(self.sumOfBase):
                ansEachBase = 1
                for channe in range(self.sumOfChannels):
                    if self.C[base][channe] == user:
                        ansEachChannel = 1 - self.asm_array[base][channe]
                        ansEachBase *= ansEachChannel
                data = ans - ansEachBase
                if data == float('inf'):
                    print(str(self.ansArray))
                    print(data)
                    exit(1)
                self.ansArray[user].append(ans - ansEachBase)

    def getPERofBaseChannelWithIntegral(self):
        # 从基站考虑，计算每个信道的可靠性
        self.asm_array = []
        for base in range(self.sumOfBase):
            self.asm_array.append([])
            for channel in range(self.sumOfChannels):
                user = self.C[base][channel]
                if user != -1:
                    s = self.P[base][channel] * self.powerOfBase[base] * ((self.distanceUserToBase[user][base]) ** (-4))
                    try:
                        asm = math.e ** (-(self.tau * self.__N0) / s)
                    except:
                        print(self.tau)
                        print(self.__N0)
                        print(s)
                        print(-(self.tau * self.__N0) / s)
                        print(str(self.P[base][channel] * self.powerOfBase[base]) + " " + str(s))
                    for otherBase in range(self.sumOfBase):
                        if otherBase != base:
                            # 当前产生干扰的基站信道，是否被占用，未被占用，则不产生干扰
                            if self.C[otherBase][channel] != -1:
                                ii = self.P[otherBase][channel] * self.powerOfBase[otherBase] * (
                                        (self.distanceUserToBase[user][otherBase]) ** (
                                    -4)) * self.tau
                                try:
                                    ivalue = s / (s + ii)
                                except Exception:
                                    print("ss:" + str(s) + " ii: " + str(ii))
                                asm = asm * ivalue

                    self.asm_array[base].append(asm)
                else:
                    self.asm_array[base].append(0)

    def printMy(self):
        self.getPERofBaseChannelWithIntegral()
        self.getAns()

        return [self.ansArray, self.asm_array]

    def getSINR(self):
        print("执行getsinr函数")
        fileName = 'sinrInGet.txt'
        f = open(fileName, 'a')
        SINR = []
        WhiteNoise = -174
        for base in range(self.sumOfBase):  # 对于所有的基站s
            SINR.append([])
            for channel in range(self.sumOfChannels):  # 对于基站s里的所有的信道m，计算信噪比，每个信道的信噪比
                user = self.C[base][channel]  # 信道分配的用户user
                '''信道没有分配给任何用户,则sinr为-1'''
                sinr = -1
                if (user != -1):
                    '''信道分配了，则需要计算SINR，计算信道功率增益， # 功率增益模型，基站到用户的距离'''
                    G = (self.distanceUserToBase[user][base]) ** (-4)
                    '''在用户k处能接受到的信号强度,信道功率×功率增益'''
                    S = self.P[base][channel] * self.powerOfBase[base] * G * self.Bias
                    I = 0
                    Noise = self.Qmax * self.powerOfBase[base] * self.Bias * (
                            self.baseRadius[base] ** (-4)) / self.Alpha  # 计算噪声
                    for otherBase in range(self.sumOfBase):
                        '''如果不是当前基站，且基站信道处于非闲置状态，即功率不是0,# 其他基站在用户user处的信道增益'''
                        if (otherBase != base) and (self.C[otherBase][channel] != -1):
                            GOther = self.distanceUserToBase[user][otherBase] ** (-4)
                            Ik = self.P[otherBase][channel] * self.powerOfBase[otherBase] * GOther * self.Bias
                            I += Ik  # 干扰相加，得到总的干扰  此处得到来自其他基站的干扰
                    sinr = S / (I + Noise)
                    if I != 0:
                        f.write("base" + str(base) + " channel" + str(channel) + "S/I" + str(
                            S / I) + "S/(I+N) " + str(
                            sinr) + "noise " + str(Noise / self.Bias) + '\n')
                    else:
                        f.write("I 0" + " S/(I+N)" + str(sinr) + " noise" + str(
                            Noise / self.Bias) + '\n')
                SINR[base].append(round(sinr, 9))
        return SINR
