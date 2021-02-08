from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty, ListProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.utils import rgba

from configs.color import OneUIColors


class OneUIVerticalBar(RelativeLayout):
    x_width = NumericProperty(80)
    state = StringProperty("open")
    border_radius = ListProperty([0, 0, 0, 0])
    back_color = ListProperty(rgba(OneUIColors.SaveButton.value))

    def __init__(self, **kwargs):
        super(OneUIVerticalBar, self).__init__(**kwargs)
        self.size_hint_x = None
        self.width = dp(self.x_width)

    def set_state(self, state: str):
        if state == "close":
            self.__close()
        elif state == "open":
            self.__open()
        elif state == "toggle":
            self.__toggle()

    def __toggle(self):
        if self.state == "open":
            self.__close()
        else:
            self.__open()

    def __close(self):
        self.state = "close"
        self.width = dp(0)

    def __open(self):
        self.state = "open"
        self.width = dp(self.x_width)
