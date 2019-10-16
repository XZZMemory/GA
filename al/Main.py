from al.Matching import Matching
from al.Population import Population
from al.GA import GA

last = -1
current = 0
times = 0
population = Population()
tau = 0.00001
while current - last > tau:
    if times == 0:
        matching = Matching() # C、P
        baseVisitedUEWithVideoBase = matching.matching()
        ga = GA(baseVisitedUEWithVideoBase)
        CPResult = ga.runGa()
        print("**************")
        print(CPResult[0])
        print(CPResult[1])
        times = 1
    else:
        matching = Matching()
        matching.init(CPResult[0], CPResult[1])  # C、P
        baseVisitedUEWithVideoBase = matching.matching()
        ga = GA(baseVisitedUEWithVideoBase)
        CPResult = ga.runGa()
        population.initialization(baseVisitedUEWithVideoBase[0], baseVisitedUEWithVideoBase[1])
        CPResult = population.creatPopulation()
