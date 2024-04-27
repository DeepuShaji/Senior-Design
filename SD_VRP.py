# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 14:02:45 2024

@author: deepu
"""
# Mobile locker routing code for Senior Design
# CSV file contains stopping nodes for Temple neighborhood

import csv
from pulp import *
from collections import defaultdict

#nodes
nodes = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']

3
# time matrix
tij = {}


with open(r'C:\Users\deepu\OneDrive\Documents\Seniordesign\LFT.csv', newline='') as csvfile:
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
d = {'A':0,'B':11,'C':15,'D':12,'E':9,'F':20,'G':17,'H':10,'I':13,'J':8,'K':11,'L':14,'M':19,'N':12,'O':15,'P':12}

# time windows
t = {'A':(0,0),
     'B':(25,30),
     'C':(325,330),
     'D':(55,60),  #'C':(90,210) 12,'D':(240,360),9
     'E':(115,120),
     'F':(355,360),
     'G':(415,420),
     'H':(625,630),
     'I':(655,660),
     'J':(205,210),
     'K':(505,510),
     'L':(745,750),
     'M':(805,810),
     'N':(865,870),
     'O':(565,570),
     'P':(265,270),
     }
service_time = 45

# capacity of mobile locker
capacity = 50

# number of vehicles
ML = 4
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

# Constraint 1
for j in nodes[1:]:
    problem += lpSum(xij[i, j, k] for i in nodes for k in range(ML)) == 1

# Constraint saying a trip must start and end at depot A
for k in range(ML):
    problem += lpSum(xij[i, 'A', k] for i in nodes) == 1
    problem += lpSum(xij['A', j, k] for j in nodes) == 1

# constraint 2
for i in nodes[1:]:
    problem += lpSum(xij[i, j, k] for j in nodes for k in range(ML)) == 1



# capacity constraint
for k in range(ML):
            problem+= lpSum(d[j] * xij[i,j,k] for i in nodes for j in nodes) <= capacity

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


for v in problem.variables():  
    if v.varValue == 1.0:
       print(v.name)
       
# arrival times
print('Arrival time at each nodes (In order of A to F):')
for i in nodes:
    print(s[i].varValue)

print('objective_fun =',value(problem.objective))