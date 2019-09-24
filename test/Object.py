import time

class MyObject:
    def __int__(self):
        self.type = 0

    def initPara(self):
        self.individualList = []
        for i in range(10):
            self.individualList.append(i)

    def changeType(self, type):
        self.type = type


list1 = [1, 2, 3, 3, 4, 4, 5, 6, 6, 6, 7, 8, 9]
list1 = list(set(list1))
print(list1)
print("list1: " + str(list1))
print("test: ")
for type in range(1, 6):
    print(type)
print("listTest")



# 格式化成2016-03-20 11:45:39形式
print (time.strftime("%Y%m%d", time.localtime()))
