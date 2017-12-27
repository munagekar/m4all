'''
lfm2.py wrapper
Next Lfm wrapper under development for future development
Currently Music Brainz mbid are not supported since they aren't in use
'''
from kivy.network.urlrequest import UrlRequest
import os
import shutil
import time
from threading import Thread
from kivy.storage.dictstore import DictStore

#Fix all possible errors in the store

thousand =1000
million =thousand * thousand
billion = million *thousand

API_key = ''

class Track:
	name = None
	artist = None
	album = None
	duration = None
	listeners = None 
	playcount = None
	coverart_low = None
	coverart_med = None
	coverart_high = None
	coverart_vhigh = None
	tags = None #5 tags
	wiki = None

	def __init__(self,name,artist):
		self.artist = artist
		self.name = name

	#TODO: Write Track Constructors and Make Wrapper Changes

class Artist:
	name = None
	coverart_low = None
	coverart_med = None
	coverart_high = None
	coverart_vhigh = None
	listeners = None
	playcount = None
	tags = None#5
	similar = None #5
	bio = None

	def __init__(self,name):
		self.name = name

	def setImageData(self,l,m,h,v):
		self.coverart_low =l
		self.coverart_med = m
		self.coverart_high = h
		self.coverart_vhigh = v

'''

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

def easyreadnum(num):
	if num >= billion:
		return str(num//billion)+'B'
	if num >=million:
		return str(num//million)+'M'
	if num >=thousand:
		return str(num//thousand)+'K'
'''


#Path fixing for cross platform support
def pathfixer(path):
	return path.replace('?','(ques)')



def remotefilesaver(linklocation,filepath):
	req =UrlRequest(linklocation)
	req.wait()
	with open(filepath,'wb') as f:
		f.write(req.result)

#Lfm Helper is a class that handles everything- URL requests, Caching, Multithreading
#Easiest Interface to LastFM
class LfmHelper():
	lfmcachedir = None
	cache_version = '1'
	def __init__(self,root_folder):
		self.lfmcachedir =  os.path.join(root_folder,'lfmcache')
		if not os.path.exists(self.lfmcachedir):
			os.makedirs(self.lfmcachedir)
		self.__sanity_test()
	
	def __versioning(self):
		versionfilepath = os.path.join(self.lfmcachedir,'version.txt')
		versionfile = open(versionfilepath,'w')
		versionfile.write(self.cache_version)
		versionfile.close()


	def clear_cache(self):	#Used to clear the cache
		shutil.rmtree(self.lfmcachedir)
		if not os.path.exists(self.lfmcachedir):
			os.makedirs(self.lfmcachedir)

	def __sanity_test(self):		#Check if the old cache can be used
		versionfilepath = os.path.join(self.lfmcachedir,'version.txt')
		if os.path.exists(versionfilepath):
			versionfile = open(versionfilepath,'r')
			cache_version = versionfile.read()
			if cache_version != self.cache_version:
				print ('Cache Version Mismatch...Clearing cache')
				self.clear_cache()
		if not os.path.exists(versionfilepath):
			self.__versioning()

	def getTopTracks(self,callback):
		infocache = os.path.join(self.lfmcachedir,'infocache')
		needsupdate = True
		store = DictStore(infocache)
		lastupdated =0     #Time stamp when last updated assumed 1980
		if 'toptracks' in store:
			lastupdated = store['toptracks']['lastupdated']
			if time.time() - lastupdated < 36000:
				needsupdate = False
				tracks = store['toptracks']['tracks']
				callback(tracks)

		if needsupdate == True:
			Thread(target=self.getTopTrackThreadFn,args=(callback,)).start()

	def getTopTrackThreadFn(self,callback):
		n =50
		print ('Attempting URL fetch to get the top tracks')
		req = UrlRequest('http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key='+API_key+'&format=json&limit='+str(n))
		req.wait()
		jsonresult = req.result
		#print (jsonresult)
		#print('http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key='+API_key+'&format=json')
		jsontracklist = jsonresult['tracks']['track']
		tracks =[]
		for i in range(n):
			jsontrack =jsontracklist[i]
			trackname = jsontrack['name']
			playcount = jsontrack['playcount']
			listeners = jsontrack['listeners']
			trackartist = jsontrack['artist']['name']
			trackart_low = str(jsontrack['image'][0]['#text']).replace("https:","http:")
			trackart_mid = str(jsontrack['image'][1]['#text']).replace("https:","http:")
			trackart_high = str(jsontrack['image'][2]['#text']).replace("https:","http:")
			trackart_vhigh = str(jsontrack['image'][3]['#text']).replace("https:","http:")
			curTrack = Track(trackname,trackartist)
			curTrack.listeners = listeners
			curTrack.playcount = playcount
			curArtist = Artist(trackartist)
			curArtist.setImageData(trackart_low,trackart_mid,trackart_high,trackart_vhigh)
			self.updateArtist(curArtist) #Update the artist data
			self.updateTrack(curTrack)
			#Add the track to the return list
			tracks.append(curTrack)
		#Cache the top tracks here
		infocache = os.path.join(self.lfmcachedir,'infocache')
		curtime = time.time()
		infocache = os.path.join(self.lfmcachedir,'infocache')
		store = DictStore(infocache)
		store['toptracks'] = {'lastupdated':curtime,'tracks':tracks}
		callback(tracks)

	def updateArtist(self,artist):		
		artist_name = artist.name
		self.updateArtistArt(artist)
		artist_folder = os.path.join(self.lfmcachedir,artist_name)
		if not os.path.exists(artist_folder): # If the directory doesn't exist create a directory
			os.makedirs(artist_folder)
		artist_file = os.path.join(artist_folder,'infofile')
		store = DictStore(artist_file)
		store['artist']={'artist':artist,'lastupdated':time.time()}
		#TODO add more stuff as app gets developed

	def updateArtistArt(self,artist): #Currently this method only get the high quality stuff
		imagelink = artist.coverart_vhigh
		stripedname = "vh_"+imagelink[imagelink.rindex('/')+1:]
		imagepath = os.path.join(self.lfmcachedir,artist.name,stripedname)
		if not os.path.exists(imagepath):
			Thread(target=remotefilesaver,args=(imagelink,imagepath)).start()
		#TODO support lower quality art stuff later

	def getArtistCoverPath(self,artist_name):
		artist_file= os.path.join(self.lfmcachedir,artist_name,'infofile')
		store = DictStore(artist_file)
		artist = store['artist']['artist']
		imagelink = artist.coverart_vhigh
		strippedname = 'vh_'+imagelink[imagelink.rindex('/')+1:]
		check_path = os.path.join(self.lfmcachedir,artist_name,strippedname)
		print (check_path)
		if os.path.exists(check_path):	#Check if the cached copy exists else return the link
			return check_path
		print ('Failed to find the path')
		return imagelink

	def updateTrack(self,track):
		trackartist = track.artist
		trackname = track.name
		artist_folder = os.path.join(self.lfmcachedir,trackartist)
		track_file = os.path.join(artist_folder,trackname)
		track_file = pathfixer(track_file)
		store = DictStore(track_file)
		store['lastupdated'] = {'lastupdated':time.time(),'track':track}
		#TODO add more stuff as app gets developed









		