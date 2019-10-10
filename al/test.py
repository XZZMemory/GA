from random import choice

user = 8
userList = []
for user in range(user):
    userList.append(user)
print(userList)
pop = choice(userList)
print("移除的元素是：" + str(pop))
userList.remove(pop)
print("移除元素后的list是：" + str(userList))

# print(userList.pop())

fruits = {"apple", "banana", "cherry"}

print(fruits.pop())

print(fruits)
configPath = './config.txt'
print("读取配置文件")


def processing(configPath):
    times = 1
    with open(configPath) as file_object:
        for line in file_object:
            if times == 1:
                locationOfBaseList = eval(line)
                print(str(locationOfBaseList))
            elif times == 2:
                locationOfUserList = eval(line)
                print(str(locationOfUserList))
            elif times == 3:
                VN = eval(line)
                print(str(VN))
            times = times + 1


processing(configPath)
print("求a的b次方")
print(4 ** 5)
data = [0]
print("求最大值1: " + str(max(data)))
data.append(9)
print("求最大值2: " + str(max(data)))
print(str(data))
result=0 in data
print("in test： " + str(0 in data))
print("not in test： " +str( 0 not in data))
