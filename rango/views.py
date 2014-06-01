# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.forms import InstagramForm
import requests
import json
import urllib
from urlparse import urlparse
import os
import time

INSTAGRAM_ACCESS_TOKEN = '268066931.1fb234f.b3ace901202049fb96067641d0e41a7e'



def save_pagination(media_response):
	try:
		next_page = str(media_response['pagination']['next_url'])
		next_page_json = requests.get(next_page)
		print next_page_json.content
		next_page_json = json.loads(next_page_json.text)
		save_photos(next_page_json)
	except Exception,e:
		print (e)


def save_photos(media_response):
	print 'save_photos'
	media_list = []
	for user_media in media_response['data']:
		media_list.append(user_media['images']['standard_resolution']['url'])
	#Specify the path required. for Eg : /home/Pictures/insta_pics. this is for linux users
	for media in media_list:
		print media
		urllib.urlretrieve(str(media))
		print 'saved'
	if media_response['pagination']:
		save_pagination(media_response)
	else:
		return False

def index(request):
	if request.method == 'POST':
		insta_form = InstagramForm(request.POST)
		if insta_form.is_valid():
			username = insta_form.cleaned_data['username']
			resp = requests.get('https://api.instagram.com/v1/users/search?q='+username+'&access_token='+INSTAGRAM_ACCESS_TOKEN)
			resp = json.loads(resp.text)
			if resp['data'][0]['username'] == username:
				user_id = str(resp['data'][0]['id'])
				media_url = 'https://api.instagram.com/v1/users/'+user_id+'/media/recent?access_token='+INSTAGRAM_ACCESS_TOKEN
				media_response = requests.get(media_url)
				media_response = json.loads(media_response.text)
				save_photos(media_response)

				form = InstagramForm()
				return render_to_response('repos.html', locals(), context_instance=RequestContext(request))
		else:
			form = InstagramForm()
			return render_to_response('repos.html', locals(), context_instance=RequestContext(request))			
	else:
		form = InstagramForm()
		return render_to_response('repos.html', locals(), context_instance=RequestContext(request))

