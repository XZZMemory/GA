# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    samples_num = 60
    radius=500
    t = np.random.random(size=samples_num) * 2 * np.pi - np.pi
    x = np.cos(t)
    y = np.sin(t)
    i_set = np.arange(0, samples_num, 1)
    for i in i_set:
        len = np.sqrt(np.random.random())
        x[i] = x[i] * len*radius
        y[i] = y[i] * len*radius
    plt.figure(figsize=(10, 10.1), dpi=125)
    plt.plot(x, y, 'ro')
    _t = np.arange(0, 7, 0.1)
    _x = np.cos(_t)
    _y = np.sin(_t)
    plt.plot(_x, _y, 'g-')
    plt.xlim(-radius-100,radius+100 )
    plt.ylim(-radius-100,radius+100)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Random Scatter')
    plt.grid(True)
    plt.savefig('imag.png')
    plt.show()