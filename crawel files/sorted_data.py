#encoding=utf8
from pymongo import MongoClient
from pprint import pprint
import json
client = MongoClient('mongodb://localhost:27017/') # 连接到mongodb
db = client.Music #打开数据库Library
collection=db.MusicInfo # 打开数据表Books
sorted_collection=db.MusicInfoSorted
# 查找全部
curosr = collection.find()
curosr.distinct("api_data")
curosr.distinct("url")
for song in curosr.sort('commentTotals',-1):
	sorted_collection.insert(song)
