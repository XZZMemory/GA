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
        return resultVQD
        print("GA结束")

    def ga(self, population, fileName, maxFitnessFile):
        population.creatPopulation()  # 生成种群
        points = []
        painter = Painter()
        painter.paintNetworkTopology(population.baseRadius, population.locationOfBase, population.locationOfUser,
                                     population.basevisitedUE, maxFitnessFile)
        '''存储结果，用于绘图，文件操作'''
        iterations = 1  # 当前迭代次数
        while (iterations <= population.iterations):
            fitness = population.getAllFitnessIntegral()
            maxFitnessInCurrentPopulation = max(fitness)
            print("代数：" + str(iterations) + "  最好值：" + str(maxFitnessInCurrentPopulation))
            if iterations == 1:
                maxFitness = maxFitnessInCurrentPopulation
            else:
                maxFitness = maxFitness if maxFitness > maxFitnessInCurrentPopulation else maxFitnessInCurrentPopulation
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
        fitness = population.getAllFitnessIntegral()
        index = Utils.getImportant(fitness)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%9090909090")
        print(population.individualList[index].getFitnessOfMatching())
        print("asm_array: " + str(population.individualList[index].asm_array))
        print("ansArray: " + str(population.individualList[index].ansArray))
        print("VN： " + str(population.VN))
        print("C: " + str(population.individualList[index].C))
        print("P: " + str(population.individualList[index].P))
        return [population.individualList[index].C, population.individualList[index].P, fitness[index],
                population.individualList[index].ansArray]
