from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout


class Scroll(ScrollView):
    pass


class OneUIBox(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'


class OneUIGrid(MDGridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
