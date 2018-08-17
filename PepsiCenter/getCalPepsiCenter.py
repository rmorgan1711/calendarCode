import gzip
import json
from urllib import request
from urllib import response

url = "https://alttix.ksehq.com/api/Calendar?venueId=9&start=2018-09-01&end=2018-12-15"

dateStart = "2018-09-01"
dateEnd = "2018-12-31"

url = "https://alttix.ksehq.com/api/Calendar?venueId=9&start=" + dateStart + "&end=" + dateEnd

headers = {
    "Host": "alttix.ksehq.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://alttix.ksehq.com/calendar-PC2.html",
    "DNT": "1",
    "Connection": "keep-alive"
    }

req = request.Request(url, None, headers, method="GET")
resp = request.urlopen(req)

gzipped = resp.read()

content = gzip.decompress(gzipped).decode("utf-8")
content = json.loads(content)

content = sorted(content, key=lambda k: k["first_start_time"])

with open("pepsiCenter.txt", "w") as f:
    f.write(json.dumps(content, indent=4))


