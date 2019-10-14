import numpy


class MyClass:
    k = 0

    def __init__(self, sumOfBase):
        i = 0  # init的局部变量，其他函数中无法访问
        self.se = 9
        # sumOfBase = sumOfBase 局部变量，无法访问

    def print(self):
        # print(str(self.i))
        print(str(self.se))
        # print(str(self.sumOfBase))
        print(str(self.k))
        print("pi: " + str(numpy.pi))
        r = numpy.random.random(10)
        print("t: " + str(r))

        t = r * 2 * numpy.pi - numpy.pi
        print("t: " + str(t))
        x = numpy.cos(t)
        y = numpy.sin(t)
        print("x: " + str(x))
        print("y: " + str(y))
        i_set = numpy.arange(0, 10, 1)
        print("set： " + str(i_set))
        list = [3, 7, 9]
        list2 = [1, 3]
        differVideoList1 = [item for item in list if item not in list2]
        print(differVideoList1)
