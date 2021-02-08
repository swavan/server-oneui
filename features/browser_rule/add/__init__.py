from kivy.lang import Builder
from kivy.metrics import dp

from configs.codes import RULES_FOR
from configs.color import OneUIColors
from widgets.layout import OneUIBox, OneUIGrid
from widgets.panel import OneUIExpandablePanel
from widgets.toolbar import OneUITopBar

Builder.load_file("features/browser_rule/add/ui.kv")


class OneUIBrowserRule(OneUIBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 15
        self.md_bg_color = OneUIColors.PageBackground.value

    def add_response_logics(self):
        if self.ids.rule_logics:
            _widget = OneUIRuleLogicWidget()

            body_container = OneUIExpandablePanel()
            head_panel = OneUIBrowserResponseHeaderPanel()
            head_panel.toggle = lambda: body_container.toggle_body_content()
            head_panel.remove = lambda: self.remove_response(body_container)
            head_panel.on_release = lambda: body_container.toggle_body_content()
            _widget.ids.rule_logic_name.bind(text=head_panel.ids.browser_rule_response_header.setter("text"))

            body_container.head = head_panel
            body_container.bodies = [_widget]
            body_container.adaptive_height = True
            self.ids.rule_logics.add_widget(body_container)

    def remove_response(self, child):
        self.ids.rule_logics.remove_widget(child)
        print("Remove responses")

    def save(self):
        print("Saving")

    def cancel(self):
        print("cancel")

    def rules_for(self) -> list:
        return RULES_FOR.keys()


class OneUIRuleLogicWidget(OneUIGrid):

    def __init__(self, **kwargs):
        super(OneUIRuleLogicWidget, self).__init__(**kwargs)
        self.padding = dp(25)
        self.spacing = 20
        self.md_bg_color = OneUIColors.Background.value
        self.on_adaptive_height = True

    def add_filter(self) -> None:
        if self.ids.rule_filters:
            _widget = OneUIRuleLogicFilterWidget()
            _widget.remove = lambda x: self.remove_filter(_widget)
            self.ids.rule_filters.add_widget(_widget)

    def remove_filter(self, filter) -> None:
        if self.ids.rule_filters:
            self.ids.rule_filters.remove_widget(filter)


class OneUIRuleLogicFilterWidget(OneUIGrid):
    remove = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4

    def on_release(self):
        if self.remove:
            try:
                self.remove(self)
            except:
                pass
        print("Remove filter")


class OneUIBrowserResponseHeaderPanel(OneUITopBar):

    def remove(self):
        pass

    def toggle(self):
        pass


class OneUIBrowserRuleData(OneUIBox):

    def add_header(self):
        header = OneUIBrowserRuleDataHeader()
        header.bind(delete=self.remove)
        self.ids.add_widget(header)

    def remove(self, child):
        self.remove_widget(child)


class OneUIBrowserRuleDataHeader(OneUIBox):

    def remove(self):
        pass
