# Capacited Mobile locker Routing Problem in Last Mile Delivery

# Background of Problem & Clustering
Last mile delivery is the very last step of the delivery process when a package is moved from a transportation hub to its final destination—which, usually, is a personal residence. Delivering packages to your own houses causes packages to be stolen from porches in major cities such as Philadelphia. Currently, the only option for online package delivery is to your house, or to a stationary pick-up locker where you have to walk to. An alternative solution to this is the mobile package lockers.

**Mobile package lockers**: Mobile package lockers are lockers which moves from one customer location to another customer location based on the demand and time window for that node. 

**How this project works:** 
When a customer orders packages from online, instead of getting it delievered to their house or a stationary locker, they will have an option to get it delievered to their prefferred location at their prefferred time. For example, person A leaves work at 3 PM so person A inputs the work location and the time they are at that location. Then our program will take that location, and time data and create clusters of customers with similar location and overlapping pickup times. Then a mobile locker will be at person A's location at their prefferred time, before it moves to another location to serve other customers. 

**Clustering:**
The first part of this project is clustering, which is grouping together all customers which have close distance and which share the same pick-up time windows. This is done via a math model. After grouping the similar customer orders together, a stopping location is selected for each clusters which is where the mobile locker will be stopped at in order to serve the customers. The yellow dots are the stopping location and the blue dots are the customers. 


![Clustering](https://github.com/DeepuShaji/Senior-Design/assets/93225563/f1502638-fd6d-4db8-8423-006414663397)

# Routing
Routing of the mobile locker is the problem which deals with finding the optimal route for each mobile locker to take from one stopping location (yellow dot in the picture) to another stopping location (yellow dot) so that each locker can get to the nodes within their time windows and without exceeding the capacity of the mobile locker. This is similar to a **Capacited vehicle routing problem with time windows** problem in operations research.

**Key details:**


Capacity of 1 mobile locker: 50 units


Number of mobile lockers: 4

Service time at each node: 45 minutes

Nodes (stopping location): [A,'B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']


Depot: A
Demand at each location:  {'A':0,'B':11,'C':15,'D':12,'E':9,'F':20,'G':17,'H':10,'I':13,'J':8,'K':11,'L':14,'M':19,'N':12,'O':15,'P':12}



Time window of each location: 


A	Depot	


B	6:30-7:30	AM


C	11:30-12:30	AM/PM


D	7:00-8:00	AM


E	8:00-9:00	AM


F	12:00-1	PM


G	1:00-2:00	PM


H	4:30-5:30	PM


I	5:00-6:00	PM


J	9:30-10:30	AM


K	2:30-3:30	PM


L	6:30-7:30	PM


M	7:30-8:30	PM


N	8:30-9:30	PM


O	3:30-4:30	PM


P	10:30-11:30	AM


**Objective:** Minimizing the total travel time of mobile lockers



**Decision variables:** **𝑿_𝒊𝒋𝒌**  - Deciding what route to take [0- trip is not traveled 1- trip is traveled]
I = current location 
J = arrival location 
k = vehicle assigned to the route



𝑼_𝒌– Denotes the position of the node in the sequence of visits by K mobile locker




𝑺_𝒊𝒌 -  Time mobile locker K arrives at node i

The math model for the routing of mobile locker is as such: 
![Screenshot (133)](https://github.com/DeepuShaji/Senior-Design/assets/93225563/8062b75d-ce56-4679-8385-e9d5e810191a)



![Screenshot (134)](https://github.com/DeepuShaji/Senior-Design/assets/93225563/fec939a4-cafe-40f3-8fbd-90e1e3012f0c)

Constraints 1 & 2: Only 1 mobile locker can enter and exit a node 


Constraints 3 & 4: Mobile locker must start and end at the depot A


Constraint 5: Capacity constraint 


Constraint 6 & 7: Miller Tucker Zemlin subtour elimination constraint


Constraint 8 & 9: Time window constraint


Constraint 10: Binary Constraint

# Results: 
The above math model is solved using Pulp solver in Python. The python file which contains the code for the math model is called "SD_VRP" and the csv file which contains the distance matrix of the stopping locations is called "LFT". To run the SD_VRP program, make sure the LFT csv file and SD_VRP python file are in the same folder. 

After solving the model, the objective function is 50 minutes. The routes taken by 4 mobile lockers is as such: 

**Mobile locker 1 route: A -> B -> J -> F -> K -> A**


![Locker1](https://github.com/DeepuShaji/Senior-Design/assets/93225563/91e1c0ff-2686-4261-a97d-aa40096650eb)

**Mobile locker 2 route: A -> D -> P -> I -> N -> A**


![locker2](https://github.com/DeepuShaji/Senior-Design/assets/93225563/12ce14c3-6a42-419f-8872-b7a696515c92)


**Mobile locker 3 route: A -> E -> C -> O -> H -> A**


![locker3](https://github.com/DeepuShaji/Senior-Design/assets/93225563/737dfd38-44ba-4b40-8edd-5d27ed19af52)


**Mobile locker 4 route: : A- > G -> L -> M -> A**


![locker4](https://github.com/DeepuShaji/Senior-Design/assets/93225563/ae9e6e42-22d8-4d5b-9395-b73c35603b0d)

