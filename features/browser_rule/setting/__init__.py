import webbrowser

from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineAvatarListItem

from widgets.layout import OneUIBox

Builder.load_file("features/browser_rule/setting/ui.kv")


class OneUIBrowserRuleSetting(OneUIBox):
    pass


class OneUIBrowserRuleReloadOnAction(OneLineAvatarListItem):
    pass


class OneUIBrowserRuleChangeMockServer(OneUIBox):
    pass


class OneUIBrowserResourceType(OneLineAvatarListItem):
    def on_release(self):
        if self.ids.left_checkbox.active:
            self.ids.left_checkbox.active = False
        else:
            self.ids.left_checkbox.active = True


class OneUIBrowserRuleResourceTypes(OneUIBox):
    resources = ListProperty()

    def on_resources(self, _, resources):
        if self.ids:
            for resource in resources:
                row = OneUIBrowserResourceType()
                row.text = resource.title()
                self.ids.browser_rile_filter_resource_type.add_widget(row)

    def open_page(self):
        webbrowser.open("https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/webRequest/ResourceType")