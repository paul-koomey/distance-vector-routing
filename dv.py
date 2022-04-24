# Paul Koomey
# 1001696560

# to run:
# 
# run code
# python3 dv.py [input_file]


# import libraries
import sys
import time


# given an array of nodes and links, this function will get the number of nodes in the network
def get_num_nodes(nodes):
    num_nodes = 0
    for n in nodes:
        num_nodes = max(num_nodes, n[0], n[1])
    return num_nodes


# given number of nodes and node matrices, print out the distance vector tables
def print_tables(num_nodes, distance_vector_table, routing_table):
    for i in range(num_nodes):
        print("Node %d Distance Vector Table" % (i + 1), end='')
        print(" " * (5 * num_nodes), end='')
        print("Node %d Routing Table" % (i + 1))
        print('     ', end='')
        for num in range(num_nodes):
            print('    %d' % (num+1), end='')
        print(' (cost to)         Next Router  |  Destination', end='')
        print('\n=====', end='')
        print("=====" * num_nodes, end='')
        print("                   ===========================")
        for count, r in enumerate(distance_vector_table[i]):
            print("  ", (count+1), "|", end='')
            for n in r:
                print("| %2d " % n, end='')
            print("                       %s       |       %d" % (routing_table[i][count], count + 1), end='')
            print()
        print('(from)')
        print()


# initialize variables for distance vector algorithm
inputs = []                     # input array
nodes = []                      # distance vector array
num_nodes = -1                  # number of nodes in the network
infinity = 16                   # number representing infinity in the network
without_intervention = False    # when true, the program will run all the way through without intervention
num_cycles = 1                  # number of cycles for algorithm to reach stable state
changes = True                  # set changes to true to go through while loop
original_connections = []       # keeps track of which nodes connect to others


# read file and create input array of nodes and link values
try:
    with open(sys.argv[1], 'r') as input_file:
        inputs = input_file.readlines()
        for i in range(len(inputs)):
            inputs[i] = inputs[i].split()
            inputs[i] = [int(n) for n in inputs[i]]
    num_nodes = get_num_nodes(inputs)
except:
    exit("Error: enter input file in correct format")



# create matrix to hold link values between nodes in the network
# create routing table to hold next node to reach destination
# create matrix to store which nodes are neighbors
# create matrix to store link costs between neighbors
distance_vector_table = [[[infinity for x in range(num_nodes)] for y in range(num_nodes)] for z in range(num_nodes)]
routing_table = [["-" for x in range(num_nodes)] for y in range(num_nodes)]
original_connections = [[0 for y in range(num_nodes)] for z in range(num_nodes)]
link_costs = [[0 for x in range(num_nodes)] for y in range(num_nodes)]

# assign link values and routing nodes
for i in range(len(distance_vector_table)):
    distance_vector_table[i][i][i] = 0
    for n in inputs:
        if n[0]-1 == i:
            distance_vector_table[i][n[0]-1][n[1]-1] = n[2]
            routing_table[n[0]-1][n[1]-1] = n[1]
            link_costs[n[0]-1][n[1]-1] = n[2]
        if n[1]-1 == i:
            distance_vector_table[i][n[1]-1][n[0]-1] = n[2]
            routing_table[n[1]-1][n[0]-1] = n[0]
            link_costs[n[1]-1][n[0]-1] = n[2]
        original_connections[n[0]-1][n[1]-1] = 1
        original_connections[n[1]-1][n[0]-1] = 1

# print initial links to user
print("--------------------") 
print("--------------------") 
print("Initail Link Costs:\n")
print_tables(num_nodes, distance_vector_table, routing_table)
print("--------------------") 


# update nodes until they cannot be updated any more
while(True):

    # set changes to false initially incase there are none
    changes = False


    # get input from user to determine if program will update a node or continue
    if not without_intervention:
        
        # ask user for input and confirm that it is 'c', 'w', 'n', or 'q'
        print("Type 'c' to continue, 'w' to continue without stopping, 'n' to change value of a node, or 'q' to quit.")
        command = input("> ")
        while command != "c" and command != "w" and command != "n" and command != "q":
            command = input("Invalid, type 'c', 'w', 'n', or 'q': ")

        # if q is entered, quit the program
        # if w is entered, run the program until stable state
        # if n is entered, change node and skip loop
        # if c is entered, go through loop
        # otherwise ask for input again
        
        if command == 'q':
            exit(0)
        elif command == 'w':
            without_intervention = True
            # get starting time for algorithm
            start = time.time()
        elif command == 'n':
            node1, node2 = '', ''
            
            # ask for the first node
            print("Enter the two nodes you would like to change the link cost between:")
            node1 = input("Node 1: ")
            while (not node1.isnumeric() or int(node1) < 1 or int(node1) > num_nodes):
                print("Invalid node, enter again.")
                node1 = input("Node 1: ")
            node1 = int(node1) - 1
            
            # ask for the second node
            node2 = input("Node 2: ")
            while (not node2.isnumeric() or int(node2) < 1 or int(node2) > num_nodes or node1 == int(node2)-1):
                print("Invalid node, enter again.")
                node2 = input("Node 2: ")
            node2 = int(node2) - 1

            # ask for the new link cost
            print("What would you like to change the link cost to?")
            new_link_cost = input("New link cost: ")
            while (not new_link_cost.isnumeric() or int(new_link_cost) < 0 or int(new_link_cost) > infinity):
                print("Invalid link cost, enter again.")
                new_link_cost = input("New link cost: ")

            # convert the link cost to an int and set the new link costs in the table
            new_link_cost = int(new_link_cost)
            distance_vector_table[node1][node1][node2] = new_link_cost
            distance_vector_table[node2][node2][node1] = new_link_cost
            link_costs[node1][node2] = new_link_cost
            link_costs[node2][node1] = new_link_cost

            # set changes to true so that the loop will be looped through again
            changes = True

            # print links to user
            print("--------------------")
            print()
            print("----Changed Nodes---")
            print_tables(num_nodes, distance_vector_table, routing_table)
            print("--------------------")
            num_cycles = 1
            continue
    

    # send DV row to all immediate neighbors
    for i in range(num_nodes):
        for j in range(num_nodes):
            if original_connections[i][j]== 1:
                distance_vector_table[j][i] = distance_vector_table[i][i][:]


    # print links to user
    print("--------------------")
    print("Cycle %d:\n" % num_cycles)
    print_tables(num_nodes, distance_vector_table, routing_table)
    print("--------------------")


    # once all rows are sent, recompute all link costs
    for i in range(num_nodes): # from node
        for j in range(num_nodes): # to node
            if i != j: # so that a nodes link to itself isnt calculated
                
                # set temporary variables to check minimum cost
                original_dv = distance_vector_table[i][i][j]
                temp_min = infinity + 1
                distance_vector_table[i][i][j] = link_costs[i][0] + distance_vector_table[i][0][j]
                prev_node = 1

                for k in range(1, num_nodes): # intermediate node

                    # if the current calculated total link cost is less than the current min, replace the min and change the routing table
                    if link_costs[i][k] + distance_vector_table[i][k][j] < temp_min:
                        temp_min = link_costs[i][k] + distance_vector_table[i][k][j]
                        prev_node = k + 1
                
                # update distance vector table
                distance_vector_table[i][i][j] = temp_min
                
                # if dv table is update, set changes to True
                if original_dv != distance_vector_table[i][i][j]:
                    changes = True
                    routing_table[i][j] = prev_node


    
    
    # if there were changes, then the number of cycles increased
    if changes != True:
        # get time that distance vector algorithm completes
        end = time.time()

        # print final output to the user
        print()
        print("Algorithm has reached a stable state.")
        if without_intervention:
            print("Total time to execute: %.6f seconds" % (end - start))
        print("Number of cycles: %d" % num_cycles)
        print()
        without_intervention = False
    
    # increment number of cycles for algorithm
    num_cycles += 1
