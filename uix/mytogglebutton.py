from kivy.uix.togglebutton import ToggleButton


class MyToggleButton(ToggleButton):

    def __init__(self, **kwargs):
        super(MyToggleButton, self).__init__(**kwargs)
        self.border = 0, 0, 0, 0

    def set_state(self, down):
        self.state = 'down' if down else 'normal'

    def on_background_normal(self, instance, value):
        self.background_disable_normal = self.background_normal

    def on_background_down(self, instance, value):
        self.background_disable_down = self.background_down
