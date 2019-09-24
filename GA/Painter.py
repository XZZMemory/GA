'''
需要画图，基站位置，用户位置
生成之后再画图，
'''

import numpy
from matplotlib.patches import Ellipse, Circle
import matplotlib.pyplot as plt


class Painter:
    def paint(self, resultVQD1, resultVQD2, resultVQD3, resultVQD4, iterations):
        maxFitness = []
        maxFitness.append(resultVQD1.maxFitness)
        maxFitness.append(resultVQD2.maxFitness)
        maxFitness.append(resultVQD3.maxFitness)
        maxFitness.append(resultVQD4.maxFitness)
        minFitness = []
        minFitness.append(resultVQD1.minFitness)
        minFitness.append(resultVQD2.minFitness)
        minFitness.append(resultVQD3.minFitness)
        minFitness.append(resultVQD4.minFitness)
        plt.figure(2)
        plt.title("GA", fontsize=24)
        plt.xlabel("iterations", fontsize=14)
        plt.ylabel("fitness", fontsize=14)
        plt.scatter(numpy.array(resultVQD1.points)[:, 0], numpy.array(resultVQD1.points)[:, 1], marker='.', c='black',
                    label=resultVQD1.fileName,
                    s=1)  # marker定义形状，label与plt.legend画出右上角图例

        plt.scatter(numpy.array(resultVQD2.points)[:, 0], numpy.array(resultVQD2.points)[:, 1], marker='.', c='green',
                    label=resultVQD2.fileName,
                    s=1)  # marker定义形状，label与plt.legend画出右上角图例
        plt.scatter(numpy.array(resultVQD3.points)[:, 0], numpy.array(resultVQD3.points)[:, 1], marker='.', c='blue',
                    label=resultVQD3.fileName,
                    s=1)  # marker定义形状，label与plt.legend画出右上角图例
        plt.scatter(numpy.array(resultVQD4.points)[:, 0], numpy.array(resultVQD4.points)[:, 1], marker='.', c='red',
                    label=resultVQD4.fileName,
                    s=1)  # marker定义形状，label与plt.legend画出右上角图例
        plt.axis([0, iterations, min(minFitness) - 1, max(maxFitness) + 2])
        plt.legend(
            loc='upper right')  # center left lower right right upper center lower center center right lower left best.....
        plt.show()

    # fileName,maxFitness,points)
    def paint34(self, resultVQD3, resultVQD4, iterations):
        maxFitness = []
        maxFitness.append(resultVQD3.maxFitness)
        maxFitness.append(resultVQD4.maxFitness)
        minFitness = []
        minFitness.append(resultVQD3.minFitness)
        minFitness.append(resultVQD4.minFitness)
        plt.figure(2)
        plt.title("GA", fontsize=24)
        plt.xlabel("iterations", fontsize=14)
        plt.ylabel("fitness", fontsize=14)
        plt.scatter(numpy.array(resultVQD3.points)[:, 0], numpy.array(resultVQD3.points)[:, 1], marker='.', c='blue',
                    label=resultVQD3.fileName,
                    s=1)  # marker定义形状，label与plt.legend画出右上角图例
        plt.scatter(numpy.array(resultVQD4.points)[:, 0], numpy.array(resultVQD4.points)[:, 1], marker='.', c='red',
                    label=resultVQD4.fileName,
                    s=1)  # marker定义形状，label与plt.legend画出右上角图例
        plt.axis([0, iterations, min(minFitness) - 1, max(maxFitness) + 1])
        plt.legend(
            loc='upper right')  # center left lower right right upper center lower center center right lower left best.....
        plt.show()

    def paintOne(self, resultVQD, iterations):
        maxFitness = []
        maxFitness.append(resultVQD.maxFitness)
        minFitness = []
        minFitness.append(resultVQD.minFitness)
        plt.figure(2)
        plt.title("GA", fontsize=24)
        plt.xlabel("iterations", fontsize=14)
        plt.ylabel("fitness", fontsize=14)
        fileName = resultVQD.fileName
        plt.scatter(numpy.array(resultVQD.points)[:, 0], numpy.array(resultVQD.points)[:, 1], marker='.', c='blue',
                    label=fileName[len(fileName) - 8:len(fileName) - 4],
                    s=1)  # marker定义形状，label与plt.legend画出右上角图例
        plt.axis([0, iterations, min(minFitness) - 1, max(maxFitness) + 1])
        plt.legend(
            loc='upper right')  # center left lower right right upper center lower center center right lower left best.....
        plt.show()
        # plt.savefig(fileName[1:len(fileName) - 4] + ".png")

    def paintNetworkTopology(self, baseCoverArea, locationOfBase, locationOfUser, basevisitedUE, fileName):
        for base in range(len(basevisitedUE)):
            print("base: " + str(base) + " user: " + str(basevisitedUE[base]))
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for base in range(len(locationOfBase)):
            if base == 0:
                cir2 = Circle(xy=(locationOfBase[base][0], locationOfBase[base][1]), radius=baseCoverArea[base],
                              alpha=0.5,
                              color='gray')
            else:
                cir2 = Circle(xy=(locationOfBase[base][0], locationOfBase[base][1]), radius=baseCoverArea[base],
                              alpha=0.5,
                              color='gray')
            '''
            cir3 = Circle(xy=(locationOfBase[base][0], locationOfBase[base][1]), radius=5, alpha=0.5,
                          color='black')
            ax.add_patch(cir3)
            '''
            ax.add_patch(cir2)
        for user in range(len(locationOfUser)):
            cir2 = Circle(xy=(locationOfUser[user][0], locationOfUser[user][1]), radius=5, alpha=0.5, color='red')
            ax.add_patch(cir2)
        for base in range(len(basevisitedUE)):
            for user in basevisitedUE[base]:
                ax.annotate("",
                            xy=(locationOfBase[base][0], locationOfBase[base][1]), xycoords='data',
                            xytext=(locationOfUser[user][0], locationOfUser[user][1]), textcoords='data',
                            arrowprops=dict(arrowstyle="-",
                                            connectionstyle="arc3"),
                            )

        ell1 = Ellipse(xy=(0.0, 0.0), width=4, height=8, angle=30.0, facecolor='yellow', alpha=0.3)
        ax.add_patch(ell1)
        ell1 = Ellipse(xy=(0.0, 0.0), width=4, height=8, angle=30.0, facecolor='yellow', alpha=0.3)
        ax.add_patch(ell1)
        x, y = 0, 0
        ax.plot(x, y, 'ro')
        plt.axis('scaled')
        plt.axis('equal')  # changes limits of x or y axis so that equal increments of x and y have the same length
        plt.show()
        # './png/data/maxFitness/20190513-1-VQD4-NetworkTopology.png'

    def paint9(self):
        points = [[0, 35.99972526544358], [1, 36.999245344915586], [2, 37.99851896670715], [3, 37.99851896670715], [4, 38.99851389104737], [5, 38.99851389104737], [6, 40.998465598338115], [7, 40.998465598338115], [8, 40.998465598338115], [9, 40.998465598338115]]


        iterations = 100

        plt.figure(2)
        plt.title("GA", fontsize=24)
        plt.xlabel("iterations", fontsize=14)
        plt.ylabel("fitness", fontsize=14)
        plt.scatter(numpy.array(points)[:, 0], numpy.array(points)[:, 1], marker='.', c='blue',
                    label="VQD:4",
                    s=1)  # marker定义形状，label与plt.legend画出右上角图例
        plt.axis([0, iterations, 20, 70])
        plt.legend(
            loc='upper right')  # center left lower right right upper center lower center center right lower left best.....
        plt.show()

    def paint10(self):
        locationOfBase = [[50, 50], [0, 0], [0, 100], [100, 0], [100, 100]]  # 基站位置初始化
        locationOfUser = [[25, 0], [50, 0], [75, 0], [0, 25], [0, 50], [0, 75], [25, 25], [25, 50],
                          [75, 50]]  # 用户位置初始化
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for base in range(len(locationOfBase)):
            if base == 0:
                cir2 = Circle(xy=(locationOfBase[base][0], locationOfBase[base][1]), radius=500,
                              alpha=0.5,
                              color='gray')
            else:
                cir2 = Circle(xy=(locationOfBase[base][0], locationOfBase[base][1]), radius=100,
                              alpha=0.5,
                              color='green')
            cir3 = Circle(xy=(locationOfBase[base][0], locationOfBase[base][1]), radius=5, alpha=0.5,
                          color='black')
            ax.add_patch(cir3)
            ax.add_patch(cir2)
        for user in range(len(locationOfUser)):
            cir2 = Circle(xy=(locationOfUser[user][0], locationOfUser[user][1]), radius=10, alpha=0.5)
            ax.add_patch(cir2)

        ell1 = Ellipse(xy=(0.0, 0.0), width=4, height=8, angle=30.0, facecolor='yellow', alpha=0.3)
        ax.add_patch(ell1)
        ell1 = Ellipse(xy=(0.0, 0.0), width=4, height=8, angle=30.0, facecolor='yellow', alpha=0.3)
        ax.add_patch(ell1)
        x, y = 0, 0
        ax.plot(x, y, 'ro')
        plt.axis('scaled')
        plt.axis('equal')  # changes limits of x or y axis so that equal increments of x and y have the same length
        plt.show()

    def paintBasesAndUsers(self, locationOfBase, locationOfUser):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for base in range(len(locationOfBase)):
            if base == 0:
                cir2 = Circle(xy=(locationOfBase[base][0], locationOfBase[base][1]), radius=500,
                              alpha=0.5,
                              color='gray')
            else:
                cir2 = Circle(xy=(locationOfBase[base][0], locationOfBase[base][1]), radius=100,
                              alpha=0.5,
                              color='green')
            cir3 = Circle(xy=(locationOfBase[base][0], locationOfBase[base][1]), radius=5, alpha=0.5,
                          color='black')
            ax.add_patch(cir3)
            ax.add_patch(cir2)
        for user in range(len(locationOfUser)):
            cir2 = Circle(xy=(locationOfUser[user][0], locationOfUser[user][1]), radius=10, alpha=0.5)
            ax.add_patch(cir2)

        ell1 = Ellipse(xy=(0.0, 0.0), width=4, height=8, angle=30.0, facecolor='yellow', alpha=0.3)
        ax.add_patch(ell1)
        ell1 = Ellipse(xy=(0.0, 0.0), width=4, height=8, angle=30.0, facecolor='yellow', alpha=0.3)
        ax.add_patch(ell1)
        x, y = 0, 0
        ax.plot(x, y, 'ro')
        plt.axis('scaled')
        plt.axis('equal')  # changes limits of x or y axis so that equal increments of x and y have the same length
        plt.show()

    def paintNetworkTopology1(self):
        VN = [[1, -1, 1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, 1, -1, 1],
              [1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, -1, -1, 1],
              [-1, -1, 1, 1, -1, -1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1],
              [-1, 1, 1, 1, 1, 1, 1, 1, -1, 1, -1, -1, 1, 1, 1, -1, 1, -1, -1, -1]]
        sum = 0
        for video in range(len(VN)):
            if VN[video][17] == 1:
                print(str(video))
                sum += 1
        print(sum)
        baseCoverArea = [500, 100, 100, 100, 100, 100, 100]
        locationOfBase = [[0, 0], [346, 200], [0, 400], [-346, 200], [-346, -200], [0, -400], [346, -200]]

        locationOfUser = [[337.2631696625841, 250.2445139240397], [-341.94661511724223, -36.63797744242588],
                          [-274.49708673772585, 159.2435408201836], [-20, 377.85831021712113],
                          [-149.76468697372144, 344.4262640065619], [-487, -65],
                          [67.35214258872664, 113.99694915282447], [147, 352],
                          [-120.53587670222394, -388.2839154549412], [-145.51818802384983, -68],
                          [-239.98934669846153, 370.5932928423781], [-128, 234.89338992927946],
                          [431.70313500687996, -191.4812147540513], [-335, 192],
                          [145.8211788904833, 250.25655756158767], [79.33030867625578, -120.10491641757523],
                          [-252.6934480137271, -402.22348031537666], [337.05888317443726, 159.12791180485462],
                          [-216.73973223345803, 124.46229396333888],
                          [-114.24179725841555, -40.547156953680194]]  # 用户位置初始化
        basevisitedUE = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 19], [17], [], [2, 13], [], [],
                         [12]]
        o = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 19], [17], [], [2], [], [], [12]]
        print(str(locationOfUser[17]))
        print(str(locationOfBase[1]))
        for user in range(len(locationOfUser)):
            print("user: " + str(user) + " location: " + str(locationOfUser[user]))
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for base in range(len(locationOfBase)):
            if base == 0:
                cir2 = Circle(xy=(locationOfBase[base][0], locationOfBase[base][1]), radius=baseCoverArea[base],
                              alpha=0.5,
                              color='gray')
            else:
                cir2 = Circle(xy=(locationOfBase[base][0], locationOfBase[base][1]), radius=baseCoverArea[base],
                              alpha=0.5,
                              color='gray')
            '''
            cir3 = Circle(xy=(locationOfBase[base][0], locationOfBase[base][1]), radius=5, alpha=0.5,
                          color='black')
            ax.add_patch(cir3)
            '''
            ax.add_patch(cir2)
        for user in range(len(locationOfUser)):
            cir2 = Circle(xy=(locationOfUser[user][0], locationOfUser[user][1]), radius=5, alpha=0.5, color='red')
            ax.add_patch(cir2)
        for base in range(len(basevisitedUE)):
            for user in basevisitedUE[base]:
                ax.annotate("",
                            xy=(locationOfBase[base][0], locationOfBase[base][1]), xycoords='data',
                            xytext=(locationOfUser[user][0], locationOfUser[user][1]), textcoords='data',
                            arrowprops=dict(arrowstyle="-",
                                            connectionstyle="arc3"),
                            )

        ell1 = Ellipse(xy=(0.0, 0.0), width=4, height=8, angle=30.0, facecolor='yellow', alpha=0.3)
        ax.add_patch(ell1)
        ell1 = Ellipse(xy=(0.0, 0.0), width=4, height=8, angle=30.0, facecolor='yellow', alpha=0.3)
        ax.add_patch(ell1)
        x, y = 0, 0
        ax.plot(x, y, 'ro')
        plt.axis('scaled')
        plt.axis('equal')  # changes limits of x or y axis so that equal increments of x and y have the same length
        plt.show()

    # './png/data/maxFitness/20190513-1-VQD4-NetworkTopology.png'

    def paintNetworkTopology9(self):
        VN = [[1, -1, 1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, 1, -1, 1],
              [1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, -1, -1, 1],
              [-1, -1, 1, 1, -1, -1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1],
              [-1, 1, 1, 1, 1, 1, 1, 1, -1, 1, -1, -1, 1, 1, 1, -1, 1, -1, -1, -1]]
        sum = 0
        for video in range(len(VN)):
            if VN[video][17] == 1:
                print(str(video))
                sum += 1
        print(sum)
        baseCoverArea = [500, 100, 100, 100, 100, 100, 100]
        locationOfBase = [[0, 0], [346, 200], [0, 400], [-346, 200], [-346, -200], [0, -400], [346, -200]]

        locationOfUser = [[337.2631696625841, 250.2445139240397], [-341.94661511724223, -36.63797744242588],
                          [-274.49708673772585, 159.2435408201836], [-20, 377.85831021712113],
                          [-149.76468697372144, 344.4262640065619], [-487, -65],
                          [67.35214258872664, 113.99694915282447], [147, 352],
                          [-120.53587670222394, -388.2839154549412], [-145.51818802384983, -68],
                          [-239.98934669846153, 370.5932928423781], [-128, 234.89338992927946],
                          [431.70313500687996, -191.4812147540513], [-335, 192],
                          [145.8211788904833, 250.25655756158767], [79.33030867625578, -120.10491641757523],
                          [-252.6934480137271, -402.22348031537666], [337.05888317443726, 159.12791180485462],
                          [-216.73973223345803, 124.46229396333888],
                          [-114.24179725841555, -40.547156953680194]]  # 用户位置初始化
        print(str(locationOfUser[17]))
        print(str(locationOfBase[1]))
        for user in range(len(locationOfUser)):
            print("user: " + str(user) + " location: " + str(locationOfUser[user]))
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for base in range(len(locationOfBase)):
            if base == 0:
                cir2 = Circle(xy=(locationOfBase[base][0], locationOfBase[base][1]), radius=baseCoverArea[base],
                              alpha=0.5,
                              color='gray')
            else:
                cir2 = Circle(xy=(locationOfBase[base][0], locationOfBase[base][1]), radius=baseCoverArea[base],
                              alpha=0.5,
                              color='gray')
            ax.add_patch(cir2)
        for user in range(len(locationOfUser)):
            cir2 = Circle(xy=(locationOfUser[user][0], locationOfUser[user][1]), radius=5, alpha=0.5, color='red')
            ax.add_patch(cir2)

        ell1 = Ellipse(xy=(0.0, 0.0), width=4, height=8, angle=30.0, facecolor='yellow', alpha=0.3)
        ax.add_patch(ell1)
        ell1 = Ellipse(xy=(0.0, 0.0), width=4, height=8, angle=30.0, facecolor='yellow', alpha=0.3)
        ax.add_patch(ell1)
        x, y = 0, 0
        ax.plot(x, y, 'ro')
        plt.axis('scaled')
        plt.axis('equal')  # changes limits of x or y axis so that equal increments of x and y have the same length
        plt.show()
    def paint22(self):
        points=[[0, 35.99972526544358], [1, 36.999245344915586], [2, 37.99851896670715], [3, 37.99851896670715], [4, 38.99851389104737], [5, 38.99851389104737], [6, 40.998465598338115], [7, 40.998465598338115], [8, 40.998465598338115], [9, 40.998465598338115]]

        plt.figure(2)
        plt.title("GA", fontsize=24)
        plt.xlabel("iterations", fontsize=14)
        plt.ylabel("fitness", fontsize=14)
        plt.scatter(numpy.array(points)[:, 0], numpy.array(points)[:, 1], marker='.', c='black',
                    label="name",
                    s=1)  # marker定义形状，label与plt.legend画出右上角图例


        plt.axis([0, 12, 0, 50])
        plt.legend(
            loc='upper right')  # center left lower right right upper center lower center center right lower left best.....
        plt.show()

pa = Painter()
pa.paint22()
