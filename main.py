import json
import kivy
from kivy.app import App
from kivy.config import Config
from models.light import Light

kivy.require('1.9.1')


class EricApp(App):

    def on_start(self):
        self.read_config()

    def read_config(self):
        with open('config.json') as config_file:
            config = json.load(config_file)
            self.room_number = config['room_number']
            self.sgh_address = config['sgh_address']
            self.sgh_port = config['sgh_port']
            self.pic_address = config['pic_address']
            self.tv_remote_code = config['tv_remote_code']
            self.lights = []
            for light in config['lights']:
                self.lights.append(Light(light['type']))

if __name__ == '__main__':
    Config.set('graphics', 'fullscreen', 'auto')
    EricApp().run()
