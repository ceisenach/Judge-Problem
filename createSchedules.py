# The goal of this program is to find many team schedules so that then we can rank them
# according to our metric.  Just in case it also will track isomorphism classes though
# we expect there to only be one

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

	Status: """ + str(len(schedules[0])) + """ nonisomorphic graphs found so far
	Status: """ + str(len(schedules[1])) + """ unique schedules found so far
	
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

def checkNewSchedule(schedules,teamSchedule,count) : 
	#first handle isomorphism
	tableList = createTableListFromDictionary(teamSchedule)
	newGraph = createGraphFromTableList(tableList)
	
	#if schedules is empty
	if not schedules[0]:
		schedules[0] = [(teamSchedule,1)]
	
	#otherwise we have to check against all graphs currently in the list
	else : 
		unique = True 
		for i,(schedule,count) in enumerate(schedules[0]) :
			if unique : 
				scheduleGraph = createGraphFromTableList(createTableListFromDictionary(schedule))
				if graph_tool.topology.isomorphism(newGraph,scheduleGraph) :
					unique = False
					schedules[0][i] = (schedule,count + 1)
		if unique : 
			schedules[0].append((teamSchedule,1))
	
	#second deal with uniqueness
	if not schedules[1] :
		schedules[1] = [tableList]
	else:
		unique = True
		for i in range(len(schedules[1])) :
			if unique : 
				if schedules[1][i] == tableList : 
					unique = False
		if unique :
			count = count + 1
			schedules[1].append(tableList)

	return schedules,count

def main(argv) : 
	pickleFileName = ""
	schedules = [[],[]]
	count = 0
	iterations = 0
	
	#see if an arg for a pickle file was read in
	try:
		pickleFileName = argv[0]
		schedules = readNonIsomorphSchedulesFromFile(pickleFileName)
	except IndexError:
		pickleFileName = "scheduleDictionary.pkl"	

	#generate 3000 unique schedules, 
	while not schedules[1] or len(schedules[1]) < 3000 : 
		#find a valid, random schedule
		teamSchedule = {}
		status = ""
		while status != "Optimal" : 
			teamSchedule,status = createRandomScheduleDictionary(7)

		schedules,count = checkNewSchedule(schedules,teamSchedule,count)

		#every ten iterations write to file
		iterations = iterations + 1
		if iterations == 10:
			writeNonIsomorphSchedulesToFile(pickleFileName,schedules)
			iterations = 0


if __name__ == "__main__":
   main(sys.argv[1:])
