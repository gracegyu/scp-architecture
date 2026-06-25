# VT API Gateway — Claude Code 작업 가이드

> **대상**: Claude Code(개발 표준 AI 에이전트)가 VT API Gateway 스펙·설계 작업을 **이어서** 수행할 때 읽는 핸드오프 문서.
>
> **실행 컨텍스트**: **`scp-architecture/docs/VT_API_Gateway/`** 를 작업 루트로 둔다.
>
> **갱신**: 2026-06-25 · 참조 경로를 [참조 카탈로그](<참조-카탈로그.md>)로 일원화 · 주요 결정 현행화(ADR-11·GW presigned 비발급·webhook provider 호스트·AWS 전용·디바이스=EzServer). **기술 세부 정본은 항상 SRS** — 본 가이드는 요약·핸드오프.

---

## 1. 이 문서를 먼저 읽는 이유

VT API Gateway는 **문서가 두 체계**로 나뉜다.

| 체계 | 역할 | 어디에 두는가 |
| --- | --- | --- |
| **Scott 통제 문서** | IEC 62304 / ISO 13485 감사용 — PRD·ARD·요구사항 명세 등 | VKS(Confluence) + `08.VT_API_Gateway/` (워크스페이스 하위) |
| **SSOT (요구공학)** | 분석·설계·변경의 **단일 정본** — SRS·One Pager·Sub-SRS | `08.VT_API_Gateway/specs/` → baseline 후 Azure git |
| **입력 참고** | CSV·AXS 스냅샷·회의록 — SSOT 작성 시 읽기만 | `references/` |
| **작성 틀** | SRS·One Pager 항목 구조 | `templates/` |

AI는 **SSOT를 수정**하고, Scott 문서는 **추출·참조**만 한다. 같은 내용을 두 곳에 각각 쓰지 않는다.

---

## 2. Multi-root 워크스페이스 · 레포

Claude Code / VS Code는 `~/Documents/Azure/scp.code-workspace`로 여러 레포를 동시에 연다. **워크스페이스 폴더↔로컬 경로·레포 카탈로그(용도·clone 상태)는 [참조 카탈로그 §1·§2](<참조-카탈로그.md>)** 가 단일 정본이다(여기서 중복 표기하지 않는다).

---

## 3. 현재 진행 상태 (2026-06-25)

### 3.1 Case D — 통합 실행 범위

PRD §12.1 기준 **케이스 D**: ③ SRS + ③-C Sub-SRS + ④ Sub-SRS + design 산출물을 **통합 진행**한다.

| 스펙 | 로컬 초안 | 상태 | 공식 등록처 |
| --- | --- | --- | --- |
| **③ GW SRS** | `08.VT_API_Gateway/specs/03-srs-gateway/SRS.md` | **작성 중**(§1~§7·baseline 전) — ADR-11·presigned 중계·webhook·AWS 정합 반영 | `vt-api-gateway/docs/specs/SRS.md` |
| **design OpenAPI** | `08.VT_API_Gateway/specs/03-srs-gateway/design/openapi/` | 초안 — presigned 중계(②③)·라우팅(ADR-11)·webhook provider 호스트 반영 | `vt-api-gateway/docs/specs/design/openapi/` |
| **design DBML** | `08.VT_API_Gateway/specs/03-srs-gateway/design/dbml/` | 초안 — 분배 레지스트리·region_catalog 포함 | `vt-api-gateway/docs/specs/design/dbml/` |
| **design well-known** | `08.VT_API_Gateway/specs/03-srs-gateway/design/well-known/` | sample JSON + README | (③ SRS §7.7.2) |
| **③-C Console Sub-SRS** | `08.VT_API_Gateway/specs/03c-subsrs-gw-console/` | 미작성 | `vt-api-gateway-console` 또는 gateway `docs/` |
| **④ AXS Sub-SRS** | `08.VT_API_Gateway/specs/04-subsrs-straumann-axs/` | 미작성 (③ baseline 후) | `vt-api-gateway/docs/specs/04-subsrs-straumann-axs/` |
| **① API 호환 One Pager** | `08.VT_API_Gateway/specs/01-onepager-api-compatibility/` | 미작성 | VKS Confluence |
| **② Presigned One Pager** | `08.VT_API_Gateway/specs/02-onepager-presigned-url/` | 미작성 | VKS Confluence |

### 3.2 Azure 이관

- `vt-api-gateway`에 placeholder 구조·브랜치 `docs/specs-initial-structure` PR이 **리뷰 대기**일 수 있음.
- **규칙**: 초안 완료(baseline 직전) → Azure로 **PR 이관** → `scp-architecture` 쪽은 **URL 포인터로 교체**(복제·symlink 금지). 상세: [`08.VT_API_Gateway/specs/README.md`](08.VT_API_Gateway/specs/README.md).

### 3.3 최근 확정 (2026-06, 정본=SRS Appendix A·B·변경이력)

이번 주 회의·리뷰로 확정된 핵심(상세·근거는 SRS):

- **라우팅 ADR-11(CCB 승인 2026-06-25)** — `Vatech-Target` 유무로 GW 고유 API vs 프록시(verbatim bypass), upstream=레지스트리 1행.
- **업로드 = GW presigned 비발급·중계만** — 발급=CleverSpace(②)/AXS(③). `/v1/uploads`·리전 Signer·Upload Session 폐기.
- **Webhook 유연 수신 + provider별 전용 호스트**(`{provider}.webhook.gw.vatech.com`)로 발신자 식별(Host/SNI), 식별≠인증(HMAC). 클라우드 수신=CleverLab만(CleverSpace 대상 아님).
- **GW = AWS 전용 배포**(AWS 미지원국도 가까운 AWS GW 접속·storage=Provider MinIO 중계). 스택: EKS·Aurora PostgreSQL(권장)·ElastiCache·SQS(A 내부 큐)·MQTT(B 엣지·IoT Core/Amazon MQ).
- **디바이스 = EzServer**(GW 관점) — 물리 영상장비는 EzServer 뒤·GW 비대상. 클리닉 등록=EzServer가 LMP Clinic-ID 수신 시 자동·무조건.
- **Console 사용자 = Admin + C/S**(C/S=등록 확인) — 세부는 ③-C Sub-SRS.

---

## 4. 디렉터리·파일 맵 (워크스페이스)

```
docs/VT_API_Gateway/                         ← Claude Code 실행 루트
├── README.md
├── VT API Gateway — Claude Code 작업 가이드.md   ← 본 문서
│
├── 08.VT_API_Gateway/                       ← Scott 통제 + SSOT
│   ├── 08.VT_API_Gateway.md
│   ├── README.md                            # VKS·Azure URL 매핑
│   ├── VT API Gateway — PRD (v2).md
│   ├── VT API Gateway — ARD (아키텍처).md
│   ├── specs/03-srs-gateway/SRS.md          # ★ 메인 SSOT
│   └── …
│
├── references/                              ← 입력 자료 (SSOT 아님)
│   ├── CleverAPI호환성체크/
│   └── Straumann연동/AXS_docs/openapi/
│
└── templates/
    ├── SRS_v3.3_template.md
    └── OnePager_v1.0_template.md
```

> `references/`(입력 자료)·`templates/`(작성 틀)의 상세 경로·상태는 [참조 카탈로그 §3](<참조-카탈로그.md>) 참조.

---

## 5. 읽기 순서 (우선순위)

새 세션에서 맥락을 잡을 때 아래 순서를 권장한다.

1. **본 문서** + [`README.md`](README.md) — 워크스페이스 인덱스
2. [`08.VT_API_Gateway/specs/README.md`](08.VT_API_Gateway/specs/README.md) — SSOT·이관 규칙
3. [`08.VT_API_Gateway/specs/03-srs-gateway/_status.md`](08.VT_API_Gateway/specs/03-srs-gateway/_status.md)
4. [`08.VT_API_Gateway/specs/03-srs-gateway/SRS.md`](08.VT_API_Gateway/specs/03-srs-gateway/SRS.md) — **작업 정본**
5. [`08.VT_API_Gateway/VT API Gateway — PRD (v2).md`](08.VT_API_Gateway/VT%20API%20Gateway%20—%20PRD%20(v2).md) §12.1
6. [`08.VT_API_Gateway/VT API Gateway — ARD (아키텍처).md`](08.VT_API_Gateway/VT%20API%20Gateway%20—%20ARD%20(아키텍처).md)
7. [`08.VT_API_Gateway/README.md`](08.VT_API_Gateway/README.md) — VKS·Azure URL (공유 문서는 URL만)
8. [`08.VT_API_Gateway/specs/03-srs-gateway/design/`](08.VT_API_Gateway/specs/03-srs-gateway/design/)
9. [`references/`](references/README.md) · [`templates/`](templates/README.md) — 입력·틀

**④ AXS Sub-SRS 작성 시 추가:**

- [`references/Straumann연동/AXS_docs/`](references/Straumann연동/AXS_docs/)
- `vt-api-gateway/docs/specs/references/axs-openapi/` (Azure placeholder)
- [AXS Developer Portal](https://developer.axs.straumann.com/api)

---

## 6. Repository · 공식 URL

- **레포 카탈로그**(Azure/SVN·로컬 경로·clone 상태): [참조 카탈로그 §2](<참조-카탈로그.md>).
- **통제·공유 문서 정본 URL**(VKS pageId·Azure SRS 경로 — SRS §1.5용): [`08.VT_API_Gateway/README.md`](08.VT_API_Gateway/README.md) 문서 URL 매핑.

**vt-api-gateway 레포 내 스펙 경로(공식 SSOT):**

```
vt-api-gateway/
├── CLAUDE.md                 # ESIP Jira·브랜치·버전 규칙
└── docs/specs/
    ├── README.md · SRS.md
    ├── 03c-subsrs-gw-console/Sub-SRS.md · 04-subsrs-straumann-axs/Sub-SRS.md
    ├── design/openapi/vt-api-gateway.openapi.yaml · design/dbml/vt-api-gateway.dbml
    └── references/axs-openapi/
```

### 6.1 Jira (VTS)

| 항목 | URL |
| --- | --- |
| ESIP 보드 | https://vts.vatech.com/secure/RapidBoard.jspa?rapidView=373 |
| Epic v1.0 | https://vts.vatech.com/browse/ESIP-2 |
| Project | **ESIP** · Component: **platform/api-gateway** · 버전 `gw/<Major>.<Minor>.<Patch>.<Build>` |

Jira 작업: es-toolkit **`/es-ticket`**(브랜치·티켓 자동). vt-api-gateway `CLAUDE.md` 참조.

---

## 7. AI 방법론 — `munto-dev-assistant`

문토 제품용 하네스이지만, **스펙 작성·리뷰·dev-chain 프로세스**는 VT GW에 그대로 적용한다.

**레포**: `~/Documents/GitMunto/munto-dev-assistant`

### 7.1 먼저 읽을 문서

| 파일 | 내용 |
| --- | --- |
| [`AGENTS.md`](../../../../GitMunto/munto-dev-assistant/AGENTS.md) | 하네스 진입점 · dev-chain 순서 · 절대 금지 |
| [`document/dev-process-guide.md`](../../../../GitMunto/munto-dev-assistant/document/dev-process-guide.md) | PHASE 0~3 실무 교과서 |
| [`document/spec-standard.md`](../../../../GitMunto/munto-dev-assistant/document/spec-standard.md) | SRS·One Pager **항목 구조 고정** |
| [`document/spec-writing-tips.md`](../../../../GitMunto/munto-dev-assistant/document/spec-writing-tips.md) | TBD / N/A / Will Not Do |
| [`document/ip-standard.md`](../../../../GitMunto/munto-dev-assistant/document/ip-standard.md) | 구현계획서(IP) — PHASE 1 이후 |

> **워크스페이스에서 열었을 때**: `munto-dev-assistant/AGENTS.md` 등 **폴더명 기준**으로 접근하면 된다.

### 7.2 dev-chain PHASE (VT GW 적용)

```
PHASE 0   Spec 작성     → SRS / One Pager (현재: ③ SRS 작성 중)
PHASE 0.5 WBS (선택)    → dev-chain-wbs
PHASE 1   상위설계      → dev-chain-design → DBML + Swagger + Unit TCL → IP
PHASE 2   구현          → dev-chain-backend (NestJS) — vt-api-gateway
PHASE 3   검증          → dev-chain-verify
```

**지금 단계**: PHASE 0 (③ SRS 마무리) → 곧 PHASE 1 (design baseline · Unit TCL · IP).

### 7.3 스킬 경로 (`.agents/skills/` = 정본)

Claude Code는 `.claude/skills/*/SKILL.md` 래퍼를 읽으면 **`.agents/` 원본**을 따라간다.

| 작업 | 스킬 | 원본 경로 |
| --- | --- | --- |
| SRS 작성 | `munto-spec-writer` | `.agents/skills/common/docs/munto-spec-writer/SKILL.md` |
| SRS 리뷰 | `munto-spec-review` | `.agents/skills/common/docs/munto-spec-review/SKILL.md` |
| 스펙 변경 | `munto-spec-change` | `.agents/skills/common/docs/munto-spec-change/SKILL.md` |
| DBML·Swagger·TCL | `dev-chain-design` | `.agents/skills/common/docs/dev-chain-design/SKILL.md` |
| IP 작성 | `dev-chain-implementation-plan` | `.agents/skills/common/docs/dev-chain-implementation-plan/SKILL.md` |
| NestJS 구현 | `dev-chain-backend` | `.agents/skills/backend/dev-chain-backend/SKILL.md` |
| 검증 | `dev-chain-verify` | `.agents/skills/common/docs/dev-chain-verify/SKILL.md` |
| DBML only | `dbml-writer` / `dbml-reviewer` | `.agents/agents/` 서브에이전트 |
| Swagger only | `swagger-writer` | `.agents/agents/swagger-writer.md` |
| Unit TCL | `unit-tcl-writer` | `.agents/agents/unit-tcl-writer` |
| 설계 정합성 | `design-consistency-reviewer` | 3종(DBML·Swagger·TCL) fan-in |

**VT GW 백엔드 규칙** (구현 단계): es-toolkit `/es-arch`·`/es-style`이 Vatech 표준이며, NestJS는 **DI abstract class 포트** 패턴 (`ezcloud/CLAUDE.md`와 동일 계열).

### 7.4 SRS 작성 시 VT 프로젝트 특수 규칙

- **§1.5 Related Documents**: 로컬 `../../` 경로 **금지** — [`08.VT_API_Gateway/README.md`](08.VT_API_Gateway/README.md)의 **VKS·Azure URL**만 사용.
- **라우팅 ADR-11**(§4.1): `Vatech-Target` 유무로 GW 고유 API / 프록시(B 내부·C 외부) 구분 — verbatim bypass, B/C OpenAPI 재정의 금지.
- **Parent/Child**: ④·③-C는 ③ SRS **하위** — 본문 중복 금지, §앵커 참조.
- **Scott 문서**는 SSOT에서 **추출** — Requirements.md에 직접 쓰지 말고 SRS를 수정.

---

## 8. AI 방법론 — `es-toolkit`

**레포**: `~/Documents/Azure/es-toolkit`

Vatech 전사 개발 표준 배포 meta-repo. **`setup.sh`** 로 `~/.claude/`에 명령·에이전트가 배포된다.

### 8.1 Claude 명령 (`/es-*`)

| 명령 | VT GW에서 쓰는 경우 |
| --- | --- |
| `/es-ticket` | ESIP Jira 티켓 + `tasks/ESIP-NNN-slug` 브랜치 |
| `/es-git` | 커밋·PR 규약 (Conventional Commits) |
| `/es-pr` | **Azure DevOps PR** 생성 |
| `/es-confluence` | VKS 페이지 CRUD (One Pager ①② 등록 시) |
| `/es-arch` | DDD 4-layer·DI 포트 검증 (구현 단계) |
| `/es-style` | 코드 스타일 리뷰 |
| `/es-tdd` | 테스트 우선 사이클 |
| `/es-review` | 변경 리뷰 |
| `/es-qa-check` / `/es-qa-resolve` | QA 이슈 |

명령 본문: `es-toolkit/packages/es-toolkit-cli/templates/claude-commands/`

### 8.2 vt-api-gateway `CLAUDE.md`

구현 레포 루트: **`vt-api-gateway/CLAUDE.md`** (워크스페이스 폴더명 기준)

- Jira **ESIP** · Component **platform/api-gateway**
- 브랜치 `tasks/ESIP-NNN-slug`
- 커밋 `type(api-gateway): ESIP-NNN <요약>`

---

## 9. 워크플로우 — 작성 → 리뷰 → baseline

```
[초안]     scp-architecture/docs/VT_API_Gateway/08.VT_API_Gateway/specs/
              ↓  (baseline 직전 PR)
[공식]     vt-api-gateway/docs/specs/  (Azure PR · baseline 태그)
              ↓  (포인터만 남김)
[로컬]     scp-architecture — URL 안내 또는 파일 삭제 (복제 금지)
[공유]     VKS — PRD/ARD 링크 · One Pager(①②) 본문
```

**드리프트 방지:**

- 같은 파일을 두 레포에 **복제하지 않는다**.
- baseline 이후 수정은 **Azure git만**.
- 외부 문서 인용은 **공식 URL**.

---

## 10. API·설계 핵심 개념 (SRS 요약)

Claude Code가 SRS/OpenAPI를 수정할 때 **반드시 유지**할 경계:

### 10.1 라우팅 = ADR-11 target-routed proxy (2면)

- **GW 고유 API**(`Vatech-Target` 없음): GW가 OpenAPI로 정의 — `/v1/auth/*`·`/v1/webhooks/*`·`/v1/clinics/*`·`/admin/v1/*` 등. **`/v1/uploads`는 폐기**(GW는 presigned 비발급).
- **프록시**(`Vatech-Target` 있음): 논리 ID(예 `cleverspace`·`axs`)로 upstream 결정해 **verbatim bypass**. 차이는 trust profile뿐 — **B(내부: CleverSpace·OneID)** / **C(외부: AXS·OAuth·고정 egress IP)**. upstream 추가=레지스트리 1행. B/C OpenAPI 재정의 금지.
- **업로드**: GW는 presigned 비발급·**중계만**. 발급=CleverSpace(②)/AXS(③), 바이트는 storage 직결(GW 미경유).

### 10.2 Webhook (§4.1.3·§7.6)

- **발신자 식별** = provider별 전용 호스트(`{provider}.webhook.gw.vatech.com`, Host/SNI) — 유연 수신(경로/스키마 비강제). **식별≠인증**(인증=HMAC+timestamp).
- **분배** = 내부 경로(클라우드 HTTP push=CleverLab만·갈래B 보류 / Edge=EzServer MQTT). 클라우드 수신 대상에 **CleverSpace는 아님**.

### 10.3 OpenAPI vs code-first

- 지금: `design/openapi/vt-api-gateway.openapi.yaml` = **설계 합의 초안**.
- 구현 착수 후: NestJS `@nestjs/swagger` **`/api-docs`가 정본** — 초안은 설계 근거로만 유지.

### 10.4 DBML → Prisma

- `design/dbml/vt-api-gateway.dbml` = 테이블 SSOT → 구현 시 Prisma schema.

---

## 11. 다음 작업 후보 (우선순위 제안)

사용자 지시 없이 **자동 착수하지 말 것**. 아래는 핸드오프 시점의 후보 목록.

| 우선 | 작업 | 입력 |
| --- | --- | --- |
| 1 | ③ SRS Appendix B TBD 정리 · baseline 준비 | SRS.md, _status.md |
| 2 | scp-architecture design → **vt-api-gateway PR 이관** | specs/README.md 이관 규칙 |
| 3 | **④ Sub-SRS** 초안 (AXS OAuth·Webhook·presign 경로③) | AXS_docs, §4.1.4·§7.5 |
| 4 | **③-C Sub-SRS** 초안 | §7.9 관리 API, PRD §12.1 |
| 5 | **①② One Pager** (VKS) | CleverAPI호환성, Roadmap |
| 6 | PHASE 1: Unit TCL · IP | dev-chain-design 완료 후 |

---

## 12. 작성·커밋 규칙

| 항목 | 규칙 |
| --- | --- |
| 언어 | 사용자 대화·문서 본문 **한국어** (코드 주석·커밋은 영어 — es-toolkit 표준) |
| 커밋 | **사용자가 요청할 때만** — AI가 임의 commit/push 금지 |
| scp-architecture 커밋 메시지 | **한국어** (`.cursorrules`) |
| vt-api-gateway 커밋 | `type(api-gateway): ESIP-NNN <요약>` |
| 이모지 | 문서·코드 주석에 **사용 금지** |
| Markdown | scp-architecture `guide.mdc` — 간결, 중복 최소 |
| Spec 구조 | SRS Template v3.3 **항목 추가·삭제·번호 변경 금지** |

---

## 13. Claude Code 시작 프롬프트 예시

아래를 Claude Code 첫 메시지로 붙여넣을 수 있다.

```
VT API Gateway 스펙 작업을 이어한다.
작업 루트: scp-architecture/docs/VT_API_Gateway
먼저 읽을 파일:
- VT API Gateway — Claude Code 작업 가이드.md
- README.md
- 08.VT_API_Gateway/specs/README.md
- 08.VT_API_Gateway/specs/03-srs-gateway/SRS.md
- 08.VT_API_Gateway/specs/03-srs-gateway/_status.md

방법론: munto-dev-assistant dev-chain + es-toolkit /es-*
워크스페이스: ~/Documents/Azure/scp.code-workspace

현재: ③ SRS 작성 중. §4.1.4 업로드 3경로 반영 완료.
다음 작업: [여기에 구체 지시]
```

---

## 14. 관련 링크 빠른 모음

| 자료 | 링크 |
| --- | --- |
| 본 가이드 | `docs/VT_API_Gateway/VT API Gateway — Claude Code 작업 가이드.md` |
| 워크스페이스 | `docs/VT_API_Gateway/README.md` |
| SSOT 초안 | `docs/VT_API_Gateway/08.VT_API_Gateway/specs/03-srs-gateway/SRS.md` |
| URL 매핑 | `docs/VT_API_Gateway/08.VT_API_Gateway/README.md` |
| CleverAPI 참고 | `docs/VT_API_Gateway/references/CleverAPI호환성체크/` |
| AXS 참고 | `docs/VT_API_Gateway/references/Straumann연동/` |
| SRS 템플릿 | `docs/VT_API_Gateway/templates/SRS_v3.3_template.md` |
| Azure GW SRS (공식) | https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway?path=/docs/specs/SRS.md |
| dev-process-guide | `munto-dev-assistant/document/dev-process-guide.md` |
| spec-standard | `munto-dev-assistant/document/spec-standard.md` |
| es-toolkit | `es-toolkit/CLAUDE.md` |
