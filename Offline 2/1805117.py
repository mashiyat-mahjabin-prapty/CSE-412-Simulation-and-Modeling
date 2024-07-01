import PMMLCG
import math

outfile = open("out.txt", "w")

# initialization function
def initialize():
    # init the simulation clock
    global sim_time
    sim_time = 0.0

    # init the state variables
    global inv_level
    global initial_inv_level
    inv_level = initial_inv_level

    global time_last_event
    time_last_event = 0.0

    # init the statistical counters
    global total_ordering_cost
    total_ordering_cost = 0.0

    global area_holding
    area_holding = 0.0

    global area_shortage
    area_shortage = 0.0

    # init the event list
    global time_next_event
    global mean_interdemand
    global num_months
    time_next_event = [0.0, 1.0e+30, sim_time+expon(mean_interdemand), num_months, 0.0]

# timing function
def timing():
    global sim_time
    global next_event_type
    global time_next_event
    global num_events
    
    min_time_next_event = 1.0e+29
    next_event_type = 0

    for i in range(1, num_events + 1):
        if time_next_event[i] < min_time_next_event:
            min_time_next_event = time_next_event[i]
            next_event_type = i
    
    if next_event_type == 0:
        outfile.write("Event list empty at time " + str(sim_time))
        exit()
        
    # advance the simulation clock    
    sim_time = min_time_next_event

# order arrival event function
def order_arrival():
    global inv_level
    global amount
    global time_next_event

    # increment the inventory level by the amount ordered
    inv_level += amount

    # since no order is outstanding, eliminate the order arrival event from consideration
    time_next_event[1] = 1.0e+30

# demand event function
def demand():
    # decrement the inventory level by a generated demand size
    global inv_level
    global prob_distrib_demand
    inv_level -= random_integer(prob_distrib_demand)

    # schedule the time of the next demand
    global sim_time
    global mean_interdemand
    global time_next_event
    time_next_event[2] = sim_time + expon(mean_interdemand)

# inventory evaluation event function
def evaluate():
    # check whether inventory level is less than smalls
    global inv_level
    global smalls
    global bigs
    global inv_level
    global time_next_event
    global sim_time
    global amount
    global total_ordering_cost
    global setup_cost
    global minlag, maxlag

    if inv_level < smalls:
        # place an order for the appropriate amount
        amount = bigs - inv_level
        total_ordering_cost += setup_cost + incremental_cost * amount
        # schedule the arrival of the order
        time_next_event[1] = sim_time + uniform(minlag, maxlag)

    # schedule the next inventory evaluation
    time_next_event[4] = sim_time + 1.0

# report generator function
def report():
    # compute and write estimates of desired measures of performance
    global total_ordering_cost
    global area_holding
    global area_shortage 
    global num_months
    global holding_cost
    global shortage_cost
    global smalls
    global bigs

    avg_ordering_cost = total_ordering_cost / num_months
    avg_holding_cost = holding_cost * area_holding / num_months
    avg_shortage_cost = shortage_cost * area_shortage / num_months

    avg_total_cost = avg_ordering_cost + avg_holding_cost + avg_shortage_cost

    outfile.write("\n(" + str(smalls) + ", " + str(bigs) + ")\t\t" + str("{:.2f}".format(avg_total_cost)).center(8) + 3*"\t" + str("{:.2f}".format(avg_ordering_cost)).center(8) + 4*"\t" + str("{:.2f}".format(avg_holding_cost)).center(8) + 4*"\t" + str("{:.2f}".format(avg_shortage_cost)).center(8) + "\n")

# update area accumulators for time-average statistics
def update_time_avg_stats():
    global sim_time
    global inv_level
    global time_last_event
    global area_holding
    global area_shortage

    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time

    if inv_level < 0:
        area_shortage -= inv_level * time_since_last_event
    elif inv_level > 0:
        area_holding += inv_level * time_since_last_event

# random integer generation function
def random_integer(prob_distrib):
    # generate a U(0,1) random variate
    u = PMMLCG.lcgrand(1)

    # find the interval into which u falls
    i = 1
    while u >= prob_distrib[i]:
        i += 1

    return i

# uniform variate generation function
def uniform(a, b):
    # generate a U(a,b) random variate
    u = PMMLCG.lcgrand(1)

    return a + u * (b - a)

def expon(mean):
    return -mean * math.log(PMMLCG.lcgrand(1))

# main function
def main():
    global num_events
    num_events = 4

    global initial_inv_level
    global num_months
    global num_policies
    global setup_cost
    global incremental_cost
    global holding_cost
    global shortage_cost
    global minlag
    global maxlag
    global smalls
    global bigs
    global num_values_demand
    global mean_interdemand

    infile = open("in.txt", "r")
    p = infile.readline()
    initial_inv_level, num_months, num_policies = p.split()
    initial_inv_level = int(initial_inv_level)
    num_months = int(num_months)
    num_policies = int(num_policies)
    p = infile.readline()
    num_values_demand, mean_interdemand = p.split()
    num_values_demand = int(num_values_demand)
    mean_interdemand = float(mean_interdemand)
    p = infile.readline()
    setup_cost, incremental_cost, holding_cost, shortage_cost = p.split()
    setup_cost = float(setup_cost)
    incremental_cost = float(incremental_cost)
    holding_cost = float(holding_cost)
    shortage_cost = float(shortage_cost)
    p = infile.readline()
    minlag, maxlag = p.split()
    minlag = float(minlag)
    maxlag = float(maxlag)

    global prob_distrib_demand
    prob_distrib_demand = [0.0] * (num_values_demand+1)
    p = infile.readline()
    ff = p.split()
    for i in range(1, num_values_demand+1):
        prob_distrib_demand[i] = float(ff[i-1])

    outfile.write('------Single-Product Inventory System------\n\n')
    outfile.write('Initial inventory level: ' + str(initial_inv_level) + ' items\n\n')
    outfile.write('Number of demand sizes: ' + str(num_values_demand) + '\n\n')
    outfile.write('Distribution function of demand sizes: ')
    for i in range(1, num_values_demand+1):
        outfile.write(str("{:.2f}".format(prob_distrib_demand[i])) + ' ')
    outfile.write('\n\n')
    outfile.write('Mean inter-demand time: ' + str("{:.2f}".format(mean_interdemand)) + ' months\n\n')
    outfile.write('Delivery lag range: ' + str("{:.2f}".format(minlag)) + ' to ' + str("{:.2f}".format(maxlag)) + ' months\n\n')
    outfile.write('Length of simulation: ' + str(num_months) + ' months\n\n')
    
    outfile.write('Costs:\n')
    outfile.write('K = ' + str("{:.2f}".format(setup_cost)) + '\n')
    outfile.write('i = ' + str("{:.2f}".format(incremental_cost)) + '\n')
    outfile.write('h = ' + str("{:.2f}".format(holding_cost)) + '\n')
    outfile.write('pi = ' + str("{:.2f}".format(shortage_cost)) + '\n\n')

    outfile.write('Number of policies: ' + str(num_policies) + '\n\n')
    outfile.write('Policies:\n')
    outfile.write('--------------------------------------------------------------------------------------------------\n')
    outfile.write('Policy\t\tAvg_total_cost\t\tAvg_ordering_cost\t\tAvg_holding_cost\t\tAvg_shortage_cost\n')
    outfile.write('--------------------------------------------------------------------------------------------------\n')

    for i in range(num_policies):
        p = infile.readline()
        smalls, bigs = p.split()
        smalls = int(smalls)
        bigs = int(bigs)
        initialize()
        while True:
            timing()
            # update time-average statistical accumulators
            update_time_avg_stats()

            # invoke the appropriate event function
            if next_event_type == 1:
                order_arrival()
            elif next_event_type == 2:
                demand()
            elif next_event_type == 4:
                evaluate()
            elif next_event_type == 3:
                report()
                break
    outfile.write('\n--------------------------------------------------------------------------------------------------')

    infile.close()
    outfile.close()

if __name__ == "__main__":
    main()