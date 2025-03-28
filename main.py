from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import random
import os

MOODS = [
    "🔥열정",
    "😴나른",
    "🤯과부하",
    "✨영감",
    "😎여유",
    "🥶냉정",
    "🧠아이디어",
    "🫠현타",
]

# 폰트 경로 (예: 현재 디렉토리의 fonts 폴더)
# FONT_PATH = os.path.join("fonts", "NotoSansKR-Regular.otf")
FONT_PATH = os.path.join(
    os.path.dirname(__file__), "resources", "fonts", "malgunsl.ttf"
)


class MoodSpinnerApp(App):
    def build(self):
        self.root_layout = BoxLayout(orientation="vertical", padding=30, spacing=20)

        self.title_label = Label(
            text="🌀 무드 스피너", font_size=32, font_name=FONT_PATH
        )
        self.result_label = Label(
            text="기분을 골라보자!", font_size=24, font_name=FONT_PATH
        )
        self.advice_label = Label(
            text="", font_size=18, font_name=FONT_PATH, color=(0.5, 0.5, 0.5, 1)
        )

        self.spin_button = Button(
            text="돌려!", size_hint=(1, 0.3), font_size=20, font_name=FONT_PATH
        )
        self.spin_button.bind(on_press=self.spin_mood)

        self.root_layout.add_widget(self.title_label)
        self.root_layout.add_widget(self.result_label)
        self.root_layout.add_widget(self.advice_label)
        self.root_layout.add_widget(self.spin_button)

        return self.root_layout

    def spin_mood(self, instance):
        mood = random.choice(MOODS)
        self.result_label.text = f"🎉 오늘의 무드: {mood}"
        self.advice_label.text = self.get_ai_advice(mood)

    def get_ai_advice(self, mood):
        advice = {
            "🔥열정": "당신의 열정이 오늘 하루를 밝혀줄 거예요!",
            "😴나른": "천천히 가도 괜찮아요. 나른함도 당신의 일부예요.",
            "🤯과부하": "숨 좀 돌리세요. 당신은 잘하고 있어요.",
            "✨영감": "지금 떠오른 그 생각, 놓치지 마세요!",
            "😎여유": "이 여유 속에서 진짜 중요한 걸 보게 될 거예요.",
            "🥶냉정": "차분함은 때로 가장 강력한 무기예요.",
            "🧠아이디어": "지금의 아이디어가 미래를 바꿀지도 몰라요.",
            "🫠현타": "현타도 과정의 일부예요. 곧 다시 올라갈 거예요.",
        }
        return advice.get(mood, "오늘 하루도 당신답게 살아가세요.")


if __name__ == "__main__":
    MoodSpinnerApp().run()
