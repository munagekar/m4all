from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from lfm import LfmHelper
import os
import time
import utils


#Global Variables
#Screen Manager
sm = None
songscreen = None



lfm = None          #LFM helper object- easy interface to Lfm with caching, threading support

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []
        self.getTracks()

    def getTracks(self):       #See if data exists and use if possible 
        global lfm
        lfm.getTopTracks(self.datafiller)

    def datafiller(self,tracks):
        print ('Reached here inside datafiller')
        #Got the Tracks now get the artist coverartlink
        imagepaths = []
        for i in range(len(tracks)):
            imagepaths.append(lfm.getArtistCoverPath(tracks[i].artist))
        self.data =[{'imagelink':imagepaths[i],'trackname':tracks[i].name,'trackartist':tracks[i].artist} for i in range(len(tracks))]

class GridItem(FloatLayout):
    trackname = StringProperty()
    trackartist = StringProperty()
    imagelink = StringProperty()

    def on_press_action(self):
        global sm
        sm.current='song'
        songscreen.update(self.trackname,self.trackartist)



class TopTrackScreen(Screen):
    pass


class SongScreen(Screen):
    trackname = StringProperty()
    trackartist = StringProperty()
    listeners = StringProperty()
    playcount = StringProperty()
    imagelink = StringProperty()
    wiki = StringProperty()
    lyrics = StringProperty()
    duration = StringProperty()
    trackimage = StringProperty()

    def reset(self):
        self.listeners = 'Updating'
        self.playcount = 'Updating'
        self.wiki = 'fetching'
        self.lyrics = 'fetching'
        self.duration = 'Updating'
        self.trackimage = 'test.png'

    def update(self,trackname, trackartist):
        self.reset()
        self.trackname = trackname
        self.trackartist = trackartist
        lfm.getTrackDetails(trackartist,trackname,self.setDetails)
        lfm.getTrackLyrics(trackartist,trackname,self.setLyrics)

    def setLyrics(self,lyrics): #Callback Function for setting the lyrics
        self.lyrics = lyrics

    def setDetails(self,track):
        global lfm
        #TODO ADD More stuff inside this function
        self.playcount = utils.easyreadnum(track.playcount)
        self.listeners = utils.easyreadnum(track.listeners)
        self.wiki = track.wiki
        self.duration = str(track.duration)
        self.trackimage = lfm.getTrackCoverPath(track)
        tagstackitems = [self.ids.tagstack1,self.ids.tagstack2,self.ids.tagstack3,self.ids.tagstack4,self.ids.tagstack5]
        for i in range(len(track.tags)):
            tagstackitems[i].text = track.tags[i]



class M4AllApp(App):
    def build(self):
        self.initilize_global_vars()
        global sm
        global songscreen
        sm = ScreenManager()
        sm.add_widget(TopTrackScreen(name='toptracks'))
        songscreen = SongScreen(name='song')
        sm.add_widget(songscreen)
        return sm
        

    def initilize_global_vars(self):
        global lfm
        root_folder = self.user_data_dir
        lfm = LfmHelper(root_folder)

if __name__ == '__main__':
    M4AllApp().run()
    