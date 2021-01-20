from kivy.uix.dropdown import DropDown
from kivy.uix.behaviors import ButtonBehavior

from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.label import Label
from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.uix.gridlayout import MDGridLayout


class OneUIComboButtonText(Label):
    pass


class OneUIComboItem(ButtonBehavior, MDBoxLayout):
    key = StringProperty()
    text = StringProperty()


class OneUICombo(DropDown):
    _items = ListProperty()
    text = StringProperty()

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, values: list):
        self._items = values
        self.create()

    def create(self):
        self.clear_widgets()
        for _item in self.items:
            btn = OneUIComboItem()
            btn.text = _item.title()
            btn.size_hint_y = None
            btn.height = dp(60)
            btn.bind(on_release=lambda x: self.select(x.text))
            self.add_widget(btn)


class OneUIComboButton(ButtonBehavior, MDGridLayout):
    placeholder = StringProperty()
    combo_field = ObjectProperty()
    __menu = OneUICombo()

    def __init__(self, **kwargs):
        super(OneUIComboButton, self).__init__(**kwargs)
        self.__menu.size_hint_max_y = None
        self.__menu.max_height = 300
        self.__menu.on_select = lambda x: self.selected(x)

    def selected(self, data):
        self.combo_field.text = data

    @property
    def menu(self) -> OneUICombo:
        return self.__menu

    def open(self):
        self.menu.open(self)


class OneUIComboDropdown(OneUIComboButton):
    pass
    # preSelected = StringProperty("Select option")
    # __items = ListProperty()
    #
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #
    # @property
    # def items(self):
    #     return self.__items
    #
    # @items.setter
    # def items(self, values: list):
    #     self.__items = list(values)
    #     self.update()
    #
    # def update(self):
    #     super().menu.items = self.__items

