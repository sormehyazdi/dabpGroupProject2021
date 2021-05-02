"""
File Name: dabp_project_code.py
Author: aliiftik, ppuvvadi, jscanlo2, sormehy
Date: May, 2021
Python version: 3
Purpose: POD site allocation 
    - 1100 blocks
    - 47 possible PODs
    - hours each POD is available = 12
    - people per vehicle = 4
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
    carsPerHour = 6

    budget = 1000000000000

    #distance = pd.read_csv('Distances.csv', header=None, sep=',')
    distance = genfromtxt(PATH + '/Distances.csv', delimiter=',') 

    #population = pd.read_csv('Populations.csv', header=None, sep=',')
    population = genfromtxt(PATH + '/Populations.csv', delimiter=',') 
    #population = population.astype(float)


    #loadingSites = pd.read_csv('LoadingSites.csv', header=None, sep=',')
    loadingSites = genfromtxt(PATH + '/LoadingSites.csv', delimiter=',') 
    capacity = loadingSites * hoursOpen * peoplePerCar * carsPerHour

    #supplies = pd.read_csv('Supplies.csv', header=None, sep=',')
    supplies = genfromtxt(PATH + '/Supplies.csv', delimiter=',') 

    #labor = pd.read_csv('Labor.csv', header=None, sep=',')
    labor = genfromtxt(PATH + '/Labor.csv', delimiter=',') 
    cost = labor + (supplies.sum()*loadingSites*hoursOpen*carsPerHour)

    return(pod_sites, blocks, distance, population, loadingSites, capacity, supplies, labor, cost)


def main():
    (pod_sites, blocks, distance, population, loadingSites, capacity, supplies, labor, cost) = define_parameters()
    print("Set up parameters...")
    


if __name__ == '__main__':
    main()