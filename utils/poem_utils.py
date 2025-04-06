import os
# import openai

# 안전하게 OpenAI 클라이언트 설정
api_key = os.getenv("OPENAI_API_KEY")
client = None

# if not api_key:
#     print("[경고] OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")
# else:
#     client = openai.OpenAI(api_key=api_key)


def generate_poem_with_openai(mood, s, m, e):
    """
    하루의 기분과 계획을 바탕으로 감성적인 시를 생성
    """
    prompt = f"""
오늘의 기분은 "{mood}"입니다.
아침 – {s}
낮 – {m}
밤 – {e}

이 하루 계획을 바탕으로 짧은 감성 시 한 편을 써줘.
3~5줄 이내로, 한국어로, 이모지 없이, 감성적으로.
"""
    if client is None:
        return "❗API 키가 설정되지 않아 시를 생성할 수 없습니다."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.9,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[OpenAI 오류] {e}")
        return "시를 생성하는 데 문제가 발생했어요."
