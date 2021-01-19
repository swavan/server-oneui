from kivymd.uix.screen import MDScreen
class OneUIMockPage(MDScreen):

    def __init__(self, **kwargs):
        super(OneUIMockPage, self).__init__(**kwargs)

    def switch(self, name: str) -> None:
        self.ids.mock_screen_manager.current = name

