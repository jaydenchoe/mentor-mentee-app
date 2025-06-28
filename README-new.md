# 멘토-멘티 매칭 웹애플리케이션

전문 멘토와 멘티를 연결하는 웹 플랫폼입니다.

## 🚀 기능

- **사용자 인증**: JWT 기반 회원가입/로그인
- **프로필 관리**: 개인정보 및 프로필 이미지 업로드
- **멘토 검색**: 이름, 전문분야로 멘토 검색 및 정렬
- **매칭 시스템**: 멘토-멘티 매칭 요청/수락/거절
- **실시간 상태**: 매칭 요청 상태 실시간 조회
- **API 문서**: Swagger UI를 통한 API 문서 제공

## 🛠 기술 스택

### Backend
- **Python 3.8+**
- **Flask**: 웹 프레임워크
- **SQLAlchemy**: ORM
- **SQLite**: 데이터베이스
- **JWT**: 인증/인가
- **bcrypt**: 비밀번호 암호화
- **Pillow**: 이미지 처리
- **Swagger UI**: API 문서화

### Frontend
- **Vanilla JavaScript**: 순수 자바스크립트
- **HTML5/CSS3**: 모던 웹 표준
- **Python HTTP Server**: 정적 파일 서빙

## 📦 설치 및 실행

### 사전 요구사항
- Python 3.8 이상
- pip (Python 패키지 관리자)

### 1. 프로젝트 클론
```bash
git clone <repository-url>
cd mentor-mentee-app
```

### 2. 백엔드 설정 및 실행
```bash
cd backend

# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 가상환경 활성화 (Windows)
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
python app.py
```

백엔드 서버는 http://localhost:8080에서 실행됩니다.

### 3. 프론트엔드 실행
새 터미널 창에서:
```bash
cd frontend

# Python HTTP 서버로 실행
python3 -m http.server 3000
```

프론트엔드는 http://localhost:3000에서 실행됩니다.

### 4. 간편 실행 (VS Code)
VS Code에서 `Ctrl+Shift+P` → "Tasks: Run Task" → "Start All Services"를 선택하면 백엔드와 프론트엔드가 동시에 실행됩니다.

## 🌐 API 엔드포인트

### 인증
- `POST /api/auth/register` - 회원가입
- `POST /api/auth/login` - 로그인

### 사용자 프로필
- `GET /api/users/{id}/profile` - 프로필 조회
- `PUT /api/users/{id}/profile` - 프로필 수정
- `POST /api/users/{id}/profile/image` - 프로필 이미지 업로드

### 멘토
- `GET /api/mentors` - 멘토 목록 조회 (검색/정렬 지원)

### 매칭 요청
- `POST /api/match-requests` - 매칭 요청 생성
- `GET /api/match-requests/incoming` - 받은 요청 조회 (멘토용)
- `GET /api/match-requests/outgoing` - 보낸 요청 조회 (멘티용)
- `POST /api/match-requests/{id}/respond` - 요청 응답 (수락/거절)
- `DELETE /api/match-requests/{id}` - 요청 취소

## 📖 API 문서

Swagger UI: http://localhost:8080/swagger-ui

## ⚡ 핵심 특징

- **완성도**: 풀스택 웹애플리케이션 (백엔드 + 프론트엔드)
- **실용성**: 실제 사용 가능한 멘토-멘티 매칭 플랫폼
- **사용자 경험**: 직관적이고 반응형 UI/UX
- **빠른 개발**: 3시간 내 MVP 완성
- **확장성**: 모듈화된 코드 구조로 기능 추가 용이
- **호환성**: 다양한 환경에서 실행 가능

## 📁 프로젝트 구조

```
mentor-mentee-app/
├── backend/
│   ├── app.py              # Flask 애플리케이션
│   ├── requirements.txt    # Python 의존성
│   ├── uploads/           # 업로드된 이미지
│   ├── venv/              # 가상환경
│   └── start-backend.sh   # 백엔드 실행 스크립트
├── frontend/
│   ├── index.html         # 메인 HTML
│   ├── styles.css         # 스타일시트
│   ├── app.js            # JavaScript 로직
│   ├── package.json      # 프론트엔드 설정
│   └── start-frontend.sh # 프론트엔드 실행 스크립트
├── .vscode/
│   └── tasks.json        # VS Code 작업 설정
└── README.md
```

## 🧪 테스트

1. **회원가입**: 멘토 또는 멘티로 계정 생성
2. **로그인**: 생성한 계정으로 로그인
3. **프로필 설정**: 이름, 자기소개, 전문분야 입력
4. **이미지 업로드**: 프로필 이미지 업로드
5. **멘토 검색**: 멘토 목록에서 원하는 멘토 검색
6. **매칭 요청**: 멘토에게 매칭 요청 전송
7. **요청 관리**: 받은/보낸 매칭 요청 확인 및 응답

## 🔧 개발 환경

- **OS**: macOS, Linux, Windows
- **Python**: 3.8+
- **브라우저**: Chrome, Firefox, Safari, Edge (최신 버전)

## 📈 향후 개선사항

- [ ] 실시간 채팅 기능
- [ ] 이메일 알림
- [ ] 평가 시스템
- [ ] 고급 검색 필터
- [ ] 모바일 앱 지원
- [ ] 소셜 로그인
- [ ] 멘토링 세션 예약

## 👥 기여

프로젝트에 기여하고 싶으시다면:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 🆘 문제 해결

### 일반적인 문제들

1. **포트 충돌**: 8080 또는 3000 포트가 사용 중인 경우 다른 포트 사용
2. **Python 버전**: Python 3.8 이상 필요
3. **가상환경**: 의존성 충돌 방지를 위해 가상환경 사용 권장
4. **CORS 오류**: 백엔드와 프론트엔드가 다른 포트에서 실행되므로 CORS 설정 확인

### 지원

문제가 발생하면 GitHub Issues에 문의하거나 개발팀에 연락하세요.
