from kivy.metrics import dp
from kivy.properties import StringProperty, NumericProperty

from widgets.layout import OneUIGrid


class OneUIDivider(OneUIGrid):

    type = StringProperty()
    line_width = NumericProperty(1)

    def __init__(self, **kwargs):
        super(OneUIDivider, self).__init__()
        self.md_bg_color = [0, 0, 0, 0.2]
        self.cols = 0
        self.rows = 0
        self.size_hint_x = None
        self.width = dp(1)

    def on_type(self, _, _type):

        if _type == "horizontal":
            self.size_hint_y = None
            self.size_hint_x = 1
            self.height = self.line_width

        elif _type == "vertical":
            self.size_hint_y = 1
            self.size_hint_x = None
            self.width = self.line_width

