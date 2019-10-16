def printListWithTwoDi(name, list):
    times = 0
    for video in range(len(list)):
        for desc in list[video]:
            if desc == 1:
                times = times + 1
    print("VN-Times: " + str(times))
    mat = "{:^2}\t"
    print(str(name))
    for i in range(len(list)):
        if i == 0:
            print(mat.format(" "), end=' ')
            for k in range(len(list[i])):
                print(mat.format(str(k)), end=' ')
            print()
        for j in range(len(list[i])):
            if j == 0:
                print(mat.format(str(i)), end=' ')
            if list[i][j] == 1:
                print(mat.format(str(list[i][j])), end=' ')
            else:
                print(mat.format("  "), end=' ')
        print()
    return times


def getImportant(data):
    temp = []
    for i in range(len(data)):
        temp.append((data[i], i))
    result = sorted(temp, key=lambda temp: temp[0], reverse=True)
    return result[0][1]


VN = [[1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0],
      [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1],
      [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
      [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]]
