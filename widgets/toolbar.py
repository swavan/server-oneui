from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.gridlayout import MDGridLayout


class OneUITopBar(ButtonBehavior, MDGridLayout):
    def __init__(self, **kwargs):
        super(OneUITopBar, self).__init__(**kwargs)
        self.cols = 2
        self.row_default_height = dp(55)
        self.row_force_default = True
