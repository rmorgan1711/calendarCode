import icalendar
from icalendar import Calendar, Event, Alarm
import datetime
import dateutil.parser
import pytz
import base64

def AttachPNG(event, imgPath):
    attachVal = None
    with open(imgPath, 'rb') as f:
        content = f.read()
        attachval = base64.encodestring(content).decode('utf-8').replace('\n', '')

    paramdict = {'FMTTYPE':'image/png', 'ENCODING':'BASE64', 'VALUE':'BINARY',
                        'X-FILENAME':'propose.png', 'X-APPLE-FILENAME':'propose.png'}
    event.add('ATTACH', attachval, parameters = paramdict)

cal = Calendar()
cal.add('prodid', '-//jbowCalPy')
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

tz = pytz.timezone('America/Denver')

event = Event()
event.add('dtstart',tz.localize(datetime.datetime(2018, 1, 13, 10, 00, 00)))
event.add('dtend',tz.localize(datetime.datetime(2018, 1, 13, 11, 15, 00)))
event.add('dtstamp',tz.localize(datetime.datetime(2018, 1, 9, 6, 27, 00)))
event.add('created',tz.localize(datetime.datetime(2018, 1, 9, 6, 27, 00)))
event.add('description', 'Description is really cool!')
event.add('comment', 'Commentary about this event is that it\'s the bomb!')
event.add('summary', 'In summary, come!')

imgPath = "/Users/Bowen/Documents/calendar/propose.PNG"
AttachPNG(event, imgPath)
event.add('url', 'www.google.com')

geo = icalendar.vGeo([39.743476, -105.003218])
event.add('geo', geo)
event.add('location', '1900 16th Street\nDenver, CO 80220')

alarm = Alarm()
alarm.add('action', 'DISPLAY')
alarm.add('description', 'Event starting soon')
dur = icalendar.vDuration(datetime.timedelta(0, 0, 0, 0, -23))
alarm.add('trigger', dur)
event.add_component(alarm)

cal.add_component(event)

calPath = "/Users/Bowen/Documents/calendar/jbcal.ics"
with open(calPath, 'wb') as f:
    f.write(cal.to_ical())
