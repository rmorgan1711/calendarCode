import icalendar
from icalendar import Calendar, Event, Alarm
import datetime
from dateutil import parser
import pytz
from pytz import timezone

def InitCalWithPrelims():
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

def AddByeWeek(cal):
    tzStr = "America/Denver"
    dt = datetime.datetime(2018,11,11,10,0,0)
    event = Event()
    event.add('dtstart', dt, {'TZID':tzStr})
    event.add('dtend', dt, {'TZID':tzStr})

    summary = 'Broncos Bye Week'
    event.add('summary', summary)
    AddAlarm(event, summary, 1440)    
    AddAlarm(event, summary, 7200)

    cal.add_component(event)

def GetParamDict(field):
    pairs = field.split(";")
    params = {}
    for pair in pairs:
        kv = pair.split('=')
        params[kv[0]] = kv[1]
    return params

def AddAlarm(event, desc, minutesBefore):
    alarm = Alarm()
    alarm.add('action', 'DISPLAY')
    alarm.add('DESCRIPTION', desc)
    dur = icalendar.vDuration(datetime.timedelta(0, 0, 0, 0, -minutesBefore))
    alarm.add('TRIGGER', dur)
    event.add_component(alarm)

def EventFromLine(line):
    fields = line.split('\t')
    event = Event()
    params = GetParamDict(fields[0])
    dtstart = parser.parse(fields[1])
    event.add('dtstart', dtstart, params)

    params = GetParamDict(fields[2])
    dtend = parser.parse(fields[3])
    event.add('dtend', dtend, params)

    summary = fields[4].split(' ')
    if summary[1] == "at":
        summary[1] = "@"
    else:
        tmp = summary[0]
        summary[0] = summary[2]
        summary[2] = tmp
        summary[1] = "@"
        
    event.add('summary', " ".join(summary))
    event.add('location', fields[5].replace('|', "\r\n"))

    desc = "Broncos Game " + dtstart.strftime("%I:%M %p")
    AddAlarm(event, desc, 180)
    AddAlarm(event, desc, 1440)
    
    return event

cal = InitCalWithPrelims()

dataPath = "/Users/Bowen/Documents/calendar/calendarCode/Broncos/events.txt"
lines = []
with open(dataPath) as f:
    f.readline()
    for line in f:
        event = EventFromLine(line.strip())
        cal.add_component(event)

AddByeWeek(cal) 

calPath = "/Users/Bowen/Documents/calendar/calendarCode/Broncos/BroncosGames.ics"
with open(calPath, 'wb') as f:
    f.write(cal.to_ical())
