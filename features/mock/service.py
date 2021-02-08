import enum
from typing import Any

from kivy.event import EventDispatcher
from kivy.properties import NumericProperty, ListProperty, Property


class Action(enum.Enum):
    Add = 1
    Edit = 2
    Delete = 3
    Load = 4


class MockEvent(EventDispatcher):
    def __init__(self, **kwargs):
        self.register_event_type('on_save')
        self.register_event_type('on_load')
        self.register_event_type('on_delete')
        self.register_event_type('on_edit')
        self.register_event_type('on_error')
        super(MockEvent, self).__init__(**kwargs)

    def on_save(self, *args):
        pass

    def on_load(self, *args):
        pass

    def on_delete(self, *args):
        pass

    def on_edit(self, *args):
        pass

    def on_error(self, *args):
        pass

    def load(self, val: Any):
        self.dispatch('on_load', val)

    def save(self, val: Any):
        self.dispatch('on_save', val)

    def edit(self, val: Any):
        self.dispatch('on_edit', val)

    def delete(self, val: Any):
        self.dispatch('on_delete', val)

    def error(self, val: Any):
        self.dispatch('on_error', val)


class MockService:
    event = None

    @classmethod
    def load(cls) -> MockEvent:
        if MockService.event is None:
            MockService.event = MockEvent()
