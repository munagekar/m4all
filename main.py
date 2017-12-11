from kivy.app import App
from kivy.uix.widget import Widget
from kivy.network.urlrequest import UrlRequest
from kivy.uix.recycleview import RecycleView


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in range(100)]

class MainDisplay(Widget):
    pass

class M4AllApp(App):
    def build(self):
        mainDisplay = MainDisplay()
        return mainDisplay

def got_json(req, result):
    print (result)




if __name__ == '__main__':
    req = UrlRequest('http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key=f420e235b5a52c620114d88c28b6f186&format=json', on_success=got_json) 
    M4AllApp().run()
    