# -*- coding: utf-8 -*-
#coding=UTF-8
from django.shortcuts import render,render_to_response
from django.template import RequestContext
import json

def highchartsTry(request):
	if request.method == 'GET':
		topMusics = [
			[u"晴天",1329.656],
		    [u"告白气球",248.533],
		    [u"演员",175.353],
		    [u"Five Hundred Miles",121.012],
		    [u"Booty Music",111.814],
		    [u"超越无限",105.345],
		    [u"刚刚好",104.539],
		    [u"你还要我怎样",102.994],
		    [u"夜空中最亮的星",84.444],
		    [u"全世界谁倾听你 ",64.522],
		    [u"明天，你好",63.626],
		    [u"今年勇",63.285],
		    [u"我好想你",58.791],
		    [u"The Phoenix",53.883],
		    [u"Es rappelt im Karton",52.513],
		    [u"男孩别哭",50.105],
		    [u"Sugar",49.248],
		    [u"好久不见",48.844],
		    [u"一次就好",46.127],
		    [u"Viva La Vida",45.274],
		    [u"彩虹",43.802]
		]
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
		# return render(request, 'try.html', context)
		return render_to_response('try.html', RequestContext(request,{'lists':lists}))