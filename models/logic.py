# ✅ AI 로직 최종본 (GPT는 유튜브 영상 추천 전용, 공감 제거)
# backend/models/logic.py

import json
import random
import os
import re
from openai import OpenAI

config_path = os.path.join(os.path.dirname(__file__), "../config/openai_config.json")

with open(config_path, "r") as f:
    config = json.load(f)
    api_key = config.get("api_key")

    client = OpenAI(api_key=api_key)

# 유튜브 영상 추천 JSON 불러오기
base_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(base_dir, "..", "final_video_recommendations_clean.json")

with open(json_path, "r", encoding="utf-8") as f:
    video_data = json.load(f)

# ✅ 감정 및 위험 키워드 탐지 함수 (상담 응답용 모델과 연결 전용)
def detect_emotion_and_danger(text):
    emotion_prompt = f"""
다음 문장의 감정을 하나로 분류해줘.
["우울", "불안", "무기력", "자존감 낮음", "스트레스", "분노"] 중 하나.
문장: "{text}"
감정:
"""
    emotion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": emotion_prompt}],
        temperature=0.3,
        max_tokens=10
    ).choices[0].message.content.strip()

    danger_map = {
        "자해": ["자해", "죽고 싶", "손목", "칼", "없어졌으면"],
        "학교폭력": ["학교폭력", "친구가 때려", "괴롭힘", "왕따", "따돌림", "따돌려"],
        "가정폭력": ["부모님이 때려", "집에서 맞았어요", "가정폭력", "때려", "맞았어", "아빠가 떄려", "엄마가 떄려", "집에서 폭력을"],
        "데이트폭력": ["연인이 때려", "데이트폭력", "남자친구가 때려"]
    }
    danger = None
    for label, keywords in danger_map.items():
        if any(kw in text for kw in keywords):
            danger = label
            break

    return emotion, danger

# ✅ 감정/위험 기반 영상 리스트 반환
def recommend_videos(emotion=None, danger=None, max_k=3):
    if danger:
        if danger == "자해":
            return video_data["위험상황별"]["자해"][:max_k]
        else:
            return video_data["위험상황별"]["폭력"].get(danger, [])[:max_k]
    elif emotion:
        return video_data["감정별"].get(emotion, [])[:max_k]
    return []

# ✅ GPT를 통해 영상 소개 멘트만 생성 (공감 제거)
def generate_video_response(emotion, danger, video_links):
    video_list = "\n".join(f"- {v}" for v in video_links)

    prompt = f"""
너는 상담 챗봇의 보조 역할을 맡고 있어.
주 상담은 이미 다른 AI 모델이 처리했으며, 너는 유튜브 영상 추천을 자연스럽게 소개하는 역할이야.

다음 규칙을 지켜줘:
- 공감 멘트는 절대 쓰지 마
- 같은 말 반복하지 마
- 영상이 있다면 자연스럽게 목적에 맞게 소개해줘
- 영상이 없다면 말하지 않아도 돼
- 같은 말 반복하지 말고 영상 하나하나를 맞게 소개해줘

감정: {emotion}
위험 상황: {danger}
추천 영상:
{video_list}

응답:
"""

    result = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.75,
        max_tokens=400
    )
    return convert_links_to_iframe(result.choices[0].message.content.strip())

def convert_links_to_iframe(text):
    pattern = r"(https:\/\/(?:www\.)?youtube\.com\/watch\?v=|https:\/\/youtu\.be\/)([a-zA-Z0-9_-]{11})"
    return re.sub(
    pattern,
    lambda m: f'''
        <div style="margin-top: 10px; margin-bottom: 10px;">
            <iframe
                width="100%"
                height="600"
                src="https://www.youtube.com/embed/{m.group(2)}"
                title="YouTube video"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
                style="border-radius: 8px;"
            ></iframe>
        </div>
    ''',
    text
)