from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.storage.dictstore import DictStore
from kivy.uix.screenmanager import ScreenManager, Screen
import lfm
import os
import time

cache_folder= None
info_file = None
image_cache = None

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []
        self.getTracks()

    def getTracks(self):       #See if data exists and use if possible 
        global info_file
        global image_cache
        store = DictStore(info_file)
        lastupdated =0     #Time stamp when last updated assumed 1980
        
        
        needs_update =True      #Flag: Does the data need to be updated
        
        if 'toptracks' in store:
            lastupdated = store['toptracks']['lastupdated']
            tracks = store['toptracks']['toptracks']
            self.datafiller(tracks)
            if time.time() - lastupdated < 36000:
                needs_update = False
        
        if needs_update == True:
            lfm.getTopTracks(self.updateTracks)
            

            

    def updateTracks(self,tracks):
        global info_file
        global image_cache
        store = DictStore(info_file)
        store['toptracks']={'toptracks':tracks,'lastupdated':time.time()}
        self.datafiller(tracks)
        lfm.imageCachePopulator(tracks,image_cache)



    def datafiller(self,tracks):
        global image_cache
        lfm.cacheLocationFixer(tracks,image_cache)
        self.data =[{'imagelink':tracks[i].coverartlink_artist,'trackname':tracks[i].name,'trackartist':tracks[i].artist} for i in range(len(tracks))]

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
        global root_folder
        global cache_folder
        global info_file
        global image_cache
        root_folder = self.user_data_dir
        cache_folder = os.path.join(root_folder,'cache')
        image_cache = os.path.join(root_folder,'image_cache')
        info_file=os.path.join(cache_folder,'info')
        if not os.path.exists(cache_folder):
            os.makedirs(cache_folder)
        if not os.path.exists(image_cache):
            os.makedirs(image_cache)


if __name__ == '__main__':
    lfm.getTrackInfo('believe','cher',None)
    M4AllApp().run()
    