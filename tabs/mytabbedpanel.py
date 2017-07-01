from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader


class MyTabbedPanel(TabbedPanel):

    def switch_to(self, header, do_scroll=False):
        other_tab = self._current_tab != header
        # Avoid calling on_unselected when switching from default tab
        if other_tab and self._current_tab.__class__ != TabbedPanelHeader:
            self._current_tab.on_unselected()
        super(MyTabbedPanel, self).switch_to(header, do_scroll)
        # Avoid calling on_selected when switching to default tab
        if other_tab and self._current_tab.__class__ != TabbedPanelHeader:
            self._current_tab.on_selected()

    # Call on_selected when first tab is selected automatically
    def _switch_to_first_tab(self, *l):
        super(MyTabbedPanel, self)._switch_to_first_tab(*l)
        self._current_tab.on_selected()
