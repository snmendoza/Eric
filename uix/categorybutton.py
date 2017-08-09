from appplayers import MusicPlayer
from kivy.properties import ObjectProperty
from kivy.uix.togglebutton import ToggleButton


class CategoryButton(ToggleButton):

    category = ObjectProperty()

    def __init__(self, **kwargs):
        super(CategoryButton, self).__init__(**kwargs)
        self.group = 'categories'
        self.bind(on_release=self._on_release)

    def on_category(self, instance, value):
        self.text = self.category.title
        if MusicPlayer.category and self.category.id == MusicPlayer.category.id:
            self.state = 'down'
            self.disabled = True
        else:
            self.state = 'normal'
            self.disabled = False

    def _on_release(self, instance):
        if self.state == 'down':
            MusicPlayer.set_category(self.category)
            self.disabled = True
