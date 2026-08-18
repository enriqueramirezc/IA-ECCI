**PLANTEAMIENTO DE UN PROBLEMA DE BÚSQUEDA**  
 

**CONSTRUIR EL PLANTEAMIENTO DE ESTE PROBLEMA**   
**COMO UN PROBLEMA DE BÚSQUEDA**  
 

**ORDENAR COLORES**  
 

**Se tiene una matriz de 25 filas x 6 columnas donde las columnas representan 6 pilas o columnas donde se pueden colocar fichas de colores.  Al colocar las fichas éstas se van al fondo de la columna  ( similar al juego 4 en línea ).**  
 

**Existen 5 fichas de cada uno de los 5 colores disponibles, a saber (rojo, verde, azul, blanco, negro ).**  
 

**Inicialmente las fichas quedan distribuidas mezclando la cantidad de fichas por columna y los colores aleatoriamente en las 6 columnas.**  
    	

**El juego inicia con un estado donde las fichas de colores fueron colocadas aleatoriamente en cualquier columna.  Al colocar la ficha esta se va al fondo.**

**Las reglas para mover son las siguientes:**  
**1\) solo se puede mover una ficha a la vez tomada de la parte superior de cualquier columna**   
**2\) solo se puede colocar una ficha sobre el fondo vacío de una columna o sobre otra ficha que debe ser de su mismo color.**  
 

**En otras palabras: NO SE PUEDEN COLOCAR FICHAS DE UN COLOR SOBRE OTRAS DE UN COLOR DIFERENTE AL SUYO.**  
 

**El objetivo es separar por colores las fichas, y que todas las de cada color queden en una misma columna. Un posible estado objetivo (no el único) puede ser el siguiente:**

| V | R | A |   | B | N |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **V** | **R** | **A** |   | **B** | **N** |
| **V** | **R** | **A** |   | **B** | **N** |
| **V** | **R** | **A** |   | **B** | **N** |
| **V** | **R** | **A** |   | **B** | **N** |

 

**En el estado final solo se muestran las 5 filas del fondo que es donde quedan ubicadas las fichas.**

**USTEDES DEBEN FORMULAR FORMALMENTE EL PROBLEMA COMO UN PROBLEMA DE BÚSQUEDA IDENTIFICANDO LO QUE SE INDICA EN EL CUADRO, ADEMÁS CONTESTANDO LAS SIGUIENTES PREGUNTAS:**  
 

1. **¿Es su formulación del problema una formulación Incremental o de Estado Completo?**  
     
2. **¿Cuál es el máximo branching factor?**

 

**RECUERDEN**  
**![][image1]**

**LABORATORIO**  
   
   
**Pasos del laboratorio**

1. **Plantee el problema considerando:**  
   * **El estado inicial aleatorio.**  
   * **Las acciones que pueden ser ejecutadas en dicho estado.**  
   * **El modelo de transición luego de aplicar una acción sobre el estado actual.**  
   * **Prueba de cumplimiento**   
   * **Calcule el costo de transición.**  
2. **Plantee un caso específico para este problema con una baja profundidad al objetivo y dibuje todas las posibles secuencias de pasos en forma de árbol (espacio de búsqueda)**   
3. **Indique una posible solución para este ejemplo.**  
4. **Deben proponer una función heurística para este problema, que cumpla con los requerimientos teóricos y que sea capaz de determinar cuán cerca o lejos se encuentra la solución.**  
5. **Validar la heurística empleando estas propiedades: desigualdad triangular (consistencia), monotonicidad, subestimación (admisibilidad).**  
6. **Desarrolle un algoritmo de búsqueda ancho primero (BFS) sin información:**  
   * **Use tanto una lista abierta como una cerrada.**  
   * **Utilice el lenguaje de programación Python (3.13+).**

      **7\.  Modifique el código de ancho primero para que con la heurística construida lleve a cabo una exploración con el algoritmo A\*.**

**Construya una copia del cuaderno de Júpiter que se les suministra para trabajar de esa forma.  El código suministrado es con fines ilustrativos para el problema de la ventana corrediza.**  

**Explique la funcionalidad de cada segmento de código y la intención con la que fue creado.**

**Construya su código utilizando python.**

**Sugerencia: Construya el diagrama usando draw.io ( [https://app.diagrams.net/](https://app.diagrams.net/) ) ANTES de iniciar el desarrollo.**  
 

**TAREA CORTA PARA LA SIGUIENTE SEMANA ( LUNES EN OCHO )**  
   
**Basándose en el algoritmo desarrollado durante el laboratorio, deben implementar uno alternativo que permita encontrar una solución para este juego utilizando IDS\* (Se explica en libro de texto Russel) con las siguientes características:**

1. **Solución recursiva que no haga uso extensivo de memoria.**  
2. **No debe usar Lista Abierta ni Lista Cerrada sino que debe ir explorando si los nodos ubicados a la profundidad estimada con la heurística ( más la profundidad actual) corresponden al estado final de una solución.  Caso contrario estime la nueva profundidad con el menor valor de heurística calculado sobre los nodos ubicados en la profundidad explorada.**  
3. **Debe hacer uso de su heurística para establecer la profundidad de búsqueda de IDS\* en cada iteración.** 

**4\. Evalúe la complejidad espacial y temporal de los tres algoritmos creados y haga un análisis comparativo.  Para tal efecto debe ejecutar al menos 20 veces cada algoritmo y dar sus resultados basándose en un promedio de las 20 ejecuciones.** 
