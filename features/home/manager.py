from typing import List, Callable, Set, Tuple

from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.utils import rgba
from kivymd.uix.screen import MDScreen

from widgets.button import OneUITooltipIconButton
from widgets.layout import OneUIBox


def menus() -> List:
    return [
        # {"icon": "home", "text": "Home", "screen": "home"},
        {"icon": "cloud", "text": "Mock", "screen": "mock"},
        {"icon": "ruler", "text": "Browser Rules", "screen": "browser_rule"},
        {"icon": "help", "text": "Help", "screen": "help"},
        {"icon": "information", "text": "About", "screen": "about"},
    ]


class OneUIPageManager(MDScreen):
    main_screen_manager = ObjectProperty()
    menuItems = ObjectProperty()

    def __init__(self, **kwargs):
        super(OneUIPageManager, self).__init__()
        for item in menus():
            box = OneUIBox()
            box.padding = [dp(15), dp(10), dp(15), dp(10)]
            box.adaptive_height = True
            menu_item = OneUITooltipIconButton(icon=item.get("icon"), tooltip_text=item.get("text"))
            menu_item.screen = item.get("screen")
            menu_item.bind(on_release=lambda x: self.change_page(x.screen))
            menu_item.theme_text_color = "Custom"
            menu_item.text_color = [1, 1, 1, 1]
            menu_item.md_bg_color = rgba("#175873")
            box.add_widget(menu_item)
            self.menuItems.add_widget(box)

    def change_page(self, name):
        self.ids.main_screen_manager.current = name
