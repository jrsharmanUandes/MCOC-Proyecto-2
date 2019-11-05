# MCOC-Proyecto-2
Readme Personal Nicolás Yeomans

El objetivo principal de esta entrega consiste en medir el tiempo y realizar una validación respecto a la simulación del transporte de sedimentos.Ademas, se busca optimizar el modelo, reduciendo los tiempos de integración.

Características de computador:
===============
Modelo: Acer Aspire A315-51

Procesador: Intel(R) Core(TM) i5-7200 CPU @ 2.50GHz 2.71GHz.

Memoria instalada (RAM): 8.00 GB.

Tipo de sistema:  Sistema operativo de 64 bits.

Sitema operativo: Windows 10

Programa Python-2.7 escritor de texto Sublime text 3


Tiempo de simulación:
===============
Cabe destacar que se considera un dt=0,00001[s] , y un tiempo_maximo= 0,2[s]

N=2: Tiempo transcurrido 16,6 segundos.

N=5: Tiempo transcurrido 40.4 segundos.

N=10: Tiempo transcurrido 86,53 segundos.

N=20: Tiempo transcurrido 185,25 segundos.

El objetivo principal en esta ocasión fue reducir los tiempos, y lograr un crecimiento lineal a medida que aumenta el número de partículas. En la entrega 4 se observó que el crecimiento del tiempo era cuadrático, donde el mayor tiempo se llevaba a cabo en el integrador de Python odeint, por ende, esta optimización reduce el tiempo de integración, de tal forma que el computador sea capaz de integrar en menos tiempo, dado que el intervalo es menor. 
Por otra parte, se realiza dos procesos de integración, uno de forma individual y otro cuando hay impacto entre partículas. Además, se incorporan comandos capaces de crear archivos de textos con el fin de ir controlando la posición y velocidad de cada partícula.



