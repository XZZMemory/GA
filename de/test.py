# coding: utf8
import numpy as np

N=20  # 编码长度
MAX=10.0/(2**(N))  # [0,10), 区间内有两个最大值（17）的点
NUM=500  # 种群数量

def f(x):  # 函数
    return 10*np.sin(5*x) + 7*np.cos(4*x)

def new(num=NUM,len=N):  # 随机生成(low,high,size)
    return np.random.randint(1,2**len,num)

def n2b(nums):  # 数字编码
    return [bin(i)[2:].zfill(N) for i in nums]

def b2n(bits):  # 解码
    return [int(i,base=2) for i in bits]

def fit(nums,s_rate=0.15,r_rate=0.05):  # 适应度和选择
    n=len(nums)
    sn=int(n*s_rate)
    on=int(n*r_rate)
    np.random.shuffle(nums)
    outs=nums[:on]
    res=[f(i*MAX) for i in nums]   # 适应度选择和随机选择，可能有重复
    temp=np.argsort(res)
    others=[nums[i] for i in temp[-sn:]]
    outs=np.concatenate((outs, others))
    return outs,nums[temp[-1]]*MAX,res[temp[-1]]

def repo(fits,mode='DE'):  # 扩增，此处5倍；增加了进化算法
    n=len(fits)
    pt=np.random.randint(0,n,4*n)
    pt=np.reshape(pt,(2*n,2))
    bits=n2b(fits)
    new_bits=bits
    for i in pt:
        b1,b2=exchange([bits[j] for j in i])
        new_bits.append(b1)
        new_bits.append(b2)
    if mode=='DE':
        return dmut(new_bits)
    return mut(new_bits)

def exchange(bits,change_rate=0.4,mode='cross'):  #交换，提供了随机交换和节点互换
    n=int(change_rate*N)
    if mode=='rand':
        rn=range(N)
        new_bits=[list(i) for i in bits]
        for i in rn[:n]:
            new_bits[0][i] = bits[1][i]
            new_bits[1][i] = bits[0][i]
        new_bits=[''.join(i) for i in new_bits]
    else:
        n = int(change_rate * N)
        new_bits = [list(i) for i in bits]
        new_bits[0][:n] = bits[1][:n]
        new_bits[1][:n] = bits[0][:n]
        new_bits = [''.join(i) for i in new_bits]
    return new_bits

def mut(bits,mut_rate=0.03):  # 变异
    length=len(bits)*N
    n = int(mut_rate * length)
    if n<1: n=1
    rn = range(length)
    np.random.shuffle(rn)
    for i in rn[:n]:
        j=int(bits[i/N][i%N])
        bits[i/N]=swap(bits[i/N],i%N,str(1-j))
    return bits

def swap(str,i,char):  # 字符串交换
    str2=list(str)
    str2[i]=char
    return ''.join(str2)

def dmut(bits,mut_rate=1.0,F=0.5):   #  差分变异
    length = len(bits)
    n = int(mut_rate * length)
    if n < 1: n = 1
    rn = np.random.randint(0,length,3*n)
    rn = np.reshape(rn,(n,3))
    nums=b2n(bits)
    for i in rn:
        nums[i[0]]+=int(F*(nums[i[1]]-nums[i[2]]))
        if nums[i[0]]<0:
            nums[i[0]]*=-1
    return n2b(nums)

def train(iter=50):  # 训练入口
    nums=new()
    outs,x,fx=fit(nums)
    for i in range(iter):
        new_bits = repo(outs)
        nums=b2n(new_bits)
        outs,x,fx=fit(nums)
        print (str(i)+" 11 "+str(x)+" 22 "+str(fx))


if '__main__==main()':
    train()