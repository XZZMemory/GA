###################################
#   coding=utf-8
#   !/usr/bin/env python
#   __author__ = 'pipi'
#   ctime 2014.10.11
#   绘制椭圆和圆形
###################################
from matplotlib.patches import Ellipse, Circle
import matplotlib.pyplot as plt


def paintNetworkTopology(coverArea, locationOfBase, locationOfUser, basevisitedUE):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for base in range(len(locationOfBase)):
        if base == 0:
            cir2 = Circle(xy=(locationOfBase[base][0], locationOfBase[base][1]), radius=coverArea[base], alpha=0.5,
                          color='gray')
        else:
            cir2 = Circle(xy=(locationOfBase[base][0], locationOfBase[base][1]), radius=coverArea[base], alpha=0.5,
                          color='green')
        ax.add_patch(cir2)
    for user in range(len(locationOfUser)):
        cir2 = Circle(xy=(locationOfUser[user][0], locationOfUser[user][1]), radius=5, alpha=0.5)
        ax.add_patch(cir2)
    for base in range(len(basevisitedUE)):
        for user in range(len(basevisitedUE[base])):
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
