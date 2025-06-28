# 천하제일 입코딩 대회 2025 제출 정보

## 📋 제출 양식

### 앱 제출자 정보
- **제목**: 앱 제출
- **참가자 이름**: 최재훈
- **GitHub 프로필 URL**: https://github.com/jaehunchoe
- **GitHub 리포지토리 URL**: [GitHub 업로드 후 입력]
- **스크린샷 URL**: [스크린샷 업로드 후 입력]
- **소개 동영상 URL**: [동영상 업로드 후 입력]

### 프론트엔드 앱 정보
- **프론트엔드 앱 기본 URL**: http://localhost:3000
- **프론트엔드 앱 경로**: ./frontend
- **프론트엔드 앱 실행 명령어**: 
  ```bash
  chmod +x start-frontend.sh && ./start-frontend.sh &
  ```

### 백엔드 앱 정보
- **백엔드 앱 기본 URL**: http://localhost:8080/api
- **백엔드 앱 경로**: ./backend
- **백엔드 앱 실행 명령어**: 
  ```bash
  chmod +x start-backend.sh && ./start-backend.sh &
  ```
- **Swagger UI URL**: http://localhost:8080/swagger-ui
- **OpenAPI 문서 URL**: http://localhost:8080/api/openapi.json

## 🚀 앱 특징

### 구현된 핵심 기능
✅ JWT 기반 회원가입/로그인 (RFC 7519 클레임 준수)
✅ 역할별 프로필 관리 (멘토/멘티)
✅ 멘토 검색/필터링/정렬
✅ 매칭 요청 시스템 (요청/수락/거절)
✅ 이미지 업로드 (1MB 제한, jpg/png 지원)
✅ OpenAPI 3.0 문서화 + Swagger UI
✅ SQLite 데이터베이스 자동 초기화
✅ 데모 계정 자동 생성
✅ 한국어 UI/UX
✅ 반응형 웹 디자인

### 보안 기능
✅ SQL 인젝션 방지
✅ XSS 공격 방지
✅ JWT 토큰 1시간 유효기간
✅ 입력 값 검증 및 필터링
✅ 이미지 업로드 검증

### 데모 계정
**멘토**: mentor1@test.com ~ mentor5@test.com / password123
**멘티**: mentee1@test.com ~ mentee5@test.com / password123

## 📱 주요 화면

1. **메인 화면**: 로그인 방식 선택 (메뉴얼/아이콘)
2. **회원가입**: 이메일, 비밀번호, 역할 선택
3. **로그인**: 이메일/비밀번호 또는 아이콘 클릭
4. **대시보드**: 프로필 관리, 멘토 찾기, 매칭 관리
5. **프로필 관리**: 이름, 자기소개, 이미지, 기술스택
6. **멘토 찾기**: 검색, 정렬, 매칭 요청
7. **매칭 관리**: 요청 목록, 상태 확인, 수락/거절

## 🛠 기술 스택

**백엔드**: Python Flask + SQLAlchemy + SQLite + JWT + Swagger
**프론트엔드**: Vanilla JavaScript + HTML5 + CSS3
**특징**: 순수 웹 기술, 외부 라이브러리 최소화, 빠른 실행

---

**개발 시간**: 3시간
**최종 제출일**: 2025년 6월 28일
