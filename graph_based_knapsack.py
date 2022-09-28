# In this example, we generate random data for networkX graph and perform traffic demands to paths allocation as multi-knapsack problem

# Generetae random data for multi-knapsack problem

import random
from random import randrange

def reven(n):
   mydict = {}
   for i in range(n):
     mydict['item_'+str(i)] = randrange(10,100)
   return mydict

def dem(n):
   mydict = {}
   for i in range(n):
     mydict['item_'+str(i)] = randrange(1000,5000)
   return mydict

def cap(n):
   mydict = {}
   for i in range(n):
     mydict['path_'+str(i)] = randrange(1000,5000)
   return mydict

def clas(n):
   mydict = []
   for i in range(n):
        mydict.append('item_'+str(i))
     #mydict['item'+str(i)] = randrange(1000,5000)
   return mydict

def paths(n):
   mydict = []
   for i in range(n):
        mydict.append('path_'+str(i))
     #mydict['path'+str(i)] = randrange(1000,5000)
   return mydict
 
revenue = reven(100)
bw_dem = dem(100)
classes = clas(100)

# capacities and paths count should be equal
capacities = cap(10)
paths = paths(10)

# print("Revenues: ", revenue)
# print("Demands: ", bw_dem)
# print("Capacities: ", capacities)
# print("Classes: ", classes)


# MULTI-KNAPSACK Model with random data

import numpy as np
import pandas as pd

import gurobipy as gp
from gurobipy import GRB
import networkx as nx



# This value above are just exemples
m = gp.Model('ks')



# Insert the decision variables
x = m.addVars(classes, paths, vtype = gp.GRB.BINARY)

# Define the objective function
m.setObjective(gp.quicksum(x[i, j] * revenue[i] for i in classes for j in paths), sense=gp.GRB.MAXIMIZE)

# Constraint 1: satisfy the demand once, assign demand to only one knapsack at most
c1 = m.addConstrs(gp.quicksum(x[i,j] for j in paths) <= 1 for i in classes)

# Constraint 2: respect the path capacity
c2 = m.addConstrs(gp.quicksum(x[i,j] * bw_dem[i] for i in classes) <= capacities[j] for j in capacities)

# Run the model
m.optimize()
m.setParam(GRB.Param.OutputFlag, 0)

# Status checking
status = m.Status
if status in (GRB.INF_OR_UNBD, GRB.INFEASIBLE, GRB.UNBOUNDED):
    print('The model cannot be solved because it is infeasible or '
            'unbounded')
    sys.exit(1)

if status != GRB.OPTIMAL:
    print('Optimization was stopped with status ' + str(status))
    sys.exit(1)
    
# Display optimal values of decision variables
for v in m.getVars():
    if v.x > 1e-6:
        print(v.varName, v.x)

# Display optimal total matching score
print('Total matching score: ', m.objVal)
