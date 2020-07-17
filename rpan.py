#!/usr/bin/env python3

# rpan.py by zizzu 2020
# list of reddit pubblic access network streams
# no option list streams category, title, url
# option -p add urls to playlist and play it via mpv
# https://mpv.io/manual/master/#keyboard-control, < and > should be default playlist buttons

import os
import sys
import json
import shlex
import requests
import subprocess

playlist=False
cmd = 'mpv --playlist='
tmpfile='/tmp/rpan.txt'

def truncate(string, width):
        if len(string) > width: string = string[:width-3] + '...'
        return string

if len(sys.argv) > 1:
        if sys.argv[1] == '-p': playlist=True
        else: print('invalid option'); sys.exit(0);

response = requests.get('https://strapi.reddit.com/broadcasts')
jsonResponse = response.json()

if playlist == False:
        for i in jsonResponse['data']:
                subreddit = i['post']['subreddit']['name']
                title = i['post']['title']
                url = i['stream']['hls_url']
                print('{:<20} {:<40.40} {:<20}'.format(subreddit, truncate(title,40), url))
else:
        f = open(tmpfile, 'w')
        for i in jsonResponse['data']:
                url = i['stream']['hls_url']
                f.write(url + '\n')
        f.close()

        subprocess.call(shlex.split(cmd+tmpfile), shell=False)

        os.remove(tmpfile)
