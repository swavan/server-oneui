from typing import List

from kivy.metrics import dp
from kivy.uix.dropdown import DropDown
from kivy.uix.behaviors import ButtonBehavior

from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.uix.gridlayout import MDGridLayout

from configs.color import OneUIColors


class OneUIComboButtonText(Label):
    pass


class OneUIComboItem(ButtonBehavior, MDBoxLayout):
    key = StringProperty()
    text = StringProperty("Items")


class OneUICombo(DropDown):
    back_color = StringProperty(OneUIColors.Background.value)
    border_radius = ListProperty([10])
    _items = ListProperty()
    text = StringProperty()

    def __init__(self, items: List = [], **kwargs):
        super(OneUICombo, self).__init__(**kwargs)
        if len(items) > 0:
            self.items = items

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, values: list):
        self._items = values
        self.create()

    def create(self):
        for _item in self.items:
            btn = OneUIComboItem()
            btn.text = _item.title()
            btn.size_hint_y = None
            btn.height = dp(60)
            btn.bind(on_release=lambda x: self.select(x.text))
            self.add_widget(btn)


class OneUIComboButton(MDGridLayout):
    placeholder = StringProperty()
    combo_field = ObjectProperty()
    combo_button = ObjectProperty()
    __menu = None
    items = ListProperty()

    def __init__(self, **kwargs):
        super(OneUIComboButton, self).__init__(**kwargs)
        self.__menu = OneUICombo()
        self.__menu.size_hint_max_y = None
        self.__menu.max_height = 300
        self.__menu.on_select = lambda x: self.selected(x)

    def selected(self, data):
        self.combo_field.text = data
        print(data)

    @property
    def text(self) -> str:
        return self.combo_field.text if self.combo_field else ""

    @text.setter
    def text(self, val) -> None:
        if self.combo_field:
            self.combo_field.text = val

    def release(self):
        self.__menu.open(self)

    def on_items(self, instance, val):
        self.__menu.items = val

    def search(self, val):
        print(val)


class OneUIComboDropdown(OneUIComboButton):
    pass
