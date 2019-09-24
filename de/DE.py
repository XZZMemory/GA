from de.Population import Population
def de():
    population = Population()  # 初始化
    population.initialization()  # 初始化网络拓扑，测试
    for i in range(population.iterations):
        '''执行de算法'''
        mutatedPpulation = population.mutate(population.individualList)
