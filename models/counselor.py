# backend/models/counselor.py

import torch
import os
import gc
from transformers import AutoTokenizer, AutoModelForCausalLM

# 모델 경로 및 장치 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../model")
MODEL_PATH = os.path.normpath(MODEL_PATH)  # 실제 모델 디렉토리 경로에 맞게
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("모델 경로:", MODEL_PATH)

# 시스템 프롬프트 (스트림릿 코드 기반)
SYSTEM_PROMPT = """
당신은 공감 능력이 뛰어난 전문 청소년 상담사입니다.
(중략) [원래 텍스트 유지]
"""

# 모델 로딩 (서버 시작 시 1회만 실행)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto",
    low_cpu_mem_usage=True
)
model.eval()

def clear_cuda_cache():
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()

# FastAPI에서 호출할 응답 생성 함수
def generate_response(user_input: str) -> str:
    conversation = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]

    prompt = tokenizer.apply_chat_template(conversation, tokenize=False)
    prompt += "<|im_start|>assistant\n"

    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=1024,
            do_sample=True,
            temperature=0.8,
            top_p=0.9,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=[
                tokenizer.convert_tokens_to_ids("<|endofturn|>"),
                tokenizer.convert_tokens_to_ids("<|im_end|>")
            ],
            no_repeat_ngram_size=3,
            repetition_penalty=1.2
        )

    decoded = tokenizer.decode(outputs[0][inputs.input_ids.shape[-1]:], skip_special_tokens=False)

    for eos in ["<|endofturn|>", "<|im_end|>"]:
        if eos in decoded:
            decoded = decoded.split(eos)[0]

    return decoded.strip()