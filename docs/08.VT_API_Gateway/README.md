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
| 08. VT API Gateway (허브) | `08.VT_API_Gateway.md` | https://vks.vatech.com/spaces/ESDEVELOPER/pages/311608279/08.+VT+API+Gateway | ESDEVELOPER / 04. PDP / 08 |
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
| AXS OpenAPI 스냅샷 (사내) | https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/references/axs-openapi/README.md | 외부 정본에서 취득(2026-06-16) · Confidential |
| VT API Gateway — ESMN 진척 (MeetingNotes) | https://vks.vatech.com/spaces/ESMN/pages/311608221/VT+API+Gateway+platform+api-gateway | PM용 · README 기존 링크 |
| Jira ESIP (작업) | https://vts.vatech.com/browse/ESIP-2 | Epic v1.0 |

## 프로젝트 진행·문서 전략 (개인 운영용 · VKS 미공유)

분석 아키텍트 개인 관리 문서. 팀 공유용 스펙 단위 표는 [PRD §12.1](<VT API Gateway — PRD (v2).md>).

- [VT API Gateway — 프로젝트 진행·문서 전략](<VT API Gateway — 프로젝트 진행·문서 전략.md>)

## 관련 레포·참고 자료 (연동 개발 참고)

GW 본체(`vt-api-gateway`) 외에, 외부 연동(Straumann AXS 등)·클라이언트 호환·인증 개발 시 참고하는 레포·문서를 모은다. 새 참고 대상이 생기면 여기에 추가한다.

### 레포

| 레포 | Azure Repos | 용도 | 상태 |
|------|-------------|------|------|
| vt-api-gateway | [es-platforms/vt-api-gateway](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway) | GW 본체(신규 개발) | ✅ clone · 구현 예정 |
| cleveronegroup | http://essvn.vatech.co.kr/svn/vatech/trunk/product/cleveronegroup/ | CleverOne 클라이언트 — 식별 헤더·연동 흐름 | ✅ clone · ✅ URL 확보 |
| ezserver_pms_integration | [ezserver/ezserver_pms_integration](https://dev.azure.com/ewoosoft/ezserver/_git/ezserver_pms_integration) | EzServer PMS 연동 모듈 — EZ↔외부(AXS 등) 연동 참고 소스 | ✅ clone |
| ezserver-pms-integration-onepager | [ezserver/ezserver-pms-integration-onepager](https://dev.azure.com/ewoosoft/ezserver/_git/ezserver-pms-integration-onepager) | PMS 연동 OnePager 문서 | ✅ clone |
| oneid | [scp-sharedservice/oneid](https://dev.azure.com/ewoosoft/scp-sharedservice/_git/oneid) | OneID 인증 연계(OIDC) | ✅ clone |
| ezcloud | [ezicloud/ezcloud](https://dev.azure.com/ewoosoft/ezicloud/_git/ezcloud) | CleverSpace/클라우드 백엔드 | ✅ clone |
| ESLinkageCloudPlatform | http://essvn.vatech.co.kr/svn/vatech/trunk/product/common/ESLinkageCloudPlatform | ES Linkage 연동 플랫폼·공용 (common/) | ✅ clone · ✅ URL 확보 |
| **EzServer 본체 (EPI/PHP)** | (URL 확인 필요) | 경로 A 중계·MQTT·헤더 대리·클리닉별 버전 | 🔴 미확보 |
| **CleverLab** | (URL 확인 필요) | 5단계 갈래 B — 기공소 PMS·클라우드↔AXS | 🔴 미확보 |
| **GW Console** | 추천 `vt-api-gateway-console` — [es-platforms/vt-api-gateway-console](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console) (미생성) | Admin Web — 매핑·클리닉·상태 관리. SSOT: **③-C Sub-SRS** ([PRD §12.1](<VT API Gateway — PRD (v2).md>)) | 🔴 미확보 |
| **GW 인프라 (IaC)** | 추천 `vt-api-gateway-infra` — [es-platforms/vt-api-gateway-infra](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-infra) (미생성) | K8s·Route 53 GeoDNS·고정 egress IP 등. **인프라 담당 별도** — 개발 시 직접 다루지 않음, **③ SRS에 배치·GeoDNS 계획만** 기술 | 🔴 미확보 (인프라 담당 참조) |

> **GW 레포 명명 (추천).** 본체 `vt-api-gateway`와 동일하게 Azure DevOps **`es-platforms`** 프로젝트·`vt-api-gateway-*` sibling 패턴. Console = Admin SPA/웹, Infra = Terraform/Helm 등 IaC. 인프라 담당·플랫폼팀과 생성 전 이름 합의 권장.

### 참고 문서·자료

| 자료 | 용도 | 상태 |
|------|------|------|
| [Straumann AXS API](https://developer.axs.straumann.com/api) · [Getting Started](https://developer.axs.straumann.com/docs/getting-started) | AXS 공식 포털 | ✅ 온라인 |
| [AXS_docs 인덱스](<../Straumann연동/AXS_docs/README.md>) | 인증·Webhooks·Integration·Regions 로컬 스냅샷 (2026-06-16) | ✅ 확보 |
| [docs/Straumann연동](<../Straumann연동/README.md>) | 분석보고서 · 4/2 제안 · 4/30 회의록 | ✅ 확보 |
| [API 호환성 방안 비교](<../CleverAPI호환성체크/API호환성_방안비교_보고서.md>) 및 `docs/` 하위 CSV·SRS | CleverSpace v1.3 · EzCloud RestApi · OneID · EzServer PMS SRS | ✅ 확보 |
| **CleverOne SRS** (작성: Nick) | 클라이언트 식별 헤더·연동 흐름 | 🔴 미확보 |
| **AXS OpenAPI 전체 스냅샷** | [AXS_docs/openapi](<../Straumann연동/AXS_docs/openapi/README.md>) — 5 API YAML + index.json | ✅ 확보 (2026-06-16) |
| **AXS sandbox OAuth Client·endpoint** | `unstable` 연동 테스트 | 🔴 미확보 (Straumann 제공 대기) |
| **고정 egress IP (AXS whitelist)** | GW→AXS 아웃바운드 | 🔴 미확보 (인프라 담당) |
| **운영 호환성 매트릭스** | API × 최소 클라이언트 버전 확정본 | 🔴 미확보 |
| **CleverSpace v1.3 통합 SRS** (마크다운) | CSV 외 단일 SSOT | 🟡 부분 (CSV만 확보) |

> **SSOT 작성 vs 외부 확보:** `vt-api-gateway`·`vt-api-gateway-console` 구현·①·②·③·③-C·④ SSOT 본문·② presigned 신규 발급 상세 스펙은 **우리가 작성**하는 산출물이며, 위 표의 🔴 미확보와 구분한다. ② presigned 신규 발급은 **2단계 One Pager**에서 정의한다.
