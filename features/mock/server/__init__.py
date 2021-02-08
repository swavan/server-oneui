from kivy.lang import Builder
from kivy.properties import ObjectProperty, BooleanProperty, ListProperty
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

from configs.color import OneUIColors
from features.mock import data
from features.mock.controller import load_mock_servers, remove_mock_server, save_mock_server
from widgets.layout import OneUIBox, OneUIGrid
from storage.cache import OneUIApplicationCache

Builder.load_file("features/mock/server/server.kv")


class OneUIMockServerBoard(MDScreen):
    close = BooleanProperty(False)
    current = ObjectProperty(force_dispatch=True)

    def dismiss(self):
        self.close = True

class OneUIMockServers(OneUIGrid):
    editable = ObjectProperty()
    selected = ObjectProperty()
    servers = ListProperty()
    dialog = None

    def __init__(self, **kwargs):
        super(OneUIMockServers, self).__init__()
        self.servers = load_mock_servers()

    def on_servers(self, instance, servers):
        self.clear_widgets()
        for server in servers:
            _mock = OneUIMockServerList(server)
            _mock.bind(edit=self.edit)
            _mock.bind(delete=self.delete)
            _mock.bind(default=self.default)
            _mock.bind(selected=self.select)
            self.add_widget(_mock)

    def reload(self):
        self.servers = load_mock_servers()

    def select(self, _, mock: data.Mock):
        self.selected = mock

    def edit(self, _, mock: data.Mock):
        self.editable = mock

    def delete(self, _, mock: data.Mock):
        confirm_button = MDFlatButton(text="Accept", text_color=OneUIColors.SaveButton.value)
        confirm_button.bind(on_release=lambda x: self.remove(mock))
        cancel_button = MDFlatButton(text="Cancel", text_color=OneUIColors.AccentColor.value)
        cancel_button.bind(on_release=lambda x: self.dialog.dismiss())
        self.dialog = MDDialog(
            title=f"Remove mock server ( {mock.name} : {mock.port} )?",
            text="This will remove all endpoint and associated data",
            buttons=[confirm_button, cancel_button],
        )
        self.dialog.open()

    def remove(self, mock: data.Mock):
        try:
            removed = remove_mock_server(mock.id)
            if removed:
                self.servers = load_mock_servers()
        finally:
            if self.dialog:
                self.dialog.dismiss()

    def default(self, mock: data.Mock):
        self.servers = load_mock_servers()


class OneUIMockModify(OneUIBox):
    close = BooleanProperty(False)
    edit = ObjectProperty()
    saved = BooleanProperty(False, force_dispatch=True)
    id = 0

    @property
    def data(self):
        return data.Mock(
            id=self.id,
            name=self.ids.mock_env_name.text,
            port=int(self.ids.mock_env_port.text or 0),
            delay=int(self.ids.mock_response_delay.text or 0)
        )

    def on_edit(self, _, mock):
        self.id = mock.id
        self.ids.mock_env_name.text = mock.name
        self.ids.mock_env_port.text = str(mock.port)
        self.ids.mock_response_delay.text = str(mock.delay)
        self.ids.mock_server_save_button.icon = "pencil"

    def reset(self):
        self.id = 0
        self.ids.mock_env_name.text = ""
        self.ids.mock_env_port.text = ""
        self.ids.mock_response_delay.text = ""
        self.ids.mock_server_save_button.icon = "plus"

    def dismiss(self):
        self.close = True

    @property
    def is_valid(self):
        return self.ids.mock_env_name.text.strip() and self.ids.mock_env_port.text and self.ids.mock_response_delay.text

    def record(self):
        try:
            if self.is_valid:
                message, status = save_mock_server(self.data)
                if status:
                    self.saved = True
                    self.reset()
                toast(message)

        except ValueError as err:
            toast(f"Ops something went wrong, unable to save {self.ids.mock_env_name.text}")


class OneUIMockServerList(TwoLineAvatarIconListItem):
    id = None
    server = ObjectProperty()
    selected = ObjectProperty()
    edit = ObjectProperty(force_dispatch=True)
    delete = ObjectProperty(force_dispatch=True)
    default = ObjectProperty(force_dispatch=True)
    menu = None

    def __init__(self, mock: data.Mock = data.Mock()):
        super(OneUIMockServerList, self).__init__()
        self.server = mock
        self.menu = MDDropdownMenu(caller=self.ids.mock_server_option_button, items=self.options, width_mult=3)
        self.menu.bind(on_release=self.selected_option)

    def on_server(self, _, mock: data.Mock):
        self.id = mock.id
        self.text = f'{mock.name} :{mock.port}'
        self.secondary_text = f'Response delay: {mock.delay}'
        self.disabled = OneUIApplicationCache.mock.current_server == mock.id
        if self.id in OneUIApplicationCache.mock.running_server:
            self.toggle_server()

    def toggle_server(self):
        self.ids.mock_server_status_button.icon = "play" \
            if self.ids.mock_server_status_button.icon == "stop-circle" \
            else "stop-circle"

    def on_release(self):
        self.selected = self.server

    def update(self):
        self.edit = self.server

    def selected_option(self, instance_menu, instance_menu_item):
        if instance_menu_item.text.lower() == "edit":
            self.edit = self.server
        elif instance_menu_item.text.lower() == "delete":
            self.delete = self.server
        elif instance_menu_item.text.lower() == "default":
            self.default = self.server
        instance_menu.dismiss()

    def open_menu(self):
        if self.menu:
            self.menu.open()

    @property
    def options(self):
        return [{"text": "Edit", "icon": "pencil"},
                {"text": "Delete", "icon": "trash-can"},
                {"text": "Default", "icon": "shield-check"}, ]
