import os

from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup

from widgets.layout import OneUIGrid, OneUIBox
from widgets.text import OneUITextFieldWrapper


class OneUIFileChoosePopup(Popup):
    load = ObjectProperty()


class OneUIFileBar(OneUITextFieldWrapper):
    file_url = ObjectProperty()
    modal = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(OneUIFileBar, self).__init__(**kwargs)
        self.cols = 2

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

    @property
    def text(self):
        return "" if self.file_url == "" else self.file_url.text

    @text.setter
    def text(self, val: str):
        self.file_url.text = val


class OneUIFileOptionAction(ButtonBehavior, OneUIBox):
    pass
