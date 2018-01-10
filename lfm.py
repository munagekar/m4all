'''
lfm2.py wrapper
Next Lfm wrapper under development for future development
Currently Music Brainz mbid are not supported since they aren't in use
'''
from kivy.network.urlrequest import UrlRequest
import os
import shutil
import time
import utils
from threading import Thread
from kivy.storage.dictstore import DictStore

#API Key For Last FM
API_key = ''

#This is a class for a Single Song
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

#Class for Singer or Track Artist
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

	#Convinience Method for Setting Image Art Data
	def setImageData(self,l,m,h,v):
		self.coverart_low =l
		self.coverart_med = m
		self.coverart_high = h
		self.coverart_vhigh = v

#Function to Save some something from iternet to local storage
def remotefilesaver(linklocation,filepath):
	req =UrlRequest(linklocation)
	req.wait()
	with open(filepath,'wb') as f:
		f.write(req.result)

#Lfm Helper is a class that handles everything- URL requests, Caching, Multithreading
#Easiest Interface to LastFM
class LfmHelper():
	lfmcachedir = None
	#Cahce Version is used for Cahce consistency, version changes
	cache_version = '1'

	#Lfm Helper is initialized with the root folder
	def __init__(self,root_folder):
		self.lfmcachedir =  os.path.join(root_folder,'lfmcache')
		if not os.path.exists(self.lfmcachedir):
			os.makedirs(self.lfmcachedir)
		self.__sanity_test()
	
	#This method is used to create a new version file for a New Cache
	def __versioning(self):
		versionfilepath = os.path.join(self.lfmcachedir,'version.txt')
		versionfile = open(versionfilepath,'w')
		versionfile.write(self.cache_version)
		versionfile.close()

	#This method is used to clear the complete cache
	def clear_cache(self):	
		shutil.rmtree(self.lfmcachedir)
		if not os.path.exists(self.lfmcachedir):
			os.makedirs(self.lfmcachedir)

	#Deletes old cache in case it cannot be used and does versioning
	def __sanity_test(self):		
		versionfilepath = os.path.join(self.lfmcachedir,'version.txt')
		if os.path.exists(versionfilepath):
			versionfile = open(versionfilepath,'r')
			cache_version = versionfile.read()
			if cache_version != self.cache_version:
				print ('Cache Version Mismatch...Clearing cache')
				self.clear_cache()
		if not os.path.exists(versionfilepath):
			self.__versioning()

	#Get the most played track around the world
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

	#Actual Thread Function for Fetching the Top Tracks
	def getTopTrackThreadFn(self,callback):
		n =50
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
			trackartist = jsontrack['artist']['name']
			trackart_low = str(jsontrack['image'][0]['#text']).replace("https:","http:")
			trackart_mid = str(jsontrack['image'][1]['#text']).replace("https:","http:")
			trackart_high = str(jsontrack['image'][2]['#text']).replace("https:","http:")
			trackart_vhigh = str(jsontrack['image'][3]['#text']).replace("https:","http:")
			curTrack = Track(trackname,trackartist)
			curArtist = Artist(trackartist)
			curArtist.setImageData(trackart_low,trackart_mid,trackart_high,trackart_vhigh)
			self.updateArtist(curArtist) #Update the artist data
			self.updateTrack(curTrack,actualfetch=False)
			#Add the track to the return list
			tracks.append(curTrack)
		#Cache the top tracks here
		infocache = os.path.join(self.lfmcachedir,'infocache')
		curtime = time.time()
		infocache = os.path.join(self.lfmcachedir,'infocache')
		store = DictStore(infocache)
		store['toptracks'] = {'lastupdated':curtime,'tracks':tracks}
		callback(tracks)

	#Used to Update the artist Data in Local Cache
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

	#Used to Update & Fetch Artist Art in Local Cache
	def updateArtistArt(self,artist): #Currently this method only get the high quality stuff
		imagelink = artist.coverart_vhigh
		stripedname = "vh_"+imagelink[imagelink.rindex('/')+1:]
		imagepath = os.path.join(self.lfmcachedir,artist.name,stripedname)
		if not os.path.exists(imagepath):
			Thread(target=remotefilesaver,args=(imagelink,imagepath)).start()
		#TODO support lower quality art stuff later

	#Returns the cover art given the artist name
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
		return imagelink

	#Updates Track Details in the Local Cache
	def updateTrack(self,track,actualfetch):
		trackartist = track.artist
		trackname = track.name
		artist_folder = os.path.join(self.lfmcachedir,trackartist)
		track_file = os.path.join(artist_folder,trackname)
		track_file = utils.pathfixer(track_file)
		store = DictStore(track_file)
		store['track'] = {'lastupdated':time.time(),'track':track,'actualtrackfetch':actualfetch}
		#TODO add more stuff as app gets developed

	#Does an actual song info fetch from LastFm for a track
	def getTrackDetails(self,artistname,trackname,callback):
		needsupdate = True
		cachefile = os.path.join(self.lfmcachedir,artistname,utils.pathfixer(trackname))
		store = DictStore(cachefile)
		curtime = time.time()
		lastupdated = store['track']['lastupdated']
		track = store['track']['track']
		actualtrackfetch = store['track']['actualtrackfetch']
		if actualtrackfetch==True and curtime - lastupdated < 36000:
			callback(track)

		#TODO Incomplete method need to perform proper track detail update here
		else:
			Thread(target=self.getTopTrackDetailsThreadFn,args=(artistname,trackname,callback,)).start()

	#Function to get Similar Tracks
	def getSimilarTracks():
		pass

	#Thread Function for getting Actual Track Details
	def getTopTrackDetailsThreadFn(self,artistname,trackname,callback):
		req = UrlRequest('http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key='+API_key+'&artist='+utils.urlfixer(artistname)+'&track='+utils.urlfixer(trackname)+'&format=json')
		print ('http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key='+API_key+'&artist='+utils.urlfixer(artistname)+'&track='+utils.urlfixer(trackname)+'&format=json')
		req.wait()
		result = req.result
		print (result)
		cachefile = os.path.join(self.lfmcachedir,artistname,utils.pathfixer(trackname))
		store = DictStore(cachefile)
		while not os.path.exists(cachefile) or not 'track' in store :
			print 'Had to sleep'
			store = DictStore(cachefile)
			time.sleep(1)
		track = store['track']['track']
		track.duration = int(result['track']['duration'])
		track.playcount = int(result['track']['playcount'])
		track.listeners = int(result['track']['listeners'])
		if 'album' in result['track']:
			track.album = result['track']['album']['title']
			track.coverart_low =result['track']['album']['image'][0]['#text'].replace("https:","http:")
			track.coverart_med = result['track']['album']['image'][1]['#text'].replace("https:","http:")
			track.coverart_high = result['track']['album']['image'][2]['#text'].replace("https:","http:")
			track.coverart_vhigh = result['track']['album']['image'][3]['#text'].replace("https:","http:")
			self.updateTrackArt(track)
		else:
			print ('No album data')
		track.tags =[]
		for i in range(len(result['track']['toptags']['tag'])):
			track.tags.append(result['track']['toptags']['tag'][i]['name'])
		if 'wiki' in result['track']:
			track.wiki = result['track']['wiki']['content']
		else:
			track.wiki = 'Not available. Could you contribute some information on LastFM'

		store['track'] = {'track':track, 'lastupdated':time.time(), 'actualtrackfetch':True}
		callback(track)

	#Gets the lyrics given trackname & artistname
	def getTrackLyrics(self, artistname , trackname, callback):
		cachefile = os.path.join(self.lfmcachedir,artistname,utils.pathfixer(trackname))
		store = DictStore(cachefile)
		if 'lyrics' in store:
			callback(store['lyrics']['lyrics'])
		else:
			Thread(target=self.getTrackLyricsThreadFn,args=(artistname,trackname,callback,)).start()

	#Threaded Function for Lyrics Fetching
	def getTrackLyricsThreadFn(self,artistname,trackname,callback):
		#TODO: Add artistname & trackname corrections to make the fetch more robust
		base_api_link = 'http://lyricscore.eu5.org/api/v1/?'
		request_url = base_api_link +'artist='+utils.urlfixer(artistname)+'&title='+utils.urlfixer(trackname)+'&format=xml'
		print (request_url)
		req =UrlRequest(request_url)
		req.wait()
		result = req.result
		print (result)
		result = result[result.index('<lyrics>')+8:result.rindex('</lyrics>')]
		result = result.replace('<br />','\n')
		cachefile = os.path.join(self.lfmcachedir,artistname,utils.pathfixer(trackname))
		store = DictStore(cachefile)
		store['lyrics']= {'lyrics':result}
		callback(result)

	#Checks if Track Art image exists if not it is refetched
	def updateTrackArt(self,track):
		imagelink = track.coverart_vhigh
		if imagelink ==None:
			return
		strippedname = "vh_"+imagelink[imagelink.rindex('/')+1:]
		imagepath = os.path.join(self.lfmcachedir,track.artist,strippedname)
		if not os.path.exists(imagepath):
			Thread(target=remotefilesaver,args=(imagelink,imagepath)).start()

	#Get the path for the Coverart Image 
	def getTrackCoverPath(self,track):
		cachefile = os.path.join(self.lfmcachedir,track.artist,utils.pathfixer(track.name))
		store = DictStore(cachefile)
		track = store['track']['track']
		imagelink = track.coverart_vhigh
		if imagelink == None:
			return self.getArtistCoverPath(track.artist)
		strippedname = 'vh_'+imagelink[imagelink.rindex('/')+1:]
		check_path = os.path.join(self.lfmcachedir,track.artist,strippedname)
		if os.path.exists(check_path):	#Check if the cached copy exists else return the link
			return check_path
		return imagelink




















		