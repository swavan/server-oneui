from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

Builder.load_file("widgets/tab/tab.kv")


class OneUITabPanel(TabbedPanel):
    pass


class OneUITabbedPanelItem(TabbedPanelItem):
    pass
