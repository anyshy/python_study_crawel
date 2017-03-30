message = ''
f=open('E:\\topSongInfo.md','r')
while True:
	line = f.readline()
	if line:
		message+=line
	else:
		break
f.close()
print message