# This is to interpret CPLEX sol file
# File is read in as command line argument
# File must be the stripped out variable angle bracketed tags
# Each variable is a binary integer variable, important to note below when summing them

import sys
import string

# splits up constraint and variable lines
# First define global variables
DEFAULT_JUDGES = 20


NUM_ROUNDS = 5
NUM_JUDGES = DEFAULT_JUDGES
NUM_TABLES = 4

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

	# find k
	startIndex = string.find(indexString,'_',endIndex) + 1
	endIndex = string.find(indexString,')',endIndex)
	k = int(indexString[startIndex:endIndex])

	return (i,j,k)

def makeVariableDictionaryFromFile(solution):
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

	return Judge

def makeTables(Judge):
	#TODO MAKE ERROR CHECKING!!!!!!!!!!!!!!!!!!!!!!
	roundTables = []

	for k in range(NUM_ROUNDS):
		thisRound = []
		for t in range(NUM_TABLES): 
			tableJudges = []

			#find judges
			for j in range(NUM_JUDGES) :
				if Judge[k,j,t] == 1 :
					tableJudges.append(j)

			#add back to thisRound
			thisRound.append(tableJudges)

		roundTables.append(thisRound)

	return roundTables

#checks to make sure judges work together at most once
def checkJudgePairs(Judge):
	for u in range(NUM_JUDGES) :
		for v in range(u + 1,NUM_JUDGES) : 
			sum = 0
			for k in range(NUM_ROUNDS) : 
				together = False
				for t in range(NUM_TABLES) : 
					if Judge[k,u,t] == 1 and Judge[k,v,t] == 1 :
						together = True
				if together :
					sum = sum + 1
			if sum > 1 : 
				print "ERR - Judge " + str(u) + " works with " + str(v) + " " + str(sum) + " times"

def main(argv):
	global NUM_JUDGES

	#open solution file, process argv, quit if used improperly
	try:
		solution = open(argv[0])
		NUM_JUDGES = int(argv[1])
	except IndexError:
		print 'SYNTAX ERROR - usage as follows "judgeScheduleInterpreter.py solution_file num_judges"' 
		quit()

	#make variable dictionaries and check to make sure constraints are actually satisfied in the created solution
	Judge = makeVariableDictionaryFromFile(solution)
	checkJudgePairs(Judge)

	#generate schedule
	roundTables = makeTables(Judge)

	#print out schedule
	for k in range(NUM_ROUNDS):
		thisRound = roundTables[k]
		print "Round Number " + str(k) +" :\n"
		print thisRound
		print "\n"

if __name__ == "__main__":
   main(sys.argv[1:])