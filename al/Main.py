from al.Matching import Matching
from al.Population import Population
from al.GA import GA

last = -1
current = 0
times = 0
population = Population()
tau = 0.00001
fileName = 'total.txt'
f = open(fileName, 'w')
while current - last > tau:
    if times == 0:
        matching = Matching()  # C、P
        matching.init(None, None, None, None, None)
        f.write(str(times + 1) + " matching before " + ": " + str(matching.getFitnessOfMatching()) + '\n')
        baseVisitedUEWithVideoBase = matching.matching()
        f.write(str(times + 1) + " matching end " + ": " + str(matching.getFitnessOfMatching()) + '\n')
        print("matching结束")
        ga = GA(baseVisitedUEWithVideoBase)
        CPResult = ga.runGa()
    else:
        matching = Matching()
        matching.init(CPResult[0], CPResult[1], baseVisitedUEWithVideoBase[1], baseVisitedUEWithVideoBase[2],
                      CPResult[3])  # C、P
        f.write(str(times + 1) + " matching before " + ": " + str(matching.getFitnessOfMatching()) + '\n')
        print("&&&&&&&&&&&&&&&&&&&&888888888888888888888888888888888888888888")
        print(matching.ansArray)
        #print(matching.asm_array)
        baseVisitedUEWithVideoBase = matching.matching()
        f.write(str(times + 1) + " matching end" + ": " + str(matching.getFitnessOfMatching()) + '\n')
        print("matching结束")
        ga = GA(baseVisitedUEWithVideoBase)
        CPResult = ga.runGa()
    print("GA结束")
    times = times + 1
    last = current
    current = CPResult[2]
    f.write(str(times) + " " + "GA: " + str(current) + '\n')
