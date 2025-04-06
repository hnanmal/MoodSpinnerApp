from kivy.core.text import LabelBase
import os

# 앱 기준 폰트 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FONT_PATH = os.path.join(BASE_DIR, "resources", "fonts", "malgunsl.ttf")

LabelBase.register(name="KoreanFont", fn_regular=FONT_PATH)

__all__ = ["FONT_PATH"]