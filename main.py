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

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []
        self.getTracks()

    def getTracks(self):       #See if data exists and use if possible 
        store = DictStore('info')
        lastupdated =0     #Time stamp when last updated assumed 1980
        needs_update =True      #Flag: Does the data need to be updated
        if 'toptracks' in store:
            lastupdated = store['toptracks']['lastupdated']
            tracks = store['toptracks']['toptracks']
            self.datafiller(tracks)
            if time.time() - lastupdated < 36000:
                needs_update = False

        if needs_update == True:
            lfm.getTopTracks(self.updateTracks,50)
            

    def updateTracks(self,tracks):
        store = DictStore('info')
        store['toptracks']={'toptracks':tracks,'lastupdated':time.time()}
        self.datafiller(tracks)


    def datafiller(self,tracks):
        self.data =[{'displaytext':"[b]"+tracks[i].name+"\n-"+tracks[i].artist+"[/b]",'imagelink':(tracks[i].coverartlink).replace("https:","http:")} for i in range(len(tracks))]


class GridItem(FloatLayout):
    displaytext =StringProperty()
    imagelink = StringProperty()
    #aimg = AsyncImage(source=imagelink)
    pass
        

class MainDisplay(Widget):
    pass

class M4AllApp(App):
    def build(self):
        mainDisplay = MainDisplay()
        self.initilize_global_vars()
        return mainDisplay

    def initilize_global_vars(self):
        global root_folder
        global cache_folder
        root_folder = self.user_data_dir
        cache_folder = os.path.join(root_folder,'cache')

        if not os.path.exists(cache_folder):
            os.makedirs(cache_folder)



if __name__ == '__main__':
    
    #lfm.getTopTracks()
    M4AllApp().run()
    