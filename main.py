import kivy
from kivy.app import App
from kivy.config import Config

kivy.require('1.9.1')


class EricApp(App):
    pass

if __name__ == '__main__':
    Config.set('graphics', 'fullscreen', 'auto')
    EricApp().run()
