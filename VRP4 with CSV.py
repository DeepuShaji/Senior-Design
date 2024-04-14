# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 11:47:14 2024

@author: deepu
"""



import csv

from pulp import *

#nodes
nodes = ['A','B','C','D','E','F']

tij = {}

with open(r'C:\Users\deepu\OneDrive\Documents\Seniordesign\Test Data.csv', newline = '') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
    
    fieldnames = [key.strip() for key in reader.fieldnames[0].split(',')]
    
    for row in reader:
        From = row['From']
        To = row['To']
        Cost = float(row['Cost'])
        
        if From not in tij:
            tij[From] = {}
        if To not in tij:
            tij[To] = {}
        
        tij[From][To] = Cost
        tij[To][From] = Cost

# demand level
d = {'A':0,'B':10,'C':22,'D':23,'E':13,'F':19}


# time windows
# can just use upper limit
t = {'A':(0,0),
     'B':(580,585),
     'C':(300,305),
     'D':(400,405),# D: 400
     'E':(70,75),
     'F':(406,501)
     }
service_time = 45


#print(t['B'][1])
# capacity of of mobile locker
capacity = 45

# number of vehicles
ML = 2
M = 1000
# decision variables
xij = LpVariable.dicts('x',((i,j,k)for i in nodes for j in nodes for k in range(ML)),0,1,LpBinary)


# subtour elimination decision variable
u = LpVariable.dicts('u',nodes,0,None,LpInteger)

# arrival time
s = LpVariable.dicts('s',nodes,cat=LpContinuous)

# objective function
problem = LpProblem("VRP_with_time_window",LpMinimize)

problem+= lpSum(xij[i,j,k]*tij[i][j] for i in nodes for j in nodes for k in range(ML))



# assign mobile lockers to only one node
for j in nodes[1:]:
        problem+= lpSum(xij[i,j,k]for i in nodes for k in range(ML))== 1

    

# vehicle trip starts from depot A
for k in range(ML):
    problem+= lpSum(xij['A',j,k] for j in nodes) == 1
    problem+= lpSum(xij[i,'A',k] for i in nodes) == 1

# each node is visited only once
for i in nodes[1:]:
    problem+= lpSum(xij[i,j,k] for j in nodes for k in range(ML)) == 1
    
    
# capacity constraint
for k in range(ML):
    for j in nodes:
        for i in nodes:
            print(d[j])
            print(xij[i,j,k])
            problem+= lpSum(d[j] * xij[i,j,k] for i in nodes) <= capacity

             
# MTZ subtour elimination constraint
for i in nodes[1:]:
    for j in nodes[1:]:
        for k in range(ML):
            if i != j and (i != 'A' and j != 'A') and (i,j,k) in xij:
                problem+= u[i] - u[j] + capacity*xij[i,j,k] <= capacity - d[j] 
    

# Time window constraint
for k in range(ML):
    for i in nodes:
        for j in nodes:
            if i != j and (i != 'A' and j != 'A') and (i,j) in tij:
                problem += s[i] + service_time + tij[i][j] - M * (1 - xij[i,j,k]) <= s[j]


for k in range(ML):           
    for i in nodes[1:]:
        problem+= t[i][0] - s[i] <= 0
        
for k in range(ML):  
    for i in nodes[1:]:
        problem+= s[i] - t[i][0] >=0

#solve the problem
optimal_sol = problem.solve()

LpStatus[optimal_sol]


for i in nodes:
    print(s[i].varValue)


# Extract the sequence of visited nodes
visited_nodes = []
for v in problem.variables():  
    if v.varValue == 1.0:
        print(v.name)

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

# Print the route
# Print the route
print(' -> '.join(route))
print(' -> '.join(route_2))


#print(test)
print('objective_fun =',value(problem.objective))

#Vehicle 1- C:300 D: 400 
# Vechile 2- E:70 F: 406 B: 580