import icalendar
import datetime
import pytz

from icalendar import Calendar, Event, Alarm
from dateutil import parser
from pytz import timezone

def delimitedFileToDictList(path, sep=','):
    eventDicts = []
    with open(path) as f:
        headings = f.readline().split(sep)
        for line in f:
            fields = line.split(sep)
            event = {headings[i]: fields[i] for i in range(len(headings))}
            eventDicts.append(event)
    
    return eventDicts
            
def listOfListsToFile(path, listOfLists):
    with open(path, 'w') as f:
        for row in listOfLists:
            text = [str(e) for e in row]
            text = '\t'.join(text) + '\r\n'
            f.write(text)

def initCalWithPrelims():
    cal = Calendar()
    cal.add('prodid', '-//CalPy')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')

    tzd = icalendar.TimezoneDaylight()
    tzd.add('rrule', {'freq': 'yearly', 'bymonth': 3, 'byday': '2su'})
    tzd.add('dtstart', datetime.datetime(2007, 3, 11, 2, 0, 0))
    tzd.add('tzname', 'MDT')
    tzd.add('TZOFFSETFROM', datetime.timedelta(hours=-7))
    tzd.add('TZOFFSETTO', datetime.timedelta(hours=-6))

    tzs = icalendar.TimezoneStandard()
    tzs.add('rrule', {'freq': 'yearly', 'bymonth': 11, 'byday': '1su'})
    tzs.add('dtstart', datetime.datetime(2007, 11, 4, 2, 0, 0))
    tzs.add('tzname', 'MST')
    tzs.add('TZOFFSETFROM', datetime.timedelta(hours=-6))
    tzs.add('TZOFFSETTO', datetime.timedelta(hours=-7))

    tzc = icalendar.Timezone()
    tzc.add('tzid', 'America/Denver')
    tzc.add_component(tzd)
    tzc.add_component(tzs)

    cal.add_component(tzc)

    return cal

def getParamDict(field):
    pairs = field.split(";")
    params = {}
    for pair in pairs:
        kv = pair.split('=')
        params[kv[0]] = kv[1]
    return params

def addAlarm(event, desc, minutesBefore):
    alarm = Alarm()
    alarm.add('action', 'DISPLAY')
    alarm.add('DESCRIPTION', desc)
    dur = icalendar.vDuration(datetime.timedelta(0, 0, 0, 0, -minutesBefore))
    alarm.add('TRIGGER', dur)
    event.add_component(alarm)

def paramsToString(parameters):
    paramDict = parameters.items()
    params = []
    if len(paramDict) > 0:
        for key, value in paramDict:
            params.append(str(key) + "=" + str(value))
            return ";".join(params)
    else:
        return ""

def getDateInfo(component, field):
    info = []    
    date = component.get(field)

    paramStr = paramsToString(date.params)
    if len(paramStr) > 0:
        info.append(str(date.dt))
        info.append(paramStr)
    else:
        tzStr = "America/Denver"
        mountainTz = timezone(tzStr)
        mt = date.dt.astimezone(mountainTz)
        info.append(str(mt))        
        info.append("TZID=" + tzStr)
    
    return "\t".join(info)

def eventFromLine(line, alarmDescSeed, alarmsInMinsBefore):
    fields = line.split('\t')
    event = Event()
    dtstart = parser.parse(fields[0])
    params = getParamDict(fields[1])
    event.add('dtstart', dtstart, params)

    dtend = parser.parse(fields[2])
    params = getParamDict(fields[3])
    event.add('dtend', dtend, params)

    event.add('summary', fields[4])
    event.add('location', fields[5].replace('|', "\r\n"))

    desc = alarmDescSeed + ' ' + dtstart.strftime("%I:%M %p")
    for mins in alarmsInMinsBefore:
        addAlarm(event, desc, mins)
    
    return event