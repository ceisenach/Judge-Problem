#check if coaches schedule is in the isomorph eq class we found

from scheduleIsomorphisms import *
from judge import *

idealSchedule = createFixedTeamDictionary()
foundSchedulesList = readNonIsomorphSchedulesFromFile("scheduleDictionary.pkl")

foundSchedule = foundSchedulesList[0][0]

idealScheduleGraph = createGraphFromTableList(createTableListFromDictionary(idealSchedule))
foundScheduleGraph = createGraphFromTableList(createTableListFromDictionary(idealSchedule))

print graph_tool.topology.isomorphism(idealScheduleGraph,foundScheduleGraph)