# A Integer Linear Programming Model using PuLP, a LP modelling interface written in Python
# and used in conjunction with either CPLEX or GLPK, to solve "The Judge Problem"

# --------------- THE JUDGE PROBLEM -----------------
# The judge problem is given as follows: you have a debate tournament among 16
# teams.  In each round, groups of 4 teams compete with each other, each group
# is judged by 3 judges.  The tournament consists of 5 rounds and each team
# plays each other team once.  The assignment of judges to groups of teams is
# subject to the following constraints: a judge may see any individual team at 
# most once and any pair of judges can work together at most twice.

# There are numerous different approaches that we can try to arrive at a solution
# of course there is the traditional brute force approach, but we can also
# try other things such as meet in the middle and optimizations such as
# fixing a given round.  We also want to be able to find the best solution
# on a given schedule.

from pulp import *

#Define Universal Constants
NUMBER_OF_ROUNDS = 5
NUMBER_OF_TEAMS = 16
NUMBER_OF_TABLES = 4

# create 3 dictionaries of LpVariables, one dictionary for each of 
# k_J_ui, k_T_ij, k_Lr_uv - for T variables i < j, for L, u < v.
# Each LpVariable is integer valued and has range {0,1}
# The dictionaries will be indexed by a tuple of the subscripts described above
def createVariableDictionaries(NumTeams,NumJudges,NumRounds,startRound = 0): 
	T_INDICES = [(k,i,j) for k in range(startRound,NumRounds)
						for i in range(NumTeams) 
						for j in range(NumTeams) 
						if i < j]
	J_INDICES = [(k,u,i) for k in range(startRound,NumRounds)
						for u in range(NumJudges) 
						for i in range(NumTeams)]
	L_INDICES = [(k,u,v) for k in range(startRound,NumRounds)
						for u in range(NumJudges) 
						for v in range(NumJudges) 
						if u < v]

	return (LpVariable.dicts("T",T_INDICES,0,1,LpInteger),
			LpVariable.dicts("J",J_INDICES,0,1,LpInteger),
			LpVariable.dicts("L",L_INDICES,0,1,LpInteger))

def createFixedTeamDictionary() : 
	#### FIXED SCHEDULE OF TEAMS - IDEAL SCHEDULE FROM COACH ####
	tables = [[[15,0,5,10],[14,1,4,11],[13,2,7,8],[12,3,6,9]],
			  [[7,9,14,0],[6,8,15,1],[5,11,12,2],[4,10,13,3]],
			  [[11,13,0,6],[10,12,1,7],[9,15,2,4],[8,14,3,5]],
			  [[0,4,8,12],[1,5,9,13],[2,6,10,14],[3,7,11,15]],
			  [[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]]]

	T = {}

	#### Create Dictionary from the list ####
	for k in range(5) : 
		for i in range(16) :
			for j in range(i+1,16) : 
				together = False
				for t in range(4) : 
					if i in tables[k][t] and j in tables[k][t]:
						together = True
				if together :
					T[k,i,j] = 1
				else :
					T[k,i,j] = 0

	return T


#Given a schedule in dictionary form (that is a dict of T variables), assign judges
def runJudgeInstanceGivenFixedSchedule(T,numJudges,numTeams = 16,numRounds = 5) : 
	# Create Problem
	judgeProblem = LpProblem("judge_problem",LpMinimize)

	# Add in arbitrary objective function
	judgeProblem += 0, "Arbitrary Objective Function"

	(_,J,L) = createVariableDictionaries(numTeams,numJudges,numRounds)

	# (1) Fixing u,v \sum_k k_L_uv <= 1
	for u in range(numJudges):
		for v in range(u+1,numJudges):
			judgeProblem += lpSum(L[(k,u,v)] for k in range(numRounds)) <= 1,""

	# (2) Fixing u,v,k,i k_J_ui + k_J_vi <= k_L_uv + 1
	for k in range(numRounds):
		for u in range(numJudges):
			for v in range(u+1,numJudges):
				for i in range(numTeams):
					judgeProblem += J[(k,u,i)] + J[(k,v,i)] <= L[(k,u,v)] + 1,""

	# (3) Fixing u,i \sum_k k_J_ui <= 2
	for u in range(numJudges):
		for i in range(numTeams):
			judgeProblem += lpSum(J[(k,u,i)] for k in range(numRounds)) <= 2,""

	# (4) Fixing k, k_T_ij + k_J_ui <= 1 + k_J_ui
	for k in range(numRounds):
		for i in range(numTeams):
			for j in range(i+1,numTeams):
				for u in range(numJudges):
					if T[k,i,j] == 1 : 
						judgeProblem += J[(k,u,i)] == J[(k,u,j)],""

	# (5) Fixing k,i \sum_u k_J_ui = 3
	for k in range(numRounds):
		for i in range(numTeams):
			judgeProblem += lpSum(J[k,u,i] for u in range(numJudges)) == 3,""

	# (6) Fixing k,u \sum_i k_J_ui <= 4
	for k in range(numRounds):
		for u in range(numJudges):
			judgeProblem += lpSum(J[k,u,i] for i in range(numTeams)) <= 4,""

	# keepFiles = 1 in case want raw sol files
	judgeProblem.solve(CPLEX_CMD(keepFiles=1))

	#check if optimal - if not, do not want to attempt dict creation
	#potential badness?
	if LpStatus[judgeProblem.status] != "Optimal" : 
		return False,None,None

	#otherwise, make the dictionaries
	Judge = {}

	# make variable dicts from LPVariable dicts
	for k in range(NUMBER_OF_ROUNDS):
		for i in range(NUMBER_OF_TEAMS) : 
			for u in range(NUMBER_OF_JUDGES) : 
				Judge[k,u,i] = J[k,u,i].value()

	return True,Judge,T


# CODE TO GENERATE SCHEDULES GIVEN TEAM AND JUDGE VAR DICTS
# ALSO ERROR CHECKING TO ENSURE THE SCHEDULES ARE VALID
def makeTables(Judge,Team):
	roundTables = []

	for k in range(NUMBER_OF_ROUNDS):
		teamSet = range(NUMBER_OF_TEAMS)
		thisRound = []
		while teamSet != [] : 
			tableTeams = []
			tableJudges = []
			firstTeam = teamSet[0]
			tableTeams.append(firstTeam)

			#find judges
			for j in range(NUM_JUDGES) :
				if Judge[k,j,firstTeam] > 0.5 :
					tableJudges.append(j)
			
			#find teams
			for i in teamSet :
				if i < firstTeam :
					if Team[k,i,firstTeam] > 0.5 :
						tableTeams.append(i)
				if i > firstTeam :	
					if Team[k,firstTeam,i] > 0.5 :
						tableTeams.append(i)

			#remove teams in tableTeams from teamSet
			for i in tableTeams:
				teamSet.remove(i)

			#add back to thisRound
			thisRound.append((tableTeams,tableJudges))

		roundTables.append(thisRound)

	return roundTables

def createTableListFromDictionary(Team):
	tableList = []

	for k in range(NUMBER_OF_ROUNDS):
		teamSet = range(NUMBER_OF_TEAMS)
		thisRound = []
		while teamSet != [] : 
			tableTeams = []
			tableJudges = []
			firstTeam = teamSet[0]
			tableTeams.append(firstTeam)
			
			#find teams
			for i in teamSet :
				if i < firstTeam :
					if Team[k,i,firstTeam] > 0.5 :
						tableTeams.append(i)
				if i > firstTeam :	
					if Team[k,firstTeam,i] > 0.5 :
						tableTeams.append(i)

			#remove teams in tableTeams from teamSet
			for i in tableTeams:
				teamSet.remove(i)

			#add back to thisRound
			thisRound.append((tableTeams))

		tableList.append(thisRound)

	return tableList

#checks to make sure teams play the correct number of teams in each round
def checkMatches(Team) : 
	for k in range(NUMBER_OF_ROUNDS) : 
		for i in range(NUMBER_OF_TEAMS) : 
			sum = 0
			for j in range(i+1,NUMBER_OF_TEAMS) : 
				sum = sum + Team[k,i,j]
			for j in range(i) : 
				sum = sum + Team[k,j,i]
			if sum != 3 :
				print "ERR - Team " + str(i) + " plays " + str(sum) + " teams" + " in round " + str(k)

#checks to make sure teams only play together once
def checkTeamPlays(Team) : 
	for i in range(NUMBER_OF_TEAMS) : 
		for j in range(i+1,NUMBER_OF_TEAMS) :
			sum = 0
			for k in range(NUMBER_OF_ROUNDS) : 
				sum = sum + Team[k,i,j]
			if sum != 1 : 
				print "ERR - Team " + str(i) + " plays team " + str(j) + " " + str(sum) + " times"

#checks to make sure judges work together at most once
def checkJudgePairs(Judge,numberOfJudges):
	for u in range(numberOfJudges) :
		for v in range(u + 1,NUM_JUDGES) : 
			sum = 0
			for k in range(NUMBER_OF_ROUNDS) : 
				together = False
				for i in range(NUMBER_OF_TEAMS) : 
					if Judge[k,u,i] == 1 and Judge[k,v,i] == 1 :
						together = True
				if together :
					sum = sum + 1
			if sum > 1 : 
				print "ERR - Judge " + str(u) + " works with " + str(v) + " " + str(sum) + " times"

#checks to make sure a judge does not see a team more than twice
def checkJudgeTeams(Judge):
	for u in range(numberOfJudges) :
		for i in range(NUMBER_OF_TEAMS) : 
			sum = 0
			for k in range(NUMBER_OF_ROUNDS) :  
				if Judge[k,u,i] == 1 :
					sum = sum + 1
			if sum > 2 : 
				print "ERR - Judge " + str(u) + " judges team " + str(i) + " " + str(sum) + " times"