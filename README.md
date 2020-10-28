# Convertidor de Gramáticas

Este proyecto esta pensado para crear un convertidor de gramaticas a:

- Gramática equivalente en forma normal de Chomsky
- Gramática equivalente en forma normal de Greibach
- Un automata de pila que acepte el lenguaje

Dentro de esta carpeta se encuentra el archivo de python `project.py` el cual es necesario ejecutar para poder usar el software.

## Consideraciones

Para poder hacer uso de este software se necesita tener instalada la librería de Graphviz tanto en su sistema como en python.

## Flujo del Sistema

El flujo del sistema es algo sencillo, `project.py` es el archivo que se necesita ejecutar para correr el software, se le pide al usuario el nombre del archivo .txt el cual contiene la gramática.

Las gramáticas que soporta este sistema se escriben de la siguiente forma:

```
S->aSb|b|
```

En este caso el poner un pipe antes de dejar vacío indica una epsilon producción.

Tras recibir el archivo el proceso que sigue es el siguiente:

1. Se lee el archivo y se genera un diccionario basado en la gramatica
2. Se limpia la gramática (Se eliminan las producciones unitarias, epsilon producciones y producciones inútiles)
3. Se transforma a una gramática en la forma normal de Chomsky (`toChomsky`)
    - Se crean simbolos `0-9` para las nuevas producciones unitarias
    - Se crean simbolos `C_` para las producciones con mas de dos generadores
4. Se llama a la función `printGrammar` la cual crea un archivo `-Chomsky.txt` la cual tiene la representación de la gramática en la forma normal de Chomsky
5. Se transforma a una gramática en la forma normal de Greibach (`toGreibach`)
    - Realiza los reemplazos necesarios respecto la nueva numeración
    - Elimina la recursividad por la izquierda de la gramática
    - Realiza la sustitución de elementos para terminar la forma normal
6. Se llama a la función `printGrammar` la cual crea un archivo `-Greibach.txt` la cual tiene la representación de la gramática en la forma normal de Greibach
7. Se llama a la función `toAutomaton` la cual crea un archivo `.pdf` el cual contiene el automata que acepta el lenguaje

---

*Desarrollado por Diego Cabrera Nieto*

*Matrícula A01633860*

*Tecnológico de Monterrey Campus Guadalajara*
