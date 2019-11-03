# -*- coding: utf-8 -*-
from matplotlib.pylab import *
from scipy.integrate import odeint
import random 
from time import time
tiempo_inicial = time()

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

rho_agua = 1000.*_kg/(_m**3)        # Densidad del agua
rho_particula = 2650.*_kg/(_m**3)   # Densidad de las particulillas

dt = 0.00001*_s      # paso de tiempo 
tmax = 0.01*_s      # tiempo maximo de simulacion
t = arange(0, tmax, dt)
Nt=len(t)
Cd = 0.47    #Coeficiente de arrastre
Cm = 0.5    #Masa adicional
CL = 0.2    #Coeficiente de lift
Rp = 73.  # Errepe

ustar = 0.14    #  (m/s)  0.14 - 0.23 usestrella

#Nparticulas = 2    #Numero de particulas


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
print Nparticulas


tau_star = 0.067   # Tau star (Shear stress)


R = (rho_particula/rho_agua - 1)   # Esta es la letra erre
alpha = 1/(1 + R + Cm)          # A en griego, de aqui viene la palabra "alfabeto"

ihat = array([1,0])         # itongo
jhat = array([0,1])         # jotatongo

tau_cr = 0.22*Rp**(-0.6)+0.06*10**(-7*Rp**(-0.6))   # tau critico
ustar = sqrt(tau_star * g * Rp * d)     # uestrella de verdad ahora si final final ok para siempre

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
    rij = x - array([closest_s,0])  #Vector entre el centro de particula y el centro de particula de fondo mas cercana
    dist = d/2. + df/2.  #Suma de radios de particula mas particula de fondo
    if norm(rij) < dist:
        delta = dist - norm(rij) 
        nij = rij/norm(rij)
        return nij*delta
    else:
        return array([0.,0.])

def perfil_fondo(x,di): #Define el perfil de fondo
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
def choques(z,zp):
    for i in range(Nparticulas):
        xi = z[(4*i):(4*i+2)]
        for j in range(Nparticulas):
            if i > j:
                xj = z[(4*j):(4*j+2)]
                rij = xj - xi           #Vector entre los centros de las particulas
                if norm(rij) < d:   #Verificación de que las distancias sean mayores a la suma de sus radios
                    delta = d - norm(rij) #Distancia de traslape
                    nij = rij/norm(rij)     #Vector normalizado de centros
                    Fj = k_penal*delta*nij  #Fuerza con que se repele la particula j
                    Fi = -Fj    #Fuerza con que se repele la particula i
                    zp[(4*i+2):(4*i+4)] += Fi/m #calculo de posicion
                    zp[(4*j+2):(4*j+4)] += Fj/m
    return zp
def particulas(z,t):
    zp = zeros(4*Nparticulas)
    for i in range(Nparticulas):
        xi = z[4*i:(4*i+2)]
        vi = z[4*i+2:(4*i+4)]   

        
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
    
    zp=choques(z,zp)
    return zp   
def particula(z,t):
    zp = zeros(4*Nparticulas)
    for i in range(Nparticulas):
        xi = z[4*i:(4*i+2)]
        vi = z[4*i+2:(4*i+4)]   

        
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
    return zp   

###############################################

condicion_inicial= True
doit=True
resultados=open("resultados.txt","w")
tiempo_bloque_1=0
tiempo_bloque_2=0

if condicion_inicial:
    print " condicion inicial"
    data=load("initial_condition.npz")
    x0=data["x0"]
    y0=data["y0"]
    vx0=data["vx0"]
    vy0=data["vy0"]
    Nparticulas=data["Nparticulas"]
else:
    print " generando nueva condicion inicial"
    itry=1
    while True:
        dmin=infty
        
        x0=800*d*rand(Nparticulas)
        y0=5*d*rand(Nparticulas)+1*d
        for i in range(Nparticulas):
            xi,yi=x0[i],y0[i]
            for j in range(i+1,Nparticulas):
                xj,yj=x0[j],y0[j]
                dij=sqrt((xi-xj)**2 +sqrt(yi-yj)**2)
                dmin=min(dmin,dij)
        print "try#",itry,"dmin/d=",dmin/d
        if dmin>0.9*d:
            break
        itry+=1
    vx0=ustar*rand(Nparticulas)
    vy0=0
    savez("initial_condition.npz",x0=x0,y0=y0,vx0=vx0,vy0=vy0,Nparticulas=Nparticulas)
t=arange(0,tmax,dt)
Nt=len(t)
zk=zeros((4*Nparticulas))
zkm1=zeros((4*Nparticulas))
zk[0::4] = x0
zk[1::4] = y0
zk[2::4] = vx0
zk[3::4] = vy0

done=zeros(Nparticulas,dtype=int32)
impacting_set=zeros(Nparticulas,dtype=int32)
print "Integrando"
k=0
if doit:
    while dt*k< int(tmax/dt-1)*dt:
        resultados.write("{}".format(dt*k))
        savetxt(resultados,zk,fmt="%.24e",newline="")
        resultados.write("\n")

        if k%100==0:
            print "k={}  t={}".format(k,k*dt)
        done+=0

        for i in range(Nparticulas):
            irange=slice(4*i,4*i+4)
            zk_i=zk[irange]
            di=d
            if done[i]==0:
                hay_impacto =False
                impacting_set*=0
                M=1

                for j in range(i+1,Nparticulas):
                    jrange=slice(d*j,4*j+4)
                    zk_j=zk[jrange]
                    dj=d
                    rij=zk_j[0:2]-zk_i[0:2]

                    if norm(rij)<0.5*(di+dj)*3:
                        hay_impacto=True
                        impacting_set[0]=i
                        impacting_set[M]=j
                        M+=1
                if hay_impacto:
                    zk_all=zk_i
                    for j in impacting_set[1:M]:
                        jrange=slice(4*j,4*j+4)
                        zk_j=zk[jrange]
                        zk_all=hstack((zk_all,zk_j))
                    ti=time()
                    zkm1_all=odeint(particulas,zk_all,[dt*k,dt*(k+1)])
                    tf=time()
                    tiempo_bloque_1+=tf-ti
                    
                    zkm1[irange]=zkm1_all[1,0:4]
                    done[i]=1
                    pos_j=1
                    for j in impacting_set[1:M]:
                        jrange=slice(4*j,4*j+4)
                        zkm1[jrange]=zkm1_all[1,4*pos_j:4*pos_j+4]
                        done[j]=1
                        pos_j+=1
                else:
                    ti=time()
                    zkm1_i=odeint(particula,zk_i,[dt*k,dt*(k+1)])
                    tf=time()
                    tiempo_bloque_2+=tf-ti

                    zkm1[irange]=zkm1_i[1,0:4]

                    done[i]=1
        zk=zkm1
        k+=1
"""
else:
    data=load("solution.npz")
    t=data["t"]
    z=data["z"]
    dt=data["dt"]
"""
tiempo_final=time()

print "tiempo_bloque_1",tiempo_bloque_1
print "tiempo_bloque_2",tiempo_bloque_2
print "Tiempo total:",tiempo_final-tiempo_inicial

resultados.close()
exit(0)



################################################
"""
print 'Integrando'
t1=time()
z = odeint(particula, z0, t)
t2=time()
print 'Fin'
print "tiempo",(t2-t1)
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

figure()
for i in range(2):
    for part in range(Nparticulas):
        subplot(2,1,i+1)
        x1 = z[:,part*4:2+part*4]
        plot(t,x1[:,i])
        if i==0:
            plt.ylabel("Xi(t) (m)")
        else:
            plt.ylabel("Yi(t) (m)")
        plt.title("Particula "+str(Nparticulas)+'Posicion')
        plt.legend()


show()

"""