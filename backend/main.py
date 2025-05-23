from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models.logic import detect_emotion_and_danger, recommend_videos, generate_video_response
from models.counselor import generate_response

app = FastAPI()

class TextInput(BaseModel):
    text: str

class ChatRequest(BaseModel):
    text: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/recommend-videos")
async def recommend_videos_route(input: TextInput):
    try:
        user_input = input.text
        if not user_input:
            raise HTTPException(status_code=400, detail="text 값이 필요합니다.")

        emotion, danger = detect_emotion_and_danger(user_input)
        videos = recommend_videos(emotion, danger)

        if not videos:
            return {"response": ""}

        response = generate_video_response(emotion, danger, videos)
        return {"response": response}

    except Exception as e:
        print("🔥 서버 오류:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/counselor/")
async def chat_endpoint(req: ChatRequest):
    reply = generate_response(req.text)
    return {"response": reply}