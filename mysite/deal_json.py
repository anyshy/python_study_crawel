#encoding=utf8
import requests
import json
from pprint import pprint

headers = {
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.10 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch'
}
songUrl = 'http://music.163.com/api/song/detail/?ids=%5B461347998%5D'
reqInfo = requests.post(songUrl, headers = headers)#利用requests的post方式获取数
song = reqInfo.json()['songs'][0]
print song['name']
artists = song['artists']
for i in artists:
    print i['name']
print song['popularity']
print song['score']

