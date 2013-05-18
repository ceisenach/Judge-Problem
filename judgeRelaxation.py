# A relaxation of some of the constraints

from pulp import *

#Define Constants
NUMBER_OF_JUDGES = 13
NUMBER_OF_TEAMS = 16
NUMBER_OF_ROUNDS = 5

# Create Problem
judgeProblem = LpProblem("Judge Problem",LpMinimize)

# Add in arbitrary objective function
judgeProblem += 0, "Arbitrary Objective Function"

# Now set up 3 dictionaries of LpVariables, one dictionary for each of 
# k_J_ui, k_T_ij, k_Lr_uv - for T variables i < j, for L, u < v.
# Each LpVariable is integer valued and has range {0,1}
# The dictionaries will be indexed by a tuple of the subscripts described above

T_INDICES = [(k,i,j) for k in range(NUMBER_OF_ROUNDS)
					for i in range(NUMBER_OF_TEAMS) 
					for j in range(NUMBER_OF_TEAMS) 
					if i < j]
J_INDICES = [(k,u,i) for k in range(NUMBER_OF_ROUNDS)
					for u in range(NUMBER_OF_JUDGES) 
					for i in range(NUMBER_OF_TEAMS)]
L_INDICES = [(k,u,v) for k in range(NUMBER_OF_ROUNDS)
					for u in range(NUMBER_OF_JUDGES) 
					for v in range(NUMBER_OF_JUDGES) 
					if u < v]

J = LpVariable.dicts("J",J_INDICES,0,1,LpInteger)
T = LpVariable.dicts("T",T_INDICES,0,1,LpInteger)
L = LpVariable.dicts("L",L_INDICES,0,1,LpInteger)

# (1) k_T_ij + k_Til <= k_Tlj + 1, where k is fixed, i<j<l 
for k in range(NUMBER_OF_ROUNDS):
	for i in range(NUMBER_OF_TEAMS):
		for j in range(i+1,NUMBER_OF_TEAMS):
			for l in range(j+1,NUMBER_OF_TEAMS):
				judgeProblem += T[(k,i,j)] + T[(k,i,l)] <= T[(k,j,l)] + 1,""
				judgeProblem += T[(k,i,j)] + T[(k,j,l)] <= T[(k,i,l)] + 1,""
				judgeProblem += T[(k,j,l)] + T[(k,i,l)] <= T[(k,i,j)] + 1,""

# (2) Fixing u,v \sum_k k_L_uv <= 2
for u in range(NUMBER_OF_JUDGES):
	for v in range(u+1,NUMBER_OF_JUDGES):
		judgeProblem += lpSum(L[(k,u,v)] for k in range(NUMBER_OF_ROUNDS)) <= 2,""

# (3) Fixing u,v,k,i k_J_ui + k_J_vi <= k_L_uv + 1
for k in range(NUMBER_OF_ROUNDS):
	for u in range(NUMBER_OF_JUDGES):
		for v in range(u+1,NUMBER_OF_JUDGES):
			for i in range(NUMBER_OF_TEAMS):
				judgeProblem += J[(k,u,i)] + J[(k,v,i)] <= L[(k,u,v)] + 1,""

# (4) Fixing u,i \sum_k k_J_ui <= 2
for u in range(NUMBER_OF_JUDGES):
	for i in range(NUMBER_OF_TEAMS):
		judgeProblem += lpSum(J[(k,u,i)] for k in range(NUMBER_OF_ROUNDS)) <= 2,""

# (5) Fixing k, k_T_ij + k_J_ui <= 1 + k_J_ui
for k in range(NUMBER_OF_ROUNDS):
	for i in range(NUMBER_OF_TEAMS):
		for j in range(i+1,NUMBER_OF_TEAMS):
			for u in range(NUMBER_OF_JUDGES):
				judgeProblem += T[(k,i,j)] + J[(k,u,i)] <= J[(k,u,j)] + 1,""
				judgeProblem += T[(k,i,j)] + J[(k,u,j)] <= J[(k,u,i)] + 1,""

# (6) Fixing k, sum_{i,j} k_T_ij = 24
for k in range(NUMBER_OF_ROUNDS):
	judgeProblem += lpSum(T[(k,i,j)] for i in range(NUMBER_OF_TEAMS) for j in range(NUMBER_OF_TEAMS) if i < j) == 24,""

# (7) Fixing i,j, \sum_k k_T_ij = 1
for i in range(NUMBER_OF_TEAMS):
	for j in range(i+1,NUMBER_OF_TEAMS):
		judgeProblem += lpSum(T[k,i,j] for k in range(NUMBER_OF_ROUNDS)) == 1,""

# (8) Fixing k,i \sum_u k_J_ui = 3
for k in range(NUMBER_OF_ROUNDS):
	for i in range(NUMBER_OF_TEAMS):
		judgeProblem += lpSum(J[k,u,i] for u in range(NUMBER_OF_JUDGES)) == 3,""

# (9) Fixing k,u \sum_i k_J_ui <= 4
for k in range(NUMBER_OF_ROUNDS):
	for u in range(NUMBER_OF_JUDGES):
		judgeProblem += lpSum(J[k,u,i] for i in range(NUMBER_OF_TEAMS)) <= 4,""

# Having loaded all our constraints and variables, we can solve the problem!
judgeProblem.writeLP("judgeProblem.lp")
judgeProblem.solve(CPLEX_CMD())

print "Status: ",LpStatus[judgeProblem.status]