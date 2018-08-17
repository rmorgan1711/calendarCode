import gzip
from urllib import request
from urllib import response

url = "https://www.stanza.co/?category=5339d047dcf9e6534d405757&type=dead&file=/api/schedules/nfl-broncos/nfl-broncos.ics"
url = "https://www.stanza.co/api/schedules/nfl-broncos/nfl-broncos.ics"

headers = {
    "Host": "www.stanza.co",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv\":52.0) Gecko/20100101 Firefox/52.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",   
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
    }

req = request.Request(url, None, headers, method="GET")
resp = request.urlopen(req)

gzipped = resp.read()

content = gzip.decompress(gzipped).decode("utf-8")
lines = content.split("\n")

with open("broncos.txt", "w") as f:
    for line in lines:
        if len(line) > 75:
            while len(line) > 75:
                f.write(line[0:73])
                line = "\n " + line[73:]
            f.write(line + "\n")
        else:
            f.write(line + "\n")

