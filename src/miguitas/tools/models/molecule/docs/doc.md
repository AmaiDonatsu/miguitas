# Modelo de molecula
El modelo de la molecula estará diseñado para abstraer la información de una molecula y además simular su comportamiento y sus reacciones químicas.

## plan:
* 1 - crear una molecula: para construir una molecula, primero se le pasan los átomos u otras moleculas que la componen, y las energías necesarias para que la molecula se forme si son necesarias.
* 2 - verificar la posibilidad de que la molecula se forme: se deben añadri unas funciones que hagan unos calculos internos, para verificar que la molecula pueda formarse, por ejemplo, si la molecula requiere energía para formarse, se debe verificar que la energía disponible sea suficiente, o que los atomos o moleculas sean lo suficientemente reactivos, si no lo son, entonces lo que devolvera serán todos los componentes separados sin la molecula formada.
* 3 - interactuabilidad de la molecula: añadir funciones que permitan que la molecula interactúe con otros átomos o moleculas, por ejemplo, si a la molecula se le pone a que interactúe con un oxidante, entonces debe oxidarse, y si la reacción modifica la molecula principal, modificará sus propiedades, además si produce otros productos o residuos los devolverá.


## Construcción de la molecula
#### Ejemplo con el carbono: 
un átomo de carbono con 6 electrones es eléctricamente neutro, la suma de cargas es cero
$(+6 protones) + (-6 electrones) = 0$

sin embargo aunque es neutro no está completamente "satisfecho".

* el primer piso, solo tiene espacio para 2 electrones, está lleno.
* el segundo piso (la capa de valencia) tiene espacio para 8 electrones, pero, solo tiene 4.

Aquí es dondee entra la Regla del Octeto, aunque el átomo sea neutro su geometría interna está cincompleta. para alcanzar laa estabilidad máxima (menor energía posible) el carbono "necesita" 4 electrones más.

## 2 ¿Cómo medimos esta "hambre de energía?
No usamos una regla, usamos enerrgía de intercambio, hay tres formas principales de medirla:

### A: Energía de Ionización (EI):
Es la energía necesaria para robarle un electrón a un átomo, se mide en electronvoltios ($eV$) o kilojoules ($KJ$) por mol ($KJ/mol$).

X + energía -> X$^+$ + e$^-$

### B Afinidad electrónica (AE):
Es la energía que se libera cuando un átomo captura un electró, es como el "alivio" energético que siente el átomo al estar más cerca de completar su capa

### C Ley de Coulomb:
A nivel fundamenta, todo se mide con la fuerza de atracción entre cargas, la energía potencial, eléctrica se calcula así:

$U = k \frac{q_1 q_2}{r^2}$

Donde $q_1$ y $q_2$ son las cargas, $r$ es la distancia entre ellas y $k$ es la constante de Coulomb.

## e la gemometría, la pelea por el espacio

la repulsión de cargas negativas provoca las formas, esto se llama teoría de repulsión de pares de electrónes de la capa de valencia VSEPR
los electrones son nuves de carga negativa, como un negativo con negativo, se repelen, estas nubes intentan alejarse lo más posible unas de otras mientras sigen ancladas al núcelo

* si tienes 2 grupos de electrones se ponen a $180°$ (forma lineal).
* si tienes 4 grupos como el metano $CH_4$, la forma más legana posible en 3D es un tetraedro con ángulos de $109.5°$.
