# 구현 계획서: 오늘의 할 일 웹 앱

**브랜치**: `001-오늘의-할-일` | **작성일**: 2026-07-15 | **명세서**: [spec.md](spec.md)

**입력**: [spec.md](spec.md) 기반의 사용자 요구사항

## 요약

이 기능은 FastAPI 기반의 단일 페이지 할 일 관리 웹 앱을 구현한다. 사용자는 할 일을 생성, 완료 토글, 삭제할 수 있고, 남은 개수와 필터 조건에 따라 목록을 실시간으로 갱신할 수 있다. 데이터는 SQLite를 사용해 영속화하며, 프런트엔드는 단일 HTML 템플릿과 바닐라 JavaScript로 구성한다.

## 기술 컨텍스트

**언어/버전**: Python 3.11+

**주요 의존성**: FastAPI, SQLAlchemy 2.x, Pydantic, pytest, FastAPI TestClient, Jinja2

**저장소**: SQLite. 데이터베이스 파일 경로는 .env의 DATABASE_URL 환경변수로 관리한다.

**테스트**: pytest + FastAPI TestClient

**대상 플랫폼**: 웹 브라우저 기반 애플리케이션

**프로젝트 유형**: 웹 애플리케이션

**성능 목표**: 단일 사용자 기준으로 즉시 응답되는 할 일 CRUD 작업

**제약 조건**: 별도 빌드 도구 없이 실행 가능해야 하며, 모바일 화면에서도 사용 가능해야 한다.

**규모/범위**: 단일 사용자, 단일 페이지, CRUD 중심 기능

## Constitution Check

- [x] 스펙 우선 원칙을 준수한다. 구현 전 명세서가 존재한다.
- [x] 테스트 필수 원칙을 준수한다. 핵심 API 동작은 pytest로 검증한다.
- [x] 설정 분리 원칙을 준수한다. DB 경로는 .env로 관리한다.
- [x] 추적 가능한 커밋 원칙을 준수한다. 작업별 태스크 ID를 커밋 메시지에 포함한다.
- [x] 단순성 원칙을 준수한다. 불필요한 라이브러리 추가 없이 요구사항 범위만 구현한다.

## 프로젝트 구조

### 문서 구조

```text
specs/001-오늘의-할-일/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### 소스 코드 구조

```text
app/
├── main.py
├── models.py
├── schemas.py
├── crud.py
├── database.py
└── templates/
    └── index.html

tests/
└── test_api.py
```

**구조 결정**: 단일 FastAPI 애플리케이션 구조를 채택한다. 라우터와 API 진입점은 app/main.py에 두고, ORM 모델은 app/models.py, Pydantic 스키마는 app/schemas.py, DB 로직은 app/crud.py, 세션 설정은 app/database.py에 배치한다. 프런트엔드는 app/templates/index.html에 포함하고, 테스트는 tests/test_api.py에서 수행한다.

## 복잡도 추적

없음.
