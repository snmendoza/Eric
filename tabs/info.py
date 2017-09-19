from appevents import Events
from appstatus import Status
import formatter
from kivy.lang import Builder
import os
from uix.mytabbedpanel import MyTabbedPanelItem

path = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(os.path.join(path, 'info.kv'))


class Info(MyTabbedPanelItem):

    DEFAULT_TIME = '--:--'
    DEFAULT_TEXT = '----'

    def __init__(self, **kwargs):
        super(Info, self).__init__(**kwargs)
        Events.on_account_update += self.update

    def update(self):
        self.ids.date = formatter.as_date(Status.date)
        self.ids.time = formatter.as_time(Status.time)
        if Status.service_open:
            self.ids.shift_start = formatter.as_time(Status.shift_start)
            self.ids.shift_end = formatter.as_time(Status.shift_end)
            self.ids.alarm = formatter.as_time(Status.alarm)
            self.ids.lodging = formatter.as_money(Status.lodging)
            self.ids.surcharge = formatter.as_money(Status.surcharge)
            self.ids.bar = formatter.as_money(Status.bar)
            self.ids.bonus = formatter.as_money(Status.bonus)
            self.ids.paid = formatter.as_money(Status.paid)
            self.ids.total = formatter.as_money(Status.total)
            self.ids.special_offer = Status.special_offer
        else:
            self.ids.shift_start = self.DEFAULT_TIME
            self.ids.shift_end = self.DEFAULT_TIME
            self.ids.alarm = self.DEFAULT_TIME
            self.ids.lodging = formatter.as_money(0)
            self.ids.surcharge = formatter.as_money(0)
            self.ids.bar = formatter.as_money(0)
            self.ids.bonus = formatter.as_money(0)
            self.ids.paid = formatter.as_money(0)
            self.ids.total = formatter.as_money(0)
            self.ids.special_offer = self.DEFAULT_TEXT
