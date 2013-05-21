# Take the schedules we found, rank them, and print the top 3

import cPickle as pickle
from judge import *
from operator import itemgetter

#low rankings are best
def checkAndInsert(topThree,newSchedule,ranking) :
	topThree.append((newSchedule,ranking))
	sortedFour = sorted(topThree, key = itemgetter(1))
	return sortedFour[:3]

def rankAccordingToFairMetric(schedule) :
	ranks = []
	for k in range(NUMBER_OF_ROUNDS) : 
		for t in range(NUMBER_OF_TABLES) :
			ranks.append(sum(schedule[k][t]))
	return sum((x-30)**2 for x in ranks) / 20

def rankAccordingToExcitingMetric(schedule) :
	teamScores = [0]*16
	for k in range(NUMBER_OF_ROUNDS) :
		for t in range(NUMBER_OF_TABLES) :
			results = sorted(schedule[k][t])
			teamScores[results[0]] = teamScores[results[0]] + 5
			teamScores[results[1]] = teamScores[results[1]] + 3
			teamScores[results[2]] = teamScores[results[2]] + 1
	return sum((x-11.25)**2 for x in teamScores) / 16

def topThreeAccordingToMetric(schedules,metric) :
	topThree = [([],sys.maxint),([],sys.maxint),([],sys.maxint)]
	for s in schedules :
		ranking = metric(s)
		topThree = checkAndInsert(topThree,s,ranking)
	return topThree

def lowestAccordingToMetric(schedules,metric) :
	lowest = sys.maxint
	for s in schedules :
		srank = metric(s)
		if srank < lowest :
			lowest = srank
	return lowest

def highestAccordingToMetric(schedules,metric) :
	highest = -sys.maxint-1
	for s in schedules :
		srank = metric(s)
		if srank > highest :
			highest = srank
	return highest

def printSchedule(schedule) :
	for k,thisRound in enumerate(schedule):
		print "Round Number " + str(k) +" :\n"
		print thisRound
		print "\n"

def main(argv) : 
	pickleFileName = ""
	
	#see if an arg for a pickle file was read in
	try:
		pickleFileName = argv[0]
	except IndexError:
		pickleFileName = "scheduleDictionary.pkl"	

	# first entry is isomorphisms - ignore it
	pickleFile = open(pickleFileName, 'rb')
	schedules = pickle.load(pickleFile)[1]
	pickleFile.close()

	excitingTopThree = topThreeAccordingToMetric(schedules,rankAccordingToExcitingMetric)
	fairTopThree = topThreeAccordingToMetric(schedules,rankAccordingToFairMetric)

	#print out the top three with their ranking
	for i,(schedule,rank) in enumerate(excitingTopThree) :
		print "Exciting Schedule " + str(i) + " with rank " + str(rank) + " and rank " + str(rankAccordingToFairMetric(schedule)) + " according to the fair metric \n"
		printSchedule(schedule)
	for i,(schedule,rank) in enumerate(fairTopThree) :
		print "Fair Schedule " + str(i) + " with rank " + str(rank) + " and rank " + str(rankAccordingToExcitingMetric(schedule)) + " according to the exciting metric \n"
		printSchedule(schedule)

	#print max and min
	print "Highest according to exciting metric " + str(highestAccordingToMetric(schedules,rankAccordingToExcitingMetric))
	print "And lowest " + str(lowestAccordingToMetric(schedules,rankAccordingToExcitingMetric))
	print "Highest according to fair metric " + str(highestAccordingToMetric(schedules,rankAccordingToFairMetric))
	print "And lowest " + str(lowestAccordingToMetric(schedules,rankAccordingToFairMetric))

if __name__ == "__main__":
   main(sys.argv[1:])