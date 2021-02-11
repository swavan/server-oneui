from typing import List

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

from features.browser_rule import data
from features.browser_rule.controller import BrowserRuleController

Builder.load_file("features/browser_rule/ui.kv")


class OneUIBrowserRulePage(MDScreen):

    @property
    def right_size_menu_items(self) -> List:
        return [
            ['arrange-bring-to-front', lambda x: self.ids.browser_rule_drawer.set_state("toggle")],
            ['cog', lambda x: self.change_screen("browser-rules-setting", x)]
        ]

    def change_screen(self, name: str, _) -> None:
        self.ids.browser_screen_manager.current = name

    def load_rules(self) -> None:
        rows = BrowserRuleController.load()
        print(rows)
        self.ids.one_ui_browser_rules.rules = BrowserRuleController.load()

    def edit(self, rule: data.Rule):
        self.change_screen("add-browser-rule", self)
        self.ids.browser_rule_creator.rule = rule
        
    def remove(self, rule: data.Rule):
        BrowserRuleController.save(rule, True)
        self.load_rules()

    def add(self):
        self.ids.browser_rule_creator.rule = data.Rule()
        self.change_screen("add-browser-rule", self)
