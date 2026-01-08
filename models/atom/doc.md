# Arquitectura del Atomo

## diagrama de Moeller

![Diagrama de Moeller](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Moeller_diagram.svg/1200px-Moeller_diagram.svg.png)

los electrones siguen una ruta diagonal, en química conocida como la regla de las diagonales.

s: puede cargar hasta 2 electrones
p: puede cargar hasta 6 electrones
d: puede cargar hasta 10 electrones
f: puede cargar hasta 14 electrones

Orden de llenado: 1s - 2s - 2p - 3s - 3p - 4s - 3d - 4p - 5s - 4d - 5p - 6s - 4f - 5d - 6p - 7s - 5f - 6d - 7p

1s
2s 2p
3s 3p
4s 3d 4p
5s 4d 5p
6s 4f 5d 6p
7s 5f 6d 7p

los electrones buscan primero formarse en donde haya más "espacio" disponible, es decir, 
antes que empezara llenar 3s, comensarán a intentar llenar a 2p, porque necesita más energía para formarse en 3s que en 2p

p empieza desde 2 y no desde 1, s puede tener hasta 2 electrones, al llegar a 3s contaríamos 6 electrones, y como p puede albergar hasta 6 electrones, entonces se desbloquea ese nivel.


n = es el piso, puede ser cualquier nímero entero positivo
l = la forma solo puede tomar valores enteros que van desde el 0 hasta n - 1

# n=1
según la regla, l solo puede ser desde 0 hasta 1-1 = 0
solo existe l = 0 es la obital s, en el primer piso solo hay 1s, no hay espacio matemático para un p

# n=2
aquí l puede ser desde 0 hasta 2-1 = 1
entonces existe l = 0 y l = 1
l = 0 es la obital s
l = 1 es la obital p

# n=3
aquí l puede ser desde 0 hasta 3-1 = 2
entonces existe l = 0, l = 1 y l = 2
l = 0 es la obital s
l = 1 es la obital p
l = 2 es la obital d

ejercicio con el sodio
el sodio tiene 11 electrones

acomodarlos:
# n=1
l = 0 <= n -1 = 1 - 1 = 0
solo tenemos l=0, es decir, solo existe 1s a s = 2 electrones
entonces 1s = 2 electrones

# n=2
l = 0 <= n -1 = 2 - 1 = 1
tenemos l=0 y l=1, entonces tenemos 2s y 2p
s puede tener hasta 2 electrones, p puede tener hasta 6 electrones
entonces 2s = 2 electrones y 2p = 6 electrones
con un total de 8 electrones

# n=3
l = 0 <= n -1 = 3 - 1 = 2
entonces tenemos l=0, l=1 y l=2, entonces tenemos 3s, 3p y 3d, 
pero el sodio solo tiene 11 electrones, entonces solo se llena hasta 3s con un electron
o sea 3s1

en total quedaría 1s2 2s2 2p6 3s1

# vizualisando sodio

- 1 Núcleo: 11 protones (+)
- capa 1 (1s2) 
- capa 2 (2s2 2p6) una esfera más grande 2s que envuelve a la pequeña, y tres "cacaguates" (2p) cruzándose en X, Y y Z envolviendo las esferas
- capa 3, 3s1: una esfera gigante y muy difusa que envuelve todo lo anterior 

# Ejercicio 2 Hierro

Z = 26
 si siguieramos llenando los niveles de forma puramente lineal el átomo sería inestable y colapsaría. 
 regla n +1
 para saber que orbital se llena primero, los físicos ussan la regla de madelung, el electrón siempre elegirá el orbital donde la suma de n + 1 sea menor.

para el orbital 4s: n = 4, l = 0 -> suma = 4
para el orbital 3d: n = 3, l = 2 -> suma = 5

matemáticamente, el piso 4 en su forma de esfera simple es más barato de mantener que el piso 3 en su forma de trébol complejo, por eso el 4s se llena antes que el 3d.

## n=1
l = 0 <= n -1 = 1 - 1 = 0
Solo hay 1s llenamos con 2 (quedan 24) -> 1s2

## n=2
hay l = 0 <= n - 1 = 2 - 1 = 1
l = 0 es la obital s
l = 1 es la obital p

Hay 2s y 2p, llenamos con 2 y 6. (quedan 16) -> 2s2 2p6

## n=3
l = 0 <= n - 1 = 3 - 1 = 2
l = 1 <= n - 1 = 3 - 1 = 2
l = 2 <= n - 1 = 3 - 1 = 2

l = 0 es la obital s
l = 1 es la obital p
l = 2 es la obital d

Hay 3s y 3p. llenamos con 2 y 6 quedan 8 -> 3s2 3p6

## n=4
l = 0 <= n - 1 = 4 - 1 = 3
l = 1 <= n - 1 = 4 - 1 = 3
l = 2 <= n - 1 = 4 - 1 = 3
l = 3 <= n - 1 = 4 - 1 = 3

l = 0 es la obital s
l = 1 es la obital p
l = 2 es la obital d
l = 3 es la obital f

 Salto, antes de tocar 3d, el mapa nos manda al 4s. llenamos con 2 quedan 6 -> 4s2
 regreso al nivel 3 ahora sí, los 6 que sobran entran al 3d -> 3d6

resultado final 
```json
[
    {
        "n": 1,
        "l": 0,
        "electrons": 2
    },
    {
        "n": 2,
        "l": 0,
        "electrons": 2
    },
    {
        "n": 2,
        "l": 1,
        "electrons": 6
    },
    {
        "n": 3,
        "l": 0,
        "electrons": 2
    },
    {
        "n": 3,
        "l": 1,
        "electrons": 6
    },
    {
        "n": 3,
        "l": 2,
        "electrons": 6
    },
    {
        "n": 4,
        "l": 0,
        "electrons": 2
    },
    {
        "n": 4,
        "l": 1,
        "electrons": 6
    },
    {
        "n": 4,
        "l": 2,
        "electrons": 6
    },
    {
        "n": 4,
        "l": 3,
        "electrons": 6
    }
]
```

 