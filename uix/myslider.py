from kivy.uix.slider import Slider


class MySlider(Slider):

    def __init__(self, **kwargs):
        super(MySlider, self).__init__(**kwargs)
        self.register_event_type('on_press')
        self.register_event_type('on_release')
        self.register_event_type('on_move')

    def on_touch_down(self, touch):
        if super(MySlider, self).on_touch_down(touch):
            self.dispatch('on_press')
            return True

    def on_touch_up(self, touch):
        super(MySlider, self).on_touch_up(touch)
        if touch.grab_current is self:
            self.dispatch('on_release')
            touch.ungrab(self)
            return True

    def on_touch_move(self, touch):
        super(MySlider, self).on_touch_move(touch)
        if touch.grab_current is self:
            self.dispatch('on_move')
            return True

    def on_press(self):
        pass

    def on_release(self):
        pass

    def on_move(self):
        pass
