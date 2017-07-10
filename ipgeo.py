import json
import urllib2
with open('ip.txt') as inf:
    for line in inf:
        count, ipaddr = line.lstrip().rstrip().split(" ");
        response = urllib2.urlopen('http://ip-api.com/json/' + ipaddr )
        json_txt = response.read()
        data     = json.loads(json_txt)
        print data['city']

