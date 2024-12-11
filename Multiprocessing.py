import random
import time
import multiprocessing
from multiprocessing import Lock, Process, Barrier, Array, Queue

def grafo(n_nodos, grado_maximo, semilla):
    random.seed(semilla)
    peso = [[0 for _ in range(grado_maximo)] for _ in range(n_nodos)]
    peso_index = [[0 for _ in range(grado_maximo)] for _ in range(n_nodos)]

    for i in range(n_nodos):
        for j in range(grado_maximo):
            peso_index[i][j] = i + j
            if i != j:
                peso[i][j] = random.randint(1, 10)
            else:
                peso[i][j] = 0

    return peso, peso_index

def inicializar_array(n_nodos, INT_MAX1):
    distancia = multiprocessing.Array('i', range(n_nodos))
    cola = multiprocessing.Array('i', range(n_nodos))
    for i in range(n_nodos):
        distancia[i] = INT_MAX1
        cola[i] = 1
    distancia[0] = 0
    return distancia, cola

def mostrar_matriz_adyacencia(peso, grado_maximo, n_nodos):
    for i in range(n_nodos):
        print(' '.join(f'{peso[i][j]:4}' for j in range(grado_maximo)))

def mostrar_soluciones(distancia, n_nodos):
    print("\nSoluciones desde el nodo inicial (A):")
    for i in range(n_nodos):
        print(f"Distancia al nodo {i}: {distancia[i]}")

def realizar_trabajo(tid, distancia, cola, n_nodos, DEG, n_procesos, id_proceso, locks, lock, terminar, rango, peso, peso_index):
    tiempo_inicio = time.time()
    n_local = n_nodos
    INT_MAX2 = 1000000000
    id_proceso[tid] = 0
    nodo_actual = 0

    grado_maximo = DEG.value
    n_procesos = n_procesos.value
    i_inicio = tid * grado_maximo // n_procesos
    i_fin = (tid + 1) * grado_maximo // n_procesos

    barrier = Barrier(n_procesos)

    barrier.wait()

    n_nodos_val = n_nodos.value
    while terminar[0] == 0:
        while id_proceso[0] < rango[0]:
            for i in range(grado_maximo):
                idx = peso_index[nodo_actual][i]
                if idx < n_nodos_val:
                    locks[idx].acquire()
                    if distancia[idx] > distancia[nodo_actual] + peso[nodo_actual][i]:
                        distancia[idx] = distancia[nodo_actual] + peso[nodo_actual][i]
                    locks[idx].release()

            lock.acquire()
            if id_proceso[0] < rango[0]:
                id_proceso[0] += 1
                nodo_actual = id_proceso[0]
                if id_proceso[0] >= n_nodos_val - 1:
                    terminar[0] = 1
            lock.release()

        if tid == 0:
            rango[0] *= grado_maximo
            if rango[0] >= n_nodos_val:
                rango[0] = n_nodos_val

        barrier.wait()

    tiempo_final = time.time() - tiempo_inicio
    print(f'TID: {tid}, Tiempo de ejecución: {tiempo_final} segundos')

def main():
    n_nodos = 8
    grado_maximo = 8
    n_procesos = 1
    INT_MAX1 = 1000000000

    P = multiprocessing.Value('i', n_procesos)
    N = multiprocessing.Value('i', n_nodos)
    DEG = multiprocessing.Value('i', grado_maximo)

    rango = multiprocessing.Array('i', range(1))
    terminar = multiprocessing.Array('i', range(1))
    id_proceso = multiprocessing.Array('i', range(n_procesos))
    locks = [multiprocessing.Lock() for _ in range(n_nodos)]

    semilla = 42
    peso, peso_index = grafo(n_nodos, grado_maximo, semilla)
    distancia, cola = inicializar_array(n_nodos, INT_MAX1)

    rango[0] = 1
    terminar[0] = 0

    procesos = [Process(target=realizar_trabajo, args=(i, distancia, cola, N, DEG, P, id_proceso, locks, Lock(), terminar, rango, peso, peso_index)) for i in range(1, n_procesos)]

    for p in procesos:
        p.start()

    realizar_trabajo(0, distancia, cola, N, DEG, P, id_proceso, locks, Lock(), terminar, rango, peso, peso_index)

    for p in procesos:
        p.join()

    mostrar_matriz_adyacencia(peso, grado_maximo, n_nodos)
    mostrar_soluciones(distancia, n_nodos)

if __name__ == "__main__":
    main()
