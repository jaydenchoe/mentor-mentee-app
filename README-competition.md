# 멘토-멘티 매칭 앱

대회 요구사항에 따라 개발된 멘토-멘티 매칭 웹 애플리케이션입니다.

## 🚀 실행 방법

### 백엔드 실행
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

백엔드가 http://localhost:8080 에서 실행됩니다.

### 프론트엔드 실행
```bash
cd frontend
python3 -m http.server 3000
```

프론트엔드가 http://localhost:3000 에서 실행됩니다.

## 📋 기능

- 회원가입/로그인 (JWT 인증)
- 프로필 관리 (이미지 업로드 포함)
- 멘토 검색 및 목록 조회
- 매칭 요청 및 수락/거절
- 역할별 네비게이션

## 🛠 기술 스택

- **백엔드**: Python Flask, SQLite, JWT
- **프론트엔드**: Vanilla JavaScript, HTML5, CSS3
- **API 문서**: Swagger/OpenAPI

## 📡 API 엔드포인트

- Swagger UI: http://localhost:8080/
- OpenAPI JSON: http://localhost:8080/openapi.json
- API Base: http://localhost:8080/api

## ✅ 대회 요구사항 준수

- ✅ 포트: 프론트엔드(3000), 백엔드(8080)
- ✅ JWT 토큰 (RFC 7519 표준 클레임)
- ✅ OpenAPI 문서 및 Swagger UI
- ✅ 테스트 ID 요구사항 준수
- ✅ 프로필 이미지 업로드 및 검증
- ✅ 보안 (SQL 인젝션, XSS 방지)

## 🧪 테스트 사용자

애플리케이션 시작 시 자동으로 생성되는 데모 사용자들:

**멘토:**
- mentor1@example.com / password123
- mentor2@example.com / password123
- (총 5명)

**멘티:**
- mentee1@example.com / password123
- mentee2@example.com / password123
- (총 5명)
