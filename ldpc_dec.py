#coding:utf-8
import numpy as np
import random
import math

def module(data):
    ans=[]
    for i in range(len(data)):
        if(data[i]==1):ans.append(-1)
        if(data[i]==0):ans.append(1)
    return ans

def demodule(data):
    ans=[]
    for i in range(len(data)):
        if(data[i]>0):ans.append(0)
        if(data[i]<=0):ans.append(1)
    return ans



def gen_noi():
    return random.normalvariate(0,1)

def channel(data,SNR):
    sigma=math.sqrt(10**(-SNR/10))
    for i in range(len(data)):
        data[i]+=sigma*gen_noi()
    return data

#H:二维list
def decode(H,data):
    for num in range(100):
        if(num%10==0):print(num)
        ans=np.zeros(512)
        for i in H:
            tmp=0
            for j in range(len(i)):
                tmp+=i[j]*data[j]
                tmp%=2
            if tmp==1:
                for j in range(len(i)):
                    if i[j]==1:
                        ans[j]+=1
        flag=True
        for i in ans:
            if i>1:
                data[int(i)]+=1
                data[int(i)]%=2
                flag=False
        if flag:break
    return data

def cal_rate(data):
    num=0.0
    for i in data:
        if i==1:
            num+=1
    rate=num/512
    return rate

def load_H():
    import scipy.io as sio
    load_fn = 'hh.mat'
    load_data = sio.loadmat(load_fn)
    ans = load_data['ans']
    return ans


if __name__ == '__main__':
    data=np.zeros(512).tolist()
    data=module(data)
    data=channel(data,3)
    data=demodule(data)
    H=load_H()
    #print(H.shape)
    data=decode(H,data)
    rate=cal_rate(data)
    print(rate)

''' 
最大迭代次数100次  
rate:
SNR,rate
1     0.115234375
1.5   0.11328125
2     0.099609375
2.5   0.103515625
3     0.05859375
'''

