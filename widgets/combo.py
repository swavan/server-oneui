from dataclasses import field
from typing import List, Dict

from kivy.metrics import dp
from kivy.uix.dropdown import DropDown
from kivy.uix.behaviors import ButtonBehavior

from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout

from configs.color import OneUIColors
from widgets.text import OneUITextFieldWrapper


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


class OneUIComboButton(OneUITextFieldWrapper, ButtonBehavior):
    placeholder = StringProperty()
    combo_field = ObjectProperty()
    combo_button = ObjectProperty()
    text = StringProperty()
    __menu = None
    items = ListProperty([])
    dict_items = ObjectProperty({})
    key = StringProperty()

    def __init__(self, **kwargs):
        super(OneUIComboButton, self).__init__(**kwargs)
        self.cols = 2

    def selected(self, data):
        self.combo_field.text = data

    def set_text(self):
        revered = {v: k for k, v in self.dict_items.items()}
        self.text = revered.get(self.combo_field.text, self.combo_field.text)

    def on_text(self, _, data):
        if len(self.dict_items.items()) > 0 or len(self.items) > 0:
            self.combo_field.text = self.dict_items.get(data, data)
        else:
            raise ValueError("Always set the items or dict_items first then only set text")

    def release(self):
        if self.__menu:
            self.__menu.open(self)

    def on_items(self, _, items: List):
        self.create_menu(items)

    def on_dict_items(self, _, items: Dict):
        rows = [row for row in items.values()]
        self.create_menu(rows)

    def create_menu(self, items: List):
        if not self.__menu:
            self.__menu = OneUICombo()
            self.__menu.size_hint_max_y = None
            self.__menu.max_height = 300
            self.__menu.on_select = lambda x: self.selected(x)
            self.__menu.items = items

    def on_release(self):
        self.release()


class OneUIComboDropdown(OneUIComboButton):
    pass
