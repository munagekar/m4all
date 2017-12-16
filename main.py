from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty
import lfm
import os

cache_folder= None

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        #This is required
        #[{'text': '0'}, {'text': '1'}, {'text': '2'}]
        lfm.getTopTracks(self.datafiller)
        self.data = []
    def datafiller(self,tracks):
        global cache_folder
        print ('Value of Cache_folder is')
        print (cache_folder)
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
    