# dabpGroupProject2021
tldr: Spring Semester 2021, DABP course group project repository

Team: Ali Iftikhar (aliiftik), Pooja Puvvadi (ppuvvadi), Jeffrey Scanlon (jscanlo2), Sormeh Yazdi (sormehy)
Date: May, 2021
Course: Decision Analytics for Public Policy

This repository contains three directories:
- V1_DABP_Code
- V2_DABP_Code
- Final_DABP

### Final_DABP
This directory contains the files necessary to run `final_dabp_project.py` and the csv files necessary to run the script.
Files necessary to run `final_dabp_project.py`:
- Distances.csv: lists distances between the census blocks and the POD sites (1100 x 47)
- Labor.csv: list of cost of labor at each POD site (47 x 1)
- LoadingSites.csv: list of available loading spots at each POD site (47 x 1)
- Populations.csv: list of population in each census block (1100 x 1)
- Supplies.csv: list of cost of supplies that are given to the population (9 x 1)
- pgh_blocks.csv: list of population in each block specifically within Pittsburgh (361 x 1)
- pgh_pods.csv: list of POD capacities within Pittsburgh (11 x 1)
- popDens.csv: dataframe of population and population density of each census block (1100 x 3)

`final_dabp_project.py`
- To run this script from the terminal: `<python3 final_dabp_project.py>`
- Contains 6 functions:
  - define_parameters()
      - loads all necessary csv files for the code, calculate daily cost, set other necessary parameters
  - min_tot_distance(pod_sites, blocks, distance, population, loadingSites, capacity, supplies, labor, cost, budget, opening_cost, bigM, max_days_open)
      - creates gurobi model minimizing total weighted distance traveled by all census blocks
  - min_max_distance(pod_sites, blocks, distance, population, loadingSites, capacity, supplies, labor, cost, budget, opening_cost, bigM, max_days_open)
      - creates gurobi model minimizing the maximum distance traveled by any individual census block
  - run_scenario_one(opening_cost, budget, bigM)
      - focuses on scenario one (Allegheny County emergency)
      - runs both min_tot_distance and min_max_distance, looping through budget values for sensitivity analysis
      - creates dataframes that are saved as csv files for future plotting
      - iterates through 9 different budget values
  - run_scenario_two()
      - focuses on scenario one (Pittsburgh City emergency)
      - runs both min_tot_distance and min_max_distance, looping through budget values for sensitivity analysis
      - creates dataframes that are saved as csv files for future plotting
      - iterates through 9 different budget values
  - main()
      - runs both run_scenario_one and run_scenario_two
      - prints dataframes for sanity check

#### OutputFiles
Contains the outputfiles created by `final_dabp_project.py`
- s1_m1_blockDistances.csv
  - lists budget, cost, block, distances traveled (miles), and designated POD for each budget simulation (9899 x 5)
- s1_m1_optimalVals.csv
  - lists budget, cost, and optimal total distance traveled (miles) (9 x 3)
- s1_m1_podDays.csv
  - lists budget, cost, POD #, number of days the POD remains open (422 x 4)
- s1_m2_blockDistances.csv
- s1_m2_optimalVals.csv
- s1_m2_podDays.csv
- s2_m1_blockDistances.csv
- s2_m1_optimalVals.csv
- s2_m1_podDays.csv
- s2_m2_blockDistances.csv
- s2_m2_optimalVals.csv
- s2_m2_podDays.csv

### V1_DABP_Code
Our first round of coding - can be ignored

### V2_DABP_Code
Most of our work lives in this directory. Many different iterations of the code, in many different files, along with all the csv files necessary.
