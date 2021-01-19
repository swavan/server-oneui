from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen

from widgets.layout import OneUIGrid
from widgets.panel import OneUIExpandablePanel
from widgets.toolbar import OneUITopBar


class OneUIMockAdd(MDScreen):
    responses = ObjectProperty()

    def save(self):
        print("Saving Mock")

    def add_response(self):
        body_container = OneUIExpandablePanel()

        head_panel = OneUIMockResponseHeaderPanel()
        head_panel.load_data_page = lambda: body_container.switch_body(0)
        head_panel.load_headers_page = lambda: body_container.switch_body(1)
        head_panel.load_rules_page = lambda: body_container.switch_body(2)
        head_panel.toggle_view = lambda: body_container.toggle_body_content()
        head_panel.on_release = lambda: body_container.toggle_body_content()
        head_panel.remove = lambda: self.remove_response(body_container)
        body_container.head = head_panel

        data = OneUIMOckResponseData()
        header = OneUIMOckResponseHeaders()
        rule = OneUIAddMockResponseRules()
        body_container.bodies = [data, header, rule]
        body_container.adaptive_height = True
        self.responses.add_widget(body_container)

    def remove_response(self, widget):
        self.responses.remove_widget(widget)


class OneUIAddMockButtons(OneUIGrid):
    pass


class OneUIAddMockResponseRules(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add()

    def add(self):
        rule = OneUIAddMockResponseRule()
        rule.on_delete = lambda: self.delete(rule)
        self.ids.mock_rules.add_widget(rule)

    def delete(self, widget):
        self.ids.mock_rules.remove_widget(widget)


class OneUIAddMockResponseRule(MDGridLayout):
    def on_delete(self):
        pass


class OneUIMOckResponseHeaders(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add()

    def add(self):
        fields = OneUIMockHeader()
        fields.on_delete = lambda: self.remove(fields)
        self.ids.headers.add_widget(fields)

    def remove(self, widget):
        self.ids.headers.remove_widget(widget)


class OneUIMOckResponseData(OneUIGrid):
    pass


class OneUIMockResponseHeaderPanel(OneUITopBar):

    def load_headers_page(self):
        pass

    def load_data_page(self):
        pass

    def load_rules_page(self):
        pass

    def toggle_view(self):
        pass

    def remove(self):
        pass


class OneUIMockHeader(MDGridLayout):
    def on_delete(self):
        pass
