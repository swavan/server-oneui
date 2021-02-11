from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import BooleanProperty
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

Builder.load_file("widgets/tab/tab.kv")


class OneUITabPanel(TabbedPanel):

    adaptive_height = BooleanProperty(False)
    adaptive_width = BooleanProperty(False)

    def __init__(self,**kwargs):
        super(OneUITabPanel, self).__init__(**kwargs)
        self.do_default_tab = False
        self.tab_height = dp(40)
        self.minimum_height = dp(40)


    def on_adaptive_height(self, _, val):
        self.size_hint_y = None
        self.height = self.minimum_height

    def on_adaptive_width(self, _, val):
        self.size_hint_x = None
        self.width = self.minimum_width


class OneUITabbedPanelItem(TabbedPanelItem):
    adaptive_height = BooleanProperty(False)
    adaptive_width = BooleanProperty(False)

    def on_adaptive_height(self, _, val):
        if val:
            self.size_hint_y = None
            # self.height = self.minimum_height

    def on_adaptive_width(self, _, val):
        if val:
            self.size_hint_x = None
            self.width = self.minimum_width
