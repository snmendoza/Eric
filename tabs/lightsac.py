from kivy.uix.tabbedpanel import TabbedPanelItem


class LightsAC(TabbedPanelItem):

    def on_selected(self):
        print('selected lights')

    def on_unselected(self):
        print('unselected lights')
