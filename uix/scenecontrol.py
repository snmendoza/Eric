from appconnections import PICConnection
from commands import piccommands
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.properties import ObjectProperty
from models.light import Light
import os

path = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(os.path.join(path, 'scenecontrol.kv'))


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
            PICConnection.send_command(
                piccommands.RecordLightScene(self.scene.value))
