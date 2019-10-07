# -*- coding: utf-8 -*-
"""

"""

from matplotlib.pylab import *
from scipy.integrate import odeint
import random 



def particula(z,t):
            xi=z[:2]
            vi=z[2:]
            vf=array([vfx,vfy])
            vrel=vf-vi
            fD=(0.5*Cd*rho_agua*norm(vrel)*A)*vrel
            #fL=3.0/3.0*alpha*cD
            Fi=W+fD+fB
            if xi[1]<0:
                Fi[1]+=-k_penal*xi[1]
            zp=zeros(4)
            zp[:2]=vi
            zp[2:]=Fi/m
            return zp
    


# unidades base SI(m,kg,s)

_m=1
_kg=1
_s=1
_mm=1e-3*_m
_gr=1e-3*_kg

vfx= 5.0 *_m/_s     #m/s
vfy=0.0   *_m/_s    #m/s

# parametros 
g=9.81*_m/_s**2
d=[1.*_mm,2.*_mm,3.*_mm,4.*_mm,5.*_mm]
rho_agua=1000.*_kg/(_m**3)
rho_particula=2700*_kg/(_m**3)
Cd=0.47  # drag para una particula # coeficiente de drag

dt= 0.001*_s     #paso de tiempo 
tmax=2*_s        # tiempo maximo de simulacion
ti= 0.*_s          #tiempo actual

# prueba para n particulas 
N=len(d)
posicion=[]
velocidad=[]
for i in range (0,N):
        # parametros 
        A=pi*(d[i]/2)**2
        V=(4./3.)*pi*(d[i]/2)**3
        m=rho_particula*V              # masa de particula
        a=float(random.randint(0,25))
        b=float(random.randint(0,25))
        x0=array([b*_mm,a*_mm], dtype=double)  # particula en posicion cero 
        print "Particula N:", i+1
        print " Posicion inicial:",x0
        v_x=float(random.randint(1,5))
        v_y=float(random.randint(1,5))
        v0=array([v_x*_m/_s,v_y*_m/_s], dtype=double) # velocidad en 1 m/s para x y en y
        print " Velocidad inicial:",v0

        xi=x0#zeros(2, dtype=double)           # posicion actual
        vi=v0#zeros(2, dtype=double)           # velocidad actual
        xim1=zeros(2, dtype=double)         # posicion siguiente
        vim1=zeros(2, dtype=double)         # velocidad siguiente

        W=array([0,-m*g])   # vector que en x es 0 y en y es -mg
        fB=array([0,rho_agua*V*g])  
        t=arange(0,tmax,dt)
        Nt=len(t)

        norm=lambda  v: sqrt(dot(v,v))

        k_penal=1000*0.5*Cd*rho_agua*norm(v0)/(1*_mm)
        
        
        z0=zeros(4)
        z0[:2]=x0
        z0[2:]=v0
        z=odeint(particula,z0,t)
        x=z[:,:2]
        v=z[:,2:]

        # guardar informacion para particulas desde 1,...,N
        posicion.append(x)   # posicion de la particula
        velocidad.append(v)  # velocidad de la particula  



figure()
for i in range(len(posicion)):
    x_=posicion[i]
    plot(x_[:,0],x_[:,1])
    ylim([0,10*_mm])
    plt.title("Rebote de N particulas")
    plt.xlabel("Posicion en x")
    plt.ylabel("Posicion en Y")

figure()
for i in range(len(posicion)):
    x_=posicion[i]
    v_=velocidad[i]
    subplot(2,1,1)
    plot(t,x_[:,0], label="x")
    plot(t,x_[:,1], label="y")
    plt.title("Posicion de N particulas")
    plt.xlabel("Tiempo")
    plt.ylabel("Posicion")
    subplot(2,1,2)
    plot(t,v_[:,0], label="vx")
    plot(t,v_[:,1], label="vy")
    plt.title("Velocidad de N particulas")
    plt.xlabel("Tiempo")
    plt.ylabel("Velocidad")
show()
