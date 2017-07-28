# -*- coding: utf-8 -*-

from appconfig import Config
from appconnections import PICConnection
from appevents import Events
from appstatus import Status
from commands import piccommands
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from models.ac import AC
from models.light import Light
import os
from threading import Timer
from uix.mytabbedpanel import MyTabbedPanelItem
from uix.scenecontrol import SceneControl

path = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(os.path.join(path, 'lightsac.kv'))


class LightsAC(MyTabbedPanelItem):

    def __init__(self, **kwargs):
        super(LightsAC, self).__init__(**kwargs)
        self.can_update = True
        self.update_timer = None
        self.scene_control = None
        Events.on_status_config_update += self.load_light_controls
        Events.on_status_update += self.update_controls
        Events.on_control_change += self.start_update_timer

    def on_selected(self):
        if Config.ready:
            self.load_light_controls()

    def load_light_controls(self):
        dimmers = []
        on_offs = []
        for light in Status.lights:
            if light.type == Light.Types.dimmer:
                dimmers.append({'light': light})
            else:
                on_offs.append({'light': light})
        self.ids.lights_rv.data = dimmers + on_offs
        self.update_controls()
        if Config.config_mode:
            if not self.scene_control:
                self.scene_control = SceneControl()
                self.ids.lights_layout.add_widget(self.scene_control, 1)
        else:
            if self.scene_control:
                self.ids.lights_layout.remove_widget(self.scene_control)
                self.scene_control = None

    def update_controls(self, command=None):
        if self.can_update:
            for light_control in self.ids.lights_rv_layout.children:
                light_control.update_value(
                    Status.lights[light_control.light.number].value)
            self.ids.ac_power.update_status(Status.ac.status)
            self.ids.ac_temp.text = str(Status.ac.temp) + '°C'
            self.ids.ac_status.text = Status.ac.status_label
            self.ids.ac_mode.text = Status.ac.mode

    def enable_update(self):
        self.can_update = True

    def start_update_timer(self):
        self.can_update = False
        if self.update_timer:
            self.update_timer.cancel()
        self.update_timer = Timer(2.5, self.enable_update)
        self.update_timer.start()

    def ac_power(self):
        if Status.ac.status == AC.Status.off:
            Status.ac.set_status(AC.Status.turning_on.value)
            PICConnection.send_command(piccommands.ACOn(Status.ac.temp_code))
        elif Status.ac.status == AC.Status.on:
            Status.ac.set_status(AC.Status.turning_off.value)
            PICConnection.send_command(piccommands.ACOff())
        self.update_controls()
        self.start_update_timer()

    def ac_temp_down(self):
        if Status.ac.status == AC.Status.on:
            Status.ac.temp_down()
            PICConnection.send_command(
                piccommands.SetACTemp(Status.ac.temp_code))
            self.update_controls()
            self.start_update_timer()

    def ac_temp_up(self):
        self.update_controls()
        if Status.ac.status == AC.Status.on:
            Status.ac.temp_up()
            PICConnection.send_command(
                piccommands.SetACTemp(Status.ac.temp_code))
            self.update_controls()
            self.start_update_timer()


class LightsRV(RecycleView):

    def __init__(self, **kwargs):
        super(LightsRV, self).__init__(**kwargs)
