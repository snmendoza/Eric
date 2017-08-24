from kivy.uix.button import Button
from kivy.properties import StringProperty


class MyButton(Button):

    background = StringProperty('')

    def on_background(self, instance, value):
        self.background_normal = self.background
        self.background_down = self.background
        self.bakground_disabled_normal = self.background
        self.background_disabled_down = self.background
