# This is to interpret CPLEX sol file
# File is read in as command line argument
# File must be the stripped out variable angle bracketed tags
# Each variable is a binary integer variable, important to note below when summing them

import sys
import string

from judge import *

# splits up constraint and variable lines
# First define global variables
DEFAULT_JUDGES = 20

NUMBER_OF_JUDGES = DEFAULT_JUDGES
FIXED_SCHEDULE = False


def stringToIndex(indexString):
	(i,j,k) = (0,0,0)
	
	# find i
	startIndex = string.find(indexString,'(') + 1
	endIndex = string.find(indexString,',',startIndex)
	i = int(indexString[startIndex:endIndex])

	# find j
	startIndex = string.find(indexString,'_',endIndex) + 1
	endIndex = string.find(indexString,',',startIndex)
	j = int(indexString[startIndex:endIndex])

	# find kpython function overloadpython dictionary check for keying
	startIndex = string.find(indexString,'_',endIndex) + 1
	endIndex = string.find(indexString,')',endIndex)
	k = int(indexString[startIndex:endIndex])

	return (i,j,k)

def makeJudgeVariableDictionaryFromFile(solution):
	Judge = {}

	for line in solution:
		#first find the tuple to index judge
		beginName = string.find(line,'name="') + 6
		endName = string.find(line,'"',beginName)
		name = line[beginName:endName]
		index = stringToIndex(name)

		beginValue = string.find(line,'value="') + 7
		endValue = string.find(line,'"',beginValue)

		value = int(line[beginValue:endValue])

		#now add to proper dictionary
		if name[0] == 'J' :
			Judge[index] = value

		#test if was optimized or not
		if (0,0,0) not in Judge :
			Judge = addJudgePresetsToDictionary(Judge)
	
	return Judge

def makeTeamVariableDictionaryFromFile(solution):
	Team = {}

	for line in solution:
		#first find the tuple to index judge
		beginName = string.find(line,'name="') + 6
		endName = string.find(line,'"',beginName)
		name = line[beginName:endName]
		index = stringToIndex(name)

		beginValue = string.find(line,'value="') + 7
		endValue = string.find(line,'"',beginValue)

		value = int(line[beginValue:endValue])

		if name[0] == 'T' :
			Team[index] = value

		#test if was optimized or not
		if (0,0,1) not in Team :
			Team = addTeamPresetsToTeamDictionary(Team)
	
	return Team	


# Add round 0 presets
def addJudgePresetsToDictionary(Judge) :
	for u in range(NUM_JUDGES) : 
		for i in range(NUMBER_OF_TEAMS) : 
			Judge[(0,u,i)] = 0

	Judge[0,0,0] = 1
	Judge[0,0,1] = 1
	Judge[0,0,2] = 1
	Judge[0,0,3] = 1
	Judge[0,1,0] = 1
	Judge[0,1,1] = 1
	Judge[0,1,2] = 1
	Judge[0,1,3] = 1
	Judge[0,2,0] = 1
	Judge[0,2,1] = 1
	Judge[0,2,2] = 1
	Judge[0,2,3] = 1
	Judge[0,3,4] = 1
	Judge[0,3,5] = 1
	Judge[0,3,6] = 1
	Judge[0,3,7] = 1
	Judge[0,4,4] = 1
	Judge[0,4,5] = 1
	Judge[0,4,6] = 1
	Judge[0,4,7] = 1
	Judge[0,5,4] = 1
	Judge[0,5,5] = 1
	Judge[0,5,6] = 1
	Judge[0,5,7] = 1
	Judge[0,6,8] = 1
	Judge[0,6,9] = 1
	Judge[0,6,10] = 1
	Judge[0,6,11] = 1
	Judge[0,7,8] = 1
	Judge[0,7,9] = 1
	Judge[0,7,10] = 1
	Judge[0,7,11] = 1
	Judge[0,8,8] = 1
	Judge[0,8,9] = 1
	Judge[0,8,10] = 1
	Judge[0,8,11] = 1
	Judge[0,9,12] = 1
	Judge[0,9,13] = 1
	Judge[0,9,14] = 1
	Judge[0,9,15] = 1
	Judge[0,10,12] = 1
	Judge[0,10,13] = 1
	Judge[0,10,14] = 1
	Judge[0,10,15] = 1
	Judge[0,11,12] = 1 
	Judge[0,11,13] = 1
	Judge[0,11,14] = 1
	Judge[0,11,15] = 1

	return Judge

def addTeamPresetsToDictionary(Team) :
	for i in range(NUMBER_OF_TEAMS) :  
		for j in range(NUMBER_OF_TEAMS) :
			if i < j : 
				Team[(0,i,j)] = 0

	Team[0,0,1] = 1
	Team[0,1,2] = 1
	Team[0,1,3] = 1
	Team[0,0,2] = 1
	Team[0,2,3] = 1
	Team[0,0,3] = 1
	Team[0,4,5] = 1
	Team[0,4,6] = 1
	Team[0,4,7] = 1
	Team[0,5,6] = 1
	Team[0,5,7] = 1
	Team[0,6,7] = 1
	Team[0,8,9] = 1
	Team[0,8,10]= 1
	Team[0,8,11]= 1
	Team[0,9,10] = 1
	Team[0,9,11] = 1
	Team[0,10,11] = 1
	Team[0,12,13]= 1
	Team[0,12,14]= 1
	Team[0,12,15]= 1
	Team[0,13,14] = 1
	Team[0,13,15] = 1
	Team[0,14,15] = 1

	return Team

def makeVariableDictionaryFromFile(solution) : 
	if(FIXED_SCHEDULE) : 
		return (makeJudgeVariableDictionaryFromFile(solution),
				createFixedTeamDictionary())
	else : 
		return (makeJudgeVariableDictionaryFromFile(solution),
				makeTeamVariableDictionaryFromFile(solution))


#All other constraints such as number of teams at a table or judges judging at a table if not met
#will appear clearly in the printed schedule

def main(argv):
	global NUMBER_OF_JUDGES
	global FIXED_SCHEDULE

	#open solution file, process argv, quit if used improperly
	try:
		solution = open(argv[0])
		NUMBER_OF_JUDGES = int(argv[1])
	except IndexError:
		print 'SYNTAX ERROR - usage as follows "interpreter.py solution_file num_judges fixed?"' 
		quit()

	try:
		fixed = argv[2]
		if fixed == "fixed" :
			FIXED_SCHEDULE = True
	except IndexError:
		pass

	#make variable dictionaries and check to make sure constraints are actually satisfied in the created solution
	(Judge,Team) = makeVariableDictionaryFromFile(solution)
	checkMatches(Team)
	checkTeamPlays(Team)
	checkJudgePairs(Judge,NUMBER_OF_JUDGES)
	checkJudgeTeams(Judge,NUMBER_OF_JUDGES)

	#generate schedule
	roundTables = makeTables(Judge,Team)

	#print out schedule
	for k in range(NUMBER_OF_ROUNDS):
		thisRound = roundTables[k]
		print "Round Number " + str(k) +" :\n"
		print thisRound
		print "\n"

if __name__ == "__main__":
   main(sys.argv[1:])