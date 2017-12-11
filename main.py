from kivy.app import App
from kivy.uix.widget import Widget
from kivy.network.urlrequest import UrlRequest
from kivy.uix.recycleview import RecycleView

import json

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

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        #This is required
        #[{'text': '0'}, {'text': '1'}, {'text': '2'}]
        self.data = [{'text': str(x)} for x in range(3)]
        

class MainDisplay(Widget):
    pass

class M4AllApp(App):
    def build(self):
        mainDisplay = MainDisplay()
        return mainDisplay

def topTrackParser(req, result):
    
    jsonresult = result
    jsontracklist = jsonresult['tracks']['track']
    tracks =[]
    for i in range(1):
        jsontrack =jsontracklist[i]
        trackname = jsontrack['name']
        print(trackname)
        trackartist = jsontrack['artist']['name']
        print(trackartist)
        trackurl = jsontrack['url']
        print(trackurl)
        trackart = jsontrack['image'][1]['#text']
        print(trackart)
        tracks.append(Track(trackname,trackartist,trackart,trackurl))

    

def getTopTracks():
    result = UrlRequest('http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key=f420e235b5a52c620114d88c28b6f186&format=json', on_success=topTrackParser) 
    






if __name__ == '__main__':
    
    getTopTracks()
    M4AllApp().run()
    