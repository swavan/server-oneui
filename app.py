import os

import trio as trio
from kivy.config import Config
from kivy.base import async_runTouchApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from pony import orm
from features.home.manager import OneUIPageManager
from storage import db


class OneUI(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


def startup_database():
    db.bind(provider='sqlite', filename='swavan.sqlite', create_db=True)
    orm.sql_debug(False)


class SwaVanServerApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        startup_database()

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
    Config.set('graphics', 'window_state', 'restore')
    Config.set('kivy', 'window_icon', 'assets/images/logo/big.png')
    Config.set('graphics', 'borderless', False)
    Config.set('graphics', 'width', '1000')
    Config.set('graphics', 'height', '800')
    Config.set('graphics', 'minimum_width', '800')
    Config.set('graphics', 'minimum_height', '600')
    Config.write()
    trio.run(async_runTouchApp, SwaVanServerApp().run(), "trio")
