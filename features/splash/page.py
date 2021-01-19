import time

from kivy.clock import Clock
from kivy.properties import ObjectProperty, NumericProperty
from kivymd.uix.screen import MDScreen


class OneUISplashPage(MDScreen):
    screen_manager = None
    progress_val = NumericProperty(0)

    def on_enter(self):
        Clock.schedule_once(self.launch_one_ui, 5)
        Clock.schedule_once(self.update_progress, 2)

    def launch_one_ui(self, args):
        self.screen_manager.current = "OneUI"

    def update_progress(self, args):
        for i in range(100):
            time.sleep(0.1)
            self.progress_val = 99

