from appconfig import Config
from appevents import Events
from models.ac import AC


class Status(object):

    def __init__(self):
        self.ac = AC()
        self.lights = []
        Events.on_config_ready = self.update_from_config
        Events.on_config_update = self.update_from_config
        Events.on_pic_status = self.update_status

    def update_from_config(self):
        for idx, light in enumerate(Config.lights):
            if idx < len(self.lights):
                light.set_value(self.lights[idx].value)
        self.lights = Config.lights
        Events.on_status_config_update()

    def update_from_command(self, command):
        self.ac.update_from_command(command)
        map(lambda light: light.update_from_command(command), self.lights)
        Events.on_status_update()
