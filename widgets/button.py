from kivy.uix.button import Button
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.behaviors.touchripple import TouchRippleButtonBehavior


class OneUIRippleButton(TouchRippleButtonBehavior, Button):
    def __init__(self, **kwargs):
        super(OneUIRippleButton, self).__init__(**kwargs)


class OneUIBaseButton(Button):
    back_color = ListProperty([1, 0, 1, 1])

    def __init__(self, **kwargs):
        super(OneUIBaseButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ""


class OneUIButton(OneUIBaseButton):
    border_radius = ListProperty([10])


class OneUIStrokeButton(OneUIBaseButton):
    border_radius = NumericProperty(10)


class OneUIToggleButton(OneUIBaseButton):
    border_radius = ListProperty([10])


class OneUIStrokeToggleButton(OneUIBaseButton):
    border_radius = NumericProperty(10)
