# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 13:48:25 2022

@author: Carlos Velázquez Fernández

Travelling Salesman Problem (TSP)
    with Genetic Algorithms
    
"""

import time as t
import random
import math


def main(file):
    
    # Locations is an array: [[id0, x0, y0], ..., [idn, xn, yn]]
    locations = readFile(file)
    
    # Genetic Algorithm
    t0 = t.perf_counter()
    sol = geneticAlgorithm(locations)
    t1 = t.perf_counter() - t0
    print('\nGenetic Algorithm time: ' + str(t1) + ' s')
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
            
            
def geneticAlgorithm(locations):
    
    # Initialize population
    population = []
    numOfLocations = len(locations)
    numOfFitnessEval = 0
    bestScore = 999999
    
    for i in range (50):
        chromosome = [locations[j] for j in range(1, numOfLocations)]
        random.shuffle(chromosome)
        chromosome.insert(0, locations[0])
        chromosome.append(locations[0])
        population.append(chromosome)
    
    # Calculate fitness of each individual
    scores = []
    for i in range (len(population)):
        scores.append(fitness(population[i]))
        numOfFitnessEval += 1
    
    while (1):
        
        # Select parents
        parents = selectParents(population, scores)
        bestScore = fitness(parents[0])
        numOfFitnessEval += 2
        print('Fitness Evaluations: ' + str(numOfFitnessEval))
        print('Best Distance: ' + str(bestScore))
        
        # It returns here
        if (numOfFitnessEval >= 250000 or bestScore <= 9000):
            return [parents[0], bestScore]
        
        # Crossover
        crossoverResults = crossover(parents)
        
        # Mutation
        mutatedChild1 = mutation(crossoverResults[0])
        mutatedChild2 = mutation(crossoverResults[1])
        
        # Replacement
        posWorst = worstInPopulation(population, scores)
        population[posWorst[0]] = mutatedChild1
        population[posWorst[1]] = mutatedChild2
        scores[posWorst[0]] = fitness(mutatedChild1)
        scores[posWorst[1]] = fitness(mutatedChild2)
    
    
    
def distance(location1, location2):
    x1 = location1[1]
    x2 = location2[1]
    y1 = location1[2]
    y2 = location2[2]
    
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    
    return distance


# Returns the total distance
def fitness(solution):
    totalDistance = 0
    for i in range (len(solution) - 1):
        totalDistance += distance(solution[i], solution[i+1])
    return totalDistance


# Returns the two best individuals
def selectParents(population, scores):
    minDistance1 = 999999
    minDistance2 = 999999
    pos1 = 1
    pos2 = 1
    for i in range(len(scores)):
        if (scores[i] < minDistance1):
            minDistance1 = scores[i]
            pos1 = i
    for i in range(len(scores)):
        if (scores[i] < minDistance2 and scores[i] > minDistance1):
            minDistance2 = scores[i]
            pos2 = i
            
    return (population[pos1], population[pos2])


def crossover(parents):
    
    child1 = generateChild(parents[0], parents[1])
    child2 = generateChild(parents[1], parents[0])
    
    return [child1, child2]
    


def generateChild(parent1, parent2):
    
    numOfLocations = len(parent1) - 1
    
    # Generate random positions and number of cities to copy from the first parent
    posOfCities = random.randrange(1, numOfLocations - 1, 1)
    numOfCities = random.randrange(1, min(numOfLocations - posOfCities, 7), 1)
    
    child = [0 for i in range (numOfLocations)]
    child[0] = parent1[0]
    child.append(parent1[0])
    
    # Copy the cities from the first parent
    for i in range (posOfCities, posOfCities + numOfCities):
        child[i] = parent1[i]
    
    # Copy the cities from the second parent
    for i in range (1, numOfLocations):
        if (parent2[i] not in child):
            for j in range (1, numOfLocations):
                if (child[j] == 0):
                    child[j] = parent2[i]
                    break
    
    return child
 

def mutation(genome):
    
    numOfElements = len(genome) - 1
    
    randomPos1 =  random.randrange(1, numOfElements - 1, 1)
    randomPos2 =  random.randrange(1, numOfElements - 1, 1)
    
    element = genome[randomPos1:randomPos2+1]
    element.reverse()
    genome[randomPos1:randomPos2+1] = element
    
    
    return genome


def worstInPopulation(locations, scores):
    maxDistance1 = 0
    maxDistance2 = 0
    pos1 = 1
    pos2 = 1
    for i in range(len(scores)):
        if (scores[i] > maxDistance1):
            maxDistance1 = scores[i]
            pos1 = i
    for i in range(len(scores)):
        if (scores[i] > maxDistance2 and scores[i] < maxDistance1):
            maxDistance2 = scores[i]
            pos2 = i
    return [pos1, pos2]



     

main("test_file.txt")