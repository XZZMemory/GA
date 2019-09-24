import random
import copy  # 深复制，浅复制
import Utils
from Individual import Individual
from Painter import Painter
import numpy as np


class Population:
    # 类似于类变量，各个函数都可以使用
    individualList = []  # 初始个体列表
    # 种群参数设置
    sizeOfPopulation = 30  # 测试，先写10个种群大小
    iterations = 70  # 迭代次数
    crossoverPc = 0.95  # 交叉概率
    mutatePm = 0.09  # 0.02#变异概率

    def __init__(self):
        self.tau = 1
        self.sumOfBase = 7  # 0代表的是宏基站
        self.sumOfUser = 20  # 用户个数
        # self.sumOfMicroUser
        self.sumOfChannels = 25
        self.sumOfVideo = 4
        self.baseCapacity = []
        self.baseCapacity.append(200)
        for i in range(self.sumOfBase - 1):
            self.baseCapacity.append(50)
        self.powerOfBase = []
        for i in range(self.sumOfBase):
            if i == 0:
                self.powerOfBase.append(20000)
            else:
                self.powerOfBase.append(1000)
        self.baseRadius = []
        for base in range(self.sumOfBase):
            if base == 0:
                self.baseRadius.append(500)
            else:
                self.baseRadius.append(100)
        self.Alpha = 100000  # 计算噪声参数

    '''
    1.初始化 1-VN
             2-VQS
             3-location(BS、UE)，VQD
             4-BasevisitedUE
             5-BScapacity
    2.creatPopulation
    3.crossover 
    4.mutate
    5.GetAllFitness，**
    6.PopulationRevise？？   后续适应值低会自动淘汰掉'''

    def initialization(self):
        # self.VN = self.VNInitial()  # 就需要特殊处理了。
        self.VN = [[1, -1, 1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, 1, -1, 1],
                   [1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, -1, -1, 1],
                   [-1, -1, 1, 1, -1, -1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1],
                   [-1, 1, 1, 1, 1, 1, 1, 1, -1, 1, -1, -1, 1, 1, 1, -1, 1, -1, -1, -1]]
        # self.typeOfVQD = typeOfVQD  # 表示VQD种类，如果是4
        # 每个视频的大小是50KBytes。
        self.VQS = []
        for video in range(self.sumOfVideo):
            self.VQS.append([])
            for j in range(10):
                self.VQS[video].append(5)
        Utils.printListWithTwoDi("VN: ", self.VN)
        self.allLocationInitialTest()  # ,500m

    # 测试
    def allLocationInitialTest(self):
        self.VN = [[1, -1, 1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, 1, -1, 1],
                   [1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, -1, -1, 1],
                   [-1, -1, 1, 1, -1, -1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1],
                   [-1, 1, 1, 1, 1, 1, 1, 1, -1, 1, -1, -1, 1, 1, 1, -1, 1, -1, -1, -1]]
        self.VQS = [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]
        self.locationOfBase = [[0, 0], [346, 200], [0, 400], [-346, 200], [-346, -200], [0, -400],
                               [346, -200]]  # 基站位置初始化
        self.locationOfUser = [[337.2631696625841, 250.2445139240397], [-341.94661511724223, -36.63797744242588],
                               [-274.49708673772585, 159.2435408201836], [-20, 377.85831021712113],
                               [-149.76468697372144, 344.4262640065619], [-487, -65],
                               [67.35214258872664, 113.99694915282447], [147, 352],
                               [-120.53587670222394, -388.2839154549412], [-145.51818802384983, -68],
                               [-239.98934669846153, 370.5932928423781], [-128, 234.89338992927946],
                               [431.70313500687996, -191.4812147540513], [-335, 192],
                               [145.8211788904833, 250.25655756158767], [79.33030867625578, -120.10491641757523],
                               [-252.6934480137271, -402.22348031537666], [337.05888317443726, 159.12791180485462],
                               [-216.73973223345803, 124.46229396333888],
                               [-114.24179725841555, -40.547156953680194]]  # 用户位置初始化
        self.userToBaseSorted = self.getSortedBaseToUser(self.locationOfBase, self.locationOfUser)
        self.getVQD(self.userToBaseSorted)  # 视频描述存储位置初始化

    def initializationOfVQD(self, typeOfVQD):
        self.typeOfVQD = typeOfVQD
        if (self.typeOfVQD == 1):
            self.VQD = self.VQD1
        elif (self.typeOfVQD == 2):
            self.VQD = self.VQD2
        elif (self.typeOfVQD == 3):
            self.VQD = self.VQD3
        elif (self.typeOfVQD == 4):
            self.VQD = self.VQD4
        elif (self.typeOfVQD == 5):
            self.VQD = self.VQD5
        if ((self.typeOfVQD == 1) or (self.typeOfVQD == 2) or (self.typeOfVQD == 3)):
            self.basevisitedUE = self.getBaseVisitedUE(VQD=self.VQD)  # 返回函数值，每个基站的访问用户，在基站分配信道时使用
        elif (self.typeOfVQD == 4):
            self.baseVisitedOfUserVisitingVideo = self.getBaseVisitedOfUserVisitingVideoOfVQD4(self.VQD4,
                                                                                               self.userToBaseSorted,
                                                                                               self.VN)  # 用户访问视频的描述时访问哪个基站
            self.basevisitedUE = self.getBaseVisitedUserOfVQD45(
                copy.deepcopy(self.baseVisitedOfUserVisitingVideo))  # 得到基站的访问用户
        elif (self.typeOfVQD == 5):
            self.baseVisitedOfUserVisitingVideo = self.getBaseVisitedOfUserVisitingVideoOfVQD5(self.VQD5)
            self.basevisitedUE = self.getBaseVisitedUserOfVQD45(
                copy.deepcopy(self.baseVisitedOfUserVisitingVideo))  # 得到基站的访问用户

    def allLocationInitial(self):
        self.locationOfBase = self.baseLocationInitial()  # 基站位置初始化
        self.locationOfUser = self.userLocationInitial(radius=500, radius2=100, )  # 用户位置初始化 为了测试注解掉这个初始化
        paint = Painter()
        paint.paintBasesAndUsers(self.locationOfBase, self.locationOfUser)
        self.userToBaseSorted = self.getSortedBaseToUser(self.locationOfBase, self.locationOfUser)
        self.getVQD(self.userToBaseSorted)  # 视频描述存储位置初始化

    '''矩阵数据均从下标0就开始存储'''
    '''1.VN矩阵，用户与视频之间的访问关系，会返回生成矩阵，在总的初始化矩阵中再调用这个函数'''

    def VNInitial(self):
        VN = []
        for i in range(0, self.sumOfVideo):
            VN.append([])
            for j in range(0, self.sumOfUser):
                p = random.random()
                if (p < 0.5):
                    VN[i].append(-1)
                else:
                    VN[i].append(1)
        print("VN: " + str(VN))
        return VN

    '''2.生成VQS矩阵，即，每个视频的描述大小,会返回生成的矩阵，在总的初始化矩阵中再调用这个函数'''

    def VQSInitial(self):
        VQS = []
        for video in range(self.sumOfVideo):
            VQS.append([])
            numofdescription = int(random.randint(9, 10))
            for description in range(numofdescription):
                sizeOfDescription = random.randint(4, 5)
                VQS[video].append(sizeOfDescription)
                # sum+=sizeOfDescription
                description += 1
        print("vqs:  " + str(VQS))
        return VQS

    '''3.基站位置的初始化。基站是4个,整个拓扑，长=宽=500m
    七个基站，0是宏基站，
    Pn,max为基站最大功率，在本模型中，共有两种类型的基站，其中宏基站的最大功率设为43dBm（合20000mW）
    ，即P1,max = 43dbm，微微基站的最大功率设为30dBm（合1000mW），即P2,max = P3,max = … = PK,max = 30dbm。'''

    def baseLocationInitial(self):
        locationOfBase = [[0, 0], [346, 200], [0, 400], [-346, 200], [-346, -200], [0, -400], [346, -200]]
        self.width = 500
        self.height = 500
        return locationOfBase

    '''4.用户位置的初始化'''

    def userLocationInitial(self, radius, radius2):
        locationOfUser = []
        userNum = self.sumOfUser
        radius = self.baseRadius[0]
        t = np.random.random(size=userNum) * 2 * np.pi - np.pi
        x = np.cos(t)
        y = np.sin(t)
        i_set = np.arange(0, userNum, 1)
        for i in i_set:
            len = np.sqrt(np.random.random())
            x[i] = x[i] * len * radius
            y[i] = y[i] * len * radius
            locationOfUser.append([x[i], y[i]])
        return locationOfUser

        '''
        locationOfUser = []
        for i in range(self.sumOfUser):
            x = random.randint(0, radius)
            yRadius = int((radius ** 2 - x ** 2) ** 0.5)
            y = random.randint(0, yRadius)
            xFlag = random.random()
            if xFlag < 0.5:
                x = -x
            yFlag = random.random()
            if yFlag < 0.5:
                y = -y
            locationOfUser.append([x, y])
        print("locationOfUser:  " + str(locationOfUser))
        return locationOfUser
        '''

    # 需要条件：用户访问视频矩阵，VQS视频的描述大小， 基站分布
    def getVQD(self, userToBaseSorted):  # 得到四种视频存储位置，顺序存储，随机存储，按照视频重要度，离访问用户最近的基站
        self.VQD1 = self.getVQD1()  # 顺序存储
        self.VQD2 = self.getVQD2()  # 随机存储
        self.VQD3 = self.getVQD3()  # 基于视频重要度+距离确定存储位置
        self.VQD4 = self.getVQD4(userToBaseSorted)  # 存储在距离访问用户最近的基站
        self.VQD5 = self.getVQD5()  # 宏基站能存储所有的视频，在某一微基站

    def getVQD1(self):  # 顺序存储，实际是一个三维矩阵，基站+视频+描述
        VQD1 = []
        baseCapacity = copy.deepcopy(self.baseCapacity)  # =self.BScapacity #BScapacity=self.BScapacity#标记每个基站的声剩余存储容量
        flagOfBase = 0  # 顺序存储，当前访问到哪个基站，初始化为0基站
        # 顺序存储。，基站1-->S,用户1-->V
        for i in range(len(self.VQS)):
            VQD1.append([])
            for j in range(len(self.VQS[i])):  # 对于视频i的所有描述
                if (baseCapacity[flagOfBase] < self.VQS[i][j]):  # 当前基站不能存下这个视频
                    flagOfBase += 1
                    if (flagOfBase >= self.sumOfBase):
                        exit("超出所有基站容量，退出")
                VQD1[i].append(flagOfBase)  # 在VQD中存储当前描述存储的基站
                baseCapacity[flagOfBase] -= self.VQS[i][j]  # 当前基站的剩余容量=基站容量-视频描述大小
        return VQD1

    def getVQD2(self):  # 随机存储
        baseCapacity = copy.deepcopy(self.baseCapacity)  # self.BScapacity#存储每个基站的容量，以得到VQD2
        VQD2 = []  # 返回的数据，视频的存储矩阵
        for i in range(len(self.VQS)):  # 基站
            VQD2.append([])
            for j in range(len(self.VQS[i])):  # 对于视频i的所第j个描述
                # 随机产生一个基站（满足：基站剩余容量能够存储这个描述，否则继续产生一个随机矩阵，直至能够存储下这个描述）
                n = random.randint(0, self.sumOfBase - 1)  # 随机产生一个基站
                while (baseCapacity[n] < self.VQS[i][j]):  # 如果基站剩余容量不能存储这个视频描述
                    n = random.randint(0, self.sumOfBase - 1)  # 继续产生一个随机数
                VQD2[i].append(n)  # 在VQD中存储当前描述存储的基站
                baseCapacity[n] -= self.VQS[i][j]  # 当前基站的剩余容量=基站容量-视频描述大小
        return VQD2

    # 根据视频的重要度进行排序
    def getVQD3(self):
        VQD3 = []  # 返回的数据，视频的存储矩阵，第三种存储方式
        baseCapacity = copy.deepcopy(self.baseCapacity)  # self.BScapacity#每个基站的存储容量
        '''确认视频存储到哪个基站的距离到所有访问用户的距离最近横-视频video，竖-基站，存储在哪个基站 ，离所有访问用户的距离最近'''
        sorted_Base_Distance = self.getNearestBaseToVideoVisitingUser(self.VN, self.locationOfBase, self.locationOfUser)
        videoImportance = self.getVideoImportance(self.VN)  # 视频的重要读排序是一个一维数组，基于视频的访问用户多少进行排序
        for i in range(self.sumOfVideo):
            VQD3.append([])
        for i in range(len(videoImportance)):  # i:0-->5,视频Video_importance[i]，0 3 1 2视频存储顺序不是按照顺序，而是按照重要度
            flagOfBase = 0  # 从距离最近的基站开始
            video = videoImportance[i]  # 视频
            for description in range(
                    len(self.VQS[video])):  # 描述大小VQS[Video_importance[i][description]#访问用户+基站位置--》视频放哪儿合适
                # 找到能够存储，且距离最小的基站，1.视频的重要度 2.距离的计算（访问用户到各个基站的总距离）
                videoDescriptionSize = self.VQS[video][description]  # 描述大小
                flag = 0  # 描述>基站剩余容量
                '''找到能够存这个描述的基站，则直接跳出while循环'''
                while flag == 0:
                    storedBS = sorted_Base_Distance[video][flagOfBase]
                    if videoDescriptionSize > baseCapacity[storedBS]:
                        flagOfBase += 1
                    else:
                        flag = 1
                baseCapacity[storedBS] -= videoDescriptionSize
                VQD3[video].append(storedBS)
        return VQD3

    '''在基站有剩余容量的情况下，视频可以存储几遍，这样命中率就高了,
       思路：存储在离访问用户最近的基站'''

    def getVQD4(self, userToBaseSorted):
        VQD = []  # 返回的数据，视频的存储位置，第四种方式
        baseCapacity = copy.deepcopy(self.baseCapacity)  # self.BScapacity#每个基站的存储容量
        '''确认视频存储到哪个基站的距离到所有访问用户的距离最近横-视频video，竖-基站，存储在哪个基站，离所有访问用户的距离最近'''
        nearestBaseDistance = self.getNearestBaseToVideoVisitingUser(self.VN, self.locationOfBase, self.locationOfUser)
        videoImportance = self.getVideoImportance(self.VN)  # 视频的重要读排序是一个一维数组，基于视频的访问用户多少进行排序
        for i in range(self.sumOfVideo):
            VQD.append([])
        for videoFlag in range(len(videoImportance)):  # i:0-->5,视频Video_importance[i]，0 3 1 2视频存储顺序不是按照顺序，而是按照重要度
            flagOfBase = 0  # 从距离最近的基站开始
            video = videoImportance[videoFlag]  # 视频
            for description in range(
                    len(self.VQS[video])):  # 描述大小VQS[Video_importance[i][description]#访问用户+基站位置--》视频放哪儿合适
                # 找到能够存储，且距离最小的基站，1.视频的重要度 2.距离的计算（访问用户到各个基站的总距离）
                VQD[video].append([])
                videoDescriptionSize = self.VQS[video][description]  # 描述大小
                flag = 0  # 描述>基站剩余容量
                '''找到能够存这个描述的基站，则直接跳出while循环'''
                while (flag == 0):
                    storedBS = nearestBaseDistance[video][flagOfBase]
                    if (videoDescriptionSize > baseCapacity[storedBS]):
                        flagOfBase += 1
                    else:
                        flag = 1
                baseCapacity[storedBS] -= videoDescriptionSize
                VQD[video][description].append(storedBS)
        for videoFlag in range(len(videoImportance)):
            video = videoImportance[videoFlag]
            for user in range(len(self.VN[video])):
                isVisited = self.VN[video][user]
                if (isVisited == 1):  # 用户user访问视频video,看看离用户最近的基站存储了没，没存储的话，就存储一遍//访问每个description
                    for description in range(len(self.VQS[video])):
                        isStored = False  # 表示对于这个视频藐视的这个访问用户，视频是否找到哦啊合适的存储地，False-没找到，True-找到了
                        flagOfBase = 0
                        currentBase = userToBaseSorted[user][flagOfBase]  # 找到当前应该存储的基站,看看VQD4有没有这个基站，没有就存储一下。
                        while (((currentBase in VQD[video][description]) == False) & (
                                isStored == False)):  # 对于这个视频的这个访问用户，视频还没有找到很好的存储地
                            if (flagOfBase >= self.sumOfBase):  # 所有基站的存储容量都用完了
                                return VQD
                            if (self.VQS[video][description] > baseCapacity[currentBase]):
                                flagOfBase += 1
                                currentBase = userToBaseSorted[user][flagOfBase]

                            else:
                                VQD[video][description].append(currentBase)
                                isStored = True
                                baseCapacity[currentBase] -= self.VQS[video][description]
        return VQD

    ''' 宏基站能够存储所有视频，用户在微基站覆盖范围内的，则访问微基站，微基站没有改视频，则访问宏基站
    确定视频描述的存储位置，首先宏基站存储一遍，对于每个微基站，找到覆盖范围内访问用户最多的基站，存储该视频'''

    def getVQD5(self):
        baseCapacity = copy.deepcopy(self.baseCapacity)  # self.BScapacity#每个基站的存储容量
        VQD = []
        for video in range(self.sumOfVideo):
            VQDVideo = []
            for description in range(len(self.VQS[video])):
                VQDVideo.append([0])
            VQD.append(VQDVideo)
        baseCapacity[0] = 0  # 宏基站的存储容量为0
        '''得到每个基站的覆盖范围内的用户'''
        baseCoveredUsers = self.getBaseCoveredUsers()
        '''得到每个微基站的存储的视频'''
        for base in range(1, self.sumOfBase):
            # 得到每个微基站覆盖范围内的用户访问最多的视频
            videoImportant = self.getBaseCoveredVideoImportant(baseCoveredUsers[base])
            # 在微基站中存储视频
            currentBaseCapacity = self.baseCapacity[base]
            videoFlag = 0
            while (currentBaseCapacity > 0 and videoFlag < len(videoImportant)):
                currentVideo = videoImportant[videoFlag]
                description = 0
                while (description < len(self.VQS[currentVideo]) and (currentBaseCapacity >= self.VQS[currentVideo][
                    description])):
                    currentBaseCapacity -= self.VQS[currentVideo][description]
                    VQD[currentVideo][description].append(base)
                    description += 1
        return VQD

    '''4.1 基站与用户距离排序，getVQD4()会用到，看看用户离那个基站最近，这样在存储视频时就存储在离用户最近的基站'''

    def getBaseCoveredUsers(self):
        baseCoveredUsers = []
        baseCoveredUsers.append([])
        for base in range(1, self.sumOfBase):
            users = []
            for user in range(self.sumOfUser):
                print("user: " + str(self.locationOfUser[user]) + "  base: " + str(self.locationOfBase[base]))
                if (self.isCovered(self.locationOfBase[base], self.locationOfUser[user], self.baseRadius[base])):
                    users.append(user)
            baseCoveredUsers.append(users)
        return baseCoveredUsers

    def getBaseCoveredVideoImportant(self, users):
        videoImportant = []
        for video in range(self.sumOfVideo):
            videoImportant.append([0, video])
        for user in users:
            for video in range(self.sumOfVideo):
                if self.VN[video][user] == 1:
                    videoImportant[video][0] = videoImportant[video][0] + 1
        n = sorted(videoImportant, key=lambda videoImportant: videoImportant[0], reverse=True)
        important = []
        for video in range(len(n)):
            if n[video][0] != 0:
                important.append(n[video][1])
        return important

    # user是否在base覆盖范围内
    def isCovered(self, locationOfBase, locationOfUser, baseRadius):
        distance = (locationOfBase[0] - locationOfUser[0]) ** 2 + (locationOfBase[1] - locationOfUser[1]) ** 2
        if distance <= (baseRadius ** 2):
            return True
        return False

    def getSortedBaseToUser(self, locationOfBase, locationOfUser):
        distance = []  # 计算基站到用户的距离
        for user in range(len(locationOfUser)):
            distance.append([])
            for base in range(len(locationOfBase)):
                currentDistance = ((locationOfBase[base][0] - locationOfUser[user][0]) ** 2 + (
                        locationOfBase[base][1] - locationOfUser[user][1]) ** 2) ** 0.5
                distance[user].append([base, currentDistance])
        for user in range(len(distance)):  # 横-用户 竖-基站
            userToBase = distance[user]
            userToBase.sort(key=lambda userToBase: userToBase[1])
        userToBaseSorted = []
        for user in range(len(distance)):
            userToBaseSorted.append([])
            for base in range(len(distance[user])):
                userToBaseSorted[user].append(distance[user][base][0])
        return userToBaseSorted

    def getBaseVisitedOfUserVisitingVideoOfVQD5(self, VQD5):
        userVideoBase = []
        for user in range(self.sumOfUser):
            userVideoBase.append([])
            for video in range(self.sumOfVideo):
                userVideoBase[user].append([])
                if self.VN[video][user] == 1:
                    for description in range(len(VQD5[video])):
                        base = self.getBaseOfVQD5(user, self.VQD5[video][description])
                        userVideoBase[user][video].append(base)
        return userVideoBase

    def getBaseOfVQD5(self, user, storedBaseList):
        if user == 17:
            print("storedBase: " + str(storedBaseList))
        storedBase = 0
        for base in storedBaseList:
            if base != 0 and self.isCovered(self.locationOfBase[base], self.locationOfUser[user],
                                            self.baseRadius[base]):
                storedBase = base
        return storedBase

    '''4.2 用户访问视频时访问哪个基站-个体初始化时用到
    找到用户访问视频时访问哪个基站最好（离用户距离越近的约好），VQD4中视频的描述可能存储在多个基站中，所以我们需要找到访问哪个基站最好，
    可以在getVQD4()中确定，但本身getVQD4()函数处理过程比较麻烦，若再确定，还需要再加条件判断，所以在这直接写个函数，逻辑处理会简单些'''

    def getBaseVisitedOfUserVisitingVideoOfVQD4(self, VQD4, userToBaseSorted, VN):
        userVideoBase = []
        for user in range(self.sumOfUser):
            userVideoBase.append([])
            for video in range(self.sumOfVideo):
                userVideoBase[user].append([])
                if (VN[video][user] == 1):
                    for description in range(len(VQD4[video])):
                        base = self.getBaseVQD4(userToBaseSorted[user], VQD4[video][description])
                        userVideoBase[user][video].append(base)
        return userVideoBase

    '''4.3'''

    def getBaseVQD4(self, userToBaseSorted, storedBase):
        for base in userToBaseSorted:
            if base in storedBase:
                return base
        return -1

    '''4.3每个基站的访问用户，Individual个体的初始化，分配基站的信道和功率时使用，由于VQD4存储方式和其他不一样，所以单独写个函数'''
    '''# userVideoDescription: 用户访问视频的描述时访问哪个基站'''

    def getBaseVisitedUserOfVQD45(self, baseVisitedOfUserVisitingVideo):  # user-video-description
        temp = []
        '''由于每个描述存储的地址是一个list，所以先求出video的所有描述存储地址，然后再进行合并'''
        for user in range(len(baseVisitedOfUserVisitingVideo)):
            temp.append([])  # user
            for video in range(len(baseVisitedOfUserVisitingVideo[user])):
                temp[user].extend(baseVisitedOfUserVisitingVideo[user][video])
        for user in range(len(temp)):
            temp[user] = list(set(temp[user]))
        basevisitedUE = []  # 横坐标i：基站，纵坐标j：用户
        for base in range(self.sumOfBase):
            basevisitedUE.append([])
        for user in range(len(temp)):
            for base in temp[user]:
                basevisitedUE[base].append(user)
        return basevisitedUE  # 返回每个基站的访问用户（根据视频描述存储位置+每个视频的访问用户）

    '''3.1. 根据每个视频的每个访问用户，确认视频存储到哪个基站的距离到所有访问用户的距离最近,GetVQD3函数会调用这个函数'''

    def getNearestBaseToVideoVisitingUser(self, VN, locationOfBase, locationOfUser):  # 计算每个视频的每个访问用户到哪个基站的距离最近
        minDistance = []
        distance = []  # 计算视频访问用户到基站的距离，没有排序
        for video in range(self.sumOfVideo):  # 视频i 横
            distance.append([])
            for bs in range(self.sumOfBase):  # 基站j 竖
                distance[video].append([0, bs])  # 加入基站标识，这样在对距离进行排序时，基站也会自动排序
                for user in range(len(VN[video])):  # 对于这个视频的所有访问用户k
                    if (VN[video][user] == 1):  # 用户k到基站j的距离
                        currentDistance = ((locationOfBase[bs][0] - locationOfUser[user][0]) ** 2 + (
                                locationOfBase[bs][1] - locationOfUser[user][1]) ** 2) ** 0.5
                        distance[video][bs][0] += currentDistance
        # 下面基于得到的距离矩阵Distance，进行排序，计算结果：视频 1-->V ,基站 距离小-->距离大
        ss = []
        for video in range(len(distance)):  # 在每一行中，即每个视频中的所有基站，基于距离进行排序（距离+基站标识），是一个三维矩阵
            nn = distance[video]
            nn.sort(key=lambda nn: nn[0])
            ss.append(nn)
        # MinDistance排序后的距离
        for video in range(len(ss)):  # 对三维矩阵，对于每一个视频，每一行，数据原本是距离+基站标识，抽取出基站标识
            minDistance.append([])
            for bs in range(len(ss[video])):
                minDistance[video].append(ss[video][bs][1])
        return minDistance  # 返回基于距离排序后，基站的优先存储顺序

    '''3.2. 计算视频的访问用户数量，哪个视频比较重要（越重要，访问用户越多）'''

    def getVideoImportance(self, VN):  # 根据VN(每个视频的访问用户)，对视频的重要度排序，返回排序后的视频
        VideoImportance = []
        Sort_Video = []  # 返回的数组
        for i in range(len(VN)):
            VideoImportance.append(0)
            for j in range(len(VN[i])):
                if (VN[i][j] == 1):  # 代表用户j访问视频i
                    VideoImportance[i] += 1
        ns = []
        for i in range(self.sumOfVideo):
            ns.append((VideoImportance[i], i))
        n = sorted(ns, key=lambda ns: ns[0], reverse=True)
        for i in range(len(n)):
            Sort_Video.append(n[i][1])
        return Sort_Video

    '''4.每个基站的访问用户，Individual个体的初始化，分配基站的信道和功率时使用'''

    def getBaseVisitedUE(self, VQD):
        VQD = copy.deepcopy(VQD)
        # 去掉列表中的重复元素
        temp_VQD = []  # 视频描述的存储位置，去掉列表VQD中的重复元素后的数组
        for i in range(len(VQD)):
            temp_VQD.append([])
            for element in VQD[i]:
                if element not in temp_VQD[i]:
                    temp_VQD[i].append(element)
        basevisitedUE = []  # 横坐标base：基站，纵坐标user：用户
        for base in range(self.sumOfBase):
            basevisitedUE.append([])
            for video in range(len(temp_VQD)):  # 视频j，访问用户，没有重复元素
                for flagOfStoredBase in range(len(temp_VQD[video])):
                    if (temp_VQD[video][flagOfStoredBase] == base):  # 当前j视频的第k个描述存储在基站i上，找到这个视频的访问用户
                        for user in range(len(self.VN[video])):
                            if ((self.VN[video][user] == 1) and (user not in basevisitedUE[base])):
                                basevisitedUE[base].append(user)
            basevisitedUE[base].sort()
        return copy.deepcopy(basevisitedUE)  # 返回每个基站的访问用户（根据视频描述存储位置+每个视频的访问用户）
        # 基于VN（视频访问用户）和VQD

    # 1.创建种群
    def creatPopulation(self):  # 创建种群
        print("***********种群中验证参数*************")
        print("self: " + str(self))
        print("typeOfVQD: " + str(self.typeOfVQD))
        self.individualList = []
        for i in range(Population.sizeOfPopulation):
            individual = Individual(self, self.typeOfVQD)
            self.individualList.append(individual)
        print("self.individualList: " + str(self.individualList))
        print("***********种群中验证参数完毕************")

    # 2.交叉，返回空或者交叉之后的两个新个体，交叉操作已测试成功
    def crossover(self,
                  individualForCross):  # individualForCross是一个数组，里面有两个个体individualForCross[0],individualForCross[1]
        if (random.random() < self.crossoverPc):  # 小于这个概率，执行交叉操作
            print("种群中发生交叉")
            return individualForCross[0].crossover(individualForCross[1])  # 使用个体类自己的方法
        else:
            return []

    # 3.变异，传入参数是两个个体，返回变异之后的两个个体，有可能是原个体，有可能是新的个体
    def mutate(self, individualForMutate):  # individualForMutate，自己写，只有一个个体参数
        for i in range(2):
            if (random.random() < self.mutatePm):  # 小于mutatePm，执行变异操作
                print("种群个体发生变异")
                individualForMutate[i].mutate()

    # 4.得到所有个体的适应值
    def getAllFitness(self):
        fitnessList = []
        for i in range(self.sizeOfPopulation):
            fitnessList.append(self.individualList[i].getFitness())  # 在individual文件中，这个函数的写法比较重要，好好写
        return fitnessList

    def getAllFitnessIntegral(self):
        fitnessList = []
        for i in range(self.sizeOfPopulation):
            fitnessList.append(self.individualList[i].getFitnessWithIntegral())  # 在individual文件中，这个函数的写法比较重要，好好写
        return fitnessList

    '''根据种群适应值，选择两个个体，进行交叉，锦标赛选择法，
    随机产生两个样本，分别竞争第一组竞争'''

    def select(self):
        if len(self.individualList) < 2:
            print("种群个体列表长度小于2")
        competitors_1 = random.sample(self.individualList, 2)
        competitors_2 = random.sample(self.individualList, 2)
        fitness_1 = [competitors_1[0].getFitness(), competitors_1[1].getFitness()]
        fitness_2 = [competitors_2[0].getFitness(), competitors_2[1].getFitness()]
        '''选择适应大的个体去交叉'''
        father = competitors_1[1] if fitness_1[1] > fitness_1[0] else competitors_1[0]
        mather = competitors_2[1] if (fitness_2[1] > fitness_2[0]) else competitors_2[0]
        return [copy.deepcopy(father), copy.deepcopy(mather)]
