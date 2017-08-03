# -*- coding:utf-8 -*-  
message = ''
f=open('D:\\marchine_learning\\python_study_crawel-master\\crawel files\\topSongInfo.md','rb+')
while True:
	line = f.readline()
	if line:
		message+=line.decode('utf-8')
	else:
		break
f.close()
print(message)