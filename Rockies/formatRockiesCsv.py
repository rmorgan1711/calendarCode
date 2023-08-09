import datetime
from dateutil import parser

import sys
sys.path.append('/Users/Bowen/Documents/calendar/calendarCode/')
import calMethods

eventsList = calMethods.delimitedFileToDictList('EventTicketPromotionPrice.csv')

dateParams = 'TZID=America/Denver'

headers = ['DTSTART','Params','DTEND','Params','SUMMARY','LOCATION']
lines = [headers]

for eventDict in eventsList:
    if eventDict['LOCATION'] != 'Coors Field - Denver':
        continue

    dtstart = eventDict['START DATE'] + ' ' + eventDict['START TIME']
    dtstart = parser.parse(dtstart)

    dtend = dtstart + datetime.timedelta(hours = 3)

    summary = eventDict['SUBJECT'].replace('at', '@')
    location = 'Coors Field|2001 Blake St.|Denver, CO 80205'

    line = [dtstart, dateParams, dtend, dateParams, summary, location]
    lines.append(line)

calMethods.listOfListsToFile('rockiesHomeGames2019.txt', lines)