# The approach used here will be to solve the problem given NUMBER_OF_JUDGES judges
# does there exist an assignment of judges and groups of teams to matches such that
# the constraints described above are satisfied.  Here we start with a preffered
# table assignment

from judge import *

#Define Constants
NUMBER_OF_JUDGES = 14

T = createFixedTeamDictionary()

runJudgeInstanceGivenFixedSchedule(T,NUMBER_OF_JUDGES)