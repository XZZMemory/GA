# 程序入口
from Result import Result
import copy
from Painter import Painter
from al.Population import Population
import time
import Utils


class GA:
    def __init__(self, basevisitedUEWithVideoBase):
        self.population = Population()  # 初始化
        self.population.initialization(basevisitedUEWithVideoBase[0], basevisitedUEWithVideoBase[1])  # 初始化网络拓扑，测试

    def runGa(self):
        # 根据初始化参数，执行
        dataTime = time.strftime("%Y%m%d", time.localtime())
        rootPath = "./data"
        fileName = dataTime + "-matching"  ".txt"
        populationFitnessPath = rootPath + "/populationFitness/" + fileName
        maxFitnessPath = rootPath + "/maxFitness/" + fileName
        resultVQD = self.ga(self.population, populationFitnessPath, maxFitnessPath)
        print("画图数据")
        print("VQD" + str(type) + ".points " + str(resultVQD.points) + '\n')
        print("画收敛图")

    def ga(self, population, fileName, maxFitnessFile):
        population.creatPopulation()  # 生成种群
        # 存储结果，用于绘图
        points = []
        #f = open(fileName, 'w')
        #f.write(fileName + '\n')
        #m = open(maxFitnessFile, 'w')
        #m.write(maxFitnessFile + '\n')
        painter = Painter()
        painter.paintNetworkTopology(population.baseRadius, population.locationOfBase, population.locationOfUser,
                                     population.basevisitedUE, maxFitnessFile)
        '''存储结果，用于绘图，文件操作'''
        iterations = 1  # 当前迭代次数
        while (iterations <= population.iterations):
            fitness = population.getAllFitnessIntegral()
            maxFitnessInCurrentPopulation = max(fitness)
            print("当前迭代的代数：" + str(iterations) + "   当前种群适应值最好的：" + str(maxFitnessInCurrentPopulation))
            if iterations == 1:
                maxFitness = maxFitnessInCurrentPopulation
            else:
                maxFitness = maxFitness if maxFitness > maxFitnessInCurrentPopulation else maxFitnessInCurrentPopulation
            #m.write(str(iterations) + ": " + str(maxFitnessInCurrentPopulation) + '\n')
            #f.write(str(iterations + 1) + '\n')
            #f.write(str(fitness) + '\n')
            points.append([iterations, maxFitnessInCurrentPopulation])
            tempIndividulalList = []
            while (len(tempIndividulalList) < population.sizeOfPopulation):
                individualForCrossover = population.select()  # 选择--锦标赛选择法
                if len(individualForCrossover) != 2:
                    print("select error! " + str(len(individualForCrossover)))
                    exit(1)
                individualForMutate = population.crossover(individualForCrossover)  # 交叉随机点位的交叉操作，交叉完毕之后判断是否满足约束
                if (len(individualForMutate) == 2):
                    population.mutate(individualForCrossover)
                    for i in range(len(individualForCrossover)):
                        tempIndividulalList.append(individualForCrossover[i])
            tempFitness = []
            for i in range(len(tempIndividulalList)):
                fit = tempIndividulalList[i].getFitnessOfMatching()
                tempFitness.append(fit)
            for i in range(population.sizeOfPopulation):
                if tempIndividulalList == None:
                    print(str(i) + "个体是空！")
                    exit(1)
                if (tempFitness[i] > fitness[i]):
                    population.individualList[i] = copy.deepcopy(tempIndividulalList[i])
            iterations += 1
        print("GA结束后适应值最大的个体信道分配情况")
        fitness = population.getAllFitnessIntegral()
        index = Utils.getImportant(fitness)

        for i in range(len(population.individualList[0].C)):
            print(str(population.individualList[0].C[i]))
        print("population.individualList:" + str(population.individualList))
        #m.write(str(points) + '\n')
        #f.close()
        #m.close()
        return [population.individualList[index].C, population.individualList[index].P]
