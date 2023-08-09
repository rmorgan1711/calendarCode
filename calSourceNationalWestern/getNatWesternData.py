import gzip
from urllib import request
from urllib import response

import requests
from bs4 import BeautifulSoup


headers = {
    "Host": "nationalwesterncomplex.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:67.0) Gecko/20100101 Firefox/67.0",
    "Accept": "ttext/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",   
    "DNT": "1",
    "Connection": "keep-alive",
    "Cookie": "cookie_notice_accepted=true",
    "Upgrade-Insecure-Requests": "1",
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
    }


months = ['06','07','08','09','10','11','12',]
distinctLinks = set()

for m in months:
    endpoint = '2019-' + m

    resp = requests.get('https://nationalwesterncomplex.com/events/' + endpoint, headers=headers)

    soup = BeautifulSoup(resp.text, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href != None and 'https://nationalwesterncomplex.com/event' in href:
            distinctLinks.add(href)

for a in sorted(distinctLinks):
    print(a)

for testUrl in distinctLinks:
    # testUrl = 'https://nationalwesterncomplex.com/event/region-8-arabian-horse-show-2/'
    print(testUrl)
    resp = requests.get(testUrl, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')

    title = soup.find_all('h1', {'class': 'tribe-events-single-event-title'})
    startTime = soup.find_all('span', {'class': 'tribe-event-date-start'})
    endTime = soup.find_all('span', {'class': 'tribe-event-date-end'})
    eventUrl = soup.find_all('dd', {'class': 'tribe-events-event-url'})

    if len(title) == 0 or len(startTime) == 0 or len(endTime) == 0 or len(eventUrl) == 0:
        continue

    title = soup.find_all('h1', {'class': 'tribe-events-single-event-title'})[0]
    startTime = soup.find_all('span', {'class': 'tribe-event-date-start'})[0]
    endTime = soup.find_all('span', {'class': 'tribe-event-date-end'})[0]
    eventUrl = soup.find_all('dd', {'class': 'tribe-events-event-url'})[0]

    print(title)
    print(startTime)
    print(endTime)
    print(eventUrl)