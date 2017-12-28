'''
Future Feature
Yet to be integrated
'''
from lfm import Track
import utils
from kivy.network.urlrequest import UrlRequest
from xml.dom import minidom
import re
#Update incase of breakage
base_api_link = 'http://lyricscore.eu5.org/api/v1/?'

#TODO ADD THREADING & CALLBACK SUPPORT
def get_lyrics(track):
	#artist = utils.spacefixer(track.artist)
	#name = utils.spacefixer(track.name)
	artist = 'katy+perry'
	name ='roar'
	request_url = base_api_link +'artist='+artist+'&title='+name+'&format=xml'
	print request_url
	req =UrlRequest(request_url)
	req.wait()
	result = req.result
	print (result)
	result = str(result)
	result = result[result.index('<lyrics>')+8:result.rindex('</lyrics>')]
	result = result.replace('<br />','\n')
	print result
get_lyrics('crap')

