# Mood Spinner: 단계별 배경색 연출 (Result 화면 필터 제거)

import os
import json
import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.clock import Clock

from utils.share_utils import save_result_screenshot

# 경로 및 설정
BASE_DIR = os.path.dirname(__file__)
FONT_PATH = os.path.join(BASE_DIR, "resources", "fonts", "malgunsl.ttf")
CHOICE_FILE = os.path.join(BASE_DIR, "resources", "choices.json")
BG_IMAGE = os.path.join(BASE_DIR, "resources", "images", "background_main.png")

LabelBase.register(name="KoreanFont", fn_regular=FONT_PATH)
Window.size = (360, 780)

MOODS = ["열정", "나른함", "영감", "여유", "냉정", "현타"]
planner_choices = {"start": None, "middle": None, "end": None}


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = FloatLayout()

        self.bg = Image(
            source=BG_IMAGE,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
        )
        self.layout.add_widget(self.bg)

        self.label = Label(
            text="오늘의 무드를 골라볼까요?",
            pos_hint={"center_x": 0.5, "center_y": 0.7},
            font_size=22,
            font_name="KoreanFont",
            color=(0, 0, 0, 1),
        )
        self.layout.add_widget(self.label)

        self.spin_button = Button(
            text="룰렛 돌리기",
            size_hint=(0.5, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            font_name="KoreanFont",
        )
        self.spin_button.bind(on_release=self.start_spin)
        self.layout.add_widget(self.spin_button)

        self.plan_button = Button(
            text="기분 따라가기",
            size_hint=(0.5, 0.08),
            pos_hint={"center_x": 0.5, "center_y": 0.35},
            font_name="KoreanFont",
            disabled=True,
        )
        self.plan_button.bind(on_release=self.go_to_planner)
        self.layout.add_widget(self.plan_button)

        self.add_widget(self.layout)
        self.spin_count = 0

    def start_spin(self, instance):
        self.spin_count = 0
        self.label.text = "룰렛을 돌리는 중..."
        Clock.schedule_interval(self.spin_animation, 0.05)

    def spin_animation(self, dt):
        if self.spin_count >= 20:
            Clock.unschedule(self.spin_animation)
            mood = self.final_mood
            App.get_running_app().selected_mood = mood
            self.label.text = f"오늘의 무드: {mood}"
            self.plan_button.disabled = False
            return False
        else:
            self.final_mood = random.choice(MOODS)
            self.label.text = f"🤔 {self.final_mood}"
            self.spin_count += 1

    def go_to_planner(self, instance):
        planner_choices.update({"start": None, "middle": None, "end": None})
        App.get_running_app().generate_random_choices()
        self.manager.current = "start"


class SelectButton(Button):
    def __init__(self, stage, value, **kwargs):
        super().__init__(**kwargs)
        self.text = value
        self.font_name = "KoreanFont"
        self.font_size = 16
        self.size_hint = (0.8, None)
        self.height = 50
        self.stage = stage
        self.value = value
        self.bind(on_release=self.select)

    def select(self, instance):
        planner_choices[self.stage] = self.value
        App.get_running_app().root.current = {
            "start": "middle",
            "middle": "end",
            "end": "result",
        }[self.stage]


class StepScreen(Screen):
    def __init__(self, stage, **kwargs):
        super().__init__(**kwargs)
        self.stage = stage
        self.layout = FloatLayout()

        stage_color = {
            "start": (1, 1, 1, 1),
            "middle": (1, 0.95, 0.85, 1),
            "end": (0.85, 0.9, 1, 1),
        }.get(stage, (1, 1, 1, 1))

        self.bg = Image(
            source=BG_IMAGE,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            color=stage_color,
        )
        self.layout.add_widget(self.bg)

        self.label = Label(
            text=f"{stage.capitalize()} 단계: 선택하세요",
            size_hint=(1, 0.1),
            pos_hint={"top": 1},
            font_size=20,
            font_name="KoreanFont",
            color=(0, 0, 0, 1),
        )
        self.layout.add_widget(self.label)
        self.add_widget(self.layout)

    def on_pre_enter(self):
        for widget in list(self.layout.children):
            if isinstance(widget, SelectButton):
                self.layout.remove_widget(widget)

        options = App.get_running_app().random_options[self.stage]
        for idx, opt in enumerate(options):
            btn = SelectButton(
                self.stage,
                opt,
                pos_hint={"center_x": 0.5, "center_y": 0.7 - idx * 0.15},
            )
            self.layout.add_widget(btn)


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()

        self.bg = Image(
            source=BG_IMAGE,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
        )
        layout.add_widget(self.bg)

        self.label = Label(
            text="",
            font_size=18,
            font_name="KoreanFont",
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            size_hint=(0.9, None),
            color=(0, 0, 0, 1),
        )
        layout.add_widget(self.label)

        def go_home(instance):
            App.get_running_app().root.current = "main"

        back_btn = Button(
            text="처음으로",
            size_hint=(0.4, 0.08),
            pos_hint={"center_x": 0.5, "y": 0.05},
            font_name="KoreanFont",
        )
        back_btn.bind(on_release=go_home)
        layout.add_widget(back_btn)

        share_btn = Button(
            text="이미지로 저장하기",
            size_hint=(0.5, 0.08),
            pos_hint={"center_x": 0.5, "y": 0.15},
            font_name="KoreanFont",
        )
        share_btn.bind(on_release=lambda instance: save_result_screenshot())
        layout.add_widget(share_btn)

        self.add_widget(layout)

    def on_pre_enter(self):
        s = planner_choices["start"]
        m = planner_choices["middle"]
        e = planner_choices["end"]
        mood = App.get_running_app().selected_mood
        text = f"""
오늘의 기분: {mood}
하루 이렇게 보내보는 건 어때요?

    » 아침 – {s}
    » 낮 – {m}
    » 밤 – {e}
"""
        self.label.text = text.strip()


class MoodPlannerApp(App):
    def build(self):
        self.selected_mood = None
        self.random_options = {}
        self.choice_pool = self.load_choice_pool()

        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(StepScreen("start", name="start"))
        sm.add_widget(StepScreen("middle", name="middle"))
        sm.add_widget(StepScreen("end", name="end"))
        sm.add_widget(ResultScreen(name="result"))

        return sm

    def load_choice_pool(self):
        try:
            with open(CHOICE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[오류] 선택지 불러오기 실패: {e}")
            return {"start": [], "middle": [], "end": []}

    def generate_random_choices(self):
        self.random_options = {
            stage: random.sample(self.choice_pool.get(stage, []), 3)
            for stage in ["start", "middle", "end"]
        }


if __name__ == "__main__":
    MoodPlannerApp().run()
