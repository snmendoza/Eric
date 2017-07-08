# -*- coding: utf-8 -*-

from appconfig import AppConfig
from appevents import AppEvents
from commands import piccommands
from connections.wrappers import PICCW
from jobq.qpool import AppQPool
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.recycleview import RecycleView
from kivy.uix.slider import Slider
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.togglebutton import ToggleButton
from models.ac import AC
from models.light import Light
from threading import Timer


class LightsAC(TabbedPanelItem):

    def __init__(self, **kwargs):
        super(LightsAC, self).__init__(**kwargs)
        self.ac = AC()
        self.can_update = True
        self.update_timer = None
        self.scene_control = None
        AppEvents.on_config_changed += self.load_light_controls
        AppEvents.on_config_changed += self.record_light_types
        AppEvents.on_pic_status += self.update_controls

    def on_selected(self):
        if AppConfig.ready:
            self.load_light_controls()
            self.record_light_types()
        PICCW.send_command(piccommands.GetStatus(), periodic=True, period=1000)

    def on_unselected(self):
        AppQPool.cancelJobs(piccommands.GetStatus.__name__)

    def record_light_types(self):
        light_types = [0 if light.type == Light.TYPE_DIMMER else 1
                       for light in AppConfig.lights]
        PICCW.send_command(
            piccommands.RecordLightTypes(light_types),
            retry=True,
            period=5000)

    def load_light_controls(self):
        dimmers = []
        on_offs = []
        for light in AppConfig.lights:
            if light.type == Light.TYPE_DIMMER:
                dimmers.append({'light': light})
            else:
                on_offs.append({'light': light})
        self.ids.lights_rv.data = dimmers + on_offs
        self.update_controls()
        if AppConfig.config_mode:
            if not self.scene_control:
                self.scene_control = SceneControl()
                self.ids.lights_layout.add_widget(self.scene_control, 1)
        else:
            if self.scene_control:
                self.ids.lights_layout.remove_widget(self.scene_control)
                self.scene_control = None

    def update_controls(self, command=None):
        if self.can_update:
            if command:
                self.ac.update_from_command(command)
                if AppConfig.ready:
                    for light in AppConfig.lights:
                        light.update_from_command(command)
            for light_control in self.ids.lights_rv_layout.children:
                light_control.update_value(
                    AppConfig.lights[light_control.light.number].value)
            self.ids.ac_power.update_status(self.ac.status)
            self.ids.ac_temp.text = str(self.ac.temp) + '°C'
            self.ids.ac_status.text = self.ac.status_label
            self.ids.ac_mode.text = self.ac.mode

    def enable_update(self):
        self.can_update = True

    def start_update_timer(self):
        self.can_update = False
        if self.update_timer:
            self.update_timer.cancel()
        self.update_timer = Timer(1, self.enable_update)
        self.update_timer.start()

    def ac_power(self):
        if self.ac.status == AC.Status.off:
            self.ac.set_status(AC.Status.turning_on.value)
            PICCW.send_command(piccommands.ACOn(self.ac.temp_code))
        elif self.ac.status == AC.Status.on:
            self.ac.set_status(AC.Status.turning_off.value)
            PICCW.send_command(piccommands.ACOff())
        self.update_controls()
        self.start_update_timer()

    def ac_temp_down(self):
        if self.ac.status == AC.Status.on:
            self.ac.temp_down()
            PICCW.send_command(piccommands.SetACTemp(self.ac.temp_code))
            self.update_controls()
            self.start_update_timer()

    def ac_temp_up(self):
        self.update_controls()
        if self.ac.status == AC.Status.on:
            self.ac.temp_up()
            PICCW.send_command(piccommands.SetACTemp(self.ac.temp_code))
            self.update_controls()
            self.start_update_timer()


class LightsRV(RecycleView):

    def __init__(self, **kwargs):
        super(LightsRV, self).__init__(**kwargs)


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
            Dimmer() if self.light.type == Light.TYPE_DIMMER else OnOff()
        self.add_widget(self.control)

    def update_value(self, value):
        self.control.update_value(self.light.value)


class Dimmer(Slider):

    def update_value(self, value):
        self.value = value


class OnOff(ToggleButton):

    def update_value(self, value):
        self.state = 'down' if value else 'normal'


class ACPower(ToggleButton):

    def __init__(self, **kwargs):
        super(ACPower, self).__init__(**kwargs)
        self.clock = None
        self.status = None

    def update_status(self, status):
        if self.status != status:
            self.status = status
            if self.clock:
                self.clock.cancel()
            if status == AC.Status.on:
                self.disabled = False
                self.state = 'down'
            elif status == AC.Status.off:
                self.disabled = False
                self.state = 'normal'
            else:
                self.disabled = True
                self.clock = Clock.schedule_interval(self.toggle, .25)

    def toggle(self, dt):
        self.state = 'normal' if self.state == 'down' else 'down'


class SceneControl(BoxLayout):

    class SceneButton(Button):

        scene = ObjectProperty()

    def __init__(self, **kwargs):
        super(SceneControl, self).__init__(**kwargs)
        self.dropdown = DropDown()
        self.scene = None
        for scene in Light.Scenes:
            btn = self.SceneButton(
                scene=scene, text=scene.name, size_hint_y=None)
            btn.bind(on_release=lambda btn: self.select_scene(btn.scene))
            self.dropdown.add_widget(btn, 1)

    def select_scene(self, scene):
        self.scene = scene
        self.ids.select_scene.text = scene.name
        self.dropdown.dismiss()

    def record_scene(self):
        if self.scene:
            PICCW.send_command(piccommands.RecordLightScene(self.scene.value))
