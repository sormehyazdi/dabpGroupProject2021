"""
File Name: dabp_project_code.py
Author: aliiftik, ppuvvadi, jscanlo2, sormehy
Date: May, 2021
Python version: 3
Purpose: POD site allocation 
    - 1100 blocks
    - 47 possible PODs
    - hours each POD is available = 12
    - people per vehicle = 3
    - each POD can serve 7 cars per hour
"""

import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import os
from numpy import genfromtxt


path = os.getcwd()

def define_parameters():
    ## Setting up problem. Defining parameters
    num_pod_sites = 47
    num_blocks = 1100

    pod_sites = range(num_pod_sites)
    blocks = range(num_blocks)

    hoursOpen = 12
    peoplePerCar = 3
    carsPerHourPerLoading = 6

    #distance = pd.read_csv('Distances.csv', header=None, sep=',')
    distance = genfromtxt(path + '/Distances.csv', delimiter=',') 

    #population = pd.read_csv('Populations.csv', header=None, sep=',')
    population = genfromtxt(path + '/Populations.csv', delimiter=',') 
    #population = population.astype(float)


    #loadingSites = pd.read_csv('LoadingSites.csv', header=None, sep=',')
    loadingSites = genfromtxt(path + '/LoadingSites.csv', delimiter=',') 
    capacity = loadingSites * hoursOpen * peoplePerCar * carsPerHourPerLoading

    #supplies = pd.read_csv('Supplies.csv', header=None, sep=',')
    supplies = genfromtxt(path + '/Supplies.csv', delimiter=',') 

    #labor = pd.read_csv('Labor.csv', header=None, sep=',')
    labor = genfromtxt(path + '/Labor.csv', delimiter=',') 
    cost = labor*12 + (supplies.sum()*loadingSites*hoursOpen*carsPerHourPerLoading)

    budget = [1000000000, 2000000000, 10000000000, 100000000000, 1000000000000]

    return(pod_sites, blocks, distance, population, loadingSites, capacity, supplies, labor, cost, budget)

def find_min_budget(pod_sites, blocks, distance, population, loadingSites, capacity, supplies, labor, cost, budget):
####### MODEL to figure out what the minimum cost would be (assuming we fix the prices)
    m_cost = gp.Model()

    # Decision variables
    x1 = m_cost.addVars(pod_sites, vtype=GRB.CONTINUOUS, lb = 0.0)
    y1 = m_cost.addVars(pod_sites, blocks, vtype=GRB.BINARY)
    #days = m_cost.addVars(GRB.CONTINUOUS, lb = 0.0)
    
    
    
    # Objective function
    m_cost.setObjective(sum(cost[i]*x1[i] for i in pod_sites))
    #m_cost.setObjective(sum(sum(distance[k, i]*population[k]*y1[i,k] for i in pod_sites) for k in blocks))
    
    
    # Constraints
    
    ## all pod sites are bounded by a given capacity
    for i in pod_sites:
        m_cost.addConstr(sum(y1[i, k]*population[k] for k in blocks) <= capacity[i]*x1[i])
     #   m_cost.addConstr(sum(y1[i, k]*population.iloc[k] for k in blocks) <= capacity.iloc[i]*x1[i])
     
    
    ## each block is assigned to exactly 1 pod site
    for k in blocks:
        m_cost.addConstr(sum(y1[i, k] for i in pod_sites) == 1)

        # the total money used is at most the maximum budget
        #m_cost.addConstr(sum(cost[i]*x1[i] for i in pod_sites) <= b)
        #m_cost.addConstr(sum(cost.iloc[i]*x1[i] for i in pod_sites) <= budget)

    m_cost.optimize()
    
    lst = []
    lst_np = np.zeros([len(pod_sites), 1100])

    for i in pod_sites:
        for k in blocks:
            if(x1[i].x >= 0):
                lst_np[i,k] = distance[k,i]*y1[i,k].x
                lst.append(distance[k,i]*y1[i,k].x)
    
    lst_6.append(lst_np)   
    return(m_cost.objVal) 

"""
def min_tot_distance(pod_sites, blocks, distance, population, loadingSites, capacity, supplies, labor, cost, budget):
    try:
        ####### MODEL 1
        m1 = gp.Model()
    
        # Decision variables
        x1 = m1.addVars(pod_sites, vtype=GRB.CONTINUOUS, lb = 0.0)
        y1 = m1.addVars(pod_sites, blocks, vtype=GRB.BINARY)
        #days = m1.addVars(GRB.CONTINUOUS, lb = 0.0)
        
        
        
        # Objective function
        m1.setObjective(sum(sum(distance[k,i]*population[k]*y1[i,k] for i in pod_sites) for k in blocks))
        #m1.setObjective(sum(sum(distance[k, i]*population[k]*y1[i,k] for i in pod_sites) for k in blocks))
        
        
        # Constraints
        
        ## all pod sites are bounded by a given capacity
        for i in pod_sites:
            m1.addConstr(sum(y1[i, k]*population[k] for k in blocks) <= capacity[i]*x1[i])
         #   m1.addConstr(sum(y1[i, k]*population.iloc[k] for k in blocks) <= capacity.iloc[i]*x1[i])
         
        
        ## each block is assigned to exactly 1 pod site
        for k in blocks:
            m1.addConstr(sum(y1[i, k] for i in pod_sites) == 1)
    
            # the total money used is at most the maximum budget
            m1.addConstr(sum(cost[i]*x1[i] for i in pod_sites) <= b)
            #m1.addConstr(sum(cost.iloc[i]*x1[i] for i in pod_sites) <= budget)
    
        m1.optimize()
        
        lst = []
        lst_np = np.zeros([len(pod_sites), 1100])
    
        for i in pod_sites:
            for k in blocks:
                if(x1[i].x >= 0):
                    lst_np[i,k] = distance[k,i]*y1[i,k].x
                    lst.append(distance[k,i]*y1[i,k].x)
        
        lst_6.append(lst_np)
    except AttributeError:
        options.append(b)
        print(b, "was infeasible...moving on...")
        continue
"""
def main():
    (pod_sites, blocks, distance, population, loadingSites, capacity, supplies, labor, cost, budget) = define_parameters()
    #min_tot_distance(pod_sites, blocks, distance, population, 
    #    loadingSites, capacity, supplies, labor, cost, budget)
    print("Set up parameters...")
    petra = find_min_budget(pod_sites, blocks, distance, population, loadingSites, capacity, supplies, labor, cost, budget)
    print("Ran find_min_budget...")
    print("PETRA", petra)

if __name__ == '__main__':
    main()