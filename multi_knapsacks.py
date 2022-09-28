import numpy as np
import pandas as pd

import gurobipy as gp
from gurobipy import GRB
import networkx as nx

revenue = {'item_1': 50, 'item_2': 10, 'item_3': 30, 'item_4': 40, 'item_5': 50} 
bw_dem = {'item_1': 1000, 'item_2': 2000, 'item_3': 3000, 'item_4': 4000, 'item_5': 5000} 
capacities = {'path_1': 1000, 'path_2': 6000, 'path_3': 8000}

classes = ['item_1', 'item_2', 'item_3', 'item_4', 'item_5']
paths = ['path_1', 'path_2', 'path_3']

# This value above are just exemples
m = gp.Model('ks')



# Insert the decision variables
x = m.addVars(classes, paths, vtype = gp.GRB.BINARY)

# Define the objective function
m.setObjective(gp.quicksum(x[i, j] * revenue[i] for i in classes for j in paths), sense=gp.GRB.MAXIMIZE)

# Constraint 1: satisfy the demand once, assign demand to only one knapsack at most
c1 = m.addConstrs(gp.quicksum(x[i,j] for j in paths) <= 1 for i in classes)

# Constraint 2: respect the path capacity
c2 = m.addConstrs(gp.quicksum(x[i,j] * bw_dem[i] for i in classes) <= capacities[j] for j in knapsacks)

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
