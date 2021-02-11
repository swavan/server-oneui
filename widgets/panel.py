from kivy.properties import ListProperty, ObjectProperty, NumericProperty, StringProperty
from kivy.uix.widget import WidgetException
from kivymd.uix.gridlayout import MDGridLayout


class OneUIExpandablePanel(MDGridLayout):
    # TODO: Add animation on expand and colapse  i.e. on close use "out_sine" and on open use "out_cubic"
    # TODO: Add animation on widget switch between

    __bodies = ListProperty()
    __head = ObjectProperty()
    __current = NumericProperty(-1)
    _panelState = StringProperty("close")

    def __init__(self, **kwargs):
        super(OneUIExpandablePanel, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2
        self.adaptive_height = True

    @property
    def head(self):
        return self.__head

    @head.setter
    def head(self, val):
        self.__head = val
        super().add_widget(self.head)

    @property
    def bodies(self):
        return self.__bodies

    @bodies.setter
    def bodies(self, val):
        self.__bodies = val

    def switch_body(self, position: int):
        if self.__current == position and self._panelState == "open":
            self.remove()
            self._panelState = "close"
        elif self.bodies:
            try:
                self.remove()
                super().add_widget(self.bodies[position])
                self.__current = position
                self._panelState = "open"
            except WidgetException:
                pass

    def remove(self):
        if len(self.children) == 2:
            self.remove_widget(self.children[0])

    def toggle_body_content(self):
        if len(self.children) == 2:
            self.remove()
            self._panelState = "close"
        else:
            self.switch_body(self.__current)
