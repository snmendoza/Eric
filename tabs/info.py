from appevents import Events
from appstatus import Status
from formatter import Formatter
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
        self.ids.date = Formatter.as_date(Status.date)
        self.ids.time = Formatter.as_time(Status.time)
        if Status.service_open:
            self.ids.shift_start = Formatter.as_time(Status.shift_start)
            self.ids.shift_end = Formatter.as_time(Status.shift_end)
            self.ids.alarm = Formatter.as_time(Status.alarm)
            self.ids.lodging = Formatter.as_money(Status.lodging)
            self.ids.surcharge = Formatter.as_money(Status.surcharge)
            self.ids.bar = Formatter.as_money(Status.bar)
            self.ids.bonus = Formatter.as_money(Status.bonus)
            self.ids.paid = Formatter.as_money(Status.paid)
            self.ids.total = Formatter.as_money(Status.total)
            self.ids.special_offer = Status.special_offer
        else:
            self.ids.shift_start = self.DEFAULT_TIME
            self.ids.shift_end = self.DEFAULT_TIME
            self.ids.alarm = self.DEFAULT_TIME
            self.ids.lodging = Formatter.as_money(0)
            self.ids.surcharge = Formatter.as_money(0)
            self.ids.bar = Formatter.as_money(0)
            self.ids.bonus = Formatter.as_money(0)
            self.ids.paid = Formatter.as_money(0)
            self.ids.total = Formatter.as_money(0)
            self.ids.special_offer = self.DEFAULT_TEXT
