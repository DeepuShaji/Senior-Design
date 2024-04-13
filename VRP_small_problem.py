# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 14:02:45 2024

@author: deepu
"""
import csv
from pulp import *

#nodes
nodes = ['A','B','C','D','E','F']


# time matrix
tij = {}


with open(r'C:\Users\deepu\OneDrive\Documents\Seniordesign\firstdata.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    
    # Read the first row to get the field names
    fieldnames = next(reader)
    
    # Remove any unwanted characters from field names
    fieldnames = [name.strip().replace('\ufeff', '') for name in fieldnames]
    
    # Loop through each row in the CSV file
    for row in reader:
        From = row[0].strip()  # Use index 0 for 'From'
        To = row[1].strip()    # Use index 1 for 'To'
        Cost = float(row[2])   # Use index 2 for 'Cost'
        
        # Populate the dictionary
        if From not in tij:
            tij[From] = {}
        if To not in tij:
            tij[To] = {}
        
        tij[From][To] = Cost
        tij[To][From] = Cost

# demand level
d = {'A':0,'B':15,'C':12,'D':9,'E':20,'F':17}

# time windows
t = {'A':(0,0),
     'B':(30,150),
     'C':(90,210),  #'C':(90,210) 12,'D':(240,360),9
     'D':(240,360),
     'D':(240,360),
     'E':(150,270),
     'F':(300,420)
     }
service_time = 45

# capacity of mobile locker
capacity = 25

# number of vehicles
ML = 3
# big constant M
M = 1000

# decision variables
xij = LpVariable.dicts('x', ((i, j, k) for i in nodes for j in nodes for k in range(ML)), 0, 1, LpBinary)
u = LpVariable.dicts('u',nodes,0, M, LpInteger)
s = LpVariable.dicts('s', nodes, cat=LpContinuous)


# objective function
problem = LpProblem("VRP_with_time_window", LpMinimize)
problem += lpSum(xij[i, j, k] * tij[i][j] for i in nodes for j in nodes for k in range(ML))

# Constraints
for j in nodes[1:]:
    problem += lpSum(xij[i, j, k] for i in nodes for k in range(ML)) == 1

for k in range(ML):
    problem += lpSum(xij[i, 'A', k] for i in nodes) == 1
    problem += lpSum(xij['A', j, k] for j in nodes) == 1

for i in nodes[1:]:
    problem += lpSum(xij[i, j, k] for j in nodes for k in range(ML)) == 1



# capacity constraint
for k in range(ML):
    for j in nodes:
        for i in nodes:
            problem+= lpSum(d[j] * xij[i,j,k]) <= capacity

# subtour
# MTZ subtour elimination constraint
for i in nodes[1:]:
    for j in nodes[1:]:
        for k in range(ML):
            if i != j and (i != 'A' and j != 'A') and (i,j,k) in xij:
                problem+= u[i] - u[j] + M*xij[i,j,k] <= M - d[j]
# time window
for k in range(ML):
    for i in nodes[1:]:
        for j in nodes[1:]:
            if i != j:
                problem += s[i] + service_time + tij[i][j] - M * (1 - xij[i, j, k]) <= s[j]

for k in range(ML):
    for i in nodes[1:]:
        problem += t[i][0] - s[i] <= 0

for k in range(ML):
    for i in nodes[1:]:
        problem += s[i] - t[i][0] <= 0


# CONSTRAINT TO TRACK THE VEHICLES AND TO MAKE SURE THE SAME VEHICLE DOES THE ENTIRE ROUTE
for k in range(ML):  
    for i in nodes:
        for j in nodes:
            if i != j:  
                # If i is connected to j by vehicle k, then j must be connected to a subsequent node by the same vehicle
                problem += xij[(i, j, k)] <= lpSum(xij[(i, h, k)] for h in nodes if h != i) 
                problem += xij[(i, j, k)] <= lpSum(xij[(h, j, k)] for h in nodes if h != j)
            else:
                problem += xij[(i, j, k)] == 0  # Ensure that xij[(i, i, k)] is always 0
    
# constraint to ensure each vehicle's route is continuous
for k in range(ML): 
    for i in nodes:
        # Ensure that the sum of outgoing edges from a node equals the sum of incoming edges to that node
        problem += lpSum(xij[(i, j, k)] for j in nodes if j != i) == lpSum(xij[(j, i, k)] for j in nodes if j != i)




#solve the problem
optimal_sol = problem.solve()

# arrival times


for v in problem.variables():  
    if v.varValue == 1.0:
       print(v.name)

# printing code
visited_nodes = []

for v in problem.variables():
    if v.varValue == 1.0:
        current_node = v.name.split("_")[1][-3]
        next_node = v.name.split("_")[2][1]
        visited_nodes.append((current_node, next_node))

# Start with node 'A'
current_node = 'A'
route = [current_node]
route_1 = []
# Construct the route
while True:
    next_node = None
    for connection in visited_nodes:
        if connection[0] == current_node:
            next_node = connection[1]
            visited_nodes.remove(connection)
            route_1.append(next_node)
            break
    if next_node == 'A' or next_node is None:
        route_1.remove('A')
        route.append(next_node)
        break
    route.append(next_node)
    current_node = next_node

#2nd mobile locker

visited_nodes_2 = []

for v in problem.variables():   
    if v.varValue == 1.0:
        current_node = v.name.split("_")[1][-3]
        next_node = v.name.split("_")[2][1]
        visited_nodes_2.append((current_node, next_node))

#print(visited_nodes_2)
# Start with node 'A'
current_node_2 = 'A'
route_2 = [current_node_2]

# Construct the route
while True:
    next_node = None
    for connection_2 in visited_nodes_2:
        #print(connection_2)
        if connection_2[0] == current_node_2 and connection_2[1] not in route_1:
            next_node = connection_2[1]
            visited_nodes_2.remove(connection_2)
            break
    if next_node == 'A' or next_node is None:
        route_2.append(next_node)
        break
    route_2.append(next_node)
    current_node_2 = next_node
    
print('Route 1:', ' -> '.join(route))
print('Route 2:', ' -> '.join(route_2))

print('objective_fun =',value(problem.objective))