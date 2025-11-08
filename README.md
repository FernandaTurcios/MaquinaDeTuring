# MaquinaDeTuring
**1.	Descripción del programa:**
-	El programa muestra se forma gráfica/visual el funcionamiento de una Máquina de Turing. En este caso lo que se hace es verificar si una cadena es aceptada o rechazada por un lenguaje y en la simulación se observa como carácter por carácter va siendo analizado. En la simulación se puede ver la cinta y el cabezal de la máquina. 
-	La ejecución puede ser paso a paso o de forma automática, al final independientemente de la forma en que se ejecute se mostrará si la cadena es aceptada o rechazada. 
-	También, casa carácter que es leído se cambia por una “p”, una q” o una “r”.
  
**2.	Instrucciones de instalación y ejecución:**
-	Para poder correr el proyecto se necesita contar con Python instalado (Python 3.10+).
-	La carpeta del proyecto debe de abrirse en Visual Studio 2022 o cualquier otro editor, se recomienda este porque fue el que se utilizó para trabajar el proyecto. 
-	Después se debe ejecutar desde la clase MaquinaDeTuring.py
  
**3.	Ejemplo de ejecución:**
-	En pantalla aparecerá la Maquina de Turing gráfica, lo primero que se debe hacer es seleccionar el lenguaje que se quiera utilizar haciendo click en recuadro de la esquina superior derecha, se desplegarán opciones, se debe seleccionar una.  
-	Después de haber seleccionado el lenguaje se debe colocar la cadena que se quiera analizar en el recuadro donde se solicita la cadena (esquina superior izquierda) y presionar el botón de "aplicar", automáticamente la cadena aparecerá en la cinta.
-	Posteriormente puede presionar el botón “iniciar” para que la simulación avance automáticamente o presionar “paso” para ir moviendo la cinta paso por paso hasta que finalice el proceso.  Estos se encuentran centrados en la parte inferior de la interfaz. 
-	Al finalizar la simulación se mostrará un mensaje en el que avisa si la cadena es aceptada o rechazada por el lenguaje después de pasar por la MT. Se muestra debajo de la cinta.
-	Si se desea analizar otra cadena es importante presionar el botón “reiniciar” antes de volver a correr la cinta, ya sea paso a paso o automáticamente. Este también se encuentra en la parte inferior de la pantalla.
  
**4.	Explicación de las expresiones regulares:**

**L1: a(b|aa)***
-	Acepta cadenas que inician con a y luego contienen cero o más bloques, donde cada bloque es b o aa.
-	Después de la primera a, la cadena avanza, o agrega un b, o agrega un par aa.
-	Ejemplos aceptados: a, ab, aaa, abaa.
-	Ejemplos rechazados: b.
-	
**L2: 0*1***
-	Acepta cualquier cantidad de ceros seguidos de cualquier cantidad de unos.
-	Todos los 0 aparecen antes que los 1, una vez que la cadena tiene un 1, ya no puede volver a 0.
-	Ejemplos aceptados: 0, 1, 00111.
-	Ejemplos rechazados: 10, 101.

**L3: ([ab]|c[ab])*c**
-	Acepta cadenas que terminan en c y no contienen cc (no hay dos c consecutivas).
-	Entre letras a y b se puede intercalar c, pero cada c debe estar seguida por a o b, menos la última que cierra la cadena.
-	Ejemplos aceptados: ac, bc, abc, cabac.
-	Ejemplos rechazados: cualquier cadena con cc, a, ab.
  
 **L4: (a|b)*a(a|b)***
-	Acepta todas las cadenas sobre {a, b} que contienen al menos una a (en cualquier posición).
-	La expresión permite cualquier mezcla de a y b, mientras exista al menos una a.
-	Ejemplos aceptados: a, ba, ababa.
-	Ejemplos rechazados: b.
**L5: 1(01)*0**
-	Acepta cadenas que empiezan con 1, repiten cero o más veces el bloque 01 y terminan en 0.
-	La forma general es 1 seguido de repeticiones 01 y final 0. }
-	Ejemplos aceptados: 10, 1010, 101010.
-	Ejemplos rechazados: 1, 11, 100, 1011.
