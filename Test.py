from MyClass import MyClass
import numpy as np

Alpha = 100000  # 计算噪声参数

myClass = MyClass(3)
myClass.print()
BW = 1e7

__N0_dbm = -174 + 10 * np.log10(BW)
__N0 = 10 ** ((__N0_dbm - 30) / 10)
Noise1 = 20 * (500 ** (-4)) / Alpha  # 计算噪声
Noise2 = 1 * (100** (-4)) / Alpha  # 计算噪声
'''
g = self.genep[n][s]/self.Qmax*self.BS[n].power*self.Bias*(Distence**(-4))   #计算当前信道功率（17.04.18修正为信号强度）
Noise = self.Qmax*self.BS[n].power*self.Bias*(self.BS[n].coverArea**(-4))/self.Alpha  #计算噪声'''
noise3=20* (500 **-4) /10
noise4=1* (100 **-4) /10
p=20*(300 **-4)
p2=1/30*(80**-4)
i = 0
