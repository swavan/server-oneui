from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty

from configs.color import OneUIColors
from features.browser_rule import data
from features.browser_rule.controller import BrowserRuleController
from widgets.layout import OneUIBox, OneUIGrid
from widgets.panel import OneUIExpandablePanel
from widgets.toolbar import OneUITopBar

Builder.load_file("features/browser_rule/add/ui.kv")


class OneUIBrowserRule(OneUIBox):
    rule = ObjectProperty()
    saved = BooleanProperty(force_dispatch=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = None
        self.orientation = 'vertical'
        self.spacing = 15
        self.md_bg_color = OneUIColors.PageBackground.value

    def add_response_logics(self, response: data.BrowserRuleResponse = data.BrowserRuleResponse()):
        if self.ids.rule_logics:
            _widget = OneUIRuleLogicWidget()
            _widget.response = response

            body_container = OneUIExpandablePanel()
            head_panel = OneUIBrowserResponseHeaderPanel()
            head_panel.toggle = lambda: body_container.toggle_body_content()
            head_panel.remove = lambda: self.remove_response(body_container)
            head_panel.on_release = lambda: body_container.toggle_body_content()
            _widget.ids.tags.bind(text=head_panel.ids.browser_rule_response_header.setter("text"))

            body_container.head = head_panel
            body_container.bodies = [_widget]
            body_container.adaptive_height = True
            self.ids.rule_logics.add_widget(body_container)

    def remove_response(self, child):
        self.ids.rule_logics.remove_widget(child)

    def save(self):
        BrowserRuleController.save(self.data)
        self.saved = True

    def on_rule(self, _, rule: data.Rule):
        self.id = rule.id
        self.ids.name.text = rule.name
        self.ids.description.text = rule.description
        self.ids.source_type.text = rule.source_type
        self.ids.operator.text = rule.operator
        self.ids.source.text = rule.source
        self.ids.is_enabled.active = rule.is_enabled
        self.ids.rule_logics.clear_widgets()
        for response in rule.responses:
            self.add_response_logics(response)

    @property
    def data(self) -> data.Rule:
        have_responses = len(self.ids.rule_logics.children) > 0
        _rule = data.Rule(
            id=self.id,
            name=self.ids.name.text,
            description=self.ids.description.text,
            source_type=self.ids.source_type.text,
            operator=self.ids.operator.text,
            source=self.ids.source.text,
            is_enabled=self.ids.is_enabled.active
        )
        _responses = [response.data for response in self.ids.rule_logics.children[0].children
                      if (isinstance(response, OneUIRuleLogicWidget))] if have_responses else []
        _rule.responses = _responses
        return _rule


class OneUIRuleLogicWidget(OneUIGrid):
    response = ObjectProperty(data.BrowserRuleResponse())

    def __init__(self, response: data.BrowserRuleResponse = data.BrowserRuleResponse()):
        super(OneUIRuleLogicWidget, self).__init__()
        self.padding = dp(25)
        self.spacing = 20
        self.md_bg_color = OneUIColors.Background.value
        self.adaptive_height = True
        self.response = response

    def on_response(self, _, response: data.BrowserRuleResponse):
        self.ids.data_source_type.text = response.data_source_type
        self.ids.http_method.text = response.http_method
        self.ids.tags.text = response.tags
        self.ids.delay.text = str(response.delay)
        self.ids.is_logic_enabled.active = response.is_logic_enabled
        for _filter in response.filters:
            self.add_filter(_filter)

    def update_control(self, source_type: str):
        self.ids.browser_rule_data_widget_handler.clear_widgets()
        if source_type == 'r':
            self.ids.browser_rule_data_widget_handler.add_widget(OneUIBrowserRuleDataLink())
        if source_type == 'd':
            self.ids.browser_rule_data_widget_handler.add_widget(OneUIBrowserRuleData())

    def add_filter(self, _filter: data.RequestFilter = data.RequestFilter()) -> None:
        if self.ids:
            _widget = OneUIRuleLogicFilterWidget()
            _widget.filter = _filter
            _widget.remove = lambda x: self.remove_filter(_widget)
            self.ids.filters.add_widget(_widget)

    def remove_filter(self, child) -> None:
        if self.ids:
            self.ids.filters.remove_widget(child)

    @property
    def data(self) -> data.BrowserRuleResponse:

        have_data = len(self.ids.browser_rule_data_widget_handler.children) > 0
        return data.BrowserRuleResponse(
            delay=int(self.ids.delay.text),
            data_source_type=self.ids.data_source_type.text,
            http_method=self.ids.http_method.text,
            is_logic_enabled=self.ids.is_logic_enabled.active,
            tags=self.ids.tags.text,
            filters=[_filter.data for _filter in self.ids.filters.children],
            data=self.ids.browser_rule_data_widget_handler.children[0].data if have_data else data.MockData()
        )


class OneUIRuleLogicFilterWidget(OneUIGrid):
    filter = ObjectProperty()

    remove = None

    def on_release(self):
        if self.remove:
            try:
                self.remove(self)
            finally:
                pass

    def on_filter(self, _, _filter: data.RequestFilter):
        self.ids.filter_by.text = _filter.filter_by
        self.ids.key.text = _filter.key
        self.ids.value.text = _filter.value

    @property
    def data(self) -> data.RequestFilter:
        return data.RequestFilter(
            filter_by=self.ids.filter_by.text,
            key=self.ids.key.text,
            value=self.ids.value.text)


class OneUIBrowserResponseHeaderPanel(OneUITopBar):

    def remove(self):
        pass

    def toggle(self):
        pass


class OneUIBrowserRuleDataLink(OneUIBox):
    link = StringProperty()

    def on_link(self, _, val: str):
        self.ids.link.text = val

    @property
    def data(self) -> data.MockData:
        return data.MockData(link=self.ids.link.text)


class OneUIBrowserRuleData(OneUIBox):
    mock_data = ObjectProperty(data.MockData())

    def __init__(self, **kwargs):
        super(OneUIBrowserRuleData, self).__init__(**kwargs)
        self.adaptive_height = True

    def on_mock_data(self, _, mock_data: data.MockData):
        self.ids.content.text = mock_data.content
        self.ids.link.text = mock_data.link
        self.ids.status.text = mock_data.status
        self.ids.content_type.text = mock_data.content_type
        self.ids.cloud_store_permission = True if mock_data.cloud_store_permission == "a" else False
        for header in mock_data.headers:
            self.add_header(header=header)

    def add_header(self, header: data.DataHeader = data.DataHeader()) -> None:
        _widget = OneUIBrowserRuleDataHeader()
        _widget.header = header
        _widget.remove = lambda x: self.remove(x)
        if self.ids:
            self.ids.browser_rule_mock_headers.add_widget(_widget)

    def remove(self, child):
        self.ids.browser_rule_mock_headers.remove_widget(child)

    @property
    def data(self) -> data.MockData:
        return data.MockData(
            content=self.ids.content.text,
            link=self.ids.link.text,
            status=self.ids.status.text,
            content_type=self.ids.content_type.text,
            headers=[_header.data for _header in self.ids.browser_rule_mock_headers.children],
            cloud_store_permission="a" if self.ids.cloud_store_permission.active else "na")


class OneUIBrowserRuleDataHeader(OneUIBox):
    header = ObjectProperty()

    def remove(self, x):
        pass

    def on_header(self, _, header: data.DataHeader):
        self.ids.key.text = header.key
        self.ids.value.text = header.value

    @property
    def data(self) -> data.DataHeader:
        return data.DataHeader(key=self.ids.key.text, value=self.ids.value.text)
