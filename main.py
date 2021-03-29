#!/usr/bin/python
# -*- coding: UTF-8 -*-
import copy
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


"""
Verify if the given graph is related using a boolean
"""


def is_related_with_boolean(graph):
    nb_nodes = len(graph)
    markers = [0 for node in range(nb_nodes)]
    markers[0] = 1
    has_marked = 1
    while has_marked == 1:
        has_marked = 0
        for line in range(nb_nodes):
            if markers[line] == 1:
                for column in range(line, nb_nodes):
                    if markers[column] == 0 and graph[line][column] == 1:
                        markers[column] = 1
                        has_marked = 1
    if 0 in markers:
        return False
    else:
        return True


"""
Verify if the given graph is related using a boolean
"""


def is_related_with_array(graph):
    to_treat = [0]
    already_treated = []
    while len(to_treat) != 0:
        treated_node = to_treat.pop()
        for other_node in range(0, len(graph)):
            if other_node not in to_treat and other_node not in already_treated \
                    and graph[treated_node][other_node] != 0:
                to_treat.append(other_node)
            already_treated.append(treated_node)
    return len(graph) == len(already_treated)


"""
Returns the isthmus list from the graph
"""


def isthmus_list(graph):
    isthmus_list = []
    for node_x in range(0, len(graph)):
        for node_y in range(0, len(graph)):
            if is_an_isthmus(graph, node_x, node_y):
                isthmus_list.append([node_x, node_y])
    return isthmus_list


"""
Check if the given nodes relationship is an isthmus inside the graph
"""


def is_an_isthmus(graph, nodeX, nodeY):
    if graph[nodeX][nodeY] == 1:
        copy_graph = copy.deepcopy(graph)
        copy_graph[nodeX][nodeY] = 0
        copy_graph[nodeY][nodeX] = 0
        x_graph = [nodeX]
        get_related_nodes(copy_graph, nodeX, x_graph)
        y_graph = [nodeY]
        get_related_nodes(copy_graph, nodeY, y_graph)
        for node in range(len(x_graph)):
            if x_graph[node] in y_graph:
                return False
        return True
    return False


"""
Recursive algorithm to obtain all the nodes attached to the starting node
"""


def get_related_nodes(graph, starting_node, related_nodes):
    for otherNode in range(0, len(graph[starting_node])):
        if graph[starting_node][otherNode] == 1 and otherNode not in related_nodes:
            related_nodes.append(otherNode)
            get_related_nodes(graph, starting_node, related_nodes)


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


"""
Simply prints graph adjacency matrix
"""


def print_graph_matrix(graph):
    for i in range(len(graph)):
        print(graph[i])


###########################################################################################
#                                    SEQUENCES DU COURS                                   #
###########################################################################################

"""
Sequences 1 and 2
"""


def prompt_for_graph():
    # Sequences 1 et 2
    print("Ce programme permet de générer un graphe aléatoire, puis de saisir une chaîne.")
    print("Si cette chaîne appartient au graphe, elle est ensuite transformée en chaîne élémentaire.")
    nbNodes = int(input("Combien de noeuds ?"))
    probability = -1
    while probability < 0 or probability > 100:
        probability = float(input("Pourcentage de probabilités d'avoir une arête entre deux noeuds ? %"))
    print("Matrice d'adjacence du graphe généré : ")
    graph = generate_graph(nbNodes, probability)
    print_graph_matrix(graph)
    return graph


"""
Chains sequence
"""


def prompt_for_chain():
    chain = []
    print("Saisie de la chaine, entrez -1 quand la saisie est terminée.")
    chain_node = int(input("Noeud : "))
    while chain_node != -1:
        if 0 <= chain_node < len(graph):
            chain.append(chain_node)
        else:
            print("Le noeud saisi n'appartient pas au graphe.")
        chain_node = int(input("Noeud : "))
    print("Chaine saisie : ")
    print(chain)
    return chain


def reduce_chain_if_in_graph(graph,chain):
    if chain_in_graph(graph, chain):
        print("La chaine saisie appartient bien au graphe.")
        print("Chaine elementaire : ")
        chain = elementary_chain(chain)
        print(chain)
    else:
        print("La chaine saisie n'appartient pas au graphe.")


if __name__ == '__main__':
    # Isthmus sequence
    print("Dessin du graphe en entrée")
    print("E          B\n"
          "| \\      / |\n"
          "|   A---D  |\n"
          "| /      \\ |\n"
          "F          C")
    graph = import_matrix('AdjacencyMatrixSamples/Graphe1Isthme.txt')
    print('Matrice d\'adjacence correspondante')
    print_graph_matrix(graph)
    print('Vérification de la fonction is_an_isthmus pour l\'arête A,D')
    print(is_an_isthmus(graph, 0, 3))
    print('Liste des isthmes')
    print(isthmus_list(graph))

    # Older sequences
    # graph = prompt_for_graph()
    # chain = prompt_for_chain()
    # reduce_chain_if_in_graph(graph,chain)

