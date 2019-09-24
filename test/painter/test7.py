import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle



def paintCircle():
    coverArea = [500, 100, 100, 100, 100, 100, 100]
    locationOfBase = [[0, 0], [346, 200], [0, 400], [-346, 200], [-346, -200], [0, -400], [346, -200]]
    for base in range(len(locationOfBase)):
        # ==========================================
        # 圆的基本信息
        # 1.圆半径
        r = coverArea[base]
        # 2.圆心坐标
        a, b = (locationOfBase[0], locationOfBase[1])
        # ==========================================
        # 方法一：参数方程
        theta = np.arange(0, 2 * np.pi, 0.01)
        x = a + r * np.cos(theta)
        y = b + r * np.sin(theta)
        fig = plt.figure()
        axes = fig.add_subplot(111)
        axes.plot(x, y)
        axes.axis('equal')
        plt.title('www.jb51.net')
        # ==========================================


def plot_data():
    coverArea = [500, 100, 100, 100, 100, 100, 100]
    locationOfBase = [[0, 0], [346, 200], [0, 400], [-346, 200], [-346, -200], [0, -400], [346, -200]]
    plt.figure(2)
    plt.title("GA", fontsize=24)
    plt.xlabel("x", fontsize=14)
    plt.ylabel("y", fontsize=14)
    plt.scatter(np.array(locationOfBase)[:, 0], np.array(locationOfBase)[:, 1], marker='.', c='red',
                label="base",
                s=50)  # marker定义形状，label与plt.legend画出右上角图例

    plt.scatter(np.array(locationOfUser)[:, 0], np.array(locationOfUser)[:, 1], marker='*', c='green',
                label="user",
                s=10)  # marker定义形状，label与plt.legend画出右上角图例
    plt.axis([-600, 600, -600, 600])
    plt.legend(
        loc='upper right')  # center left lower right right upper center lower center center right lower left best.....
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ell1 = Ellipse(xy=(0.0, 0.0), width=4, height=8, angle=30.0, facecolor='yellow', alpha=0.3)
    cir1 = Circle(xy=(0.0, 0.0), radius=2, alpha=0.5)
    ax.add_patch(ell1)
    ax.add_patch(cir1)

    x, y = 0, 0
    ax.plot(x, y, 'ro')

    plt.axis('scaled')
    # ax.set_xlim(-4, 4)
    # ax.set_ylim(-4, 4)
    plt.axis('equal')  # changes limits of x or y axis so that equal increments of x and y have the same length

    plt.show()


plot_data()
