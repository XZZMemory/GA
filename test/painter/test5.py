import matplotlib.pyplot as plt

plt.figure(1, figsize=(3, 3))
ax = plt.subplot(111)
'''

arrowprops = {
    arrowstyle 箭头类型
    connectionstyle：xy与xytext连接之间类型
}
'''
ax.annotate("s",
            xy=(0.2, 0.2), xycoords='data',
            xytext=(0.8, 0.8), textcoords='data',
            arrowprops=dict(arrowstyle="-",
                            connectionstyle="arc3"),
            )

plt.show()