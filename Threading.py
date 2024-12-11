import random
import time
import threading
from threading import Semaphore

VALOR_MAXIMO = 1000000000
NUM_NODOS = 8
GRADO = 8
NUM_HILOS = 2

class Barrera:
    def __init__(self, num_hilos):
        self.num_hilos = num_hilos
        self.cuenta = 0
        self.mutex = Semaphore(1)
        self.barrera = Semaphore(0)

    def wait_barrier(self):
        self.mutex.acquire()
        self.cuenta += 1
        self.mutex.release()
        if self.cuenta == self.num_hilos:
            self.barrera.release()
        self.barrera.acquire()
        self.barrera.release()

def generar_grafo():
    random.seed(42)
    pesos = [[0 for _ in range(GRADO)] for _ in range(NUM_NODOS)]
    indices_pesos = [[0 for _ in range(GRADO)] for _ in range(NUM_NODOS)]
    for i in range(NUM_NODOS):
        for j in range(GRADO):
            indices_pesos[i][j] = i + j
            if i != j:
                pesos[i][j] = random.randint(1, 10)
            else:
                pesos[i][j] = 0
    return pesos, indices_pesos

def inicializar_arreglos():
    distancias = [VALOR_MAXIMO for _ in range(NUM_NODOS)]
    cola = [1 for _ in range(NUM_NODOS)]
    distancias[0] = 0
    return distancias, cola

def realizar_trabajo(id_hilo, pesos, indices_pesos, distancias, cola, minimos_locales, barrera):
    nodos_restantes = NUM_NODOS
    nodo_actual = 0

    inicio_indice = id_hilo * GRADO // NUM_HILOS
    fin_indice = (id_hilo + 1) * GRADO // NUM_HILOS

    while nodos_restantes > 0:
        minimo = VALOR_MAXIMO
        indice_minimo = NUM_NODOS - 1

        for j in range(inicio_indice, fin_indice):
            if j < NUM_NODOS and distancias[j] < minimo and cola[j]:
                minimo = distancias[j]
                indice_minimo = indices_pesos[nodo_actual][j]
        minimos_locales[id_hilo] = indice_minimo

        barrera.wait_barrier()

        if id_hilo == 0:
            minimo_global = VALOR_MAXIMO
            indice_minimo_global = 0
            for k in range(NUM_HILOS):
                if distancias[minimos_locales[k]] < minimo_global and cola[minimos_locales[k]]:
                    minimo_global = distancias[minimos_locales[k]]
                    indice_minimo_global = minimos_locales[k]
            nodo_actual = NUM_NODOS - nodos_restantes
            cola[nodo_actual] = 0

        barrera.wait_barrier()

        for i in range(inicio_indice, fin_indice):
            if i < NUM_NODOS:
                vecino = indices_pesos[nodo_actual][i]
                if vecino < NUM_NODOS:
                    if distancias[vecino] > distancias[nodo_actual] + pesos[nodo_actual][i]:
                        distancias[vecino] = distancias[nodo_actual] + pesos[nodo_actual][i]

        nodos_restantes -= 1

def mostrar_matriz_adyacencia(matriz):
    letras = [chr(65 + i) for i in range(NUM_NODOS)]
    print("   ", "  ".join(letras))
    for i, fila in enumerate(matriz):
        print(f"{chr(65 + i)} ", " ".join(f"{v:3}" for v in fila))

def main():
    pesos, indices_pesos = generar_grafo()
    distancias, cola = inicializar_arreglos()

    minimos_locales = [0 for _ in range(NUM_HILOS)]
    barrera = Barrera(NUM_HILOS)

    inicio_tiempo = time.time()

    hilos = []
    for i in range(NUM_HILOS):
        hilo = threading.Thread(target=realizar_trabajo, args=(i, pesos, indices_pesos, distancias, cola, minimos_locales, barrera))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    tiempo_total = time.time() - inicio_tiempo

    print("Matriz de Adyacencia:")
    mostrar_matriz_adyacencia(pesos)

    print("\nDistancias desde el nodo origen:")
    for i, distancia in enumerate(distancias):
        print(f"Nodo {chr(65 + i)}: {distancia}")

    print(f"\nTiempo total de ejecución: {tiempo_total} segundos")

if __name__ == "__main__":
    main()
