from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen

from configs.codes import HTTP_METHODS
from widgets.combo import OneUICombo
from widgets.layout import OneUIGrid
from widgets.panel import OneUIExpandablePanel
from widgets.toolbar import OneUITopBar

from features.mock.controller import save_endpoint_identifier


class OneUIMockAdd(MDScreen):
    endpoint_identifier = ObjectProperty()
    endpoint_description = ObjectProperty()

    responses = ObjectProperty()

    def save(self):
        print(f"Name: {self.endpoint_identifier.text}")
        print(f"Description: {self.endpoint_description.text}")
        # print("Responses: ", self.responses.children[0].bodies)
        endpoint_identifier = save_endpoint_identifier(self.endpoint_identifier.text, self.endpoint_description.text)

        for _response in self.responses.children:
            response, head, rule = _response.bodies
            print(f"Http Method: {response.mock_http_method.text}")
            print(f"URL: {response.mock_url.text}")
            print(f"Delay: {response.mock_response_delay.text}")
            print(f"Content-Type: {response.mock_content_type.text}")
            print(f"Status Code: {response.mock_status_code.text}")
            print(f"File Path: {response.mock_file_url.text}")
            print(f"Raw Data: {response.mock_data.text}")

            print("---------------Headers--------------")
            _, headers = head.children
            for header in headers.children:
                print(f"Header Key: {header.header_key_field.text}\tValue: {header.header_value_field.text}")

            print("---------------Rules--------------")
            print(rule.children)
            _, filters = rule.children
            for f in filters.children:
                print(f"By: {f.mock_filter_by.text}")
                print(f"\tKey: {f.mock_filter_key.text}")
                print(f"\t\tOperator: {f.mock_filter_operator.text}")
                print(f"\t\t\tValue: {f.mock_filter_value.text}")

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
    mock_filter_by = ObjectProperty()
    mock_filter_key = ObjectProperty()
    mock_filter_operator = ObjectProperty()
    mock_filter_value = ObjectProperty()

    def on_delete(self):
        pass


class OneUIMOckResponseHeaders(MDBoxLayout):
    headers = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add()

    def add(self):
        fields = OneUIMockHeader()
        fields.on_delete = lambda: self.remove(fields)
        self.headers.add_widget(fields)

    def remove(self, widget):
        self.headers.remove_widget(widget)


class OneUIMOckResponseData(OneUIGrid):
    http_method = OneUICombo()
    mock_http_method = ObjectProperty()
    mock_url = ObjectProperty()
    mock_response_delay = ObjectProperty()
    mock_content_type = ObjectProperty()
    mock_status_code = ObjectProperty()
    mock_file_url = ObjectProperty()
    mock_data = ObjectProperty()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print(self.ids)
        self.http_method.size_hint_max_y = None
        self.http_method.max_height = 300
        self.http_method.items = HTTP_METHODS.keys()
        self.http_method.on_select = lambda x: self.mock_http_update(x)


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
    header_key_field = ObjectProperty()
    header_value_field = ObjectProperty()

    def on_delete(self):
        pass
