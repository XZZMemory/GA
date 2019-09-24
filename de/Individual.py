import copy
import random


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
    #perFileName = "./data/picture/20190528-VQD5-2-picture.txt"
    '''个体中需要用到的：1.C、P的初始化 
                        2.个体的适应值计算
                        3.交叉 child1.crossover(child2)  return ([child1,child2])
                        4.变异 child.mutate return copyChild
                        修改:需要在初始化的时候，基站有剩余的存储容量，要存储多的视频，多存几遍视频'''
    '''初始化的时候加上population.方便传输参数'''

    def __init__(self, population, typeOfVQD):
        self.population = population
        '''（--------以下均是拷贝种群参数信息------'''
        self.baseList = copy.deepcopy(population.baseList)  # 拷贝基站和用户的坐标位置
        self.userList = copy.deepcopy(population.userList)
        self.sumOfBase = population.sumOfBase
        self.sumOfUser = population.sumOfUser
        self.sumOfVideo = population.sumOfVideo
        self.sumOfChannels = population.sumOfChannels
        self.VN = population.VN
        ''' 每个基站的访问用户，在个体初始化C、P时使用'''
        self.basevisitedUE = population.basevisitedUE
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
                distance = self.baseList[base].distanceToUser(self.userList[user])
                distance[user].append(int(distance))
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

            功率分配的从1开始有点太少了，应该计算出一个最小功率'''

    '''基站功率不满足条件，修正功率'''

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

    def getSINR(self):
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
                        f.write("基站： " + str(base) + "  信道： " + str(channel) + "信号与干扰比：" + str(S / I) + " 信噪比：" + str(
                            sinr) + " noise: " + str(Noise / self.Bias) + '\n')
                    else:
                        f.write("***********来自其他基站的干扰为0**************" + " 信噪比：" + str(sinr) + " noise: " + str(
                            Noise / self.Bias) + '\n')
                SINR[base].append(round(sinr, 9))
        return SINR

    def mutate(self):
        '''从种群中随机选择三个个体'''
        c=random.randint(0,)
        '''
         double[][] mutated_population = new double[population_size][param_num];
        for (int i = 0; i < population_size; i++) {
            /* Random.nextInt() 在一个范围内随机取一个整数 */
            int ind1 = rand.nextInt(population_size);
            int ind2 = rand.nextInt(population_size);
            int ind3 = rand.nextInt(population_size);
            while (ind1 == i || ind2 == i || ind3 == i
                    || ind1 == ind2 || ind1 == ind3 || ind2 == ind3) {
                ind1 = rand.nextInt(population_size);
                ind2 = rand.nextInt(population_size);
                ind3 = rand.nextInt(population_size);
            }

            /*一个个体的基因是从1-param_num，是一个个体，当前个体是i，编*/
            for (int j = 0; j < param_num; j++) {
                mutated_population[i][j] = population[ind1][j] + F * (population[ind2][j] - population[ind3][j]);
            }
        }

        return mutated_population;
        '''
        i=0
    def crossover(self):
        i=0
    def mutate(self):
        i=90
