# -*- coding: utf-8 -*-
"""
Created on Mon May  1 10:05:03 2017
@author: Johnson, Brian, and Brendan
"""

import numpy as np
import numpy.linalg as la
import random as randy
import math
    
#pop = []
#stats = []
#
#for x in range(lpop):
#    pop.append(0)
#    stats.append(0) 
#pop = np.array([pop])
#stats = np.array([stats])
# popSize: Total population size
# initInfect: How many to infect to start with
def initRandyInfect(popSize, initInfect):
    # Total population size
    # Array of the population: 3 values for each individual: infection number, immunity number, status (susceptible, infected, infectious, symptomatic, immune)
    pop = np.zeros((popSize, 3))
    # Set initial immunity
    for x in range(popSize):
        pop[x][1] = np.random.normal(2.5,.15)
    # Go through and place each infected member
    for x in range(initInfect):
        # Random integer in [0,lpop]
        infect = math.floor(popSize*randy.random())
        # Make sure this member isn't already infected. Else get a new random number
        while (pop[infect][0] != 0):
            infect = math.floor(popSize*randy.random())
        # Add to the infection level
        pop[infect][0] += 10/pop[infect][1]
        # Set the status to infected
        pop[infect][2] = 1
    #Return the new infected population
    return pop

# Simulate 1 day
def oneDay(pop, QuarEff):
    # Go through each individual
    for x in range(int(pop.size/3)):
        # Infectious and Symptomatic individual
        if (pop[x][2] == 2 or pop[x][2] == 3):
            if(pop[x][2] == 3):
                Randy = randy.uniform(0,1)
                if (Randy <= QuarEff):
                    pop[x][2] = 5
            # Increase immunity
            if (pop[x][1] <= 12):
                pop[x][1] += 2
            # Add to their own infection
            pop[x][0] *= 10/pop[x][1]
            # Change to symptomatic when reaches 15 infection level
            if pop[x][0] >= 15:
                pop[x][2] = 3
            # Change to immune if drop back below 10
            if pop[x][0] <= 10:
                pop[x][2] = 4
            # Infect others. Number of people on each side is Poisson distributed: rate param 4
            numInf = np.random.poisson(4)
            # Go through each person to be possibly infected.
            for i in range(2*numInf):
                # Possible new infected person
                j = x - numInf + i
                #Wrap around if j is negative or past the array
                if(j < 0):
                    j += int(pop.size/3)
                elif(j >= pop.size/3):
                    j -= int(pop.size/3)
                # Don't want to infect the person who is infecting, and can't infect already infected persons.
                if (i != numInf and pop[j][2] == 0):
                    # Calc contact times in contact using Exp. distribution
                    time = np.random.exponential(1)
                    # Infcetion level depends on infection of infectious individual, length of contact
                    infection = pop[x][0]*time/10
                    # Only infect if the infection count is greater than 1
                    if (infection > 1):
                        # Add infection to the individual
                        pop[j][0] += infection
                        # Set status to infected
                        pop[j][2] = 1   
        # Infected individual
        elif (pop[x][2] == 1):
            # Increase immunity
            pop[x][1] += 2
            # Infection increase amount
            infection = 10/pop[x][1]
            # If infection will decrease, move to immune
            if (infection <= 1):
                pop[x][2] = 4
            # Else increase infection
            else:
                pop[x][0] *= infection
            # Change to infectious if reach 10
            if pop[x][0] >= 10:
                pop[x][2] = 2
        # Immune or Susceptible individual
        elif (pop[x][2] == 0 or pop[x][2] == 4 or pop[x][2] == 5):
            #Do nothing?
            y = 0
    return pop

# Calculate how many are in each group
def popDist(pop):
    Sus = 0
    Inf = 0
    Info = 0
    Sym = 0
    Imm = 0
    Quar = 0
    for x in range(int(pop.size/3)):
        if (pop[x][2] == 0):
            Sus += 1
        elif (pop[x][2] == 1):
            Inf += 1
        elif (pop[x][2] == 2):
            Info += 1
        elif (pop[x][2] == 3):
            Sym += 1
        elif (pop[x][2] == 4):
            Imm += 1
        elif (pop[x][2] == 5):
            Quar += 1
    return (Sus, Inf, Info, Sym, Imm, Quar)

# Simulate a number of days
def simDaysVerbose(pop,days, QuarEff):
    for i in range(days):
        pop = oneDay(pop, QuarEff)
        print(pop, popDist(pop), '\n')

def simDays(pop,days, QuarEff):
    for i in range(days):
        pop = oneDay(pop, QuarEff)
        
# Start a pop and simulate until no longer  have infected
def simInfectionGoneVerbose(popSize, inInfect, QuarEff):
    pop = initRandyInfect(popSize, inInfect)
    Dist = popDist(pop) 
    Days = 0
    while (Dist[1] != 0 or Dist[2] != 0 or Dist[3] != 0):
        print ('Day', Days)
        Dist = popDist(pop)
        simDays(pop,1, QuarEff)
        Days += 1
    print('\n', pop, Dist, Days, 'Days')
    
def simInfectionGone(popSize, inInfect, QuarEff):
    pop = initRandyInfect(popSize, inInfect)
    Dist = popDist(pop) 
    Days = 0
    while (Dist[1] != 0 or Dist[2] != 0 or Dist[3] != 0):
        Dist = popDist(pop)
        simDays(pop,1, QuarEff)
        Days += 1
    return(Dist, Days)
def ManyInfections(popSize,inInfect, n, QuarEff):
    sumDays = 0
    sumSus = 0
    sumImm = 0
    sumQuar = 0
    for i in range(0,n):
        (Dist, Days) = simInfectionGone(popSize, inInfect, QuarEff)
        sumDays += Days
        sumSus += Dist[0]
        sumImm += Dist[4]
        sumQuar += Dist[5]
    return ("Average Days for Infection to Die:",sumDays/n,"Average Susceptible:",sumSus/n,"Average Immune:",sumImm/n, "Average Quarantined:", sumQuar/n)

def QuarEffRange(popSize,inInfect,n):
    for i in range(0,11):
        print("\nQuarantine efficiency:", i/10)
        print(ManyInfections(popSize,inInfect,n,i/10))
        
QuarEffRange(500,15,100)