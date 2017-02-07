### Portfolio Note
# This is a tool used to numerically solve the schroedinger equation for
# any given potential and produces plots of various quantities of interest.
# Various options can be modified, the "sampling rate", inclusion of random noise,
# etc...


# -*- coding: utf-8 -*-
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import random


Dx = .01
x = np.arange(0,100,Dx)


Dt = .01
t = np.arange(0,2,Dt)

#y0 = np.complex(.8*np.random.normal(),.8*np.random.normal())
#
#yp0 = np.complex(.8*np.random.normal(),.8*np.random.normal())

y0 = np.complex(0,0)

yp0 = np.complex(0,0)

E = abs(np.random.normal())

RandDamp = 0.01

#h_bar = 10**(-4)
#m = 10^-2
#mu = ((2*m)/(h_bar**2))

mu = 10


#m_electron = 9.10938291(40)×10−31 kg
#planck_const = 1.054571800(13)×10−34
# i h_bar psi= (-(h_bar)^2/2m *D^2/dx^ + V(x))psi



def V(q):    
    return -100./(1+1000*(q-10)**2)-100/(1+1000*(q-30)**2)-100/(1+1000*(q-70)**2)- 100/(1+1000*(q-50)**2)-100/(1+1000*(q-90)**2)
        
        
    
    #if (2 < q) and (q < 7):
    #    return  (q-2)*(q-7)
    #else:
    #    return 0
    #
    #if (2 > q) or (q > 8):
    #    return  -1
    #else:
    #    return 0
    
    #return 1 + q*np.sin(q)/3 + np.log(1/(q**.5+1))
    #
    #if q < 10:
    #    return np.cos(3*q)
    #return .1*(q-10)*(q-20)
    #
    #return 0
    
    #return -np.sin(2*q)
    
Vs = []
for k in x:
    Vs = Vs + [V(k)]
      

yprime = [yp0]
y = [y0]






for k in range(len(x)-1):
    ypnorm = yprime[-1]*(1 + (RandDamp**1.5)*np.random.normal())+(RandDamp**1.5)*np.random.normal()
    ynorm = y[-1]*(1 + RandDamp*np.random.normal())+(RandDamp**1.5)*np.random.normal()

    yprime = yprime + [ypnorm + mu*(V(x[k])-E)*ynorm*Dx]
    y = y + [ynorm + ypnorm*Dx]

TimeEvo = []

for k in range(len(x)-1):
    xevo = [y[k]]
    for j in range(len(t)-1):
        xnorm = -np.complex(0,1)*xevo[-1]*(1 + RandDamp*np.random.normal())
        xevo = xevo + [xnorm*(1+Dt)]
    TimeEvo = TimeEvo + [xevo]

psiFinal = [TimeEvo[0][-1]]
for k in range(len(TimeEvo)):
    psiFinal = psiFinal + [TimeEvo[k][-1]]
    
rey0 = round(np.real(y0),3)
imy0 = round(np.imag(y0),3)
reyp0 = round(np.real(yp0),3)
imyp0 = round(np.imag(yp0),3)

fig = plt.figure(figsize = (20,10))
fig.suptitle('RDamp = ' + str(.01*np.ceil(100*RandDamp)) + 
             ',     mu = ' + str(.01*np.ceil(100*mu)) + 
             ',   E = ' + str(.01*np.ceil(100*E)) +
             ',  Psi(0,t_0) = ' + str(rey0) + ' + ' + str(imy0) + 'j' + 
             ',   (d/dx) Psi(0, t_0) = ' + str(reyp0) + ' + ' + str(imyp0) + 'i', 
             fontsize=16, fontweight='bold')

ax1 = fig.add_subplot(321)   
ax1.set_title('Potential, V(x)')
plt.plot(x,Vs)

ax2 = fig.add_subplot(322)   
ax2.set_title('Wave Function, Psi(x,t_0)')
plt.plot(x,y)


ax4 = fig.add_subplot(323)   
for k in range(0,len(TimeEvo)-1,int(len(TimeEvo)/1 -1)):
    plt.plot(t,np.angle(TimeEvo[356]))
ax4.set_title('Time Evolution Samples, Psi(x_k,t)')

ax5 = fig.add_subplot(324)   
plt.plot(x,psiFinal)
ax5.set_title('Re(Psi(x,t_f))')

PsiMag = []
PsiPhase = []
for k in y:
    PsiMag = PsiMag + [np.abs(k)]
    PsiPhase = PsiPhase + [np.angle(k)]
    
ax3 = fig.add_subplot(325)   
ax3.set_title('|Psi(x,t_0)|')
plt.plot(x,PsiMag)

ax6 = fig.add_subplot(326)   
ax6.set_title('Phase(Psi(x,t_0))')
plt.plot(x,PsiPhase)






#xs = []
#ys = []
#zs = []
#SampleSize = 30
#for i in range(0,len(t)-1,int(len(t)/SampleSize)):
#    for k in range(0, len(TimeEvo)-1,int(len(TimeEvo)/SampleSize)):
#        for j in range(0, len(TimeEvo[k])-1,int(len(TimeEvo[k])/SampleSize)):
#            xs = xs + [x[k]]
#            ys = ys + [TimeEvo[k][j]]
#            zs = zs + [t[i]]
            
#fig100 = plt.figure()
#ax = fig100.gca(projection='3d')
#ax.plot_trisurf(xs,ys,zs)


plt.show()
