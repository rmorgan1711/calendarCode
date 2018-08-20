import datetime
import icalendar
from icalendar import Calendar
from pytz import timezone

def getDateInfo(component, field):
    info = []    
    date = component.get(field)

    paramStr = paramsToString(date.params)
    if len(paramStr) > 0:
        info.append(paramStr)
        info.append(str(date.dt))
    else:
        tzStr = "America/Denver"
        mountainTz = timezone(tzStr)
        mt = date.dt.astimezone(mountainTz)
        info.append("TZID=" + tzStr)
        info.append(str(mt))        
    
    return "\t".join(info)


def paramsToString(parameters):
    paramDict = parameters.items()
    params = []
    if len(paramDict) > 0:
        for key, value in paramDict:
            params.append(str(key) + "=" + str(value))
            return ";".join(params)
    else:
        return ""

calPath = '/Users/Bowen/Documents/calendar/calendarCode/Broncos/nfl-broncos_fromWeb.ics'

cal = None
with open(calPath, 'rb') as f:
    cal = Calendar.from_ical(f.read())

lines = []
header = "Params\tDTSTART\tParams\tDTEND\tSUMMARY\tLOCATION"
lines.append(header)
for component in cal.walk():
    if component.name == "VEVENT":
        line = ""
        line += getDateInfo(component, 'dtstart') + "\t"
        line += getDateInfo(component, 'dtend') + "\t"
        line += component.get('summary') + "\t"
        line += component.get('location') + "\t"
        
        lines.append(line)


outPath = '/Users/Bowen/Documents/calendar/calendarCode/Broncos/events.txt'
with open(outPath, 'w') as f:
    for line in lines:
        f.write(line + "\r\n")
