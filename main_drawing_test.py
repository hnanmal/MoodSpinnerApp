from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.core.text import LabelBase
from utils.drawing_screen import DrawingCanvas  # 기존 코드에서 가져옴
from utils.fonts import FONT_PATH

import os
from datetime import datetime

# 폰트 등록
LabelBase.register(name="KoreanFont", fn_regular=FONT_PATH)


class DrawingTestApp(App):
    def build(self):
        layout = FloatLayout()
        self.canvas_widget = DrawingCanvas(size_hint=(1, 0.9), pos_hint={"top": 1})
        layout.add_widget(self.canvas_widget)

        save_btn = Button(
            text="저장",
            font_name="KoreanFont",
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.25, "y": 0.02},
        )
        clear_btn = Button(
            text="지우기",
            font_name="KoreanFont",
            size_hint=(0.3, 0.1),
            pos_hint={"center_x": 0.75, "y": 0.02},
        )

        save_btn.bind(on_release=self.save_drawing)
        clear_btn.bind(on_release=self.clear_drawing)

        layout.add_widget(save_btn)
        layout.add_widget(clear_btn)

        return layout

    def save_drawing(self, instance):
        save_dir = os.path.join(self.user_data_dir, "drawings_test")
        os.makedirs(save_dir, exist_ok=True)
        filename = f"drawing_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        save_path = os.path.join(save_dir, filename)

        print(f"[INFO] 저장 경로: {save_path}")
        try:
            self.canvas_widget.export_to_png(save_path)
            print(f"[✔] 저장 완료: {save_path}")
        except Exception as e:
            print("[❌] 저장 실패:", e)

    def clear_drawing(self, instance):
        self.canvas_widget.clear_canvas()


if __name__ == "__main__":
    Window.size = (360, 720)
    DrawingTestApp().run()
