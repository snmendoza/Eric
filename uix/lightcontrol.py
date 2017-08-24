from appconnections import PICConnection
from appstatus import Status
from commands import piccommands
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, ObjectProperty
from kivy.lang import Builder
from models.light import Light
import os
from uix.myslider import MySlider
from uix.mytogglebutton import MyToggleButton

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
        if value == self.control.value:
            self.control.on_value(self.control, value)
        self.control.value = value

    def set_bright(self):
        self.dispatch('on_set_bright')
        PICConnection.send_command(piccommands.SetBright(
             [light.value for light in Status.lights]))

    def on_set_bright(self):
        pass


class Dimmer(MySlider):

    def __init__(self, **kwargs):
        super(Dimmer, self).__init__(**kwargs)
        self.max = 100
        self.bind(on_release=self.set_bright)

    def on_value(self, instance, value):
        self.value = value

    def set_bright(self, instance):
        self.parent.light.set_value(self.value)
        self.parent.set_bright()


class OnOff(MyToggleButton):

    value = NumericProperty()

    def on_value(self, instance, value):
        self.state = 'down' if value else 'normal'

    def set_bright(self):
        self.parent.light.set_value(100 if self.state == 'down' else 0)
        self.parent.set_bright()
