from icalendar import Calendar, Event, Alarm
import datetime

import sys
sys.path.append('/Users/Bowen/Documents/calendar/calendarCode/')
import calMethods

def AddByeWeek(cal):
    tzStr = "America/Denver"
    dt = datetime.datetime(2019,11,10,10,0,0)
    event = Event()
    event.add('dtstart', dt, {'TZID':tzStr})
    event.add('dtend', dt, {'TZID':tzStr})

    summary = 'Broncos Bye Week'
    event.add('summary', summary)
    calMethods.addAlarm(event, summary, 1440)    
    calMethods.addAlarm(event, summary, 7200)

    cal.add_component(event)

cal = calMethods.initCalWithPrelims()

dataPath = "/Users/Bowen/Documents/calendar/calendarCode/Broncos/broncos-2019.txt"
lines = []
with open(dataPath) as f:
    f.readline()
    for line in f:
        event = calMethods.eventFromLine(line.strip(), 'Broncos Game', [1440, 7200])
        cal.add_component(event)

AddByeWeek(cal) 

calPath = "/Users/Bowen/Documents/calendar/calendarCode/Broncos/BroncosGames-2019.ics"
with open(calPath, 'wb') as f:
    f.write(cal.to_ical())
