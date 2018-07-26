import base64

f = open('/Users/Bowen/Documents/calendar/propose.PNG', 'rb')
content = f.read()

imgread = base64.encodestring(content)

print('hello')

print(isinstance(imgread, compat.)

printable = imgread.decode('utf-8')
print(type(printable))

out = open('/Users/Bowen/Documents/calendar/encoded.txt', 'wt')
out.write(imgread.decode('utf-8'))

##code = base64.b64encode(content)
##decoded = base64.b64decode(content)

print('done')
