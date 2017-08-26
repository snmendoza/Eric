from kivy.clock import Clock
from uix.mybutton import MyButton


class RepeatButton(MyButton):

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

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            self.clock.cancel()
            if not self.lp_fired:
                self.dispatch('on_repeat')
        return super(RepeatButton, self).on_touch_up(touch)
