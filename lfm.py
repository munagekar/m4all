from kivy.network.urlrequest import UrlRequest
import os
from threading import Thread


thousand =1000
million =thousand * thousand
billion = million *thousand

API_key = ''

class Track:
	name = None
	artist = None
	coverartlink_artist= None
	url= None
	mbid = None
	duration = None

	def __init__(self,name=None,artist=None,coverartlink_artist=None,url=None,mbid = None, duration= None):
		self.name=name
		self.artist=artist
		self.coverartlink_artist=coverartlink_artist
		self.url=url
		self.mbid = mbid
		self.duration = duration

def getTopTracks(callback,n=50):
	Thread(target=getTopTrackThreadFn,args=(callback,n)).start()

def getTopTrackThreadFn(callback, n):
	req = UrlRequest('http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key='+API_key+'&format=json&limit='+str(n))
	req.wait()
	jsonresult = req.result
	jsontracklist = jsonresult['tracks']['track']
	tracks =[]
	for i in range(n):
		jsontrack =jsontracklist[i]
		trackname = jsontrack['name']
		trackartist = jsontrack['artist']['name']
		trackurl = jsontrack['url']
		trackart = str(jsontrack['image'][3]['#text']).replace("https:","http:")
		tracks.append(Track(trackname,trackartist,trackart,trackurl))
	callback(tracks)

def imageCachePopulator(tracks,image_cache):
	for i in range(len(tracks)):
		artist = tracks[i].artist
		artist_folder = os.path.join(image_cache,artist)
		if not os.path.exists(artist_folder):
			os.makedirs(artist_folder)
		linklocation = tracks[i].coverartlink_artist
		print (linklocation)
		stripedname = linklocation[linklocation.rindex('/')+1:]
		filepath = os.path.join(artist_folder,stripedname)
		if not os.path.exists(filepath):
			Thread(target=filesaver,args=(linklocation,filepath)).start()

def cacheLocationFixer(tracks,image_cache):
	for i in range(len(tracks)):
		artist = tracks[i].artist
		linklocation = tracks[i].coverartlink_artist
		if 'http:' in linklocation:
			artist_folder = os.path.join(image_cache,artist)
			stripedname = linklocation[linklocation.rindex('/')+1:]
			filepath =os.path.join(artist_folder,stripedname)
			if os.path.exists(artist_folder):
				if os.path.exists(filepath):
					tracks[i].coverartlink_artist = filepath


def getTrackInfo(name,artist,callback):
	Thread(target=getTrackInfoThreadFn,args=(name,artist,callback)).start()
	

def getTrackInfoThreadFn(name,artist,callback):	
	req = UrlRequest('http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key='+API_key+'&artist='+artist+'&track='+name+'&format=json')
	req.wait()
	jsonresult = req.result
	mbid = jsonresult['track']['mbid']
	duration = int(jsonresult['track']['duration'].strip())
	listeners = easyreadnum(int(jsonresult['track']['listeners'].strip()))
	playcount = easyreadnum(int(jsonresult['track']['playcount'].strip()))
	print (jsonresult)
	print (mbid)
	print (duration)
	print (listeners)
	print (playcount)

def easyreadnum(num):
	if num >= billion:
		return str(num//billion)+'B'
	if num >=million:
		return str(num//million)+'M'
	if num >=thousand:
		return str(num//thousand)+'K'


def filesaver(linklocation,filepath):
	req =UrlRequest(linklocation)
	req.wait()
	with open(filepath,'wb') as f:
		f.write(req.result)



		