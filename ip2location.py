#!/usr/bin/python3
# Convert ip2location lite database to human readable
# https://lite.ip2location.com/file-download 

from socket import inet_ntoa
from struct import pack

def long2ip(ip):
        return inet_ntoa(pack("!L", ip))

fin = open('IP2LOCATION-LITE-DB3.CSV','r')
fout = open('IP2LOCATION-LITE-DB3.txt','w')

for line in fin:
        tokens = line.replace('"','').split(',')
        start = int(tokens[0])
        stop = int(tokens[1])
        code = tokens[2]
        country = tokens[3]
        region = tokens[4]
        city = tokens[5]

        fout.write('%s %s %s %s %s %s' %
        (long2ip(start),long2ip(stop),code, country, region, city)
        )

fin.close()
fout.close()
