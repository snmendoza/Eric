from appevents import AppEvents
import hashlib
import json
from kivy.logger import Logger
from models.light import Light


class AppConfigParser(object):

    def __init__(self):
        self.md5hash = None
        self.ready = False

    def read_file(self):
        Logger.debug(__name__ + ': Reading config file')
        try:
            config_file = open('config.json')
            md5hash = hashlib.md5(config_file.read()).hexdigest()
            if self.md5hash != md5hash:
                Logger.info(__name__ + ': Config file updated')
                config_file.seek(0)
                config = json.load(config_file)
                self.room_number = config['room_number']
                self.sgh_address = config['sgh_address']
                self.sgh_port = config['sgh_port']
                self.pic_address = config['pic_address']
                self.tv_remote_code = config['tv_remote_code']
                self.lights = []
                for idx, light in enumerate(config['lights']):
                    self.lights.append(Light(idx, light['type']))
                AppEvents.on_config_changed()
        except IOError:
            Logger.error(__name__ + ': config.json cannot be opened')
            return False
        except KeyError as e:
            Logger.error(__name__ + ': Config file is missing a key: ' + str(e))
            config_file.close()
            return False
        except ValueError:
            Logger.error(__name__ + ': Malformed config file')
            config_file.close()
            return False
        else:
            config_file.close()
            self.md5hash = md5hash
            self.ready = True
            return True

AppConfig = AppConfigParser()
