#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 14:09:15 2021

@author: Pooja
"""

import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd


# indices and parameters

num_pod_sites = 47
num_blocks = 1100

pod_sites = range(num_pod_sites)
blocks = range(num_blocks)

hoursOpen = 12
peoplePerCar = 3
carsPerHour = 6

distance = pd.read_csv('Distances.csv', header=None, sep=',')

population = pd.read_csv('Populations.csv', header=None, sep=',')
population = population.astype(float)

loadingSites = pd.read_csv('LoadingSites.csv', header=None, sep=',')
capacity = loadingSites * hoursOpen * peoplePerCar * carsPerHour

supplies = pd.read_csv('Supplies.csv', header=None, sep=',')
labor = pd.read_csv('Labor.csv', header=None, sep=',')
cost = labor + (supplies.sum()*loadingSites*hoursOpen*carsPerHour)

budget = 1000000000000


####### MODEL 1
m1 = gp.Model()


# Decision variables
x1 = m1.addVars(pod_sites, vtype=GRB.BINARY)
y1 = m1.addVars(pod_sites, blocks, vtype=GRB.BINARY)

# Objective function
m1.modelSense = GRB.MINIMIZE
m1.setObjective(sum(sum(distance.iloc[k, i]*population.iloc[k]*y1[i,k] for i in pod_sites) for k in blocks))


# Constraints

## all pod sites are bounded by a given capacity
for i in pod_sites:
    m1.addConstr(sum(y1[i, k]*population.iloc[k] for k in blocks) <= capacity.iloc[i]*x1[i])

## each block is assigned to exactly 1 pod site
for k in blocks:
    m1.addConstr(sum(y1[i, k] for i in pod_sites) == 1)

# the total money used is at most the maximum budget
m1.addConstr(sum(cost.iloc[i]*x1[i] for i in pod_sites) <= budget)


m1.optimize()



####### MODEL 2
m2 = gp.Model()

# Decision variables
x2 = m2.addVars(pod_sites, vtype=GRB.BINARY)
y2 = m2.addVars(pod_sites, blocks, vtype=GRB.BINARY)
M = m2.addVar(lb=0.0, obj=1.0, vtype=GRB.CONTINUOUS)

# Objective function
m2.modelSense = GRB.MINIMIZE
m2.setObjective(M)

# Constraints

## maximum distance traveled for anyone is M
for i in pod_sites:
    for k in blocks:
        m2.addConstr((y2[i, k]*distance.iloc[k, i]) <= M)

## all pod sites are bounded by a given capacity
for i in pod_sites:
    m2.addConstr(sum(y2[i, k]*population.iloc[k] for k in blocks) <= capacity.iloc[i]*x2[i])

## each block is assigned to exactly 1 pod site
for k in blocks:
    m2.addConstr(sum(y2[i, k] for i in pod_sites) == 1)

# the total money used is at most the maximum budget
m2.addConstr(sum(cost.iloc[i]*x2[i] for i in pod_sites) <= budget)


m2.optimize()

