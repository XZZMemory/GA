from de.MyObject import Base
from de.MyObject import Video
from de.MyObject import User
import random


class ma:
    def matching(self, baseList, videoList, C, P, userList, ):
        # 1. 初始化base和video
        # *2.  获取交换对
        # 3, 更新状态
        # end(while 无交换对)*#

        # 1. 初始化base和video
        Qmax = 2  # 每个基站最多能存储多少视频流
        baseVideo = []
        for base in range(len(baseList)):
            storedOfBase = []
            for storedVideoSum in Qmax:
                video = random.randint(0, len(videoList) - 1)
                storedOfBase.append(video)
            baseVideo.append(storedOfBase)
        # *2.  获取交换对
        for base in range(len(baseVideo)):
            self.getSwapBlock(base, baseVideo)

        i = 0

    def getSINR(self, sumOfBase, sumOfChannels):
        fileName = 'sinrInGetSINR.txt'
        f = open(fileName, 'w')
        SINR = []
        WhiteNoise = -174
        for base in range(self.sumOfBase):  # 对于    所有的基站s
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
                    # print("xii"+str(Noise))
                    for otherBase in range(self.sumOfBase):
                        '''如果不是当前基站，且基站信道处于非闲置状态，即功率不是0,# 其他基站在用户user处的信道增益'''
                        if (otherBase != base) and (self.C[otherBase][channel] != -1):
                            GOther = self.distanceUserToBase[user][otherBase] ** (-4)
                            Ik = self.P[otherBase][channel] * self.powerOfBase[otherBase] * GOther * self.Bias
                            I += Ik  # 干扰相加，得到总的干扰  此处得到来自其他基站的干扰
                    sinr = S / (I + Noise)
                    # print("基站： "+str(base)+" 信道："+str(channel)+" 噪声："+str(Noise)+" 干扰： "+str(I)+" 该信道信号大小：： "+str(S)+" 信噪比： "+str(sinr))

                SINR[base].append(round(sinr, 9))
        f.write(str(SINR) + '\n')
        for i in range(len(SINR)):
            f.write(str(SINR[i]) + '\n')
        f.write('\n')
        return SINR

    # 对于基站而言，是否可以交换,找到交换对
    def getSwapBlock(self, base, baseVideo):
        videoList = baseVideo[base]
        for currentBase in range(len(baseVideo)):
            if currentBase != base:
                currentBaseVideoList = baseVideo[currentBase]
                for videoFlag in range(len(videoList)):
                    i = 0
