# Download all comment from a twitch video to a file, need video id as argument.
# The video id is the last part of the video url.
# Es: in https://www.twitch.tv/videos/494918762 the id is 494918762
# i found the core of this code in RechatTool which is C# source code
# and i ported it to python.

import sys
import json
import requests
import datetime

if len(sys.argv) == 1:
    print('Error need a video id!')
    sys.exit()

videoid = sys.argv[1]
api='https://api.twitch.tv/v5/videos/' + videoid + '/comments'

headers = {
    'Accept': 'application/vnd.twitchtv.v5+json',
    'Client-ID': 'jzkbprff40iqj646a697cyrvl0zt2m6'
    }

next = None
url = ''
segcount = 0

s = requests.session()

with open(videoid + '.txt', 'w', encoding='utf-8') as f:
    while 1:
        if next == None:
            url = api + '?content_offset_seconds=0'
        else:
            url = api + '?cursor=' + next

        r = s.get(url, headers=headers)
        #print(r.content)

        resp_dict = json.loads(r.text)

        timespan = ''
        for c in resp_dict['comments']:
            timespan = str(datetime.timedelta(seconds=c['content_offset_seconds']))
            user = c['commenter']['display_name'] + ': '
            message = c['message']['body']
            #print(timespan + user + message)
            f.write('[' + timespan  + '] ' + user + message + '\n')

        segcount += 1
        print('Downloaded ' + str(segcount) + ' segments, offset=' + timespan, end='\r')

        if '_next' in resp_dict:
            next = resp_dict['_next']
        else:
            break
    
        if next == None:
            break

print('',end = '\n')
print('Downloading chat log to ' + videoid + '.txt done!')
