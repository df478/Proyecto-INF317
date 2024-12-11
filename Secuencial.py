import random
import time

INFINITO = float('inf')
NUM_NODOS = 8
SEED = 42 


def generar_grafo(num_nodos):
    random.seed(SEED) 
    grafo = [[0 if i == j else random.randint(1, 10) for j in range(num_nodos)] for i in range(num_nodos)]
    return grafo


def inicializar_arreglos(num_nodos):
    distancias = [INFINITO] * num_nodos
    visitados = [False] * num_nodos
    distancias[0] = 0 
    return distancias, visitados


def dijkstra(grafo, distancias, visitados):
    num_nodos = len(grafo)

    for _ in range(num_nodos):
        min_distancia = INFINITO
        nodo_actual = -1

        for nodo in range(num_nodos):
            if not visitados[nodo] and distancias[nodo] < min_distancia:
                min_distancia = distancias[nodo]
                nodo_actual = nodo

        if nodo_actual == -1:
            break 

        visitados[nodo_actual] = True

        for vecino in range(num_nodos):
            if grafo[nodo_actual][vecino] > 0 and not visitados[vecino]:
                nueva_distancia = distancias[nodo_actual] + grafo[nodo_actual][vecino]
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia


def imprimir_matriz_adyacencia(grafo):
    num_nodos = len(grafo)
    nodos = [chr(65 + i) for i in range(num_nodos)]

    print("   " + " ".join(f"{nodo:3}" for nodo in nodos))
    for i, fila in enumerate(grafo):
        print(f"{nodos[i]:3}" + " ".join(f"{peso if peso != INFINITO else '∞':3}" for peso in fila))


def imprimir_solucion(distancias, nodo_inicial):
    print(f"\nDistancias mínimas desde el nodo inicial ({chr(65 + nodo_inicial)}):")
    for i, distancia in enumerate(distancias):
        print(f"Distancia al nodo {chr(65 + i)}: {distancia if distancia != INFINITO else '∞'}")


def main():
    grafo = generar_grafo(NUM_NODOS)
    distancias, visitados = inicializar_arreglos(NUM_NODOS)
    nodo_inicial = 0

    print("Matriz de adyacencia del grafo:")
    imprimir_matriz_adyacencia(grafo)

    tiempo_inicio = time.time()
    dijkstra(grafo, distancias, visitados)

    imprimir_solucion(distancias, nodo_inicial)
    print(f"\nTiempo de ejecución: {time.time()- tiempo_inicio} segundos")


if __name__ == "__main__":
    main()
