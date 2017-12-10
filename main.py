from kivy.app import App
from kivy.uix.widget import Widget
from kivy.network.urlrequest import UrlRequest

class MainDisplay(Widget):
    print ('I reached here')
    pass

class M4AllApp(App):
    def build(self):
        mainDisplay = MainDisplay()
        return mainDisplay

def got_json(req, result):
    print ('Reached here')
    print (result)


if __name__ == '__main__':
    req = UrlRequest('http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country=india&api_key=f420e235b5a52c620114d88c28b6f186&format=json', on_success=got_json)
    M4AllApp().run()
    