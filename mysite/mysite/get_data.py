# encoding = utf-8
import json
from pymongo import MongoClient

def GetMusicData():
    client = MongoClient("localhost", 27017)
    db = client.Music 
    collection=db.MusicInfo
    # 查找全部
    cursor = collection.find()
    songlists=[]

    for song in cursor:
        tmp=[song['name'],song['commentTotals']]
        songlists.append(tmp)
    
    songlists.sort(reverse=True)
    return songlists

# topSongMessage = ''
# f=open('E:\\topSongMessage.md','w') 

    # topSongMessage +="1. "+song['artist'][0]+"  ["+song['name']+"]("+ song['url']+")\n"
    #print (song['name'], song['commentTotals'])
# f.write(topSongMessage.encode('utf-8'))    
# f.close()