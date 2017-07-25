from kivy.clock import Clock
from kivy.uix.button import Button


class RepeatButton(Button):

    def __init__(self, **kwargs):
        super(RepeatButton, self).__init__(**kwargs)
        self.register_event_type('on_repeat')

    def on_repeat(self):
        pass

    def on_press(self):
        self.lp_fired = False
        self.clock = Clock.schedule_interval(self.on_long_press, .5)

    def on_long_press(self, dt):
        self.lp_fired = True
        self.dispatch('on_repeat')

    def on_release(self):
        self.clock.cancel()
        if not self.lp_fired:
            self.dispatch('on_repeat')
