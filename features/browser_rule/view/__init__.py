import json
from dataclasses import asdict
from typing import List

from kivy.core.clipboard import Clipboard
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty
from kivymd.toast import toast
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

from features.browser_rule import data

Builder.load_file("features/browser_rule/view/ui.kv")


class OneUIBrowserRules(MDScreen):
    rules = ListProperty()
    edit = ObjectProperty(force_dispatch=True)
    delete = ObjectProperty()

    def on_rules(self, _, rules: List[data.Rule]):
        self.ids.browser_rules_view.clear_widgets()
        for rule in rules:
            item = OneUIBrowserRulesListItem()
            item.rule = rule
            item.bind(edit=self.edit_row)
            item.bind(delete=self.delete_row)
            self.ids.browser_rules_view.add_widget(item)

    def edit_row(self, _, row: data.Rule):
        self.edit = row

    def delete_row(self, _, row: data.Rule):
        self.delete = row


class OneUIBrowserRulesListItem(OneLineAvatarIconListItem):
    rule = ObjectProperty()
    edit = ObjectProperty(force_dispatch=True)
    delete = ObjectProperty(force_dispatch=True)
    copy = ObjectProperty(force_dispatch=True)
    favorite = ObjectProperty(force_dispatch=True)

    menu = None

    def __init__(self, **kwargs):
        super(OneUIBrowserRulesListItem, self).__init__(**kwargs)
        self.menu = MDDropdownMenu(
            caller=self.ids.rule_item,
            items=self.menu_items,
            width_mult=3,
            selected_color=[0, 0, 0, .3]
        )
        self.menu.bind(on_release=self.menu_callback)

    @property
    def style(self):
        return {
            "height": "40dp",
            "top_pad": "12dp",
            "bot_pad": "12dp",
            "divider": None,
            "font_style": 'Caption'
        }

    @property
    def menu_items(self):
        return [
            {"text": "Edit", "icon": "pencil", **self.style},
            {"text": "Delete", "icon": "trash-can", **self.style},
            {"text": "Copy", "icon": "content-copy", **self.style},
            {"text": "Favorite", "icon": "bookmark", **self.style},
        ]

    def menu_callback(self, instance_menu, instance_menu_item):
        if instance_menu_item.text.lower() == "edit":
            self.edit = self.rule
        elif instance_menu_item.text.lower() == "delete":
            self.delete = self.rule
        elif instance_menu_item.text.lower() == "copy":
            Clipboard.copy(json.dumps(asdict(self.rule)))
            toast('Copied !!!')
        elif instance_menu_item.text.lower() == "favorite":
            self.favorite = self.rule
        instance_menu.dismiss()

    def on_rule(self, _, val):
        self.text = val.name

    def release_edit(self):
        self.edit = self.rule
