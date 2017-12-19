from kivy.network.urlrequest import UrlRequest
import os
import thread
#import netutils

API_key = "
topTrackCallback = None
nos_track = 0

class Track:
	name = None
	artist = None
	coverartlink = None
	url= None

	def __init__(self,name=None,artist=None,coverartlink=None,url=None):
		self.name=name
		self.artist=artist
		self.coverartlink=coverartlink
		self.url=url

def getTopTracks(callback,n):
	print 'Url UrlRequest was made'
	global topTrackCallback
	global nos_track
	nos_track = n
	#print (callback)
	topTrackCallback=callback	
	result = UrlRequest('http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key='+API_key+'&format=json&limit='+str(n), on_success=topTrackParser)

def topTrackParser(req,result):
	print 'topTrackParser was called'
	global topTrackCallback
	global nos_track
	jsonresult = result
	jsontracklist = jsonresult['tracks']['track']
	tracks =[]
	for i in range(nos_track):
		jsontrack =jsontracklist[i]
		trackname = jsontrack['name']
		#print(trackname)
		trackartist = jsontrack['artist']['name']
		#print(trackartist)
		trackurl = jsontrack['url']
		#print(trackurl)
		trackart = str(jsontrack['image'][3]['#text']).replace("https:","http:")
		tracks.append(Track(trackname,trackartist,trackart,trackurl))
	topTrackCallback(tracks)





def imageCachePopulator(tracks,image_cache):
	for i in range(len(tracks)):
		artist = tracks[i].artist
		artist_folder = os.path.join(image_cache,artist)
		if not os.path.exists(artist_folder):
			os.makedirs(artist_folder)
		linklocation = tracks[i].coverartlink
		print (linklocation)
		stripedname = linklocation[linklocation.rindex('/')+1:]
		filepath = os.path.join(artist_folder,stripedname)
		if not os.path.exists(filepath):
			thread.start_new_thread(filesaver,(linklocation,filepath))

def cacheLocationFixer(tracks,image_cache):
	for i in range(len(tracks)):
		artist = tracks[i].artist
		linklocation = tracks[i].coverartlink
		if 'http:' in linklocation:
			artist_folder = os.path.join(image_cache,artist)
			stripedname = linklocation[linklocation.rindex('/')+1:]
			filepath =os.path.join(artist_folder,stripedname)
			if os.path.exists(artist_folder):
				if os.path.exists(filepath):
					tracks[i].coverartlink = filepath





def filesaver(linklocation,filepath):

	req =UrlRequest(linklocation)
	req.wait()
	with open(filepath,'wb') as f:
		f.write(req.result)

		