from appconfig import AppConfig
from appevents import AppEvents
from commands import piccommands
from connections.wrappers import PICCW
from jobq.qpool import AppQPool
from kivy.uix.recycleview import RecycleView
from kivy.uix.tabbedpanel import TabbedPanelItem
from models.ac import AC
from threading import Timer


class LightsAC(TabbedPanelItem):

    def __init__(self, **kwargs):
        super(LightsAC, self).__init__(**kwargs)
        self.ac = AC()
        self.lights = []
        self.can_update = True
        self.update_timer = None

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
        if self.can_update:
            pass

    def enable_update(self):
        self.can_update = True

    def start_update_timer(self):
        self.can_update = False
        if self.update_timer:
            self.update_timer.cancel()
        self.update_timer = Timer(1000, self.enable_update)
        self.update_timer.start()

    def ac_power(self):
        if self.ac.status == AC.Status.off:
            self.ac.status = AC.Status.turning_on
            PICCW.send_command(piccommands.ACOn(self.ac.temp_code))
        elif self.ac.status == AC.Status.on:
            self.ac.status = AC.Status.turning_off
            PICCW.send_command(piccommands.ACOff())
        self.start_update_timer()
        self.update_controls()

    def ac_temp_down(self):
        if self.ac.status == AC.Status.on:
            self.ac.temp_down()
            PICCW.send_command(piccommands.SetACTemp(self.ac.temp_code))
            self.start_update_timer()
            self.update_controls()

    def ac_temp_up(self):
        if self.ac.status == AC.Status.on:
            self.ac.temp_up()
            PICCW.send_command(piccommands.SetACTemp(self.ac.temp_code))
            self.start_update_timer()
            self.update_controls()


class LightsRV(RecycleView):

    def __init__(self, **kwargs):
        super(LightsRV, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in range(100)]
