# MCOC-Proyecto-2

Introducción
==============

El principal objetivo del presente proyecto es la instauración de un código que simule el proceso que lleva a la sedimentación de las partículas al transportar cantidades de agua en superficies no completamente lisas, bajo el contexto de la mecánica de fluidos. En superficies que no son lisas o poseen partículas en suspensión la tensión de corte originada por el fluído puede generar una serie de inconvenientes, al arrastrar las partículas del fondo en el sentido del movimiento del fluido. Para la ingeniería civil y sus aplicaciones como la construcción de represa y transporte de agua, es necesario poder predecir este transporte de sedimentos, para así lograr prevenir los inconvenientes que se puedan presentar y el costo que se invertirá en esto. 

Integrantes
==============

Gabriela Isidora Orellana
Gabriel Riquelme
John Sharman
Nicolas Yeomans

Entrega 3: Modelación del perfil de velocidad de una partícula 
==============
Se modeló el comportamiento de una partícula dado un perfil de velocidades sencillo en dos dimensiones. Los parámetros tomados en cuenta fueron la masa de la partícula, su dimensión, la gravedad de la partícula sumergida y el coeficiente drag, relacionado con la fuerza de arrastre. De este modo se definen las fuerzas que actuan sobre la partícula y con estas su aceleración, y usando el método iterativo de euler se predice la posición de esta en un instante de tiempo determinado. Finalmente, se muestra un gráfico que indica la posición de la partícula en el tiempo. 

Resultados
==============

Mediante el código realizado se obtuvo el siguiente gráfico, el cual indica la posición de una partícula, arrastrada por el fluido en sus com ponentes X,Y:

![imagen_entrega_03](https://user-images.githubusercontent.com/53490100/66011537-ee42df80-e499-11e9-8348-09c269d8cbe5.PNG)

Al utilizar la integración propia de python y agregar la condición de rebote de la partícula con el fondo se obtuvo la siguiente gráfica para la posición en el tiempo.

![con_rebote](https://user-images.githubusercontent.com/53490100/66012138-4f6bb280-e49c-11e9-9af2-b6b18cd7ac7f.PNG)

Al observar el último gráfico obtenido, se puede apreciar que modela de mejor forma el comportamiento de una partícula al ser arrastrada por un fluído, esto corresponde al inicio de la modelación, pues falta incorporar fuerzas a las cuales está sometida la partícula dentro del fluído.

Entrega 4: Validación de múltiples partículas 
==============
Para incorporar en el modelo la simulación del movimiento de múltiples partículas (N), fue necesario definir la posición en el tiempo de cada partícula para esto se utilizaron integradores de Python como "odeint" el cual recorre una función en el tiempo "t", es decir recorre la función "t" veces. Para hacer aún más real la simulación, se creó la función partícula la cual define el choque de partículas, además, se consideró una función con las fuerzas hidrodinámicas (fuerza de arrastre(drag), fuerza de levante(liftting) y fuerza peso) y con relacion al choque de las particulas en el fondo.
Para identificar que partículas chocan, se establece un vector de distancia, la cual compara la distancia entre el centro de dos partículas en relación con los radios de estas, esto indica si las partículas chocan o no. Al producirse la colisión, las partículas en cuestión cambian su velocidad y posición, esto se debe a la conservación de momentum.

Cabe destacar que para efectos de este modelo se consideró un numero de partículas N=2,5,10,20.

Parámetros de diseño:
===============
- Densidad de partícula:  2650 kg/m3. 
- Densidad del agua: 1000 kg/m3.
- Partícula esférica
- Diámetro de la partícula: ### mm.
- Constante de arrastre(drag): 0.47 
- Constante de levante(liftting):0.2
- Esfuerzo de corte:0.067

Lectura Código
=================
Para efectos de código se creó una simulación la cual lee las condiciones iniciales para cada simulación entregada por saf correspondiente a pack_validacion, cada una con su respectiva carpeta para un cierto número de partículas.

Simulación 1
==========
![simulacion_1_1](https://user-images.githubusercontent.com/53490100/66692259-032a2a80-ec73-11e9-99a9-eeb704ead90e.PNG)

![simulacion_1_2](https://user-images.githubusercontent.com/53490100/66692291-69af4880-ec73-11e9-8829-879e9a4b12af.PNG)


Simulación 2
==========
![simulacion_2_1](https://user-images.githubusercontent.com/53490100/66692394-5fda1500-ec74-11e9-99d3-7f5ca6225888.PNG)

![simulacion_2_2](https://user-images.githubusercontent.com/53490100/66692397-741e1200-ec74-11e9-83af-e16d54c8e442.PNG)



Simulación 3
==========
![simulacion_3_1](https://user-images.githubusercontent.com/53490100/66692480-2ce45100-ec75-11e9-899d-150267f282ca.PNG)

![simulacion_3_2](https://user-images.githubusercontent.com/53490100/66692491-3ff72100-ec75-11e9-9ac7-01589732e143.PNG)

Simulación 4
==========
![simulacion_4_1](https://user-images.githubusercontent.com/53490100/66692790-30c5a280-ec78-11e9-9122-6e3feab0b734.PNG)

![simulacion_4_2](https://user-images.githubusercontent.com/53490100/66692798-476bf980-ec78-11e9-9a85-bff59d5917ea.PNG)
