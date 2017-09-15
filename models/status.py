from appconfig import Config
from appevents import Events
from datetime import date, datetime, time
from models.ac import AC


class Status(object):

    def __init__(self):
        self.ac = AC()
        self.lights = []
        self.date = date.today()
        self.time = time()
        self.service_open = False
        self.shift_start = None
        self.shift_end = None
        self.alarm = None
        self.lodging = 0
        self.surcharge = 0
        self.bar = 0
        self.bonus = 0
        self.discount = 0
        self.paid = 0
        self.total = 0
        self.special_offer = None
        Events.on_config_ready += self.update_from_config
        Events.on_config_update += self.update_from_config
        Events.on_pic_status += self.update_from_command
        Events.on_sgh_account_info += self.update_account_from_command

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

    def update_account_from_command(self, command):
        self.date = datetime.strptime(command[1:7], '%d%m%y').date()
        self.time = datetime.strptime(command[7:11], '%H%M').time()
        self.service_open = bool(command[11])
        self.shift_start = datetime.strptime(command[12:16], '%H%M').time()
        self.shift_end = datetime.strptime(command[16:20], '%H%M').time()
        self.alarm = datetime.strptime(command[20:24], '%H%M').time()
        self.lodging = command[24:30]
        self.surcharge = command[30:36]
        self.bar = command[36:42]
        self.bonus = command[42:48]
        self.discount = command[48:54]
        self.paid = command[54:60]
        self.total = command[60:66]
        self.special_offer = command[66:96]
        Events.on_account_update()
