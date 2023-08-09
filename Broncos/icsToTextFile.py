import datetime
import icalendar
from icalendar import Calendar
from pytz import timezone

import sys
sys.path.append('/Users/Bowen/Documents/calendar/calendarCode/')
import calMethods

def formatSummary(summaryComponent):
    summaryParts = summaryComponent.split()

    if summaryParts[1] == "at":
        summaryParts[1] = "@"
    else:
        tmp = summaryParts[0]
        summaryParts[0] = summaryParts[2]
        summaryParts[1] = "@"
        summaryParts[2] = tmp
        
    
    return ' '.join(summaryParts)

workingDir = '/Users/Bowen/Documents/calendar/calendarCode/Broncos/'
calPath = 'nfl-broncos-2019.ics'

cal = None
with open(calPath, 'rb') as f:
    cal = Calendar.from_ical(f.read())

lines = []
header = "DTSTART\tParams\tDTEND\tParams\tSUMMARY\tLOCATION"
lines.append(header)
for component in cal.walk():
    if component.name == "VEVENT":
        line = ""
        line += calMethods.getDateInfo(component, 'dtstart') + "\t"
        line += calMethods.getDateInfo(component, 'dtend') + "\t"
        line += formatSummary(component.get('summary')) + "\t"
        line += component.get('location') + "\t"
        
        lines.append(line)


outPath = workingDir + 'broncos-2019.txt'
with open(outPath, 'w') as f:
    for line in lines:
        f.write(line + "\r\n")
