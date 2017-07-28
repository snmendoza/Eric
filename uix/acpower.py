from kivy.clock import Clock
from kivy.uix.togglebutton import ToggleButton
from models.ac import AC


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
