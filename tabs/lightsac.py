from appconfig import AppConfig
from appevents import AppEvents
from kivy.uix.recycleview import RecycleView
from kivy.uix.tabbedpanel import TabbedPanelItem


class LightsAC(TabbedPanelItem):

    def on_selected(self):
        if AppConfig.ready:
            self.load_light_controls()
        AppEvents.on_cofig_changed += self.load_light_controls()
        AppEvents.on_pic_status += self.update_controls()

    def on_unselected(self):
        pass

    def load_light_controls(self):
        pass

    def update_controls(self):
        pass


class LightsRV(RecycleView):

    def __init__(self, **kwargs):
        super(LightsRV, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in range(100)]
