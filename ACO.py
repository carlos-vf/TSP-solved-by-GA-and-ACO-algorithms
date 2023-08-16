# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 19:56:23 2022

@author: Carlos Velázquez Fernández

Travelling Salesman Problem (TSP)
    with Ant Colony Optimization
    
"""

import time as t
import random
import math


def main(file):
    
    # Locations is an array: [[id0, x0, y0], ..., [idn, xn, yn]]
    locations = readFile(file)
    
    # Ant Colony Optimization
    t0 = t.perf_counter()
    sol = antColonyOptimization(locations)
    t1 = t.perf_counter() - t0
    print('\nAnt Colony Optimization: ' + str(t1) + ' s')
    print(sol)
    
  
    
def readFile(file):
    locations = []
    with open(file, 'r') as file:
        for line in file:
            loc = []
            thisLine = line.split()
            loc.append(thisLine[0])
            loc.append(float(thisLine[1]))
            loc.append(float(thisLine[2].split('\n')[0]))
            locations.append(loc)
    return locations


def antColonyOptimization(locations):
    
    numAnts = 25
    maxIter = 250
    globalBest = [0, 999999]
    
    # Create matrix with distances
    distances = [[0 for i in range(len(locations))] for j in range(len(locations))]
    for i in range(len(locations)):
        for j in range(len(locations)):
            distances[i][j] = distance(locations[i], locations[j])
    
    # Create eta matrix
    eta = [[0 for i in range(len(locations))] for j in range(len(locations))]
    for i in range(len(locations)):
        for j in range(len(locations)):
            if (distances[i][j] > 0):
             eta[i][j] = 1 / distances[i][j]
    
    # Create pheromone matrix
    pheromone = [[0 for i in range(len(locations))] for j in range(len(locations))]
    for i in range(len(locations)):
        for j in range(len(locations)):
            if (i != j):
             pheromone[i][j] = 10
    
    # Lists
    cost = [0 for i in range(numAnts)]
    
    
    for iteration in range(maxIter):
        
        print('Iter: ' + str(iteration))
        visitedNodes = [[0 for i in range(len(locations))] for j in range(numAnts)]
        # Initialize the ants (every ant has visited city '1')
        initialNode = locations[0]
        for k in range(numAnts):
            visitedNodes[k][0] = initialNode[0]
            
        # Build the solutions
        for i in range(1, len(locations)):
            for k in range(numAnts):
                visitedNodes[k][i] = transitionRule(visitedNodes[k], pheromone, eta)
        for k in range(numAnts):
            visitedNodes[k].append(initialNode[0])
        
        # Calculate the total cost of the ants and the best ant
        for k in range(numAnts):
            cost[k] = C(visitedNodes[k], distances)
        actualBest = best(cost)
        
        # Update the pheromone
        for i in range(len(locations)):
            for j in range(len(locations)):
                pheromoneUpdate(pheromone, i, j, visitedNodes, cost)
        
                
        if (actualBest[1] < globalBest[1]):
            globalBest = actualBest
            solution = visitedNodes[globalBest[0]]
            if(globalBest[1] < 9000):
                break
        print('Global best:' + str(globalBest[1]))
    
    return [solution, globalBest[1]]
    
    
        
def distance(location1, location2):
    
    x1 = location1[1]
    x2 = location2[1]
    y1 = location1[2]
    y2 = location2[2]
    
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    
    return distance
    
   
# Returns the id of a location following the probabilistic rule    
def transitionRule(visitedNodesAnt, pheromone, eta):
    probabilities = [0 for i in range(len(pheromone[0]))]
    alpha = 1
    beta = 5
    
    # Last node visited
    lastNodeVisited = visitedNodesAnt[0]
    for i in range(len(visitedNodesAnt)):
        if (visitedNodesAnt[i] != 0):
            lastNodeVisited = visitedNodesAnt[i]
        else:
            break
    
    # Equation (down)
    down = 0
    for i in range(len(pheromone[0])):
        if (hasBeenVisited(str(i+1), visitedNodesAnt) == False):
            tauRS = pheromone[int(lastNodeVisited) - 1][i]**alpha
            etaRS = eta[int(lastNodeVisited) - 1][i]**beta
            down += tauRS * etaRS
        
    # Equation (up and result)
    for i in range(len(pheromone[0])):
        if (hasBeenVisited(str(i+1), visitedNodesAnt) == False):
            tauRS = pheromone[int(lastNodeVisited) - 1][i]**alpha
            etaRS = eta[int(lastNodeVisited) - 1][i]**beta
            up = tauRS * etaRS
            probabilities[i] = (up / down) * 100
 
    ids = [str(i) for i in range(1, len(visitedNodesAnt) + 1)]
    random.seed(a=None, version=2)
    chosenLocationId = random.choices(ids, weights=probabilities, k = 1)
    return chosenLocationId[0]    
    

# Returns the total cost of the path    
def C(visitedNodesAnt, distances):
    cost = 0
    for i in range(len(visitedNodesAnt) - 1):
        node1 = visitedNodesAnt[i]
        node2 = visitedNodesAnt[i+1]
        cost += distances[int(node1) - 1][int(node2) - 1]
    return cost    


def pheromoneUpdate(pheromone, i, j, visitedNodes, cost):
    summatory = 0
    p = random.random()

    for l in range(len(cost)):
        summatory += 1 / cost[l]
    pheromone[i][j] = (1 - p) * pheromone[i][j] + summatory
    
    return 0    


# Returns the pos and cost of the best ant
def best(cost):
    pos = 0
    minimum = 999999
    for i in range(len(cost)):
        if (cost[i] < minimum):
            minimum = cost[i]
            pos = i
    return [pos, minimum]


def hasBeenVisited(idNode, visitedNodesAnt):
    for i in range(len(visitedNodesAnt)):
        node = visitedNodesAnt[i]
        if (node != 0 and idNode == node):
            return True    
    return False


main("test_file.txt")    