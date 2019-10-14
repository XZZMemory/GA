import random
import math
from random import choice
import numpy as np
import Utils


# 求user访问视频的可靠性大小，每个描述均存在同一位置，直接a的b次方得到结果

# *在matching过程中，基站信道可靠性未发生变化，基站访问用户也未发生变化，所以*#
class Matching:
    # k考虑将这些通用信息放到一个配置文件中
    sumOfBase = 7
    sumOfUser = 20
    sumOfVideo = 4
    sumOfDescription = 10  # 视频描述的数量，视频描述的大小默认是5
    sumOfChannels = 20
    matchingTimes = 0  # 记录成功执行了多少次matching
    Qmax = 1  # 实数功率等级，所以最大功率等级是1

    '''信道分配矩阵'''
    C = []
    '''功率分配矩阵'''
    P = []
    BW = 1e7
    __N0_dbm = -174 + 10 * np.log10(BW)
    __N0 = 10 ** ((__N0_dbm - 30) / 10)
    tau = 1  # 计算信道可靠性时使用
    flag = 1  # 标识是否有交换块，matching算法种终止条件，当没有交换块时，flag=0，matching算法结束

    # 基站存储容量，宏基站：4，微基站：1个
    baseCapacity = []
    baseCapacity.append(4)
    for i in range(sumOfBase - 1):
        baseCapacity.append(1)
    powerOfBase = []
    for i in range(sumOfBase):
        if i == 0:
            powerOfBase.append(20000)
        else:
            powerOfBase.append(1000)

    # 不传输个体了，不然还要有VQD的type等，很麻烦
    def __init__(self):
        configPath = './config.txt'
        self.processing(configPath)  # 读取配置信息
        # 这个在初始化时就固定了，不会发生变化，一直就是这个，所以放在这里
        self.distanceUserToBase = self.getDistanceUserToBase()
        self.init(None, None)

    # 读取配置文件信息
    def processing(self, configPath):
        times = 1
        with open(configPath) as file_object:
            for line in file_object:
                if times == 1:
                    self.locationOfBase = eval(line)
                elif times == 2:
                    self.locationOfUser = eval(line)
                elif times == 3:
                    self.VN = eval(line)
                times = times + 1
        self.VNTimes = Utils.printListWithTwoDi(str(self.VN), self.VN)

    # 初始化C、P，确定base和video的映射关系
    def init(self, C, P):
        # 程序刚开始，没有C和P的话，需要初始化一个，如果经过GA算法，有了C和P，则不用再初始化了
        if C == None:
            self.initOfCAndP()
        else:
            self.C = C
            self.P = P
        # 2. 确定的映射关系
        # 随机产生video和base对应关系，即：matching初始状态是随机产生的
        # 随机初始化映射关系：
        self.initMappingOfMatching()
        # 3. 获取用户访问基站时的可靠性
        self.asm_array = self.getPERofBaseChannelWithIntegral()  # 基站每个信道的可靠性
        self.printData("asm_array", self.asm_array)
        self.ansArray = self.getAns()  # 获取每个用户访问基站时，基站为用户提供的可靠性
        self.printData("ansArray", self.ansArray)

    def printData(self, name, data):
        print("执行print函数" + name)
        for i in range(len(data)):
            print(str(i) + ": " + str(data[i]))

    # 随机初始化映射关系：
    def initMappingOfMatching(self):
        # 2. 确定的映射关系
        # 随机产生video和base对应关系，即：matching初始状态是随机产生的
        # 随机初始化映射关系：
        # 对每个基站随机产生存储基站
        self.restOfBaseCapacity = self.baseCapacity  # 每个基站存储容量状态
        self.baseVideo = []  # 每个基站存储的视频
        self.videoBase = []  # 每个视频存储在哪些基站上
        for video in range(self.sumOfVideo):
            self.videoBase.append([])
        for base in range(self.sumOfBase):
            self.baseVideo.append([])
        for base in range(self.sumOfBase):
            # 用于随机产生基站存储视频
            videoList = []
            for video in range(self.sumOfVideo):
                videoList.append(video)
            # print("matching随机初始化，随机产生" + str(videoList))
            # print("存储容量" + str(base) + " " + str(self.baseCapacity[base]))
            for currentTime in range(self.baseCapacity[base]):
                # 初始化时，有些基站是存不满的，有空闲资源块
                if (random.random() > 0.2):
                    # 当前基站存储的视频：currentVideo
                    currentVideo = choice(videoList)
                    # 存储匹配状态
                    self.baseVideo[base].append(currentVideo)
                    self.videoBase[currentVideo].append(base)
                    videoList.remove(currentVideo)
                    self.restOfBaseCapacity[base] = self.restOfBaseCapacity[base] - 1

        self.printData("videoBase初始化", self.videoBase)
        self.printData("baseVideo初始化", self.baseVideo)

    # 在程序启动时，没有C和P，随机初始化一个C和P
    def initOfCAndP(self):
        # 初始化，分配C和P
        # 1. 初始化C、P
        # 1. 访问用户列表

        basevisitedUE = []
        # 2. 对每个基站，随机产生访问用户
        for base in range(self.sumOfBase):
            userList = []
            for user in range(self.sumOfUser):
                userList.append(user)
            length = len(userList)
            basevisitedUE.append([])
            baseVisitedUserSum = np.random.randint(int(length / 3), length + 1, 1)[0]  # 随机生成基站访问用户数量
            print("baseVisitedUserSum:" + str(baseVisitedUserSum))
            for userFlag in range(baseVisitedUserSum):
                user = choice(userList)
                userList.remove(user)
                basevisitedUE[base].append(user)
        self.basevisitedUE = basevisitedUE
        # 3. 获得了每个基站的访问用户（随机产生的访问用户），则初始化，分配C和P
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
        print("初始化，基因分配")
        for base in range(self.sumOfBase):
            print(str(base) + " : " + str(self.C[base]))
        print("P")
        for base in range(self.sumOfBase):
            print(str(base) + " : " + str(self.P[base]))

    def matching(self):
        fitnessFileName = 'fitness.txt'
        ff = open(fitnessFileName, 'w')
        ff.write(str(self.getFitnessOfMatching() / self.VNTimes) + '\n')
        # 1. 初始化base和video self.init()
        # *2.  获取交换对  执行matching算法
        # 3, 更新状态
        # end(while 无交换对)*#
        print("初始状态")
        self.printData("videoBase:", self.videoBase)
        self.printData("baseVideo", self.baseVideo)
        fileName = './result.txt'
        f = open(fileName, 'w')
        self.writeFile(f, "videoBase", self.videoBase)
        self.writeFile(f, "baseVideo", self.baseVideo)
        while self.flag == 1:
            if self.getSwapBlock(f) == 1:
                f.write("matching successfully matching times:" + str(self.matchingTimes) + '\n')
                break

        print("matchingTimes:" + str(self.matchingTimes))
        f.write("matchingTimes:" + str(self.matchingTimes) + '\n')
        print("结束状态")
        self.printData("videoBase:", self.videoBase)
        self.printData("baseVideo", self.baseVideo)
        self.writeFile(f, "videoBase", self.videoBase)
        self.writeFile(f, "baseVideo", self.baseVideo)
        ff.write(str(self.getFitnessOfMatching() / self.VNTimes) + '\n')

    def writeFile(self, f, name, data):
        f.write(name + '\n')
        for i in range(len(data)):
            f.write(str(i) + ":  " + str(data[i]) + '\n')

    # 计算用户到基站的距离
    def getDistanceUserToBase(self):
        distance = []
        for user in range(self.sumOfUser):
            distance.append([])
            for base in range(self.sumOfBase):
                n = ((self.locationOfUser[user][0] - self.locationOfBase[base][0]) ** 2 + (
                        self.locationOfUser[user][1] - self.locationOfBase[base][1]) ** 2) ** 0.5
                distance[user].append(int(n))
        return distance

    # 每个基站信道的可靠性，在matching过程中，基站信道可靠性一直没变化，基站访问用户也未发生变化
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

    # 得到用户与每个基站进行通信时的链路可靠性，根据每个信道的可靠性，self.C。横-用户，纵-基站
    def getAns(self):
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

    # 获取当前基站的功效函数
    # 基站功效函数，基站为这些访问用户所能提供的可靠性
    def baseUtilty(self, base):
        # * 1.基站访问用户
        # 2. 基站存储视频，
        # 3. 用户与视频访问关系
        # 4. 基站信道可靠性-> 用户访问基站时，提供的可靠性*#
        anv = 0  # 基站的功效值
        visitedUserList = self.C[base]  # 基站信道分配的访问用户，有重复元素，因为一个基站的多个信道可以分配给同一用户
        stordedVideoList = self.baseVideo[base]
        list2 = list(set(visitedUserList))  # 基站访问用户
        for user in list2:
            for video in stordedVideoList:
                if self.VN[video][user] == 1:
                    anv = anv + self.ansArray[user][base]

        return anv

    # 获取当前视频的功效函数，考虑，与以前不同，多个基站为同一视频提供可靠性
    def videoUtilty(self, video):
        # *1. 视频的所有访问用户 self.VN
        # 2. 视频的访问基站 self.videoBase[video]
        # 3.  *#
        totalUtilty = 0
        # 多个基站为同一提供可靠性，选择可靠性最大的那个
        for user in range(len(self.VN[video])):
            totalUtilty = totalUtilty + self.getUserVisitVideoDescriptionReliability(user, video)
        return totalUtilty

    # 获取某一用户访问某视频描述的可靠性,
    def getUserVisitVideoDescriptionReliability(self, user, video):
        userUtiltyList = [0]  # 存储该视频的基站提供的可靠性，访问可靠性最大的基站
        if self.VN[video][user] == 1:
            for storedBase in self.videoBase[video]:
                # 获取这个基站为用户提供的的可靠性
                userUtiltyList.append(self.ansArray[user][storedBase])
        return max(userUtiltyList)  # 多个基站为同一提供可靠性，选择可靠性最大的那个

    # 对于视频而言，是否可以交换,找到交换对
    # 对于某一视频而言找交换对,video-anotherVideo,base1-base2，有四种情况，分别讨论
    def getSwapBlock(self, f):
        self.printData("videoBase:", self.videoBase)
        self.printData("baseVideo", self.baseVideo)
        # 1. 交换已匹配资源
        for video1 in range(self.sumOfVideo):
            baseList = self.videoBase[video1]
            initialV1Utilty = self.videoUtilty(video1)
            for video2 in range(video1 + 1, self.sumOfVideo):
                print("*********************" + str(video1) + " " + str(video2))
                initialV2Utilty = self.videoUtilty(video2)
                anotherBaseList = self.videoBase[video2]
                print("videoBase: " + str(video1) + ": ", baseList)
                print("anotherBaseList: " + str(video2) + ": ", anotherBaseList)

                # 求差，看能否交换，或者，video和空的基站交换
                # A-B
                differVideoList1 = [item for item in baseList if item not in anotherBaseList]
                print("differVideoList1: " + str(differVideoList1))
                # B-A
                differVideolist2 = [item for item in anotherBaseList if item not in baseList]
                print("differVideoList2: " + str(differVideolist2))
                # 交换已匹配资源对应的资源，看是否形成交换块
                for base1 in differVideoList1:
                    for base2 in differVideolist2:
                        print("执行交换操作之前")
                        print("videoBase " + str(video1) + ": ", self.videoBase[video1])
                        print("videoBase " + str(video2) + ": ", self.videoBase[video2])
                        print("baseVideo " + str(base1) + ": ", self.baseVideo[base1])
                        print("baseVideo " + str(base2) + ": ", self.baseVideo[base2])

                        initialBase1Utilty = self.baseUtilty(base1)
                        initialBase2Utilty = self.baseUtilty(base2)
                        print(str(video1) + " " + str(base1) + " " + str(video2) + " " + str(base2))
                        self.swapBase(video1, base1, video2, base2)
                        # 看四者的功效函数是否都大于等于并
                        differ1 = self.videoUtilty(video1) - initialV1Utilty
                        differ2 = self.videoUtilty(video2) - initialV2Utilty
                        differ3 = self.baseUtilty(base1) - initialBase1Utilty
                        differ4 = self.baseUtilty(base2) - initialBase2Utilty
                        totalDiffer = differ1 + differ2 + differ3 + differ4
                        # 形成交换对了，直接返回
                        if differ1 >= 0 and differ2 >= 0 and differ3 >= 0 and differ4 >= 0 and totalDiffer > 0:
                            self.flag = 1
                            self.matchingTimes = self.matchingTimes + 1
                            f.write(
                                "matching success " + str(video1) + " " + str(video2) + " " + str(base1) + " " + str(
                                    base2) + '\n')
                            self.writeFile(f, "videoBase", self.videoBase)
                            self.writeFile(f, "baseVideo", self.baseVideo)
                            return 1
                        # 不能形成交换块，返回初始状态，并继续判断下一个
                        else:
                            print("未形成交换块，回到初始状态")
                            self.swapBase(video1, base2, video2, base1)
                            self.flag = 0
                # 看是否可交换了，或者有个基站有空闲资源,考虑空闲资源块
        # 2. 抢夺已匹配基站,video1 抢夺vidoe2的 base1
        for video1 in range(self.sumOfVideo):
            initialV1Utilty = self.videoUtilty(video1)
            for video2 in range(self.sumOfVideo):
                if video1 != video2:
                    initialV2Utilty = self.videoUtilty(video2)
                    print("videoBase: " + str(video1) + ": ", baseList)
                    print("anotherBaseList: " + str(video2) + ": ", anotherBaseList)
                    # B-A
                    differVideolist2 = [item for item in self.videoBase[video2] if item not in self.videoBase[video1]]
                    print("differVideoList2: " + str(differVideolist2))
                    # 交换已匹配资源对应的资源，看是否形成交换块
                    for base2 in differVideolist2:
                        print("执行交换操作之前")
                        print("videoBase " + str(video1) + ": ", self.videoBase[video1])
                        print("videoBase " + str(video2) + ": ", self.videoBase[video2])
                        print("baseVideo " + str(base2) + ": ", self.baseVideo[base2])
                        initialBase2Utilty = self.baseUtilty(base2)
                        print(str(video1) + " " + str(video2) + " " + str(base2))
                        self.snatchDistributedBase(video1, video2, base2)
                        # 看四者的功效函数是否都大于等于并
                        differ1 = self.videoUtilty(video1) - initialV1Utilty
                        differ2 = self.videoUtilty(video2) - initialV2Utilty
                        differ4 = self.baseUtilty(base2) - initialBase2Utilty
                        totalDiffer = differ1 + differ2 + differ4
                        # 形成交换对了，直接返回
                        if differ1 >= 0 and differ2 >= 0 and differ4 >= 0 and totalDiffer > 0:
                            self.flag = 1
                            self.matchingTimes = self.matchingTimes + 1
                            f.write(
                                "matching success " + str(video1) + " " + str(video2) + " " + str(base2) + '\n')
                            self.writeFile(f, "videoBase", self.videoBase)
                            self.writeFile(f, "baseVideo", self.baseVideo)
                            return 1
                        # 不能形成交换块，返回初始状态，并继续判断下一个
                        else:
                            print("未形成交换块，回到初始状态")
                            self.snatchDistributedBase(video2, video1, base2)
                            self.flag = 0

                    # 看是否可交换了，或者有个基站有空闲资源,考虑空闲资源块
        # 4. 抢夺未匹配资源
        # 看是否有可用基站，形成交换块，或抢夺或交换，有两种
        for video1 in range(self.sumOfVideo):
            initialV1Utilty = self.videoUtilty(video1)
            print("videoBase: " + str(video1) + ": ", baseList)
            exchangeableBaseList = self.getExchangeableBaselist(video1)
            for base in exchangeableBaseList:
                initialBaseUtilty = self.baseUtilty(base)
                self.useAvaiableBase(video1, base)
                differ1 = self.videoUtilty(video1) - initialV1Utilty
                differ2 = self.baseUtilty(base) - initialBaseUtilty
                totalDiffer = differ1 + differ2
                if differ1 >= 0 and differ2 >= 0 and totalDiffer > 0:
                    self.matchingTimes = self.matchingTimes + 1
                    self.flag = 1
                    f.write("matching  aviable success" + str(video1) + "  " + str(base) + '\n')
                    self.writeFile(f, "videoBase", self.videoBase)
                    self.writeFile(f, "baseVideo", self.baseVideo)
                    return 1
                    # 不能形成交换块，返回初始状态，并继续判断下一个
                else:
                    self.deuseAvaiableBase(video1, base)

        # 3. 交换未匹配资源
        for video1 in range(self.sumOfVideo):
            initialV1Utilty = self.videoUtilty(video1)
            baseList = self.videoBase[video1]
            print("videoBase: " + str(video1) + ": ", baseList)
            # 也是求二者的差集
            exchangeableBaseList = self.getExchangeableBaselist(video1)
            differVideolist1 = [item for item in self.videoBase[video1] if item not in exchangeableBaseList]
            # 使用base2，不使用base1
            for base1 in differVideolist1:
                for base2 in exchangeableBaseList:
                    initialBase1Utilty = self.baseUtilty(base1)
                    initialBase2Utilty = self.baseUtilty(base2)
                    self.useAvaiableBase(video1, base2)
                    self.deuseAvaiableBase(video1, base1)
                    differ1 = self.videoUtilty(video1) - initialV1Utilty
                    differ2 = self.baseUtilty(base) - initialBaseUtilty
                    totalDiffer = differ1 + differ2
                    if differ1 >= 0 and differ2 >= 0 and totalDiffer > 0:
                        self.matchingTimes = self.matchingTimes + 1
                        self.flag = 1
                        f.write("matching  aviable success" + str(video1) + "  " + str(base) + '\n')
                        self.writeFile(f, "videoBase", self.videoBase)
                        self.writeFile(f, "baseVideo", self.baseVideo)
                        return 1
                        # 不能形成交换块，返回初始状态，并继续判断下一个
                    else:
                        self.deuseAvaiableBase(video1, base)

        self.flag = 0
        return 0

    def getFitnessOfMatching(self):
        # self.SINR = self.getSINR()
        # 在执行初始化时已得到该值
        # self.asm_array = self.getPERofBaseChannelWithIntegral()  # 得到每个基站信道的可靠性
        # self.ansArray = self.getAns()  # 得到每个用户访问某基站的可靠性
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
        return fitness

    def getPEROfVQDMatching(self, user, video):
        ''' self.SINR = self.getSINR()
               self.asm_array = self.getPERofBaseChannelWithIntegral()
               self.ans = self.getAns(self.asm_array)'''
        Pnv = 1
        if self.VN[video][user] == 1:
            '''找user访问video的描述description时，访问的基站，去哪个基站找这个视频'''
            for decsription in range(len(self.VQD[video])):
                visitedBase = (np.array(self.baseVisitedOfUserVisitingVideo))[user][video][decsription]
                Pnvq = self.ansArray[user][visitedBase]
                Pnv *= Pnvq  # 多个描述，每个描述都要求误码率
        else:
            Pnv = 0
        return Pnv

        def printdataFirst(self, name, data):
            print(name)
            print(str(data))

    # 交换video对应的base
    # video、base对应存储的基站、视频也要变化
    def swapBase(self, video1, base1, video2, base2):
        self.videoBase[video1].remove(base1)
        self.videoBase[video1].append(base2)
        self.videoBase[video2].remove(base2)
        self.videoBase[video2].append(base1)
        self.baseVideo[base1].remove(video1)
        self.baseVideo[base1].append(video2)
        self.baseVideo[base2].remove(video2)
        self.baseVideo[base2].append(video1)
        print("------执行交换操作之后")
        print("videoBase " + str(video1) + ": ", self.videoBase[video1])
        print("videoBase " + str(video2) + ": ", self.videoBase[video2])
        print("baseVideo " + str(base1) + ": ", self.baseVideo[base1])
        print("baseVideo " + str(base2) + ": ", self.baseVideo[base2])

    def useAvaiableBase(self, video, base):
        self.restOfBaseCapacity[base] = self.restOfBaseCapacity[base] - 1
        self.videoBase[video].append(base)
        self.baseVideo[base].append(video)

    def deuseAvaiableBase(self, video, base):
        self.restOfBaseCapacity[base] = self.restOfBaseCapacity[base] + 1
        self.videoBase[video].remove(base)
        self.baseVideo[base].remove(video)

    def snatchDistributedBase(self, video1, video2, base):
        self.videoBase[video1].append(base)
        self.videoBase[video2].remove(base)
        self.baseVideo[base].remove(video2)
        self.baseVideo[base].append(video1)

    def snatchDistributedBase(self, video1, video2, base):
        self.videoBase[video1].append(base)
        self.videoBase[video2].remove(base)
        self.baseVideo[base].remove(video2)
        self.baseVideo[base].append(video1)

    def getExchangeableBaselist(self, video):
        exchangeableBaseList = []
        for base in range(len(self.restOfBaseCapacity)):
            if self.restOfBaseCapacity[base] > 0 and base not in self.videoBase[video]:
                exchangeableBaseList.append(base)
        return exchangeableBaseList
