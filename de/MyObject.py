import math

class Base:
    def __init__(self, sumOfChannels, power, location, capacity, radius):
        self.sumOfChannels = sumOfChannels
        self.power = power
        self.location = location
        self.capacity = capacity
        self.radius = radius
        self.video=[]
    def addVideo(self,video):
        self.video.append(video)

    #user是否在base覆盖范围内
    def isCovered(self,user):
        distance=self.distanceToUser(user)
        if(distance<=self.radius):
            return True
        return False
    def distanceToUser(self, user):
        distance = math.sqrt(self.location[0] - user.location[0]) ** 2 + (self.location[1] - user.location[1])
        return distance

    #只存储用户标识
    def setCoveredUsers(self,users):
        self.coveredUsers=users


class User:
    def __init__(self, location):
        self.location = location


class Video:
    def __init__(self, sumOfDesc,size):
        self.sumOfDesc = sumOfDesc
        self.size=size
        self.decs = []
        self.storedBase = []

    def appendDesc(self, size):
        self.decs.append(size)
    #只存储基站标识 0/1/2/3/4
    def setStoredBase(self,storedBaseOfDesc):
        self.storedBaseOfDesc=storedBaseOfDesc
