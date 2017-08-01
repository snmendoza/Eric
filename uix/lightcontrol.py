from appconnections import PICConnection
from appstatus import Status
from commands import piccommands
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ObjectProperty
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
        self.register_event_type('on_set_bright')
        self.control = None

    def on_light(self, instance, value):
        if self.control:
            self.remove_widget(self.control)
        self.ids.name.text = self.light.name
        self.control = \
            Dimmer() if self.light.type == Light.Types.dimmer else OnOff()
        self.add_widget(self.control)

    def update_value(self, value):
        self.control.value = value

    def set_bright(self):
        self.dispatch('on_set_bright')
        PICConnection.send_command(piccommands.SetBright(
             [light.value for light in Status.lights]))

    def on_set_bright(self):
        pass


class Dimmer(Slider):

    def on_touch_up(self, touch):
        super(Dimmer, self).on_touch_up(touch)
        if touch.grab_current is self:
            self.parent.light.set_value(self.value)
            self.parent.set_bright()
            touch.ungrab(self)
            return True


class OnOff(ToggleButton):

    value = NumericProperty()

    def on_value(self, instance, value):
        self.state = 'down' if value else 'normal'

    def set_bright(self):
        self.parent.light.set_value(100 if self.state == 'down' else 0)
        self.parent.set_bright()
