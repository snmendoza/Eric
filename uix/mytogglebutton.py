from kivy.uix.togglebutton import ToggleButton


class MyToggleButton(ToggleButton):

    def set_state(self, down):
        self.state = 'down' if down else 'normal'
