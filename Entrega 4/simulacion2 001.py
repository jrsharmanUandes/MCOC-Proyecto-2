# -*- coding: utf-8 -*-

from timeit import timeit
from matplotlib.pylab import *
from scipy.integrate import odeint
import random 


#Unidades base son SI (m, kg, s)
_m = 1.
_kg = 1.
_s = 1.
_mm = 1e-3*_m
_cm = 1e-2*_m
_gr = 1e-3*_kg
_in = 2.54*_cm

g = 9.81*_m/_s**2
d = 0.15*_mm

rho_agua = 1000.*_kg/(_m**3)		# Densidad del agua
rho_particula = 2650.*_kg/(_m**3)	# Densidad de las particulillas

dt = 0.0001*_s    	# paso de tiempo 
tmax = 2*_s      # tiempo maximo de simulacion
t = arange(0, tmax, dt)
Cd = 0.47    #Coeficiente de arrastre
Cm = 0.5	#Masa adicional
CL = 0.2	#Coeficiente de lift
Rp = 73.  # Errepe

ustar = 0.14	#  (m/s)  0.14 - 0.23 usestrella

#Nparticulas = 2	#Numero de particulas


#x0 = rand(Nparticulas)*100*d      #Posiciones iniciales de cada particula
#y0 = rand(Nparticulas)*30*d + d/2


#vx0 = rand(Nparticulas)/2           #Velocidades iniciales de cada particula
#vy0 = rand(Nparticulas)/2 
#Nparticulas = data["Nparticulas"]
data = load("initial_condition.npz")
x0 = data["x0"]
y0 = data["y0"]
vx0 = data["vx0"]
vy0 = data["vy0"]
Nparticulas = data["Nparticulas"]



tau_star = 0.067   # Tau star (Shear stress)


R = (rho_particula/rho_agua - 1)   # Esta es la letra erre
alpha = 1/(1 + R + Cm)			# A en griego, de aqui viene la palabra "alfabeto"

ihat = array([1,0])			# itongo
jhat = array([0,1])			# jotatongo

tau_cr = 0.22*Rp**(-0.6)+0.06*10**(-7*Rp**(-0.6))   # tau critico
ustar = sqrt(tau_star * g * Rp * d)		# uestrella de verdad ahora si final final ok para siempre

print "tau_star = ", tau_star
print "tau_cr = ", tau_cr
print "tau_star/tau_cr = ", tau_star/tau_cr
print "ustar = ", ustar

# formulillas que no estoy usando
# tau_ratio = 2
# Rep = ws*d/nu
# Rp_computed = (R*g*d**3)/nu 
# tau = ustar**2 / (g * Rp * d)


# ley de la pared.... 
# wall law.... the wall.... the law of pink floyd
def velocidades(x):
	z = x[1] / d
	# z = x[1] 
	if z > 1/30.:
		uf = ustar*log(30.*z)/0.41
		uf = uf * (uf > 0)
	else:
		uf = 0

	return array([uf,0])

# estimar k_penal.... 
vfx = velocidades([0, 10*d])[0]
A=pi*(d/2)**2           #Area de cada particula
V=(4./3.)*pi*(d/2)**3   #Volumen de cada particula
m=rho_particula*V       #Masa de cada particula
W = -m*g
k_penal = 0.5*Cd*rho_agua*A*norm(vfx)**2/(d/20)

df = d

def vec_particula_fondo(x): 
	xi = x[0] #Distancia desde el origen a la que se encuentra la particula
	closest_s = round(xi/df)*df + df/2. #Encuentra el centro de la esfera de fondo mas cercano
	rij = x - array([closest_s,0]) 	#Vector entre el centro de particula y el centro de particula de fondo mas cercana
	dist = d/2. + df/2.  #Suma de radios de particula mas particula de fondo
	if norm(rij) < dist:
		delta = dist - norm(rij) 
		nij = rij/norm(rij)
		return nij*delta
	else:
		return array([0.,0.])

def perfil_fondo(x,di):	#Define el perfil de fondo
	x_mod_d = (x % di) - di/2
	y = sqrt((di/2)**2 - x_mod_d**2)
	return y

def fuerzas_hidrodinamicas(x,v):
    xtop= x + (d/2)*jhat
    xbot= x - (d/2)*jhat
    vf=velocidades(x+0*jhat)
    vf_top=abs(velocidades(xtop)[0])
    vf_bot=abs(velocidades(xbot)[0])
    vrel=vf-v

    fD = (0.5*Cd*alpha*rho_agua*norm(vrel)*A)*vrel #Fuerza de arrastre (drag)
    fL = (0.5*CL*alpha*rho_agua*(vf_top*2 - vf_bot*2)*A)*vrel[0]*jhat #Fuerza de levante
    fW=(-m*g)*jhat
    Fh=fW+fL+fD
    return Fh 

def particula(z,t):
	zp = zeros(4*Nparticulas)
	for i in range(Nparticulas):
		xi = z[4*i:(4*i+2)]
		vi = z[4*i+2:(4*i+4)] 	
		"""
		vf = velocidades(xi,di) #Velocidad del flujo 
		vf_top = norm (velocidades(xi + (di/2) *jhat,di)) #Velocidad en parte superior de particula
		vf_bot = norm (velocidades(xi - (di/2) *jhat,di)) #Velocidad en parte inferior de particula
		vrel = vf - vi #Diferencia de velocidades en parte superior e inferior
		fD = (0.5*Cd*alpha*rho_agua*norm(vrel)*Ai)*vrel #Fuerza de arrastre (drag)
		fL = (0.5*Cl*alpha*rho_agua*(vf_top*2 - vf_bot*2)*Ai)*jhat #Fuerza de levante
		
		"""

		Fi = fuerzas_hidrodinamicas(xi,vi) #Fuerzas aplicadas a la particula
		### Verifica de que la particula no pase a negativo ###
		
		if xi[1] < perfil_fondo(xi[0],d+df): 
			if xi[1] > 0:
				Fi+= k_penal*vec_particula_fondo(xi)
			else:
				Fi[1]+= -k_penal*(xi[1])

		zp[4*i:(4*i+2)] = vi
		zp[4*i+2:(4*i+4)] = Fi / m

	### Loop para casos de choque ###
	
	for i in range(Nparticulas):
		xi = z[(4*i):(4*i+2)]
		for j in range(Nparticulas):
			if i > j:
				xj = z[(4*j):(4*j+2)]
				rij = xj - xi 			#Vector entre los centros de las particulas
				if norm(rij) < d:	#Verificación de que las distancias sean mayores a la suma de sus radios
					delta = d - norm(rij) #Distancia de traslape
					nij = rij/norm(rij) 	#Vector normalizado de centros
					Fj = k_penal*delta*nij 	#Fuerza con que se repele la particula j
					Fi = -Fj 	#Fuerza con que se repele la particula i
					zp[(4*i+2):(4*i+4)] += Fi/m #calculo de posicion
					zp[(4*j+2):(4*j+4)] += Fj/m
	
	return zp	


z0 = zeros(4*Nparticulas)
z0[0::4] = x0
z0[1::4] = y0
z0[2::4] = vx0
z0[3::4] = vy0


print 'Integrando'
z = odeint(particula, z0, t)

print 'Fin'

fig = figure ()
ax = gca() #linea suelo
for i in range(Nparticulas):
	xi = z[:, 4*i]
	yi = z[:, 4*i+1]
	col = rand(4)
	plot (xi/d,yi/d,"--.", color=col)


x = linspace(0, 1000*d,40000)
x_mod_d = (x % d) - d/2
y = sqrt((d/2)**2 - x_mod_d**2)

plot(x, y)


ax.axhline(d/2,color="k",linestyle="--")
xlabel("x/d")
ylabel("z/d")
title("Movimiento de particulas (plano XY)")
legend()

show ()
 


figure()
for i in range(2):
	for part in range(Nparticulas):
		subplot(2,1,i+1)
		x1 = z[:,part*4:2+part*4]
		plot(t,x1[:,i],label="x"+str(p+1))
		plt.title("Particula "+str(p+1)+'\nPosicion')
		plt.legend()

show()



"""

fig = figure()


x = linspace(0, 20*df*tmax/dt,4000)
x_mod_d = (x % df) - df/2
y = sqrt((df/2)**2 - x_mod_d**2)
plot(x,y,"--", color="k")

ax = gca()
for i in range(Nparticulas):
	xi = z[:,4*i]/d
	yi = z[:,4*i+1]/d
	col = rand(3)
	plot(xi[0],yi[0],"o", color="r")
	plot(xi/d,yi/d,"--.", color=col)
	for x,y in zip(xi,yi): #Marca inicio de particula
		ax.add_artist(Circle(xy=(x,y),radius=d/2,color=col,alpha=0.7))
	#for j in range(int(tmax/dt)): #Marca esferas
		#if j%8 == 0: 
			#circle = plt.Circle((xi[j], yi[j]), d/2, color ='r', clip_on=True)
		#ax.add_artist(circle)	
		
	#plot (xi[0], yi[0], "o", color ="r")



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
#axis("equal")
#show()
