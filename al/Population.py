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
    iterations = 3000  # 迭代次数
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

    def initialization(self, basevisitedUE):
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
        '''用户与基站之间的距离，用于计算SINR'''
        self.distanceUserToBase = self.getDistanceUserToBase()
        self.basevisitedUE = basevisitedUE

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
        fitness_1 = [competitors_1[0].getFitnessOfMatching(), competitors_1[1].getFitnessOfMatching()]
        fitness_2 = [competitors_2[0].getFitnessOfMatching(), competitors_2[1].getFitnessOfMatching()]
        '''选择适应大的个体去交叉'''
        father = competitors_1[1] if fitness_1[1] > fitness_1[0] else competitors_1[0]
        mather = competitors_2[1] if (fitness_2[1] > fitness_2[0]) else competitors_2[0]
        return [copy.deepcopy(father), copy.deepcopy(mather)]
