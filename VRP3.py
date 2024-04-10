# 1 mobile locker with miller tucker zemlin constraint, and capacity constraint
# Time windows are implemented with 1 mobile locker
# Multiple vehicles
# test

from pulp import *

#nodes
nodes = ['A','B','C','D','E','F']

# time matrix
tij = {'A':{'A':2000,'B':5,'C':14,'D':9,'E':10,'F':16},
       'B':{'A':5,'B':2000,'C':9,'D':4,'E':5,'F':11},
       'C':{'A':14,'B':9,'C':2000.,'D':3,'E':4,'F':4},
       'D':{'A':9,'B':4,'C':3,'D':2000,'E':1,'F':8},
       'E':{'A':10,'B':5,'C':4,'D':1,'E':2000,'F':8},
       'F':{'A':16,'B':11,'C':4,'D':8,'E':8,'F':2000}}
#print(tij['B']['A'])


# demand level
d = {'A':0,'B':10,'C':22,'D':23,'E':13,'F':19}

# time windows
# can just use upper limit
t = {'A':(0,0),
     'B':(580,585),
     'C':(580,585),
     'D':(400,405),
     'E':(70,75),
     'F':(400,405)
     }
service_time = 45


#print(t['B'][1])
# capacity of of mobile locker
capacity = 1000

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


  
# ensure each node with same time windows are not visisted
for i in nodes[1:]:
    for j in nodes[1:]:
        if t[i] == t[j] and i != j:
            for k in range(ML):
                problem+= xij[i,j,k] + xij[j,i,k]<= 1


             
# MTZ subtour elimination constraint
for i in nodes[1:]:
    for j in nodes[1:]:
        for k in range(ML):
            if i != j and (i != 'A' and j != 'A') and (i,j,k) in xij:
                problem+= u[i] - u[j] + capacity*xij[i,j,k] <= capacity - d[j] 
    
# time window constraint
for k in range(ML):
    for i in nodes[1:]:
        for j in nodes[1:]:
            if i != j:
                problem+=  s[i]+ service_time + tij[i][j]- M*(1-xij[i,j,k]) <= s[j]
           # service time added to left hand side

for k in range(ML):           
    for i in nodes[1:]:
        problem+= t[i][0] - s[i]<= 0
        
for k in range(ML):  
    for i in nodes[1:]:
        problem+= s[i] - t[i][0]<=0
            
#solve the problem
optimal_sol = problem.solve()

LpStatus[optimal_sol]




# printing code

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

# Construct the route
while True:
    next_node = None
    for connection in visited_nodes:
        if connection[0] == current_node:
            next_node = connection[1]
            visited_nodes.remove(connection)
            break
    if next_node == 'A' or next_node is None:
        route.append(next_node)
        break
    route.append(next_node)
    current_node = next_node



# Print the route
print(' -> '.join(route))



#print(test)
print('objective_fun =',value(problem.objective))