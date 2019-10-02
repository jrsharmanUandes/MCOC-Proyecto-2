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
