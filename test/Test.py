import matplotlib.pyplot as plt
import numpy as np
mat = "{:^3}\t{:^3}\t{:^3}"
print(mat.format("占1个长度", "占1个长度", "占1长度"))
mat = "{:^5}\t{:^5}\t{:^5}"
print(mat.format("占1个长度", "占1个长度", "占1长度"))
# 如果需要居中输出在宽度前面加一个^
mat = "{:^20}\t{:^28}\t{:^32}"
print(mat.format("占4个长度", "占8个长度", "占12长度"))
VN = [[1, -1, 1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, 1, -1, 1],
      [1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1, -1, -1, 1],
      [-1, -1, 1, 1, -1, -1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1, -1, 1, -1, 1],
      [-1, 1, 1, 1, 1, 1, 1, 1, -1, 1, -1, -1, 1, 1, 1, -1, 1, -1, -1, -1]]
times = 0
for video in range(len(VN)):
    for desc in VN[video]:
        if desc == 1:
            times=times+1
print("VN-Times: " + str(times))
data1=[[0, 36.999436017087476], [1, 36.999436017087476], [2, 38.99941385085644], [3, 38.99941385085644], [4, 38.999740028512505], [5, 38.999740028512505], [6, 40.99971949007229], [7, 40.99973830359974], [8, 40.99973830359974], [9, 40.99973830359974], [10, 40.99973830359974], [11, 40.99973830359974], [12, 40.99973830359974], [13, 40.99973830359974], [14, 40.99973830359974], [15, 40.99977478579174], [16, 41.99916213527321], [17, 41.99916213527321], [18, 41.99916213527321], [19, 41.99919861746521], [20, 41.99919861746521], [21, 41.99919861746521], [22, 41.99926730101864], [23, 41.99926730101864], [24, 41.99926730101864], [25, 41.99926730101864], [26, 41.99926730101864], [27, 41.999278074882156], [28, 41.999278074882156], [29, 41.999278074882156], [30, 41.999278074882156], [31, 41.999278074882156], [32, 41.999278074882156], [33, 41.999278074882156], [34, 41.999278074882156], [35, 41.999278074882156], [36, 41.99974917941346], [37, 41.99974917941346], [38, 41.99974917941346], [39, 41.99974917941346], [40, 41.99974917941346], [41, 41.99977820922431], [42, 41.99977820922431], [43, 41.99977820922431], [44, 41.99977820922431], [45, 41.99977820922431], [46, 42.99970127531505], [47, 42.99970127531505], [48, 42.99970127531505], [49, 42.99970127531505]]
data2=[[0, 1.786841340271013e-20], [1, 5.917787737162363e-20], [2, 3.0898372795410637e-14], [3, 2.1684200069516082e-13], [4, 2.1684200069516082e-13], [5, 4.32308221902606e-12], [6, 4.32308221902606e-12], [7, 5.076499878331417e-12], [8, 1.3169554489803586e-11], [9, 1.3948868136167155e-10], [10, 1.3948868136167155e-10], [11, 1.3948868136167155e-10], [12, 3.2624431464080674e-10], [13, 3.266587005463873e-10], [14, 3.266587005463873e-10], [15, 3.266587005463873e-10], [16, 9.225435063806581e-10], [17, 9.225435063806581e-10], [18, 9.225435063806581e-10], [19, 1.0614345133026858e-09], [20, 1.0722371335988027e-09], [21, 1.0722371335988027e-09], [22, 1.0722371335988027e-09], [23, 1.1780684041633218e-09], [24, 1.2839422736599795e-09], [25, 1.2839422736599795e-09], [26, 6.384265928451146e-09], [27, 6.384265928451146e-09], [28, 6.384265928451146e-09], [29, 6.384265928451146e-09], [30, 6.38426592845115e-09], [31, 6.38426592845115e-09], [32, 6.38426592845115e-09], [33, 6.38426592845115e-09], [34, 6.453810685909459e-09], [35, 6.453810685909459e-09], [36, 6.4552725167177716e-09], [37, 6.4552725167177716e-09], [38, 4.4786281328961645e-08], [39, 4.4786281328961645e-08], [40, 4.652613282943067e-08], [41, 0.0010607190053672688], [42, 0.0010607190053672688], [43, 0.0010607190053672688], [44, 0.0011000544550008706], [45, 0.0011000544550008706], [46, 0.0011000719756478618], [47, 0.0011000719756478618], [48, 0.0011000719756478618], [49, 0.001101685828831591]]
data3=[[0, 39.99946821184961], [1, 39.99956415109956], [2, 41.99938528504449], [3, 41.99938528504449], [4, 41.99938643495827], [5, 42.9993846729368], [6, 42.9993846729368], [7, 42.99938468217765], [8, 42.99938469142501], [9, 42.999424848342514], [10, 42.999424848342514], [11, 42.999424848342514], [12, 42.99942487506881], [13, 42.999424899080815], [14, 42.99948246298877], [15, 42.99948246298877], [16, 42.99948246298877], [17, 42.99962463251075], [18, 42.99962463251075], [19, 42.99962463251075], [20, 42.99962463251075], [21, 42.99962463251075], [22, 42.99962463251075], [23, 42.99962463251075], [24, 42.99962463251075], [25, 42.99962463251075], [26, 42.99962463251075], [27, 42.99962463251075], [28, 42.99962463251075], [29, 42.999644771100584], [30, 42.999644771100584], [31, 42.999644771100584], [32, 42.999644771100584], [33, 42.999644771100584], [34, 42.999644771100584], [35, 42.999644771100584], [36, 42.999644771100584], [37, 42.999644771100584], [38, 42.999644771100584], [39, 42.999644771100584], [40, 42.999644771100584], [41, 42.999644771100584], [42, 42.999644771100584], [43, 42.999644771100584], [44, 42.999644771100584], [45, 42.999644771100584], [46, 42.999644771100584], [47, 42.999644771100584], [48, 42.999644771100584], [49, 42.99964502186745]]
data5=[[0, 21.918108829930357], [1, 21.918108829930357], [2, 23.14120098510078], [3, 23.773297893240223], [4, 23.778082406123673], [5, 24.45194575856959], [6, 24.597817695928487], [7, 24.707007115457095], [8, 24.945082869210918], [9, 25.123255867917948], [10, 25.37977947627966], [11, 25.677585443925047], [12, 26.117507939190514], [13, 26.204211043684694], [14, 26.204211043684694], [15, 26.330657732736356], [16, 26.685477484875612], [17, 26.75808933591978], [18, 26.762348211034904], [19, 26.901542444635293], [20, 27.367598670969677], [21, 27.554212717239135], [22, 27.69445326405877], [23, 28.016217308665148], [24, 28.017646131106897], [25, 28.02404516519116], [26, 28.027829672200273], [27, 28.02784115490587], [28, 28.23208681162347], [29, 28.71308288683769], [30, 28.713083021549508], [31, 28.713083043673333], [32, 28.71308304674662], [33, 28.71308304674662], [34, 28.71308304674662], [35, 28.7130830504405], [36, 28.713083068870443], [37, 28.713083068870443], [38, 28.713083068870443], [39, 28.713083068870443], [40, 28.713083068870443], [41, 28.713083068870443], [42, 28.713083068870443], [43, 28.762602881919246], [44, 28.762602881919246], [45, 29.06469153825312], [46, 29.844108271488384], [47, 29.844108271488384], [48, 29.85174731464552], [49, 29.85174731464552]]
data4=[[0, 23.389563250940444], [1, 25.21711412948466], [2, 25.21711412948466], [3, 25.21711412948466], [4, 26.134353699062697], [5, 26.134353699062697], [6, 27.504368909967788], [7, 27.504368909967788], [8, 27.504369045093934], [9, 27.693899037983595], [10, 27.693899037983595], [11, 27.693899037983595], [12, 27.752382224834847], [13, 27.752382224834847], [14, 27.873078560321673], [15, 28.046086049205588], [16, 28.046086049205588], [17, 28.338294620967375], [18, 29.1672816643207], [19, 29.1672816643207], [20, 29.20980675568858], [21, 29.20980675568858], [22, 29.20980675568858], [23, 29.455645676274436], [24, 31.050911607225256], [25, 31.050911607225256], [26, 31.433496505418038], [27, 31.433496505418038], [28, 31.433496505418038], [29, 31.43365837190015], [30, 31.43365837190015], [31, 31.45289278541726], [32, 31.45289278541726], [33, 31.453004328198073], [34, 31.45306816384222], [35, 31.45319567168948], [36, 31.857935971698193], [37, 31.93361178354661], [38, 31.933665097566685], [39, 31.936652220829927], [40, 31.936652272203805], [41, 31.936652272203805], [42, 31.936707646340512], [43, 31.93670946497244], [44, 32.009076700126876], [45, 32.009076700126876], [46, 32.04786053388493], [47, 32.04786053388493], [48, 32.055816996253434], [49, 32.055816996253434]]
x1=[]
y1=[]
for i in range (len(data1)):
    x1.append(data1[i][0])
    y1.append(data1[i][1])
x5=[]
y5=[]
for i in range (len(data5)):
    x5.append(data5[i][0])
    y5.append(data5[i][1])
x4=[]
y4=[]
for i in range (len(data2)):
    x4.append(data4[i][0])
    y4.append(data4[i][1])
x3=[]
y3=[]
for i in range (len(data3)):
    x3.append(data3[i][0])
    y3.append(data3[i][1])
x2 = []
y2 = []
for i in range(len(data2)):
    x2.append(data2[i][0])
    y2.append(data2[i][1])
plt.plot(x1, y1,color="gray")
plt.plot(x4, y4,color="black")
plt.plot(x2, y2, color="green",label="VQD4")
plt.plot(x3, y3,color="blue")
plt.plot(x5, y5,color="red")

plt.xlabel("iterations", fontsize=14)
plt.ylabel("fitness", fontsize=14)
plt.show()
