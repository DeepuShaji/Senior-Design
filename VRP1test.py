# 1 mobile locker with miller tucker zemlin constraint, and capacity constraint
# capacity of mobile locker is 100, but demand is less than 100 so only 1 mobile locker is used




from pulp import *

#nodes
nodes = ['A','B','C','D','E','F']

# time matrix
tij = {'A':{'A':2000,'B':5,'C':14,'D':9,'E':10,'F':16},
       'B':{'A':5,'B':2000,'C':9,'D':4,'E':5,'F':11},
       'C':{'A':14,'B':9,'C':2000.,'D':3,'E':4,'F':4},
       'D':{'A':9,'B':4,'C':3,'D':2000,'E':1,'F':8},
       'E':{'A':10,'B':5,'C':4,'D':1,'E':2000,'F':8},
       'F':{'A':16,'B':11,'C':4,'D':8,'E':8,'F':200}}
print(tij['B']['A'])

# demand level
d = {'A':0,'B':10,'C':22,'D':23,'E':13,'F':19}

# capacity of of mobile locker
capacity = 100

# number of vehicles
ML = 1

# decision variables
xij = LpVariable.dicts('x',[(i,j)for i in nodes for j in nodes],0,1,cat='Binary')

# subtour elimination
u = LpVariable.dicts('u',nodes,0,capacity,LpInteger)

# objective function
problem = LpProblem("VRP_with_time_window",LpMinimize)

problem+= lpSum([xij[i,j]*tij[i][j] for i in nodes for j in nodes])

# CONSTRAINTS

# assign mobile lockers to only one node
for i in nodes:
    problem+= lpSum(xij[i,j]for j in nodes)==1

for j in nodes:
    problem+= lpSum(xij[i,j]for i in nodes)==1
  
# MTZ subtour elimination constraint
for i in nodes:
    for j in nodes:
        if i != j and (i != 'A' and j != 'A') and (i,j) in xij:
            problem+= u[i] - u[j] + capacity*xij[i,j] <= capacity - d[j] 

# capacity constraint
for i in nodes[1:]:
    problem+= lpSum(d[j]*xij[i,j] for j in nodes) <= capacity

#solve the problem
optimal_sol = problem.solve()

LpStatus[optimal_sol]

for v in problem.variables():
    if v.varValue == 1.0:
        print(v.name,"=",v.varValue)
        #print(v.name-)

print('objective_fun =',value(problem.objective))