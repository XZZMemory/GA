from al.Matching import Matching
from al.Population import Population

last = 0
matching = Matching()
matching.matching()
f = matching.getFitnessOfMatching()
current = 1
times = 0
population = Population()
while True:
    if times == 0:
        matching = Matching()
        matching.init(None, None)  # C、P
        result = matching.matching()
        population.initialization()
        CPResult = population.creatPopulation(result[0], result[1])
        times = 1
    else:
        matching = Matching()
        matching.init(CPResult[0], CPResult[1])  # C、P
        result = matching.matching()
        population.initialization()
        CPResult = population.creatPopulation(result[0], result[1])
