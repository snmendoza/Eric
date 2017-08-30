from kivy.properties import ListProperty
from kivy.uix.togglebutton import ToggleButton


class MyToggleButton(ToggleButton):

    background_down_color = ListProperty()

    def __init__(self, **kwargs):
        super(MyToggleButton, self).__init__(**kwargs)
        self.border = 0, 0, 0, 0
        self.background_down_color = self.background_color
        self.original_background_color = self.background_color

    def set_state(self, down):
        self.state = 'down' if down else 'normal'

    def on_state(self, widget, value):
        if value == 'down':
            print(str(self.background_down_color))
            self.background_color = self.background_down_color
        else:
            # original background is just a list
            self.background_color = self.original_background_color

    def on_background_normal(self, instance, value):
        self.background_disabled_normal = self.background_normal

    def on_background_down(self, instance, value):
        self.background_disabled_down = self.background_down
