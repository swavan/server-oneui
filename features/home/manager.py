from typing import List

from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen

from widgets.menu import OneUIMenuItems


def menus() -> List:
    return [
        {"icon": "home", "text": "Home", "screen": "home"},
        {"icon": "cloud", "text": "Mock", "screen": "mock"},
        {"icon": "ruler", "text": "Browser Rules", "screen": "browser_rule"},
        {"icon": "help", "text": "Help", "screen": "help"},
        {"icon": "information", "text": "About", "screen": "about"},
    ]


class OneUIPageManager(MDScreen):
    main_screen_manager = ObjectProperty()
    menuItems = ObjectProperty()

    def __init__(self, **kwargs):
        super(OneUIPageManager, self).__init__(**kwargs)
        for item in menus():
            menu_item = OneUIMenuItems(icon=item.get("icon"), text=item.get("text"))
            menu_item.screen = item.get("screen")
            menu_item.bind(on_release=lambda x: self.change_page(x.screen))
            self.menuItems.add_widget(menu_item)

    def change_page(self, name):
        print("What the heck it is", name)
        self.ids.main_screen_manager.current = name
        self.ids.nav_drawer.set_state('toggle')
