from matplotlib.pylab import *

datos = loadtxt("resultados.txt")
print datos.shape

Nparticulas = (datos.shape[1]-1)/4

figure()

ax = gca()


color = "#006B93"
colorlist = []
for i in range(Nparticulas):
	xi = datos[:,1+4*i]
	yi = datos[:,1+4*i+1]
	col = rand(3)
	colorlist.append(col)
	ax.plot(xi[0::100], yi[0::100], "o", color=col)
	ax.plot(xi, yi, "--", color=col, alpha=0.5)

#ax.set_ylim([0,5])
ax.axhline(0.,color="k", linestyle="--")
ax.axhline(1/30., color="gray",linestyle="--")
ax.set_xlabel("$\\dfrac{x}{d}$")
ax.set_ylabel("$\\dfrac{z}{d}$")

tight_layout()

show()
	
"""
fig = figure()

ax = gca()
for i in range(Nparticulas):
	xi = z[:,4*i]/d
	yi = z[:,4*i+1]/d
	col = rand(3)
	plot(xi[0], yi[0], "o", color="r")
	plot(xi,yiy"--.", color=col)


ax.axhline(0.5,color="k",linestyle="--")
"""