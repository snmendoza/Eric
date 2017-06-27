from appconfig import AppConfig
from appevents import AppEvents
from commands import piccommands
from connections.wrappers import PICCW
from jobq.qpool import AppQPool
from kivy.uix.recycleview import RecycleView
from kivy.uix.tabbedpanel import TabbedPanelItem
from models.ac import AC


class LightsAC(TabbedPanelItem):

    def __init__(self, **kwargs):
        super(LightsAC, self).__init__(**kwargs)
        self.ac = AC()

    def on_selected(self):
        if AppConfig.ready:
            self.load_light_controls()
        AppEvents.on_cofig_changed += self.load_light_controls()
        AppEvents.on_pic_status += self.update_controls()
        PICCW.send_command(piccommands.GetStatus(), periodic=True, period=1000)

    def on_unselected(self):
        AppQPool.cancelJobs(piccommands.GetStatus.__name__)

    def load_light_controls(self):
        pass

    def update_controls(self):
        pass

    def ac_power(self):
        if self.ac.status == AC.Status.off:
            PICCW.send_command(piccommands.ACOn(self.ac.temp_code))
        elif self.ac.status == AC.Status.on:
            PICCW.send_command(piccommands.ACOff())

    def ac_temp_down(self):
        if self.ac.status == AC.Status.on:
            self.ac.temp_down()
            PICCW.send_command(piccommands.SetACTemp(self.ac.temp_code))

    def ac_temp_up(self):
        if self.ac.status == AC.Status.on:
            self.ac.temp_up()
            PICCW.send_command(piccommands.SetACTemp(self.ac.temp_code))


class LightsRV(RecycleView):

    def __init__(self, **kwargs):
        super(LightsRV, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in range(100)]
