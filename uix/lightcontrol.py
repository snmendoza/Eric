from appconfig import Config
from appconnections import PICConnection
from appevents import Events
from commands import piccommands
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton
from models.light import Light
import os

path = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(os.path.join(path, 'lightcontrol.kv'))


class LightControl(BoxLayout):

    light = ObjectProperty()

    def __init__(self, **kwargs):
        super(LightControl, self).__init__(**kwargs)
        self.control = None

    def on_light(self, instance, value):
        if self.control:
            self.remove_widget(self.control)
        self.ids.name.text = self.light.name
        self.control = \
            Dimmer() if self.light.type == Light.Types.dimmer else OnOff()
        self.add_widget(self.control)

    def update_value(self, value):
        self.control.update_value(self.light.value)

    def set_bright(self):
        if Config.ready:
            PICConnection.send_command(piccommands.SetBright(
                [light.value for light in Config.lights]))
            Events.on_control_change()


class Dimmer(Slider):

    def update_value(self, value):
        self.value = value

    def set_bright(self):
        self.parent.light.set_value(self.value)
        self.parent.set_bright()


class OnOff(ToggleButton):

    def update_value(self, value):
        self.state = 'down' if value else 'normal'

    def set_bright(self):
        self.parent.light.set_value(100 if self.state == 'down' else 0)
        self.parent.set_bright()
