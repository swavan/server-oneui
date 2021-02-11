from kivy.properties import StringProperty
from kivymd.uix.list import ILeftBody, IRightBody, OneLineAvatarIconListItem, \
    OneLineAvatarListItem
from kivymd.uix.selectioncontrol import MDCheckbox, MDSwitch


class OneUILeftSwitch(ILeftBody, MDSwitch):
    pass


class OneUIRightSwitch(IRightBody, MDSwitch):
    pass


class OneUIRightCheckbox(IRightBody, MDCheckbox):
    pass


class OneUILeftCheckbox(ILeftBody, MDCheckbox):
    pass


class OneUISingleIconWithCheckbox(OneLineAvatarIconListItem):
    icon = StringProperty("android")


class OneUISingleItemWithCheckbox(OneLineAvatarListItem):
    pass


class OneUISingleItemWithSwitch(OneLineAvatarListItem):
    pass
