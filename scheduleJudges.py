# A Integer Linear Programming Model using PuLP, a LP modelling interface written in Python
# and used in conjunction with either CPLEX or GLPK, to solve "The Judge Scheduling Problem"

# --------------- THE JUDGE SCHEDULING PROBLEM -----------------
# The judge problem is given as follows: can you assign X judges to 4 tables over 5 rounds such
# that there are three judges per table and no two judges work together more than once

from pulp import *

#Define Constants
NUMBER_OF_JUDGES = 12
NUMBER_OF_ROUNDS = 5
NUMBER_OF_TABLES = 4

# Create Problem
judgeScheduler = LpProblem("judge_scheduler",LpMinimize)

# Add in arbitrary objective function
judgeScheduler += 0, "Arbitrary Objective Function"

J_INDICES = [(k,u,i) for k in range(NUMBER_OF_ROUNDS)
					for u in range(NUMBER_OF_JUDGES) 
					for i in range(NUMBER_OF_TABLES)]
L_INDICES = [(k,u,v) for k in range(NUMBER_OF_ROUNDS)
					for u in range(NUMBER_OF_JUDGES) 
					for v in range(NUMBER_OF_JUDGES) 
					if u < v]

J = LpVariable.dicts("J",J_INDICES,0,1,LpInteger)
L = LpVariable.dicts("L",L_INDICES,0,1,LpInteger)

# (1) Fixing u,v \sum_k k_L_uv <= 1
for u in range(NUMBER_OF_JUDGES):
	for v in range(u+1,NUMBER_OF_JUDGES):
		judgeScheduler += lpSum(L[(k,u,v)] for k in range(NUMBER_OF_ROUNDS)) <= 1,""

# (2) Fixing u,v,k,t k_J_ut + k_J_vt <= k_L_uv + 1
for k in range(NUMBER_OF_ROUNDS):
	for u in range(NUMBER_OF_JUDGES):
		for v in range(u+1,NUMBER_OF_JUDGES):
			for t in range(NUMBER_OF_TABLES):
				judgeScheduler += J[(k,u,t)] + J[(k,v,t)] <= L[(k,u,v)] + 1,""

# (3) Fixing k,t \sum_u k_J_ut = 3
for k in range(NUMBER_OF_ROUNDS):
	for t in range(NUMBER_OF_TABLES):
		judgeScheduler += lpSum(J[k,u,t] for u in range(NUMBER_OF_JUDGES)) == 3,""

# (4) Fixing k,u \sum_i k_J_ui <= 1
for k in range(NUMBER_OF_ROUNDS):
	for u in range(NUMBER_OF_JUDGES):
		judgeScheduler += lpSum(J[k,u,i] for i in range(NUMBER_OF_TABLES)) <= 1,""

# Having loaded all our constraints and variables, we can solve the problem!
# keepFiles = 1 necessary because for some reason parsing solutions back in 
# doesnt quite work right in PuLP, so we will keep files and use our own interpreter
#judgeProblem.writeLP("judgeProblem.lp")
judgeScheduler.solve(CPLEX_CMD(keepFiles=1)) 

print "Status: ",LpStatus[judgeScheduler.status]