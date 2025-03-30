import os
from datetime import datetime
from kivy.core.window import Window
from kivy.app import App


def save_result_screenshot(prefix="moodshare"):
    """
    현재 앱 화면을 캡처하여 PNG 이미지로 저장합니다.
    저장 경로는 앱의 user_data_dir 하위입니다.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}_{timestamp}.png"
    path = os.path.join(App.get_running_app().user_data_dir, filename)
    Window.screenshot(name=path)
    print(f"[✔] 결과 이미지 저장 완료: {path}")
    return path
