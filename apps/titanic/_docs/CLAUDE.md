# Titanic 앱 행동 지침 (메인)

> **본 문서가 메인 규칙이다.** 충돌 시 `CLAUDE.md`가 우선한다.  
> [`.cursorrules`](.cursorrules)는 보조 참고용이다.

상위 메인: [sangho `CLAUDE.md`](../../../_claude/CLAUDE.md) · [루트 `CLAUDE.md`](../../../../CLAUDE.md)

**패키지:** `titanic` · **API prefix:** `/titanic`

---

## 1–4. 행동 원칙 — Titanic 맥락 (요약)

- **구현 전:** 가장 가까운 `crew_*` / `passenger_*` 세트 Read · prefix·프론트 URL 확인
- **단순성:** 레이어 풀세트만 추가 · [`.cursorrules`](.cursorrules)(보조) §2 네이밍 준수
- **정밀 수정:** 요청한 캐릭터만 · `main.py`에 Titanic 로직 넣지 않음
- **목표 중심:** 본 문서 §1–4 체크리스트 + curl `/titanic/...` + (해당 시) www Network 200

```text
1. router 등록 → /docs 경로 노출
2. interactor·repo → curl 200
3. www 연동 → 브라우저 Network 200
```

---

## 형제 앱 (메인 규칙 위치)

| 앱 | `.cursorrules` |
|----|----------------|
| **titanic** | 본 파일과 같은 폴더 |
| kayfabe | `kayfabe/_docs/.cursorrules` (추가 예정) |
| friday13th | `friday13th/_docs/.cursorrules` (추가 예정) |
