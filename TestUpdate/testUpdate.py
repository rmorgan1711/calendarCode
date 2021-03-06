import icalendar
from icalendar import Calendar, Event, Alarm
import datetime

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

cal = InitCalWithPrelims()

seq = 0

event = Event()
params = {"TZID":"America/Denver"}
event.add('dtstart', datetime.datetime(2018, 8, 21, 10, 0, 0), params)
event.add('dtend', datetime.datetime(2018, 8, 21, 11, 0, 0), params)
event.add('sequence', seq)
event.add('summary', 'Test publish update 1')
event.add('uid', '2cba2310-8246-4408-985c-5b2bb067d248')
cal.add_component(event)

event = Event()
params = {"TZID":"America/Denver"}
event.add('dtstart', datetime.datetime(2018, 8, 22, 10, 0, 0), params)
event.add('dtend', datetime.datetime(2018, 8, 22, 11, 0, 0), params)
event.add('sequence', seq)
event.add('summary', 'Test publish update 2')
event.add('uid', '0dab10b8-e138-4ea4-aba3-e4816f912b35')
cal.add_component(event)

calPath = "/Users/Bowen/Documents/calendar/calendarCode/TestUpdate/TestUpdate.ics"
with open(calPath, 'wb') as f:
    f.write(cal.to_ical())
