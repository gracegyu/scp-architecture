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

## 관련 레포·참고 자료 (연동 개발 참고)

GW 본체(`vt-api-gateway`) 외에, 외부 연동(Straumann AXS 등)·클라이언트 호환·인증 개발 시 참고하는 레포·문서를 모은다. 새 참고 대상이 생기면 여기에 추가한다. **아직 clone하지 않은 레포는 상태를 `필요`로 적어 두면 받아 놓는다.**

### 레포 (대부분 로컬 워크스페이스 clone됨)

| 레포 | Azure Repos | 용도 | 상태 |
|------|-------------|------|------|
| vt-api-gateway | [es-platforms/vt-api-gateway](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway) | GW 본체 | clone |
| cleveronegroup | (URL 확인 필요) | CleverOne 클라이언트 — 식별 헤더·연동 흐름 | clone |
| ezserver_pms_integration | [ezserver/ezserver_pms_integration](https://dev.azure.com/ewoosoft/ezserver/_git/ezserver_pms_integration) | EzServer PMS 연동 모듈 — EZ↔외부(AXS 등) 연동 참고 소스 | clone |
| ezserver-pms-integration-onepager | [ezserver/ezserver-pms-integration-onepager](https://dev.azure.com/ewoosoft/ezserver/_git/ezserver-pms-integration-onepager) | PMS 연동 OnePager 문서 | clone |
| oneid | [scp-sharedservice/oneid](https://dev.azure.com/ewoosoft/scp-sharedservice/_git/oneid) | OneID 인증 연계(OIDC) | clone |
| ezcloud | [ezicloud/ezcloud](https://dev.azure.com/ewoosoft/ezicloud/_git/ezcloud) | CleverSpace/클라우드 백엔드 | clone |
| ESLinkageCloudPlatform | (URL 확인 필요) | ES Linkage 연동 플랫폼·공용 (common/) | clone |

### 참고 문서·자료

- 외부 API — [Straumann AXS API](https://developer.axs.straumann.com/api) · [AXS 연동 가이드 (Getting Started)](https://developer.axs.straumann.com/docs/getting-started) · 로컬 스냅샷: [AXS_docs 인덱스](<../Straumann연동/AXS_docs/README.md>) (인증·Webhooks·Integration·Regions, 취득 2026-06-16)
- Straumann 연동 문서 — [docs/Straumann연동](<../Straumann연동/README.md>) (분석보고서 · 4월2일 바텍 제안 · 4월30일 회의록)
- 레거시·호환성 문서 — [docs/CleverAPI호환성체크 (API 호환성 방안 비교)](<../CleverAPI호환성체크/API호환성_방안비교_보고서.md>) 및 그 `docs/` 하위 스펙(CleverSpace v1.3 SRS · EzCloud RestApi · OneID API · EzServer PMS SRS 등)
- CleverOne SRS (작성: Nick) — 클라이언트 식별 헤더·연동 흐름 참고