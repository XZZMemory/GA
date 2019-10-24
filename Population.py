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
    sizeOfPopulation = 50
    iterations = 6000  # 迭代次数
    crossoverPc = 0.95  # 交叉概率
    mutatePm = 0.09  # 0.02#变异概率

    def __init__(self):
        self.tau = 1
        self.sumOfBase = 7  # 0代表的是宏基站
        self.sumOfUser = 30  # 用户个数
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
                self.powerOfBase.append(20)
            else:
                self.powerOfBase.append(1)
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
        self.VQS = []
        for video in range(self.sumOfVideo):
            self.VQS.append([])
            for j in range(10):
                self.VQS[video].append(5)
        self.allLocationInitialTest()  # ,500m
        Utils.printListWithTwoDi("VN: ", self.VN)
        print(str(len(self.VN[0])))
        '''用户与基站之间的距离，用于计算SINR'''
        self.getDistanceUserToBase()

    # 测试
    def allLocationInitialTest(self):
        self.VQS = [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
                    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]
        self.locationOfBase = [[0, 0], [346, 200], [0, 400], [-346, 200], [-346, -200], [0, -400],
                               [346, -200]]  # 基站位置初始化
        '''2- 30个用户，随机分配在宏基站覆盖范围内
        self.locationOfUser = [[314.93815668388834, 311.12784298818843], [-148.22158671732868, 469.78058532939565],
                               [-99.67037517599852, 216.2997056215897], [314.1879176115775, -15.207483828329952],
                               [-225.45652305892702, 226.82795326465106], [385.74347681305403, -48.73962698498847],
                               [-349.9903283580378, 37.38531186137528], [-393.78147417918285, 182.47889521447826],
                               [106.8057922709783, -381.87700402605776], [-370.87121408772094, -167.35190807740787],
                               [69.3125778140751, -216.99086052014906], [-14.561411757123876, 176.1318565303015],
                               [-267.52967086739915, -183.92691832530272], [32.57995418612326, 487.6800770379008],
                               [-235.11664822573863, -24.708207712083468], [154.3637484351586, -360.35491289007916],
                               [350.41256583515974, 270.06571677166613], [-451.5981282666048, -7.88481761759265],
                               [-9.422004437182395, -374.74053115352444], [-205.2214518013454, -247.45080096452998],
                               [281.91274010812725, -10.36430870692823], [169.38164332474787, -34.68796978191863],
                               [-287.57043337990746, 162.20389509012983], [-314.38931538253837, 85.18510967736607],
                               [-218.98721006855064, -189.29431298665023], [165.4415049663331, 139.42973861790634],
                               [335.0766673897913, 256.80854615422123], [33.59205284414872, -439.70754053519033],
                               [-252.84050888567367, 78.55502711745886], [-336.7361902049034, 280.3853526192622]]'''
        '''30个用户
        self.locationOfUser = [[347.26319978955024, 259.25312170758724], [369.186312709777, 141.1818561930079],
                               [266.2804458682548, 166.001976451566], [379.3118326962556, 276.5857102735613],
                               [409.53733563902716, 150.78422435303762], [10.738913756518869, 424.56065667283667],
                               [-68.4693923474341, 364.25113398414834], [-56.2319859432063, 362.7965989477528],
                               [79.62622143361261, 396.99192890355124], [-8.987360336516561, 333.35756136096245],
                               [-368.4966880361795, 126.31975957795395], [-342.09613679780784, 109.2755596625156],
                               [-361.7975770115996, 155.04687378943368], [-259.2336399076692, 184.09533215430622],
                               [-338.95614201745053, 259.4628917032581], [-345.7923083471936, -274.4150608387994],
                               [-319.9724809908709, -241.47386546843774], [-301.6719542524903, -213.3393366145805],
                               [-374.23313237614445, -239.31403398197557], [-268.38040753893586, -205.60001390876437],
                               [81.81458142405333, -451.58706650516297], [9.349042248130893, -356.01090564477374],
                               [-33.313077865183665, -415.93047530659334], [-63.90557516896962, -407.4715723660239],
                               [-5.422696222643595, -449.76136471752693], [410.58370753661893, -150.17858713138082],
                               [248.77648858495778, -210.62327247117327], [357.8889226513754, -164.78051780251752],
                               [380.73145771604806, -171.76656088472112], [336.052774489954, -193.24367021627305]] 
                                用户位置全在微基站中，且访问关系随机生成
                                 self.VN = [
            [-1, -1, -1, -1, 1, 1, 1, 1, -1, 1, -1, 1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, -1],
            [-1, 1, 1, 1, 1, -1, 1, -1, -1, 1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, 1, -1, -1, -1, 1, 1, -1, 1, 1, -1],
            [-1, 1, -1, 1, -1, -1, -1, -1, 1, -1, -1, -1, 1, 1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1, 1, -1,
             -1],
            [-1, 1, -1, -1, 1, -1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, -1, -1]]'''
        ''' self.locationOfUser = [[305.96212762264906, 131.25364916562523], [289.57643206774475, 145.44403854417064],
                               [406.39283501445135, 131.17229479349172], [389.5110492791143, 227.0444709880261],
                               [289.43385447654094, 203.31281941487086], [47.08760959109169, 354.71919105088796],
                               [8.94781029569983, 324.9331989704249], [61.2513850664053, 381.05954615119316],
                               [57.36120166732663, 364.90525923765165], [-27.121267877796285, 387.8196355977238],
                               [-332.4581528299449, 122.71269584284829], [-343.271626945513, 156.10340091006563],
                               [-350.2991129365175, 120.70331678676506], [-312.67038028301056, 171.48776669890623],
                               [-373.1689630234092, 259.44814827844436], [-423.53085953609866, -261.96365920129375],
                               [-336.4349324414945, -205.10566571305816], [-298.6078049753206, -195.36224387075046],
                               [-401.79397484744254, -155.29533242608431], [-283.7974650650451, -212.95409490363062],
                               [-11.463433173277922, -332.7881585848451], [60.925191925195485, -427.6133948057043],
                               [-76.52980156608852, -389.0738487020604], [3.166958856250013, -417.8970789534774],
                               [68.57483875317207, -360.34771656856196], [351.3014633208597, -108.61437900393514],
                               [291.0596615986839, -247.14272987541483], [299.23199964783413, -163.72401214156],
                               [269.074342921944, -147.81745965853176], [369.62920091002326, -141.611472724778]]

        
       self.VN = [[1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]],用户可全访问微基站
                   '''
        '''self.VN = [[1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0],
                   [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1],
                   [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
                   [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]]'''
        self.VN = [[1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0],
                   [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                   [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1],
                   [1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0]]
        self.VNTimes = Utils.getVNTimes(self.VN)
        self.locationOfUser = [[399.59413192549425, 202.17265320257155], [433.67031109477176, 243.2511996717791],
                               [355.94812711853825, 130.29866820493834], [336.0213785186953, 158.11956202575186],
                               [40.187964896169845, 327.9027832245315], [-57.676308608070535, 420.7128629554954],
                               [4.9112317747963, 483.2350310906051], [-66.63843912992044, 380.21683501837344],
                               [-424.3015612082439, 183.19194229432586], [-327.13553454055557, 178.26002275691812],
                               [-305.92545207536796, 221.2938200783817], [-405.35961915801136, 152.88700650297082],
                               [-304.7051511930708, -175.6058841222297], [-312.62550055998565, -241.53715452822397],
                               [-311.0372341658077, -176.8480650057702], [-316.5854439049896, -183.15581093795566],
                               [-7.725709606449042, -430.7006302232473], [-21.769677045554133, -362.92345511605254],
                               [-75.80060785607789, -461.7633500772326], [-46.59625749948575, -412.868563773172],
                               [353.1982513484292, -276.99318612705144], [371.5713216299222, -193.15801829873283],
                               [359.12485727666126, -259.20658582257937], [252.94806577055778, -225.48773360142056],
                               [-5.454097315018147, 71.26848948526256], [-227.16745395554648, -119.7783243809939],
                               [52.36924896570608, 186.31550118865587], [283.6746506040315, 18.61335005320503],
                               [-139.29264437685498, -23.99578719648378], [235.39926107500517, 143.31237750586322]]

        # self.userLocationInitial3()  # 用户位置初始化,选择第二种初始化方式，均在微基站覆盖范围内
        # self.randomVN()  # 在随机初始化几个值，增加访问关系
        # print("VN:   " + str(self.VN))
        # print("self.locationOfUser" + str(self.locationOfUser))
        self.getSortedBaseToUser()
        # self.getVQD()  # 视频描述存储位置初始化

    def randomVN(self):
        # 在随机初始化几个值，增加访问关系
        for video in range(len(self.VN)):
            for user in range(len(self.VN[video])):
                if self.VN[video][user] == 0:
                    if random.random() < 0.5:
                        self.VN[video][user] = 1
        print("random函数中VN" + str(self.VN))

    def initializationOfVQD(self, typeOfVQD):
        self.typeOfVQD = typeOfVQD
        if (typeOfVQD == 1):
            self.getVQD1()
            self.VQD = self.VQD1
        elif (typeOfVQD == 2):
            self.getVQD2()
            self.VQD = self.VQD2
        elif (typeOfVQD == 3):
            self.getVQD3()
            self.VQD = self.VQD3
        elif (typeOfVQD == 4):
            self.getVQD4()
            self.VQD = self.VQD4
        elif (typeOfVQD == 5):
            self.getVQD5()
            self.VQD = self.VQD5
        if ((self.typeOfVQD == 1) or (self.typeOfVQD == 2) or (self.typeOfVQD == 3)):
            self.baseVisitedOfUserVisitingVideo = None  # 多个方式，调用同一个函数，均传递相同的参数，不存在的为None
            self.getBaseVisitedUE(self.VQD)  # 返回函数值，每个基站的访问用户，在基站分配信道时使用
        elif (self.typeOfVQD == 4):
            # 用户访问视频的描述时访问哪个基站
            self.getBaseVisitedOfUserVisitingVideoOfVQD4()
            self.getBaseVisitedUserOfVQD45()  # 得到基站的访问用户
        elif (self.typeOfVQD == 5):
            # 用户访问视频的描述时访问哪个基站
            self.getBaseVisitedOfUserVisitingVideoOfVQD5()
            self.getBaseVisitedUserOfVQD45()  # 得到基站的访问用户

    def allLocationInitial(self):
        self.baseLocationInitial()  # 基站位置初始化
        self.userLocationInitial1(radius=500, radius2=100, )  # 用户位置初始化 为了测试注解掉这个初始化
        paint = Painter()
        paint.paintBasesAndUsers(self.locationOfBase, self.locationOfUser)
        self.getSortedBaseToUser()
        # self.getVQD()  # 视频描述存储位置初始化

    '''矩阵数据均从下标0就开始存储'''
    '''1.VN矩阵，用户与视频之间的访问关系，会返回生成矩阵，在总的初始化矩阵中再调用这个函数'''

    def VNInitial(self):
        self.VN = []
        for i in range(0, self.sumOfVideo):
            self.VN.append([])
            for j in range(0, self.sumOfUser):
                p = random.random()
                if (p < 0.5):
                    self.VN[i].append(-1)
                else:
                    self.VN[i].append(1)
        print("VN: " + str(self.VN))

    '''2.生成VQS矩阵，即，每个视频的描述大小,会返回生成的矩阵，在总的初始化矩阵中再调用这个函数'''

    def VQSInitial(self):
        self.VQS = []
        for video in range(self.sumOfVideo):
            self.VQS.append([])
            numofdescription = int(random.randint(9, 10))
            for description in range(numofdescription):
                sizeOfDescription = random.randint(4, 5)
                self.VQS[video].append(sizeOfDescription)
                # sum+=sizeOfDescription
                description += 1
        print("vqs:  " + str(self.VQS))

    '''3.基站位置的初始化。基站是4个,整个拓扑，长=宽=500m
    七个基站，0是宏基站，
    Pn,max为基站最大功率，在本模型中，共有两种类型的基站，其中宏基站的最大功率设为43dBm（合20000mW）
    ，即P1,max = 43dbm，微微基站的最大功率设为30dBm（合1000mW），即P2,max = P3,max = … = PK,max = 30dbm。'''

    def baseLocationInitial(self):
        self.locationOfBase = [[0, 0], [346, 200], [0, 400], [-346, 200], [-346, -200], [0, -400], [346, -200]]
        self.width = 500
        self.height = 500

    '''4.用户位置的初始化,这种初始化，用户随机分布在宏基站覆盖 范围内，但不一定在微基站覆盖范围内'''

    def userLocationInitial1(self):
        self.locationOfUser = []
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
            self.locationOfUser.append([x[i], y[i]])

    # 用户位置初始化，用户全部在微基站覆盖范围内，初始化VN看看
    def userLocationInitial2(self):
        self.VN = []
        for video in range(self.sumOfVideo):
            self.VN.append([])
            for user in range(self.sumOfUser):
                self.VN[video].append(0)

        self.locationOfUser = []
        baseFlag = 0  # 用户全部在微基站覆盖范围内
        userNum = self.sumOfUser
        avgUserNum = self.sumOfUser / (self.sumOfBase - 1)
        t = np.random.random(size=userNum) * 2 * np.pi - np.pi
        x = np.cos(t)
        y = np.sin(t)
        i_set = np.arange(0, userNum, 1)
        list = [0, 1, 2, 3]
        for user in i_set:
            if user % avgUserNum == 0:
                video = random.choice(list)
                baseFlag = baseFlag + 1
            len = np.sqrt(np.random.random())
            x[user] = x[user] * len * self.baseRadius[baseFlag]
            y[user] = y[user] * len * self.baseRadius[baseFlag]
            self.locationOfUser.append(
                [x[user] + self.locationOfBase[baseFlag][0], y[user] + self.locationOfBase[baseFlag][1]])
            self.VN[video][user] = 1
        print("***********userLocation:" + str(self.locationOfUser))
        print("***********VN:" + str(self.VN))

        # 用户位置初始化，用户2/3在微基站覆盖范围内，1/3在宏基站覆盖范围内初始化VN看看

    def userLocationInitial3(self):
        self.VN = []
        for video in range(self.sumOfVideo):
            self.VN.append([])
            for user in range(self.sumOfUser):
                self.VN[video].append(0)

        self.locationOfUser = []
        baseFlag = 0  # 用户全部在微基站覆盖范围内
        print("self.sumOfUser: " + str(self.sumOfUser))
        userNum = int(self.sumOfUser / 5 * 4)
        print("self.userNum: " + str(userNum))
        avgUserNum = int(userNum / (self.sumOfBase - 1))
        userNum = avgUserNum * (self.sumOfBase - 1)
        print("self.userNum: " + str(userNum))
        t = np.random.random(size=userNum) * 2 * np.pi - np.pi
        x = np.cos(t)
        y = np.sin(t)
        i_set = np.arange(0, userNum, 1)
        list = [0, 1, 2, 3]
        for user in i_set:
            if user % avgUserNum == 0:
                videoList = random.sample(list, 1)  # 随机选择两个video，用户访问
                baseFlag = baseFlag + 1
            len = np.sqrt(np.random.random())
            x[user] = x[user] * len * self.baseRadius[baseFlag]
            y[user] = y[user] * len * self.baseRadius[baseFlag]
            self.locationOfUser.append(
                [x[user] + self.locationOfBase[baseFlag][0], y[user] + self.locationOfBase[baseFlag][1]])
            for currentVideo in videoList:
                self.VN[currentVideo][user] = 1
            self.VN[random.choice(list)][user] = 1

        # 初始化在宏基站覆盖范围内的用户
        userNum = self.sumOfUser - userNum
        t = np.random.random(size=(userNum)) * 2 * np.pi - np.pi
        x = np.cos(t)
        y = np.sin(t)
        i_set = np.arange(0, userNum, 1)
        list = [0, 1, 2, 3]
        for user in i_set:
            videoList = random.sample(list, 1)
            len = np.sqrt(np.random.random())
            x[user] = x[user] * len * (self.baseRadius[0] / 3 * 2)
            y[user] = y[user] * len * (self.baseRadius[0] / 3 * 2)
            self.locationOfUser.append([x[user], y[user]])
            for currentVideo in videoList:
                self.VN[currentVideo][user] = 1
        # Utils.printData("locationOfUser", self.locationOfUser)

    def getDistanceUserToBase(self):
        self.distanceUserToBase = []
        for user in range(self.sumOfUser):
            self.distanceUserToBase.append([])
            for base in range(self.sumOfBase):
                n = ((self.locationOfUser[user][0] - self.locationOfBase[base][0]) ** 2 + (
                        self.locationOfUser[user][1] - self.locationOfBase[base][1]) ** 2) ** 0.5
                self.distanceUserToBase[user].append(int(n))

    # 需要条件：用户访问视频矩阵，VQS视频的描述大小， 基站分布
    def getVQD(self):  # 得到四种视频存储位置，顺序存储，随机存储，按照视频重要度，离访问用户最近的基站
        self.getVQD1()  # 顺序存储
        self.getVQD2()  # 随机存储
        self.getVQD3()  # 基于视频重要度+距离确定存储位置
        self.getVQD4()  # 存储在距离访问用户最近的基站
        self.getVQD5()  # 宏基站能存储所有的视频，在某一微基站

    def getVQD1(self):  # 顺序存储，实际是一个三维矩阵，基站+视频+描述
        self.VQD1 = []
        baseCapacity = copy.deepcopy(self.baseCapacity)  # =self.BScapacity #BScapacity=self.BScapacity#标记每个基站的声剩余存储容量
        flagOfBase = 0  # 顺序存储，当前访问到哪个基站，初始化为0基站
        # 顺序存储。，基站1-->S,用户1-->V
        for i in range(len(self.VQS)):
            self.VQD1.append([])
            for j in range(len(self.VQS[i])):  # 对于视频i的所有描述
                if (baseCapacity[flagOfBase] < self.VQS[i][j]):  # 当前基站不能存下这个视频
                    flagOfBase += 1
                    if (flagOfBase >= self.sumOfBase):
                        exit("超出所有基站容量，退出")
                self.VQD1[i].append(flagOfBase)  # 在VQD中存储当前描述存储的基站
                baseCapacity[flagOfBase] -= self.VQS[i][j]  # 当前基站的剩余容量=基站容量-视频描述大小

    def getVQD2(self):  # 随机存储
        baseCapacity = copy.deepcopy(self.baseCapacity)  # self.BScapacity#存储每个基站的容量，以得到VQD2
        self.VQD2 = []  # 返回的数据，视频的存储矩阵
        for i in range(len(self.VQS)):  # 基站
            self.VQD2.append([])
            for j in range(len(self.VQS[i])):  # 对于视频i的所第j个描述
                # 随机产生一个基站（满足：基站剩余容量能够存储这个描述，否则继续产生一个随机矩阵，直至能够存储下这个描述）
                n = random.randint(0, self.sumOfBase - 1)  # 随机产生一个基站
                while (baseCapacity[n] < self.VQS[i][j]):  # 如果基站剩余容量不能存储这个视频描述
                    n = random.randint(0, self.sumOfBase - 1)  # 继续产生一个随机数
                self.VQD2[i].append(n)  # 在VQD中存储当前描述存储的基站
                baseCapacity[n] -= self.VQS[i][j]  # 当前基站的剩余容量=基站容量-视频描述大小

    # 根据视频的重要度进行排序
    def getVQD3(self):
        self.VQD3 = []  # 返回的数据，视频的存储矩阵，第三种存储方式
        baseCapacity = copy.deepcopy(self.baseCapacity)  # self.BScapacity#每个基站的存储容量
        '''确认视频存储到哪个基站的距离到所有访问用户的距离最近横-视频video，竖-基站，存储在哪个基站 ，离所有访问用户的距离最近'''
        sorted_Base_Distance = self.getNearestBaseToVideoVisitingUser(self.VN, self.locationOfBase, self.locationOfUser)
        videoImportance = self.getVideoImportance()  # 视频的重要读排序是一个一维数组，基于视频的访问用户多少进行排序
        for i in range(self.sumOfVideo):
            self.VQD3.append([])
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
                baseCapacity[storedBS] = baseCapacity[storedBS] - videoDescriptionSize
                self.VQD3[video].append(storedBS)

    '''在基站有剩余容量的情况下，视频可以存储几遍，这样命中率就高了,
       思路：存储在离访问用户最近的基站'''

    def getVQD4(self):
        self.VQD4 = []  # 返回的数据，视频的存储位置，第四种方式
        baseCapacity = copy.deepcopy(self.baseCapacity)  # self.BScapacity#每个基站的存储容量
        '''确认视频存储到哪个基站的距离到所有访问用户的距离最近横-视频video，竖-基站，存储在哪个基站，离所有访问用户的距离最近'''
        nearestBaseDistance = self.getNearestBaseToVideoVisitingUser(self.VN, self.locationOfBase, self.locationOfUser)
        videoImportance = self.getVideoImportance()  # 视频的重要读排序是一个一维数组，基于视频的访问用户多少进行排序
        for i in range(self.sumOfVideo):
            self.VQD4.append([])
        for videoFlag in range(len(videoImportance)):  # i:0-->5,视频Video_importance[i]，0 3 1 2视频存储顺序不是按照顺序，而是按照重要度
            flagOfBase = 0  # 从距离最近的基站开始
            video = videoImportance[videoFlag]  # 视频
            for description in range(
                    len(self.VQS[video])):  # 描述大小VQS[Video_importance[i][description]#访问用户+基站位置--》视频放哪儿合适
                # 找到能够存储，且距离最小的基站，1.视频的重要度 2.距离的计算（访问用户到各个基站的总距离）
                self.VQD4[video].append([])
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
                self.VQD4[video][description].append(storedBS)
        for videoFlag in range(len(videoImportance)):
            video = videoImportance[videoFlag]
            for user in range(len(self.VN[video])):
                isVisited = self.VN[video][user]
                if (isVisited == 1):  # 用户user访问视频video,看看离用户最近的基站存储了没，没存储的话，就存储一遍//访问每个description
                    for description in range(len(self.VQS[video])):
                        isStored = False  # 表示对于这个视频藐视的这个访问用户，视频是否找到哦啊合适的存储地，False-没找到，True-找到了
                        flagOfBase = 0
                        currentBase = self.userToBaseSorted[user][flagOfBase]  # 找到当前应该存储的基站,看看VQD4有没有这个基站，没有就存储一下。
                        while (((currentBase in self.VQD4[video][description]) == False) & (
                                isStored == False)):  # 对于这个视频的这个访问用户，视频还没有找到很好的存储地
                            if (flagOfBase >= self.sumOfBase):  # 所有基站的存储容量都用完了
                                return self.VQD4
                            if (self.VQS[video][description] > baseCapacity[currentBase]):
                                flagOfBase += 1
                                currentBase = self.userToBaseSorted[user][flagOfBase]

                            else:
                                self.VQD4[video][description].append(currentBase)
                                isStored = True
                                baseCapacity[currentBase] -= self.VQS[video][description]

    ''' 宏基站能够存储所有视频，用户在微基站覆盖范围内的，则访问微基站，微基站没有改视频，则访问宏基站
    确定视频描述的存储位置，首先宏基站存储一遍，对于每个微基站，找到覆盖范围内访问用户最多的基站，存储该视频'''

    def getVQD5(self):
        baseCapacity = copy.deepcopy(self.baseCapacity)  # self.BScapacity#每个基站的存储容量
        self.VQD5 = []
        for video in range(self.sumOfVideo):
            VQDVideo = []
            for description in range(len(self.VQS[video])):
                VQDVideo.append([0])
            self.VQD5.append(VQDVideo)
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
                    self.VQD5[currentVideo][description].append(base)
                    description += 1

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

    def getSortedBaseToUser(self):
        distance = []  # 计算基站到用户的距离
        for user in range(len(self.locationOfUser)):
            distance.append([])
            for base in range(len(self.locationOfBase)):
                currentDistance = ((self.locationOfBase[base][0] - self.locationOfUser[user][0]) ** 2 + (
                        self.locationOfBase[base][1] - self.locationOfUser[user][1]) ** 2) ** 0.5
                distance[user].append([base, currentDistance])
        for user in range(len(distance)):  # 横-用户 竖-基站
            userToBase = distance[user]
            userToBase.sort(key=lambda userToBase: userToBase[1])
        self.userToBaseSorted = []
        for user in range(len(distance)):
            self.userToBaseSorted.append([])
            for base in range(len(distance[user])):
                self.userToBaseSorted[user].append(distance[user][base][0])

    def getBaseVisitedOfUserVisitingVideoOfVQD5(self):
        self.baseVisitedOfUserVisitingVideo = []
        for user in range(self.sumOfUser):
            self.baseVisitedOfUserVisitingVideo.append([])
            for video in range(self.sumOfVideo):
                self.baseVisitedOfUserVisitingVideo[user].append([])
                if self.VN[video][user] == 1:
                    for description in range(len(self.VQD5[video])):
                        base = self.getBaseOfVQD5(user, self.VQD5[video][description])
                        self.baseVisitedOfUserVisitingVideo[user][video].append(base)

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

    def getBaseVisitedOfUserVisitingVideoOfVQD4(self):
        self.baseVisitedOfUserVisitingVideo = []
        for user in range(self.sumOfUser):
            self.baseVisitedOfUserVisitingVideo.append([])
            for video in range(self.sumOfVideo):
                self.baseVisitedOfUserVisitingVideo[user].append([])
                if (self.VN[video][user] == 1):
                    for description in range(len(self.VQD4[video])):
                        base = self.getBaseVQD4(self.userToBaseSorted[user], self.VQD4[video][description])
                        self.baseVisitedOfUserVisitingVideo[user][video].append(base)

    '''4.3'''

    def getBaseVQD4(self, userToBaseSorted, storedBase):
        for base in userToBaseSorted:
            if base in storedBase:
                return base
        return -1

    '''4.3每个基站的访问用户，Individual个体的初始化，分配基站的信道和功率时使用，由于VQD4存储方式和其他不一样，所以单独写个函数'''
    '''# userVideoDescription: 用户访问视频的描述时访问哪个基站'''

    def getBaseVisitedUserOfVQD45(self):  # user-video-description
        temp = []
        '''由于每个描述存储的地址是一个list，所以先求出video的所有描述存储地址，然后再进行合并'''
        for user in range(len(self.baseVisitedOfUserVisitingVideo)):
            temp.append([])  # user
            for video in range(len(self.baseVisitedOfUserVisitingVideo[user])):
                temp[user].extend(self.baseVisitedOfUserVisitingVideo[user][video])
        for user in range(len(temp)):
            temp[user] = list(set(temp[user]))
        self.basevisitedUE = []  # 横坐标i：基站，纵坐标j：用户
        for base in range(self.sumOfBase):
            self.basevisitedUE.append([])
        for user in range(len(temp)):
            for base in temp[user]:
                self.basevisitedUE[base].append(user)

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

    def getVideoImportance(self):  # 根据VN(每个视频的访问用户)，对视频的重要度排序，返回排序后的视频
        VideoImportance = []
        Sort_Video = []  # 返回的数组
        for i in range(len(self.VN)):
            VideoImportance.append(0)
            for j in range(len(self.VN[i])):
                if (self.VN[i][j] == 1):  # 代表用户j访问视频i
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
        self.basevisitedUE = []  # 横坐标base：基站，纵坐标user：用户
        for base in range(self.sumOfBase):
            self.basevisitedUE.append([])
            for video in range(len(temp_VQD)):  # 视频j，访问用户，没有重复元素
                for flagOfStoredBase in range(len(temp_VQD[video])):
                    if (temp_VQD[video][flagOfStoredBase] == base):  # 当前j视频的第k个描述存储在基站i上，找到这个视频的访问用户
                        for user in range(len(self.VN[video])):
                            if ((self.VN[video][user] == 1) and (user not in self.basevisitedUE[base])):
                                self.basevisitedUE[base].append(user)
            self.basevisitedUE[base].sort()

    # 1.创建种群 ()
    def creatPopulation(self):  # 创建种群
        print("***********创建种群*************")
        print("typeOfVQD: " + str(self.typeOfVQD))
        self.individualList = []
        for i in range(Population.sizeOfPopulation):
            self.individualList.append(
                Individual(self.tau, self.typeOfVQD, self.VQD, np.array(self.baseVisitedOfUserVisitingVideo),
                           self.sumOfBase, self.sumOfUser, self.sumOfVideo,
                           self.sumOfChannels, self.powerOfBase, self.baseRadius, self.Alpha, self.VN,
                           self.basevisitedUE, self.distanceUserToBase, self.VNTimes))

    # 2.交叉，返回空或者交叉之后的两个新个体，交叉操作已测试成功
    def crossover(self, individualForCross):  # individualForCross是一个数组，里面有两个个体
        if (random.random() < self.crossoverPc):  # 小于这个概率，执行交叉操作
            return individualForCross[0].crossover(individualForCross[1])  # 使用个体类自己的方法
        else:
            return []

    # 3.变异，传入参数是两个个体，返回变异之后的两个个体，有可能是原个体，有可能是新的个体
    def mutate(self, individualForMutate):  # individualForMutate，自己写，只有一个个体参数
        for i in range(2):
            if (random.random() < self.mutatePm):  # 小于mutatePm，执行变异操作
                individualForMutate[i].mutate()

    '''选择，根据种群适应值，选择两个个体，进行交叉，锦标赛选择法，
       随机产生两个样本，分别竞争第一组竞争'''

    def select(self):
        if len(self.individualList) < 2:
            print("种群个体列表长度小于2")
        competitors_1 = random.sample(self.individualList, 2)
        competitors_2 = random.sample(self.individualList, 2)
        fitness_1 = [competitors_1[0].getFitnessWithIntegral(), competitors_1[1].getFitnessWithIntegral()]
        fitness_2 = [competitors_2[0].getFitnessWithIntegral(), competitors_2[1].getFitnessWithIntegral()]
        '''选择适应大的个体去交叉'''
        father = competitors_1[1] if fitness_1[1] > fitness_1[0] else competitors_1[0]
        mather = competitors_2[1] if (fitness_2[1] > fitness_2[0]) else competitors_2[0]
        return [copy.deepcopy(father), copy.deepcopy(mather)]

    def getAllFitnessIntegral(self):
        fitnessList = []
        for i in range(self.sizeOfPopulation):
            fitnessList.append(self.individualList[i].getFitnessWithIntegral())
        return fitnessList
