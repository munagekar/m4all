from kivy.app import App
from kivy.uix.widget import Widget

class MainDisplay(Widget):
    print ('I reached here')
    pass

class M4AllApp(App):
    def build(self):
        return MainDisplay()


if __name__ == '__main__':
    M4AllApp().run()
