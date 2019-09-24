from de.MyObject import Base
from de.MyObject import Video
from de.MyObject import User
import copy
import random
import numpy


class Population:
    # 类似于类变量，各个函数都可以使用
    individualList = []  # 初始个体列表
    # 种群参数设置
    sizeOfPopulation = 50  # 测试，先写10个种群大小
    iterations = 50  # 迭代次数
    Fl = 0.1  # DE相关参数
    Fu = 0.9
    crossoverPc = 0.95  # 交叉概率
    mutatePm = 0.09  # 0.02#变异概率

    def __init__(self):
        self.sumOfBase = 7  # 0代表的是宏基站
        self.sumOfUser = 20  # 用户个数
        self.sumOfChannels = 25
        self.sumOfVideo = 4
        self.sumOfVideoDesc = 10
        self.sizeOfDesc = 5
        self.Alpha = 10  # 计算噪声参数

        self.baseList = []
        self.videoList = []
        self.userList = []
        # 基站信息初始化
        locationOfBase = [[0, 0], [346, 200], [0, 400], [-346, 200], [-346, -200], [0, -400],
                          [346, -200]]  # 基站位置初始化
        for base in range(self.sumOfBase):
            baseEntity = Base()
            baseEntity.sumOfChannels = 25
            baseEntity.location = locationOfBase[base]
            if base == 0:  # 宏基站
                baseEntity.radius = 500
                baseEntity.power = 20000
                baseEntity.capacity = 200
            else:
                baseEntity.radius = 100
                baseEntity.power = 1000
                baseEntity.capacity = 50
            self.baseList.append(base)

    def initialization(self):
        # 视频信息初始化
        for video in range(self.sumOfVideo):
            videoEntity = Video()
            decsList = []
            for desc in range(self.sumOfVideoDesc):
                decsList.append(self.sizeOfDesc)
            videoEntity.decs = decsList
            videoEntity.sumOfDesc = self.sumOfVideoDesc
            self.videoList.append(videoEntity)
        # 用户与视频的访问关系初始化
        self.VN = [[1, -1, 1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, 1, -1, 1],
                   [1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, -1, -1, 1],
                   [-1, -1, 1, 1, -1, -1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1],
                   [-1, 1, 1, 1, 1, 1, 1, 1, -1, 1, -1, -1, 1, 1, 1, -1, 1, -1, -1, -1]]
        self.allLocationInitialTest()

    # 用户位置初始化
    def allLocationInitialTest(self):

        locationOfUser = [[-127.2631696625841, -411.2445139240397], [-341.94661511724223, -36.63797744242588],
                          [-274.49708673772585, 159.2435408201836], [-94.997913574648, -288.85831021712113],
                          [-149.76468697372144, 344.4262640065619], [-487.2445614641922, -65.16896102420833],
                          [67.35214258872664, 113.99694915282447], [147.9380448388373, 352.0346798362575],
                          [-120.53587670222394, -388.2839154549412], [-145.51818802384983, -68.55547540105599],
                          [-239.98934669846153, 370.5932928423781], [-128.48929037429383, 234.89338992927946],
                          [431.70313500687996, -191.4812147540513], [-335.55544809488447, 192.207752371465],
                          [145.8211788904833, 250.25655756158767], [79.33030867625578, -120.10491641757523],
                          [-252.6934480137271, -402.22348031537666], [337.05888317443726, 159.12791180485462],
                          [-216.73973223345803, 124.46229396333888],
                          [-114.24179725841555, -40.547156953680194]]  # 用户位置初始化
        for user in range(self.sumOfUser):
            user = User()
            user.location = locationOfUser[user]
            self.userList.append(user)

    def initializationOfVQD(self, typeOfVQD):
        self.typeOfVQD = typeOfVQD
        if (self.typeOfVQD == 5):
            self.VQD = self.VQD5
        if (self.typeOfVQD == 5):
            self.baseVisitedOfUserVisitingVideo = self.getBaseVisitedOfUserVisitingVideoOfVQD5(self.VQD5)
            self.basevisitedUE = self.getBaseVisitedUserOfVQD45(
                copy.deepcopy(self.baseVisitedOfUserVisitingVideo))  # 得到基站的访问用户

    def getVQD5(self):
        baseCapacity = copy.deepcopy(self.baseCapacity)  # self.BScapacity#每个基站的存储容量
        VQD = []
        for video in range(self.sumOfVideo):
            VQDVideo = []
            for description in range(len(self.videoList[video].desc)):
                VQDVideo.append([0])
            self.videoList[video].setStoredBase(VQDVideo)
            VQD.append(VQDVideo)
        self.baseList[0].capacity = 0  # 宏基站的存储容量为0
        '''得到每个基站的覆盖范围内的用户实体'''
        '''得到每个微基站的存储的视频'''
        for base in range(1, self.sumOfBase):
            # 得到每个微基站覆盖范围内的用户访问最多的视频
            videoImportant = self.getBaseCoveredVideoImportant(self.baseList[base].coveredUsers)
            # 在微基站中存储视频
            currentBaseCapacity = self.baseList[base].capacity
            videoFlag = 0
            while (currentBaseCapacity > 0 and videoFlag < len(videoImportant)):
                currentVideo = videoImportant[videoFlag]
                description = 0
                while (description < len(self.VQS[currentVideo]) and (currentBaseCapacity >= self.VQS[currentVideo][
                    description])):
                    currentBaseCapacity -= self.VQS[currentVideo][description]
                    VQD[currentVideo][description].append(base)
                    description += 1
            self.baseList[base].capacity = currentBaseCapacity
        return VQD

    '''4.1 基站与用户距离排序，getVQD4()会用到，看看用户离那个基站最近，这样在存储视频时就存储在离用户最近的基站'''

    # 获取每个基站的覆盖用户实体
    def getBaseCoveredUsers(self):
        coveredUsers = []
        for base in range(1, self.sumOfBase):
            baseCoveredUsers = []
            for user in range(self.sumOfUser):
                if (self.baseList[base].isCovered(self.userList[user])):
                    baseCoveredUsers.append(user)
            coveredUsers.append(baseCoveredUsers)
            self.baseList[base].setCoveredUsers(coveredUsers)
        return coveredUsers

    # 计算每个基站覆盖范围内的用户，哪个视频访问的最多，最重要 users：覆盖的用户
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

    # VQD5存储方式时，用户访问视频描述时，访问哪个基站，
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

    def getBaseOfVQD5(self, user, storedBases):
        storedBase = 0
        for base in storedBases:
            if base != 0 and self.baseList[base].isCovered(self.baseList[base]):
                storedBase = base
        return storedBase

    '''4.3每个基站的访问用户，Individual个体的初始化，分配基站的信道和功率时使用，由于VQD4和VQD5存储方式和其他不一样，所以单独写个函数'''
    '''# userVideoDescription: 用户访问视频的描述时访问哪个基站'''

    def getBaseVisitedUserOfVQD45(self, baseVisitedOfUserVisitingVideo):  # user-video-description
        temp = []
        '''由于每个描述存储的地址是一个list，所以先求出video的所有描述存储地址，然后再进行合并'''
        for user in range(len(baseVisitedOfUserVisitingVideo)):
            temp.append([])  # user
            for video in range(len(baseVisitedOfUserVisitingVideo[user])):
                temp[user].extend(baseVisitedOfUserVisitingVideo[user][video])
        # 去掉重复数据
        for user in range(len(temp)):
            temp[user] = list(set(temp[user]))
        basevisitedUE = []  # 横坐标i：基站，纵坐标j：用户
        for base in range(self.sumOfBase):
            basevisitedUE.append([])
        for user in range(len(temp)):
            for base in temp[user]:
                basevisitedUE[base].append(user)
        return basevisitedUE  # 返回每个基站的访问用户（根据视频描述存储位置+每个视频的访问用户）

    def mutate(self, individualForMutate):
        mutatedPopulation=[]
        for i in range(len(individualForMutate)):
            '''当前要变异的个体是i ， 从种群中随机选择三个个体计算缩放因子和变异因子'''
            b = random.randint(0, self.sizeOfPopulation)
            m = random.randint(0, self.sizeOfPopulation)
            w = random.randint(0, self.sizeOfPopulation)
            indI = individualForMutate[i]
            indB = self.individualList[b]
            indM = self.individualList[m]
            indW = self.individualList[w]
            while (indI == indB or indI == indM or indI == indW or indB == indM or indB == indW or indM == indW):
                b = random.randint(0, self.sizeOfPopulation)
                m = random.randint(0, self.sizeOfPopulation)
                w = random.randint(0, self.sizeOfPopulation)
                indB = self.individualList[b]
                indM = self.individualList[m]
                indW = self.individualList[w]
            '''缩放因子 Fi'''
            fitList = self.sortByFit([indB, indM, indW])
            indB = fitList[0][0]
            indM = fitList[1][0]
            indW = fitList[2][0]
            fitnessB = fitList[0][1]
            fitnessM = fitList[1][1]
            fitnessW = fitList[2][1]
            Fi = 0.1 + 0.8 * ((fitnessM - fitnessB) / (fitnessW - fitnessB))  # 求得当前个体的缩放因子
            indI.P = numpy.mat( numpy.array(indB.P) + Fi * (numpy.mat(numpy.array(indW.P)) + numpy.mat(numpy.array(indW.P))))
            indI.C=[]=numpy.mat( numpy.array(indB.C) + Fi * (numpy.mat(numpy.array(indW.C)) + numpy.mat(numpy.array(indW.C))))
        return  mutatedPopulation

    def sortByFit(self, list):
        fitList = []
        for i in range(len(list)):
            fitList.append([list[i].getFitness(), i])
        sorted(fitList, key=lambda fitList: fitList[0], reverse=True)
        return fitList

    def crossover(self, individualForCrossover, fitnessList):
        cr = []
        min = self.getMinNum(fitnessList)
        max = self.getMaxNum(fitnessList)
        avg = self.getAve(fitnessList)
        for i in range(len(individualForCrossover)):
            '''计算交叉概率'''
            if fitnessList[i]>avg:
                cr.append(0.1+0.5*((fitnessList[i]-min)/(max-min)))
            else:
                cr.append(0.1)

    def getMaxNum(num):
        sum = num[0]
        for i in range(len(num)):
            if sum < num[i]:
                sum = num[i]
        return sum

    def getMinNum(num):
        sum = num[0]
        for i in range(len(num)):
            if sum > num[i]:
                sum = num[i]
        return sum

    def getAve(num):
        total = 0
        for i in range(len(num)):
            total = total + num[i]
        return total / (len(num))
