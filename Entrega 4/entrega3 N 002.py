# -*- coding: utf-8 -*-

from timeit import timeit
from matplotlib.pylab import *
from scipy.integrate import odeint
import random 


# unidades base SI(m,kg,s)

_m=1
_kg=1
_s=1
_mm=1e-3*_m
_cm=1e-2*_m
_gr=1e-3*_kg
_in=2.54*_cm

g=9.81*_m/_s**2 	#Aceleracion de gravedad
dm=1.*_mm 		#Diametro medio de particulas

rho_agua=1000.*_kg/(_m**3) 	#Densidad del agua
rho_particula=2700*_kg/(_m**3) 	#Densidad particula

dt= 0.001*_s     #Paso de tiempo 
tmax=0.5*_s        #Tiempo maximo de simulacion
ti= 0.*_s        #Tiempo actual

### Definicion variables particula
Nparticulas = 20

d = rand(Nparticulas)*dm + dm/2	#Array de diametros de cada particula

x0 = rand(Nparticulas)*100*dm		#Posiciones iniciales de cada particula
y0 = rand(Nparticulas)*30*dm + max(d)/2


vx0 = rand(Nparticulas)/2 			#Velocidades iniciales de cada particula
vy0 = rand(Nparticulas)/2 

A=pi*(d/2)**2 			#Area de cada particula
V=(4./3.)*pi*(d/2)**3 	#Volumen de cada particula
m=rho_particula*V  		#Masa de cada particula
W = zeros([Nparticulas,2])
for i in range(Nparticulas):
	W[i][1] = -m[i]*g	#Fuerza de peso aplicada a cada particula

t = arange(0, tmax, dt)
Nt = len(t)

norm = lambda v: sqrt(dot(v,v)) #Funcion que calcula la norma de un vector

Cd = 0.47 
Cm = 0.5
Cl = 0.2
Rp = 73.
R = (rho_particula/rho_agua - 1)
alpha = 1/(1 + R + Cm)

ihat = array([1,0])
jhat = array([0,1])

ustar = 0.14
factor = 1e2


def velocidades(x,d):	#Define perfil logaritmico de aceleraciones en el eje y
	z = x[1]/d 	#La variable z es la altura a la que se encuentra la particula
	if z > 1./30:
		uf = ustar*log(30.*z)/0.41
	else:
		uf = 0
	return array([uf,0]) 	#Devuelve un vector con la acceleracion en eje x
print "dm: {}".format(4*dm)
print "1/30 {}".format(1/30.)
vfx = velocidades([0, 4*dm],dm)[0]
print ("Vfx {}".format(vfx))

k_penal = factor*0.5*Cd*rho_agua*A*norm(vfx)*2/(1*_mm) 

def particula(z,t):
	zp = zeros(4*Nparticulas)
	for i in range(Nparticulas):
		di = d[i]
		mi = m[i]
		Ai = A[i]
		Wi = W[i]
		xi = z[4*i:(4*i+2)]
		vi = z[4*i+2:(4*i+4)] 	
		vf = velocidades(xi,di) #Velocidad del flujo 
		vf_top = norm (velocidades(xi + (di/2) *jhat,di)) #Velocidad en parte superior de particula
		vf_bot = norm (velocidades(xi - (di/2) *jhat,di)) #Velocidad en parte inferior de particula
		vrel = vf - vi #Diferencia de velocidades en parte superior e inferior
		fD = (0.5*Cd*alpha*rho_agua*norm(vrel)*Ai)*vrel #Fuerza de arrastre (drag)
		fL = (0.5*Cl*alpha*rho_agua*(vf_top*2 - vf_bot*2)*Ai)*jhat #Fuerza de levante

		Fi = Wi + fD +fL #Fuerzas aplicadas a la particula
		### Verifica de que la particula no pase a negativo ###
		if xi[1] < di/2: 
			Fi[1]+= -k_penal[i]*(xi[1]-di/2)

		zp[4*i:(4*i+2)] = vi
		zp[4*i+2:(4*i+4)] = Fi / mi

	### Loop para casos de choque ###
	
	for i in range(Nparticulas):
		xi = z[(4*i):(4*i+2)]
		for j in range(Nparticulas):
			if i > j:
				xj = z[(4*j):(4*j+2)]
				rij = xi - xj 			#Distancia entre los centros de las particulas
				dist = d[i]/2 + d[j]/2 	#Suma de los radios de las particulas i y j
				if norm(rij) < dist:	#Verificación de que las distancias sean mayores a la suma de sus radios
					delta = dist - norm(rij) #Distancia de traslape
					nij = rij/norm(rij) 	#Vector normalizado de centros
					Fj = k_penal[j]*delta*nij 	#Fuerza con que se repele la particula j
					Fi = -k_penal[i]*delta*nij 	#Fuerza con que se repele la particula i
					zp[(4*i+2):(4*i+4)] += Fi/m[i] #calculo de posicion
					zp[(4*j+2):(4*j+4)] += Fj/m[j]
	
	return zp	


z0 = zeros(4*Nparticulas)
z0[0::4] = x0
z0[1::4] = y0
z0[2::4] = vx0
z0[3::4] = vy0

print 'Integrando'
z = odeint(particula, z0, t)

print 'Fin'

fig = figure()

ax = gca()
for i in range(Nparticulas):
	di = d[i]
	xi = z[:,4*i]/di
	yi = z[:,4*i+1]/di
	col = rand(3)
	plot(xi[0],yi[0],"o", color="r")
	plot(xi,yi,"--.", color=col)
	for x,y in zip(xi,yi): #Marca inicio de particula
		ax.add_artist(Circle(xy=(x,y),radius=d[i]/2,color=col,alpha=0.7))
	for j in range(int(tmax/dt)): #Marca esferas
		if j%8 == 0: 
			circle = plt.Circle((xi[j], yi[j]), d[i]/2, color ='r', clip_on=True)
		ax.add_artist(circle)	
		
	#plot (xi[0], yi[0], "o", color ="r")
	plot (xi,yi,"--.", color=col)

"""

figure()

for i in range(Nparticulas):
	xi = z[:,4*i]
	yi = z[:,4*i+1]
	print xi
	plot(xi,yi,"o", color="r")
	ylim([0,10*_mm])
	plt.title("Rebote de N particulas")
	plt.xlabel("Posicion en x")
	plt.ylabel("Posicion en Y")
"""

#show()
