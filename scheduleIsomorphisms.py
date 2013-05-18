# The goal of this program is to find team schedules which are not isomorphic
# should pickle graphs which it determines are not isomorphic so we can use them
# later, perhaps to improve the number of judges used.

from teamScheduleGenerator import *
import cPickle as pickle
from graph_tool.all import * 
from judge import *

def writeNonIsomorphSchedulesToFile(pickleFileName,schedules) :
	print """	########################################################
	########################################################
	########################################################
	########################################################
	########################################################

	Status: """ + str(len(schedules)) + """ nonisomorphic graphs found so far"
	
	########################################################
	########################################################
	########################################################
	########################################################
	########################################################
	########################################################"""
	
	try:
		os.remove(pickleFileName)
	except: 
		pass

	pickleFile = open(pickleFileName, 'wb')
	pickle.dump(schedules, pickleFile)
	pickleFile.close()

def readNonIsomorphSchedulesFromFile(pickleFileName) : 
	pickleFile = open(pickleFileName, 'rb')
	schedules = pickle.load(pickleFile)
	pickleFile.close()
	return schedules

def createGraphFromTableList(tableList):
	#creating graph with 36 vertices (16 teams + 20 for 5 rounds* 4 tables)
	g = Graph()
	for i in range(36) : g.add_vertex()

	#add edges from teams to tables
	for i in range(NUMBER_OF_ROUNDS) :
		for j in range(NUMBER_OF_TABLES) :
			for team in tableList[i][j] :
				g.add_edge(g.vertex(team),g.vertex(j+16+4*i))

    #add edges between tables in a round
	for i in range(NUMBER_OF_ROUNDS) :
		for t1 in range(NUMBER_OF_TABLES) :
			for t2 in range(NUMBER_OF_TABLES) :
				g.add_edge(g.vertex(16 + 4 * i +t1),g.vertex(16 + 4 * i +t2))

	return g

def checkNewSchedule(schedules,teamSchedule) : 
	newGraph = createGraphFromTableList(createTableListFromDictionary(teamSchedule))
	
	#if schedules is empty
	if len(schedules) == 0 :
		schedules.append((teamSchedule,1))
	
	#otherwise we have to check against all graphs currently in the list
	else : 
		unique = True
		for i,(schedule,count) in enumerate(schedules) :
			if unique : 
				scheduleGraph = createGraphFromTableList(createTableListFromDictionary(schedule))
				if graph_tool.topology.isomorphism(newGraph,scheduleGraph) :
					unique = False
					schedules[i] = (schedule,count + 1)
		if unique : 
			schedules.append((teamSchedule,1))
	
	return schedules

def main(argv) : 
	pickleFileName = ""
	schedules = []
	iterations = 0
	
	#see if an arg for a pickle file was read in
	try:
		pickleFileName = argv[0]
		schedules = readNonIsomorphSchedulesFromFile(pickleFileName)
	except IndexError:
		pickleFileName = "scheduleDictionary.pkl"	

	#indefinitely try to find nonisomorphic schedules
	while True : 
		#find a valid, random schedule
		teamSchedule = {}
		status = ""
		while status != "Optimal" : 
			teamSchedule,status = createRandomScheduleDictionary(7)

		schedules = checkNewSchedule(schedules,teamSchedule)


		#every ten iterations write to file
		iterations = iterations + 1
		if iterations == 15:
			writeNonIsomorphSchedulesToFile(pickleFileName,schedules)
			iterations = 0


if __name__ == "__main__":
   main(sys.argv[1:])
