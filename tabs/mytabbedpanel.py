from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader


class MyTabbedPanel(TabbedPanel):

    def switch_to(self, header, do_scroll=False):
        # Avoid calling on_unselected when switching from the default tab
        if self._current_tab.__class__ != TabbedPanelHeader:
            self._current_tab.on_unselected()
        super(MyTabbedPanel, self).switch_to(header, do_scroll)
        # Avoid calling on_selected when switching from the default tab
        if self._current_tab.__class__ != TabbedPanelHeader:
            self._current_tab.on_selected()
