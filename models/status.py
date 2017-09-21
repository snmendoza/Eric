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
        self.date = self.get_date(command.params[1:7])
        self.time = self.get_time(command.params[7:11])
        self.service_open = bool(command.params[11])
        self.shift_start = self.get_time(command.params[12:16])
        self.shift_end = self.get_time(command.params[16:20])
        self.alarm = self.get_time(command.params[20:24])
        self.lodging = self.get_int(command.params[24:30])
        self.surcharge = self.get_int(command.params[30:36])
        self.bar = self.get_int(command.params[36:42])
        self.bonus = self.get_int(command.params[42:48])
        self.discount = self.get_int(command.params[48:54])
        self.paid = self.get_int(command.params[54:60])
        self.total = self.get_int(command.params[60:66])
        self.special_offer = self.get_str(command.params[66:96])
        Events.on_account_update()

    def get_date(self, params):
        try:
            return datetime.strptime(self.get_str(params), '%d%m%y').date()
        except:
            return None

    def get_time(self, params):
        try:
            return datetime.strptime(self.get_str(params), '%H%M').time()
        except:
            return None

    def get_str(self, params):
        return ''.join(map(lambda val: chr(val), params))

    def get_int(self, params):
        try:
            return int(self.get_str(params))
        except:
            return 0
