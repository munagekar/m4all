from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from lfm import LfmHelper
import os
import time

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

class TopTrackScreen(Screen):
    pass

class SongScreen(Screen):
    pass

class M4AllApp(App):
    def build(self):
        self.initilize_global_vars()
        
        sm = ScreenManager()
        sm.add_widget(TopTrackScreen(name='toptracks'))
        sm.add_widget(SongScreen(name='song'))
        return sm
        

    def initilize_global_vars(self):
        global lfm
        root_folder = self.user_data_dir
        lfm = LfmHelper(root_folder)

if __name__ == '__main__':
    M4AllApp().run()
    