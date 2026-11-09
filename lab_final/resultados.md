# laboratorio clustering

- Andrés Camacho, Anthony Sanchez, Enrique Ramirez

## Resultados

Hay 164 palabras pero cautivación no aparece, entonces se agrupan las otras 163.

## Tamaños de los grupos (k = 4)

| Algoritmo | Distancia | Tamaños |
| --- | --- | --- |
| K-means | Euclidiana | 62, 48, 27, 26 |
| K-means | Coseno | 45, 44, 41, 33 (cambia en cada ejecución) |
| HAC, enlace completo | Euclidiana | 83, 60, 12, 8 |
| HAC, enlace completo | Coseno | 91, 51, 12, 9 |

Si se usaba HAC con enlace promedio, casi todas las palabras quedaban en un solo grupo, así que usamos enlace completo.

## Grupos

En todos los casos, suelen surgir aproximadamente los siguientes cuatro grupos: emociones positivas, emociones negativas, palabras mezcladas (coseno, alarma, alerta, cólera...) y palabras con otro significado (atención, cuidado, consideración, dicha...)

Este último grupo era el mismo con las dos distancias. Las palabras mezcladas variaban según si se usaba euclidiana o coseno.

## Hipótesis para analizar después

Es posible que las palabras se agrupen por contexto en Word2Vec, en lugar de significado. Por ejemplo, "tristeza" y "felicidad" estaban a una distancia muy similar de "alegría". Eso tendría sentido porque generalmente las palabras que son antónimos se usan en frases similares. Por ejemplo, "sentí mucha tristeza" y "sentí mucha felicidad".

Sí se separan las palabras según la emoción, pero también según el contexto.
