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

from features.mock import data

from features.mock.controller import load_endpoint_identifiers, remove_endpoint_identifier
from widgets.layout import OneUIBox

Builder.load_file("features/mock/view/ui.kv")


class OneUIMockView(MDScreen):
    guardian_id = 0
    selected_row = ObjectProperty()
    rows = ListProperty()
    guardian = ObjectProperty()
    view_endpoint_identifier_list = ObjectProperty()

    def __init__(self, **kwargs):
        super(OneUIMockView, self).__init__(**kwargs)

    def load(self):
        self.rows = self.mock_endpoints

    def update(self, rows):
        self.view_endpoint_identifier_list.clear_widgets()
        for row in rows:
            item = OneUIMockListItem()
            item.mock = row
            item.bind(edit=self.on_edit)
            item.bind(delete=self.on_delete)
            item.bind(favorite=self.on_favorite)
            self.view_endpoint_identifier_list.add_widget(item)

    def on_rows(self, _, val):
        self.update(val)

    @property
    def mock_endpoints(self) -> List[data.EndpointIdentifier]:
        return load_endpoint_identifiers(self.guardian_id)

    def on_delete(self, _, val):
        status = remove_endpoint_identifier(val.id)
        if status:
            views = [view for view in self.views.children if view.mock.id == val.id]
            if len(views) > 0:
                self.views.remove_widget(views[0])

    def on_edit(self, _, val):
        self.selected_row = val

    def on_favorite(self, _, val):
        pass

    def search(self, _,  search_text: str):
        print(search_text)

    def on_guardian(self, _, mock: data.Mock = data.Mock()):
        self.guardian_id = mock.id
        self.load()


class OneUIMockListItem(OneLineAvatarIconListItem):
    mock = ObjectProperty()
    edit = ObjectProperty(force_dispatch=True)
    delete = ObjectProperty(force_dispatch=True)
    copy = ObjectProperty(force_dispatch=True)
    favorite = ObjectProperty(force_dispatch=True)

    menu = None

    def __init__(self, **kwargs):
        super(OneUIMockListItem, self).__init__(**kwargs)
        self.menu = MDDropdownMenu(
            caller=self.ids.mock_endpoint_identified_item,
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
            self.edit = self.mock
        elif instance_menu_item.text.lower() == "delete":
            self.delete = self.mock
        elif instance_menu_item.text.lower() == "copy":
            Clipboard.copy(json.dumps(asdict(self.mock)))
            toast('Copied !!!')
        elif instance_menu_item.text.lower() == "favorite":
            self.favorite = self.mock
        instance_menu.dismiss()

    def on_mock(self, _, val):
        self.text = val.name

    def release_edit(self):
        self.edit = self.mock
