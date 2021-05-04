def run_scenario_two_m1():
    ## Global epidemic in Allegheny county

    ## Setting up some parameters that will be looped through the main function
    #opening_cost = [5000, 10000, 25000, 50000]
    #budget = [1000000, 2500000, 5000000, 10000000]
    opening_cost = [5000]
    budget = [1000000]
    bigM = 100000000000000000000 ## This is our big M

    ## Define Parameters
    (pod_sites, blocks, distance, population, loadingSites, capacity, supplies, labor, cost, max_days_open) = define_parameters()
    print("*** Set up parameters...")

    pgh_blocks_idx = genfromtxt(path + '/pgh_blocks.csv', delimiter=',')
    pitts_pods_idx = np.array([2, 3, 6, 11, 18, 28, 29, 30, 40, 41, 45])
    pitts_pods_idx = pitts_pods_idx - 1
    pitts_pods_idx = pitts_pods_idx.tolist()
    pitts_pods_idx = genfromtxt(path + '/pgh_pods.csv', delimiter=',') 

    num_pod_sites = len(pitts_pods_idx)
    num_blocks = len(pgh_blocks_idx)

    pod_sites = range(num_pod_sites)
    blocks = range(num_blocks)

    pod_sites = [pod_sites[i] for i in pitts_pods_idx]
    blocks = [blocks[k] for k in (int(i) for i in pgh_blocks_idx)]
    population = [population[k] for k in (int(i) for i in pgh_blocks_idx)]
    loadingSites = [loadingSites[i] for i in pitts_pods_idx]
    capacity = [capacity[i] for i in pitts_pods_idx]
    cost = [cost[i] for i in pitts_pods_idx]
    distance = np.take(distance, pgh_blocks_idx, axis = 0)
    distance = np.take(distance, pitts_pods_idx, axis = 1)
        

    s1_m1_optsoln = []
    good_options = []
    bad_options = []
    s1_m1_pods = []
    s1_m1_dist = []

    ## Loop through budget values, then opening cost to find optimal solutions 
    for b in budget:
        for op_co in opening_cost:
            try:
                (m1_opt_solution, lst, pod_days, block_dist) = min_tot_distance(pod_sites, blocks, distance, 
                    population, loadingSites, capacity, supplies, labor, cost, b, op_co, bigM, max_days_open)
                good_options.append((m1_opt_solution, lst))

            ## First we make a list of the budget, opening cost, and optimal solution for that pair
                s1_m1_optsoln.append((b, op_co, m1_opt_solution))
            ## List of Tuples #2
                m1_pods = [(b, op_co, pod[0], pod[1]) for pod in pod_days]
                #s1_m1_pods.extend(m1_pods)
                s1_m1_pods = s1_m1_pods + m1_pods
                m1_dist = [(b, op_co, bdist[0], bdist[1]) for bdist in block_dist]
                #s1_m1_dist.extend(m1_dist)
                s1_m1_dist = s1_m1_dist + m1_dist

            except AttributeError:
                bad_options.append((b, op_co))
                print("*** Budget", b, "with opening cost", op_co, "was infeasible...moving on...")
                continue

    s1_m1_opt_vals_df = pd.DataFrame(s1_m1_optsoln, columns = ['Budget', 'Cost', 'TotalTravel(mi)'])
    s1_m1_pods_df = pd.DataFrame(s1_m1_pods, columns = ['Budget', 'Cost', 'POD', 'Days Open'])
    s1_m1_dist_df = pd.DataFrame(s1_m1_dist, columns = ['Budget', 'Cost', 'Block', 'DistTravel(mi)'])
    #print("*** THESE ARE THE GOOD OPTIONS: \n", good_options)

    ## Save these to csv so that plotting can be done without running everything
    s1_m1_opt_vals_df.to_csv('s1_m1_optimalVals.csv', encoding = 'utf-8')
    s1_m1_pods_df.to_csv('s1_m1_podDays.csv', encoding = 'utf-8')
    s1_m1_dist_df.to_csv('s1_m1_blockDistances.csv', encoding = 'utf-8')

    return(s1_m1_opt_vals_df, s1_m1_pods_df, s1_m1_dist_df)
