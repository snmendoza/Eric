from appconnections import SGHConnection
from appevents import Events
from appstatus import Status
from commands import sghcommands
import formatter
from appqpool import QPool
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

    def on_selected(self):
        SGHConnection.send_command(sghcommands.GetAccountInfo(),
                                   periodic=True,
                                   period=5)

    def on_unselected(self):
        print(sghcommands.GetAccountInfo.__name__)
        QPool.cancelJobs(sghcommands.GetAccountInfo.__name__)

    def update(self):
        self.ids.date.text = formatter.as_date(Status.date)
        self.ids.time.text = formatter.as_time(Status.time)
        if Status.service_open:
            self.ids.shift_start.text = formatter.as_time(Status.shift_start) \
                if Status.shift_start else self.DEFAULT_TIME
            self.ids.shift_end.text = formatter.as_time(Status.shift_end) \
                if Status.shift_end else self.DEFAULT_TIME
            self.ids.alarm.text = formatter.as_time(Status.alarm) \
                if Status.alarm else self.DEFAULT_TIME
            self.ids.lodging.text = formatter.as_money(Status.lodging)
            self.ids.surcharge.text = formatter.as_money(Status.surcharge)
            self.ids.bar.text = formatter.as_money(Status.bar)
            self.ids.bonus.text = formatter.as_money(Status.bonus)
            self.ids.discount.text = formatter.as_money(Status.discount)
            self.ids.paid.text = formatter.as_money(Status.paid)
            self.ids.total.text = formatter.as_money(Status.total)
            self.ids.special_offer.text = Status.special_offer
        else:
            self.ids.shift_start.text = self.DEFAULT_TIME
            self.ids.shift_end.text = self.DEFAULT_TIME
            self.ids.alarm.text = self.DEFAULT_TIME
            self.ids.lodging.text = formatter.as_money(0)
            self.ids.surcharge.text = formatter.as_money(0)
            self.ids.bar.text = formatter.as_money(0)
            self.ids.bonus.text = formatter.as_money(0)
            self.ids.discount.text = formatter.as_money(0)
            self.ids.paid.text = formatter.as_money(0)
            self.ids.total.text = formatter.as_money(0)
            self.ids.special_offer.text = self.DEFAULT_TEXT
