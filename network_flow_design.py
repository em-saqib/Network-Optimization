import numpy as np
import pandas as pd

import gurobipy as gp
from gurobipy import GRB
import networkx as nx

G = nx.Graph()

graph = {}

graph["S1"] = {}
graph["S2"] = {} 
graph["S3"] = {}
graph["S"] = {}
graph["A"] = {} 
graph["B"] = {}
graph["D1"] = {} 
graph["D2"] = {}
graph["D3"] = {}
graph["S1"] ["S"] = 1000 
graph["S2"] ["S"] = 2000 
graph["S3"] ["S"] = 3000 
graph["S"] ["A"] = 1000 
graph["S"] ["B"] = 5000 
graph["A"] ["D1"] = 1000 
graph["A"] ["D2"] = 2000 
graph["A"] ["D3"] = 3000 
graph["B"] ["D1"] = 1000 
graph["B"] ["D2"] = 2000 
graph["B"] ["D3"] = 3000 

# Next steps
# 1. Find all paths between S and D
# 2. Sort paths and assign demand

# graph = {
#  'S1':{'S': 100} ,
#  'S2':{'S': 200} ,
#  'S3':{'S': 300} ,
#  'S':{'A': 100, 'B': 500} ,
#  'A':{'D1': 100, 'D2': 20, 'D3': 30} ,
#  'B':{'D1': 10, 'D2': 200, 'D3': 300}
# }

# Create edges with capacity
link = {}
for k, v in graph.items():
    #print(k,v)
    for i in v:
        #print(k, i)
        link[k, i] = v[i]
        #print(v[i])
        
link
lst = list(link.keys())
lst2 = list(link.items())

# Create dictionaries to capture factory supply limits, depot throughput limits, and customer demand.

source = dict({'S1': 1000,
              'S2': 2000,
              'S3': 3000
              })

# nd = ['S1', 'S2', 'S3', 'S', 'A', 'B', 'D1', 'D2', 'D3']

node = dict({'S': 6000,
                'A': 1000,
                'B': 5000
               })

destination = dict({'D1': 1000,
               'D2': 2000,
               'D3': 3000
              })



arcs, cost = gp.multidict({
#     lst[0][0]: 1,
#     lst[1][0]: 2,
#     lst[2][0]: 3,
    
#     lst[3][0]: 1,
#     lst[4][0]: 5,

#     lst[5][0]: 1,
#     lst[6][0]: 2,
#     lst[7][0]: 3,
    
#     lst[8][0]: 1,
#     lst[9][0]: 2,
#     lst[10][0]: 3 
    
    lst[0]: 5,
    lst[1]: 4,
    lst[2]: 3,
    
    lst[3]: 5,
    lst[4]: 5,

    lst[5]: 10,
    lst[6]: 2,
    lst[7]: 3,
    
    lst[8]: 1,
    lst[9]: 2,
    lst[10]: 3 

})

model = gp.Model('SupplyNetworkDesign')
flow = model.addVars(arcs, name="flow")

# data generation limits from sources 
sources = source.keys()
source_flow = model.addConstrs((gp.quicksum(flow.select(s, '*')) <= source[s]
                                 for s in sources), name="source")

# link assignment limit 
sources = source.keys()
source_flow = model.addConstrs((gp.quicksum(flow.select(s, '*')) >= 1000
                                 for s in sources), name="source")

# data must be delivered to destinations (demands)
destinations = destination.keys()
customer_flow = model.addConstrs((gp.quicksum(flow.select('*', d)) == destination[d]
                                  for d in destinations), name="destination")

# Depot flow conservation
nodes = node.keys()
node_flow = model.addConstrs((gp.quicksum(flow.select(n, '*')) == gp.quicksum(flow.select('*', n))
                              for n in nodes), name="depot")

# Node throughput
node_capacity = model.addConstrs((gp.quicksum(flow.select('*', n)) <= node[n]
                                for n in nodes), name="n_capacity")

# Objective: maximize total matching score of all assignments
model.setObjective(flow.prod(cost), GRB.MAXIMIZE)

model.optimize()


# Display optimal values of decision variables
for v in model.getVars():
    if v.x > 1e-6:
        print(v.varName, v.x)

# Display optimal total matching score
print('Total matching score: ', model.objVal)
