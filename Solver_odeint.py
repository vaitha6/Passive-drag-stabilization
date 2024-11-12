import numpy as np
from math import *
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def Rx(theta):
  return np.matrix([[ 1, 0           , 0           ],
                   [ 0, cos(theta),-sin(theta)],
                   [ 0, sin(theta), cos(theta)]])
  
def Ry(theta):
  return np.matrix([[ cos(theta), 0, sin(theta)],
                   [ 0           , 1, 0           ],
                   [-sin(theta), 0, cos(theta)]])
  
def Rz(theta):
  return np.matrix([[ cos(theta), -sin(theta), 0 ],
                   [ sin(theta), cos(theta) , 0 ],
                   [ 0           , 0            , 1 ]])

I = [[10000, 13000, 11000], [14000, 8500, 16000], [3000, 8000, 15000]]
inv_I=np.linalg.inv(I)

C_d=0.2
rho=1
v=5
F_d = np.transpose([0.5*C_d*rho*(v**2), 0, 0])
l_mag = np.transpose([0, 0, 5])

def func(ic, t):
    
    dwdt=np.empty(6)
    dwdt[0:2] = ic[3:5]
    rot_mat=np.empty([3,3])
    rot_mat = np.dot(np.dot(Rz(ic[2]), Ry(ic[1])), Rx(ic[0])) #Rotation matrix
    #print(rot_mat) #Unit testing
    l_vect=np.empty(3)
    l_vect = np.dot(rot_mat, l_mag)
    #print(l_temp) #Unit testing
    #print(l_vect) #Unit testing
    #*np.transpose([cos(ic[0]*pi/180)*sin(ic[2]*pi/180), sin(ic[0]*pi/180)*sin(ic[2]*pi/180), cos(ic[0]*pi/180)])
    #print(np.cross(l_vect, F_d)) #Unit testing
    dwdt[3:] = np.dot(np.cross(l_vect, F_d), inv_I)
    #print(dwdt)
    
    #print(dwdt)

    return dwdt

theta_0 = [0, 0, 0]
w_0 = [0.01, -0.005, 0.02]

ic = np.concatenate([theta_0, w_0])

t=np.linspace(0, 1000, 1001)
sol = odeint(func, ic, t)

l_vect_plot=np.zeros([len(t),3])
for i in range(len(t)): 
    rot_mat = np.dot(np.dot(Rz(sol[i,2]), Ry(sol[i,1])), Rx(sol[i,0])) #Rotation matrix
    l_vect_plot[i,:] = np.dot(rot_mat, l_mag)
    
#plt.plot(t, sol[:,2])
#plt.show()

fig, ax = plt.subplots(3)
ax[0].plot(t,l_vect_plot[:,0])
ax[1].plot(t,l_vect_plot[:,1])
ax[2].plot(t,l_vect_plot[:,2])


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.plot(l_vect_plot[:,0], l_vect_plot[:,1], l_vect_plot[:,2])
