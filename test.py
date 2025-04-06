from kivy.app import App
from kivy.uix.label import Label
from kivy.core.text import LabelBase
import os

LabelBase.register(name="KoreanFont", fn_regular="resources/fonts/malgunsl.ttf")

class TestApp(App):
    def build(self):
        return Label(text="안녕하세요", font_name="KoreanFont", font_size=30)

if __name__ == '__main__':
    TestApp().run()