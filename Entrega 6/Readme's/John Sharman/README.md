# MCOC-Proyecto-2
Readme Personal
John Sharman

Esta entrega tiene como objetivo medir y comparar el desempeño de los computadores de cada integrante. En relación a su modelo, sistema operativo y características. Además se busca demostrar que el código fue optimizado de tal forma de que se obtenga una linealidad dentro de la cantidad de particulas y el tiempo de cálculo de estas.

Características de computador:
==========
Modelo: Asus G750J

Procesador: Intel(R) Core(TM) i7-4700HQ CPU @ 2.40GHz

Memoria instalada (RAM): 12.00 GB.

Sistema operativo: Ubuntu 18.04

Tipo de sistema: Sistema operativo de 64 bits.

Simulación
==========

  Tiempo de simulación: 
  
      2 particulas      13,48 s
      5 particulas      34,30 s
      10 particulas     71,80 s
      20 particulas     159,68 s

![imagen_entrega_03](https://github.com/jrsharmanUandes/MCOC-Proyecto-2/blob/master/Entrega%206/Readme's/John%20Sharman/Gr%C3%A1fico%20P%20vs%20T.png)

Concluciones
==========
A partir del gráfico se pudo comprobar que se tiene un comportamiento lineal, que comparando con la entrega anterior, ya con 10 partículas tiene un desempeño mucho mejor, donde antes demoraba 154 segundos. Para el caso de 20 partículas se tiene donde pasa de 1006 a 159 segundos, se tiene una mejora de rendimiento de más de 85%. Efectivamente disminuyendo la carga de información al procesador reduciendo las iteraciones de las partículas sin riesgo de choque y guardando toda la información en el disco duro se obtiene un mejor rendimiento.
Comparando as dos entregas se puede ver como un rendimiento lineal en situaciones más exigentes tiene un rendimiento muy superior a uno exponencial o cuadrático, dado que estos últimos suelen saturarse con mayor facilidad.
