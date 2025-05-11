# 로컬 환경 세팅 가이드

## 0. api키는 카카오톡에서 주신 파일 안에 있습니다.
## 프론트 : npm start, 백 : python manage.py, FastAPI: uvicorn backend.main:app --reload --port 8001
```bash
# OpenAI API 키 설정
client = OpenAI(api_key="")
```

## 1. 프로젝트 클론
```bash
git clone https://github.com/OnTalk-mj/BackEnd.git
cd BackEnd
```

## 2. 가상환경 생성 및 활성화
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. 패키지 설치
```bash
pip install -r requirements.txt - 아직 구현 X, 안해도 작동 가능하게 함
```

## 4. Django 서버 실행
```bash
python manage.py migrate
python manage.py runserver
```

접속: `http://localhost:8000/`

## 5. 추가 설정 (Optional)
- `.env` 파일 필요 시 안내
- SECRET_KEY, DB 설정 등 따로 공지 (현재는 Settings에 할당, 추후에 바꿀 예정)

---

# 청소년 상담 챗봇 백엔드 API 명세서

## 공통

- Base URL: `http://localhost:8000/api/`
- 포맷: JSON
- 인증 필요: 일부 API (JWT AccessToken 필요)

---

# API 목록 요약

| API 이름 | 메서드 | URL | 인증 | 설명 |
|:---|:---|:---|:---|:---|
| 회원가입 | POST | `/api/accounts/signup/` | ❌ | 사용자 회원가입 |
| 로그인 | POST | `/api/accounts/login/` | ❌ | 사용자 로그인 (JWT 발급) |
| 토큰 재발급 | POST | `/api/refresh/` | ✅ Refresh Token 필요 | Access Token 재발급 |
| ID 중복 검사 | POST | `/api/accounts/id-check/` | ❌ | username 중복 여부 확인 |
| 내 정보 조회 | GET | `/api/accounts/mypage/` | ✅ | 현재 로그인한 사용자 정보 조회 |
| 내 정보 수정 | PATCH | `/api/accounts/mypage/update/` | ✅ | 사용자 개인정보 수정 |
| 상담센터 검색 | GET | `/api/consult/` | ❌ | 지역/키워드/상담 분야 필터 검색 |

---

# 회원 (accounts)

## 1. 회원가입
- URL: `/api/accounts/signup/`
- Method: `POST`
- 인증: X, 필요 없음

### 요청 예시
```json
{
  "username": "abcd1234@naver.com",
  "password": "비밀번호",
  "name": "홍길동",
  "birthdate": "20000101",
  "phone": "01012345678",
  "address": "서울시 강남구 테헤란로 123",
  "zipcode": "12345"
}
```

### 응답 예시
```json
{
  "message": "회원가입이 완료되었습니다!"
}
```

---

## 2. 로그인
- URL: `/api/accounts/login/`
- Method: `POST`
- 인증: X, 필요 없음

### 요청 예시
```json
{
  "username": "abcd1234@naver.com",
  "password": "비밀번호"
}
```

### 응답 예시
```json
{
  "refresh": "리프레시 토큰",
  "access": "액세스 토큰"
}
```

---

## 3. 토큰 재발급
- URL: `/api/refresh/`
- Method: `POST`
- 인증: O, Refresh Token 필요

### 요청 예시
```json
{
  "refresh": "리프레시 토큰"
}
```

### 응답 예시
```json
{
  "access": "새로운 액세스 토큰"
}
```

---

## 4. ID 중복 검사
- URL: `/api/accounts/id-check/`
- Method: `POST`
- 인증: X, 필요 없음

### 요청 예시
```json
{
  "username": "abcd1234@naver.com"
}
```

### 응답 예시
```json
{
  "exists": true
}
```

> `exists: true` ➔ 사용 불가  
> `exists: false` ➔ 사용 가능

---

# 📑 마이페이지 (mypage)

## 5. 내 정보 조회
- URL: `/api/accounts/mypage/`
- Method: `GET`
- 인증: O, Access Token 필요

### 응답 예시
```json
{
  "username": "abcd1234@naver.com",
  "email": "abcd1234@naver.com",
  "phone": "01012345678",
  "name": "홍길동",
  "birthdate": "20000101",
  "address": "서울시 강남구 테헤란로 123",
  "zipcode": "12345"
}
```

---

## 6. 내 정보 수정
- URL: `/api/accounts/mypage/update/`
- Method: `PATCH`
- 인증: O, Access Token 필요

### 요청 예시
```json
{
  "name": "홍길동",
  "birthdate": "20000101",
  "phone": "01012345678",
  "address": "서울시 강남구 테헤란로 123",
  "zipcode": "12345"
}
```

### 응답 예시
```json
{
  "message": "회원 정보가 수정되었습니다!"
}
```

---

# 🏢 상담센터 검색 (consult)

## 7. 상담센터 검색
- URL: `/api/consult/`
- Method: `GET`
- 인증: X, 필요 없음

### 쿼리 파라미터
- `region` (선택): 지역명 검색
- `keyword` (선택): 센터명 키워드 검색
- `fields` (선택): 상담 분야 검색 (콤마로 구분, 예: `진로,가족`)

### 요청 예시
```
GET /api/consult/?region=서울&keyword=청소년&fields=진로,가족
```

### 응답 예시
```json
[
  {
    "id": 1,
    "name": "서울청소년상담센터",
    "region": "서울특별시 강남구",
    "category": "진로,우울",
    "phone": "02-1234-5678",
    "address": "서울시 강남구 테헤란로 123",
    "latitude": 37.498095,
    "longitude": 127.02761
  }
]
```

---

# ⚠️ 주의사항
- `mypage/`, `mypage/update/` 호출 시 `Authorization: Bearer {AccessToken}` 헤더 필요
- 모든 요청/응답은 `Content-Type: application/json` 사용

---

