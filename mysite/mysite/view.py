# -*- coding: utf-8 -*-
#coding=UTF-8
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from mysite.get_data import *
import json

def highchartsTry(request):
	if request.method == 'GET':
		topMusics = GetMusicData()
		lists = []
		for music_info in topMusics:
			# music_info[0] = unicode(music_info[0], "utf8", errors="ignore")
			# music_info[0] = music_info[0].encode('gb2312') 
			# music_info[0] = music_info[0].decode()  
			lists.append(music_info)
		context = {
		    'series': json.dumps(lists)
		}
		lists = json.dumps(lists)
		#return render(request, 'try.html', context)
		return render_to_response('try.html', {'lists':lists},RequestContext(request))