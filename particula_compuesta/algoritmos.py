import math
from collections import deque
from queue import PriorityQueue
from pprint import pformat

infinito = 1000000

def distancia_euclidiana(x_1, y_1, x_2, y_2):
    en_x = math.pow(x_1 - x_2, 2)
    en_y = math.pow(y_1 - y_2, 2)
    distancia = math.sqrt(en_x + en_y)
    return distancia

def amplitud(origen, grafo):
    visitados = []
    cola = deque()
    resultado = []
    adyacentes = []

    visitados.append(origen)
    cola.append(origen)

    while len(cola) > 0:
        vertice = cola[0]
        resultado.append(vertice)
        cola.popleft()
        adyacentes = grafo.get(vertice)

        
        for i in range(len(adyacentes)):
            ady = adyacentes[i][0]

            if ady not in visitados:
                visitados.append(ady)
                cola.append(ady)
    return resultado

def profundidad(origen, grafo):
    visitados = []
    pila = deque()
    resultado = []

    visitados.append(origen)
    pila.append(origen)

    while len(pila) > 0:
        vertice = pila[-1]
        resultado.append(vertice)
        pila.pop()
        adyacentes = grafo.get(vertice)
        
        for i in range(len(adyacentes)):
            ady = adyacentes[i][0]

            if ady not in visitados:
                visitados.append(ady)
                pila.append(ady)
    
    return resultado

def imprimirprio(cola):
    copia = PriorityQueue()
    while not cola.empty():
        arista = cola.get()
        print(arista)
        copia.put(arista)
    cola = copia

def inCola(cola, nodo):
    copia = PriorityQueue()

    while not cola.empty():
        n = cola.get()
        copia.put(n)
    cola = copia
    
    while not copia.empty():
        n = copia.get()
        if nodo == n:
            return False
        
    return True

def algoritmoPrim(grafo, origen):
    visitados = [] #lista de (1, 2)
    colaPrioridad = PriorityQueue()
    grafoRes = dict()

    adyacentes = grafo.get(origen)
    for nodo in adyacentes:
        destino = nodo[1]
        arista = (nodo[0], (origen, destino))
        colaPrioridad.put(arista) #(peso, (o_x, o_y), (d_x, d_y))

    #colaPrioridad.put(grafo.get(origen))
    visitados.append(origen)
    
    while not colaPrioridad.empty():
        aristaMin = colaPrioridad.get() #(peso, (o_x, o_y), (d_x, d_y))
        destino = aristaMin[1][1]  #tupla
        # print(aristaMin)
        # print(destino)#colaVisitados.put(aristaMin) #los que salen

        if destino not in visitados: 
            visitados.append(destino)
            adyacentes = grafo.get(destino)
            for nodo in adyacentes: #iterando a los adyacentes
                destino2 = nodo[1] #se vuelve el destino 
                arista = (nodo[0], (destino, destino2)) #el destino anterior se vuelve el origen
                # print("v", visitados)
                # print("d2", destino2)
                if destino2 not in visitados:
                    colaPrioridad.put(arista)
            #colaPrioridad.put(grafo.get(destino)) #adyacentes
#o                  d
#(200, 10)----------(250, 10)
            origen1 = aristaMin[1][0]
            destino1 = aristaMin[1][1]

            arista_o_d = (aristaMin[0], destino1) #peso, destino
            arista_d_o = (aristaMin[0], origen1) #peso, origen

            if origen1 in grafoRes:
                grafoRes[origen1].append(arista_o_d)
            else:
                grafoRes[origen1] = [arista_o_d]
            if destino1 in grafoRes:
                grafoRes[destino1].append(arista_d_o)
            else:
                grafoRes[destino1] = [arista_d_o]

    return grafoRes

def makeSet(origen, destino, disjointSet):
    l = []

    for lista in reversed(disjointSet):
        if destino in lista:
            l = lista
    for lista in disjointSet:
        if origen in lista:
            l1 = lista + l
            #print("1", l1)
            r = []
            lista.clear()
            for e in l1:
                if e not in r:
                    lista.append(e)
                    r.append(e)
            
            
            if l in disjointSet:
                disjointSet.remove(l)
            

        if [destino] == lista:
            disjointSet.remove([destino])
        
        
def findSet(vertice, disjointSet):
    for i in range(len(disjointSet)):
        if vertice in disjointSet[i]:
            return disjointSet[i]
    return []

def algoritmoKruskal(grafo):
    grafoRes = dict()
    listaOrdenada = PriorityQueue()
    disjointSet = []

    visitados = []

    for origen in grafo: #(x, y) origen -- keys
        ady = grafo.get(origen)
        disjointSet.append([origen])

        for nodo in ady: #(peso, (destino)) -- values
            destino = nodo[1]
            arista = (nodo[0] * -1, (origen, destino))
            
            if (origen, destino) not in visitados and (destino, origen) not in visitados:
                listaOrdenada.put(arista)
                visitados.append((origen, destino))
    
    while not listaOrdenada.empty():
        arista = listaOrdenada.get()
        origen = arista[1][0]
        destino = arista[1][1]
        print("arista: ", arista)
        print(disjointSet)

        if findSet(origen, disjointSet) != findSet(destino, disjointSet):
            
            peso = arista[0]

            arista_o_d = (peso, destino)
            arista_d_o = (peso, origen)

            if origen in grafoRes:
                grafoRes[origen].append(arista_o_d)
            else:
                grafoRes[origen] = [arista_o_d]
            
            if destino in grafoRes:
                grafoRes[destino].append(arista_d_o)
            else:
                grafoRes[destino] = [arista_d_o]

            makeSet(origen, destino, disjointSet)
    
    return grafoRes

def algoritmoDijkstra(grafo, origen):
    distancias = dict()
    
    listaOrdenada = PriorityQueue()

    for nodo in grafo: #key
        if nodo == origen:
            distancias[nodo] = 0
            listaOrdenada.put((0, nodo))
        else:
            distancias[nodo] = infinito
        #print(distancias)

    camino = dict()

    while not listaOrdenada.empty():
        nodo = listaOrdenada.get() #(peso, (vertice))

        ady_nodo = grafo.get(nodo[1]) #values

        for arista in ady_nodo: 
            destino = arista[1]
            peso = arista[0]

            dist = peso + nodo[0] 
            #print(dist, distancias.get(destino), destino)

            d2 = distancias.get(destino)

            if dist < d2:
                distancias[destino] = dist
                camino[destino] = nodo[1]
                listaOrdenada.put((dist, destino))
                
    s = pformat(distancias, indent = 4, width = 40)
    print(s)
    return camino

            