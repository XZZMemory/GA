class Result:
    points = []
    maxFitness = 0
    fileName = ""
    minFitness = 0

    def __init__(self, fileName, maxFitness, points, minFitness):
        self.points = points
        self.maxFitness = maxFitness
        self.fileName = fileName
        self.minFitness = minFitness
