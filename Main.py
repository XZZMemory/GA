# 程序入口
from Result import Result
import copy
from Painter import Painter
from Population import Population
import time


def ga(population, fileName, maxFitnessFile, typeOfVQD):
    population.initializationOfVQD(typeOfVQD)
    population.creatPopulation()  # 生成种群
    print(str(fileName) + " VQD: " + str(population.VQD))
    print("typeOfVQD: " + str(typeOfVQD))
    # 存储结果，用于绘图
    points = []
    maxFitness = -100
    minFitness = -100
    f = open(fileName, 'w')
    f.write(fileName + '\n')
    m = open(maxFitnessFile, 'w')
    m.write(maxFitnessFile + '\n')
    painter = Painter()
    painter.paintNetworkTopology(population.baseRadius, population.locationOfBase, population.locationOfUser,
                                 population.basevisitedUE, maxFitnessFile)
    '''存储结果，用于绘图，文件操作'''
    iterations = 1  # 当前迭代次数
    while (iterations <= population.iterations):
        fitness = population.getAllFitnessIntegral()
        maxFitness = max(maxFitness, max(fitness))
        minFitness = min(minFitness, min(fitness))
        print("代数：" + str(iterations) + "  最好值：" + str(maxFitness))
        m.write("iterations " + str(iterations) + ": " + str(maxFitness) + '\n')
        f.write("iterations " + str(iterations + 1) + '\n')
        f.write(str(fitness) + '\n')
        points.append([iterations, maxFitness])
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
            fit = tempIndividulalList[i].getFitnessWithIntegral()
            tempFitness.append(fit)
        for i in range(population.sizeOfPopulation):
            if tempIndividulalList == None:
                print(str(i) + "个体是空！")
                exit(1)
            if (tempFitness[i] > fitness[i]):
                population.individualList[i] = copy.deepcopy(tempIndividulalList[i])
        iterations += 1
    m.write(str(points) + '\n')
    f.close()
    m.close()
    # 返回画图所需的数据
    result = Result(fileName, minFitness, points, maxFitness)
    return result


def printTime(name, time):
    if time > 3:
        print(name + ": " + str(time))


# 程序从这开始执行
'''populationOfVQD2记录每代种群，每个个体的适应值，maxFitnessOfEachPopulationVQD2记录每代种群的最好适应值'''


def main2(dataTime):
    # 根据初始化参数，执行
    rootPath = "./data"
    # type:[1,5]
    list = [1, 2, 3, 4, 5]
    for type in list:
        fileName = dataTime + "-" + str(type) + "-VQD" + str(type) + ".txt"
        populationFitnessPath = rootPath + "/populationFitness/" + fileName
        maxFitnessPath = rootPath + "/maxFitness/" + fileName
        resultVQD = ga(population, populationFitnessPath, maxFitnessPath, type)
        print("画图数据")
        print("VQD" + str(type) + ".points " + str(resultVQD.points) + '\n')
        print("画收敛图")


population = Population()  # 初始化
population.initialization()  # 初始化网络拓扑，测试
# 初始化参数
dataTime = time.strftime("%Y%m%d", time.localtime())
main2(dataTime)
