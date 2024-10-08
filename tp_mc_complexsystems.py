# -*- coding: utf-8 -*-
"""TP-MC-ComplexSystems.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YF8YxmbGEx5TxUM2ihqx6WzUXwAUsXOr
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve, generate_binary_structure

N = 16
aleatorio = np.random.random((N, N))
matriz_n = np.zeros((N, N))
matriz_n[aleatorio >= 0.75] = 1
matriz_n[aleatorio < 0.75] = -1
aleatorio = np.random.random((N, N))
matriz_p = np.zeros((N, N))
matriz_p[aleatorio >= 0.25] = 1
matriz_p[aleatorio < 0.25] = -1
plt.imshow(matriz_p)

def energia(matriz):
    kernel = generate_binary_structure(2, 1)
    kernel[1][1] = False
    arr = -matriz * convolve(matriz, kernel, mode='constant', cval=0)
    return arr.sum()
energia(matriz_p)

"""# **Variables Principales:**
spin_matriz: Matriz de espines que representa el estado del sistema.

*   pasos: Número de iteraciones del algoritmo.
*   J: Constante de interacción entre espines.
*   T: Temperatura del sistema.
*   energia_inicial: Energía inicial del sistema.


# **Funcionamiento del Algoritmo:**


1.   Se selecciona un punto aleatorio en la matriz de espines y se propone un cambio de espín.
2.   Se calcula el cambio en la energía del sistema debido al cambio de espín.


3.   Se acepta o rechaza el cambio de espín con una probabilidad que depende de la energía y la temperatura.
4.   Se actualiza la matriz de espines y la energía del sistema.


5. Se repiten los pasos 1-4 durante el número especificado de iteraciones.   








# **Resultados:**


*   spins_red: Arreglo que contiene la magnetización promedio del sistema en cada iteración.
*   
energia_red: Arreglo que contiene la energía promedio del sistema en cada iteración.

"""

def metropolis(spin_matriz, pasos, J, T, energia_inicial):
    spin_matriz = spin_matriz.copy()
    spins_red = np.zeros(pasos - 1)
    energia_red = np.zeros(pasos - 1)
    energia_actual = energia_inicial
    for t in range(pasos - 1):
        x = np.random.randint(0, N)
        y = np.random.randint(0, N)
        spin_i = spin_matriz[x, y]
        spin_f = spin_i * -1
        E_i = 0
        E_f = 0
        if x > 0:
            E_i += -spin_i * spin_matriz[x - 1, y]
            E_f += -spin_f * spin_matriz[x - 1, y]
        if x < N - 1:
            E_i += -spin_i * spin_matriz[x + 1, y]
            E_f += -spin_f * spin_matriz[x + 1, y]
        if y > 0:
            E_i += -spin_i * spin_matriz[x, y - 1]
            E_f += -spin_f * spin_matriz[x, y - 1]
        if y < N - 1:
            E_i += -spin_i * spin_matriz[x, y + 1]
            E_f += -spin_f * spin_matriz[x, y + 1]
        dE = E_f - E_i
        if (dE > 0) * (np.random.random() < np.exp(-dE / (J * T))):
            spin_matriz[x, y] = spin_f
            energia_actual += dE
        elif dE <= 0:
            spin_matriz[x, y] = spin_f
            energia_actual += dE
        spins_red[t] = spin_matriz.sum()
        energia_red[t] = energia_actual
    return spins_red, energia_red
spins, energias = metropolis(matriz_n, 100000, 1, 1, energia(matriz_n))

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(spins / N**2)
plt.xlabel('Paso')
plt.ylabel('Magnetización Promedio')
plt.grid(True)
plt.subplot(1, 2, 2)
plt.plot(energias)
plt.xlabel('Paso')
plt.ylabel('Energía Promedio')
plt.grid(True)
plt.suptitle('Convergencia del Algoritmo de Metropolis', y=1.07, size=18)
plt.tight_layout()
plt.show()



"""Metropolis sistemas libres de cc"""

def metropolis_np(spin_matriz, pasos, J, T, energia_inicial):
    spin_matriz = spin_matriz.copy()
    spins_red = np.zeros(pasos - 1)
    energia_red = np.zeros(pasos - 1)
    energia_actual = energia_inicial
    for t in range(pasos - 1):
        x = np.random.randint(0, N)
        y = np.random.randint(0, N)
        spin_i = spin_matriz[x, y]
        spin_f = spin_i * -1
        E_i = 0
        E_f = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            xn, yn = x + dx, y + dy
            if 0 <= xn < N and 0 <= yn < N:
                E_i += -spin_i * spin_matriz[xn, yn]
                E_f += -spin_f * spin_matriz[xn, yn]
        dE = E_f - E_i
        if (dE > 0) * (np.random.random() < np.exp(-dE / (J * T))):
            spin_matriz[x, y] = spin_f
            energia_actual += dE
        elif dE <= 0:
            spin_matriz[x, y] = spin_f
            energia_actual += dE
        spins_red[t] = spin_matriz.sum()
        energia_red[t] = energia_actual
    return spins_red, energia_red
J = 1.0
T = 1.0
spins, energias = metropolis_np(matriz_n, 1000000, J, T, energia(matriz_n))
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(spins / N**2)
plt.xlabel('Paso')
plt.ylabel('Magnetización Promedio')
plt.grid(True)
plt.subplot(1, 2, 2)
plt.plot(energias)
plt.xlabel('Paso')
plt.ylabel('Energía Promedio')
plt.grid(True)
plt.suptitle('Sistema Libre', y=1.07, size=18)
plt.tight_layout()
plt.show()

"""# **PUNTO 3**"""

import numpy as np
import matplotlib.pyplot as plt

# Definición de constantes
TAMANIO_RED = 16

def metropolis(matriz_spines, pasos, beta_inversa, energia_inicial):
    matriz_spines = matriz_spines.copy()
    spins_red = np.zeros(pasos-1)
    energia_red = np.zeros(pasos-1)
    energia_actual = energia_inicial
    for t in range(0, pasos-1):
        x = np.random.randint(0, TAMANIO_RED)
        y = np.random.randint(0, TAMANIO_RED)
        spin_inicial = matriz_spines[x, y]
        spin_final = spin_inicial * -1

        energia_inicial_temp = 0
        energia_final_temp = 0
        if x > 0:
            energia_inicial_temp += -spin_inicial * matriz_spines[x-1, y]
            energia_final_temp += -spin_final * matriz_spines[x-1, y]
        if x < TAMANIO_RED - 1:
            energia_inicial_temp += -spin_inicial * matriz_spines[x+1, y]
            energia_final_temp += -spin_final * matriz_spines[x+1, y]
        if y > 0:
            energia_inicial_temp += -spin_inicial * matriz_spines[x, y-1]
            energia_final_temp += -spin_final * matriz_spines[x, y-1]
        if y < TAMANIO_RED - 1:
            energia_inicial_temp += -spin_inicial * matriz_spines[x, y+1]
            energia_final_temp += -spin_final * matriz_spines[x, y+1]

        delta_energia = energia_final_temp - energia_inicial_temp
        if (delta_energia > 0) * (np.random.random() < np.exp(-beta_inversa * delta_energia)):
            matriz_spines[x, y] = spin_final
            energia_actual += delta_energia
        elif delta_energia <= 0:
            matriz_spines[x, y] = spin_final
            energia_actual += delta_energia

        spins_red[t] = matriz_spines.sum()
        energia_red[t] = energia_actual

    return spins_red, energia_red

def obtener_energia_spin(matriz, betas_inversas):
    magnetizaciones = np.zeros(len(betas_inversas))
    energias_promedio = np.zeros(len(betas_inversas))
    desviaciones_energia = np.zeros(len(betas_inversas))
    for i, beta_inversa in enumerate(betas_inversas):
        spins, energias = metropolis(matriz, 1000000, beta_inversa, obtener_energia(matriz))
        magnetizaciones[i] = spins[-100000:].mean() / TAMANIO_RED**2
        energias_promedio[i] = energias[-100000:].mean()
        desviaciones_energia[i] = energias[-100000:].std()
    return magnetizaciones, energias_promedio, desviaciones_energia
def obtener_energia(matriz):
    energia = 0
    for i in range(TAMANIO_RED):
        for j in range(TAMANIO_RED):
            spin_i = matriz[i, j]
            if i > 0:
                energia += -spin_i * matriz[i-1, j]
            if i < TAMANIO_RED - 1:
                energia += -spin_i * matriz[i+1, j]
            if j > 0:
                energia += -spin_i * matriz[i, j-1]
            if j < TAMANIO_RED - 1:
                energia += -spin_i * matriz[i, j+1]
    return energia

# Inicialización de la matriz de spines
matriz_spines = np.random.choice([-1, 1], size=(TAMANIO_RED, TAMANIO_RED))

betas_inversas = np.arange(0.1, 2, 0.05)
magnetizaciones, energias_promedio, desviaciones_energia = obtener_energia_spin(matriz_spines, betas_inversas)
print(str(desviaciones_energia))
# Gráfico de las magnetizaciones
plt.figure(figsize=(8, 5))
plt.plot(1/betas_inversas, magnetizaciones)
plt.grid(True)
plt.show()