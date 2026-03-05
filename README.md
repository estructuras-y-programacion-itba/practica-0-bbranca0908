[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=22994891)
# Guia Práctica

## Instrucciones de GitHub Classroom

Este repositorio fue creado como parte de una asignación de GitHub Classroom. Para completar el ejercicio, sigue estos pasos:

1. **Clona el repositorio**: Una vez aceptada la asignación, GitHub creará automáticamente un repositorio personal para ti. Clónalo en tu máquina local usando `git clone`.
2. **Resuelve el ejercicio**: Modifica los archivos necesarios (principalmente `main.py`) para implementar la solución según los requisitos especificados.
3. **Realiza commits**: A medida que avances, realiza commits descriptivos de tus cambios usando `git commit -m "descripción del cambio"`.
4. **Envía los cambios**: Una vez finalizado, envía tu solución al repositorio remoto usando `git push`.

**Nota importante**: Asegúrate de que tu código esté completamente funcional y que todos los commits se hayan enviado antes del plazo establecido.

---

## Trabajo Práctico: Simulación del Juego de la Generala

### Objetivo

Escribir un programa que simule el juego de la Generala con 5 dados para 2 jugadores.

### Restricción Técnica

El programa debe estar estructurado utilizando funciones.

---

## Reglas del Juego

### Turnos

- Cada jugador tiene hasta tres tiradas por turno.
- En la primera tirada se lanzan los 5 dados.
- Después de cada tirada, el jugador decide qué dados mantener y cuáles volver a lanzar.
- El turno finaliza cuando el jugador decide no volver a lanzar ningún dado o cuando alcanza las tres tiradas.

### Puntaje y Opciones

Al finalizar su turno, el jugador debe elegir una categoría para registrar su puntaje. No se puede elegir una categoría ya utilizada anteriormente por ese jugador.

- **"E" (Escalera)**: 5 dados consecutivos. Vale **20 puntos**.
- **"F" (Full)**: 3 dados iguales y 2 dados iguales (distintos a los primeros). Vale **30 puntos**.
- **"P" (Póker)**: 4 dados iguales. Vale **40 puntos**.
- **"G" (Generala)**: 5 dados iguales. Vale **50 puntos**.
- **Números (1 al 6)**: Se anota la suma de los dados que coincidan con el número elegido (ej: tres dados "4" suman 12 puntos).

### Bonificaciones y Reglas Especiales

- **Primera Tirada**: Si se forma "E", "F" o "P" en la primera tirada del turno, se suman **5 puntos adicionales**.
- **Generala Real**: Si se forma "G" en la primera tirada del turno, se suman **30 puntos adicionales** y el juego termina inmediatamente (victoria automática).
- **Jugada Obligatoria**: Si al finalizar el turno no se tiene ninguna jugada válida disponible, el jugador debe elegir una categoría pendiente y anotar **0 puntos**.

### Fin del Juego

El juego termina cuando:
- Ambos jugadores completaron las 11 categorías en su planilla.
- O algún jugador obtuvo una **"Generala Real"**.

Al finalizar, el programa debe informar el ganador o si hubo empate.

---

## Registro de Datos (jugadas.csv)

Se debe crear una función que reciba el estado actual de la planilla y guarde la información en el archivo `jugadas.csv`.

- El archivo se crea la primera vez que se ejecuta.
- Debe respetar el formato de planilla (filas para categorías E, F, P, G, 1-6 y columnas para Jugador 1 y Jugador 2).
- El archivo debe reflejar el puntaje acumulado hasta el momento.

### Formato de Ejemplo

```
jugada,j1,j2
E,20,20
F,0,35
P,40,0
G,0,50
1,3,1
...
```
