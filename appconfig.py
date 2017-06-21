import json
from kivy.logger import Logger
from models.light import Light


class AppConfigParser(object):

    def read_file(self):
        Logger.info(__name__ + ': Reading config file')
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

AppConfig = AppConfigParser()
