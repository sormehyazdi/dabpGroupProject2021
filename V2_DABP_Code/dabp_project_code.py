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

## Import required packages
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import os
from numpy import genfromtxt

## Global variable
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

    return(pod_sites, blocks, distance, population, loadingSites, capacity, supplies, labor, cost)

def min_tot_distance(pod_sites, blocks, distance, population, loadingSites, capacity, supplies, labor, cost, budget, opening_cost):
    ####### MODEL 1
    m1 = gp.Model()

    ### Decision variables
    ## number of days POD is open for
    x1 = m1.addVars(pod_sites, vtype=GRB.CONTINUOUS, lb = 0.0)
    ## whether or not a block is assigned to a POD
    y1 = m1.addVars(pod_sites, blocks, vtype=GRB.BINARY)
    ## whether or not a POD is open
    z1 = m1.addVars(pod_sites, vtype=GRB.BINARY)

    ### Objective function
    ## want to minimize the total/weighted travel distance of Allegheny's population
    m1.setObjective(sum(sum(distance[k,i]*population[k]*y1[i,k] for i in pod_sites) for k in blocks))
    
    ### Constraints
    ## all pod sites are bounded by a given capacity
    for i in pod_sites:
        m1.addConstr(sum(y1[i, k]*population[k] for k in blocks) <= capacity[i]*x1[i])
        m1.addConstr(z1[i]*bob >= x1[i])
        m1.addConstr(x1[i] <= 30)
     
    ## each block is assigned to exactly 1 pod site
    for k in blocks:
        m1.addConstr(sum(y1[i, k] for i in pod_sites) == 1)

        # the total money used is at most the maximum budget
        m1.addConstr(sum(cost[i]*x1[i] + z1[i]*opening_cost for i in pod_sites) <= budget)

    ## Solve
    m1.optimize()

    lst = []
    lst_np = np.zeros([len(pod_sites), 1100])

    for i in pod_sites:
        for k in blocks:
            if(x1[i].x >= 0):
                lst_np[i,k] = distance[k,i]*y1[i,k].x
                lst.append(distance[k,i]*y1[i,k].x)
    
    # Print optimized solution
    print(m1.objVal)

    return(m1.objVal, lst) 

def run_scenario_one():
    ## Global epidemic in Allegheny county

    ## Setting up some parameters that will be looped through the main function
    opening_cost = [5000, 10000, 25000, 50000, 75000, 100000]
    budget = [100000, 250000, 500000, 1000000, 1500000, 2000000]
    bob = 1000000000000 ## This is our big M

    ## Define Parameters
    (pod_sites, blocks, distance, population, loadingSites, capacity, supplies, labor, cost) = define_parameters()
    print("Set up parameters...")

    scn1_model1_optimal_vals = []


    ## Loop through budget values to 
    for b in budget:
        try:
            for op_co in opening_cost:
                (m1_opt_solution, lst) = min_tot_distance(pod_sites, blocks, distance, 
                    population, loadingSites, capacity, supplies, labor, cost, b, op_co)
            scn1_model1_optimal_vals.append(m1_opt_solution)

        except AttributeError:
            options.append(b)
            print("Budget", b, "with opening cost", op_co, "was infeasible...moving on...")
            continue

    return(scn1_model1_optimal_vals)

def main():
    optimal_vals_1 = run_scenario_one()
    print(optimal_vals_1)
    

if __name__ == '__main__':
    main()