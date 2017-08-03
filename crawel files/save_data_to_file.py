from pymongo import MongoClient
import pymongo
import json
client = MongoClient("localhost", 27017)

db = client.Music 

collection=db.MusicInfo
print(collection.find_one())
cursor = collection.find().sort()
message = 'topMusics = [\n'
f=open('D:\\marchine_learning\\python_study_crawel-master\\crawel files\\topSongInfo.md','wb+')
for song in cursor:
    message += '    ["'+song['name']+'",'+ str(song['commentTotals']*1.0/1000)+'],\n'
    print(message)
message += ']'
f.write(message.encode('utf-8'))    
f.close()