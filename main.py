# coding=UTF-8
import random

"""
Convert .txt file containing graph matrix into integer nested arrays
Params :
    file : path to the file containing the matrix
"""
def import_matrix(file_path):
    graph = []
    with open(file_path, 'r') as matrix_file:
        node = 0
        for line in matrix_file.read().split('\n'):
            graph.append([])
            for value in line.split(' '):
                if value == '0' or value == '1':
                    graph[node].append(int(value))
            node += 1
    return graph


"""
Generate a random graph matrix
Params : 
    nbNodes : How many nodes the graph will have
    probability : How much chances from 0 to 100 two nodes will be related 
"""
def generate_graph(nbNodes, probability):
    graph = []
    for line in range(nbNodes):
        graph.append([0] * nbNodes)
    for line in range(0, nbNodes):
        for column in range(line, nbNodes):
            rand = random.random()
            if rand <= (probability / 100) and line != column:
                graph[line][column] = 1
                graph[column][line] = 1
            else:
                graph[line][column] = 0
                graph[column][line] = 0
    return graph


def is_related(graph):
    nbNodes = len(graph)
    markers = [0 for node in range(nbNodes)]
    markers[0] = 1
    spy = 1
    while spy == 1:
        spy = 0
        for line in range(nbNodes):
            if markers[line] == 1:
                for column in range(line, nbNodes):
                    if markers[column] == 0 and graph[line][column] == 1:
                        markers[column] = 1
                        spy = 1
    if 0 in markers:
        return False
    else:
        return True


"""
Verify if a chain is in graph
Params :
    graph : analysed graph
    chain : the chain to check
"""
def chain_in_graph(graph, chain):
    for node in range(0, len(chain) - 1):
        if graph[chain[node]][chain[node + 1]] == 0:
            return False
    return True


"""
Returns an elementary chain
Params : 
    chain : the chain to simplify
"""
def elementary_chain(chain):
    for start in range(0, len(chain) - 1):
        for end in range(len(chain) - 1, start, -1):
            if chain[end] == chain[start] and start < end:
                chain = chain[0:start] + chain[end:len(chain)]
    return chain


if __name__ == '__main__':
    # Sequences 1 et 2
    print("Ce programme permet de générer un graphe aléatoire, puis de saisir une chaîne.")
    print("Si cette chaîne appartient au graphe, elle est ensuite transformée en chaîne élémentaire.")
    nbNodes = int(input("Combien de noeuds ?"))
    probability = -1
    while probability < 0 or probability > 100:
        probability = float(input("Pourcentage de probabilités d'avoir une arête entre deux noeuds ? %"))
    print("Matrice d'adjacence du graphe généré : ")
    graph = generate_graph(nbNodes, probability)
    for i in range(nbNodes):
        print(graph[i])
    chain = []
    print("Saisie de la chaine, entrez -1 quand la saisie est terminée.")
    chainNode = int(input("Noeud : "))
    while chainNode != -1:
        if 0 <= chainNode < len(graph):
            chain.append(chainNode)
        else:
            print("Le noeud saisi n'appartient pas au graphe.")
        chainNode = int(input("Noeud : "))
    print("Chaine saisie : ")
    print(chain)
    if chain_in_graph(graph, chain):
        print("La chaine saisie appartient bien au graphe.")
        print("Chaine elementaire : ")
        chain = elementary_chain(chain)
        print(chain)
    else:
        print("La chaine saisie n'appartient pas au graphe.")
    graph = import_matrix('AdjacencyMatrixSamples/Graphe100.txt')
    for i in range(len(graph)):
        print(graph[i])
    print(is_related(graph))
