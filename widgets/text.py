from kivy.metrics import dp
from kivy.uix.textinput import TextInput
from kivy.properties import ListProperty, NumericProperty
from configs.color import OneUIColors
from configs.image import OneUIBackground


class OneUITextRaw(TextInput):
    pressed = None

    def __init__(self, **kwargs):
        super(OneUITextRaw, self).__init__(**kwargs)
        self.border = [10, 10, 10, 10]
        self.padding = ['12dp', '16dp', '12dp', '12dp']


class OneUITextField(OneUITextRaw):
    border_color = ListProperty([1, 1, 1, 1])
    border_radius = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(OneUITextField, self).__init__(**kwargs)
        self.background_normal = OneUIBackground.clear
        self.font_size = '14sp'
        self.background_color = OneUIColors.TextField.value
        self.hint_text_color = [0, 0, 0, 0.5]
        self.cursor_color = [0, 0, 0, 0.8]
        self.foreground_color = [0, 0, 0, 1]
        self.selection_color = [0, 1, 0, 1]

        self.padding = ['12dp', '16dp']
        self.halign = 'left'
        self.border = [8, 8, 8, 8]
        self.size_hint = (1, None)
        self.multiline = False
        self.write_tab = False


class OneUITextArea(OneUITextField):
    def __init__(self, **kwargs):
        super(OneUITextArea, self).__init__(**kwargs)
        self.multiline = True
        self.height = dp(150)


class NumberInputField(OneUITextRaw):
    start = NumericProperty(0)
    end = NumericProperty(0)

    def __init__(self, **kwargs):
        super(NumberInputField, self).__init__(**kwargs)
        self.background_normal = OneUIBackground.clear
        self.background_color = OneUIColors.TextField.value
        self.hint_text_color = [0, 0, 0, 0.5]
        self.cursor_color = [0, 0, 0, 0.8]
        self.foreground_color = [0, 0, 0, 1]
        self.selection_color = 0.925, 0.941, 0.937, 0.5
        self.size_hint_y = None
        self.height = dp(50)

    def insert_text(self, port: str, from_undo=False):
        try:
            _value = self.text + port
            _port_number = int(_value)
            if self.start <= _port_number <= self.end:
                return super(NumberInputField, self).insert_text(port, from_undo=from_undo)
        except ValueError as _:
            pass
