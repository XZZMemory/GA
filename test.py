import numpy as np
import numpy

VQS = []
for i in range(4):
    VQS.append([])
    for j in range(2):
        VQS[i].append([])
        # 是不是一个三维数组
for i in range(len(VQS)):
    for j in range(len(VQS[i])):
        for k in range(2):
            VQS[i][j].append(k)
i = 2
x = numpy.array(
    [[0, 0], [-1, 0.1], [0.3, -0.05], [0.7, 0.3], [-0.2, -0.6], [-0.15, -0.63], [-0.25, 0.55], [-0.28, 0.67]])
y = [0, 0, 0, 0, 1, 1, 2, 2]
print(list(set(y)))
print(y)
if ((1 == 1) & (2 == 2)):
    print("a")
print(str(2 in y))
print(max(y))
locationOfBase = [[50, 50], [0, 0], [0, 100], [100, 0], [100, 100]]  # 基站位置初始化
te = []
for i in range(len(locationOfBase)):
    te.append(list(set(locationOfBase[i])))
locationOfUser = [[25, 0], [50, 0], [75, 0], [0, 25], [0, 50], [0, 75], [25, 25], [25, 50], [75, 50]]  # 用户位置初始化
test = [[[1, 2, 3, 4, 5], 50], [0, 0], [0, 100], [100, 0], [100, 100]]
print(str(test[0][0][0]))
BW = 1e7
__N0_dbm = -174 + 10 * np.log10(BW)
__N0 = 10 ** ((__N0_dbm - 30) / 10)
print("BW:" + str(BW) + " __N0_dbm：" + str(__N0_dbm) + " __N0:" + str(__N0))
c = -121  # dBm
p=10**(c/10)
pp=10**((c-30)/10)*1000
print("p: "+str(p)+" pp: "+str(pp))
macrop=20000#mw
noise=macrop*(500**(-4))/10
print("noise: "+str(noise))
picrop=1000#mw
noise2=picrop*(100**(-4))/10
print("noise2: "+str(noise2))
str1="987654321"
#print(str[len(str1)-4:len(str1)])
'''
BW: 10000000.0 __N0_dbm： -104.0 __N0: 3.9810717055349693e-14
'''
str2="/data/maxFitness/"
print("length: "+str(len(str2)))