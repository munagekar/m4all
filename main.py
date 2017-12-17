from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.storage.dictstore import DictStore
import lfm
import os
import time

cache_folder= None
info_file = None

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []
        self.getTracks()

    def getTracks(self):       #See if data exists and use if possible 
        global info_file
        store = DictStore(info_file)
        print (info_file)
        lastupdated =0     #Time stamp when last updated assumed 1980
        
        
        needs_update =True      #Flag: Does the data need to be updated
        
        if 'toptracks' in store:
            print('The store exists')
            lastupdated = store['toptracks']['lastupdated']
            tracks = store['toptracks']['toptracks']
            self.datafiller(tracks)
            if time.time() - lastupdated < 36000:
                needs_update = False
        else:
            print('couldnt find the store')
        
        if needs_update == True:
            print ('I needed an update')
            lfm.getTopTracks(self.updateTracks,50)
            

    def updateTracks(self,tracks):
        global info_file
        store = DictStore(info_file)
        store['toptracks']={'toptracks':tracks,'lastupdated':time.time()}
        self.datafiller(tracks)


    def datafiller(self,tracks):
        self.data =[{'displaytext':"[b]"+tracks[i].name+"\n-"+tracks[i].artist+"[/b]",'imagelink':tracks[i].coverartlink} for i in range(len(tracks))]
        for i in range(len(tracks)):
            print (tracks[i].coverartlink)

class GridItem(FloatLayout):
    displaytext =StringProperty()
    imagelink = StringProperty()
    #aimg = AsyncImage(source=imagelink)
    pass
        

class MainDisplay(Widget):
    pass

class M4AllApp(App):
    def build(self):
        self.initilize_global_vars()
        mainDisplay = MainDisplay()
        return mainDisplay

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
    time.time()
    #lfm.getTopTracks()
    M4AllApp().run()
    