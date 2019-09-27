# 程序入口
from Result import Result
import copy
from Painter import Painter
from Population import Population
import time


def ga(population, fileName, maxFitnessFile, typeOfVQD):
    print("验证参数：" + "population:" + str(population))
    print("population.individualList:" + str(population.individualList))
    print("验证参数完毕")
    population.initializationOfVQD(typeOfVQD)
    population.creatPopulation()  # 生成种群
    print(str(fileName) + " VQD: " + str(population.VQD))
    print("typeOfVQD: " + str(typeOfVQD))
    print("初始化时个体0的信道分配情况")
    for i in range(len(population.individualList[0].C)):
        print(str(population.individualList[0].C[i]))
    print("初始化时个体0的功率分配情况")
    for i in range(len(population.individualList[0].P)):
        print(str(population.individualList[0].P[i]))
    print("population.individualList:" + str(population.individualList))
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
        maxFitnessInCurrentPopulation = getMaxNum(fitness)
        print("当前迭代的代数：" + str(iterations) + "   当前种群适应值最好的：" + str(maxFitnessInCurrentPopulation))
        minFitnessInCurrentPopulation = getMinNum(fitness)
        if iterations == 1:
            maxFitness = maxFitnessInCurrentPopulation
            minFitness = minFitnessInCurrentPopulation
        else:
            maxFitness = maxFitness if maxFitness > maxFitnessInCurrentPopulation else maxFitnessInCurrentPopulation
            minFitness = minFitness if minFitness < maxFitnessInCurrentPopulation else minFitnessInCurrentPopulation
        m.write("iterations " + str(iterations) + ": " + str(maxFitnessInCurrentPopulation) + '\n')
        f.write("iterations " + str(iterations + 1) + '\n')
        f.write(str(fitness) + '\n')
        points.append([iterations, maxFitnessInCurrentPopulation])
        tempIndividulalList = []
        while (len(tempIndividulalList) < population.sizeOfPopulation):
            individualForCrossover = population.select()  # 选择--锦标赛选择法
            if len(individualForCrossover) != 2:
                print("select error! " + str(len(individualForCrossover)))
                exit(1)
            individualForMutate = population.crossover(individualForCrossover)  # 交叉随机点位的交叉操作，交叉完毕之后判断是否满足约束
            '''
                         if len(individualForCrossover) != 2:
                print("cross error! " + str(len(individualForCrossover)))
                exit(1)
             交叉-返回的个体可能是空也可能交叉了，改成交叉返回的个体一定有两个，只有经过交叉的两个个体才可能变异
             变异 基本位变异，变异完毕之后判断是否满足约束条件
             3.变异，传入参数是两个个体，返回变异之后的两个个体，有可能是原个体，有可能是新的个体 '''
            if (len(individualForMutate) == 2):
                population.mutate(individualForCrossover)
                for i in range(len(individualForCrossover)):
                    tempIndividulalList.append(individualForCrossover[i])
        tempFitness = []
        for i in range(len(tempIndividulalList)):
            fit = tempIndividulalList[i].getFitnessWithIntegral()
            tempFitness.append(fit)
        for i in range(population.sizeOfPopulation):
            # mat = "{:40}\t{:30}\t{:40}\t{:30}"
            mat2 = "{:30}\t{:30}"
            if tempIndividulalList == None:
                print(str(i) + "个体是空！")
                exit(1)
            # print(mat.format(str(population.individualList[i]), "GA前的个体适应值 " + str(fitness[i]),str(tempIndividulalList[i]), "GA后的个体适应值" + str(tempFitness[i])))
            print(mat2.format("GA前的个体适应值 " + str(fitness[i]), "GA后的个体适应值" + str(tempFitness[i])))
            # fitness 是和 population.individualList[i].getFitness()对应的
            if (tempFitness[i] > fitness[i]):
                population.individualList[i] = copy.deepcopy(tempIndividulalList[i])
        iterations += 1
    print("GA结束后个体0的信道分配情况")
    for i in range(len(population.individualList[0].C)):
        print(str(population.individualList[0].C[i]))
    print("population.individualList:" + str(population.individualList))
    m.write(str(points) + '\n')
    f.close()
    m.close()
    # 返回画图所需的数据
    result = Result(fileName, minFitness, points, maxFitness)
    return result


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


def printTime(name, time):
    if time > 3:
        print(name + ": " + str(time))


# 程序从这开始执行
'''populationOfVQD2记录每代种群，每个个体的适应值，maxFitnessOfEachPopulationVQD2记录每代种群的最好适应值'''


def main2(dataTime):
    # 根据初始化参数，执行
    rootPath = "./data"
    # type:[1,5]
    for type in range(3, 6):
        fileName = dataTime + "-" + str(type) + "-VQD" + str(type) + ".txt"
        populationFitnessPath = rootPath + "/populationFitness/" + fileName
        maxFitnessPath = rootPath + "/maxFitness/" + fileName
        resultVQD = ga(population, populationFitnessPath, maxFitnessPath, type)
        print("画图数据")
        print("VQD" + str(type) + ".points " + str(resultVQD.points) + '\n')
        print("画收敛图")
        # painter = Painter()
        # painter.paintOne(resultVQD, population.iterations)


population = Population()  # 初始化
population.initialization()  # 初始化网络拓扑，测试
# 初始化参数
dataTime = time.strftime("%Y%m%d", time.localtime())
main2(dataTime)
