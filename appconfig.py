from appevents import Events
import hashlib
import inspect
import json
from kivy.logger import Logger
from models.light import Light
import os


class ConfigParser(object):

    def __init__(self):
        self.md5hash = None
        self.ready = False

    def read_file(self):
        Logger.debug(__name__ + ': Reading config file')
        try:
            script_dir = os.path.dirname(
                os.path.abspath(inspect.getfile(inspect.currentframe())))
            config_file = open(script_dir + '/config.json')
            md5hash = hashlib.md5(config_file.read()).hexdigest()
            if self.md5hash != md5hash:
                Logger.info(__name__ + ': Config file updated')
                config_file.seek(0)
                config = json.load(config_file)
                self.config_mode = config['config_mode']
                self.room_number = config['room_number']
                self.m3s_address = config['m3s_address']
                self.sgh_address = config['sgh_address']
                self.sgh_port = config['sgh_port']
                self.full_version = self.sgh_address and self.sgh_port
                self.pic_address = config['pic_address']
                self.audio_mixer = config['audio_mixer']
                self.audio_device = config['audio_device']
                self.tv_remote_code = config['tv_remote_code']
                self.ac_controls = config['ac_controls']
                self.lights = []
                for idx, light in enumerate(config['lights']):
                    self.lights.append(Light(light['name'], idx, light['type']))
                self.md5hash = md5hash
                if not self.ready:
                    self.ready = True
                    Events.on_config_ready()
                else:
                    Events.on_config_update()
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
            return True


Config = ConfigParser()
