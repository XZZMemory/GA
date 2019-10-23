from al.Matching import Matching
from al.Population import Population
from al.GA import GA
import time

last = -1
current = 0
times = 1
population = Population()
tau = 0.00001

'''需要记录的信息：matchingtimes、GA的结果'''
dataTime = time.strftime("%Y%m%d", time.localtime())
fileName = './' + str(dataTime) + '-result.txt'
f = open(fileName, 'w')
# dataTime_+times
while current - last > tau:
    filePath = "./" + str(dataTime) + "-" + str(times) + "-"
    maFilePath = filePath + "matching.txt"
    gaFilePath = filePath + "ga.txt"
    if times == 1:
        matching = Matching(maFilePath)  # C、P
        matching.init(None)
        f.write(str(times) + " matching before " + ": " + str(matching.getFitnessOfMatching()) + '\n')
        baseVisitedUEWithVideoBase = matching.matching()
        f.write(str(times) + " matching end " + ": " + str(matching.getFitnessOfMatching()) + '\n')
        print("matching结束")
        ga = GA(baseVisitedUEWithVideoBase)
        CPResult = ga.runGa(gaFilePath)
    else:
        matching = Matching(maFilePath)
        matching.init(CPResult[3])  # C、P
        f.write(str(times) + " matching before " + ": " + str(matching.getFitnessOfMatching()) + '\n')
        print("&&&&&&&&&&&&&&&&&&&&888888888888888888888888888888888888888888")
        print(matching.ansArray)
        baseVisitedUEWithVideoBase = matching.matching()
        f.write(str(times) + " matching end" + ": " + str(matching.getFitnessOfMatching()) + '\n')
        print("matching结束")
        ga = GA(baseVisitedUEWithVideoBase)
        CPResult = ga.runGa(gaFilePath)
    print("GA结束")
    last = current
    current = CPResult[2]
    f.write(str(times) + " " + "GA: " + str(current) + '\n')
    times = times + 1
