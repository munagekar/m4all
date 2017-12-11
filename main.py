from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView

import lfm


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



    


    






if __name__ == '__main__':
    
    lfm.getTopTracks()
    M4AllApp().run()
    