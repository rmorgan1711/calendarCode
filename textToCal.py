import sys
sys.path.append('/Users/Bowen/Documents/calendar/calendarCode/')
import calMethods

cal = calMethods.initCalWithPrelims()

workingDir = '/Users/Bowen/Documents/calendar/calendarCode/Rockies/'
dataPath = workingDir + "rockiesHomeGames2019.txt"
lines = []
with open(dataPath) as f:
    f.readline()
    for line in f:
        if line.find("Away") > -1:
            continue

        event = calMethods.eventFromLine(line.strip(), 'Rockies Home Game at', [180])
        # event = EventFromLine(line.strip())
        cal.add_component(event)
    

calPath = workingDir + 'RockiesHomeGames-2019.ics'
with open(calPath, 'wb') as f:
    f.write(cal.to_ical())
