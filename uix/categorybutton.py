from appplayers import MusicPlayer
from kivy.properties import ObjectProperty
from kivy.uix.togglebutton import ToggleButton


class CategoryButton(ToggleButton):

    category = ObjectProperty()

    def __init__(self, **kwargs):
        super(CategoryButton, self).__init__(**kwargs)
        self.group = 'categories'

    def on_category(self, instance, value):
        self.text = self.category.title

    def on_release(self):
        if self.state == 'down':
            MusicPlayer.set_category(self.category)
            self.disabled = True

    def on_state(self, instance, value):
        self.disabled = False
