# import PMMLCG file
import PMMLCG
import math

Q_LIMIT = 100

fevent = open('event_orders.txt', 'w')

def init_():
    global sim_time
    global server_status
    global num_in_q
    global time_last_event
    global num_customers_delayed
    global total_of_delays
    global area_num_in_q
    global area_server_status
    global time_next_event
    global total_events

    global total_customer

    total_events = 0

    sim_time = 0.0

    server_status = 0
    num_in_q = 0
    time_last_event = 0.0

    num_customers_delayed = 0
    total_of_delays = 0.0
    area_num_in_q = 0.0
    area_server_status = 0.0

    time_next_event = [0.0, sim_time + expon(mean_interarrival), 1.0e+30]

    total_customer = 0

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
        fout = open("results.txt", "a")
        fout.write("Event list empty at time " + str(sim_time))
        exit()
        
        
    sim_time = min_time_next_event

def arrive():
    global num_in_q
    global time_next_event
    global total_of_delays
    global num_customers_delayed
    global server_status
    global time_arrival
    global sim_time
    global total_events

    global total_customer
    time_next_event[1] = sim_time + expon(mean_interarrival)
    total_events+=1
    total_customer += 1
    fevent.write(str(total_events)+". Next event: Customer " + str(total_customer) + " Arrival\n")

    if server_status == 1:
        num_in_q += 1
        if num_in_q > Q_LIMIT:
            fout = open("results.txt", "a")
            fout.write("Overflow of the array time_arrival at time " + str(sim_time))
            exit()
        time_arrival[num_in_q] = sim_time
        
    else:
        # delay = 0.0
        # total_of_delays += delay
        
        num_customers_delayed += 1
        fevent.write("\n---------No. of customers delayed: " + str(num_customers_delayed) + "--------\n\n")
        
        server_status = 1

        time_next_event[2] = sim_time + expon(mean_service)   

def depart():
    global server_status
    global time_next_event
    global num_in_q
    global num_customers_delayed
    global total_of_delays
    global time_arrival
    global sim_time
    global total_events
    total_events += 1
    fevent.write(str(total_events)+". Next event: Customer " + str(num_customers_delayed) + " Departure\n")

    # check if queue is empty
    if num_in_q == 0:
        # server is idle
        server_status = 0
        time_next_event[2] = 1.0e+30
    else:
        num_in_q -= 1

        delay = sim_time - time_arrival[1]
        total_of_delays += delay

        num_customers_delayed += 1
        fevent.write("\n---------No. of customers delayed: " + str(num_customers_delayed) + "--------\n\n")

        time_next_event[2] = sim_time + expon(mean_service)

        # move each customer in queue (if any) up one place
        for i in range(1, num_in_q + 1):
            time_arrival[i] = time_arrival[i + 1]

def report():
    fout = open("results.txt", "a")
    fout.write("Avg delay in queue: " + str(total_of_delays / num_customers_delayed) + " minutes\n")
    fout.write("Avg number in queue: " + str(area_num_in_q / sim_time) + "\n")
    fout.write("Server utilization: " + str(area_server_status / sim_time) + "\n")
    fout.write("Time simulation ended: " + str(sim_time) + " minutes\n")
    fout.close()

def expon(mean):
    # print("mean: " + str(mean))
    return -mean * math.log(PMMLCG.lcgrand(1))

def update_time_avg_stats():
    global area_num_in_q
    global area_server_status
    global time_last_event
    global sim_time
    global time_last_event
    global num_in_q
    global server_status

    time_since_last_event = sim_time - time_last_event
    time_last_event = sim_time

    area_num_in_q += num_in_q * time_since_last_event

    area_server_status += server_status * time_since_last_event


num_events = 2
time_arrival = [0.0] * (Q_LIMIT + 1)

fin = open("IOs/io2/in.txt", "r")
# read in parameters
mean = fin.readline()
mean_interarrival, mean_service, num_delays_required = mean.split()
mean_interarrival = float(mean_interarrival)
mean_service = float(mean_service)
num_delays_required = int(num_delays_required)
fin.close()

fout = open("results.txt", "w")
fout.write("----Single-Server Queueing System----\n\n")
fout.write("Mean inter-arrival time: " + str(mean_interarrival) + " minutes\n")
fout.write("Mean service time: " + str(mean_service) + " minutes\n")
fout.write("Number of customers: " + str(num_delays_required) + "\n\n")
fout.close()

# initialize
init_()

# run simulation
while num_customers_delayed < num_delays_required:
    timing()
    update_time_avg_stats()
    if next_event_type == 1:
        arrive()
    elif next_event_type == 2:
        depart()
        
report()
fevent.close()