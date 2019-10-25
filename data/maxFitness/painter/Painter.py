import matplotlib.pyplot as plt


def painter():
    result = process()
    data1 = []
    data2 = result[1]
    data3 = result[2]
    data4 = result[3]
    data5 = result[4]
    x1 = []
    y1 = []
    for i in range(len(data1)):
        x1.append(data1[i][0])
        y1.append(data1[i][1])
    x5 = []
    y5 = []
    for i in range(len(data5)):
        x5.append(data5[i][0])
        y5.append(data5[i][1])
    x4 = []
    y4 = []
    for i in range(len(data4)):
        x4.append(data4[i][0])
        y4.append(data4[i][1])
    x3 = []
    y3 = []
    for i in range(len(data3)):
        x3.append(data3[i][0])
        y3.append(data3[i][1])
    x2 = []
    y2 = []
    for i in range(len(data2)):
        x2.append(data2[i][0])
        y2.append(data2[i][1])
    plt.plot(x1, y1, color="gray")
    plt.plot(x4, y4, color="black")
    plt.plot(x2, y2, color="green", label="VQD4")
    plt.plot(x3, y3, color="blue")
    plt.plot(x5, y5, color="red")

    plt.xlabel("iterations", fontsize=14)
    plt.ylabel("average reliability", fontsize=14)
    plt.show()


def process():
    data1FilePath = './data1.txt'
    data2FilePath = './data2.txt'
    data3FilePath = './data3.txt'
    data4FilePath = './data4.txt'
    data5FilePath = './data5.txt'
    iterations = 6000
    maxSum = 78
    data1 = []  # []processing(data1FilePath, iterations, maxSum)
    data2 = []  # processing(data2FilePath, iterations, maxSum)
    data3 = processing(data3FilePath, iterations, maxSum)
    data4 = []  # processing(data4FilePath, iterations, maxSum)
    data5 = processing(data5FilePath, iterations, maxSum)
    print("data1用户先分布在微基站再分布在宏基站中:" + str(data1))
    print("data2:" + str(data2))
    print("data3:" + str(data3))
    print("data4:" + str(data4))
    print("data5:" + str(data5))
    return [data1, data2, data3, data4, data5]


def processing(dataFilePath, iterations, maxSum):
    data1Temp = []
    for i in range(iterations):
        data1Temp.append(0)
    times = 0
    with open(dataFilePath) as file_object:
        for line in file_object:
            times = times + 1
            lineArray = eval(line)
            for i in range(len(lineArray)):
                data1Temp[i] = data1Temp[i] + float(lineArray[i][1])
    data = []
    for i in range(len(data1Temp)):
        data.append([i + 1, data1Temp[i] / times / maxSum])

    print(dataFilePath + "  --  " + str(data[0][1]) + " --- " + str(data[iterations - 1][1]))
    singleldata = []
    for i in range(len(data)):
        singleldata.append(data[i][1])
    print(str(singleldata))
    # fiName = "./data+" + dataFilePath[6] + "-single.txt"
    # ff = open(fiName, 'w')
    '''    for i in range(len(data)):
        if i % 30 == 0:
            ff.write(str(int(i / 30)) + '\n')'''

    return data


# painter()


def painterOne():
    data1 = processing('./data1.txt', 6000, 78)

    x1 = []
    y1 = []
    for i in range(len(data1)):
        x1.append(data1[i][0])
        y1.append(data1[i][1])

    plt.plot(x1, y1, color="gray")

    plt.xlabel("iterations", fontsize=14)
    plt.ylabel("average reliability", fontsize=14)
    plt.show()


#painter()


def processingTest():
    dataFilePath = './data3.txt'
    data1Temp = []
    times = 0
    with open(dataFilePath) as file_object:
        for line in file_object:
            times = times + 1
            lineArray = eval(line)
            for i in range(len(lineArray)):
                print(lineArray[i])
processingTest()