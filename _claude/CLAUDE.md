# 백엔드 행동 지침 (보조)

> **메인 규칙:** [`sangho/.cursorrules`](.cursorrules)를 먼저 Read한다.  
> 본 문서는 Karpathy 원칙의 **백엔드 적용 보조**다. 충돌 시 `.cursorrules`가 우선한다.  
**스택:** FastAPI · SQLAlchemy(async) · PostgreSQL · `main.py`

---

## 1. 구현 전 사고 — 백엔드 적용

- API prefix·라우터 마운트·프론트(`www`) URL 일치 → `main.py`, `adapter/inbound/api/__init__.py` Read
- 새 엔드포인트 → 가장 가까운 `*_router` · `*_interactor` · `*_pg_repository` · `*_provider` 세트 복제
- [`sangho/_claude/ENTITY_RULE.md`](ENTITY_RULE.md) · 앱 `_docs/` ERD 선행
- 앱 작업 시 → [`apps/titanic/_docs/.cursorrules`](apps/titanic/_docs/.cursorrules) 등 **앱 `.cursorrules` 먼저**

---

## 2. 단순성 · 3. 정밀한 수정 · 4. 목표 중심 실행

상세는 [루트 `.cursorrules`](../.cursorrules) §2–4 및 본 문서 메인인 [`sangho/.cursorrules`](.cursorrules) §4–5(실행·검증)를 따른다.

| 작업 | 검증 |
|------|------|
| 엔드포인트 추가 | curl → 기대 HTTP·JSON |
| 404 수정 | 프론트 URL = 백엔드 prefix |
| Docker | `docker compose up --build -d backend` 후 curl |

---

## 앱별 메인 규칙

| 앱 | `.cursorrules` (메인) |
|----|----------------------|
| Titanic | [`apps/titanic/_docs/.cursorrules`](apps/titanic/_docs/.cursorrules) |
| Kayfabe | `apps/kayfabe/_docs/.cursorrules` (추가 예정) |
| Friday13th | `apps/friday13th/_docs/.cursorrules` (추가 예정) |
