# VT API Gateway — 로컬 워크스페이스

Claude Code·Cursor 등 AI 에이전트의 **실행 루트**다. Scott 통제 문서·SSOT 초안·입력 참고 자료·작성 템플릿을 한곳에 모았다.

> **Claude Code 시작**: [VT API Gateway — Claude Code 작업 가이드](<VT API Gateway — Claude Code 작업 가이드.md>)를 **첫 문서**로 읽는다.

> **무엇을 어디서 관리하나** (중복 방지 — 각 관심사는 1곳)
> - **참고 소스·레포·외부 경로**(계속 추가) → [참조 카탈로그](<참조-카탈로그.md>) ← 새 경로는 여기에만
> - **통제문서 정본 URL**(VKS/Azure, SRS §1.5) → [08.VT_API_Gateway/README.md](08.VT_API_Gateway/README.md)
> - **AI 작업 절차·방법론·규칙** → [작업 가이드](<VT API Gateway — Claude Code 작업 가이드.md>)
> - **폴더 구조·역할** → 본 문서

## 폴더 구조

```
docs/VT_API_Gateway/                    ← Claude Code 실행 루트
├── README.md                           ← 본 문서
├── VT API Gateway — Claude Code 작업 가이드.md
│
├── 08.VT_API_Gateway/                  ← Scott 통제 + SSOT (VKS 08 허브)
│   ├── 08.VT_API_Gateway.md            # VKS 허브 동기
│   ├── README.md                       # VKS·Azure URL 매핑표
│   ├── VT API Gateway — PRD (v2).md
│   ├── VT API Gateway — ARD (아키텍처).md
│   ├── specs/                          # ★ SRS·Sub-SRS·design 초안
│   └── …
│
├── references/                         ← 입력 자료 (SSOT 아님 · Confidential)
│   ├── CleverAPI호환성체크/            # ① One Pager · CleverSpace v1.3 CSV
│   └── Straumann연동/                  # ④ Sub-SRS · AXS OpenAPI 스냅샷
│
└── templates/                          ← SRS·One Pager 작성 틀
    ├── SRS_v3.3_template.md
    └── OnePager_v1.0_template.md
```

## 역할 구분

| 영역 | 경로 | 성격 |
| --- | --- | --- |
| **통제·SSOT** | `08.VT_API_Gateway/` | PRD·ARD·`specs/` — 작성·baseline 대상 |
| **입력 참고** | `references/` | CSV·AXS YAML·회의록 — SSOT 작성 시 *읽기만* |
| **도구** | `templates/` | SRS/One Pager 항목 구조 틀 |
| **방법론** | `abc-dev-assistant/` (워크스페이스) | dev-chain·spec-standard |
| **구현 표준** | `es-toolkit/` (워크스페이스) | `/es-ticket` · `/es-pr` 등 |
| **공식 SSOT (baseline 후)** | `vt-api-gateway/docs/specs/` | Azure git PR |

## 빠른 링크

| 목적 | 경로 |
| --- | --- |
| ③ SRS 초안 | [08.VT_API_Gateway/specs/03-srs-gateway/SRS.md](08.VT_API_Gateway/specs/03-srs-gateway/SRS.md) |
| design OpenAPI | [08.VT_API_Gateway/specs/03-srs-gateway/design/openapi/](08.VT_API_Gateway/specs/03-srs-gateway/design/openapi/) |
| CleverAPI 호환성 | [references/CleverAPI호환성체크/](references/CleverAPI호환성체크/) |
| AXS 연동 참고 | [references/Straumann연동/](references/Straumann연동/) |
| SRS 템플릿 | [templates/SRS_v3.3_template.md](templates/SRS_v3.3_template.md) |
| URL 매핑 (VKS·Azure) | [08.VT_API_Gateway/README.md](08.VT_API_Gateway/README.md) |

## 이전 경로 (2026-06-22 이관)

| 이전 | 현재 |
| --- | --- |
| `docs/08.VT_API_Gateway/` | `docs/VT_API_Gateway/08.VT_API_Gateway/` |
| `docs/CleverAPI호환성체크/` | `docs/VT_API_Gateway/references/CleverAPI호환성체크/` |
| `docs/Straumann연동/` | `docs/VT_API_Gateway/references/Straumann연동/` |
| `docs/spec-templates/` | `docs/VT_API_Gateway/templates/` |
