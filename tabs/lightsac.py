# -*- coding: utf-8 -*-

from appconfig import Config
from appevents import Events
from appstatus import Status
from kivy.lang import Builder
from models.light import Light
import os
from threading import Timer
from uix.mytabbedpanel import MyTabbedPanelItem
from uix.lightcontrol import LightControl
from uix.scenecontrol import SceneControl

path = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(os.path.join(path, 'lightsac.kv'))


class LightsAC(MyTabbedPanelItem):

    LIGHTS_TITLE = 'LUCES'
    AC_TITLE = '/AIRE'

    def __init__(self, **kwargs):
        super(LightsAC, self).__init__(**kwargs)
        self.lights = []
        self.can_update = True
        self.update_timer = None
        self.scene_control = None
        Events.on_status_config_update += self.load_controls
        Events.on_status_update += self.update_controls

    def on_selected(self):
        if Config.ready:
            self.load_controls()

    def load_controls(self):
        self.lights = Status.lights
        self.ids.dimmers_layout.clear_widgets()
        self.ids.on_offs_layout.clear_widgets()
        for light in self.lights:
            light_control = LightControl(
                light=light)
            light_control.bind(on_set_bright=self.start_update_timer)
            if light.type == Light.Types.dimmer:
                self.ids.dimmers_layout.add_widget(light_control)
            elif light.type == Light.Types.on_off:
                self.ids.on_offs_layout.add_widget(light_control)
        self.update_controls()
        if Config.config_mode:
            if not self.scene_control:
                self.scene_control = SceneControl()
                self.ids.lights_layout.add_widget(self.scene_control, 1)
        else:
            if self.scene_control:
                self.ids.lights_layout.remove_widget(self.scene_control)
                self.scene_control = None

    def update_controls(self):
        if self.can_update:
            for light_control in self.ids.dimmers_layout.children:
                light_control.update_value(
                    Status.lights[light_control.light.number].value)
            for light_control in self.ids.on_offs_layout.children:
                light_control.update_value(
                    Status.lights[light_control.light.number].value)

    def enable_update(self):
        self.can_update = True

    def start_update_timer(self, instance):
        self.can_update = False
        if self.update_timer:
            self.update_timer.cancel()
        self.update_timer = Timer(5, self.enable_update)
        self.update_timer.start()
