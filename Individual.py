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
    __N0 = 10 ** ((__N0_dbm - 30) / 10)
    # perFileName = "./data/picture/20190528-VQD5-2-picture.txt"

    '''个体中需要用到的：1.C、P的初始化 
                        2.个体的适应值计算
                        3.交叉 child1.crossover(child2)  return ([child1,child2])
                        4.变异 child.mutate return copyChild
                        修改:需要在初始化的时候，基站有剩余的存储容量，要存储多的视频，多存几遍视频'''
    '''初始化的时候加上population.方便传输参数'''

    def __init__(self, population, typeOfVQD):
        self.tau = population.tau
        self.population = population
        '''（--------以下均是拷贝种群参数信息------'''
        self.locationOfBase = copy.deepcopy(population.locationOfBase)  # 拷贝基站和用户的坐标位置
        self.locationOfUser = copy.deepcopy(population.locationOfUser)
        self.sumOfBase = population.sumOfBase
        self.sumOfUser = population.sumOfUser
        self.sumOfVideo = population.sumOfVideo
        self.sumOfChannels = population.sumOfChannels
        self.VN = population.VN
        ''' 每个基站的访问用户，在个体初始化C、P时使用'''
        self.basevisitedUE = population.basevisitedUE
        # print("basevisitedUE: "+str(self.basevisitedUE))
        ''' 每个视频描述的存储地点'''
        self.VQD = population.VQD
        self.powerOfBase = population.powerOfBase
        self.baseRadius = population.baseRadius
        self.Alpha = population.Alpha  # 计算噪声参数
        '''视频的存储方式'''
        self.typeOfVQD = typeOfVQD
        if self.typeOfVQD == 4 or self.typeOfVQD == 5:
            self.baseVisitedOfUserVisitingVideo = population.baseVisitedOfUserVisitingVideo
        # --------拷贝种群信息结束-----------）
        self.N0 = 11
        self.Bias = 1000000  # 防止干扰和噪声过小设置的偏移值，在计算SINR之后会约掉 10^6
        self.Qmax = 1  # 实数功率等级，所以最大功率等级是1
        self.powerLimit = 0.00001  # 功率等级小于这个数就直接认为是0并且释放信道
        '''信道分配矩阵'''
        self.C = []
        '''功率分配矩阵'''
        self.P = []

        self.initialOfCandP()
        '''用户与基站之间的距离，用于计算SINR'''
        self.distanceUserToBase = self.getDistanceUserToBase()
        self.SINR = []

    '''用户与基站之间的距离，用户计算SINR'''

    def getDistanceUserToBase(self):
        distance = []
        for user in range(self.sumOfUser):
            distance.append([])
            for base in range(self.sumOfBase):
                n = ((self.locationOfUser[user][0] - self.locationOfBase[base][0]) ** 2 + (
                        self.locationOfUser[user][1] - self.locationOfBase[base][1]) ** 2) ** 0.5
                distance[user].append(int(n))
        return distance

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
                        # wp = random.randint(2,int(wholePower/(self.BS[i].chaNum-j)*0.6))-1  #随机生成一个功率值(1到剩余功率的50%+1)
                        wp = random.random() * (wholePower / (
                                self.sumOfChannels - j))  # -----------2017.06.08修改功率等级为实数
                        powe.append(wp)  # 将这个功率值分配给这个信道
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
            '''
            2019.4.25删掉，之前没有宏基站，所以在交叉变异时，各个基站的功率是可以交叉的，但是网络拓扑结构发生变化，有宏基站了，所以将功率变为一个实数，可以交叉变异
                        for channel in range(self.sumOfChannels):  # 信道分配给哪个用户传输,这个信道分配的功率是多少
                posibility = random.random()
                #信道分配用户
                if ((posibility>p) and (len(self.basevisitedUE[base]) != 0)):
                    #从基站的访问用户中随机选择一个用户分配信道,
                    random.sample()从指定的序列中随机截取指定长度的片段，不作原地修改，返回的仍是列表，不是一个单独数字
                    user = random.sample(self.basevisitedUE[base], 1)[0]
                    self.C[base].append(user)
                    self.P[base].append((random.randint(20, 35)))
                else:
                   #信道不分配
                    self.C[base].append(-1)
                    self.P[base].append(0)
            '''

    '''
            初始化信道分配和功率分配

            功率分配的从1开始有点太少了，应该计算出一个最小功率
            '''
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
        flag = 0
        for base in range(self.sumOfBase):
            if (len(self.basevisitedUE[base]) > 0):
                channel = random.randint(0, self.sumOfChannels - 1)
                '''信道处于闲置状态，没有分配给任何用户，则随机产生一个用户，将该基站base的信道channel分配给用户usernum'''
                if (self.C[base][channel] == -1):
                    ''' random.sample()从指定的序列中随机截取指定长度的片段，不作原地修改，返回的仍是列表，不是一个单独数字'''
                    if flag == 0:
                        print("发生变异")
                        flag = 1
                    user = (random.sample(self.basevisitedUE[base], 1))[0]
                    self.C[base][channel] = user  # 把信道随机分配给一个用户
                    if self.Qmax - sum(self.P[base]) < self.powerLimit * 100:  # ---------2017.07.24修改为0，如果功率溢出就修复
                        self.revisePower(base)  # 功率超了修复
                    self.P[base][channel] = random.random() * (self.Qmax - sum(
                        self.P[base]))  # -----------------------------------------------------2017.06.08功率等级修改为实数
                else:
                    '''非闲置状态,产生一个随机概率，概率p小于0.5，该信道置空；概率p大于0.5，随机选择一个用户，将信道、功率分配给该用户'''
                    p = random.random()
                    if (p < 0.5):
                        if flag == 0:
                            print("发生变异")
                            flag = 1
                        self.C[base][channel] = -1
                        self.P[base][channel] = 0
                    else:
                        ''' random.sample()从指定的序列中随机截取指定长度的片段，不作原地修改，返回的仍是列表，不是一个单独数字'''
                        user = (random.sample(self.basevisitedUE[base], 1))[0]
                        self.C[base][channel] = user  # 把信道随机分配给一个用户
                        if self.Qmax - sum(self.P[
                                               base]) < self.powerLimit * 100:  # -----------------------------------------------------------2017.07.24修改为0，如果功率溢出就修复
                            self.revisePower(base)  # 功率超了修复
                        self.P[base][channel] = random.random() * (self.Qmax - sum(
                            self.P[base]))  # -----------------------------------------------------2017.06.08功率等级修改为实数

    def revisePower(self, base):
        '''
         try:
            print("功率修复：" + str(base) + " 总功率值： " + str(sum(self.P[base])) + " 该基站的功率分配情况：" + str(self.P[base]))
        except IndexError:
            print("基站："+str(base))
            print("该基站信道分配情况："+str(self.P[base]))
        '''

        for channel in range(len(self.P[base])):
            # 如果功率非常非常小(小于最低限度)，则直接置为0
            if self.P[base][channel] != 0 and self.P[base][channel] / self.Qmax < self.powerLimit:
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

    def getFitness(self):
        fileName = "sinr.txt"
        print("执行getFitness函数")
        self.SINR = self.getSINR()
        f = open(fileName, 'w')
        f.write(str(self.SINR) + '\n')
        for i in range(len(self.SINR)):
            f.write(str(self.SINR[i]) + '\n')
        f.write('\n')
        '''
        计算用户n使用基站n的信道m访问基站n中的视频v的描述q的误码率
        每个视频描述的误码率
        误码率，是一个数组，只要用户访问这个视频了，就需要计算对于这个用户来说，整个视频描述的误码率
        用户不访问视频，误码率为0.用户访问视频，误码率为0-1
        '''
        PER = []
        for video in range(len(self.VN)):  # 视频i
            PER.append([])
            if self.typeOfVQD == 4 or self.typeOfVQD == 5:
                for user in range(len(self.VN[video])):
                    PER[video].append(self.getPEROfVQD45(user, video))
            elif self.typeOfVQD == 1 or self.typeOfVQD == 2 or self.typeOfVQD == 3:
                for user in range(len(self.VN[video])):
                    PER[video].append(self.getPEROfVQD123(user, video))
        '''个体适应值/误码率，fitness，越小越好'''
        fitness = 0
        for video in range(len(PER)):
            for user in range(len(PER[video])):
                fitness += PER[video][user]
        '''为了符合遗传算法的演进规则，即：个体适应值越大。越容易存活，将适应值变为负数，满足GA算法演进规则'''
        return -fitness

    # 这时候计算出来的就是信道的可靠性，不用求反
    def getFitnessWithIntegral(self):
        # self.SINR = self.getSINR()
        self.asm_array = self.getPERofBaseChannelWithIntegral()
        self.ans = self.getAns()
        PER = []
        for video in range(len(self.VN)):  # 视频i
            PER.append([])
            if self.typeOfVQD == 4 or self.typeOfVQD == 5:
                for user in range(len(self.VN[video])):
                    PER[video].append(self.getPEROfVNWithIntegralOfVQD45(user, video))
            elif self.typeOfVQD == 1 or self.typeOfVQD == 2 or self.typeOfVQD == 3:
                for user in range(len(self.VN[video])):
                    PER[video].append(self.getPEROfVNWithIntegralOfVQD123(user, video))
        '''个体适应值,可靠性，越高越好'''
        fitness = 0
        for video in range(len(PER)):
            for user in range(len(PER[video])):
                fitness += PER[video][user]
        return fitness
        '''
        计算用户n使用基站n的信道m访问基站n中的视频v的描述q的误码率
        每个视频描述的误码率
        误码率，是一个数组，只要用户访问这个视频了，就需要计算对于这个用户来说，整个视频描述的误码率
        用户不访问视频，误码率为0.用户访问视频，误码率为0-1
        '''
        PER = []
        for video in range(len(self.VN)):  # 视频i
            PER.append([])
            if self.typeOfVQD == 4 or self.typeOfVQD == 5:
                for user in range(len(self.VN[video])):
                    PER[video].append(self.getPEROfVNWithIntegralOfVQD45(user, video))
            elif self.typeOfVQD == 1 or self.typeOfVQD == 2 or self.typeOfVQD == 3:
                for user in range(len(self.VN[video])):
                    PER[video].append(self.getPEROfVQD123(user, video))
        '''个体适应值/误码率，fitness，越小越好'''
        fitness = 0
        for video in range(len(PER)):
            for user in range(len(PER[video])):
                fitness += PER[video][user]
        '''为了符合遗传算法的演进规则，即：个体适应值越大。越容易存活，将适应值变为负数，满足GA算法演进规则'''
        return -fitness

    '''user访问视频video的误码率'''

    def getPEROfVQD123(self, user, video):
        pnv = 1
        '''用户访问视频时，需要计算失真'''
        if self.VN[video][user] == 1:
            '''找到视频video的存储基站，到存储基站中找到信道误码率,有多个描述'''
            # 当前描述的存储位置只有一个，是确定的
            for base in self.VQD[video]:
                '''video的第q个描述，在同一基站使用多条信道，考虑频谱聚合技术'''
                uniSinr = 0
                for channel in range(len(self.P[base])):
                    if self.C[base][channel] == user:
                        uniSinr += self.SINR[base][channel]  # 使用频谱聚合技术
                pnvq = 1
                if uniSinr > self.Ti:
                    pnvq = self.ei * math.e ** (-(self.fi * uniSinr))  # 如果sinr大于sinr门限值，用公式误码率，如果小于则误码率直接为1
                # 基站s使用信道m给用户n传输数据 ei、fi包大小相关约束
                pnsvq = 0
                pnv *= pnvq  # 多个描述，每个描述都要求误码率
        else:
            pnv = 0
        return pnv

    '''user访问视频video的误码率'''

    def getPEROfVQD45(self, user, video):
        Pnv = 1
        self.baseVisitedOfUserVisitingVideo  # 用户-视频-描述
        '''用户访问这个视频了，需要计算失真'''
        if self.VN[video][user] == 1:
            '''找user访问video的描述description时，访问的基站，去哪个基站找这个视频'''
            for decsription in range(len(self.VQD[video])):
                visitedBase = (np.array(self.baseVisitedOfUserVisitingVideo))[user][video][decsription]
                ''' video的第q个描述，在同一基站使用多条信道，考虑频谱聚合技术'''
                Pnvq = 1
                uniSinr = 0
                for channel in range(len(self.P[visitedBase])):
                    if self.C[visitedBase][channel] == user:
                        uniSinr += self.SINR[visitedBase][channel]  # 频谱聚合技术
                '''如果sinr大于sinr的门限值，用公式误码率，如果小于则误码率直接为1'''
                if uniSinr > self.Ti:
                    # 基站s使用（频谱聚合技术）信道联合信道m给用户n传输数据 ei、fi包大小相关约束
                    Pnvq = self.ei * math.e ** (-(self.fi * uniSinr))
                Pnv *= Pnvq  # 多个描述，每个描述都要求误码率
        else:
            Pnv = 0
        return Pnv

    def getAns(self):
        # 得到用户与每个基站进行通信时的链路可靠性，根据每个信道的可靠性，self.C
        ansArray = []
        for user in range(self.sumOfUser):
            ansArray.append([])
            ans = 1
            for base in range(self.sumOfBase):
                ansEachBase = 1
                for channe in range(self.sumOfChannels):
                    if self.C[base][channe] == user:
                        ansEachChannel = 1 - self.asm_array[base][channe]
                        ansEachBase *= ansEachChannel
                ansArray[user].append(ans - ansEachBase)
        return ansArray

    def getPEROfVNWithIntegralOfVQD123(self, user, video):
        if self.VN[video][user] == 1:
            pnv = 1
            for visitedBase in self.VQD[video]:
                '''video的第q个描述，存储基站是visitedBase'''
                Pnvq = self.ans[user][visitedBase]
                pnv = pnv * Pnvq
        else:
            pnv = 0
        return pnv

    def getPEROfVNWithIntegralOfVQD45(self, user, video):
        ''' self.SINR = self.getSINR()
        self.asm_array = self.getPERofBaseChannelWithIntegral()
        self.ans = self.getAns(self.asm_array)'''
        Pnv = 1
        if self.VN[video][user] == 1:
            '''找user访问video的描述description时，访问的基站，去哪个基站找这个视频'''
            for decsription in range(len(self.VQD[video])):
                visitedBase = (np.array(self.baseVisitedOfUserVisitingVideo))[user][video][decsription]
                Pnvq = self.ans[user][visitedBase]
                Pnv *= Pnvq  # 多个描述，每个描述都要求误码率
        else:
            Pnv = 0
        return Pnv

    def getPERofBaseChannelWithIntegral(self):
        # 从基站考虑，计算每个信道的可靠性
        asm_array = []
        for base in range(self.sumOfBase):
            asm_array.append([])
            for channel in range(self.sumOfChannels):
                user = self.C[base][channel]
                if user != -1:
                    ss = self.P[base][channel] * self.powerOfBase[base] * (
                            (self.distanceUserToBase[user][base]) ** (-4))
                    try:
                        asm = math.e ** (-(self.tau * self.__N0) / ss)
                    except:
                        print(str(self.P[base][channel] * self.powerOfBase[base]) + " " + str(ss))
                    for otherBase in range(self.sumOfBase):
                        if otherBase != base:
                            # 当前产生干扰的基站信道，是否被占用，未被占用，则不产生干扰
                            if self.C[otherBase][channel] != -1:
                                ii = self.P[otherBase][channel] * self.powerOfBase[otherBase] * (
                                        (self.distanceUserToBase[user][otherBase]) ** (-4)) * self.tau
                                try:
                                    ivalue = ss / (ss + ii)
                                except Exception:
                                    print("ss:" + str(ss) + " ii: " + str(ii))
                                asm = asm * ivalue

                    asm_array[base].append(asm)
                else:
                    asm_array[base].append(0)
        return asm_array

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
                    # print("基站： "+str(base)+" 信道："+str(channel)+" 噪声："+str(Noise)+" 干扰： "+str(I)+" 该信道信号大小：： "+str(S)+" 信噪比： "+str(sinr))
                    if I != 0:
                        f.write("base" + str(base) + " channel" + str(channel) + "S/I" + str(
                            S / I) + "S/(I+N) " + str(
                            sinr) + "noise " + str(Noise / self.Bias) + '\n')
                    else:
                        f.write("I 0" + " S/(I+N)" + str(sinr) + " noise" + str(
                            Noise / self.Bias) + '\n')
                SINR[base].append(round(sinr, 9))
        return SINR
