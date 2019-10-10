from matplotlib.pylab import*
# unidades base SI(m,kg,s)
_m=1
_kg=1
_s=1
_mm=1e-3*_m
_gr=1e-3*_kg

vfx= 5.0 *_m/_s     #m/s
vfy=0.0   *_m/_s    #m/s

x0=array([0.,1.], dtype=double)  # particula en posicion cero 
v0=array([1.,1.], dtype=double) # velocidad en 1 m/s para x y en y

xi=x0#zeros(2, dtype=double)           # posicion actual
vi=v0#zeros(2, dtype=double)           # velocidad actual
xim1=zeros(2, dtype=double)         # posicion siguiente
vim1=zeros(2, dtype=double)         # velocidad siguiente

# parametros 
g=9.81*_m/_s**2
d=1*_mm
rho=2700*_kg/(_m**3)
Cd=0.47  # drag para una particula # coeficiente de drag

m=rho*(4./3./8.)*pi*(d**3)              # masa de particula

# inicializar Euler en x0

dt= 2e-6*_s     #paso de tiempo 
tmax=0.1*_s        # tiempo maximo de simulacion
ti= 0.*_s          #tiempo actual

W=array([0,-m*g])   # vector que en x es 0 y en y es -mg
vf=array([vfx,vfy])  # velocidad del fluido

Nt=int32(2*tmax/dt)      # numero de pasos
x_store=zeros((2,Nt))    
v_store=zeros((2,Nt))
t_store=zeros(Nt)

# metodo de euler

i=0
while ti < tmax:

    if i%100==0:
        print "ti=",ti,"|xi|=", sqrt(dot(xi,xi))
    #print "xi=",xi
    #print #vi=",vi
    
    #evaluar v. relativa
    vrel=vf-vi
    norm_vrel=sqrt(dot(vrel,vrel))    
    # evaluar fuerzas sobre la particula
    fD=0.5*Cd*norm_vrel*vrel
    Fi=W+fD
    # print "Fi=",Fi
    
    #evaluar aceleracion
    ai=Fi/m
    # print "ai=",ai
    
    # integrar
    xim1=xi + vi*dt + ai*(dt**2/2)
    vim1=vi + ai*dt
    
    # avanzar al siguiente paso
    x_store[:,i]=xi
    v_store[:,i]=vi
    t_store[:]=ti

    ti+=dt
    i+=1
    xi=xim1
    vi=vim1
    
# guardar ultimo paso
x_store[:,i]=xi
v_store[:,i]=vi
t_store[i]=ti

print x_store

figure()
plot(x_store[0,:i],x_store[1,:i])
show()



