# -*- coding: utf-8 -*-

import re
import requests
import json

def get_song(song_id):
    url = "http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.song.play&"
    data = requests.get(url).text

    data = re.findall(r'\((.*)\)',data)[0]
    data = json.loads(data)
    title = data['songinfo']['title']
    data = data.get('bitrate', None)

    if data:
        print(data)
        data = requests.get(data['show_link']).content
        with open('%s.mp3' % title, 'wb') as f:
            f.write(data)
    else:
        print("版权受限")

def get_music_ids_by_name(song_name):
    api = 'http://music.baidu.com/search'
    data = {
        'key':song_name
    }
    response = requests.get(api, params=data)
    response.encoding = 'utf-8'
    html = response.text
    ul = re.findall(r'<ul.*</ul>', html, re.S)[0]
    sids = re.findall(r'sid&quot;:(\d+),', ul, re.S)
    #print(len(sids))
    return sids



if __name__ == '__main__':
    sids = get_music_ids_by_name("刘德华")
    print(sids)