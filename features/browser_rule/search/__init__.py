from kivy.lang import Builder
from kivymd.uix.screen import MDScreen

Builder.load_file("features/browser_rule/search/ui.kv")


class OneUIBrowserRuleSearch(MDScreen):

    def search(self, query: str):
        print("Search: ", query)
