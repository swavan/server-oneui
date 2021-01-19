from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.gridlayout import MDGridLayout


class OneUIHeader(MDGridLayout):
    header_key_field = ObjectProperty()
    header_value_field = ObjectProperty()

    def __init__(self, **kwargs):
        super(OneUIHeader, self).__init__(**kwargs)

    def trash(self):
        pass


class OneUIHeaders(MDGridLayout):
    __headers = MDBoxLayout()

    def __init__(self, **kwargs):
        super(OneUIHeaders, self).__init__(**kwargs)

        self.rows = 2
        self.spacing = 5
        self.__headers.orientation = "vertical"
        self.md_bg_color = [0.3, 0.3, 0.1, 1]
        __add_new = MDFlatButton()
        __add_new.text = "Add New"
        __add_new.bind(on_release=lambda x: self.add())
        super().add_widget(self.__headers)
        super().add_widget(__add_new)

    def add(self):
        __header = OneUIHeader()
        print("Add header")
        self.__headers.add_widget(__header)

    def delete_header(self, widget):
        self.__headers.remove_widget(widget)

    def add_widget(self, widget, index, canvas):
        self.__headers.add_widget(widget)


class HeaderApp(Widget):
    pass
