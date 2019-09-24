
import numpy as np
import matplotlib.pyplot as plt



fig = plt.figure()

ax = fig.add_subplot(111)

x = np.arange(0.0, 5.0, 0.01)
y = np.cos(2*np.pi*x)
ax.plot(x, y, lw = 2)

'''
    xy=(横坐标，纵坐标)  箭头尖端
    xytext=(横坐标，纵坐标) 文字的坐标，指的是最左边的坐标
    arrowprops= {
        facecolor= '颜色',
        shrink = '数字' <1  收缩箭头
    }

'''

ax.annotate('local max', xy=(2,1), xytext=(3,1.5),
            arrowprops=dict(facecolor='black', shrink=0.05)) #

ax.set_ylim(-2, 2) #设置y轴刻度的范围

plt.show()