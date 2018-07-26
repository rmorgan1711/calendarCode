import string
import icalendar
from icalendar import Calendar

def getDateInfo(component, field):
    info = []    
    date = component.get(field)
    info.append(str(date.dt))
    info.append(paramsToString(date.params))
    return "\t".join(info)


def paramsToString(parameters):
    paramDict = parameters.items()
    params = []
    for key, value in paramDict:
        params.append(str(key) + "=" + str(value))
        return ";".join(params)

def getLocationAndSummary(component):
    location = ""
    summary = component.get('summary')

    printChars = set(string.printable)
    summary = "".join(filter(lambda x: x in printChars, summary)).strip()

    parts = summary.lower().split("@")
    if parts[0].find("colorado rockies") == -1:
        location = "Coors Field|"
        location += "2001 Blake St.|"
        location += "Denver, CO 80205"
    else:
        location = "Away"

    return summary + "\t" + location


calPath = '/Users/Bowen/Documents/calendar/Colorado Rockies.ics'

cal = None
with open(calPath, 'rb') as f:
    cal = Calendar.from_ical(f.read())

lines = []
header = "DTSTART\tParams\tDTEND\tParams\tSUMMARY\tLOCATION"
lines.append(header)
for component in cal.walk():
    if component.name == "VEVENT":
        if component.get('location').find("Watch") == -1:
            continue
        
        line = ""
        line += getDateInfo(component, 'dtstart')
        line += "\t"
        line += getDateInfo(component, 'dtend')
        line += "\t"
        line += getLocationAndSummary(component)
        
        lines.append(line)


outPath = '/Users/Bowen/Documents/calendar/events.txt'
with open(outPath, 'w') as f:
    for line in lines:
        f.write(line + "\r\n")
