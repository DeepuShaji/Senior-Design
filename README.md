# Routing of Last Mile Delivery Mobile Lockers

Last mile delivery is the very last step of the delivery process when a package is moved from a transportation hub to its final destination—which, usually, is a personal residence. Delivering packages to your own houses causes packages to be stolen from porches in major cities such as Philadelphia. Currently, the only option for online package delivery is to your house, or to a stationary pick-up locker where you have to walk to. An alternative solution to this is the mobile package lockers.

**Mobile package lockers**: Mobile package lockers are lockers which moves from one customer location to another customer location based on the demand and time window for that node. 

**How this project works:** 
When a customer orders packages from online, instead of getting it delievered to their house or a stationary locker, they will have an option to get it delievered to their prefferred location at their prefferred time. For example, person A leaves work at 3 PM so person A inputs the work location and the time they are at that location. Then our program will take that location, and time data and create clusters of customers with similar location and overlapping pickup times. Then a mobile locker will be at person A's location at their prefferred time, before it moves to another location to serve other customers. 

**Clustering:**
The first part of this project is clustering, which is grouping together all customers which have close distance and which share the same pick-up time windows. This is done via a math model. After grouping the similar customer orders together, a stopping location is selected for each clusters which is where the mobile locker will be stopped at in order to serve the customers. The yellow dots are the stopping location and the blue dots are the customers. 


