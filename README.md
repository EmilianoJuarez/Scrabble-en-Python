# Scrabble Game

Este es un juego de Scrabble en Python que permite jugar entre dos jugadores en una interfaz gráfica utilizando `tkinter`. Los jugadores deben formar palabras válidas con fichas aleatorias y acumular puntos. El juego incluye verificación de palabras válidas y gestión de turnos, además de un sistema de puntuación basado en las letras utilizadas.

## Características

- **Interfaz gráfica:** Desarrollada con `tkinter` para facilitar la interacción con los jugadores.
- **Diccionario de palabras:** Utiliza un archivo de texto (`palabras.txt`) para verificar la validez de las palabras.
- **Fichas aleatorias:** Los jugadores reciben un conjunto inicial de 7 fichas y deben formar palabras con ellas.
- **Sistema de puntuación:** Las palabras tienen un valor basado en las letras utilizadas, siguiendo las reglas del Scrabble.
- **Verificación de palabras:** Las palabras jugadas se validan utilizando un trie para buscar rápidamente en el diccionario.
- **Gestión de turnos:** El juego alterna entre dos jugadores, actualizando la puntuación y las fichas disponibles.

## Requisitos

- Python 3.x
- `tkinter` (usualmente incluido con Python)
- Archivos de texto para el diccionario de palabras (`palabras.txt`) y las fichas (`fichas.txt`)

## Instalación


