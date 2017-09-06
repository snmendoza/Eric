from kivy.uix.button import Button
from kivy.properties import ListProperty, StringProperty


class MyButton(Button):

    background = StringProperty('')
    background_down_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(MyButton, self).__init__(**kwargs)
        self.border = 0, 0, 0, 0
        self.original_background_color = self.background_color

    def on_background_color(self, instance, value):
        if value != self.background_down_color:
            self.original_background_color = value

    def on_background(self, instance, value):
        self.background_normal = self.background
        self.background_down = self.background
        self.bakground_disabled_normal = self.background
        self.background_disabled_down = self.background
        self.height = self.width

    def on_state(self, widget, value):
        if value == 'down':
            self.background_color = self.background_down_color
        else:
            # original background is just a list
            self.background_color = self.original_background_color
