from kivy.uix.tabbedpanel import TabbedPanelItem


class TV(TabbedPanelItem):

    def __init__(self, **kwargs):
        super(TV, self).__init__(**kwargs)
        self.text = 'TV'
