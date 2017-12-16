from kivy.network.urlrequest import UrlRequest

API_key = ""
topTrackCallback = None

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

def getTopTracks(callback):
	global topTrackCallback
	#print (callback)
	topTrackCallback=callback	
	result = UrlRequest('http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key='+API_key+'&format=json', on_success=topTrackParser)

def topTrackParser(req,result):
	global topTrackCallback
	jsonresult = result
	jsontracklist = jsonresult['tracks']['track']
	tracks =[]
	for i in range(50):
		jsontrack =jsontracklist[i]
		trackname = jsontrack['name']
		#print(trackname)
		trackartist = jsontrack['artist']['name']
		#print(trackartist)
		trackurl = jsontrack['url']
		#print(trackurl)
		trackart = jsontrack['image'][3]['#text']
		#print(trackart)
		tracks.append(Track(trackname,trackartist,trackart,trackurl))
	topTrackCallback(tracks)


