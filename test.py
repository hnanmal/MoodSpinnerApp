import requests
import json


def generate_advice_locally(mood):
    prompt = f"오늘 기분이 '{mood}'일 때, 사용자에게 감성적인 한마디를 해줘."

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt},
        stream=True,
    )

    result = ""
    for line in response.iter_lines():
        if line:
            try:
                data = json.loads(line.decode("utf-8"))
                result += data.get("response", "")
            except json.JSONDecodeError:
                continue  # 무시하고 다음 줄로

    return result.strip()


# 테스트 출력
print(generate_advice_locally("영감"))
