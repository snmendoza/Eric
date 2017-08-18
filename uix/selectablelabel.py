from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.label import Label
from kivy.uix.recycleview.views import RecycleDataViewBehavior
import os

path = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(os.path.join(path, 'selectablelabel.kv'))


class SelectableLabel(RecycleDataViewBehavior, Label):

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    activated_from_press = False

    def __init__(self, **kwargs):
        super(SelectableLabel, self).__init__(**kwargs)
        self.register_event_type('on_press')
        self.register_event_type('on_release')
        self.register_event_type('on_item_selected')

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            touch.grab(self)
            self.dispatch('on_press', self.index)
            self.activated_from_press = True
            result = self.parent.select_with_touch(self.index, touch)
            self.activated_from_press = False
            return result

    def on_touch_up(self, touch):
        if super(SelectableLabel, self).on_touch_up(touch):
            return True
        if touch.grab_current is self:
            self.dispatch('on_release', self.index)
            touch.ungrab(self)
            return True

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected and self.activated_from_press:
            self.dispatch('on_item_selected', self.index)

    def on_press(self, index):
        pass

    def on_release(self, index):
        pass

    def on_item_selected(self, index):
        pass
