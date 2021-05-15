import pandas as pd
import numpy as np
import math
from pyquaternion import Quaternion
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data=pd.read_excel('HW5-2.xls')
given=data.to_numpy()
Data=np.zeros([100,4])
%matplotlib tk

iter=1000
lr=0.001
q=np.array([1,0,0,0])
q_predict=np.zeros([100,4])

ax=data.loc[:,['ax']]
ay=data.loc[:,['ay']]
az=data.loc[:,['az']]
ax1=np.array(ax)
ay1=np.array(ay)
az1=np.array(az)

for i in range(100):
    for j in range(iter):
        #normalize後的acc只有方向沒有大小
        norm=math.sqrt(ax1[i,0]*ax1[i,0]+ay1[i,0]*ay1[i,0]+az1[i,0]*az1[i,0])
        a_x=ax1[i,0]/norm
        a_y=ay1[i,0]/norm
        a_z=az1[i,0]/norm
        #cost function=e
        f1=-2*(q[1]*q[3]-q[2]*q[0])-a_x
        f2=-2*(q[2]*q[3]+q[1]*q[0])-a_y
        f3=-1+2*(q[1]*q[1]+q[2]*q[2])-a_z
        f=np.array([f1,f2,f3])
        #Jacobian
        J=np.array([[2*q[2],-2*q[3],2*q[0],-2*q[1]],[-2*q[1],-2*q[0],-2*q[3],-2*q[2]],[0,4*q[1],4*q[2],0]])
        #Gradient
        G=(J.T).dot(f)
        #normalize Gradient
        norm_G=math.sqrt(G[0]*G[0]+G[1]*G[1]+G[2]*G[2]+G[3]*G[3])
        G=G/norm_G
        #Quaternion
        q=q-lr*G
        # normalize quaternion
        norm_q=math.sqrt(q[0]*q[0]+q[1]*q[1]+q[2]*q[2]+q[3]*q[3])
        q=q/norm_q
        
    q_predict[i,0]=q[0]
    q_predict[i,1]=q[1]
    q_predict[i,2]=q[2]
    q_predict[i,3]=q[3]
    
    
    
    q_1=Quaternion(q[0],q[1],q[2],q[3])
    q_1_inverse=q_1.inverse
    E=Quaternion(0,0,0,-9.8)
    #gravity to sensor frame
    q_2=q_1_inverse*E*q_1
    
    for s in range(4):
        Data[i,s]=q_2[s]
