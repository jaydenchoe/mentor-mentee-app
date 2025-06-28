# 멘토-멘티 매칭 웹앱

천하제일 입코딩 대회 2025 출품작 - Python Flask 백엔드와 Vanilla JavaScript 프론트엔드로 구현한 멘토와 멘티를 매칭하는 웹 애플리케이션입니다.

## 🌟 주요 기능

- JWT 기반 회원가입 및 로그인 인증
- 역할별 프로필 관리 (멘토/멘티)
- 이미지 업로드를 포함한 프로필 관리
- 멘토 검색 및 필터링/정렬
- 매칭 요청 시스템 (요청/수락/거절)
- 역할 기반 접근 제어
- OpenAPI 3.0 문서화

## 🛠 기술 스택

### 백엔드
- **Python Flask** - 웹 프레임워크
- **SQLAlchemy + SQLite** - 데이터베이스 ORM
- **JWT Authentication** - 인증 시스템
- **Flask-CORS** - 크로스 오리진 요청 처리
- **Swagger UI** - API 문서화

### 프론트엔드
- **Vanilla JavaScript** - 순수 자바스크립트
- **HTML5 + CSS3** - 마크업 및 스타일링
- **Python HTTP Server** - 개발 서버
- **반응형 웹 디자인** - 모바일/데스크톱 지원

## 📋 사전 요구사항

- **Python 3.8 이상**
- **웹 브라우저** (Chrome, Firefox, Safari 등)

## 🚀 설치 및 실행 방법

### 1. 프로젝트 클론
```bash
git clone [리포지토리 URL]
cd mentor-mentee-app
```

### 2. 백엔드 서버 실행 (터미널 1)
```bash
chmod +x start-backend.sh
./start-backend.sh
```

**또는 수동 실행:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
python app.py
```

### 3. 프론트엔드 서버 실행 (터미널 2)
```bash
chmod +x start-frontend.sh
./start-frontend.sh
```

**또는 수동 실행:**
```bash
cd frontend
python3 -m http.server 3000
```

## 🌐 접속 주소

- **프론트엔드 앱**: http://localhost:3000
- **백엔드 API**: http://localhost:8080/api
- **Swagger UI**: http://localhost:8080/swagger-ui
- **OpenAPI 문서**: http://localhost:8080/api/openapi.json

## 📱 사용 방법

### 1. 회원가입 및 로그인
- 이메일, 비밀번호, 역할(멘토/멘티)로 회원가입
- 이메일과 비밀번호로 로그인
- **아이콘 로그인**: 데모 계정으로 간편 로그인 가능

### 2. 프로필 관리
- 이름, 자기소개, 프로필 이미지 등록/수정
- **멘토**: 기술 스택 추가 등록
- **멘티**: 기본 프로필 정보만 등록

### 3. 멘토 찾기 (멘티 전용)
- 멘토 목록 조회
- 기술 스택으로 검색/필터링
- 이름/기술 스택별 정렬
- 매칭 요청 메시지와 함께 전송

### 4. 매칭 관리
- **멘티**: 보낸 요청 상태 확인, 요청 취소
- **멘토**: 받은 요청 확인, 수락/거절 (한 명만 수락 가능)

### 5. 데모 계정 (자동 생성)
**멘토 계정들:**
- mentor1@test.com ~ mentor5@test.com / password123

**멘티 계정들:**
- mentee1@test.com ~ mentee5@test.com / password123

## 🗄 데이터베이스

SQLite 데이터베이스가 첫 실행 시 `backend/mentor_mentee.db`에 자동 생성되며, 데모 데이터가 포함됩니다.

## 🔒 보안 기능

- **JWT 토큰 인증** (1시간 유효기간, RFC 7519 클레임 준수)
- **비밀번호 해싱** (Werkzeug 사용)
- **입력 값 검증 및 필터링**
- **SQL 인젝션 방지** (SQLAlchemy ORM)
- **XSS 공격 방지**
- **이미지 업로드 검증** (형식/크기/해상도)

## 📁 프로젝트 구조

```
mentor-mentee-app/
├── backend/
│   ├── app.py                  # Flask 메인 애플리케이션
│   ├── requirements.txt        # Python 의존성
│   ├── mentor_mentee.db       # SQLite 데이터베이스 (자동 생성)
│   └── uploads/               # 업로드 파일 저장소
├── frontend/
│   ├── index.html             # 메인 HTML
│   ├── styles.css             # 스타일시트
│   ├── app.js                 # JavaScript 로직
│   └── package.json           # 프로젝트 정보
├── start-backend.sh           # 백엔드 실행 스크립트
├── start-frontend.sh          # 프론트엔드 실행 스크립트
└── README.md
```

## 🎯 구현된 대회 요구사항

✅ **포트 준수**: 프론트엔드 3000, 백엔드 8080  
✅ **OpenAPI 문서화**: Swagger UI 자동 생성  
✅ **JWT 표준 클레임**: RFC 7519 모든 클레임 구현  
✅ **사용자 스토리**: 모든 테스트 ID 구현  
✅ **보안**: SQL 인젝션, XSS 방지  
✅ **프로필 이미지**: 기본 이미지 및 업로드 지원  
✅ **데이터베이스**: SQLite 자동 초기화  

## 🐛 문제 해결

1. **포트 충돌**: 3000, 8080 포트가 사용 가능한지 확인
2. **가상환경**: Python 가상환경이 활성화되었는지 확인
3. **의존성 문제**: `pip install -r requirements.txt` 재실행
4. **데이터베이스 초기화**: `mentor_mentee.db` 파일 삭제 후 재시작

---

## 🏆 천하제일 입코딩 대회 2025 출품작

**개발자**: 최재훈  
**개발 시간**: 3시간  
**기술 스택**: Python Flask + Vanilla JavaScript  
**특징**: 완전한 멘토-멘티 매칭 시스템, 한국어 UI, 데모 계정 제공
