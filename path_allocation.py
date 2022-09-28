import gurobipy as gp
from gurobipy import GRB

# Model with just Bandwidth Consraint

# Link and custoemr sets

C = dict({'C1': 1000,
        'C2': 2000,
        'C3': 3000})

L = dict({'L1': 1000,
          'L2': 5000
               })

# Matching score data
combinations, scores = gp.multidict({
    ('L1', 'C1'): 100,
    ('L1', 'C2'): 90,
    ('L1', 'C3'): 80,
    ('L2', 'C1'): 100,
    ('L2', 'C2'): 90,
    ('L2', 'C3'): 80
})

# Declare and initialize model
m = gp.Model('RAP')

customers = C.keys()
links = L.keys()

# Create decision variables for the RAP model
x = m.addVars(combinations, vtype=gp.GRB.BINARY, name="assign")

# CONSTRAINTS
# Create customer constraints - only one link can be assign to each customer
customer_con = m.addConstrs((x.sum('*',c) <= 1 for c in customers), name='customer')

# Customer demand must be satisfied
customer_flow = m.addConstrs((x.sum('*',c) <= C[c] for c in customers), name="customer_demand")

# Create link constraints - more custoemr can be assigned to eack link
link_con = m.addConstrs((x.sum(l,'*') <= 2 for l in links), name='link')

# Link throughput: bandwidth passing through the link to be at most equal the throughput of that link
link_through = m.addConstrs((sum(C[c] * x[l, c] for c in customers) <= L[l] for l in links), name='throughput')

# Objective Function : maximize total matching score of all assignments
m.setObjective(x.prod(scores), GRB.MAXIMIZE)

# Run optimization engine
m.optimize()

# Display optimal values of decision variables
for v in m.getVars():
    if v.x > 1e-6:
        print(v.varName, v.x)

# Display optimal total matching score
print('Total matching score: ', m.objVal)
