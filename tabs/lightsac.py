# -*- coding: utf-8 -*-

from appconfig import Config
from appconnections import PICConnection
from appevents import Events
from appstatus import Status
from commands import piccommands
from kivy.lang import Builder
from models.ac import AC
import os
from threading import Timer
from uix.mytabbedpanel import MyTabbedPanelItem
from uix.scenecontrol import SceneControl

path = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(os.path.join(path, 'lightsac.kv'))


class LightsAC(MyTabbedPanelItem):

    def __init__(self, **kwargs):
        super(LightsAC, self).__init__(**kwargs)
        self.lights = []
        self.can_update = True
        self.update_timer = None
        self.scene_control = None
        Events.on_status_config_update += self.load_light_controls
        Events.on_status_update += self.update_controls

    def on_selected(self):
        if Config.ready:
            self.load_light_controls()

    def load_light_controls(self):
        # dimmers go before on off lights
        self.lights = \
            sorted(Status.lights, key=lambda light: light.type.value)
        self.ids.lights_rv.data = \
            map(lambda light:
                {'light': light, 'on_set_bright': self.start_update_timer},
                self.lights)
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
            for light_control in self.ids.lights_rv.layout_manager.children:
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

    def ac_temp(self, direction):
        if Status.ac.status == AC.Status.on:
            {
                'up': Status.ac.temp_up,
                'down': Status.ac.temp_down
            }[direction]()
            PICConnection.send_command(
                piccommands.SetACTemp(Status.ac.temp_code))
            self.update_controls()
            self.start_update_timer()
