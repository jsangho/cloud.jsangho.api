# Specification — Multi-Agent System Test Harness

## 1. 시스템 개요 및 아키텍처

본 시스템은 허브 앤 스포크(Hub-and-Spoke) 및 온톨로지 기반의 비즈니스 ERP 멀티 에이전트 아키텍처이다.

```
외부 채널 (Gmail / Telegram / Discord)
           │
           ▼
┌─────────────────────────────────────────────┐
│  manager/  (커뮤니케이션 스포크)              │
│                                             │
│  ┌── inbound ──────────────────────────┐   │
│  │ telegram_router  (Lestrade 경찰)     │   │
│  │ discord_router   (Anderson 경찰)     │   │
│  │ received_router  ◀── Watson 게이트   │   │
│  └─────────────────────────────────────┘   │
│                                             │
│  ┌── app/use_cases ────────────────────┐   │
│  │ received_interactor  ← Holmes 처리  │   │
│  └─────────────────────────────────────┘   │
└────────────────┬────────────────────────────┘
                 │ 에스컬레이션 (Case B)
                 ▼
┌─────────────────────────────────────────────┐
│  ontology/  (온톨로지 허브 — ontology)      │
│  spam_classifier_interactor                 │
│  → 향후: 전사 컨텍스트 라우터               │
└────────────────┬────────────────────────────┘
                 │ 격상 (VIP / 보고서 요청)
                 ▼
┌─────────────────────────────────────────────┐
│  core/lol/t1_mid_faker_orchestrator.py       │
│  (Faker / EXAONE — 최고 사령탑, 미구현)      │
└─────────────────────────────────────────────┘
```

### 명칭 매핑표 (설계 명칭 → 실제 경로)

| 설계 명칭 | 실제 경로 | 상태 |
|-----------|-----------|------|
| Hub/Brain: `t1_mid_faker_orchestrator` | `core/lol/t1_mid_faker_orchestrator.py` | 미구현 |
| Ontology Bus: `ontology/` | `ontology/` (API prefix: `/star-craft`) | 개발 중 |
| Comm Spoke: `sherlock_homes/` | `manager/` | 운영 |
| Watson (Watcher Hub) | `manager/adapter/inbound/api/v1/received_router.py` | 운영 |
| Lestrade 경찰 (Telegram) | `manager/adapter/inbound/api/v1/telegram_router.py` | 운영 |
| Anderson 경찰 (Discord) | `manager/adapter/inbound/api/v1/discord_router.py` | 운영 |
| Holmes (자체 처리) | `manager/app/use_cases/received_interactor.py` | 운영 |
| 1차 분류기 | `ontology/app/use_cases/spam_classifier_interactor.py` | 운영 |

---

## 2. 에이전트 라우팅 기준

외부 채널에서 인입되는 이벤트는 중요도 및 의도(Intent)에 따라 두 가지로 라우팅된다.

- **Case A — 일반 업무**: 중요 거래처가 아니거나 단순 문의
  → `manager/app/use_cases/received_interactor.py` (Holmes)가 자체 처리 및 종결.
  → Telegram 알림 발송 후 DB 저장.

- **Case B — 에스컬레이션**: VIP 거래처이거나 보고서 자동 생성 요청
  → `ontology/` 허브를 경유하여 `t1_mid_faker_orchestrator` (Faker/EXAONE)에게 격상.
  → Faker가 전사 ERP 데이터를 취합하여 최종 보고서 생성 후 하향 전달.

---

## 3. Watson (Watcher Hub) 역할 정의

`manager/adapter/inbound/api/v1/received_router.py`의 `POST /inbox/receive`가 Watson의 현재 구현체이다.
Watson은 단순 저장소가 아닌 **Triage Nurse(초진 분류 관문)** 역할을 수행한다.

### Watson의 핵심 메커니즘

1. **감시 및 후킹 (Watch & Hook)**
   - `telegram_router`, `discord_router`, Gmail Push(`received_router`) 등 인바운드 라우터들로부터 이벤트를 수신.
   - 현재 Gmail Push → n8n → `POST /api/manager/inbox/receive` 경로로 인입.

2. **1차 분류 및 조율 (Triage)**
   - 발신자(`from_email`) 기반 VIP 거래처 여부 판단.
   - 본문(`body`) 기반 보고서 요청 의도 감지.
   - 현재 구현: `ontology/app/use_cases/spam_classifier_interactor.py`로 스팸 여부만 판단.
   - 향후 구현: VIP 매핑 테이블 + 의도 분류기 추가 필요.

3. **컨텍스트 스위칭 및 라우팅 (Routing Decision)**
   - Case A → `received_interactor.receive()` 직접 호출.
   - Case B → `ontology` 허브로 이벤트 발행(Publish) → Faker wake-up.

---

## 4. Test Harness 구현 명세

### 4-1. 가상 이벤트 생성기 (Mock Event Generator)

`telegram_router`, `discord_router`, `received_router` 등이 외부 채널에서 이벤트를 수신하는 상황을 모사한다.

**테스트 시나리오 (최소 2가지):**

```python
# Scenario 1 — 일반 거래처, 단순 문의 (Case A → Holmes 처리)
SCENARIO_NORMAL = {
    "from_email": "general@example.com",
    "from_name": "일반 거래처",
    "to_email": "leicestercity12968@gmail.com",
    "subject": "안녕하세요, 제품 문의드립니다",
    "body": "귀사 제품에 관심이 있어 문의드립니다.",
    "message_id": "mock-normal-001",
    "important_client": False,
}

# Scenario 2 — VIP 거래처, 보고서 자동 생성 요청 (Case B → Faker 에스컬레이션)
SCENARIO_VIP = {
    "from_email": "ceo@bigcorp.com",
    "from_name": "VIP 거래처 대표",
    "to_email": "leicestercity12968@gmail.com",
    "subject": "[긴급] 2분기 실적 자동 보고서 발행 요망",
    "body": "2분기 전사 실적 요약 보고서를 오늘 중으로 자동 생성하여 전달 바랍니다.",
    "message_id": "mock-vip-002",
    "important_client": True,
}
```

**실제 인바운드 경로:**

| 채널 | 현재 인입 경로 |
|------|----------------|
| Gmail | Gmail Push → Pub/Sub → n8n → `POST /api/manager/inbox/receive` |
| Telegram | `POST /api/manager/telegram/send` (아웃바운드만 구현, 인바운드 미구현) |
| Discord | `POST /api/manager/discord/send` (아웃바운드만 구현, 인바운드 미구현) |

### 4-2. Watson 라우팅 인터셉터

`manager/adapter/inbound/api/v1/received_router.py`의 `receive()` 핸들러 내부에 분류 로직을 추가한다.

```
POST /api/manager/inbox/receive
    │
    ├─ Watson.triage(from_email, subject, body)
    │       │
    │       ├─ [Case A] is_important_client=False, no_report_intent
    │       │       └─ ReceivedInteractor.receive(cmd)   ← Holmes
    │       │              → DB 저장 + Telegram 알림
    │       │
    │       └─ [Case B] is_important_client=True OR report_intent 감지
    │               └─ OntologyBus.publish(event)        ← ontology 경유
    │                      └─ FakerOrchestrator.wake_up() ← Faker
```

**Holmes 호출 트리거 (현재 구현체):**
- `manager/app/use_cases/received_interactor.py:ReceivedInteractor.receive()`
- DB 저장 → `_telegram_notify()` → 종결

**Faker 에스컬레이션 트리거 (미구현, 향후):**
- `ontology/` 허브의 이벤트 버스(`ontology` 프로토콜)로 `EscalationEvent` 발행
- `core/lol/t1_mid_faker_orchestrator.py` 활성화(Wake-up)
- MCP Notification 또는 내부 큐(Redis) 경유

### 4-3. 하네스 대시보드 — Narrative Log

이벤트 인입부터 최종 처리 완료까지 전체 저니를 콘솔에 출력한다.

```
[WATSON] 이벤트 인입 ─────────────────────────────────────
  채널    : Gmail Push (Pub/Sub → n8n → /inbox/receive)
  발신자  : general@example.com (일반 거래처)
  제목    : 안녕하세요, 제품 문의드립니다
  message_id: mock-normal-001

[WATSON → TRIAGE] 1차 분류 중...
  VIP 거래처 : ✗
  보고서 요청 : ✗
  스팸 여부   : ham (confidence: 1.0)
  판정       : Case A → Holmes 위임

[HOLMES] 처리 시작
  → DB 저장 완료 (id: 9)
  → Telegram 알림 발송: "📬 새 메일 도착 / 발신자: general@example.com"
[HOLMES] 처리 완료 ✓
─────────────────────────────────────────────────────────
총 소요 시간: 0.23s

[WATSON] 이벤트 인입 ─────────────────────────────────────
  채널    : Gmail Push
  발신자  : ceo@bigcorp.com (VIP 거래처 대표)
  제목    : [긴급] 2분기 실적 자동 보고서 발행 요망
  message_id: mock-vip-002

[WATSON → TRIAGE] 1차 분류 중...
  VIP 거래처 : ✓
  보고서 요청 : ✓ ("보고서", "자동 생성" 키워드 감지)
  판정       : Case B → 에스컬레이션

[WATSON → ONTOLOGY] 온톨로지 버스로 이벤트 발행
  Topic: ontology.escalation.report_request
  Payload: { from_email, subject, message_id, priority: "CRITICAL" }

[FAKER] Wake-up 수신 ────────────────────────────────────
  오케스트레이터: t1_mid_faker_orchestrator (EXAONE)
  → 전사 ERP 데이터 취합 중... (kayfabe, human_resource, ...)
  → 보고서 생성 완료
  → 하향 전달: ceo@bigcorp.com
[FAKER] 처리 완료 ✓
─────────────────────────────────────────────────────────
총 소요 시간: 4.71s
```

---

## 5. 구현 단계별 현황

| 단계 | 구성 요소 | 현황 |
|------|-----------|------|
| ✅ | Gmail Push → Watson 인입 경로 | 완료 (`received_router.py`) |
| ✅ | Telegram/Discord 아웃바운드 | 완료 |
| ✅ | Holmes (DB 저장 + Telegram 알림) | 완료 (`received_interactor.py`) |
| ✅ | 스팸 1차 분류 | 완료 (`spam_classifier_interactor.py`) |
| 🔧 | Watson Triage (VIP 판정 + 의도 감지) | 미구현 |
| 🔧 | Telegram/Discord 인바운드 감시 | 미구현 |
| 🔧 | ontology 이벤트 버스 (에스컬레이션 발행) | 미구현 |
| 🔧 | Faker Orchestrator (EXAONE wake-up) | 미구현 |
| 🔧 | Narrative Log 미들웨어 | 미구현 |

---

## 6. 다음 구현 우선순위

1. **Watson Triage 로직** — `received_router.py`에 VIP 판정 + 보고서 의도 분류 추가
2. **Telegram/Discord 인바운드** — 경찰 레이어 완성 (현재 아웃바운드만)
3. **ontology 이벤트 버스** — `ontology/` 허브에 `EscalationEvent` 발행 포트 추가
4. **Faker Orchestrator** — `core/lol/t1_mid_faker_orchestrator.py` 스텁(stub) 구현
5. **Narrative Log** — 저니 추적 미들웨어 (FastAPI middleware 또는 logging hook)
