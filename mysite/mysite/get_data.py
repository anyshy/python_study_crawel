# encoding = utf-8
import json
client = MongoClient('mongodb://localhost:27017/') # 连接到mongodb
db = client.Music #打开数据库Library
collection=db.MusicInfoSorted # 打开数据表MusicInfoSorted
# 查找全部
cursor = collection.find()
# topSongMessage = ''
# f=open('E:\\topSongMessage.md','w') 
for song in cursor:
    # topSongMessage +="1. "+song['artist'][0]+"  ["+song['name']+"]("+ song['url']+")\n"
    print song['name'], song['commentTotals']
# f.write(topSongMessage.encode('utf-8'))    
# f.close()