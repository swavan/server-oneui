import os

import trio as trio
from kivy.config import Config
from kivy.base import async_runTouchApp
# from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from features.home.manager import OneUIPageManager

# Window.shape_color_key = [0, 0, 0, 1]
# Window.raise_window()
# Window.clearcolor = [0, 0, 0, 1]


class OneUI(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SwaVanServerApp(MDApp):
    def build(self):
        self.title = "SwaVan Server"

        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.primary_hue = "900"

        templates = f"templates"
        for kv_file in os.listdir(templates):
            Builder.load_file(os.path.join(templates, kv_file))
        return OneUIPageManager()


if __name__ == '__main__':
    Config.set('kivy', 'desktop', 1)
    Config.set('kivy', 'window_icon', 'assets/images/logo.png')
    Config.set('graphics', 'borderless', False)
    Config.write()
    trio.run(async_runTouchApp, SwaVanServerApp().run(), "trio")
