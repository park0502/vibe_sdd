# 작업 목록: 오늘의 할 일 웹 앱

**입력**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/todo-api.json](contracts/todo-api.json)

**구성 방식**: 사용자 스토리 우선순위(P1 → P2)에 따라 정렬하며, 화면(UI)은 API 구현이 완료된 뒤 진행한다.

## Phase 1: 공통 설정

**목적**: 기본 프로젝트 구조와 공통 환경을 준비한다.

- [ ] T001 공통 프로젝트 디렉터리 구조를 생성한다. 완료 조건: [app/main.py](app/main.py), [app/models.py](app/models.py), [app/schemas.py](app/schemas.py), [app/crud.py](app/crud.py), [app/database.py](app/database.py), [app/templates/index.html](app/templates/index.html), [tests/test_api.py](tests/test_api.py) 경로가 존재한다.
- [ ] T002 FastAPI, SQLAlchemy, Pydantic, pytest, TestClient, Jinja2가 설치되도록 환경을 구성한다. 완료 조건: `pytest --version`과 Python import 확인이 가능하다.
- [ ] T003 [P] 환경 변수 관리용 `.env` 및 `.env.example` 템플릿을 추가한다. 완료 조건: `DATABASE_URL` 예시가 문서화되어 있고 `.env.example`에 값이 기록되어 있다.

---

## Phase 2: 기본 인프라

**목적**: 이후 사용자 스토리 구현의 기반이 되는 DB/라우팅/스키마를 구성한다.

- [ ] T004 SQLite 연결 설정과 세션 생명주기를 구현한다. 완료 조건: [app/database.py](app/database.py)에서 세션 생성과 DB 초기화가 가능하다.
- [ ] T005 ORM 모델과 기본 테이블 생성을 구현한다. 완료 조건: [app/models.py](app/models.py)에서 `Todo` 모델이 정의되고, `create_all`로 테이블이 생성된다.
- [ ] T006 Pydantic 스키마를 구현한다. 완료 조건: 생성/수정/응답 스키마가 [app/schemas.py](app/schemas.py)에 정의되고, 빈 제목이 422로 검증된다.
- [ ] T007 [P] FastAPI 앱 진입점과 헬스 체크 엔드포인트를 구현한다. 완료 조건: `GET /health`가 200을 반환한다.

---

## Phase 3: 사용자 스토리 1 - 할 일 목록과 생성 기능 (우선순위 P1)

**목표**: 할 일을 조회하고 새로 생성할 수 있는 기본 API를 제공한다.

**독립 테스트**: 목록 조회와 생성 API가 정상 동작하면 이 스토리의 핵심 가치를 검증할 수 있다.

### 테스트

- [ ] T008 [P] [US1] 목록 조회 API 테스트를 작성한다. 완료 조건: `GET /api/todos`가 기본 응답을 반환하고, `status=active/completed/all`에 따라 필터링된 결과가 반환된다.
- [ ] T009 [P] [US1] 할 일 생성 API 테스트를 작성한다. 완료 조건: 정상 제목으로 생성 시 200/201 응답과 생성된 항목이 반환되고, 빈 제목은 422를 반환한다.

### 구현

- [ ] T010 [US1] 목록 조회 DB 로직을 구현한다. 완료 조건: [app/crud.py](app/crud.py)에서 `get_todos(status)`가 동작한다.
- [ ] T011 [US1] 할 일 생성 DB 로직을 구현한다. 완료 조건: [app/crud.py](app/crud.py)에서 새 할 일이 저장되고 ID가 부여된다.
- [ ] T012 [US1] `GET /api/todos` 엔드포인트를 구현한다. 완료 조건: `GET /api/todos?status=all|active|completed`가 기대한 필터 결과를 반환한다.
- [ ] T013 [US1] `POST /api/todos` 엔드포인트를 구현한다. 완료 조건: 유효한 제목으로 생성 시 저장되며, 빈 제목은 422로 응답한다.

---

## Phase 4: 사용자 스토리 2 - 완료 토글과 삭제 기능 (우선순위 P1)

**목표**: 할 일을 완료 상태로 전환하고 삭제할 수 있는 API를 제공한다.

**독립 테스트**: 완료 토글과 삭제 API가 정상 동작하면 이 스토리의 핵심 가치를 검증할 수 있다.

### 테스트

- [ ] T014 [P] [US2] 완료 토글 API 테스트를 작성한다. 완료 조건: `PATCH /api/todos/{id}`로 완료 상태가 토글되고, 없는 ID는 404를 반환한다.
- [ ] T015 [P] [US2] 삭제 API 테스트를 작성한다. 완료 조건: `DELETE /api/todos/{id}`가 정상 삭제 후 204를 반환하고, 없는 ID는 404를 반환한다.

### 구현

- [ ] T016 [US2] 완료 상태 변경 DB 로직을 구현한다. 완료 조건: [app/crud.py](app/crud.py)에서 `toggle_todo`가 완료/미완료 상태를 반전시킨다.
- [ ] T017 [US2] 할 일 삭제 DB 로직을 구현한다. 완료 조건: [app/crud.py](app/crud.py)에서 해당 항목이 제거된다.
- [ ] T018 [US2] `PATCH /api/todos/{id}` 엔드포인트를 구현한다. 완료 조건: 완료 상태가 성공적으로 변경된다.
- [ ] T019 [US2] `DELETE /api/todos/{id}` 엔드포인트를 구현한다. 완료 조건: 삭제 성공 시 204, 존재하지 않는 ID는 404를 반환한다.

---

## Phase 5: 사용자 스토리 3 - 남은 개수, 필터, UI (우선순위 P2)

**목표**: 화면에서 필터와 남은 개수를 반영해 목록을 갱신한다.

**독립 테스트**: 필터와 요약 정보가 정상적으로 반영되면 이 스토리의 핵심 가치를 검증할 수 있다.

### 테스트

- [ ] T020 [P] [US3] 필터/남은 개수 UI 동작 테스트를 작성한다. 완료 조건: 필터 변경 시 표시 목록이 바뀌고, 남은 개수가 올바르게 갱신된다.
- [ ] T021 [P] [US3] 빈 상태와 반응형 UI 동작 테스트를 작성한다. 완료 조건: 할 일이 없을 때 안내 문구가 표시되고, 360px 폭 레이아웃이 기본적으로 깨지지 않는다.

### 구현

- [ ] T022 [US3] 메인 화면 템플릿을 구현한다. 완료 조건: [app/templates/index.html](app/templates/index.html)에서 입력 폼, 목록, 필터, 남은 개수 영역이 렌더링된다.
- [ ] T023 [US3] 화면에서 fetch 기반 CRUD 동작을 구현한다. 완료 조건: 페이지 새로고침 없이 목록 로드, 생성, 완료 토글, 삭제가 동작한다.
- [ ] T024 [US3] 빈 상태와 반응형 스타일을 적용한다. 완료 조건: 할 일이 없을 때 안내 문구가 표시되고, 모바일 폭에서도 레이아웃이 자연스럽게 표시된다.

---

## Phase 6: 통합 및 마무리

**목적**: 전체 기능이 함께 동작하는지 검증하고 문서를 정리한다.

- [ ] T025 통합 테스트를 실행한다. 완료 조건: `pytest`가 전체 테스트를 통과한다.
- [ ] T026 [P] README 또는 운영 문서를 보강한다. 완료 조건: 실행 방법과 주요 API 경로가 문서화되어 있다.
