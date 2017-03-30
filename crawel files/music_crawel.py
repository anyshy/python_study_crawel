#encoding=utf8
import requests
from bs4 import BeautifulSoup
import re, time
import os, json
import base64
from Crypto.Cipher import AES
from pprint import pprint
from pymongo import MongoClient

Default_Header = {
    'Referer': 'http://music.163.com/',
    'Host': 'music.163.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.10 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch'
}

BASE_URL = 'http://music.163.com'

_session = requests.session()
_session.headers.update(Default_Header)

Client = MongoClient()
# 创建数据库Music
db=Client["Music"]
# 创建表MusicInfo
collection=db["MusicInfo"]

def getPage(pageIndex):
    pageUrl = 'http://music.163.com/discover/playlist/?order=hot&cat=全部&limit=35&offset='+pageIndex
    soup = BeautifulSoup(_session.get(pageUrl).content, 'html.parser')
    songList = soup.findAll('a', attrs = {'class': 'tit f-thide s-fc0'})
    for i in songList:
        # print(i['href']) # 得到所有的url:/playlist?id=619147026
        getPlayList(i['href'])

def getPlayList(playListId):
    playListUrl = BASE_URL + playListId# 拼接url:http://music.163.com/playlist?id=619147026
    soup = BeautifulSoup(_session.get(playListUrl).content, 'html.parser')
    songList = soup.find('ul', attrs = {'class': 'f-hide'})
    for i in songList.findAll('li'):
        startIndex = (i.find('a')['href'])
        songId = startIndex.split('=')[1]
        readEver(songId)


def aesEncrypt(text, secKey):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(secKey, 2, '0102030405060708')
    ciphertext = encryptor.encrypt(text)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext

def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(text.encode('hex'), 16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)

def createSecretKey(size):
    return (''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(size))))[0:16] #创建一个16位的随机数

def readEver(songId):  
    headers = {
        'Cookie': 'appver=1.5.0.75771', 
        'Referer': 'http://music.163.com/'
    }
    text = {
        'username': '351192350@qq.com', 
        'password': 'why2014211500', 
        'rememberLogin': 'true'
    }

    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    nonce = '0CoJUm6Qyw8W8jud'
    pubKey = '010001'

    text = json.dumps(text)
    secKey = createSecretKey(16)#新建一个密钥
    encText = aesEncrypt(aesEncrypt(text, nonce), secKey)
    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
    data = {
        'params': encText,
        'encSecKey': encSecKey
    }

    # 歌曲
    # http://music.163.com/api/song/detail/?ids=%5B436514312%5D
    songUrl = 'http://music.163.com/api/song/detail/?ids=%5B'+str(songId)+'%5D'
    reqInfo = requests.post(songUrl, headers = headers)#利用requests的post方式获取数据
    songInfo = reqInfo.json()['songs'][0]
    # 歌词
    # http://music.163.com/weapi/song/lyric?csrf_token=
    # lyricUrl = 'http://music.163.com/weapi/song/lyric?csrf_token='
    # reqLyric = requests.post(lyricUrl, headers = headers, data=data)#利用requests的post方式获取数据
    # 评论
    #http://music.163.com/#/song?id=29774140
    #csrf_token:91cbfff84f0b91c0f6ab8d0a717a8c9c
    #Request URL:http://music.163.com/weapi/v1/resource/comments/R_SO_4_29774140?csrf_token=91cbfff84f0b91c0f6ab8d0a717a8c9c
    commentUrl = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_'+str(songId)+'/?csrf_token='
    reqComment = requests.post(commentUrl, headers = headers, data=data)#利用requests的post方式获取数据
    songCommment = reqComment.json()
    total = songCommment['total'] #得到数据的评论数

    if int(total) > 1000:
    	song = {} #新建一个song对象，用来存放数据
        songInfo = reqInfo.json()['songs'][0]
    	song['name'] = songInfo['name'] #歌曲名
        artists = songInfo['artists']
        song['artist']=[]
        for i in artists:
            song['artist'].append(i['name']+"")
        song['commentTotals'] = int(total) #评论数
        song['url']='http://music.163.com/#/song?id='+songId
    	song['api_data'] = songUrl
        collection.insert(song) #插入数据
    else:
        pass

if __name__ == '__main__':
    for i in range(1,43):
        getPage(str(i*35))
