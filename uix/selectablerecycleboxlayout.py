from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior


class SelectableRecycleBoxLayout(LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection behavior to the view. '''
