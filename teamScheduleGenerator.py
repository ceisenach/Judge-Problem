# Randomly generate team schedules and return a dictionary of these values

import random
from judge import *

def getSeed(population1, population2, k1, k2):
	list1 = random.sample(population1, k1)
	list2 = random.sample(population2, k2)
	if list2[0] > list2[1]:
		list2[0], list2[1] = list2[1], list2[0]
	thelist = list1 + list2
	return tuple(thelist)

def createSeedList(k):
	seedList = []
	for i in range(k) : 
 		newSeed = getSeed([0,1,2,3,4], [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], 1, 2)
 	 	seedList = seedList + [newSeed]
 	return seedList

def createRandomScheduleDictionary(numberOfSeeds) :
	# Create Problem
	teamAssignmentProblem = LpProblem("team_problem",LpMinimize)

	# Add in arbitrary objective function and create LPVariables
	teamAssignmentProblem += 0, "Arbitrary Objective Function"

	T_INDICES = [(k,i,j) for k in range(NUMBER_OF_ROUNDS)
							for i in range(NUMBER_OF_TEAMS) 
							for j in range(NUMBER_OF_TEAMS) 
							if i < j]

	T = LpVariable.dicts("T",T_INDICES,0,1,LpInteger)

	# (1) k_T_ij + k_Til <= k_Tlj + 1, where k is fixed, i<j<l 
	for k in range(NUMBER_OF_ROUNDS):
		for i in range(NUMBER_OF_TEAMS):
			for j in range(i+1,NUMBER_OF_TEAMS):
				for l in range(j+1,NUMBER_OF_TEAMS):
					teamAssignmentProblem += T[(k,i,j)] + T[(k,i,l)] <= T[(k,j,l)] + 1,""
					teamAssignmentProblem += T[(k,i,j)] + T[(k,j,l)] <= T[(k,i,l)] + 1,""
					teamAssignmentProblem += T[(k,j,l)] + T[(k,i,l)] <= T[(k,i,j)] + 1,""

	# (2) Fixing k, sum_{i,j} k_T_ij = 24
	for k in range(NUMBER_OF_ROUNDS):
		teamAssignmentProblem += lpSum(T[(k,i,j)] for i in range(NUMBER_OF_TEAMS)
												  for j in range(NUMBER_OF_TEAMS) if i < j) == 24,""

	# (3) Fixing i,j, \sum_k k_T_ij = 1
	for i in range(NUMBER_OF_TEAMS):
		for j in range(i+1,NUMBER_OF_TEAMS):
			teamAssignmentProblem += lpSum(T[k,i,j] for k in range(NUMBER_OF_ROUNDS)) == 1,""

	# (4) Randomly Seed some of the pairings in the schedule
	seedList = createSeedList(numberOfSeeds)
	for index in seedList :
		teamAssignmentProblem += T[index] == 1

	teamAssignmentProblem.solve(CPLEX_CMD())

	# Here is how pulp lpvars work - the lpproblem assigns each variable a name and the
	# variable name pair is put in a dictionary.  then that name is what it called in the lp
	# file.  then when reading in the solution it has a dict of values to names.
	# then it goes back to the variable dict field of the lpproblem and goes through each name
	# and assigns the variable indexed by that name a value.

	Team = {}

	for k in range(NUMBER_OF_ROUNDS):
		for i in range(NUMBER_OF_TEAMS) : 
			for j in range(i+1,NUMBER_OF_TEAMS) : 
				Team[k,i,j] = T[k,i,j].value()

	return Team,LpStatus[teamAssignmentProblem.status]