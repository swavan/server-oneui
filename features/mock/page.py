from typing import List, Callable

from kivy.properties import ObjectProperty, ListProperty
from kivymd.toast import toast
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.screen import MDScreen

from configs.color import OneUIColors
from features.mock import data
from features.mock.controller import load_endpoint_identifiers, get_last_seen_mock, save_mock_server
from features.mock.server import OneUIMockServerBoard
from storage.cache import OneUIApplicationCache


class OneUIMockPage(MDScreen):
    mock_nav_drawer = ObjectProperty()
    selected_endpoint_identifier = ObjectProperty({})
    items = ListProperty(load_endpoint_identifiers())
    mock_server = ObjectProperty(force_dispatch=True)

    def __init__(self, **kwargs):
        super(OneUIMockPage, self).__init__(**kwargs)

    def on_enter(self, *args):
        self.mock_nav_drawer.set_state("open")
        self.selected_server(get_last_seen_mock(OneUIApplicationCache.mock.current_server))

    def switch(self, name: str) -> None:
        self.ids.mock_screen_manager.current = name

    def menu_toggle(self):
        self.mock_nav_drawer.set_state("toggle")

    @property
    def mock_endpoint_identifiers(self) -> List[data.EndpointIdentifier]:
        return load_endpoint_identifiers(self.mock_server.id)

    @property
    def right_menus(self):
        return [
            ["play-circle", lambda x: self.server_action()],
            ["view-list", lambda x: self.menu_toggle()],
        ]

    @property
    def left_menus(self):
        return [
            ["menu-swap", lambda x: self.mock_servers()],
        ]

    def mock_servers(self):
        server_board = OneUIMockServerBoard()
        bottom_sheet_menu = MDCustomBottomSheet(screen=server_board)
        server_board.bind(close=lambda: bottom_sheet_menu.dismiss())
        server_board.bind(current=lambda _, x: self.selected_server(x, lambda: bottom_sheet_menu.dismiss()))
        bottom_sheet_menu.open()

    def selected_server(self, mock: data.Mock, bottom_sheet: Callable = None):
        if bottom_sheet:
            bottom_sheet()
        self.ids.mock_server_bar.title = f'{mock.name} :{mock.port}'
        self.mock_server = mock
        self.items = self.mock_endpoint_identifiers
        OneUIApplicationCache.mock.current_server = mock.id
        self.update_sever_status_indicator()

    def server_action(self):
        self.update_sever_status_indicator(True)

    def update_sever_status_indicator(self, toggle: bool = False):
        right_buttons = self.ids.mock_server_bar.children[0]

        is_running = self.mock_server.id in OneUIApplicationCache.mock.running_server

        for right_button in right_buttons.children:
            status = right_button.icon == "play-circle" or right_button.icon == "stop-circle"

            if status and toggle and not is_running:
                self._play(right_button)
                OneUIApplicationCache.mock.running_server.add(self.mock_server.id)
                break
            elif status and not is_running:
                self._stop(right_button)
                break

            if status and toggle and is_running:
                self._stop(right_button)
                OneUIApplicationCache.mock.running_server.remove(self.mock_server.id)
                break

            elif status and is_running:
                self._play(right_button)
                break

    def _play(self, right_button):
        right_button.icon = "stop-circle"
        right_button.theme_text_color = "Custom"
        right_button.text_color = OneUIColors.AccentColor.value

    def _stop(self, right_button):
        right_button.icon = "play-circle"
        right_button.theme_text_color = "Custom"
        right_button.text_color = OneUIColors.SaveButton.value

    def default_mock(self):
        mock = data.Mock(
            name="localhost",
            delay=0,
            port=4444
        )
        msg, status = save_mock_server(mock)
        if status:
            self.selected_server(get_last_seen_mock())
        toast(msg)
