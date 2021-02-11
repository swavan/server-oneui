from dataclasses import field
from typing import List

from kivy.lang import Builder
from kivy.properties import ObjectProperty, BooleanProperty, ListProperty
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout

from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen


from features.mock import data

from widgets.layout import OneUIGrid, OneUIBox
from widgets.panel import OneUIExpandablePanel
from widgets.toolbar import OneUITopBar

from features.mock.controller import save

Builder.load_file("features/mock/add/ui.kv")


class OneUIMockAdd(MDScreen):
    app_drawer = BooleanProperty(force_dispatch=True)
    mock_drawer = BooleanProperty(force_dispatch=True)
    responses = ObjectProperty()
    saved = BooleanProperty(force_dispatch=True)
    selected_row = ObjectProperty()
    guardian = ObjectProperty()
    dialog = None

    @property
    def endpoint_identifier(self):
        endpoint_identifier_widget = self.ids.scroll.children[0]
        return endpoint_identifier_widget.data

    def save(self):
        try:
            save(self.endpoint_identifier, self.guardian.id)
            self.saved = True
            toast(f"{self.endpoint_identifier.name} saved")
        except Exception as e:
            toast(f"Ops, something went wrong while saving {self.endpoint_identifier.name}")

    def on_selected_row(self, _, endpoint_identifier):
        self.create_form(endpoint_identifier)

    def create_form(self, endpoint_identifier=data.EndpointIdentifier()):
        if len(self.ids.scroll.children):
            self.ids.scroll.remove_widget(self.ids.scroll.children[0])
        self.ids.scroll.add_widget(OneUIMockEndpointIdentifier(endpoint_identifier))

    def toggle_app_drawer(self):
        self.app_drawer = not self.app_drawer

    def toggle_mock_drawer(self):
        self.mock_drawer = not self.mock_drawer


class OneUIMockHeaderPanel(OneUITopBar):
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


class OneUIMockEndpointIdentifier(OneUIBox):
    endpoints = ListProperty([data.Endpoint()])

    def __init__(self, endpoint_identifier: data.EndpointIdentifier = data.EndpointIdentifier()):
        super(OneUIMockEndpointIdentifier, self).__init__()
        self.id = endpoint_identifier.id
        self.ids.endpoint_identifier_name.text = endpoint_identifier.name
        self.ids.endpoint_identifier_description.text = endpoint_identifier.description
        self.endpoints = endpoint_identifier.endpoints

    def on_endpoints(self, _, endpoints):
        self.add_widget(OneUIMockEndpoints(endpoints))

    @property
    def data(self):
        return data.EndpointIdentifier(
            id=self.id,
            name=self.ids.endpoint_identifier_name.text,
            description=self.ids.endpoint_identifier_description.text,
            endpoints=self.children[0].data
        )


class OneUIMockEndpoints(OneUIBox):
    endpoints = ListProperty()

    def __init__(self, endpoints: List[data.Endpoint] = field(default_factory=list)):
        super(OneUIMockEndpoints, self).__init__()
        self.endpoints = endpoints

    def on_endpoints(self, _, endpoints):
        for endpoint in endpoints:
            self.add_endpoint(endpoint)

    def add_endpoint(self, endpoint: data.Endpoint = data.Endpoint()):
        body_container = OneUIExpandablePanel()

        head_panel = OneUIMockHeaderPanel()
        head_panel.load_data_page = lambda: body_container.switch_body(0)
        head_panel.load_headers_page = lambda: body_container.switch_body(1)
        head_panel.load_rules_page = lambda: body_container.switch_body(2)
        head_panel.toggle_view = lambda: body_container.toggle_body_content()
        head_panel.on_release = lambda: body_container.toggle_body_content()
        head_panel.remove = lambda: self.remove_endpoint(body_container)
        body_container.head = head_panel
        body_container.bodies = [
            OneUIMockEndpoint(endpoint),
            OneUIMockHeaders(endpoint.headers
                             if endpoint.id and len(endpoint.headers) > 0 else
                             [data.Header(key="Content-Type", value="application/json")]),
            OneUIMockRules(endpoint.rules)
        ]
        body_container.adaptive_height = True
        self.ids.mock_endpoints.add_widget(body_container)

    def remove_endpoint(self, widget): self.ids.mock_endpoints.remove_widget(widget)

    @property
    def data(self) -> List[data.Endpoint]:
        def _compose(endpoint_widget, header_widget, rule_widget) -> data.Endpoint:
            endpoint = endpoint_widget.data
            endpoint.headers = header_widget.data
            endpoint.rules = rule_widget.data
            return endpoint

        return [(_compose(*_endpoint.bodies)) for _endpoint in self.ids.mock_endpoints.children]

    def on_tab_switch(self, *args):
        pass


class OneUIMockEndpoint(OneUIGrid):
    def __init__(self, endpoint: data.Endpoint = data.Endpoint()):
        super(OneUIMockEndpoint, self).__init__()
        self.id = endpoint.id
        self.ids.mock_http_method.text = endpoint.http_method
        self.ids.mock_url.text = endpoint.url
        self.ids.mock_response_delay.text = str(endpoint.delay)
        self.ids.mock_status_code.text = endpoint.status
        self.ids.mock_file_url.text = endpoint.content_path
        self.ids.mock_data.text = endpoint.content

    @property
    def data(self): return data.Endpoint(
        id=self.id,
        http_method=self.ids.mock_http_method.text,
        url=self.ids.mock_url.text,
        delay=int(self.ids.mock_response_delay.text if len(self.ids.mock_response_delay.text) > 0 else 0),
        status=self.ids.mock_status_code.text,
        content_path=self.ids.mock_file_url.text,
        content=self.ids.mock_data.text,
        headers=[],
        rules=[]
    )


class OneUIMockRules(MDBoxLayout):
    rules = ListProperty()

    def __init__(self, rules: List[data.Rule] = field(default_factory=list)):
        super().__init__()
        self.rules = rules

    def on_rules(self, _, rules: List[data.Rule]):
        for rule in rules:
            self.add(rule)

    def add(self, rule: data.Rule = data.Rule()):
        rule_widget = OneUIMockRule(rule)
        rule_widget.on_delete = lambda: self.delete(rule_widget)
        self.ids.mock_rules.add_widget(rule_widget)

    def delete(self, widget):
        self.ids.mock_rules.remove_widget(widget)

    @property
    def data(self) -> List[data.Rule]: return [rule.data for rule in self.ids.mock_rules.children]


class OneUIMockRule(MDGridLayout):

    def __init__(self, rule: data.Rule = data.Rule()):
        super(OneUIMockRule, self).__init__()
        self.ids.mock_filter_by.text = rule.filter_by
        self.ids.mock_filter_key.text = rule.field
        self.ids.mock_filter_operator.text = rule.operator
        self.ids.mock_filter_value.text = rule.value

    @property
    def data(self) -> data.Rule:
        return data.Rule(
            filter_by=self.ids.mock_filter_by.text,
            field=self.ids.mock_filter_key.text,
            operator=self.ids.mock_filter_operator.text,
            value=self.ids.mock_filter_value.text,
        )

    def on_delete(self):
        pass


class OneUIMockHeaders(MDBoxLayout):
    headers = ListProperty()

    def __init__(self, headers: List[data.Header] = field(default_factory=list)):
        super(OneUIMockHeaders, self).__init__()
        self.headers = headers

    def on_headers(self, _, headers):
        for header in headers:
            self.add(header)

    def add(self, header=data.Header()):
        header_widget = OneUIMockHeader(header)
        header_widget.on_delete = lambda: self.remove(header_widget)
        self.ids.headers.add_widget(header_widget)

    def remove(self, widget):
        self.ids.headers.remove_widget(widget)

    @property
    def data(self): return [header.data for header in self.ids.headers.children]


class OneUIMockHeader(MDGridLayout):

    def __init__(self, header: data.Header = data.Header()):
        super(OneUIMockHeader, self).__init__()
        self.ids.header_key_field.text = header.key
        self.ids.header_value_field.text = header.value

    def on_delete(self):
        pass

    @property
    def data(self) -> data.Header:
        return data.Header(
            key=self.ids.header_key_field.text,
            value=self.ids.header_value_field.text,
        )
