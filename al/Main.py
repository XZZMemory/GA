from al.Matching import Matching
from al.Population import Population
from al.GA import GA
import time
import os


def writeConfigPath(configFilePath, sumOfBase, sumOfChannels, powerOfBase, locationOfBase, sumOfUser, locationOfUser,
                    sumOfVideo, baseCapacity, VNTimes, VN):
    fff = open(configFilePath, 'w')
    fff.write("sumOfBase:" + str(sumOfBase) + '\n')
    fff.write("sumOfChannels:" + str(sumOfChannels) + '\n')
    fff.write("powerOfBase:" + str(powerOfBase) + '\n')
    fff.write("locationOfBase:" + str(locationOfBase) + '\n')
    fff.write("sumOfUser:" + str(sumOfUser) + '\n')
    fff.write("locationOfUser:" + str(locationOfUser) + '\n')
    fff.write("sumOfVideo" + str(sumOfVideo) + '\n')
    fff.write("baseCapacity:" + str(baseCapacity) + '\n')
    fff.write("VNTimes:" + str(VNTimes) + '\n')
    fff.write("VN:" + str(VN) + '\n')


def test():
    i = 0
    '''if my_file.is_dir():
    # 指定的目录存在'''


last = -1
current = 0
tau = 0.00001

'''需要记录的信息：matchingtimes、GA的结果'''
dataTime = time.strftime("%Y%m%d", time.localtime())
totalTime = 4
k=1
dir = "./data/" + str(dataTime) + "-" + str(k)
os.mkdir(dir)
fileName = dir + '/result.txt'
f = open(fileName, 'w')
times = 1  # matching 和 ga执行次数
while current - last > tau:
    filePath = dir + "/" + str(times) + "-"
    maFilePath = filePath + "matching.txt"
    gaFilePath = filePath + "ga.txt"
    configFilePath = filePath + "config.txt"
    if times == 1:
        matching = Matching(maFilePath)  # C、P
        matching.init(None)
        f.write(str(times) + " matching before " + ": " + str(matching.getFitnessOfMatching()) + '\n')
        baseVisitedUEWithVideoBase = matching.matching()
        f.write(str(times) + " matching end " + ": " + str(matching.getFitnessOfMatching()) + '\n')
        print("matching结束")
    else:
        matching = Matching(maFilePath)
        matching.init(CPResult[3])  # C、P
        f.write(str(times) + " matching before " + ": " + str(matching.getFitnessOfMatching()) + '\n')
        baseVisitedUEWithVideoBase = matching.matching()
        f.write(str(times) + " matching end" + ": " + str(matching.getFitnessOfMatching()) + '\n')
        print("matching结束")
    ga = GA(baseVisitedUEWithVideoBase)
    CPResult = ga.runGa(gaFilePath)
    current = CPResult[2]
    while current < last:
        ga = GA(baseVisitedUEWithVideoBase)
        CPResult = ga.runGa(gaFilePath)
        current = CPResult[2]

    writeConfigPath(configFilePath, ga.population.sumOfBase, ga.population.sumOfChannels,
                    ga.population.powerOfBase, ga.population.locationOfBase, ga.population.sumOfUser,
                    ga.population.locationOfUser, ga.population.sumOfVideo, ga.population.baseCapacity,
                    ga.population.VNTimes, ga.population.VN)
    print("GA结束")
    last = current
    f.write(str(times) + " " + "GA: " + str(current) + '\n')
    times = times + 1
