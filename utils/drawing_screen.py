import utils.fonts  # 폰트 등록 실행
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics.fbo import Fbo
from kivy.graphics import ClearBuffers, ClearColor, Scale, Translate
from kivy.core.image import Image as CoreImage
import os
from datetime import datetime
from kivy.app import App

class DrawingCanvas(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.line_width = 3
        self.current_line = None
        self.bind(size=self.update_canvas_size, pos=self.update_canvas_size)
        self.clear_canvas()

    def update_canvas_size(self, *args):
        self.clear_canvas()
        self.update_rect()

    def clear_canvas(self):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

    def update_rect(self, *args):
        if hasattr(self, 'bg_rect'):
            self.bg_rect.pos = self.pos
            self.bg_rect.size = self.size

    def on_touch_down(self, touch):
        with self.canvas:
            Color(0, 0, 0)
            self.current_line = Line(points=[touch.x, touch.y], width=self.line_width)

    def on_touch_move(self, touch):
        if self.current_line:
            self.current_line.points += [touch.x, touch.y]

    def save(self, save_path):
        fbo = Fbo(size=self.size)
        with fbo:
            ClearColor(1, 1, 1, 1)
            ClearBuffers()
            Scale(1, -1, 1)
            Translate(0, -self.height, 0)
            self.canvas.draw()

        fbo.draw()
        texture = fbo.texture
        texture.save(save_path, flipped=False)

class DrawingScreen(Screen):
    def __init__(self, on_save_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()
        self.canvas_widget = DrawingCanvas(size_hint=(1, 0.9), pos_hint={"top": 1})
        self.layout.add_widget(self.canvas_widget)

        self.save_btn = Button(text="저장", font_name="KoreanFont", size_hint=(0.3, 0.08), pos_hint={"center_x": 0.25, "y": 0.01})
        self.clear_btn = Button(text="지우기", font_name="KoreanFont", size_hint=(0.3, 0.08), pos_hint={"center_x": 0.75, "y": 0.01})
        self.save_btn.bind(on_release=self.save_drawing)
        self.clear_btn.bind(on_release=self.clear_drawing)

        self.layout.add_widget(self.save_btn)
        self.layout.add_widget(self.clear_btn)
        self.add_widget(self.layout)

        self.on_save_callback = on_save_callback

    def save_drawing(self, instance):
        save_dir = os.path.join(App.get_running_app().user_data_dir, "drawings")
        os.makedirs(save_dir, exist_ok=True)
        filename = f"drawing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        save_path = os.path.join(save_dir, filename)
        self.canvas_widget.save(save_path)
        print(f"[✔] 그림 저장됨: {save_path}")

        if self.on_save_callback:
            self.on_save_callback(save_path)
        else:
            self.manager.current = "main"

    def clear_drawing(self, instance):
        self.canvas_widget.clear_canvas()
