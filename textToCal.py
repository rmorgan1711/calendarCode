import icalendar
from icalendar import Calendar, Event, Alarm
import datetime
from dateutil import parser
import pytz

def InitCalWithPrelims():
    cal = Calendar()
    cal.add('prodid', '-//CalPy')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')

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

def GetParamDict(field):
    pairs = field.split(";")
    params = {}
    for pair in pairs:
        kv = pair.split('=')
        params[kv[0]] = kv[1]
    return params

def EventFromLine(line):
    fields = line.split('\t')
    event = Event()
    dtstart = parser.parse(fields[0])
    params = GetParamDict(fields[1])
    event.add('dtstart', dtstart, params)

    dtend = parser.parse(fields[2])
    params = GetParamDict(fields[3])
    event.add('dtend', dtend, params)

    event.add('summary', fields[4])
    event.add('location', fields[5].replace('|', "\r\n"))

    alarm = Alarm()
    alarm.add('action', 'DISPLAY')
    desc = "Rockies Home Game at " + dtstart.strftime("%I:%M %p")
    alarm.add('DESCRIPTION', desc)
    dur = icalendar.vDuration(datetime.timedelta(0, 0, 0, 0, -180))
    alarm.add('TRIGGER', dur)
    event.add_component(alarm)
    
    return event

cal = InitCalWithPrelims()

dataPath = "/Users/Bowen/Documents/calendar/events.txt"
lines = []
with open(dataPath) as f:
    f.readline()
    for line in f:
        if line.find("Away") > -1:
            continue

        event = EventFromLine(line.strip())
        cal.add_component(event)
    

calPath = "/Users/Bowen/Documents/calendar/RockiesHomeGames.ics"
with open(calPath, 'wb') as f:
    f.write(cal.to_ical())
