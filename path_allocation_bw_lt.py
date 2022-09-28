import gurobipy as gp
from gurobipy import GRB

# Model with bandwidth and latency constraints

# demands from customers
C, dr, lt = gp.multidict( {
    'C1': ([1000, 9]),
    'C2': ([2000, 4]),
    'C3': ([3000, 3]),
    'C4': ([4000, 2]),
    'C5': ([5000, 2]) 
} )

# capacities of links
P, bw, pd = gp.multidict( {
    'P1': ([1000, 7]),
    'P2': ([6000, 2]),
    'P3': ([8000, 1])
})

customers = dr.keys()
paths = pd.keys()

# Matching score data

combinations, scores = gp.multidict({
    ('P1', 'C1'): 100,
    ('P1', 'C2'): 70,
    ('P1', 'C3'): 50,
    ('P1', 'C4'): 40,
    ('P1', 'C5'): 35,
    ('P2', 'C1'): 100,
    ('P2', 'C2'): 70,
    ('P2', 'C3'): 50,
    ('P2', 'C4'): 40,
    ('P2', 'C5'): 35,
    ('P3', 'C1'): 100,
    ('P3', 'C2'): 70,
    ('P3', 'C3'): 50,
    ('P3', 'C4'): 40,
    ('P3', 'C5'): 35,
})

# Declare and initialize model
m = gp.Model('RAP')

# Create decision variables for the RAP model
x = m.addVars(combinations, vtype=gp.GRB.BINARY, name="assign")

# Create customer constraints - only one link can be assign to each customer
customer_con = m.addConstrs((x.sum('*',c) <= 1 for c in customers), name='customer')

# Create link constraints - more custoemr can be assigned to eack link
path_con = m.addConstrs((x.sum(p,'*') <= 5 for p in paths), name='path')

# Link throughput: bandwidth passing through the link to be at most equal the throughput of that link
path_through = m.addConstrs((sum(dr[c] * x[p, c] for c in customers) <= bw[p] for p in paths), name='throughput')

# Link latency constraint
path_through = m.addConstrs((pd[p] * x[p, c] <= lt[c] for p in paths for c in customers), name='throughput')

# Objective: maximize total matching score of all assignments
m.setObjective(x.prod(scores), GRB.MAXIMIZE)

# Run optimization engine
m.optimize()

# Display optimal values of decision variables
for v in m.getVars():
    if v.x > 1e-6:
        print(v.varName, v.x)

# Display optimal total matching score
print('Total matching score: ', m.objVal)
