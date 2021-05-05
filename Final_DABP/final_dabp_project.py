"""
File Name: final_dabp_project.py
Authors: aliiftik, ppuvvadi, jscanlo2, sormehy
Date: May, 2021
Python version: 3
Purpose: POD site allocation 
    - 1100 blocks
    - 47 possible PODs
    - hours each POD is available = 12
    - people per vehicle = 3
    - each POD can serve 7 cars per hour
    - 2 different scenarios: Allegheny county rescue PODs - Pittsburgh city rescue PODs
    - 2 different models for each scenario: weighted total distance - minimize max distance for any one group
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
    max_days_open = 30

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
    cost = labor*12 #+ (supplies.sum()*loadingSites*hoursOpen*carsPerHourPerLoading)

    return(pod_sites, blocks, distance, population, loadingSites, capacity, supplies, labor, cost, max_days_open)

def min_tot_distance(pod_sites, blocks, distance, population, loadingSites, capacity, supplies, labor, cost, budget, opening_cost, bigM, max_days_open):
    ####### MODEL 1 - Minimize total distance traveled by the entire population
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
    m1.modelSense = GRB.MINIMIZE
    
    ### Constraints
    ## all pod sites are bounded by a given capacity
    for i in pod_sites:
        #m1.addConstr(sum(y1[i, k]*population[k] for k in blocks) <= capacity[i]*x1[i])
        m1.addConstr(sum(y1[i, k]*population[k] for k in blocks) == capacity[i]*x1[i])
        m1.addConstr(z1[i]*bigM >= x1[i])
        m1.addConstr(x1[i] <= max_days_open)
     
    ## each block is assigned to exactly 1 pod site
    for k in blocks:
        m1.addConstr(sum(y1[i, k] for i in pod_sites) == 1)

        # the total money used is at most the maximum budget
        m1.addConstr(sum(cost[i]*x1[i] + z1[i]*opening_cost for i in pod_sites) <= budget)

    ## Solve
    m1.optimize()

    lst = []
    lst_np = np.zeros([len(pod_sites), 1100])
    pod_days = []
    block_dist = []
    #long_ls_vals = []

    for i in pod_sites:
        for k in blocks:
            #if(x1[i].x >= 0): ## this will still print out all of them since weakly greater than 0.
            if(x1[i].x > 0):
                lst_np[i,k] = distance[k,i]*y1[i,k].x
                lst.append((budget, opening_cost, i, k, distance[k,i]*y1[i,k].x))

                #long_ls_vals.append((budget, opening_cost, m1.objVal, i, x1[i].x, k, distance[k,i]*y1[i,k].x))
        pod_days.append((i, x1[i].x))

    for k in blocks:
        for i in pod_sites:
            if(y1[i, k].x > 0):
                block_dist.append((k, distance[k,i]*y1[i,k].x, i)) 
    
    # Print optimized solution
    print(m1.objVal)

    return(m1.objVal, lst, pod_days, block_dist)

def min_max_distance(pod_sites, blocks, distance, population, loadingSites, capacity, supplies, labor, cost, budget, opening_cost, bigM, max_days_open):
    ####### MODEL 2 - Minimize the maximum distance traveled for any one block group
    m2 = gp.Model()

    ### Decision variables
    ## number of days POD is open for
    x2 = m2.addVars(pod_sites, vtype=GRB.CONTINUOUS, lb = 0.0)
    ## whether or not a block is assigned to a POD
    y2 = m2.addVars(pod_sites, blocks, vtype=GRB.BINARY)
    ## whether or not a POD is open
    z2 = m2.addVars(pod_sites, vtype=GRB.BINARY)
    ## M - the maximum distance any one car is allowed to travel
    M = m2.addVar(lb=0.0, obj=1.0, vtype=GRB.CONTINUOUS)

    ### Objective function
    ## want to minimize the total/weighted travel distance of Allegheny's population
    m2.setObjective(M)
    m2.modelSense = GRB.MINIMIZE
    
    ### Constraints
    ## all pod sites are bounded by a given capacity
    for i in pod_sites:
        #m1.addConstr(sum(y1[i, k]*population[k] for k in blocks) <= capacity[i]*x1[i])
        m2.addConstr(sum(y2[i, k]*population[k] for k in blocks) == capacity[i]*x2[i])
        m2.addConstr(z2[i]*bigM >= x2[i])
        m2.addConstr(x2[i] <= max_days_open)
     
    ## each block is assigned to exactly 1 pod site
    for k in blocks:
        m2.addConstr(sum(y2[i, k] for i in pod_sites) == 1)

        # the total money used is at most the maximum budget
        m2.addConstr(sum(cost[i]*x2[i] + z2[i]*opening_cost for i in pod_sites) <= budget)

    for i in pod_sites:
        for k in blocks:
            ## max dist traveled for anyone is M
            m2.addConstr(distance[k, i]*y2[i,k] <= M)

    ## Solve
    m2.optimize()

    lst = []
    lst_np = np.zeros([len(pod_sites), 1100])
    pod_days = []
    block_dist = []
    #long_ls_vals = []

    for i in pod_sites:
        for k in blocks:
            #if(x1[i].x >= 0): ## this will still print out all of them since weakly greater than 0.
            if(x2[i].x > 0):
                lst_np[i,k] = distance[k,i]*y2[i,k].x
                lst.append((budget, opening_cost, i, k, distance[k,i]*y2[i,k].x))

                #long_ls_vals.append((budget, opening_cost, m1.objVal, i, x1[i].x, k, distance[k,i]*y1[i,k].x))
        pod_days.append((i, x2[i].x))

    for k in blocks:
        for i in pod_sites:
            if(y2[i, k].x > 0):
                block_dist.append((k, distance[k,i]*y2[i,k].x, i)) 
    
    # Print optimized solution
    print(m2.objVal)

    return(m2.objVal, pod_days, block_dist)

def run_scenario_one(opening_cost, budget, bigM):
    ## Global epidemic in Allegheny county

    ## Define Parameters
    (pod_sites, blocks, distance, population, loadingSites, capacity, supplies, labor, cost, max_days_open) = define_parameters()
    print("*** Set up parameters...")

    s1_m1_optsoln = []
    s1_m2_optsoln = []
    good_options = []
    bad_options = []
    s1_m1_pods = []
    s1_m1_dist = []
    s1_m2_pods = []
    s1_m2_dist = []

    ## Loop through budget values, then opening cost to find optimal solutions 
    for b in budget:
        for op_co in opening_cost:
            try:
                print("*********** We are at budget:", b)
            ### Model 1
                (m1_opt_solution, lst, pod_days, block_dist) = min_tot_distance(pod_sites, blocks, distance, 
                    population, loadingSites, capacity, supplies, labor, cost, b, op_co, bigM, max_days_open)
                good_options.append((m1_opt_solution, lst))

                ## First we make a list of the budget, opening cost, and optimal solution for that pair
                s1_m1_optsoln.append((b, op_co, m1_opt_solution))
                ## List of Tuples #2 - pods open for number of days
                m1_pods = [(b, op_co, pod[0], pod[1]) for pod in pod_days]
                #s1_m1_pods.extend(m1_pods)
                s1_m1_pods = s1_m1_pods + m1_pods
                ## List of Tuples #3 - block distances traveled
                m1_dist = [(b, op_co, bdist[0], bdist[1], bdist[2]) for bdist in block_dist]
                #s1_m1_dist.extend(m1_dist)
                s1_m1_dist = s1_m1_dist + m1_dist
            except AttributeError:
                bad_options.append((b, op_co))
                print("*** Budget", b, "with opening cost", op_co, "was infeasible...moving on...")
                continue
    
    ### Model 1
    s1_m1_opt_vals_df = pd.DataFrame(s1_m1_optsoln, columns = ['Budget', 'Cost', 'TotalTravel(mi)'])
    s1_m1_pods_df = pd.DataFrame(s1_m1_pods, columns = ['Budget', 'Cost', 'POD', 'Days Open'])
    s1_m1_dist_df = pd.DataFrame(s1_m1_dist, columns = ['Budget', 'Cost', 'Block', 'DistTravel(mi)', 'DesignatedPOD'])
    #print("*** THESE ARE THE GOOD OPTIONS: \n", good_options)

    ## Save these to csv so that plotting can be done without running everything
    s1_m1_opt_vals_df.to_csv('s1_m1_optimalVals.csv', encoding = 'utf-8')
    s1_m1_pods_df.to_csv('s1_m1_podDays.csv', encoding = 'utf-8')
    s1_m1_dist_df.to_csv('s1_m1_blockDistances.csv', encoding = 'utf-8')

    for b in budget:
        for op_co in opening_cost:
            try:
                print("*********** We are at budget:", b)
            ### Model 2
                (m2_opt_solution, pod_days_m2, block_dist_m2) = min_max_distance(pod_sites, blocks, distance, 
                    population, loadingSites, capacity, supplies, labor, cost, b, op_co, bigM, max_days_open)
                good_options.append((m2_opt_solution))

                ## First we make a list of the budget, opening cost, and optimal solution for that pair
                s1_m2_optsoln.append((b, op_co, m2_opt_solution))
                ## List of Tuples #2 - pods open for number of days
                m2_pods = [(b, op_co, pod[0], pod[1]) for pod in pod_days_m2]
                #s1_m1_pods.extend(m1_pods)
                s1_m2_pods = s1_m2_pods + m2_pods
                ## List of Tuples #3 - block distances traveled
                m2_dist = [(b, op_co, bdist[0], bdist[1], bdist[2]) for bdist in block_dist_m2]
                #s1_m1_dist.extend(m1_dist)
                s1_m2_dist = s1_m2_dist + m2_dist

            except AttributeError:
                bad_options.append((b, op_co))
                print("*** Budget", b, "with opening cost", op_co, "was infeasible...moving on...")
                continue


    ### Model 2
    s1_m2_opt_vals_df = pd.DataFrame(s1_m2_optsoln, columns = ['Budget', 'Cost', 'TotalTravel(mi)'])
    s1_m2_pods_df = pd.DataFrame(s1_m2_pods, columns = ['Budget', 'Cost', 'POD', 'Days Open'])
    s1_m2_dist_df = pd.DataFrame(s1_m2_dist, columns = ['Budget', 'Cost', 'Block', 'DistTravel(mi)', 'DesignatedPOD'])
    #print("*** THESE ARE THE GOOD OPTIONS: \n", good_options)

    ## Save these to csv so that plotting can be done without running everything
    s1_m2_opt_vals_df.to_csv('s1_m2_optimalVals.csv', encoding = 'utf-8')
    s1_m2_pods_df.to_csv('s1_m2_podDays.csv', encoding = 'utf-8')
    s1_m2_dist_df.to_csv('s1_m2_blockDistances.csv', encoding = 'utf-8')

    return(s1_m1_opt_vals_df, s1_m1_pods_df, s1_m1_dist_df, s1_m2_opt_vals_df, s1_m2_pods_df, s1_m2_dist_df)

def run_scenario_two():
    ## Global epidemic in Allegheny county

    ## Setting up some parameters that will be looped through
    ## separate from the ones run for scenario 1
    opening_cost = 10000
    budget = [200000, 225000, 250000, 275000, 300000, 350000, 400000, 500000, 600000]
    
    bigM = 100000000000000000000 ## This is our big M

    ## Define Parameters
    (pod_sites, blocks, distance, population, loadingSites, capacity, supplies, labor, cost, max_days_open) = define_parameters()
    print("*** Set up parameters with define_parameter function...")

    pgh_blocks_idx = genfromtxt(path + '/pgh_blocks.csv', delimiter=',')
    pitts_pods_idx = np.array([2, 3, 6, 11, 18, 28, 29, 30, 40, 41, 45])
    pitts_pods_idx = pitts_pods_idx - 1
    pitts_pods_idx = pitts_pods_idx.tolist()

    num_pod_sites = len(pitts_pods_idx)
    num_blocks = len(pgh_blocks_idx)

    pod_sites = range(num_pod_sites)
    blocks = range(num_blocks)
    
    population = [population[k] for k in (int(i) for i in pgh_blocks_idx)]
    loadingSites = [loadingSites[i] for i in pitts_pods_idx]
    capacity = [capacity[i] for i in pitts_pods_idx]
    cost = [cost[i] for i in pitts_pods_idx]
    distance = np.take(distance, pgh_blocks_idx.astype(int), axis = 0)
    distance = np.take(distance, pitts_pods_idx, axis = 1)
    print("*** Loaded additional information for Scenario 2...")

    ### Model 1
    s2_m1_optsoln = []
    good_options = []
    bad_options = []
    s2_m1_pods = []
    s2_m1_dist = []

    ## Loop through budget values, then opening cost to find optimal solutions 
    for b in budget:
        try:
        	print("*********** We are at budget:", b)
            (m1_opt_solution, pod_days, block_dist) = min_tot_distance(pod_sites, blocks, distance, 
                population, loadingSites, capacity, supplies, labor, cost, b, opening_cost, bigM, max_days_open)
            good_options.append((m1_opt_solution))

        	## First we make a list of the budget, opening cost, and optimal solution for that pair
            s2_m1_optsoln.append((b, opening_cost, m1_opt_solution))
        	## List of Tuples #2
            m1_pods = [(b, opening_cost, pitts_pods_idx[pod[0]], pod[1]) for pod in pod_days]
            #s1_m1_pods.extend(m1_pods)
            s2_m1_pods = s2_m1_pods + m1_pods
            m1_dist = [(b, opening_cost, pgh_blocks_idx.astype(int)[bdist[0]], bdist[1], pitts_pods_idx[bdist[2]]) for bdist in block_dist]
            #s1_m1_dist.extend(m1_dist)
            s2_m1_dist = s2_m1_dist + m1_dist

        except AttributeError:
            bad_options.append((b, opening_cost))
            print("*** Budget", b, "with opening cost", opening_cost, "was infeasible...moving on...")
            continue

    s2_m1_opt_vals_df = pd.DataFrame(s2_m1_optsoln, columns = ['Budget', 'Cost', 'TotalTravel(mi)'])
    s2_m1_pods_df = pd.DataFrame(s2_m1_pods, columns = ['Budget', 'Cost', 'POD', 'Days Open'])
    s2_m1_dist_df = pd.DataFrame(s2_m1_dist, columns = ['Budget', 'Cost', 'Block', 'DistTravel(mi)', 'DesignatedPOD'])
    #print("*** THESE ARE THE GOOD OPTIONS: \n", good_options)

    ## Save these to csv so that plotting can be done without running everything
    s2_m1_opt_vals_df.to_csv(path + 's2_m1_optimalVals.csv', encoding = 'utf-8')
    s2_m1_pods_df.to_csv(path + 's2_m1_podDays.csv', encoding = 'utf-8')
    s2_m1_dist_df.to_csv(path + 's2_m1_blockDistances.csv', encoding = 'utf-8')

    ### Model 2
    s2_m2_optsoln = []
    good_options = []
    s2_m2_pods = []
    s2_m2_dist = []

    ## Loop through budget values, then opening cost to find optimal solutions 
    for b in budget:
        try:
        	print("*********** We are at budget:", b)
            (m2_opt_solution, lst, pod_days, block_dist) = min_max_distance(pod_sites, blocks, distance, 
                population, loadingSites, capacity, supplies, labor, cost, b, opening_cost, bigM, max_days_open)
            good_options.append((m2_opt_solution, lst))

        	## First we make a list of the budget, opening cost, and optimal solution for that pair
            s2_m2_optsoln.append((b, opening_cost, m2_opt_solution))
        	## List of Tuples #2
            m2_pods = [(b, opening_cost, pitts_pods_idx[pod[0]], pod[1]) for pod in pod_days]
            s2_m2_pods = s2_m2_pods + m2_pods
            m2_dist = [(b, opening_cost, pgh_blocks_idx.astype(int)[bdist[0]], bdist[1],  pitts_pods_idx[bdist[2]]) for bdist in block_dist]
            s2_m2_dist = s2_m2_dist + m2_dist

        except AttributeError:
            bad_options.append((b, opening_cost))
            print("*** Budget", b, "with opening cost", opening_cost, "was infeasible...moving on...")
            continue

    s2_m2_opt_vals_df = pd.DataFrame(s2_m2_optsoln, columns = ['Budget', 'Cost', 'TotalTravel(mi)'])
    s2_m2_pods_df = pd.DataFrame(s2_m2_pods, columns = ['Budget', 'Cost', 'POD', 'Days Open'])
    s2_m2_dist_df = pd.DataFrame(s2_m2_dist, columns = ['Budget', 'Cost', 'Block', 'DistTravel(mi)', 'DesignatedPOD'])

    ## Save these to csv so that plotting can be done without running everything
    s2_m2_opt_vals_df.to_csv(path + 's2_m2_optimalVals.csv', encoding = 'utf-8')
    s2_m2_pods_df.to_csv(path + 's2_m2_podDays.csv', encoding = 'utf-8')
    s2_m2_dist_df.to_csv(path + 's2_m2_blockDistances.csv', encoding = 'utf-8')

    return(s2_m1_opt_vals_df, s2_m1_pods_df, s2_m1_dist_df, s2_m2_opt_vals_df, s2_m2_pods_df, s2_m2_dist_df)

def main():
    ## Setting up some parameters that will be looped through the main function
    ## Specific to Scenario 1
    opening_cost = [10000]
    budget = [750000, 1000000, 1250000, 1500000, 1750000, 2000000, 2250000, 2500000, 5000000]
    
    bigM = 100000000000000000000 ## This is our big M

    #### Scenario 1
    (s1_m1_opt_vals_df, s1_m1_pods_df, s1_m1_dist_df, s1_m2_opt_vals_df, s1_m2_pods_df, s1_m2_dist_df) = run_scenario_one(opening_cost, budget, bigM)
    ### Model 1
    print("*** Scenario 1 - Model 1 - Optimal Total Distance: \n", s1_m1_opt_vals_df)
    print("*** Scenario 1 - Model 1 - POD Days Open: \n", s1_m1_pods_df)
    print("*** Scenario 1 - Model 1 - Block Distance Traveled: \n", s1_m1_dist_df)
    ### Model 2
    print("*** Scenario 1 - Model 2 - Optimal Total Distance: \n", s1_m2_opt_vals_df)
    print("*** Scenario 1 - Model 2 - POD Days Open: \n", s1_m2_pods_df)
    print("*** Scenario 1 - Model 2 - Block Distance Traveled: \n", s1_m2_dist_df)

    #### Scenario 2
    (s2_m1_opt_vals_df, s2_m1_pods_df, s2_m1_dist_df, s2_m2_opt_vals_df, s2_m2_pods_df, s2_m2_dist_df) = run_scenario_two()
    ### Model 1
    print("*** Scenario 1 - Model 1 - Optimal Total Distance: \n", s2_m1_opt_vals_df)
    print("*** Scenario 1 - Model 1 - POD Days Open: \n", s2_m1_pods_df)
    print("*** Scenario 1 - Model 1 - Block Distance Traveled: \n", s2_m1_dist_df)
    ### Model 2
    print("*** Scenario 2 - Model 2 - Optimal Total Distance: \n", s2_m2_opt_vals_df)
    print("*** Scenario 2 - Model 2 - POD Days Open: \n", s2_m2_pods_df)
    print("*** Scenario 2 - Model 2 - Block Distance Traveled: \n", s2_m2_dist_df)
    print("*** Scenario 2 - Model 2 - Block Distance Traveled: \n", s2_m2_dist_df)

if __name__ == '__main__':
    main()