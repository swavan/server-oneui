import os

from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

from widgets.layout import OneUIGrid


class OneUIFileChoosePopup(Popup):
    load = ObjectProperty()


class OneUIFileBar(OneUIGrid):
    file_url = ObjectProperty()
    modal = ObjectProperty(None)

    def open_popup(self):
        self.modal = OneUIFileChoosePopup(load=self.load)
        self.modal.open()

    def load(self, path: str, filename):
        full_path = os.path.join(path, filename[0])
        if self.file_url:
            self.file_url.text = full_path
        self.dismiss()

    def dismiss(self):
        self.modal.dismiss()
