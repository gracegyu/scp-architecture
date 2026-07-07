## Claude Code / AI 에이전트 핸드오프

Claude Code 실행 루트는 **`docs/VT_API_Gateway/`** (본 `08.VT_API_Gateway/`의 상위)다.

- [VT API Gateway — Claude Code 작업 가이드](<../VT API Gateway — Claude Code 작업 가이드.md>) — 워크스페이스·레포·참고·스킬·진행 상태
- [워크스페이스 README](<../README.md>) — 4영역(08 · references · templates) 인덱스

## comment by 김성훈/Scott

VT API Gateway 프로젝트를 시작 하기 위한 정리를 했습니다.

- 기본 중심 문서 입니다.
    - [08. VT API Gateway - ES_Development - VKS](<08.VT_API_Gateway.md>)
- PM 용 리포트 진행 상황 체크 용 페이지 입니다.
    - [VT API Gateway (platform/api-gateway) - ES_MeetingNotes - VKS](https://vks.vatech.com/spaces/ESMN/pages/311608221/VT+API+Gateway+platform+api-gateway)
- Jira board 입니다.
    - [VT API Gateway (ESIP) - Agile Board - VTS](https://vts.vatech.com/secure/RapidBoard.jspa?rapidView=373)
- Repo 입니다.
    - [vt-api-gateway - Repos](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway)

## 문서 URL 매핑 (VKS / Azure)

통제·공유 문서(SRS §1.5 Related Documents 등)는 **로컬 상대 경로(`../../…md`)가 아니라 아래 공식 URL**을 쓴다. VKS로 옮긴 뒤에도 링크가 깨지지 않게 하기 위한 **정본 매핑표**다. `TBD`는 VKS pageId 또는 Azure 경로를 확인 후 채운다.

> **용도 구분**
> - **VKS(Confluence)**: PRD·ARD·설계 해석·One Pager(①②) — ESDEVELOPER / 04. Product Development Plan / 08. VT API Gateway
> - **Azure Repos**: ③ GW SRS·Sub-SRS(③-C·④) — `vt-api-gateway/docs/specs/` (PR 리뷰, baseline 태그)
> - **로컬 전용**: `specs/` 작업 초안·`00-execution-allocation.md` 등 — VKS URL 없음(공유 문서에 링크 금지)

### ESDEVELOPER — 08. VT API Gateway (통제·설계 문서)

| 문서 | 로컬 경로 (scp-architecture) | 공식 URL | 근거 / 비고 |
| --- | --- | --- | --- |
| 08. VT API Gateway (허브) | `VT_API_Gateway/08.VT_API_Gateway/08.VT_API_Gateway.md` | https://vks.vatech.com/spaces/ESDEVELOPER/pages/311608279/08.+VT+API+Gateway | ESDEVELOPER / 04. PDP / 08 |
| PRD (v2) | `VT API Gateway — PRD (v2).md` | https://vks.vatech.com/pages/viewpage.action?pageId=311608280 | ESIP-3 |
| ARD (아키텍처) | `VT API Gateway — ARD (아키텍처).md` | https://vks.vatech.com/pages/viewpage.action?pageId=311608281 | ESIP-3 |
| API 명세·데이터 모델·주권 | `VT API Gateway — API 명세·데이터 모델·주권.md` | https://vks.vatech.com/x/CMSSEg | |
| 인증·보안·컴플라이언스 설계 | `VT API Gateway — 인증·보안·컴플라이언스 설계.md` | https://vks.vatech.com/pages/viewpage.action?pageId=311608329 | ESIP-9 |
| 요구사항 명세 (Requirements) | `VT API Gateway — 요구사항 명세 (Requirements).md` | https://vks.vatech.com/x/AcSSEg | 본 SRS가 SSOT로 흡수 — 추출 뷰 |
| 개발계획서 (착수 품의) | `VT API Gateway — 개발계획서 (착수 품의).md` | https://vks.vatech.com/pages/viewpage.action?pageId=311608330 | ESIP-10 |
| AXS 연동 테스트 환경 (unstable) | `VT API Gateway — AXS 연동 테스트 환경 (unstable).md` | https://vks.vatech.com/x/AMSSEg | ESIP-14 |
| 개발 Roadmap 결정 (배경) | `VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md` | https://vks.vatech.com/x/r9iSEg | PRD child · 통제 문서 아님 |
| 프로젝트 진행·문서 전략 | `VT API Gateway — 프로젝트 진행·문서 전략.md` | (VKS 미등록 · 개인 운영) | 팀 공유 문서에 링크하지 않음 |

### 스펙 SSOT (Case D · PRD §12.1)

| 스펙 | 작성(로컬) | 공식 URL | 비고 |
| --- | --- | --- | --- |
| ③ GW SRS | `specs/03-srs-gateway/SRS.md` | https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/SRS.md | VKS 추출본 게시 안 함 |
| ③-C GW Console Sub-SRS | `specs/03c-subsrs-gw-console/` | https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/03c-subsrs-gw-console/Sub-SRS.md | |
| ④ Straumann AXS Sub-SRS | `specs/04-subsrs-straumann-axs/` | https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/04-subsrs-straumann-axs/Sub-SRS.md | ③ 하위 |
| ① API 호환성 One Pager | `specs/01-onepager-api-compatibility/` | 경로TBD — VKS(Confluence) | |
| ② Presigned One Pager | `specs/02-onepager-presigned-url/` | 경로TBD — VKS(Confluence) | |
| OpenAPI (GW) | `docs/specs/design/openapi/` | https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/design/openapi/vt-api-gateway.openapi.yaml | dev-chain-design SSOT |
| DBML (GW) | `docs/specs/design/dbml/` | https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/design/dbml/vt-api-gateway.dbml | dev-chain-design SSOT |

### 참고·외부 (SRS §1.5 등)

| 자료 | 공식 URL | 비고 |
| --- | --- | --- |
| AXS OpenAPI (외부 정본) | https://developer.axs.straumann.com/api | Straumann API Explorer · 스펙 인덱스 `https://developer.axs.straumann.com/specs/index.json` |
| AXS OpenAPI 스냅샷 (사내) | https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/references/axs-docs/README.md | 외부 정본에서 취득(2026-06-16) · Confidential |
| VT API Gateway — ESMN 진척 (MeetingNotes) | https://vks.vatech.com/spaces/ESMN/pages/311608221/VT+API+Gateway+platform+api-gateway | PM용 · README 기존 링크 |
| Jira ESIP (작업) | https://vts.vatech.com/browse/ESIP-2 | Epic v1.0 |

## 프로젝트 진행·문서 전략 (개인 운영용 · VKS 미공유)

분석 아키텍트 개인 관리 문서. 팀 공유용 스펙 단위 표는 [PRD §12.1](<VT API Gateway — PRD (v2).md>).

- [VT API Gateway — 프로젝트 진행·문서 전략](<VT API Gateway — 프로젝트 진행·문서 전략.md>)

## 관련 레포·참고 자료

> **이동(2026-06-25)**: 레포·소스·외부 참고 경로 카탈로그는 중복 방지를 위해 **[참조 카탈로그](<../참조-카탈로그.md>)** 로 일원화했다. 새 참고 대상은 거기에 추가한다. 본 문서는 **통제문서 정본 URL 매핑**(위 표)만 보유한다.
