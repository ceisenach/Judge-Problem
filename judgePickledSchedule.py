# We have pickled team schedules from different isomorphism classes.
# What we would like to do is fit judge assignments to them

# Unfortunately all our schedules were isomorphic

import cPickle as pickle
from judge import *

def readNonIsomorphSchedulesFromFile(pickleFileName) : 
	pickleFile = open(pickleFileName, 'rb')
	schedules = pickle.load(pickleFile)
	pickleFile.close()
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

	schedules = readNonIsomorphSchedulesFromFile(pickleFileName)

	for team in schedules : 
		tableList = createTableListFromDictionary(team)
		for k in range(NUMBER_OF_ROUNDS):
			thisRound = tableList[k]
			print "Round Number " + str(k) +" :\n"
			print thisRound
			print "\n"

if __name__ == "__main__":
   main(sys.argv[1:])