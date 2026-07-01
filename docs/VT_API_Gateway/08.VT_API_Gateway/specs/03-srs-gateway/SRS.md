# VatechAPIGateway SRS (③ GW 일원화 + 멀티 Region)

> **골격(skeleton) — v0.1 작성 중.** 고정 항목(1~7장 + Appendix)을 모두 배치했다. 근거가 있는 내용은 PRD/ARD/요구사항 명세에서 가져왔고, 사람이 확정해야 할 곳은 `TBD`(4항목) 또는 `❓확인`으로 표시했다. 본 골격은 SRS v3.3 표준을 따른다.

**문서 통제**

| 문서 ID | ESIP-GW-SRS |
| --- | --- |
| 문서 버전 | v0.1 (Draft · 골격) |
| 적용 제품 버전 | gw/1.0.0.0~ |
| 분류 | 통제 문서 (Controlled · IEC 62304 / ISO 13485 — 요구사항 추적성) |
| SSOT 여부 | 본 SRS가 GW 플랫폼 요구사항의 SSOT. 기존 [요구사항 명세](https://vks.vatech.com/x/AcSSEg)·[PRD](https://vks.vatech.com/pages/viewpage.action?pageId=311608280)·[ARD](https://vks.vatech.com/pages/viewpage.action?pageId=311608281)는 추출/배경 뷰 |
| 공식 등록처 | [vt-api-gateway `docs/specs/SRS.md`](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/SRS.md) (PR 리뷰) |

---

# 1 Introduction (개요)

## 1.1 Purpose (목표)

본 SRS는 **VatechAPIGateway(이하 GW)** 의 소프트웨어 요구사항을 정의한다. 적용 제품 버전은 `gw/1.0.0.0` 이상이다.

본 문서는 **내부 개발용**으로 작성하며, 동시에 **IEC 62304 / ISO 13485 통제 문서 baseline**의 요구사항 추적성 근거로 사용한다. 외부(파트너·외주) 공유 시 §6.6 등 회사 내부 사정에 해당하는 절은 제거 후 전달한다.

## 1.2 Product Scope (범위)

CleverSpace는 유상화·이용 한도 등 새 정책으로 API를 계속 확장하지만, 클리닉·PC마다 버전이 제각각인 구버전 CleverOne·EzServer가 이를 인식하지 못해 **원인불명 실패**가 발생한다. 또한 CleverOne이 EzServer를 거치지 않고 CleverSpace로 직접 연동하는 **경로 B**가 존재해 인증·정책 통제가 두 갈래로 분산된다. 나아가 Straumann AXS처럼 보안상 직접 연결이 불가능한 외부 연동 수요가 늘고 있다. 본 프로젝트는 **모든 클라우드·디바이스 연동을 단일 게이트웨이로 일원화**하여 인증(OneID 연계)·버전 호환·Region 라우팅을 단일 집행점에서 처리하는 것을 목표로 GW는 (1) 모든 통신이 경유하는 중앙 control plane(인증·디바이스 관리·라우팅·config), (2) 파일은 presigned URL로 디바이스↔리전 직결(GW 무부하), (3) 디바이스–리전 매칭으로 데이터 주권 보장, (4) 외부 이벤트(AXS 등)의 단일 Webhook 수신·분배, (5) 클라이언트 버전 호환 게이팅을 수행한다.

**Will Not Do (의도적으로 제외):**

- **제품측(CleverSpace·CleverOne·EzServer) 변경 상세** — ① API 호환성 / ② Presigned One Pager에서 다룬다. 본 SRS는 GW 쪽 계약만 정의한다.
- **Straumann AXS connector 상세** — ④ Sub-SRS([Straumann AXS Sub-SRS](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/04-subsrs-straumann-axs/Sub-SRS.md))에서 다룬다. 본 SRS는 connector 프레임워크(§7.5)까지만.
- **GW Console(Admin Web) UI 상세** — ③-C Sub-SRS([GW Console Sub-SRS](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/03c-subsrs-gw-console/Sub-SRS.md))에서 다룬다. 본 SRS는 관리 API(§7.9)까지만.
- **CleverLab↔AXS 직접 연동(Roadmap 5단계 갈래 B)** — **현 시점 미고려**(2026-06 회의). 단 외부 cloud 서비스 연동 **일반 역량**(C 프록시·§4.1.1·§7.5)은 유지하므로, 향후 활성화 시 신규 코드가 아닌 레지스트리 등록으로 수용한다. 우선 범위는 **갈래 A(EzServer→AXS)** 다(④).
- **레거시 10만대 마이그레이션** — v2.0(FR-MIG-\*). 본 v1.0 범위 밖.

## 1.3 Document Conventions (문서규칙)

- **우선순위 표기**: 각 기능에 `(P1)/(P2)/(P3)` 표기. 하위 요구사항은 별도 표기 없으면 상위 우선순위를 상속한다.
  - **P1** = 반드시 포함, 제외 시 릴리스 불가 (요구사항 명세의 `M`·`v1.0`에 대응)
  - **P2** = 중요하나 일정 조정 가능 (`S` 또는 `v1.1`)
  - **P3** = 추가되면 좋음, 다음 Phase (`v1.2`/`v2.0`)
- **버전 표기**: 베이스라인(`gw/1.0`)은 표기 없음. 후속분만 `(v1.1)`·`(v1.2)` 표기.
- **변경 표기**: 색이 아닌 텍스트(`(변경: YYYY-MM-DD)`)로 표기, 색은 보조.
- **시간**: Unix Timestamp(ms). 필드명: camelCase.

## 1.4 Terms and Abbreviations (정의 및 약어)

> 모두가 아는 표준 용어(JWT·TLS·REST·OAuth2 등)는 제외. 본 문서 독자(개발·QA·인프라·PM) 일부가 모르거나 혼동할 만한 것만 선별.

| 용어 | 본 문서에서의 의미 | 비고 |
| --- | --- | --- |
| GW (VatechAPIGateway) | 모든 연동이 단일 경유하는 control plane | 본 SRS의 대상 제품 |
| LMP (LicenseManager) | EzServer **라이선스 관리 플랫폼** — 클리닉의 **Clinic-ID 발급원**. EzServer가 LMP에서 Clinic-ID 수신 시 GW 자동·무조건 등록(§2.3.1) | §2.3.1 |
| 디바이스(Device, GW 관점) | **= EzServer**(클리닉당 1개의 엣지 머신, 확정 2026-06-25). GW가 인증·레지스트리·enrollment·토큰을 다루는 "디바이스"는 모두 EzServer를 가리킨다. 물리 영상장비(CT/Xray)는 EzServer 뒤편이며 **GW 비대상**(엣지 내부) | §2.3.1·§7.1·§7.2·ADR-08 |
| Valkey | **캐시 엔진**(Redis 포크·완전 호환 — RESP 프로토콜·클라이언트·명령·키스페이스 동일). AWS 제품 = **ElastiCache for Valkey**. Redis는 2024 초 오픈소스 종료, Valkey가 후속·저비용이라 채택. 본 문서·키스페이스의 "Redis(호환)"는 곧 **Valkey**를 가리킴 | §3.1.2·§6.4·`design/redis/` |
| PHI | Protected Health Information — **환자 식별 가능 건강정보**(환자 정보·영상 파일 등). **GW는 PHI 본문을 저장·경유하지 않는다**(presigned 직결, 발급=CleverSpace/AXS) — control plane엔 메타·식별자만. 데이터 주권(리전 밖 미이동)·consent 게이팅 대상이며, 개발·테스트는 더미만(운영만 실 PHI) | §6.4·§6.5·§7.3.3·§3.1 |
| OTel (OpenTelemetry) | 관측성(추적·메트릭·로그) 수집·전송 **벤더 중립 표준/SDK**(CNCF). 요청 상관용 `traceId`/`spanId`를 생성 | §6.3.2·§3.1.2 |
| ADOT | **AWS Distro for OpenTelemetry** — AWS가 배포하는 OTel 수집기. OTel 계측 → ADOT 수집 → CloudWatch/Prometheus·Grafana | §3.1.2·§6.3.2 |
| PEP | Policy Enforcement Point — 요청 시점 인증·정책 집행 지점 | §7.1 |
| originator | 요청을 _시작한_ 주체(`Vatech-*` 헤더의 권위 소스) | §7.7 |
| `Vatech-Via` | 요청을 _경유한_ 중계 홉(예: EzServer) | originator와 분리 |
| Edge | 클리닉 현장의 EzServer (방화벽 뒤, inbound 불가) | §7.6 |
| soft-state | 완전 stateless가 아닌, cache TTL·mapping_version 기반 상태 | ADR-02 |
| Region Signer Agent | **폐기(2026-06-23)** — GW는 presigned 직접 발급·서명 안 함(발급=upstream CleverSpace/AXS, GW 중계) | §4.1.4·§7.4 |
| ClinicID↔Org-ID | 클리닉 식별자와 외부(AXS) 조직 식별자 매핑 | §7.3 / ④ |
| 경로 B (Path B) | CleverOne → CleverSpace 직접 연동(EzServer 미경유) | Deprecated 대상 |

> (PHI 추가됨.) 추가로 등록할 용어(예: allowlist) 또는 사내 공유 용어집 링크는 필요 시 보강.

## 1.5 Related Documents (관련문서)

**VKS (Confluence) — 통제·설계**

- [PRD (v2)](https://vks.vatech.com/pages/viewpage.action?pageId=311608280) — 상위 기획. §12.1 스펙 단위 정본
- [ARD (아키텍처)](https://vks.vatech.com/pages/viewpage.action?pageId=311608281) — ADR-01~10·컴포넌트·시퀀스
- [요구사항 명세](https://vks.vatech.com/x/AcSSEg) — FR/NFR 등록부 (본 SRS가 SSOT로 흡수, 해당 문서는 추출 뷰)
- [인증·보안·컴플라이언스 설계](https://vks.vatech.com/pages/viewpage.action?pageId=311608329) · [API 명세·데이터 모델·주권](https://vks.vatech.com/x/CMSSEg)
- [개발 Roadmap 결정 (배경)](https://vks.vatech.com/x/r9iSEg) — 케이스 D·단계

**Azure Repos — 스펙·설계 산출물 (`vt-api-gateway`)**

- [OpenAPI (GW 고유 API)](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/design/openapi/vt-api-gateway.openapi.yaml) — dev-chain-design SSOT
- [DBML (PostgreSQL)](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/design/dbml/vt-api-gateway.dbml) — dev-chain-design SSOT
- 하위 스펙:
  - ① API 호환성 One Pager (경로TBD) — VKS(Confluence), pageId 미확정
  - ② Presigned URL One Pager (경로TBD) — VKS(Confluence), pageId 미확정
  - [③-C GW Console Sub-SRS](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/03c-subsrs-gw-console/Sub-SRS.md)
  - [④ Straumann AXS Sub-SRS](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/04-subsrs-straumann-axs/Sub-SRS.md)

**외부·참고**

- [AXS OpenAPI (Straumann 정본)](https://developer.axs.straumann.com/api) · 스펙 인덱스 `https://developer.axs.straumann.com/specs/index.json`
- [AXS OpenAPI 스냅샷 (사내)](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/references/axs-openapi/README.md) — ④ 연동 입력 (취득 2026-06-16, Confidential)

## 1.6 Intended Audience and Reading Suggestions (대상 및 읽는 방법)

| #   | 챕터                | PM  | 백엔드 | 인프라/DevOps | QA  | 보안 | 경영진 |
| --- | ------------------- | --- | ------ | ------------- | --- | ---- | ------ |
| 1.2 | Product Scope       | 2   | 1      | 1             | 1   | 1    | 2      |
| 2.x | Overall Description | 2   | 2      | 2             | 2   | 1    | 1      |
| 3.x | Environment         | 1   | 2      | 2             | 2   | 1    | —      |
| 4.x | External Interface  | 1   | 2      | 2             | 2   | 2    | —      |
| 5·6 | Perf / NFR          | 1   | 2      | 2             | 2   | 2    | —      |
| 7   | Functional Req      | 1   | 2      | 1             | 2   | 1    | —      |

> 범례: 1=훑어 이해 / 2=자세히 / —=읽지 않아도 됨

## 1.7 Project Output (프로젝트 산출물)

### 1.7.1 Output Format

백엔드 서비스 (NestJS, Kubernetes(EKS) 배포, 단일 control-plane endpoint). API 문서는 `@nestjs/swagger` code-first(`/api-docs`). 서비스 공개 호스트(제안)는 §4.5 참조.

### 1.7.2 Output Name and Version

- 공식 명칭: **VatechAPIGateway**
- 레포지토리: `vt-api-gateway` (Azure es-platforms)
- 초기 버전: `gw/1.0.0.0`

### 1.7.3 Patent Information

None

---

# 2 Overall Description (전체 설명)

## 2.1 Product Perspective (제품 조망)

GW는 기존 제품군(CleverOne·EzServer·CleverSpace·OneID)과 외부 플랫폼(Straumann AXS) 사이의 **단일 control plane**으로 신규 구축된다.

```mermaid
flowchart TD
    subgraph CLINIC["클리닉 온프레미스"]
        CO["CleverOne"]
        EZ["EzServer (Edge) = GW 관점의 '디바이스'"]
        DEV["영상장비 CT/Xray<br/>(GW 비대상 · EzServer 뒤)"]
    end
    subgraph GWBOX["VatechAPIGateway (본 SRS 대상)"]
        GW["GW core<br/>인증·라우팅·region·외부 연동"]
        WHR["Webhook Ingress<br/>수신·큐·분배 (sub-tier)"]
    end
    subgraph UP["연동 서비스 (GW upstream · target-routed proxy, ADR-11)"]
        subgraph INT["내부 — B 프로파일 (우리 서비스·내부망)"]
            CS["CleverSpace (멀티 Region)"]
            CLAB["CleverLab"]
            OID["OneID"]
        end
        subgraph EXT["외부 — C 프로파일 (제3자·OAuth·고정 egress IP)"]
            AXS["Straumann AXS"]
        end
    end
    R53["Route 53 GeoDNS"]
    CONSOLE["GW Console (③-C)"]

    CO --> EZ
    EZ -->|"API 요청 (상행) · GW의 '디바이스'=EzServer"| GW
    DEV --> EZ
    %% API 호출은 대상 무관 동일 경로: GW → upstream (target-routed proxy, ADR-11). 차이는 trust profile뿐
    GW -->|"프록시 (B·내부)"| CS
    GW -->|"인증 연계 (B·내부)"| OID
    GW -->|"프록시 (C·외부: OAuth·고정 egress IP)"| AXS
    %% CleverLab은 프록시 대상이 아니라 갈래B 클라우드 클라이언트(보류) — CleverLab→GW→AXS
    CLAB -.->|"클라우드↔클라우드 (갈래B·보류): CleverLab→GW→AXS"| GW
    %% Webhook(이벤트 인바운드)은 API 호출과 별개 — 현재 AXS만 해당. 클라우드 수신=CleverLab만(갈래B 보류), CleverSpace는 webhook 대상 아님(§2.3.6)
    AXS -.->|"Webhook (인바운드·이벤트)"| WHR
    WHR -.->|"MQTT (분배·하행)"| EZ
    WHR -.->|"HTTP push (갈래B·보류)"| CLAB
    R53 -.-> GW
    CONSOLE -.-> GW

    classDef srsTarget fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#0d47a1
    class GW,WHR srsTarget
    %% GW(본 SRS) 범위 박스 = 연두 테두리(§2.1.1·§2.2 동일 색)
    style GWBOX fill:#e8f5e9,stroke:#66bb6a,stroke-width:3px
```

**색 범례** (§2.1·§2.1.1·§2.2 공통):

```mermaid
flowchart TD
    A["GW 범위"]:::scope
    B["GW core / Webhook Ingress"]:::box
    C["우리가 만드는 컴포넌트"]:::comp
    D["managed 인프라·데이터"]:::mgd
    E["외부 (비대상)"]:::ext
    classDef scope fill:#e8f5e9,stroke:#66bb6a,stroke-width:3px,color:#1b5e20
    classDef box fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#0d47a1
    classDef comp fill:#ffffff,stroke:#1565c0,stroke-width:1.5px,color:#0d47a1
    classDef mgd fill:#eceff1,stroke:#90a4ae,color:#37474f
    classDef ext fill:#ffffff,stroke:#bbbbbb,color:#555555
```

> managed(회색)=우리가 만들지 않는 AWS 자원(SQS·DB·NAT·LB) · 외부=GW 범위 박스 밖. **§2.1(상위) → §2.2(GW core 펼침)** 가 같은 색으로 줌인되어 이어진다.

| 외부 시스템 | 역할 |
| --- | --- |
| CleverOne / EzServer | 사내 호출자. EzServer는 Edge(방화벽 뒤, inbound 불가) |
| CleverSpace | 멀티 Region 백엔드(데이터 경로 대상) |
| OneID | 사람·클리닉·사내 호출자 인증(OIDC) |
| Straumann AXS | 외부 연동 대상. Webhook 수신·presigned 연동 |
| CleverLab | 우리 클라우드 기공소 PMS. GW의 **프록시 대상이 아니라 갈래 B 클라우드 클라이언트**(CleverLab→GW→AXS) + AXS 이벤트 webhook 수신처. **CleverLab↔AXS 직접 연동(갈래 B)은 현 시점 범위 외/보류**(§1.2·④ — 외부 cloud 연동 일반 역량은 유지) |
| Route 53 GeoDNS | EzServer를 최근접 GW Region에 연결 |
| GW Console | Admin Web(③-C Sub-SRS) — 관리 API 호출 |

> 상세 인터페이스는 §4. **Webhook Ingress는 GW 내부의 별도 sub-tier**(외부 서버 아님 — A면 GW 고유 API, §4.1.1·§7.6.1). *(Ingress = 수신(Webhook Receiver)·큐(SQS)·분배(Webhook Dispatcher)를 묶은 서브티어, §2.2·§7.6.7)* **API 호출 경로는 대상에 무관하게 동일하다** — `CleverOne→EzServer→GW→CleverSpace` 든 `…→GW→AXS` 든 모두 **GW를 단일 경유하는 target-routed proxy**(ADR-11, 경로 B 제거). 차이는 **trust profile뿐**: 내부(B=CleverSpace·OneID, 통과+정규화 신원) vs 외부(C=AXS, GW가 OAuth·고정 egress IP 추가). 그래서 다이어그램의 `GW→upstream` 화살표는 같은 종류이고, AXS만 라벨이 `C·외부`다. **CleverLab은 GW가 호출하는 프록시 대상이 아니라**, 클라우드↔클라우드 외부 연동(갈래 B)에서 **GW를 호출하는 클라이언트**다(CleverLab→GW→AXS) — 현 시점 **보류**(§1.2).
>
> **유일하게 다른 건 Webhook(이벤트 인바운드)** — AXS는 결과 이벤트를 GW로 _밀어 보내고_, GW가 **Webhook Ingress**로 받아 방화벽 뒤 **EzServer는 MQTT(하행, 갈래 A 역방향)**·**클라우드는 HTTP push**로 분배한다(대상=Org-ID→Clinic→리전 매핑, §7.3). 클라우드 수신 대상은 **CleverLab(갈래 B·보류)뿐**이며, **CleverSpace는 webhook 수신 대상이 아니다**(B 프록시·presigned 백엔드일 뿐 — 다이어그램엔 *API 호출 대상*으로만 그린다). 대상별 시나리오는 §2.3.6. AXS의 **외부 연동(egress)은 GW core**, **Webhook(인바운드)은 Webhook Ingress**로 들어와 방향이 반대다. 멱등·교차 리전 등 분배 상세는 **§2.3.6·§7.6**.
>
> **본 도는 control plane(정보 경로) context다** — **대용량 데이터의 presigned 직접 업로드(EzServer→발급주체 storage, GW 미경유)·AWS 미지원국 Provider MinIO·리전별 CS 노드는 생략**했다(Roadmap §2.6은 데이터 plane까지 함께 그림). 데이터 경로는 §2.3.4(경로②)·§2.3.5(경로③)·§4.1.4, 멀티 리전·MinIO는 §2.1.1·§3.1.2 참조.

### 2.1.1 배포 토폴로지 — 멀티 서버·멀티 리전 (egress·Webhook)

GW는 두 축으로 다중화된다: **멀티 서버**(한 리전 내 Multi-AZ K8s 복제본 — HA·수평 확장, §6.3.1) 와 **멀티 리전**(서울·미주 등, gw/1.2·§7.3.5). 두 경우 모두 **inbound는 안정 endpoint 하나**(리전별 LB, GeoDNS 뒤)로 수렴하지만 **outbound(egress)는 NAT EIP 다수**로 나간다 — **inbound IP ≠ egress IP**. GW pod는 **무상태(soft-state, ADR-02)** 라 DB·Redis를 pod마다 두지 않는다 — **같은 리전 pod는 동일 저장소를 공유**하고, 라우팅·식별 데이터는 **전역 일관**으로 둔다(데이터 토폴로지는 다이어그램 아래 참조).

> **v1.0은 단일 리전(예: 서울)만 실제 배포**한다(§2.7.1). 아래 다이어그램의 **멀티 리전(A·B)은 2차(gw/1.2) 목표 토폴로지**이며, v1.0 설계가 이를 *ready*로 갖춘다 — **구조(데이터 토폴로지·Region Resolver·apex DNS·egress 집합)는 동일하고 리전 수만 1→N**이다. v1.0은 리전 1개(예: RA)만 두고 GeoDNS·apex가 이를 가리킨다 — 전역 SSOT는 단일 리전 내에 존재하고, 2차에 복제를 추가한다.

> **Webhook Ingress 위치 — 컴퓨트는 리전, DNS·데이터만 전역.** Webhook Ingress(Receiver·SQS·Dispatcher, §2.2·§7.6)는 **GW 소프트웨어라 각 리전의 GW pods에서 실행**된다 — 전역 계층의 별도 컴퓨트가 아니다. 전역(리전 비종속)인 것은 **① 공개 호스트 DNS**(`axs.webhook.gw.vatech.com` = Route 53)와 **② 매핑 데이터 SSOT**뿐이다. 즉:
> - **단일 리전(v1.0)**: `axs.webhook.gw.vatech.com` → (서울) LB → **서울 리전 Webhook Ingress**가 수신·처리.
> - **멀티 리전(gw/1.2)**: 같은 호스트가 **GeoDNS(전역)** 로 **최근접 리전**에 붙고, 그 리전 Webhook Ingress가 수신 → **전역 매핑으로 대상 리전 판정** → 분배(대상이 다른 리전이면 **교차 리전**).
> - **전환 시 바뀌는 것은 DNS(단일 지정 → GeoDNS 전역 라우팅)와 데이터(단일 → 복제)뿐**이며, **Webhook Ingress 컴포넌트는 전역으로 옮기지 않는다**(항상 리전에서 실행). ← 질문의 "1안"(리전에서 실행, 전역 데이터 참조)이 맞다.

```mermaid
flowchart TB
    EZ["EzServer / CleverOne"]
    EXT["외부 (예: AXS) · region 비인지"]

    subgraph RA["GW Region A (서울)"]
        LBA["Ingress LB (inbound 1)"]
        GA["GW pods<br/>API + Webhook Ingress"]
        STA[("저장소 PG·SQS·Valkey")]
        NATA["NAT · egress EIP set A"]
        LBA --> GA
        GA --- STA
        GA --> NATA
    end

    subgraph GTIER["전역 계층 (리전 비종속 · GW 컴퓨트 없음 · AWS managed)"]
        DNS["Route 53 GeoDNS<br/>apex · axs.webhook.gw.vatech.com<br/>(리전 분기만, 처리 없음)"]
        GLOBAL[("전역 데이터 SSOT<br/>매핑·레지스트리·정책·JWKS")]
    end

    subgraph RB["GW Region B (미주) · gw/1.2"]
        LBB["Ingress LB (inbound 1)"]
        GB["GW pods<br/>API + Webhook Ingress"]
        STB[("저장소 PG·SQS·Valkey")]
        NATB["NAT · egress EIP set B"]
        LBB --> GB
        GB --- STB
        GB --> NATB
    end

    EZ --> DNS
    EXT ==>|"Webhook (공개 호스트)"| DNS
    DNS --> LBA
    DNS --> LBB

    STA -.->|"복제/sync"| GLOBAL
    STB -.->|"복제/sync"| GLOBAL
    GA -.->|"매핑 조회"| GLOBAL
    GB -.->|"매핑 조회"| GLOBAL

    NATA ==>|"egress (우리가 호출)"| EXT
    NATB ==>|"egress"| EXT
    EXT -.->|"IP whitelist = EIP A ∪ B"| NATA
    EXT -.-> NATB

    GA ==>|"분배(동일 리전) MQTT/HTTP"| EZ
    GA ==>|"대상=타 리전 → 교차 분배"| RB

    %% GW(본 SRS) 범위=전역 계층+각 리전(연두). GW 소프트웨어(pods)=연파랑, managed AWS(DNS·DB·LB·NAT)=회색
    style GTIER fill:#e8f5e9,stroke:#66bb6a,stroke-width:3px
    style RA fill:#e8f5e9,stroke:#66bb6a,stroke-width:3px
    style RB fill:#e8f5e9,stroke:#66bb6a,stroke-width:3px
    classDef srsTarget fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#0d47a1
    classDef mgd fill:#eceff1,stroke:#90a4ae,color:#37474f
    class GA,GB srsTarget
    class DNS,GLOBAL,STA,STB,NATA,NATB,LBA,LBB mgd
```

**색 범례** (§2.1과 동일):

```mermaid
flowchart TD
    A["GW 범위"]:::scope
    B["GW core / Webhook Ingress"]:::box
    C["우리가 만드는 컴포넌트"]:::comp
    D["managed 인프라·데이터"]:::mgd
    E["외부 (비대상)"]:::ext
    classDef scope fill:#e8f5e9,stroke:#66bb6a,stroke-width:3px,color:#1b5e20
    classDef box fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#0d47a1
    classDef comp fill:#ffffff,stroke:#1565c0,stroke-width:1.5px,color:#0d47a1
    classDef mgd fill:#eceff1,stroke:#90a4ae,color:#37474f
    classDef ext fill:#ffffff,stroke:#bbbbbb,color:#555555
```

> **일반화**: 아래는 **외부 서비스(C 프로파일) 공통** 규칙이며, **AXS는 한 예**다(향후 DS Core/3Shape 등 동일). egress IP whitelist·**provider별 전용 호스트(DNS) 수신**(각 리전 Webhook Ingress)·리전 분배는 provider에 무관하게 같은 방식으로 적용된다(ADR-11 레지스트리 모델과 일관).
>
> **B(내부) vs C(외부) 적용 범위**: **API 호출 경로는 내부(CleverSpace 등)·외부(AXS) 동일**(GW target-routed proxy, §2.1·§4.1.2). 본 절의 **고정 egress IP whitelist·Webhook 수신은 외부(C) 한정** 사항이다 — 내부(B) upstream은 같은 GW proxy를 타되 **내부망**이라 egress 고정 IP whitelist가 불필요하고, (현재) GW로 Webhook을 발신하지 않는다. 즉 §2.1.1이 외부(C) 토폴로지를 다루는 것이지, 내부 호출이 다른 경로라는 뜻이 아니다.

- **저장소 제품(§3.1.2 근거·비교표).** 엔진은 **PostgreSQL 확정**, 관리형 제품은 **처음부터 Aurora PostgreSQL 권장**(인프라 비준 TBD, Appendix B #18). 멀티 리전 전환이 Aurora는 **Global Database 활성화(마이그레이션 0)** 인 반면 RDS-first는 **RDS→Aurora 마이그레이션**이라 비대칭적으로 비싸 **단일 리전부터 Aurora 권장**(비용 델타 ~20%·저QPS라 작음). 캐시 = **Amazon ElastiCache for Valkey**(Redis 호환·리전 로컬·교차복제 안 함·로컬 PG에서 재적재). **다이어그램은 2차 멀티 리전 목표 토폴로지**이며 v1.0은 단일 리전에서 동일 제품으로 시작.
- **egress IP whitelist = 고정 EIP 집합(멀티 IP).** 외부 서비스(예: AXS)가 IP whitelist를 요구하면, 화이트리스트 대상은 GW가 _외부를 호출_ 할 때의 egress IP다. pod별 임시 IP가 아니라 **AZ/리전별 NAT의 고정 EIP**여야 하고, 멀티 리전이면 **전 리전 집합의 합집합(A ∪ B …)** 이며 유한·열거 가능해야 한다(FR-INT-03·§7.5.3·§2.6).
- **리스크/제약**: 오토스케일·새 AZ·**리전 증설은 egress IP를 늘리므로**, egress를 **고정 EIP 풀로 핀(pin)** 하고 외부(예: Straumann)와 **whitelist를 협의·갱신(리드타임)** 해야 한다. EIP 풀 provisioning·고정은 인프라(③-I) 책임(§2.6·§7.3.5).
- **Webhook 수신 = provider별 전용 호스트(식별), region 분배는 우리 몫.** 외부 서비스(AXS 등)는 **region을 모른다**. **provider별 전용 수신 호스트**(`{provider}.webhook.gw.vatech.com`)를 발급해 **Host(SNI)로 발신자를 식별**한다(우리가 통제하는 식별 — 상대 source IP에 의존하지 않음). **경로/형식은 provider 규약을 수용해 유연**하다(GW는 발신자 검증·라우팅만, payload 비해석; §4.1.3·§7.6.1·§4.5.1). **단 Host는 식별이지 인증이 아니며**, 신뢰는 HMAC+timestamp로 보장한다(§7.6.2). 수신 ingress(Webhook Ingress, §2.2)는 **전역 매핑(DB/캐시)에 연결**되어 webhook 내용(Org-ID 등)으로 **대상 클리닉의 리전을 판정**하고(§7.3 매핑·전역 일관), **대상 리전(A·B …)으로 재분배**한다(수신 리전 ≠ 대상 리전이면 **교차 리전 전달**). 즉 **region 결정은 외부도 GeoDNS도 아니라 수신 ingress의 매핑 조회**다. `eventId` 멱등 dedup은 인스턴스 공유 저장소(Redis)로 전역 보장(ADR-02·§7.6.4). 인바운드 검증(HMAC·timestamp; source IP allowlist는 옵션·방어심층, §7.6.2)은 egress whitelist와 **방향이 반대**다. 수신→분배 흐름 상세는 **§2.3.6·§7.6**.
  - **GeoDNS는 inbound webhook의 대상 리전을 정하지 않는다** — GeoDNS는 _호출자 위치_ 기준이라 외부의 고정 위치에선 늘 한 리전으로 귀결될 뿐이고, _처리 리전은 클리닉 소속(매핑)_ 이 정한다. provider 호스트가 어느 리전 GW로 해석되든, 그 **수신 GW가 매핑 조회 후 대상 리전으로 재분배**한다.

#### 데이터 공유·토폴로지 (멀티 서버·멀티 리전)

- **멀티 서버(리전 내) = 데이터 공유.** GW pod는 **무상태(soft-state, ADR-02)** 이며 **DB·Redis를 pod마다 두지 않는다.** 같은 리전의 모든 pod가 **동일한 리전 DB(PostgreSQL HA)·Redis를 공유**하므로 어느 pod가 처리하든 세션·멱등·캐시가 공유된다. "멀티 서버 = 데이터 분리"가 **아니다**.
- **멀티 리전 = 데이터 부류를 나눈다.**
  - **(전역 일관) 라우팅·식별 데이터** — device/clinic↔region 매핑·레지스트리·Org-ID↔ClinicID·정책(OPA)·compat matrix·JWKS. **모든 리전이 같은 답을 내야** 한다(예: B 리전에 떨어진 Webhook이 "클리닉 X는 A 리전 소속"임을 알아야 분배 가능). 따라서 **전역 일관**으로 둔다 — soft-state 캐시 + 변경 시 strong-consistency 경로·`mapping_version`(ADR-02·§7.3.1·§7.3.2).
  - **(리전 로컬) 운영 데이터** — audit log(발생 리전)·in-flight webhook/queue. **리전마다 다르며** 합쳐서 전체다.
  - **PHI는 어느 store에도 미저장**(§6.4) — 데이터 주권은 "PHI **바이트**를 매핑된 리전 storage로 라우팅"의 문제이지 GW DB 내용 분리가 아니다(§7.3.3). 전역 데이터는 PHI 미포함 control-plane 메타라 **리전 간 복제 가능**.
- **저장소 역할(PostgreSQL / Redis).** **PostgreSQL = 원본(SSOT).** 전역 일관 데이터는 **리전 간 복제/sync**(원본 → 리전 복제본), 리전 로컬 데이터(audit·in-flight queue)는 리전 전용. **Redis = 빠른 조회 캐시(리전마다).** Redis끼리 직접 복제하기보다 **각 리전이 로컬 PostgreSQL에서 캐시(cache-aside)** 하고 **TTL·`mapping_version`으로 무효화**해 일관성을 맞춘다(멱등 키·nonce 같은 휘발 상태는 리전 Redis 로컬). 즉 일관성의 근거는 _PostgreSQL 복제 + 캐시 무효화_ 다.
- **전역데이터 복제 토폴로지 세부**(원본 primary 위치·단일 vs multi-primary·충돌 처리)는 gw/1.2 설계 결정(Appendix B #15)이나, 위 **"PostgreSQL 원본+리전 복제 / Redis 리전 캐시" 모델과 "전역 일관/리전 로컬" 구분 원칙은 버전과 무관하게 고정**이다.

> **GW는 AWS에만 배포한다(2026-06-25 결정).** 비AWS·private GW 배포는 없다 — **AWS 미지원 국가도 별도 GW 없이 가장 가까운 AWS 리전 GW에 접속**(GeoDNS). 그 국가의 데이터 주권용 storage(MinIO 등)는 **Provider(CleverSpace/AXS)가 제공·GW는 presigned 중계만**(GW storage 비호스팅, §7.4·§3.1.2). 배포·NAT·EIP·GeoDNS 구성은 **인프라(③-I)** 소유이며, 본 SRS는 _GW가 전제하는 요구_ 만 기술한다(§3.1·§7.3.5·§2.6).

## 2.2 Overall System Configuration (전체 시스템 구성)

ARD §3·§4의 **3-Plane(Control / Data / Integration)** 구성을 따른다. 컴포넌트 도출 기준 = _plane(책임 영역) + 배포 단위_. **본 도는 §2.1과 같은 그림에서 GW 쪽을 확대한 것**이며(외부 시스템은 §2.1과 동일), GW를 **GW core + Webhook Ingress** 두 부분으로 나눈다.

```mermaid
flowchart LR
    %% 외부 시스템 — §2.1과 동일 (VatechAPIGateway 바깥은 §2.1과 완전히 같음: 그룹핑·노드 동일)
    subgraph CLINIC["클리닉 온프레미스"]
        CO["CleverOne"]
        EZ["EzServer (Edge) = GW 관점의 '디바이스'"]
        DEV["영상장비 CT/Xray<br/>(GW 비대상 · EzServer 뒤)"]
    end
    subgraph UP["연동 서비스 (GW upstream · target-routed proxy, ADR-11)"]
        subgraph INT["내부 — B 프로파일 (우리 서비스·내부망)"]
            CS["CleverSpace (멀티 Region)"]
            CLAB["CleverLab"]
            OID["OneID"]
        end
        subgraph EXT["외부 — C 프로파일 (제3자·OAuth·고정 egress IP)"]
            AXS["Straumann AXS"]
        end
    end
    R53["Route 53 GeoDNS"]
    CONSOLE["GW Console (③-C)"]

    subgraph GWBOX["VatechAPIGateway (§2.1 GW를 확대 — 두 부분)"]
        subgraph CORE["GW core"]
            subgraph CTRL["Control Plane (글로벌, soft-state)"]
                AUTH["Auth Service"]
                OIDI["OneID Integration"]
                ROUTER["Router / PEP<br/>(target-routed proxy)"]
                RGN["Region Resolver"]
                COMPAT["API Compatibility Gate"]
                ADM["Admin API / RBAC"]
                DREG["EzServer Registry / Lifecycle"]
                ENR["Enrollment"]
                CFG["Config"]
                FLEET["Fleet Ops"]
                OPA["Policy (OPA)"]
                AUD["Audit"]
            end
            subgraph DATA["Data Plane (리전 한정) — GW 비호스팅"]
                DNOTE["(GW 데이터 plane 컴포넌트 없음)<br/>presigned 발급·storage는 upstream(CleverSpace/AXS), GW는 중계"]
            end
            subgraph INTEG["Integration Plane"]
                CONN["Connector Framework<br/>(egress·OAuth)"]
            end
        end
        subgraph WHTIER["Webhook Ingress (Webhook Receiver → SQS → Webhook Dispatcher)"]
            WH["Webhook Receiver<br/>검증·멱등·ACK·적재"]
            SQSQ["내부 큐 A·SQS<br/>(재시도·DLQ)"]
            DISP["Webhook Dispatcher<br/>SQS consumer·별도 Deployment<br/>대상 해석·publish (ADR-12)"]
            WH --> SQSQ
            SQSQ --> DISP
        end
    end

    %% API 호출 — 대상 무관 동일 경로(target-routed proxy). 차이는 trust profile뿐
    CO --> EZ
    DEV --> EZ
    EZ -->|"API 요청 (상행)"| COMPAT
    EZ -.->|"머신 인증 (디바이스=EzServer)"| AUTH
    OIDI -->|"인증 연계 (B·내부)"| OID
    ROUTER -->|"프록시 (B·내부)"| CS
    ROUTER -->|"프록시 (C·외부)"| AXS
    ROUTER -.->|"외부(C) 시 OAuth·고정 egress IP"| CONN
    %% GW core 요청 파이프라인(PEP 체인) — 인증→호환성→라우터→(외부면 connector)→upstream, region·정책 참조
    COMPAT -->|"게이트 통과 → 라우팅"| ROUTER
    ROUTER -.->|"region 해석 참조"| RGN
    ROUTER -.->|"정책 판정(PEP)"| OPA
    %% CleverLab은 프록시 대상 아님 — 갈래B 클라우드 클라이언트(보류): CleverLab→GW→AXS
    CLAB -.->|"갈래B 보류: CleverLab→GW→AXS"| ROUTER
    CONSOLE -.-> ADM
    R53 -.-> RGN

    %% Webhook(이벤트 인바운드)은 API 호출과 별개 — 현재 AXS만. 클라우드 수신=CleverLab만(갈래B 보류), CleverSpace는 대상 아님(§2.3.6)
    AXS ==>|"Webhook 인바운드"| WH
    DISP ==>|"MQTT (하행·IoT Core)"| EZ
    DISP ==>|"HTTP push (갈래B·보류)"| CLAB

    %% 색 위계: 연두(GW 범위) > 연파랑(GW core·Webhook Ingress) > 흰카드+파란테두리(우리 컴포넌트) · 회색(managed: SQS·DB)
    style GWBOX fill:#e8f5e9,stroke:#66bb6a,stroke-width:3px
    style CORE fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style WHTIER fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    style CTRL fill:transparent,stroke:#90caf9
    style DATA fill:transparent,stroke:#90caf9
    style INTEG fill:transparent,stroke:#90caf9
    classDef comp fill:#ffffff,stroke:#1565c0,stroke-width:1.5px,color:#0d47a1
    classDef mgd fill:#eceff1,stroke:#90a4ae,color:#37474f
    class AUTH,OIDI,ROUTER,RGN,COMPAT,ADM,DREG,ENR,CFG,FLEET,OPA,AUD,CONN,WH,DISP comp
    class SQSQ,DNOTE mgd
```

**색 범례** (§2.1과 동일):

```mermaid
flowchart TD
    A["GW 범위"]:::scope
    B["GW core / Webhook Ingress"]:::box
    C["우리가 만드는 컴포넌트"]:::comp
    D["managed 인프라·데이터"]:::mgd
    E["외부 (비대상)"]:::ext
    classDef scope fill:#e8f5e9,stroke:#66bb6a,stroke-width:3px,color:#1b5e20
    classDef box fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#0d47a1
    classDef comp fill:#ffffff,stroke:#1565c0,stroke-width:1.5px,color:#0d47a1
    classDef mgd fill:#eceff1,stroke:#90a4ae,color:#37474f
    classDef ext fill:#ffffff,stroke:#bbbbbb,color:#555555
```

> **프록시 복원력(타임아웃·재시도·서킷 브레이커)의 위치**: 별도 공유 컴포넌트가 아니라 **`ROUTER`(외부 C는 `CONN`)의 데이터 경로 안 in-process 행위**다(§7.5.4) — 다이어그램에 새 박스를 두지 않는다. **런타임 상태(서킷 open/closed·실패 카운터)는 pod-local 메모리이며 GW pod 간 공유하지 않는다**(DB·Redis 미사용). 각 pod가 _자기가 관측한_ 실패로 자신을 보호하는 것이 표준(Resilience4j·Envoy outlier detection)이고, 매 요청 hot-path에 원격 상태 왕복을 두면 "빠른 실패" 목적과 모순된다. **공유 대상은 설정뿐**(임계·타임아웃 = `upstream_registry`(DB), pod별 캐시). upstream이 실제 죽으면 각 pod가 독립적으로 곧 트립하므로 상태 공유가 불필요하다.

> **그리는 규칙**: §2.2는 §2.1과 같은 그림에서 **GW 쪽만 확대**한 것이다 — **VatechAPIGateway 바깥(외부 시스템·엣지)은 §2.1과 동일**, 안쪽을 **`GW core`(Control/Data/Integration plane) + `Webhook Ingress` 두 부분**으로 펼친다. 각 외부는 GW 내부 컴포넌트와 **1개 이상 연결**(가장 깔끔하게 1개), **요청 처리 파이프라인(PEP 체인)은 연결**한다 — `COMPAT→ROUTER`(호환성 게이트 통과→라우팅), `ROUTER⇢RGN`(region 참조)·`ROUTER⇢OPA`(정책 판정)·`ROUTER⇢CONN`(외부 C). 반면 순수 **cross-cutting/관리 컴포넌트**(EzServer Registry·Enrollment·Config·Fleet·Audit)는 거의 모든 흐름이 닿아 가독성을 위해 **미연결**(외부와의 특정 연결만 표기: CONSOLE→ADM·R53→RGN). (**예외**: CleverOne은 §2.1처럼 **EzServer를 경유**해 GW에 닿으므로 GW 내부 컴포넌트에 직접 연결하지 않는다 — `CO→EZ→GW`.) **API 호출은 대상 무관 동일 경로**(`ROUTER` = target-routed proxy, ADR-11) — CleverSpace·OneID = B(내부 프록시 대상), AXS = C(외부, `ROUTER`가 `CONN`으로 OAuth·고정 egress IP 추가). **CleverLab은 프록시 대상이 아니라 갈래B 클라우드 클라이언트**(CleverLab→GW→AXS, 보류) — GW를 _호출하는_ 쪽이다. **Webhook(이벤트)만 별개** — 현재 AXS만 GW로 발신; 클라우드 수신 대상=**CleverLab만**(갈래B 보류), **CleverSpace는 webhook 대상 아님**(§2.3.6). 수신→분배 런타임은 **§2.3.6**이 정본.

> **🔍 대안 검토 — 디바이스 인증 방식** (ADR-01)
>
> - 채택안: DPoP + 하드웨어 키(SE/TPM)
> - 대안: mTLS — 10만대 운영 부담·물리 키추출 위협 미해결로 반려
> - 상세·재검토 조건: ARD ADR-01. (본 SRS는 결정을 참조하며, 핵심 결정 로그는 Appendix A)

> 핵심 아키텍처 결정은 ARD ADR-01~10에 확정. 본 SRS는 이를 참조하고 Appendix A에 결정 로그로 연결한다.

## 2.3 Overall Operation (전체 동작방식)

GW의 주요 동작을 **시나리오별 개요(overview)** 로 정리한다. 본 절은 흐름의 골격만 보이며, **상세 시퀀스·예외·재시도 정책은 ARD §5가 정본**이다. 전체 시스템 맥락은 §2.1(제품 조망)·§2.2(3-Plane 구성)을, 단계별 아키텍처 배경은 [개발 Roadmap 결정 §2.6 (배경)](https://vks.vatech.com/x/r9iSEg)을 참조한다.

시퀀스의 참여자(액터)는 §2.1 외부 시스템·§2.2 컴포넌트와 일치한다.

> **(스코프) 운영자/Console 인증 흐름(로그인 화면·세션·토큰 refresh·RBAC UI)은 본 절에 정의하지 않는다** — Console UI는 **③-C GW Console Sub-SRS**, 인증은 **OneID(OIDC) 위임**(§2.3.1·§7.1·ADR-08), GW는 **OneID 토큰 검증 + 관리 API RBAC**(§7.9)만 소유한다(토큰 발급·refresh의 권위는 OneID이지 GW가 아니다).

| 액터 | 의미 (출처) |
| --- | --- |
| EzServer(Edge=GW '디바이스') / CleverOne | 사내·현장 호출자(§2.1·§2.5). EzServer는 방화벽 뒤 Edge·GW 관점의 '디바이스'(§1.4); CleverOne은 EZ 경유. 물리 영상장비는 EzServer 뒤(GW 비대상) |
| GW | 본 SRS 대상. 내부 컴포넌트(Auth·Region Resolver·Connector·Webhook Receiver·내부 큐(A·SQS)·Webhook Dispatcher(§7.6.7)/MQTT(B))는 §2.2 |
| OneID / CleverSpace / CleverLab | 우리 클라우드 백엔드(§2.1) |
| Straumann AXS / AXS S3 | 외부 플랫폼·외부 스토리지(§2.1, 경로③·§4.1.4) |
| upstream storage(S3/MinIO) | CleverSpace·AXS 등 **발급 주체 소유** 객체 스토리지 — presigned 직접 업로드 대상(§4.1.4·§7.4) |

> **본 절 시나리오 ↔ §7 기능·§4.1.4 경로 매핑**: 온보딩(§7.2)·인증(§7.1)·리전(§7.3)·파일 업로드 경로②(§7.4·§4.1.4②)·외부 연동 경로③(§7.5·§4.1.4③)·Webhook(§7.6·§4.1.3)·버전 호환(§7.7).
>
> **API 호출 경로는 대상 무관 동일**(`…→GW→upstream` target-routed proxy, ADR-11): CleverSpace(B 내부)·AXS(C 외부)는 **같은 경로**이고 trust profile만 다르다(C는 OAuth·egress 추가). 그래서 **§2.3.5(외부 연동)는 CleverSpace에도 그대로 적용되는 일반 proxy 흐름**이며, AXS를 예로 들었을 뿐 GW 동작은 동일하다. CleverSpace presign(경로②)에 **별도 시나리오를 두지 않는 이유는 경로가 달라서가 아니라**, 그 계약이 GW 밖(② One Pager·CleverSpace OpenAPI)에 있고 GW는 verbatim bypass(B)만 하기 때문이다(§4.1.4②).

### 2.3.1 온보딩 — 클리닉/클라이언트 등록 + EzServer enrollment — FR-RGN-\* · FR-ENR-\*

온보딩은 두 단계다: (1) **클리닉/클라이언트 등록**(EzServer가 LMP Clinic-ID 수신 시 **자동·무조건** GW 등록, 매핑 자가 생성) → (2) 그 클리닉의 **디바이스 enrollment**(머신 신뢰 부트스트랩). 분배 매핑(clinic→region·Org-ID)은 **Admin이 일일이 넣지 않고 온보딩 시 자연히 채워지며**, Admin은 잘못된 것의 **교정(override, FR-RGN-04)** 만 한다.

#### (1) 클리닉/클라이언트 온보딩·리전 등록

클리닉 등록은 **자동·무조건**이다(2026-06-25 결정). **EzServer 설치 후 LMP로부터 Clinic-ID를 받는 순간 EzServer가 그 Clinic-ID를 GW로 전송해 자동 등록**한다 — **외부 연동(AXS 등) 여부와 무관하게 모든 클리닉이 GW에 등록**된다(연동 안 해도 무조건). GW는 Clinic-ID·region을 **검증(allowlist·정책)** 후 `clinic_region_mapping`·`delivery_channel`에 저장한다(이 클리닉이 어느 region인지·webhook을 어디로 보낼지 확정). **등록 주체 = 클리닉당 1개인 EzServer로 확정** — 클리닉은 **CleverOne 다수 + EzServer 1개**라 EzServer 자동 등록이 자연스럽다(기존 CleverOne 대안 TBD 종결, Appendix B #17). **외부 연동을 켤 때만** 그 provider의 Org-ID(Straumann 온보딩에서 발급, §2.3.5·④)를 등록하면 `org_mapping`에 (provider, Org-ID)→clinic이 채워져 webhook 분배 대상이 결정된다. **region은 운영 중에도 EzServer Console에서 변경 가능**(FR-RGN-04·§7.3.4 재동의·감사) — 선택지는 `GET /v1/regions`(§7.3.6)로 제공. Admin은 잘못된 등록의 **교정(override)** 만.

> **C/S 등록 확인.** 등록은 EzServer가 자동으로 하지만, 클리닉 설치를 담당한 **C/S(현장 설치 담당)는 설치 후 GW Console에서 해당 클리닉이 정상 등록됐는지 확인**한다. 따라서 **GW Console 사용자는 Admin + C/S 역할**을 갖는다(§7.9.2) — **확인 UI·역할 세부 권한은 ③-C GW Console Sub-SRS**에서 정의(본 SRS는 등록 조회 API·역할 존재까지).

```mermaid
sequenceDiagram
    autonumber
    participant LMP as LMP
    participant EZ as EzServer (클리닉당 1개)
    participant GW as GW (Onboarding/Region)
    participant DB as 전역 매핑 DB
    LMP-->>EZ: Clinic-ID 발급/전달
    EZ->>GW: Clinic-ID 자동 등록 (무조건 · 외부 연동 무관)
    GW->>GW: Clinic-ID·region 검증(allowlist·정책)
    GW->>DB: clinic_region_mapping · delivery_channel 저장
    GW-->>EZ: 등록 완료 (이 클리닉 = 해당 region)
    Note over EZ,DB: 외부 연동(AXS) 연결 시에만 provider Org-ID 등록 → org_mapping (§2.3.5·④)
    Note over GW,DB: 자동·무조건 등록(2026-06-25). Admin은 교정만(override, FR-RGN-04)
    Note over LMP,GW: 등록 주체 = EzServer 확정(클리닉당 1회). region 변경=EzServer Console(§7.3.4)
```

#### (2) EzServer enrollment

신뢰할 수 없는 EzServer(디바이스, §1.4)를 부트스트랩 신뢰(공장 토큰/OOB 일회 코드)로 검증해 allowlist에 등록하고 자격을 발급한다. nonce challenge로 replay를 막고, 머신 fingerprint를 바인딩한다(등록된 클리닉 소속). 상세는 §7.2.5·§7.2.6, 흐름은 ARD §5.1.

```mermaid
sequenceDiagram
    autonumber
    participant D as EzServer (디바이스)
    participant GW as GW (Enrollment)
    participant AUD as Audit
    D->>GW: POST /v1/enroll/start (bootstrap)
    GW->>GW: 부트스트랩 신뢰 검증 · nonce 발급
    GW-->>D: nonce challenge
    D->>D: nonce 서명 · fingerprint 산출
    D->>GW: POST /v1/enroll/complete (nonceSignature, fingerprint)
    GW->>GW: 서명·fingerprint 검증 · allowlist 등록 · 자격 발급(KMS secretRef)
    GW->>AUD: 등록 이력 append-only 기록
    GW-->>D: Credential (clientId, secretRef)
    Note over D,GW: 신뢰 검증 실패·만료/재사용 토큰 → 거부(§7.2.5)
```

### 2.3.2 EzServer(디바이스) 인증·토큰 발급 — FR-AUTH-01/05

등록된 EzServer(디바이스, §1.4)가 작업 전 단명 access token을 발급받는다. lifecycle·allowlist를 확인하고, claim(`deviceId`·`region`·`aud`·`TTL`)을 강제 바인딩한다. revoked 디바이스는 캐시 TTL과 무관하게 즉시 차단(§7.2.4). **갱신은 refresh token이 아니라 동일 `client_credentials` 재발급**으로 처리한다(§7.1.1 — 단명+즉시 revocation 모델). 상세는 §7.1.1.

```mermaid
sequenceDiagram
    autonumber
    participant D as EzServer (디바이스)
    participant GW as GW (Auth)
    loop access token 만료 시 (refresh token 미사용)
        D->>GW: POST /v1/auth/token (clientId/secret, scope)
        GW->>GW: allowlist·lifecycle 확인(§7.2) · secret 검증
        GW->>GW: claim hard binding (deviceId·region·aud·TTL)
        GW-->>D: access token (단명, Unix ms 만료)
    end
    Note over D,GW: 미등록/revoked → 거부 · secret 불일치 → 401 · scope 초과 → 403
    Note over D,GW: 갱신 = 동일 client_credentials 재발급 (refresh_token grant 미도입, §7.1.1)
```

### 2.3.3 리전 해석·라우팅 — FR-RGN-\*

인증된 호출자가 작업(업로드·연동) 직전 device/clinic→region을 해석해 리전 endpoint와 주권 정책을 받는다. `deviceId`·`clinicId`는 동일 resolver가 같은 리전으로 귀결(ADR-10)한다. PHI는 해석된 리전 밖으로 이동하지 않는다(OPA, §7.3.3). 상세는 §7.3, 흐름은 ARD §5.2.

```mermaid
sequenceDiagram
    autonumber
    participant C as 호출자 (Device/EZ)
    participant GW as GW (Region Resolver)
    participant R as Redis 캐시
    C->>GW: GET /v1/region/resolve?deviceId|clinicId
    GW->>R: 매핑 조회 (TTL)
    alt 캐시 히트
        R-->>GW: region · mappingVersion
    else 캐시 미스
        GW->>GW: strong-consistency 경로 폴백 · 캐시 갱신
    end
    GW-->>C: region endpoint + 주권 정책
    Note over C,GW: 매핑 부재 → 거부 · PHI 리전 경계 OPA 집행(§7.3.3)
```

### 2.3.4 파일 업로드 — presigned 중계 (CleverSpace 경로②) — 발급=CleverSpace

**GW는 presigned를 발급하지 않는다.** 디바이스/EzServer의 대용량 파일(CT·영상)은 **CleverSpace가 발급한 presigned**로 **CleverSpace storage에 직접** 업로드하고, GW는 발급 요청을 **중계(B bypass)** 만 한다(경로②, §4.1.4). 업로드 **세션·resumable·멱등·무결성·완료처리는 CleverSpace 책임**(② Presigned One Pager·CleverSpace OpenAPI 정본) — GW는 소유·서명하지 않는다. AXS 파일은 경로③(§2.3.5). 상세는 §7.4.

```mermaid
sequenceDiagram
    autonumber
    participant EZ as EzServer/디바이스
    participant GW as GW (proxy·중계)
    participant CS as CleverSpace (presign 발급·storage 소유)
    participant S3 as CleverSpace storage (S3/MinIO)
    EZ->>GW: presigned 발급 요청 (Vatech-Target cleverspace · B bypass)
    GW->>GW: 인증·버전 게이트·정책 (body 변환 없음)
    GW->>CS: verbatim 중계
    CS-->>GW: presigned URL (CleverSpace 발급)
    GW-->>EZ: presigned URL 전달 (GW 변환 없음)
    EZ->>S3: 파일 바이트 직접 업로드 (GW 미경유)
    Note over EZ,S3: 세션·완료처리(콜백+ObjectCreated)·무결성은 CleverSpace 책임(② One Pager). GW는 발급 중계만, 서명·세션 없음
```

### 2.3.5 외부 연동 — AXS presign·파일 bypass (경로③, 갈래 A) — FR-INT-\*

**§4.1.4 경로③ 전용 (C 프록시).** EzServer→AXS 외부 연동(5단계 갈래 A). 클라이언트는 `Vatech-Target: axs`를 실어 AXS 경로를 **그대로** 호출하고(§4.1.2), GW는 connector로 OAuth2 토큰을 관리(§7.1.3)·egress allowlist를 집행(§7.5.3)하되 요청/응답 body는 **AXS OpenAPI 그대로 통과(verbatim bypass)** 한다 — GW가 발급하거나 해석·변환하지 않는다. 대용량은 AXS가 발급한 presigned로 **AXS S3에 직접** 업로드(GW 미경유). 연동 의미·Org-ID 매핑 상세는 **④ Sub-SRS**, 본 SRS는 프레임워크·egress까지만. 상세는 §7.5.

> **경로 동일성**: 본 흐름(`EZ→GW→upstream`)은 **CleverSpace(B 내부)도 동일**하다(ADR-11 target-routed proxy). AXS(C 외부)는 GW가 **OAuth·고정 egress IP**를 추가할 뿐 경로·중계 방식은 같다. 즉 본 시나리오는 AXS를 예로 든 *일반 upstream proxy*이며, CleverSpace는 `Vatech-Target: cleverspace`로 같은 경로를 탄다(차이는 trust profile뿐).

```mermaid
sequenceDiagram
    autonumber
    participant EZ as EzServer (Edge)
    participant GW as GW (Connector)
    participant AXS as Straumann AXS
    participant AS3 as AXS S3 (외부)
    EZ->>GW: POST {AXS 경로 verbatim} (Vatech-Target: axs · 정보·Create Document)
    GW->>GW: Vatech-Target allowlist→host 해석 · OAuth2 토큰 확보·갱신(§7.1.3) · egress allowlist 검증(§7.5.3)
    GW->>AXS: host만 교체해 verbatim 전달 (body 그대로)
    AXS-->>GW: presigned URL (AXS 발급)
    GW-->>EZ: presigned URL 전달 (GW 변환 없음)
    EZ->>AS3: 대용량(영상) 직접 업로드 (GW 미경유)
    Note over GW,AXS: Vatech-Target 누락 → 400 · 미등록/allowlist 외 → 거부(403/404) · 외부 스키마는 ④/AXS 스냅샷 정본
```

### 2.3.6 Webhook 수신·분배 — FR-WH-\*

외부(AXS)가 **provider별 전용 호스트**(`axs.webhook.gw.vatech.com`)로 이벤트를 push하면, GW가 **Host/SNI로 발신자를 식별**(→그 provider의 시크릿 선택)하고 **HMAC·timestamp 검증·eventId 멱등** 후 즉시 ACK하고 대상별로 분배한다(store-and-forward, ADR-09). 클라우드는 HTTP push, 방화벽 뒤 Edge(EzServer)는 MQTT QoS1 역방향. **발신자 식별은 수신 호스트(우리가 통제)로, 목적지(분배 대상)는 Org-ID↔ClinicID 매핑(§7.3)으로** 결정한다 — 둘 다 송신 source IP에 의존하지 않으며, **Host는 식별이지 인증이 아니다**(인증=HMAC). 수신 계약은 A면(GW 고유 API), payload는 외부 참조(§4.1.3). 상세는 §7.6.

```mermaid
sequenceDiagram
    autonumber
    participant AXS as Straumann AXS
    participant WH as GW (Webhook Receiver)
    participant Q as 내부 큐(A·SQS)
    participant DISP as Webhook Dispatcher (SQS consumer·ADR-12)
    participant CL as 클라우드 대상 (CleverLab·갈래B 보류)
    participant EZ as EzServer (Edge, 방화벽 뒤)
    AXS->>WH: POST https://axs.webhook.gw.vatech.com/{provider 규약 경로} (HMAC·timestamp·eventId)
    WH->>WH: Host/SNI로 provider 식별→시크릿 선택 · HMAC·timestamp 검증(IP 옵션) · eventId 멱등 dedup
    WH-->>AXS: 2xx ACK (즉시)
    WH->>Q: 적재 (재시도·백오프·DLQ)
    DISP->>Q: pull (consume)
    DISP->>DISP: 대상 해석(org_mapping→clinic→region→delivery_channel, §7.3)
    par 클라우드 대상 = CleverLab만 (갈래B 보류)
        DISP->>CL: HTTP push (내부망)
    and Edge 대상 (갈래A 역방향, b1)
        DISP->>EZ: MQTT QoS1 publish (IoT Core · EZ outbound 구독)
    end
    Note over WH,EZ: 미등록 Host/provider → 404 · 인증(HMAC) 실패 → 401 · 식별=수신 Host / 목적지=매핑(§7.3)
    Note over Q,CL: 현 v1.0 구체 대상=EzServer(b1). 클라우드 수신=CleverLab만(갈래B 보류) · CleverSpace는 대상 아님(아래 표·§7.6.5)
```

#### 분배 대상별 시나리오 (어느 서버가 어떤 Webhook을 받나)

Webhook은 **외부 서비스(현재 AXS)가 보낸 이벤트**를 GW가 받아, 그 이벤트가 향하는 **내부 대상**으로 분배한다(대상은 Org-ID↔ClinicID 매핑, §7.3). 대상별 시나리오·메커니즘·현 상태는 다음과 같다. **불명확한 항목은 TBD로 두어 추후 조사·확정한다.**

| 분배 대상 | 어떤 이벤트를 받나(시나리오) | 메커니즘 | 현 상태 |
| --- | --- | --- | --- |
| **EzServer (Edge)** | 클리닉의 AXS 연동(**갈래 A**) **역방향** — 그 클리닉의 환자·파일·오더 상태 등 AXS가 통지하는 결과를 방화벽 뒤 EzServer로 | **MQTT QoS1**(EZ outbound 구독) | **역방향 capability는 b1(v1.0)에 포함**(WH-06·ARD v0.9·§7.6.6). 단 갈래 A의 _데이터_ 1차 범위는 EZ→AXS 단방향이며, **TBD — 역방향으로 보낼 대상 이벤트 목록·활성화 세부는 ④ Sub-SRS에서 확정**(Roadmap §3.7.1) |
| **CleverLab (클라우드)** | 기공소 주문 연동(**갈래 B**) — Straumann Scan SW→AXS로 들어온 **기공 오더 전송·확정 결과**를 CleverLab로 | **HTTP push**(내부망) | **갈래 B — 현 시점 범위 외(보류, §1.2).** **TBD — 갈래 B 활성화 여부·시점 확정 필요**(PM/제품). 활성화 시 받을 이벤트(오더·확정 결과)는 ④ |
| **CleverSpace (클라우드)** | **해당 없음 — CleverSpace는 Webhook 수신 대상이 아니다**(B 프록시·presigned 백엔드일 뿐, AXS 이벤트 수신처 아님) | — | **N/A (확정).** 클라우드 webhook 수신은 CleverLab만(갈래 B). 결정 2026-06-23 |

> 정리: **현 v1.0의 _구체적_ 분배 대상은 EzServer(갈래 A 역방향)** 가 핵심이고, **클라우드 수신 대상은 CleverLab만(갈래 B·보류)** 이다. **CleverSpace는 webhook 수신 대상이 아니다**(B 프록시·presigned 백엔드). 즉 "클라우드 HTTP push"는 *메커니즘*이고 그 수신처는 **CleverLab**이며, 활성화는 갈래 B 결정에 달려 있다. AXS 이벤트 종류(patient/file/lab-order)·대상 매핑 상세는 **④ Sub-SRS**. (갈래 B 활성화 등 미결은 Appendix B 추적)

### 2.3.7 버전 호환 게이팅 — FR-COMPAT-\*

`Vatech-*` 헤더로 originator(요청 시작 주체)와 경유 홉(`Vatech-Via`)을 분리 판정하고, well-known 공시·호환성 매트릭스와 대조해 **더 낮은 버전 기준**으로 게이팅한다. 미지원이면 표준 오류코드와 "업데이트 필요" fallback을 안내해 원인불명 실패를 제거(ADR-07)한다. 상세는 §7.7.

```mermaid
sequenceDiagram
    autonumber
    participant CO as CleverOne (originator)
    participant EZ as EzServer (경유 홉)
    participant GW as GW (Compat Gate)
    participant CS as CleverSpace
    CO->>EZ: 요청 (Vatech-Product/Version/OS)
    EZ->>GW: 전달 (+ Vatech-Via: EzServer)
    GW->>GW: originator vs Via 분리 판정 · well-known/매트릭스 대조(최저 버전 기준)
    alt 지원 버전
        GW->>CS: 정규화 신원으로 통과
        CS-->>GW: 응답
        GW-->>CO: 정상 응답
    else 미지원 버전
        GW-->>CO: 표준 오류 + "업데이트 필요" fallback
    end
    Note over GW: 공시 경로 /.well-known/{env}/server-configuration.json (§7.7.2)
```

## 2.4 Product Functions (제품 주요 기능)

> 7장 대분류와 1:1 매핑.

- 7.1 인증·토큰 (EzServer 머신 인증 + OneID 연계)
- 7.2 EzServer(디바이스) 레지스트리·온보딩
- 7.3 리전·라우팅·주권 (라우팅 키 통합)
- 7.4 파일 업로드 — presigned 중계(GW 비발급)
- 7.5 외부 연동·Connector 프레임워크
- 7.6 Webhook 수신·이벤트 분배
- 7.7 API 버전 호환성 게이트
- 7.8 Fleet 운영·Config
- 7.9 관리·감사·컴플라이언스

## 2.5 User Classes and Characteristics (사용자 계층과 특징)

| 계층                            | 사용 빈도 | 주 사용 기능                              | 권한                 | 중요도 |
| ------------------------------- | --------- | ----------------------------------------- | -------------------- | ------ |
| EzServer(디바이스, §1.4)        | 상시      | 인증·파일 업로드(upstream presign)·config | 머신(디바이스 scope) | 핵심   |
| 사내 호출자(EzServer/CleverOne) | 상시      | 인증·라우팅·Webhook 수신                  | 서비스(OneID)        | 핵심   |
| 외부 플랫폼(AXS)                | 이벤트 시 | Webhook·connector                         | 외부(OAuth2)         | 핵심   |
| 운영자/Admin                    | 일/주     | 관리 API·매핑·kill-switch                 | RBAC                 | 중요   |
| 인프라/DevOps                   | 배포 시   | IaC·관측·로그                             | 시스템               | 중요   |

## 2.6 Assumptions and Dependencies (가정과 종속 관계)

- **AXS sandbox 자격증명·OAuth Client** — Straumann 제공 대기. (미수령 시 영향: §7.5 connector E2E·④ Sub-SRS 검증 지연)
- **GW 인프라(K8s·Route 53 GeoDNS·고정 egress IP 집합·DNS 호스트)** — 인프라 담당 별도. 본 SRS는 계획·요구만 기술. (미확정 시 영향: §3·§4.5·§7.3). **고정 egress IP는 단일 IP가 아니라 AZ/리전별 NAT의 고정 EIP 집합**(멀티 서버·멀티 리전)이며, AXS는 그 **합집합을 whitelist**한다 — 오토스케일·새 AZ·리전 증설로 _whitelist에 없는_ egress IP가 생기지 않게 EIP 풀로 핀(pin)하고 증설 시 Straumann과 협의·갱신(§2.1.1).
- **MQTT 브로커 운영 주체** — TBD (미결 이유: 운영 조직 미정 / 책임자 ❓ / 마감 ❓ / 영향: §7.6·ARD MQTT Broker)
- **CleverOne SRS(Nick)** — 클라이언트 식별 헤더 상세. 미확보 시 §7.7 정밀화 제약.

## 2.7 Apportioning of Requirements (단계별 요구사항)

| 버전 | 범위 | Roadmap 단계 |
| --- | --- | --- |
| gw/1.0 (MVP) | 인증 코어·레지스트리·enrollment·단일 리전 주권·presigned 중계·AXS connector·fleet 기본·config·감사/RBAC(경량)·Webhook·COMPAT·라우팅 키 통합 | 1·2·3·(4 일부)·5 |
| gw/1.1 | DPoP+HW키·hardware attestation·fleet 확장·2nd connector | 후속 |
| gw/1.2 | 멀티 리전 활성화(Aurora Global DB·GeoDNS N리전, §2.7.1) | 4단계(후행 시) |
| v2.0 | 레거시 10만대 마이그레이션 | 후속 트랙 |

### 2.7.1 리전 구축 단계화 — 단일(1차) → 멀티(2차), 단 v1.0부터 멀티리전-ready

**리전 구축은 2단계다 — 1차 단일 리전(gw/1.0) · 2차 멀티 리전(gw/1.2).** v1.0은 **단일 리전만 실제 배포**한다(멀티 리전 동시 운영·active-active·다중 signer는 v1.0 범위 밖, FR-RGN-05). 단, **v1.0부터 "멀티리전-ready"로 설계**하여 2차 확장이 _재설계·데이터 마이그레이션 없이 설정·배포 증분_(리전 수 1→N)으로 가능해야 한다. 이 "단일로 시작하되 멀티로 자라는" 설계는 **v1.0의 요구사항**이다(결정 — Appendix A, 2026-06-23. 기존 "gw/1.0 흡수 여부 TBD"를 대체).

**멀티리전-ready 설계 요건 (v1.0 단일 리전에서도 미리 갖춘다):**

| 요소 | v1.0(단일 리전)에서 미리 갖출 것 | 2차(멀티) 확장 시 |
| --- | --- | --- |
| **데이터 모델** | 전역 일관 vs 리전 로컬 분리(§2.1.1·§6.4), `region`·`mapping_version`·ClinicID↔region 키 보유(값은 단일 리전) | 매핑 행 추가 — 스키마 변경 없음 |
| **Region Resolver** | device/clinic→region resolver를 v1.0부터 경유(단일 리전으로 해석, ADR-10·§7.3.1) | resolver 매핑만 확장 |
| **DNS** | **GeoDNS apex 호스트를 v1.0부터** 사용(단일 리전을 가리킴), 클라이언트는 apex만 호출 · 리전별 호스트는 예약(§4.5.1) | **클라이언트 변경 없이** GeoDNS 라우팅만 활성화(§7.3.5) |
| **egress** | NAT EIP **집합** 패턴(§2.1.1) — 단일 리전=1집합 | 집합 합집합 — 외부 whitelist 갱신 |
| **데이터 주권** | PHI 리전 경계 집행을 v1.0부터(OPA, §7.3.3) | 리전별 경계 그대로 적용 |

> **금지**: 단일 리전을 전제한 하드코딩(리전 고정 endpoint·단일 DB 가정·apex 없이 리전 호스트 직접 노출 등)으로 2차에 재작업이 생기지 않게 한다. (presign·storage는 GW 비소유·중계만이라 GW엔 presign broker가 없다 — FR-SES-06 해당 없음, §7.4·§7.4 FR-SES 매핑.)

## 2.8 Backward compatibility (하위 호환성)

GW 본체는 신규 구축이나, **기존 클라이언트(구버전 CleverOne/EzServer)와 경로 B**에 대한 호환 정책이 필요하다.

- 호환 대상: 구버전 클라이언트 — well-known·오류코드 fallback으로 흡수(§7.7)
- 호환 포기: 경로 B는 **Deprecated 후 EOS** (시점 TBD — §2.8, 책임자 ❓, 마감 ❓, 영향: §7.6·① One Pager)
- 호환 매트릭스(클라이언트×API 최소버전): TBD — ① 운영 호환성 매트릭스 확정본 의존

---

# 3 Environment (환경)

## 3.1 Operating Environment (운영 환경)

GW는 **개발(dev) · 테스트(test/staging) · 운영(prod) 3종 환경**으로 분리한다. 본 절(§3.1.1·§3.1.2)은 **운영(프로덕션) 런타임**이 기준이고, **개발 환경은 §3.4·테스트 환경은 §3.5**가 상세를 정의한다. 핵심은 **외부 의존(AXS·EzServer·CleverSpace·OneID·LMP)을 환경별로 실서비스/sandbox/스텁 중 무엇으로 대체하느냐**이며(§3.4 에뮬레이션 전략), **PHI는 운영에서만 실데이터**이고 개발·테스트는 **더미 데이터만** 쓴다(§6.4·§6.5).

> **환경 매트릭스 (차원별 dev / test / prod)**
>
> | 차원 | 개발(dev) | 테스트(test·staging) | 운영(prod) |
> | --- | --- | --- | --- |
> | 목적 | 기능 개발·단위 테스트 | 통합·E2E·부하·인수 | 실서비스 |
> | 배포 | 로컬(컨테이너) + 공유 dev(AWS dev 계정) | AWS staging(운영 유사·축소) | AWS prod(§3.1.2, 단일→멀티 리전 §2.7.1) |
> | DB | 로컬 PostgreSQL / dev RDS 소형 | RDS·Aurora 소형 | **Aurora PostgreSQL**(§3.1.2) |
> | 캐시 | 로컬 Valkey 컨테이너 | ElastiCache 소형 | **ElastiCache for Valkey** |
> | 큐(A)·엣지(B) | 로컬(elasticmq/LocalStack)·로컬 MQTT 브로커 | SQS·MQTT 소형 | **SQS · IoT Core/Amazon MQ** |
> | 스토리지(presigned) | MinIO/S3 dev(발급=스텁) | S3·발급주체 sandbox | S3(발급=CleverSpace/AXS) |
> | **AXS** | **sandbox**(unstable, ESIP-14) / 미수령 시 mock | **sandbox** | **production** |
> | **EzServer(=디바이스·EPI)** | **에뮬레이터/스텁**(실 EzServer는 Rust 재개발 중) | 실 EzServer(가능 시)·또는 스텁 | 실 EzServer |
> | CleverSpace(EzCloud) | **presign 발급 스텁** | sandbox·또는 실 | 실 CleverSpace |
> | OneID | dev 테넌트 / OIDC mock | staging 테넌트 | prod |
> | LMP(Clinic-ID) | 스텁·시드 | staging | prod |
> | PHI 데이터 | **더미만(PHI 금지)** | **더미만** | 실 PHI(주권·consent, §6.5·§7.3.3) |
> | egress 고정 IP | 불요(또는 dev EIP) | sandbox용 EIP(Straumann 협의) | **prod 고정 EIP**(AXS whitelist, §2.1.1·§7.5.3) |
> | 관측·CI | 로컬 로그 | CloudWatch + E2E 게이트(§3.6.2) | full 관측(§6.3.2) |
>
> 환경별 인프라 구축·계정·자격 발급은 **인프라(③-I) 소유**이며 본 SRS는 _GW 개발·검증이 전제하는 환경 요구_ 를 기술한다. 환경 구축 일정·책임은 Appendix B #24.

### 3.1.1 Hardware Environment

서비스(클라우드) — AWS EKS(Kubernetes) 노드. 사양 상세는 인프라 담당 IaC. (TBD: 노드 타입·수)

### 3.1.2 Software Environment

GW가 동작하는 소프트웨어 스택. 근거·전체 표는 [ARD §4.5 기술 스택](<../../VT API Gateway — ARD (아키텍처).md>). 버전 `TBD`는 설계 단계 확정.

> **배포 환경 = AWS 전용(2026-06-25 결정).** GW는 **AWS(EKS)에만 배포**한다 — 비AWS·private GW 배포는 두지 않는다. **AWS 미지원 국가도 별도 GW 없이 가장 가까운 AWS 리전의 GW에 접속**한다(GeoDNS, §7.3.5). 그 국가의 데이터 주권용 storage(MinIO 등)는 **GW가 아니라 Provider(CleverSpace/AXS)가 제공**하고, GW는 presigned를 **중계만** 한다(GW는 storage 비호스팅, §7.4). 상태 저장소·미들웨어는 **AWS 관리형**을 기본으로 하고(HA·백업·패치 위임, 무상태 pod ADR-02), pod→AWS 접근은 **IRSA**로 부여한다(정적 시크릿 미내장). 멀티 리전 데이터 토폴로지는 §2.1.1. 제품·버전 확정은 인프라/설계 단계(③-I·Appendix B #12).

- **언어 / 런타임**: TypeScript · Node.js LTS (버전 TBD)
- **프레임워크**: NestJS (DDD 모듈 · TDD)
- **ORM / 마이그레이션**: **Prisma** (권장 — 아래 근거) · 스키마는 DBML(dev-chain-design)에서 파생
- **관계형 DB**: **PostgreSQL 15.x(엔진 확정)** — **Aurora PostgreSQL 권장**(단일 리전부터; 인프라 비준 TBD Appendix B #18·아래 비교표) / RDS for PostgreSQL. 레지스트리·매핑·토큰메타·정책·감사 저장. 전역 일관 데이터의 리전 간 복제는 **Aurora Global Database**(§2.1.1)
- **캐시**: **Amazon ElastiCache for Valkey**(엔진=Valkey, **Redis 호환**·§1.4 — RESP·클라이언트·키스페이스 동일; Redis OSS 대비 저비용)(리전별·region-local) — region 매핑 TTL·nonce·rate-limit·idempotency·JWKS. **SSOT 아님**(캐시+휘발)·**리전 간 교차복제 안 함**(§2.1.1 — 로컬 PostgreSQL에서 재적재). 키스페이스 정본: `design/redis/redis-keyspace.md`
- **메시지 큐 (A · 내부 비동기 큐)**: **Amazon SQS** 기본(서버리스·IRSA 접근·DLQ 내장, 순서/dedup 필요 시 **SQS FIFO**) / Amazon MQ — **GW 내부** Webhook 비동기 분배·재시도·DLQ(§7.6.3). 엣지(B)와 별개 레그
- **MQTT 브로커 (B · 엣지 전달)**: 방화벽 뒤 Edge(EzServer) 역방향 push(QoS1·persistent, §7.6.6) — 지속 구독 필요(SQS 부적합). 후보 **AWS IoT Core / Amazon MQ**. **제품·운영 주체 TBD**(§2.6·Appendix B #4)
- **오브젝트 스토리지 — GW 비호스팅**: 발급 주체(CleverSpace ②/AXS ③)의 storage이며 GW는 presigned **중계만**(§7.4). AWS 리전=**S3** / **AWS 미지원 국가=Provider 제공 MinIO**(S3 호환). GW는 어느 경우든 발급·호스팅하지 않는다
- **정책 엔진**: **OPA** — 클러스터 내 sidecar/배포. allowlist·region·scope·egress 판단
- **시크릿 / 키 관리**: **AWS KMS · Secrets Manager**(enrollment·PKI는 Vault 검토). pod 주입은 **Secrets Store CSI / External Secrets**(IRSA 연계, 정적 시크릿 미내장)
- **컨테이너 / 오케스트레이션**: Docker · **EKS(Kubernetes)**. 멀티 서버 HA=k8s pod 복제. 이미지 레지스트리 **Amazon ECR**
- **인그레스 / 부하분산**: **AWS LB Controller(ALB/NLB)** — 리전별 **안정 inbound endpoint 1개**(§2.1.1) + **Route 53 GeoDNS**(§7.3.5·§4.5.1). **egress=NAT Gateway 고정 EIP 집합**(AXS whitelist=합집합, §2.1.1·§7.5.3)
- **관측성**: **OpenTelemetry(ADOT)** · 구조화 로그(Pino) → **CloudWatch / Amazon Managed Prometheus·Grafana**. 도구는 여기까지, **로그 구조(필드·상관키·레벨)는 §6.3.2가 정의**(취합·분석은 인프라 소유). PHI·시크릿 미기록(§6.2)
- **API 문서**: `@nestjs/swagger` code-first (`/api-docs`, §1.7.1)

> **DB 선택 근거.** **엔진=PostgreSQL 확정**, 관리형 제품은 **처음부터 Aurora PostgreSQL 권장**(인프라 비준 TBD, Appendix B #18). (1) **전역 일관 데이터(§2.1.1)**: 매핑·레지스트리·정책·JWKS 등 전역 SSOT의 리전 간 저지연 복제를 **Aurora Global Database**가 내장 제공(빠른 failover·스토리지 자동확장)한다 — RDS 교차 리전 읽기복제(비동기·지연·수동 승격)보다 우수. (2) **전환 비대칭성**: 멀티 리전 전환이 Aurora는 Global Database 활성화(마이그레이션 0)인 반면 RDS-first는 RDS→Aurora 플랫폼 마이그레이션(SSOT 컷오버·재검증·CCB)이라 비대칭적으로 비싸 **단일 리전부터 Aurora**를 쓴다 — 통제 제품(IEC 62304) 재검증·IaC 이중구축 회피. (3) **비용**: Aurora는 동급 인스턴스 기준 RDS 대비 **~20% 내외**(I/O·구성 변동) 높으나 저QPS control plane이라 절대 월 비용 차가 작고, 후속 마이그레이션 비용보다 작다. (4) **호환성**: Aurora PostgreSQL은 PostgreSQL 호환이라 Prisma·스키마·쿼리를 그대로 쓴다(일부 확장·최신 마이너 버전 지연 가능 — 저QPS CRUD라 영향 작음).
>
> **Aurora PostgreSQL vs RDS for PostgreSQL (둘 다 관리형 · 엔진은 PostgreSQL)**
>
> | 항목               | RDS for PostgreSQL                              | Aurora PostgreSQL (권장)                                   |
> | ------------------ | ----------------------------------------------- | ---------------------------------------------------------- |
> | 엔진               | 커뮤니티 PostgreSQL **그대로**                  | PostgreSQL **호환**(스토리지만 Aurora)                     |
> | 스토리지           | EBS 단일 볼륨                                   | 분산 스토리지(3-AZ 6중 복제·자동확장)                      |
> | 리전 내 HA         | Multi-AZ 동기 스탠바이 + 읽기복제               | 공유 스토리지 기반 읽기복제 최대 15, 더 빠른 failover      |
> | **교차 리전 복제** | 읽기복제(**비동기·지연 큼·수동 승격**)          | **Aurora Global Database**(저지연 ~1s·빠른 승격·관리형)    |
> | 호환성             | **100%**(모든 확장·버전 즉시)                   | 대부분(일부 확장 미지원·마이너 버전 지연)                  |
> | 비용·단순성        | 낮음·단순                                       | 다소 높음(동급 인스턴스 기준 **~20% 내외**, I/O·구성 변동) |
> | 멀티 리전 전환     | RDS→Aurora **마이그레이션 필요**(재검증·컷오버) | **Global Database 활성화(마이그레이션 0)**                 |
> | 적합               | v1.0 단일 리전(비용 우선 시)                    | **단일→멀티 리전 일관(권장)**                              |
>
> 결론: **엔진=PostgreSQL 확정, 제품=처음부터 Aurora PostgreSQL 권장**(단일 리전부터). RDS-first는 비용이 약간 낮으나(~20% 델타, 저QPS라 절대액 작음) **멀티 리전 시 마이그레이션 비용·재검증이 더 커서 비권장**. 최종 도장은 인프라 비준(Appendix B #18).
>
> **ORM 추천 — Prisma.** 근거: (1) control plane은 저(低) QPS·CRUD 중심(PRD §10)이라 Prisma의 타입 안전·DX 이점이 크고 복잡 쿼리 한계의 영향이 작다, (2) **DBML → Prisma schema**로 이어지는 설계 산출물 흐름과 마이그레이션 일원화에 부합(`design/dbml/`), (3) 사내 NestJS 표준·ARD §4.5에서 이미 `◎ Prisma`로 채택. 대안: TypeORM(NestJS 친화이나 유지보수 리스크)·Drizzle/Kysely(SQL-first·경량이나 배터리 적음)는 _복잡 쿼리·세밀한 SQL 제어가 핵심이 될 때만_ 재검토(결정 변경 시 ADR 추가).

## 3.2 Product Installation and Configuration (제품 설치 및 설정)

Helm Chart 기반 배포(인프라 담당). 환경 변수는 KMS/Secrets Manager. 상세 TBD.

## 3.3 Distribution Environment (배포 환경)

### 3.3.1 Master Configuration

Docker 이미지(컨테이너). 빌드 산출물·태깅 절차 TBD.

### 3.3.2 Distribution Method

Azure Pipelines CI/CD → 컨테이너 레지스트리(ECR) → EKS 배포.

### 3.3.3 Patch/Update Method

롤링 배포(K8s). 카나리·롤백 정책은 FR-FLEET-04(v1.1) 참조. 상세 TBD.

## 3.4 Development Environment (개발 환경)

GW는 **클라이언트(EzServer/CleverOne)·upstream(AXS·CleverSpace·OneID)·LMP** 등 다수 외부에 의존하므로, 이들이 모두 준비되기 전에 개발하려면 **실 sandbox·스텁·에뮬레이터를 조합**한다. 로컬(개발 PC, 컨테이너)에서 GW core를 띄우고 의존을 대체한다.

**개발 의존성 대체 (구축 필요 — 없으면 개발 불가)**

| 의존 | 역할 | 개발 환경 대체 |
| --- | --- | --- |
| **AXS** | 외부 연동(C, §7.5) | **AXS sandbox**(unstable, ESIP-14·④) — connector 1차 개발 대상. 자격증명 미수령 시(Appendix B #6) **AXS 응답 mock** |
| **EzServer PMS Integration(EPI)** | GW 호출 클라이언트(경로 A) | **클라이언트 에뮬레이터** — `Vatech-Target` 헤더 부착·presigned 중계 요청·머신 인증(client_credentials)·역방향 MQTT 구독을 흉내(실 EzServer는 Rust 재개발 중) |
| **CleverSpace(EzCloud)** | presigned 발급 주체(②) | **발급 스텁** — presigned URL 발급 응답 mock + storage=MinIO/S3 dev (GW는 중계만이라 발급 응답만 필요) |
| **OneID** | 사람·클리닉 인증(OIDC) | dev 테넌트(실) 또는 **OIDC mock** |
| **LMP** | Clinic-ID 발급원(온보딩, §2.3.1) | **스텁/시드** — Clinic-ID 발급 흉내로 자동 등록 테스트 |
| **Webhook 송신** | AXS→GW 이벤트(§7.6) | AXS sandbox webhook **또는** provider 호스트로 HMAC 서명 POST하는 **simulator** |

**AXS 연동 우선 개발 경로(개발계획서 core pilot=Straumann).** ① GW core(인증·라우팅 ADR-11) → ② **AXS connector(§7.5)** → ③ **AXS sandbox로 E2E**(파일 presign 중계·webhook 수신·역방향 MQTT). 이때 클라이언트는 **EPI 에뮬레이터**, 그 외 upstream은 **스텁**으로 두고 AXS만 실 sandbox를 쓴다. AXS smoke 케이스(TC-01~04)는 AXS 테스트환경 문서(ESIP-14).

### 3.4.1 Hardware Environment

특별 HW 요구 없음 — 표준 개발 PC(별도 규정 없음). 빌드·로컬 컨테이너(PostgreSQL·Valkey·큐 등 §3.4) 구동 가능 사양이면 충분.

### 3.4.2 Software Environment

Node.js / NestJS / Prisma / PostgreSQL(local) / Docker / **Claude Code(개발 표준)** · VS Code. 버전 TBD(설계 단계).

## 3.5 Test Environment (테스트 환경)

테스트(staging)는 **운영 유사·축소** AWS 환경으로, 통합·E2E·부하·인수 검증을 수행한다(§3.1 매트릭스). 개발(로컬·스텁 위주)과 달리 **가능한 한 실서비스/sandbox에 가깝게** 구성한다.

- **구성**: 운영과 동일 스택(EKS·Aurora·ElastiCache for Valkey·SQS·IoT Core)을 **소형**으로. 단일 리전(멀티 리전은 gw/1.2 검증 시).
- **외부 의존**: **AXS sandbox**(unstable, ESIP-14) · EzServer는 **실 EzServer(가능 시)** 또는 에뮬레이터 · OneID staging 테넌트 · CleverSpace sandbox/실 · LMP staging.
- **데이터**: **더미만(PHI 금지)** — 운영 PHI를 테스트에 반입하지 않는다(§6.5).
- **egress**: AXS sandbox용 **고정 EIP**를 Straumann과 협의해 whitelist(운영과 별개, §7.5.3).
- **검증·게이트**: 단위(Jest)·E2E·부하. CI(§3.6.2)에서 **테스트 통과를 baseline 게이트**로. 부하 목표치는 §5(규모 확정 후, Appendix B #1).

### 3.5.1 Hardware Environment

클라우드 — AWS staging. **운영 §3.1.1 HW 구성과 동일(축소본)** — 동일 스택·소형 인스턴스/노드.

### 3.5.2 Software Environment

운영(§3.1.2)과 동일 스택의 축소본. AXS `unstable` sandbox 전제(④ Sub-SRS·ESIP-14). 단위(Jest)·E2E·부하 테스트 도구 TBD.

## 3.6 Configuration Management (형상관리)

### 3.6.1 Location of Outputs

- 소스코드: Azure Repos `vt-api-gateway` (es-platforms)
- 문서: Azure Repos `vt-api-gateway` (es-platforms) `docs/specs/` — 공식 리뷰·baseline 위치 (설계 산출물은 `docs/specs/design/`)

### 3.6.2 Build Environment

Azure Pipelines(TDD 게이트 — 테스트 통과 필수). Node.js·pnpm 버전 TBD.

## 3.7 Bugtrack System (버그트래킹)

- 시스템: Jira (`https://vts.vatech.com`)
- 프로젝트 키: `ESIP` / Component `platform/api-gateway`

## 3.8 Other Environment (기타 환경)

None

---

# 4 External Interface Requirements (외부 인터페이스 요구사항)

## 4.1 System Interfaces (시스템 인터페이스)

- API: [OpenAPI — `vt-api-gateway.openapi.yaml`](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/design/openapi/vt-api-gateway.openapi.yaml)
- ERD: [DBML — `vt-api-gateway.dbml`](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/design/dbml/vt-api-gateway.dbml)

연동 시스템: OneID(OIDC), CleverSpace, Straumann AXS(④), CleverLab, EzServer(MQTT). 상세 계약은 §7 + Swagger.

### 4.1.1 API 정의 전략 — GW 고유 API vs 레지스트리 라우팅 프록시 (2면)

GW는 **두 면(surface)** 만 노출한다. 백엔드 API를 GW에서 재정의하지 않는다(중복 = 드리프트).

- **A. GW 고유 API** — GW가 직접 정의·처리하는 면(§7 전부).
- **Proxy. 레지스트리 라우팅 프록시** — 등록된 upstream으로 요청을 **그대로 전달(verbatim bypass)** 하는 면. upstream이 우리 소유(내부)냐 제3자(외부)냐에 따라 **trust profile만 다르며**(라우팅 메커니즘은 동일), 각각 **B(internal)·C(external)** 로 부른다.

**두 면은 요청의 `Vatech-Target` 헤더 유무로 배타적으로 갈린다** — 없으면 A(GW가 처리), 있으면 Proxy(등록 upstream으로 전달). 라우팅 모델·불변식은 §4.1.2, 결정 근거는 ADR-11(target-routed proxy).

| 면 | 무엇 | 라우팅 키 | GW 역할 | 정본(SSOT) |
| --- | --- | --- | --- | --- |
| **A. GW 고유 API** | §7 전부 — 인증·enrollment·디바이스 레지스트리·region resolve·Webhook 수신·**관리 API(③-C Console이 호출하는 Backoffice/관리 API 포함, §7.9·§7.8)**. UI 자체는 ③-C | **`Vatech-Target` 없음** (GW-own) | GW가 직접 처리·OpenAPI 정의(NestJS code-first `@nestjs/swagger`, §1.7.1) | 본 SRS §7 + [OpenAPI](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/design/openapi/vt-api-gateway.openapi.yaml) |
| **B. 프록시(internal)** | **우리 소유** 백엔드(CleverSpace·OneID) | **`Vatech-Target` = 논리 ID**(예 `cleverspace`) | **verbatim bypass** + 정규화 신원 전달 + 정책 체인. 내부망 trusted — 백엔드가 GW 신뢰 | 각 백엔드 제품의 OpenAPI |
| **C. 프록시(external)** | **외부 제3자**(Straumann AXS, 향후 DS Core/3Shape) | **`Vatech-Target` = 논리 ID**(예 `axs`) | **verbatim bypass** + OAuth2 인증·토큰/secret 관리(§7.1.3)·고정 egress IP·egress allowlist(§7.5)·Webhook 역수신(§7.6). 경계 밖 untrusted | ④ Sub-SRS + 외부 OpenAPI 스냅샷 |

- **handle(A) vs proxy(B/C) 판별 = `Vatech-Target` 유무**(배타). A에 헤더 부착 시 거부, proxy인데 누락 시 fail-closed(`400`). 상세 불변식은 §4.1.2.
- **B vs C = trust profile 차이일 뿐 라우팅은 동일**: B = 내부 안내 데스크(통과 + 정규화 신원), C = 거래처 방문(OAuth·토큰·secret·고정 egress IP·외부 장애 책임). C가 토큰·secret·외부 장애 책임까지 지므로 §7.5 커넥터 프레임워크로 1급 처리하고, B는 정책 체인 수준의 경량이다.
- **신규 upstream 추가 = 레지스트리 1행**(논리 ID→host + trust profile + 정책·egress)으로 끝난다 — **코드·경로 네임스페이스 변경 0**(NFR-SCL §6.3.5). §7.5.1 connector 프레임워크를 _내부·외부 전 upstream_ 으로 일반화한 것이며, 내부·외부를 **하나의 라우팅 규칙**으로 다룬다.
- **파일 업로드·presigned는 API 면과 데이터 경로를 구분한다**(§4.1.4): 경로②=B proxy(`Vatech-Target: cleverspace`)·경로③=C proxy(`Vatech-Target: axs`) — 둘 다 GW가 발급을 **중계(bypass)** 만 하고 presigned를 **직접 발급하지 않는다**(경로①=GW 직접 발급은 폐기, §4.1.4). **파일 바이트**는 어느 경로든 presigned로 **storage 직접 업로드**(GW 미경유).
- **CleverLab은 B 프록시 대상이 아니다.** 우리 클라우드 기공소 PMS지만, GW와의 관계는 **갈래 B 클라우드↔클라우드 연동(보류)** — CleverLab이 **C(AXS)를 향해 GW를 호출하는 클라이언트**(CleverLab→GW→AXS, EzServer가 GW를 호출하는 것과 같은 역할)이고, AXS 이벤트는 Webhook으로 수신(GW→CleverLab)한다. 따라서 위 B 행에 넣지 않는다(§2.1·④·§7.6.5).

### 4.1.2 라우팅·API 설계 규칙

1. **라우팅 모델 — `Vatech-Target` 유무로 면을 가른다.** 요청에 `Vatech-Target`이 **없으면 GW 고유 API(A)** 로 GW가 처리하고, **있으면 Proxy(B/C)** 로 등록 upstream에 전달한다. 두 면은 **배타** — A의 GW-own 경로에 `Vatech-Target` 부착 시 거부, proxy 호출에 누락 시 **fail-closed(`400`)**(추측 라우팅 금지). **v1.0부터 proxy 호출은 `Vatech-Target` 필수**(케이스 D 통합 — GW 전환 시 클라이언트를 어차피 변경하므로 증분 부담).
2. **목적지는 GW가 결정한다(서버측 레지스트리) — 클라이언트는 host/주소를 지정하지 않는다.** `Vatech-Target`은 **논리 서비스 ID(enum)만** 싣고 **host/URL은 금지**한다. GW가 레지스트리로 id→host를 해석(allowlist 검증)하며 **미등록 id → 거부(`404`/`403`)**. 따라서 클라이언트는 _논리 의도_ 만 표명하고 **주소 결정권은 GW**가 보유한다(SSRF·오픈 프록시·토폴로지 결합 차단). 원서버 주소 헤더·임의 라우팅 헤더(`X-Upstream` 등) 신설 금지 — 라우팅 키는 `Vatech-Target` 단일.
3. **proxy 전달은 verbatim, 정책은 path를 본다.** 클라이언트는 GW 호스트에 **upstream 경로를 그대로** 호출하고, GW는 **host만 바꿔 요청/응답 body를 그대로 통과**(필드 해석·변환 없음)한다. 단 **인증·버전 게이트·egress allowlist 정책은 (target+method+path)로 검사**한다 — GW는 path를 _라우팅엔_ 쓰지 않되 _정책엔_ 본다. **리전 목적지**는 `Vatech-Target`(어느 서비스) + `Vatech-Clinic-Id`(어느 리전, §7.3 resolver)의 **직교 조합**으로 구체 host를 정한다(멀티 Region).
4. **proxy(B·C)도 정책 체인을 통과한다** — 인증(§7.1)·버전 게이트(§7.7)·egress/allowlist(§7.5.3·§6.5). 전달이 무검증이 아니다. B/C 차이는 **trust profile**(§4.1.1)뿐 — C는 OAuth·토큰 관리(§7.1.3)·고정 egress IP가 추가된다.

> **`Vatech-Target`(라우팅) ≠ `Vatech-*` 식별 헤더(§7.7.1).** 식별·버전·리전 헤더는 `Vatech-*` 표준(`Product`·`Version`·`OS`·`Clinic-Id`·`Via`)만 쓰며 **버전 호환 판정용 필수**(FR-COMPAT-01)다 — "누가·어떤 버전·어느 클리닉"을 싣는다. `Vatech-Target`은 **라우팅용으로 proxy 호출에 필수**다 — "어느 논리 서비스로"를 싣는다. 이름이 비슷하나 역할이 다르다(식별 vs 라우팅).

5. **GW 고유 API 컨벤션**: REST/JSON, **경로 버전 프리픽스 `/v1`**(예 `/v1/auth/token`, 관리 API는 `/admin/v1/*`; Webhook 수신 경로는 유연·provider별 등록이라 본 컨벤션 예외 — §4.1.3·§7.6.1), camelCase 필드, 시간 Unix ms(§1.3), 표준 오류코드(§7.7.4), idempotency key(§4.5). 단 `/.well-known/*`은 표준 관례상 버전 프리픽스 없이 노출(§7.7.2). 스키마 정본은 Swagger(code-first).

6. **프록시 실패·타임아웃·업스트림 오류 의미론.** GW는 _서버_(downstream=원클라이언트)이자 *upstream의 클라이언트*다 — **GW의 upstream 총 deadline은 downstream 클라이언트 타임아웃보다 짧게** 잡아, 클라이언트가 포기하기 전에 GW가 **결정적 오류(504)** 를 돌려준다(고아 요청·커넥션/워커 점유·재시도 증폭 방지). 타임아웃·재시도·서킷·오류 매핑은 **per-upstream 레지스트리 설정**이며 상세는 §7.5.4, 오류코드 매핑은 §7.7.4. **GW가 생성한 오류**(연결 실패=`502` / deadline 초과=`504` / 서킷·일시불가=`503`)는 **GW 표준 error envelope**로 내고, **upstream 자체 4xx/5xx는 verbatim 통과**(body 미변형)하되 **`Vatech-Error-Origin`(`gateway`|`upstream`)** 마커로 책임을 구분한다. 클라이언트 조기 절단 시 GW는 upstream 호출을 **취소**한다(cancellation 전파).

#### 라우팅 방식 비교·결정 (ADR-11)

API Gateway가 "어느 upstream으로 보낼지"를 정하는 방식은 여럿이다. 아래 4안을 다기준으로 비교한다. 현재 **헤더 기반(`Vatech-Target`)** 으로 결정(ADR-11, CCB 승인 2026-06-25)했으나 **모든 기준에서 우수한 것은 아니며**(특히 운영/장애대응은 경로·서브도메인이 유리) **트레이드오프가 있어 재평가 안건으로 상정**한다(주간회의 7/2 R1). (표기 ◎ 우수 · ○ 양호 · △ 제약 · ✕ 부적합)

| 기준 | A. 헤더 `Vatech-Target` (현 결정) | B. 경로 프리픽스 `/axs/…` | C. 서브도메인 `axs.gw…` | D. 클라이언트 지정 host/URL |
| --- | --- | --- | --- | --- |
| 일반성(업계 관례) | △ 덜 흔함(주로 버전·카나리) | ◎ **가장 흔함** | ○ 흔함 | ✕ 안티패턴 |
| verbatim bypass(upstream 원 path 보존) | ◎ host만 교체·path 그대로 | △ 프리픽스 strip(변환) 필요 | ◎ path 그대로 | ◎ 그대로 |
| GW 고유 API ↔ 프록시 구분 | ◎ 헤더 유무로 배타·명확 | △ 둘 다 path라 경계 모호(예약 prefix 필요) | ◎ 호스트로 분리 | △ 모호 |
| 경로 충돌(우리 `/v1`·upstream 자체 path) | ◎ 없음 | △ 충돌 가능(예약·strip 관리) | ◎ 없음 | ○ |
| 클라이언트 적응 비용 | ◎ 헤더 1개 추가 | ○ 경로 프리픽스 부착 | △ base URL 변경 | ✕ |
| 보안(SSRF·오픈 프록시) | ◎ 논리 ID enum·서버 레지스트리 | ◎ 서버 레지스트리 | ◎ | ✕ host 노출·SSRF |
| DNS/TLS·인프라 비용 | ◎ 단일 apex | ◎ 단일 apex | △ upstream별 DNS·cert | ◎ |
| 멀티 리전(GW 다리전 배포 + 리전별 upstream 선택) | ◎ 단일 apex 지오라우팅 · 리전은 `Clinic-Id`로 분리(§4.1.2-3) | ◎ 동일(단일 apex · 리전도 `Clinic-Id`) | △ 서브도메인×리전 host 폭증·DNS/cert↑ | △ |
| 확장성(신규 연동 서버 추가) | ◎ 레지스트리 1행+enum, 코드변경 0 | ○ prefix 예약·충돌관리 필요 | △ DNS·cert 추가 | ✕ |
| 유지보수·장애대응(표준 로그·LB/CDN/WAF에서 target 가시·제어) | △ 커스텀 헤더 — 로그·엣지 제어에 추가 설정 필요 | ◎ URL에 target 노출 — 표준 도구로 추적·차단·rate-limit | ◎ host 노출(표준 로그) | △ |
| 관측·정책(앱 내부 target 식별) | ◎ 단일 헤더 키 | ○ path 파싱 | ○ host 파싱 | △ |

> **결론(정직 평가).** 헤더(A)는 **verbatim 중계 · GW 고유 API와 프록시 배타 구분 · 단일 apex(`gw.vatech.com`) · 클라이언트 최소 변경**에서 우수하다(멀티 리전은 A·B 동률 — 리전은 어느 방식이든 `Clinic-Id`로 정함). 반면 경로 프리픽스(B)·서브도메인(C)는 **업계 관례**와 **운영/장애대응**(target이 URL·host에 그대로 보여 표준 로그·LB/CDN/WAF로 추적·차단·rate-limit이 쉬움)에서 우수하다 — 헤더는 커스텀 헤더라 로그 캡처·엣지 룰에 추가 설정이 필요한 약점이 있다. 확장성·보안은 A·B가 비슷(레지스트리/설정 기반, SSRF 안전), C는 upstream별 DNS·인증서 부담, D는 SSRF로 반려. 즉 **"헤더가 전부 우수"는 아니고, 통합 모델 깔끔함(A) ↔ 운영 친화(B)의 트레이드오프**다. 현 결정은 verbatim·apex 단일화·A↔프록시 명확 구분의 가치를 우선한 것이며, **운영 가중치를 반영한 재평가를 주간회의(7/2 R1)에 상정**한다. 절충안: 헤더 유지 + ALB/CDN 액세스 로그의 `Vatech-Target` 캡처 의무화 + 엣지 룰을 헤더 매칭으로 구성(B의 운영 이점 일부 흡수). **ADR-11 — CCB 승인 2026-06-25**(Appendix A·B #13). 본 절은 SRS 차원 요약이며 결정 로그는 Appendix A.

### 4.1.3 Webhook API 정의 방침

Webhook은 두 면(§4.1.1) 어느 쪽에도 깔끔히 떨어지지 않는 **하이브리드**다 — *수신 엔드포인트*는 GW 수신면(외부가 `Vatech-Target` 없이 직접 POST — 단 **경로·스키마는 provider 규약 수용·유연**, GW 비강제), *이벤트 payload 스키마*는 C(외부 소유·참조만), *분배*는 내부 경로(클라우드 HTTP push·Edge MQTT)다. 단순 host 기반 프록시가 아니라 **수신→검증→멱등→ACK→매핑 기반 분배**의 store-and-forward 모델이다(§7.6). 따라서 API를 "전부 새로 정의"하지 않고, **GW가 소유하는 면만 정의하고 나머지는 참조**한다. 추후 §7.6 상세화 시 아래 4가지를 구분해 작성한다.

1. **수신 엔드포인트 = 유연·레지스트리 기반 수신기 (GW가 스키마·경로를 강제하지 않음).** GW가 소유·정의하는 것은 _수신 동작(발신자 검증→멱등→ACK→매핑 기반 분배)_ 이지 **제공자의 요청 스키마·경로가 아니다** — provider의 API 규약은 provider가 정하고, GW는 **어떤 형태의 인바운드 요청이든 수용**한다(해석 주체는 GW가 아니라 소비자).
   - **provider별 전용 호스트로 식별**(`{provider}.webhook.gw.vatech.com`, §4.5.1) — Host/SNI로 발신자를 판정한다(source IP 비의존). 그 아래 **경로/형식은 provider 규약을 수용해 유연**하게 둔다(GW 비강제). 기본 관례 `…/<provider 규약 경로>`는 예시일 뿐 확정 계약이 아니다.
   - **식별 vs 인증 분리**: **식별 = Host/SNI**(레지스트리 `inbound_host` 조회) → 그 provider의 검증 시크릿 선택. **인증(신뢰) = HMAC 서명 + timestamp**(replay 방지). **source IP allowlist는 옵션**(방어심층). **Host는 식별이지 인증이 아니다.** 미등록 Host/검증 실패 → 거부(`401`/`404`).
   - **payload는 GW가 해석하지 않는다** — 검증·라우팅에 필요한 **최상위 식별자(provider·eventId·org 식별자 등)만** 추출하고 본문은 그대로 통과(opaque). 본문 스키마를 GW가 정의/재정의하지 않는다.
   - **응답**: 즉시 `2xx` ACK(§7.6.3). 에러 `400`(형식)·`401`(서명·IP·timestamp).
   - OpenAPI에는 _수신·ACK envelope_ 만 최소 표기하고, 경로는 기본 관례로 **예시**하되 provider별로 가변임을 명시한다(payload는 opaque/`$ref`).

2. **이벤트 payload 스키마 = 정의하지 않고 참조한다 (C·외부 프로파일).** AXS 등 외부 소유. 정본은 **④ Sub-SRS + AXS OpenAPI 스냅샷**(`references/axs-openapi/`). GW는 검증(HMAC·멱등)에 필요한 **최상위 식별 필드(eventType·eventId·org 식별자 등)만 알면** 되고, 그 외는 분배 시 통과시킨다.
3. **분배 경로 = REST API로 노출하지 않는다 (내부).**
   - 클라우드 대상(**CleverLab** — 갈래 B 수신처; CleverSpace는 webhook 대상 아님): **받는 쪽 백엔드의 OpenAPI**가 정본(B·내부 프로파일 성격, 내부망 HTTP push). GW는 그 API를 호출할 뿐 정의하지 않는다.
   - Edge(EzServer): **MQTT QoS1**(§7.6.6) — REST가 아니므로 OpenAPI 대상이 아니다. 토픽 네이밍·payload·QoS·retain 규약은 별도(AsyncAPI 또는 §7.6 표)로 기술한다.
4. **목적지 결정 = 매핑이다, 송신 host가 아니다.** payload의 식별자(예 AXS Org-ID)를 ClinicID로 매핑(`org_mapping` 테이블, §6.4)하고 ClinicID→region(§7.3)→분배 채널(`delivery_channel`)로 대상 client를 정한다. GW는 본문을 해석하지 않고 이 라우팅 키만 본다. 매핑 규칙 상세는 ④ Sub-SRS.

> **정의 산출물 배치**: 수신 엔드포인트는 GW 단일 OpenAPI(`design/openapi/vt-api-gateway.openapi.yaml`)에 다른 GW 고유 API와 **함께** 둔다(code-first 단일 `/api-docs`와 일관). 외부 payload는 `$ref`로 분리 참조, MQTT 분배는 OpenAPI 밖(AsyncAPI/규약 문서). 별도 `webhook.openapi.yaml`로 쪼개지 않는다 — 같은 서비스가 노출하는 한 면이기 때문.

### 4.1.4 업로드·Presigned 경로 구분

파일 전송은 **control plane(API 면)** 과 **data plane(바이트 경로)** 을 분리해 이해한다. **GW는 presigned를 발급하지 않는다** — 발급 주체는 upstream(CleverSpace·AXS)이고 GW는 발급 요청을 **중계(bypass)** 만 한다. 파일 **바이트**는 어느 경로든 발급 주체 storage로 **직접** 업로드(GW 미경유).

> **폐기(2026-06-23 결정)**: 이전 \"경로①(GW Region Signer가 우리 리전 storage용 presigned 직접 발급, `/v1/uploads`)\"는 **철회**되었다. GW는 서명·세션·storage를 소유하지 않는다. 아래 ②③만 유효하며, 번호는 기존 참조 보존을 위해 그대로 둔다.

#### 두 가지 업로드 경로 (둘 다 GW 중계·bypass)

| # | 대상 | presign·업로드 **요청 API** (control) | presign **발급 주체** | GW 역할 | OpenAPI 정본 |
| --- | --- | --- | --- | --- | --- |
| **②** | **CleverSpace 등 사내 백엔드** presign·파일 API | **B 프록시** — `Vatech-Target: cleverspace`, upstream 경로 verbatim(§4.1.2) | **CleverSpace** | **verbatim bypass** — 요청/응답 body 그대로 통과, GW 해석·변환·서명 **없음** | CleverSpace OpenAPI |
| **③** | **Straumann AXS** 등 외부 presign·파일 API | **C 프록시** — `Vatech-Target: axs`, upstream 경로 verbatim(§4.1.2) | **AXS**(외부) | **verbatim bypass** + OAuth2·egress allowlist(§7.5) | ④ Sub-SRS + AXS 스냅샷 |

#### data plane (공통)

presigned URL을 **Client가 받은 뒤**, 파일 **바이트**는 **발급 주체 storage로 직접 업로드**한다(GW 미경유, §6.4).

```
[control] Client → GW (② B bypass / ③ C bypass · 발급 요청 중계) → upstream presign 발급 → presigned URL 반환
[data]    Client ═══════════════════════════════════════► 발급 주체 storage 직접 업로드 (GW 미경유)
```

> **GW가 하지 않는 일**: presigned **직접 발급(서명)**·업로드 **세션 소유**·region **storage 소유** — 모두 폐기. CleverSpace/AXS presign 스키마를 GW가 통합·변환하지도 않는다. GW는 발급 요청을 **중계**하고 정책(인증·버전·egress)만 적용한다.

> **②·③ 정본**: CleverSpace presign 변경은 **② Presigned One Pager**·CleverSpace OpenAPI. AXS presign·파일은 **④ Sub-SRS**·AXS 스냅샷.

## 4.2 User Interface (사용자 인터페이스)

GW 본체는 무인 control plane. Admin UI는 **③-C GW Console Sub-SRS**에서 정의(본 SRS는 관리 API §7.9까지). 따라서 본 절은 `N/A(③-C에서 정의)`.

## 4.3 Hardware Interface (하드웨어 인터페이스)

EzServer(디바이스, §1.4)와는 네트워크(REST/TLS) 인터페이스만. 직접 제어하는 HW 없음(물리 영상장비는 EzServer 뒤·GW 비대상) → `None`.

## 4.4 Software Interface (소프트웨어 인터페이스)

| 구성요소 | 버전 | 용도 |
| --- | --- | --- |
| OneID (OIDC) | TBD | 사람·클리닉·사내 호출자 인증 |
| Straumann AXS API | OpenAPI 스냅샷(2026-06-16) | 외부 연동(④) |
| PostgreSQL | 15.x | 레지스트리·매핑·토큰메타·정책·감사 |
| Redis | TBD | region 캐시·nonce·rate-limit·idempotency·JWKS |
| 메시지 큐 — **A. 내부 큐: Amazon SQS**(FIFO=순서/dedup) / Amazon MQ | TBD | **GW 내부** Webhook 비동기 분배·재시도·백오프·DLQ(§7.6.3). 엣지 전달(B)과 **별개 레그** |
| 오브젝트 스토리지 (S3 / MinIO) | TBD | 발급 주체(CleverSpace/AXS) storage — presigned 직접 업로드(GW 미경유, §4.1.4·§7.4) |
| MQTT Broker — **B. 엣지 전달**: AWS IoT Core / Amazon MQ | TBD | 방화벽 뒤 Edge(EzServer) 마지막 구간 push(QoS1·persistent, §7.6.6). 내부 큐(A·SQS)와 **별개 레그**·제품·운영주체 TBD(Appendix B #4) |
| OPA | TBD | allowlist·region·scope·egress 판단 |

## 4.5 Communication Interface (통신 인터페이스)

- 프로토콜: HTTPS(TLS 1.2+). Webhook 수신=HTTPS POST. Edge 분배=MQTT(QoS1·persistent).
- 보안: Bearer JWT(사내), OAuth2 client_credentials(디바이스·AXS), Webhook HMAC 서명·IP allowlist·timestamp.
- 동기화: idempotency key(업로드 commit·Webhook eventId), 재시도·백오프·DLQ.
- presigned: 디바이스→리전 storage 직결(GW 미경유).

### 4.5.1 공개 엔드포인트(DNS)

DNS 호스트는 *클라이언트가 접속하는 외부 계약*이므로 본 SRS에 기록한다. **GW API apex `gw.vatech.com`은 확정(Scott)** 이다. 인증서·GeoDNS 구성·리전 내부 호스트 네이밍 등 *구성*은 인프라/플랫폼팀 소유이며, 아래 표의 나머지 항목(리전 내부 호스트·Console·Webhook 경로)은 규약·예시다.

| 용도 | 호스트 | 비고 |
| --- | --- | --- |
| GW API (GeoDNS apex) | `gw.vatech.com` **(확정)** | **클라이언트가 호출하는 유일한 호스트.** Route 53 GeoDNS로 최근접 리전 라우팅(§7.3.5). **v1.0(단일 리전)에서도 apex를 사용** — apex가 단일 리전을 가리키고, 2차에 백엔드만 N개로 늘린다 |
| Webhook 수신 (provider별) | `https://{provider}.webhook.gw.vatech.com` (예: `axs.webhook.gw.vatech.com`) | **provider별 전용 호스트로 발신자 식별**(Host/SNI). **와일드카드 DNS 미사용**(엄격 관리·명시 등록; 추가는 연단위로 드묾), TLS는 `*.webhook.gw.vatech.com` 와일드카드 cert 가능. 경로/형식은 provider 규약 수용(유연, §7.6.1·§4.1.3). **Host=식별, 인증=HMAC**(§7.6.2) |
| 리전별 엔드포인트(내부) | `gw-<region>.vatech.com` (예: `-apne2`) | GeoDNS 백엔드·내부/운영용. **v1.0부터 네이밍 규칙 예약**(단일 리전 1개만 실재), 2차에 N개로 확장. 클라이언트엔 노출하지 않음 |
| GW Console | `console.gw.vatech.com` | **③-C 영역** — 본 SRS는 참조만. 확정은 ③-C Sub-SRS |

> **멀티리전-ready DNS (§2.7.1).** v1.0이 단일 리전이라도 **클라이언트는 처음부터 apex(`gw.vatech.com`)만** 사용한다(리전 호스트 직접 노출 금지). 그래야 2차 리전 추가 시 **클라이언트·헤더 변경 없이 GeoDNS 백엔드만 늘려** 멀티 리전이 활성화된다. 즉 v1.0에서 apex→단일 리전 1:1이고, 2차에 apex→GeoDNS→N리전으로 _DNS 구성만_ 바뀐다. (apex 없이 단일 리전 호스트를 클라이언트에 박으면 2차에 클라이언트 재배포가 필요 — 금지.)

- **apex 호스트명 `gw.vatech.com` 확정(Scott, 2026-06-24)** — 재논의 불요.
- 잔여(인프라/플랫폼팀): 인증서 발급·GeoDNS 구성·리전 내부 호스트(`gw-<region>.vatech.com`) 실제 등록 — 배포 구성 착수 전.
  - 결정 마감 시점: 배포 구성 착수 전
  - 영향 받는 섹션: §1.7.1·§3.1·§7.3.5·§7.6.1 · ①/②/④ 클라이언트 연동 · ③-C(Console)

## 4.6 Other Interface (기타 인터페이스)

None

---

# 5 Performance requirements (성능 요구사항)

> 수치는 §3.1 운영 환경(AWS 단일 리전 v1.0) 기준. **범위 경계**: 본 SRS는 _성능 요구치(목표)_ 만 정의한다. **서버/노드 규모·용량 산정은 GW SRS 범위 밖(인프라 IaC 영역, §3.1)** 이며, 디바이스/클리닉 운영 규모 수치는 PL이 제공한다.

## 5.1 Throughput (작업처리량)

단위 = control-plane 요청 RPS(인증·라우팅·세션 시작 등, 파일 전송 제외).

- **TBD**: v1.0 목표 RPS
  - 미결 이유: v1.0 운영 대상 디바이스/클리닉 규모가 미확정(10만대는 v2.0). 목표 RPS는 fleet 규모·디바이스당 호출 빈도에서 산출
  - 결정 책임자: **인프라 담당** (디바이스/클리닉 규모는 PL 입력). GW SRS 작성자는 요구치 문장만 보유
  - 결정 마감 시점: 설계 착수 전
  - 영향 받는 섹션: §3.1(노드 사양)·§5.2·§7.1·§7.4
- 산출 기준(제안): `목표 RPS ≈ 동시 활성 디바이스 × 디바이스당 평균 호출/초 × 피크 계수`

## 5.2 Concurrent Session (동시 세션)

세션 정의 = control plane 동시 활성 디바이스(최근 1분 내 요청).

- **TBD**: v1.0 동시 세션 목표
  - 미결 이유: §5.1과 동일(fleet 규모 미확정)
  - 결정 책임자: **인프라 담당** (규모 수치는 PL 입력). GW SRS 작성자 범위 밖
  - 결정 마감 시점: 설계 착수 전
  - 영향 받는 섹션: §3.1·§5.1·§5.4·§7.4

> ❓확인 필요 — **v1.0 운영 목표(디바이스 대수·클리닉 수·피크 업로드 패턴)**. 이 값이 정해지면 §5.1·5.2를 구체 수치로 확정한다.

## 5.3 Response Time (대응시간)

인증·프록시 **p95 < 300ms** (파일 전송 제외) — NFR-PERF. 파일 전송은 presigned 직결이라 본 목표에서 제외(§5.4).

> **🔍 대안 검토 — control-plane 응답 시간 목표 (NFR-PERF)**
>
> - 채택안: 인증·프록시 **p95 < 300ms**(파일 제외)
>   - 장점: 디바이스 작업 직전 인증·라우팅 지연 체감 최소. 일반 API 게이트웨이 통념 수준
>   - 단점: 단일 리전·강한 일관성 경로(revocation·mapping 변경)에서 여유 적음
> - 대안 1: p95 < 500ms — 인프라 비용↓이나 다수 호출 누적 시 디바이스 작업 흐름 지연 체감
> - 대안 2: p99 기준 추가(예: p99 < 1s) — 꼬리 지연까지 관리하나 측정·운영 복잡도↑
> - 선정 이유: NFR-PERF 합의치. 파일은 직결이라 본 목표가 control-plane 체감을 대표
> - 재검토 조건: 멀티 리전(gw/1.2) 도입 / 동시 세션 목표 확정 후 부하 검증 결과

## 5.4 Performance Dependency (성능 종속 관계)

- 파일은 presigned 직결로 GW 미경유 → **GW control-plane 부하와 파일 크기·전송량 무관**. §5.3 목표가 파일 크기에 영향받지 않음
- 강한 일관성 경로(revocation §7.2.4·mapping 변경 §7.3.2)는 캐시 경로보다 지연↑ → 동시 세션 증가 시 §5.3 여유 감소
- 동시 세션(§5.2) ↑ → control-plane RPS(§5.1) 자원 경합

## 5.5 Other Performance Requirements (기타 성능 요구사항)

- Webhook: 수신 후 **즉시 2xx ACK**(처리는 큐 위임, §7.6.3) — ACK 지연 목표 TBD(설계 단계, 영향: §7.6)
- presigned URL TTL: 5~15분(§7.4.2)
- **프록시 타임아웃 예산(§7.5.4)**: per-upstream `connect`/`response`/`total_deadline` — `GW 총 deadline < 클라이언트 타임아웃`이 불변식. 구체 값은 upstream SLA·인프라 입력 의존 **TBD**(Appendix B #25)

---

# 6 Non-Functional Requirements (기능 이외의 요구사항)

## 6.1 Safety requirements (안전성 요구사항)

GW는 의료 데이터(PHI) 경로의 control plane이므로, 데이터 보호·오연동 방지가 안전성의 핵심이다. 도출용 5질문 기준:

| #   | 질문                                        | 본 SRS 대응                                                                    |
| --- | ------------------------------------------- | ------------------------------------------------------------------------------ |
| 1   | 비정상 동작이 재산·프라이버시 피해를 주는가 | PHI 유출·오리전 전송이 위험 → §6.1 통제 대상                                   |
| 2   | 피해 확률                                   | 라우팅 오류·매핑 drift 시 발생 가능 → mapping_version·강한 일관성(§7.3)로 완화 |
| 3   | 비정상 종료·장애                            | Webhook 수신 실패·큐 적체 → 빠른 ACK·DLQ(§7.6.3)                               |
| 4   | 사용자(운영자) 실수                         | 매핑 오재지정 → 재동의·감사 강제(§7.3.4·§7.9)                                  |
| 5   | 피할 수 없는 피해                           | 리전 장애 시 가용성 저하 → Multi-AZ(§6.3.1)                                    |

핵심 안전 규칙:

- PHI는 **매핑된 리전 밖으로 이동하지 않는다**(FR-RGN-03). 객체 키·메타데이터에 PHI 미포함(§7.4.2)
- 디바이스 revocation은 캐시 TTL과 무관하게 **즉시 차단**(§7.2.4)
- 의료기기 SW 인증 대상 — §6.13·§6.6.1 준수

## 6.2 Security Requirements (보안 요구사항)

보안 분석 8항목 점검(상세 정책은 [인증·보안·컴플라이언스 설계](https://vks.vatech.com/pages/viewpage.action?pageId=311608329) 참조):

| #   | 항목                | GW 적용                                                                                         |
| --- | ------------------- | ----------------------------------------------------------------------------------------------- |
| 1   | Authentication      | 디바이스 OAuth2 cc + claim 바인딩(§7.1.1), 사내·사람 OneID OIDC(§7.1.4). DPoP+HW키 v1.1(ADR-01) |
| 2   | Authorization       | 운영자 RBAC(§7.9.2), scope 기반 디바이스 권한                                                   |
| 3   | Access control      | OPA allowlist(미등록 디바이스 차단 §7.2.2), egress endpoint allowlist(§7.5.3)                   |
| 4   | Non-repudiation     | append-only 감사(operator·timestamp·before/after·IP, §7.9.3)                                    |
| 5   | Confidentiality     | 전 구간 TLS, 시크릿 KMS, 외부 토큰 암호화 저장(§7.1.3), PII/PHI 비저장(NFR-SEC)                 |
| 6   | Integrity           | 업로드 checksum/ETag(§7.4.5), idempotency(§7.4.4·§7.6.4), Webhook HMAC(§7.6.2)                  |
| 7   | Secure coding       | OWASP Top 10 점검, 의존성 스캔(CI 게이트)                                                       |
| 8   | Web vulnerabilities | 입력 검증(class-validator), 표준 오류 매핑(§7.7.4)                                              |

> 보안과 편리의 트레이드오프: 디바이스는 머신 인증(무인 자동), 운영자 관리 변경에만 RBAC·감사 강화 — 행위별 보안 강도 분리.

## 6.3 Software System Attributes (소프트웨어 시스템 특성)

### 6.3.1 Availability (가용성)

- v1.0(**1차 단일 리전**): control plane **Multi-AZ ≥ 99.9%**(월 다운타임 ≤ 약 43분) — NFR-AVA. 단일 리전 내 다중 AZ로 HA 확보(멀티 서버, §2.1.1)
- v1.2(**2차 멀티 리전**): 글로벌 **active-active**(멀티 리전). v1.0이 멀티리전-ready로 설계되어(§2.7.1) 재설계 없이 확장
- 유지보수 윈도우·복구(RTO/RPO)는 인프라 담당과 협의 — TBD(영향: §6.8)
- 파일 경로는 presigned 직결이라 GW 가용성과 분리(GW 장애 시에도 발급된 URL 유효 구간 내 업로드 가능)

### 6.3.2 Maintainability (유지보수성)

NestJS 모듈(bounded context) 분리·TDD. (NFR-MNT/OBS)

**관측·구조화 로그.** 도구는 §3.1.2(Pino·OpenTelemetry/ADOT). 본 절은 **로그의 구조(요구)** 를 정의하고, 정확한 필드·레벨 확정본은 인프라 취합 포맷과 협의해 확정한다(**Appendix B #14**, 필요 시 `design/`에 로그 스키마 산출물).

- **형식**: 모든 로그는 **기계 파싱 가능한 구조화 JSON 한 줄**.
- **필수 필드(최소셋)**: `ts`(Unix ms)·`level`·`service`/`version`·**`traceId`/`spanId`(OTel 상관)**·`requestId`·`tenantId`/`clinicId`·`actor`·`action`·`result`·`latencyMs`·실패 시 `errorCode`.
- **상관키**: OpenTelemetry **`traceId`** 로 요청 전 구간을 상관하고, **`Vatech-*`(originator)·`Vatech-Via`(경유 홉)** 를 함께 남겨 클라이언트·중계 홉까지 추적한다(§7.7).
- **레벨**: error/warn/info/debug (운영 기본 info 이상).
- **금지**: **PHI·시크릿·토큰 평문 미기록**(식별자만, §6.2·§6.4·§1.4 PHI).
- **앱 계약 vs 수집층 분리.** GW **앱**은 **stdout 구조화 JSON 로그 + OTel 계측(trace/metric·traceId)** 까지만 책임진다(고정). 그 로그·텔레메트리를 실어 나르는 **수집 에이전트는 교체 가능**하며 **인프라 선택**이다(2026-06 회의·§2.6, **Appendix B #14**).
  - **권장 패턴(인프라 리뷰·확정)**: **Fluent Bit(DaemonSet) → CloudWatch**(컨테이너 로그·EKS 표준) **+ ADOT(OTel) → CloudWatch/AMP·X-Ray**(metric/trace). 단일 파이프라인 선호 시 OTel Collector가 로그까지 담당하는 구성도 가능. **OTel은 trace 상관(`traceId`)을 위해 필수**이고 Fluent Bit는 로그 전송 특화라 **둘은 경쟁이 아니라 역할 분리**.
  - 로그 백엔드(CloudWatch / Loki·Grafana / OpenSearch 등)도 인프라 선택. **어느 조합이든 앱은 stdout JSON+OTel로 동일** — 수집층 변경이 앱에 영향 없음.

- **로그 취합·분석은 인프라 담당 영역**(2026-06 회의) — GW는 구조화 로그(Pino)·trace(OpenTelemetry)를 **생성·노출**하고, 중앙 수집·저장·분석 파이프라인은 인프라가 구성한다(③-I). **로그 포맷(필드·상관관계 키·레벨)은 검토 중(TBD)** — 확정 시 GW·인프라 합의(영향: §6.2 PHI·시크릿 미기록 제약 준수, Appendix B #14).

### 6.3.3 Portability (이식성)

IaC 환경 재현으로 이식 대비. (presign broker는 GW가 두지 않음 — 발급 주체별 storage, §7.4)

### 6.3.4 Reliability (신뢰성)

Webhook 전달 보증(QoS1·재시도·DLQ), 업로드 idempotency. **동기 프록시(B/C) 복원력**: per-upstream 타임아웃·서킷 브레이커·멱등 한정 재시도로 장애 격리(한 upstream 장애가 GW 전체로 번지지 않게) — `GW deadline < 클라이언트 타임아웃` 불변식(§7.5.4·§4.1.2-6). MTBF 목표 TBD.

### 6.3.5 Remaining Attributes (나머지 특성)

- Scalability — 플랫폼·테넌트·리전 추가가 **설정 기반(코드 변경 최소)** 으로 확장(NFR-SCL). connector(§7.5.1)·리전(§7.3)·테넌트(§7.9.1)는 설정 등록으로 추가
- Interoperability — 표준 OAuth2/OIDC/OpenAPI/Webhook 준수. 그 외 `None`.

## 6.4 Logical Database Requirements (데이터베이스 요구사항)

- ERD: [DBML — `vt-api-gateway.dbml`](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/design/dbml/vt-api-gateway.dbml). 신규 테이블의 컬럼·타입·인덱스·relation은 DBML(dev-chain-design)이 SSOT

#### 6.4.1 핵심 엔터티 관계 (Clinic · Device · 외부 Org) — A안 채택(주간회의 확인 예정)

> **A안 채택(2026-07-01)**: **region SSOT = Clinic**, device는 clinic에서 region **파생**(device.region·device→region 매핑 제거). DBML·OpenAPI에 반영 완료. **주간회의(R8)에서 최종 확인**. 미래(점선)는 DBML 미정의.

```mermaid
erDiagram
    CLINIC ||--o{ DEVICE : "보유(현 1:1=EzServer · 모델 1:N)"
    CLINIC ||--|| REGION : "배정(1:1)"
    CLINIC ||--o{ EXTERNAL_ORG : "확장: 연동 provider별 1 (AXS=현재)"
    CLINIC {
        string clinic_id PK
        string region FK
    }
    DEVICE {
        string device_id PK
        string clinic_id FK "nullable · region은 clinic 파생"
        string status
    }
    EXTERNAL_ORG {
        string provider PK "예 axs"
        string external_org_id PK "예 AXS Org-ID"
        string clinic_id FK
    }
    REGION {
        string region_id PK
    }
```

기본(항상 존재) ↔ 확장(연동 시) ↔ 미래(추가 개발) 계층:

```mermaid
flowchart LR
    DEV["Device · 기본"]:::base
    CLI["Clinic · 기본"]:::base
    ORG["외부 Org-ID · 확장(AXS)"]:::ext
    FUT["미래 provider id · 확장(추가 개발)"]:::fut
    DEV -->|"clinic_id (nullable)"| CLI
    CLI -->|"provider별 1:1"| ORG
    CLI -.->|"신규 연동 시"| FUT
    classDef base fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#0d47a1
    classDef ext fill:#fff3e0,stroke:#fb8c00,stroke-width:2px,color:#e65100
    classDef fut fill:#ffffff,stroke:#9e9e9e,stroke-width:1.5px,stroke-dasharray:5 4,color:#555
```

- **기본 엔터티 = Clinic · Device**(항상 존재). **확장 엔터티 = 외부 Org-ID**(외부 연동 시에만). org는 "기본"이 아니라 **확장**이다.
- **Clinic ↔ Device = 1:N**(모델). **현재는 1:1** — 클리닉당 EzServer 1대(§2.3.1·Appendix B #17). `device.clinic_id`는 **nullable** — **미래 비-EzServer 디바이스**가 직접 등록되면 한 클리닉에 N대이거나 클리닉 비소속(clinic_id 없음)일 수 있다.
- **디바이스 등록 시 clinic_id 포함**: EzServer가 LMP Clinic-ID 수신 시 자동 등록(§2.3.1)하므로 device에 clinic_id가 채워진다 → **`device.clinic_id`(FK·nullable) 추가 완료**(DBML·OpenAPI).
- **외부 Org-ID = (provider, external_org_id) → clinic_id**(`org_mapping`). **provider별 클리닉↔외부 id 1:1**. **AXS 연동 시에만 `axs` org_id 존재**하고, 미연동이면 없다.
  - **송신(AXS)**: clinic → org_id 조회해 **org_id를 실어 보냄**.
  - **수신(Webhook)**: 이벤트에 **org_id 동반** → `(provider, org_id) → clinic` **역조회로 분배 대상** 판정(§7.6·§2.3.6).
- **확장성(제3·4 서비스)**: 신규 연동은 — (a) **동일 패턴이면 `org_mapping`에 provider 값만 추가**(외부 id가 (provider, external_id)→clinic 형태), (b) **구조가 다르면 신규 테이블·추가 개발**(현 구조에 억지로 흡수하지 않음 — 그게 정상). 어느 경우든 **Device·Clinic(기본)은 불변**, 외부 id는 **확장 레이어**로만 늘어난다. API도 동일하게 **provider 파라미터화**로 확장(특정 provider 하드코딩 금지).

> **`org_mapping` 경계·가정 (오해 방지).** `org_mapping`은 **provider별 로직이 아니라 "얇은 식별자 대응표"**(외부 org id ↔ 우리 clinic)다. provider별 인증·OAuth(→`connector`/`upstream_registry`)·webhook 검증·payload 스키마(→`webhook_provider`·④)는 **이미 별도로 분리**돼 있고, org_mapping은 그중 **가장 공통적인 조각만** 담는다. 따라서 **진짜 확장성은 "만능 org_mapping"이 아니라 "관심사 분리"에서 온다.**
> - **암묵 가정**: 외부 식별자가 ① 단일 평면 id ② clinic과 (provider 내) 1:1 ③ 추가 속성 불요. → 이걸 **위반하는 provider**(계층형 org→다수 site, clinic당 다중 id, provider별 추가 속성)는 **전용 테이블+로직으로 분기**한다. 이는 **설계된 분기이지 실패가 아니다.**
> - **가드레일(분리 신호)**: org_mapping에 **provider 조건 분기·provider 전용 컬럼**을 넣고 싶어지는 순간 = 그 provider를 **전용 테이블로 빼라는 신호**. org_mapping은 "순수 식별자 매핑"으로만 유지.
> - **한 줄**: org_mapping은 "모든 provider가 맞춰야 하는 틀"이 아니라 **"같은 모양 provider를 위한 편의"**. 2번째 provider가 달라도 org_mapping이 아니라 **그 provider 전용 테이블**이 추가될 뿐 기존은 안 깨진다.
- **`provider` 식별자 관리 (R8 확인)**: `provider`는 여러 테이블(`org_mapping`·`webhook_provider`·`webhook_event`…)에서 키로 쓰이므로 **정규 토큰**(소문자 `^[a-z0-9_]+$`, 예 `axs`)으로 관리하고 표기를 통일한다. **enum 금지**(연동 provider는 런타임 추가 → 스키마 고정 부적합). **canonical provider 레지스트리(SSOT)로 FK 강제**할지, `provider`(webhook/org 축)와 `upstream_registry.target_id`(proxy 대상 축, AXS에선 같은 `axs`)를 **하나로 통합**할지는 **R8 결정**(현재 `webhook_provider`가 webhook측 사실상 레지스트리이나 범용 아님 — cleverspace는 proxy 대상이지 webhook provider 아님).
- **region (A안 확정)**: **region SSOT = Clinic**(`clinic_region_mapping`, 1:1). **device의 region은 `device.clinic_id → clinic_region_mapping.region` 파생** — **device.region 컬럼·device-level `region_mapping` 테이블은 제거**(중복·drift 제거, relocation은 clinic 1곳만 변경). region 버전·이력은 `clinic_region_mapping.mapping_version`(FR-RGN-02). §7.3 resolver는 deviceId를 받아도 device→clinic→region으로 해석.
  - **미래(C안 여지)**: clinic 비소속(비-EzServer) device는 파생할 clinic이 없어 device-level region이 필요할 수 있음 → 실제 등장 시 추가(현재 미정의).
- **(미결·논의)** 현재 "clinic" 엔터티는 별도 테이블 없이 `clinic_region_mapping`(클리닉 레지스트리 겸 region 배정)이 대신한다 — **전용 `clinic` 테이블 분리 여부**는 별도 결정(본 A안 범위 밖).

> **DBML·OpenAPI 반영(A안·완료)**: ① `device.clinic_id`(FK→clinic_region_mapping, **nullable**)+인덱스 추가 · ② `device.region` 컬럼·`region_mapping` 테이블 **제거**(clinic 파생) · ③ OpenAPI `Device`에서 `region` 제거·`clinicId` 추가 · ④ `org_mapping`은 (provider, external_org_id) PK라 provider 확장 가능(변경 없음). **미결(별도)**: 전용 `clinic` 테이블 분리 · clinic-less device region(미래).

#### 6.4.2 테이블 조감도 (그룹 수준)

> 관심사별 그룹과 **주요 관계만** 보이는 조감도다(컬럼 없음). **전체 컬럼·관계·제약은 DBML(SSOT)**, 식별 그룹 상세는 §6.4.1.

```mermaid
flowchart TB
    subgraph ID["식별·테넌트 (§6.4.1 상세)"]
        DEV[device]
        CLI["clinic_region_mapping<br/>(= clinic · region 배정)"]
        ORG["org_mapping<br/>(외부 org id · 확장)"]
    end
    subgraph RGN["리전"]
        RC[region_catalog]
    end
    subgraph AUTH["인증·온보딩"]
        ENR[enrollment_token]
        CRED[credential]
        TOK[token]
    end
    subgraph DISP["라우팅·분배"]
        UPS[upstream_registry]
        WP[webhook_provider]
        WE[webhook_event]
        DC[delivery_channel]
        CONN[connector]
    end
    subgraph OPS["정책·운영"]
        POL[policy]
        AUD[audit_log]
        FLEET[fleet_state]
    end

    DEV --> CLI
    ORG --> CLI
    CLI --> RC
    DC --> CLI
    WE --> ORG
    WE --> WP
    CRED --> DEV
    TOK --> DEV
    FLEET --> DEV
    CONN -.-> UPS
    style ID fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
```

- 저장 정보 유형: 디바이스 레지스트리, device/clinic↔region 매핑, 토큰 메타, 정책(OPA 입력), 감사 로그, **webhook 이벤트 수신·분배 상태(`webhook_event`, 멱등·DLQ)**, **분배 지식 레지스트리** — Org-ID↔ClinicID(`org_mapping`, webhook 라우팅 키)·webhook provider 수신 config(`webhook_provider`)·Vatech-Target upstream(`upstream_registry`, 라우팅+per-upstream 복원력 설정)·분배 채널(`delivery_channel`)·**GW 운영 리전 카탈로그(`region_catalog`, §7.3.6)**. **PHI 본문은 미저장**(presigned 직결). **호환성 매트릭스는 DB 미저장** — 소스 파일 → well-known JSON(§7.7.5, `compat_matrix` 테이블 폐기).
- 캐시: **Valkey**(ElastiCache for Valkey·Redis 호환, §1.4)(region 매핑 TTL·nonce·rate-limit·idempotency·JWKS·webhook dedup). **캐시(PG 재구성 가능) + 휘발 상태(nonce·멱등·dedup·rate-limit·lock)이며 SSOT 아님.** 키 패턴·TTL·재구성 출처는 키스페이스 카탈로그 `design/redis/redis-keyspace.md`(DBML과 나란한 설계 산출물)
- **데이터 토폴로지(멀티 서버·멀티 리전, §2.1.1)**: 리전 내 pod는 **동일 DB·Redis 공유**(무상태 앱 tier). 멀티 리전에서는 **(전역 일관) 라우팅·식별 데이터**(매핑·레지스트리·Org-ID·정책·compat·JWKS) 와 **(리전 로컬) 운영 데이터**(audit·in-flight queue)로 나눈다. 전역 데이터는 어느 리전에서도 같은 답을 내야 하며(soft-state 캐시 + strong-consistency 경로·`mapping_version`), 운영 데이터는 리전 로컬이다. **저장소 구현(전역 DB 단일 vs 리전별 복제)은 gw/1.2 TBD(Appendix B #15)**, 구분 원칙은 고정.
- 무결성:
  - 감사 로그 = **append-only**(UPDATE/DELETE 금지, FR-AUD-01)
  - 매핑 변경 = `mapping_version` 증가·이력 보존(FR-RGN-02)
  - idempotency key 유니크 제약(중복 commit/이벤트 방지)
- 보존 기간:
  - **TBD**: 감사 로그·consent 보존 기간
    - 미결 이유: 의료·개인정보 법규(보존 의무 기간) 확인 필요
    - 결정 책임자: ❓ (품질/법무)
    - 결정 마감 시점: baseline 전
    - 영향 받는 섹션: §6.5·§7.9.3·§7.9.5

## 6.5 Business Rules (비즈니스 규칙)

- 데이터 주권: PHI는 매핑된 리전을 벗어나지 않는다.
- 버전 게이팅: originator(`Vatech-*`)와 경유 홉(`Vatech-Via`)을 분리해, **더 낮은 버전 기준**으로 호환 판정.
- egress allowlist: connector별 허용 endpoint만 외부 통신.

## 6.6 Design and Implementation Constraints (설계와 구현 제한사항)

### 6.6.1 Standards Compliance

IEC 62304 / ISO 13485(의료기기 SW), OAuth 2.0 / OIDC, OpenAPI 3.0, ISO 8601(내부 저장은 Unix ms).

### 6.6.2 Other Constraints

BE = NestJS + DDD + TDD, DB = PostgreSQL, ORM = Prisma, CI = Azure Pipelines. (ARD §4.5)

> **IaC 도구 — CDK 권장(확정 TBD).** ARD §4.5 baseline은 `Terraform`이나, **AWS 전용(2026-06-25, Appendix B #20)** 전환으로 Terraform의 멀티클라우드 이점이 사라졌고 조직 실무가 **AWS CDK**이며 **TypeScript로 작성 시 GW(NestJS/TS) 스택과 동일 언어**라 개발자가 인프라 코드를 함께 소유한다 → **CDK 권장**(CloudFormation 합성·AWS 네이티브). 단 IaC 도구·표준은 **인프라(③-I) 소유**이므로 최종 확정·ARD §4.5 정합은 비준 대상(Appendix B #26, 7/2 R5). Terraform 유지 시(모듈 생태계·state·멀티계정 강점) 사유를 명시한다.

## 6.7 Memory Constraints (메모리 제한 사항)

None

## 6.8 Operations (운영 요구사항)

- (대화형) 운영자 kill-switch(FR-FLEET-02)·매핑 재지정(FR-RGN-04)
- (무인) 토큰 자동 갱신·secret 회전(FR-AUTH-03/04)
- 백업/복구 RTO/RPO TBD(인프라 담당)

## 6.9 Site Adaptation Requirements (사이트 적용 요구사항)

사이트(국가/클리닉)별 적용은 **데이터 주권**과 **AWS 가용성**으로 결정된다.

- **리전·주권 적용**: 클리닉은 온보딩 시 region을 자가 등록(§2.3.1)하고, GW는 device/clinic→region resolver(§7.3·ADR-10)로 **PHI를 그 리전 밖으로 보내지 않는다**(§7.3.3·OPA). region 목록은 `region_catalog`(§7.3.6). 1차 단일 리전 → 2차 멀티 리전(gw/1.2·§2.7.1).
- **AWS 미지원 국가**: 별도 GW를 두지 않고 **가장 가까운 AWS 리전 GW에 접속**한다(§2.1.1·§3.1.2). 그 국가의 주권용 storage(예: **MinIO**)는 **GW가 아니라 Provider(CleverSpace/AXS)가 제공**하고 GW는 presigned를 **중계만** 한다(GW는 storage·signer 비소유 — `리전 signer`·Upload Session은 폐기, §7.4·ADR-03/04 철회).
- **DNS**: 클라이언트는 apex(`gw.vatech.com`)만 사용(§4.5.1), GeoDNS가 최근접 리전으로 라우팅.

상세 수치(리전 집합·국가 매핑)는 배포 구성 단계(인프라)에서 확정(§7.3·Appendix B #2).

## 6.10 Internationalization Requirements (다국어 지원 요구사항)

GW는 무인 control plane으로 UI 문자열 거의 없음. 시간은 Unix ms(UTC), 통화 무관. 운영자 메시지 다국어는 ③-C Console 영역. 본 SRS는 `N/A(기능상 해당 없음)` 수준.

## 6.11 Unicode Support (유니코드 지원)

UTF-8(메타데이터·로그)

## 6.12 64bit Support (64비트 지원)

N/A(컨테이너 런타임 64bit 기본)

## 6.13 Certification (제품 인증)

IEC 62304 / ISO 13485 대상(통제 문서 추적성). 인증 일정·준비물은 마케팅·품질팀 협의 — TBD.

## 6.14 Field Test (필드 테스트)

AXS pilot(b1) 연계 — ④ Sub-SRS·개발계획서. 상세 TBD.

## 6.15 Other Requirements (기타 요구 사항)

None

---

# 7 Functional Requirements (기능요구사항)

> 각 대분류는 요구사항 명세의 FR ID를 SSOT로 흡수한다. 우선순위는 §1.3 기준(M·v1.0=P1). 전체 API 스키마는 [OpenAPI](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/design/openapi/vt-api-gateway.openapi.yaml), DB 스키마는 [DBML](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/design/dbml/vt-api-gateway.dbml)이 SSOT이며, 본 장은 기능·동작·에러·경계를 정의한다.

## 7.1 인증·토큰 (P1)

GW는 **두 개의 인증면(surface)을 분리·공존**시킨다(ADR-08): 무인 **EzServer(디바이스, §1.4)의 머신 인증**과 사람·클리닉·사내 호출자의 **OneID(OIDC) 인증**. 두 면은 성질이 달라 단일 인증면으로 묶지 않으며, EzServer↔신원 매핑으로 연결된다.

### 7.1.1 EzServer(디바이스) 머신 인증 (P1)

FR-AUTH-01·05 (OAuth2 `client_credentials`, claim hard binding).

- **Input**: `client_id`/`client_secret`(또는 HW키 바인딩), 요청 scope
- **Trigger**: 디바이스가 작업 전 토큰 발급 요청. **토큰 갱신 = refresh token이 아니라 동일 `client_credentials`로 재발급**(만료 시 디바이스가 자기 자격으로 재인증). RFC 6749 §4.4.3(client_credentials는 refresh token 미발급)에 부합하며, 단명 토큰 + 즉시 revocation(§7.2.4) 모델을 유지한다.
- **Output**: 단명 access token. claim에 `device_id`·`region`·`aud`·`TTL`을 **강제 바인딩**. **refresh token은 발급하지 않는다.**
- **Side Effect**: 토큰 발급 이력 기록(§7.9 감사), Redis에 JWKS·rate-limit 카운터 갱신
- **에러**: 미등록/revoked 디바이스 → 거부(§7.2 lifecycle 연계), secret 불일치 → 401, scope 초과 → 403
- **비목표(Will Not Do)**:
  - **refresh token / `refresh_token` grant 미도입** — 디바이스 머신 인증은 client_credentials 재발급으로만 갱신한다. refresh token은 장수명 자격이라 별도 revocation·회전 관리가 필요해 단명+즉시차단 모델과 상충하므로 도입하지 않는다. (사람·조직의 OIDC refresh 수명주기는 §7.1.4 OneID 도메인이며 디바이스 면과 분리, ADR-08.)
  - DPoP(sender-constrained)·하드웨어 키(SE/TPM) 비추출은 **gw/1.1**(FR-AUTH-06/07). v1.0은 claim 바인딩까지. (secret 재전송 노출 완화는 refresh token이 아니라 이 DPoP+HW키 경로로 해결한다.)

### 7.1.2 사내 호출자 JWT 발급·검증 (P1)

FR-AUTH-02 (EzServer·CleverOne 등 사내 서비스용 JWT 발급·서명 검증).

- **Input**: 사내 호출자 신원(OneID 연계, §7.1.4), 대상 scope
- **Output**: 서명된 JWT. control plane 전 노드가 무상태 검증(soft-state, ADR-02)
- **에러**: 서명 검증 실패 → 401, 만료 → 401(갱신 유도)

### 7.1.3 외부 토큰 저장·갱신·secret 회전 (P1)

FR-AUTH-03·04 (외부(AXS 등) 토큰 암호화 저장·만료 전 자동 갱신, secret dual-window 회전).

- **Output**: 외부 connector(§7.5)가 사용할 유효 토큰. 평문 미노출(KMS)
- **Side Effect**: 만료 전 자동 갱신, secret 무중단 교체(이중 윈도우)
- **에러**: 갱신 실패 시 백오프 재시도 후 connector 호출 차단·알람

### 7.1.4 OneID(OIDC) 연계 — 사람·클리닉·사내 호출자 (P1)

FR-AUTH-08·09 (OneID 토큰 검증·연계, 디바이스 머신 인증 ↔ OneID 신원 분리·매핑, ADR-08).

- **Input**: OneID(OIDC) 토큰
- **Output**: 검증된 사람/클리닉/사내 호출자 신원 + 디바이스 인증면과의 매핑
- **에러**: OneID 검증 실패 → 401. 매핑 부재 → 권한 거부(§7.9 RBAC)

**비목표(Will Not Do)**: 자체 비밀번호·소셜 로그인은 도입하지 않는다 — 사람/조직 인증은 OneID 단일 위임.

## 7.2 EzServer(디바이스) 레지스트리·온보딩 (P1)

> **본 절의 '디바이스'는 EzServer를 가리킨다**(GW 관점, §1.4 — 클리닉당 1개 엣지 머신). 물리 영상장비는 EzServer 뒤편(GW 비대상).

GW는 무인 EzServer를 **레지스트리**로 관리하고, 신뢰할 수 없는 디바이스를 신뢰 가능한 상태로 전환하는 **온보딩(enrollment)** 절차를 제공한다. 온보딩 = enrollment token 발급 = allowlist 등록이며, 등록된 디바이스만 인증(§7.1.1)·작업이 허용된다. 상세 흐름은 ARD §5.1.

### 7.2.1 디바이스 레지스트리·조회 (P1)

FR-DEV-01 (등록·조회 CRUD).

- **Input**: 디바이스 식별·메타(클리닉 소속 포함)
- **Output**: 레지스트리 레코드. 조회/목록(커서 페이지네이션)
- **Side Effect**: 변경 이력 감사(§7.9)

### 7.2.2 allowlist 접근 통제 (P1)

FR-DEV-02 (OPA 기반). 미등록 디바이스 요청 → 차단(403). (§6.5)

### 7.2.3 lifecycle 상태기계 (P1)

FR-DEV-03 (`pending → active → suspended → revoked` 전이·이력).

- **에러/경계**: 허용되지 않은 전이 → 거부, 모든 전이는 이력 보존

### 7.2.4 revocation — 강한 일관성 (P1)

FR-DEV-04 (즉시 차단). revoke 시 캐시 TTL과 무관하게 strong-consistency 경로로 즉시 반영.

### 7.2.5 enrollment 부트스트랩 (P1)

FR-ENR-01·02 (enrollment token = allowlist 등록, 공장 토큰/OOB 일회 코드).

- **Input**: 부트스트랩 신뢰(공장 주입 토큰 또는 OOB 일회 코드, 짧은 TTL·1회)
- **Trigger**: 디바이스 최초 enrollment 요청
- **Output**: allowlist 등록 + 디바이스 자격(client_id/secret, HW키 바인딩) 발급
- **에러**: 신뢰 검증 실패·만료/재사용 토큰 → 거부

### 7.2.6 nonce challenge · fingerprint 바인딩 (P1)

FR-ENR-03·04 (replay 방지 nonce 서명, device fingerprint 바인딩).

- **Side Effect**: 서버 nonce 발급·검증, HW 특성 바인딩 저장

**비목표(Will Not Do)**: geo/velocity 이상탐지(FR-ENR-05)·하드웨어 attestation(FR-ENR-06)은 **gw/1.1**. v1.0은 nonce·fingerprint까지.

## 7.3 리전·라우팅·주권 (P1)

GW는 모든 데이터 경로를 **단일 리전으로 고정**하여 데이터 주권(PHI 리전 밖 미이동)을 보장한다. 라우팅 키는 **device·clinic 양쪽을 동일 resolver가 수용**한다(ADR-10) — 디바이스는 클리닉에 소속되어 같은 리전으로 귀결된다. **리전 매핑은 클리닉 온보딩 시 자가 등록으로 생성**(EzServer가 LMP Clinic-ID 수신 시 자동·무조건 GW 등록 → GW 검증, §2.3.1 — 등록 주체=EzServer 확정)되고, Org-ID 매핑은 **외부 연동 연결 시에만 provider별 등록**(§2.3.5)으로 채워진다 — 운영자 일괄 수기 설정이 아니라 온보딩 산물이며, 오설정은 §7.3.4(FR-RGN-04)로 교정한다.

### 7.3.1 Region Resolver — device/clinic → region (P1)

FR-RGN-01·06 (단일 리전 resolver, resolver가 `device_id`·`clinic_id` 모두 수용).

- **Input**: `device_id` 또는 `clinic_id`(인증된 호출자)
- **Trigger**: 작업(업로드·연동) 직전 region 해석 요청
- **Output**: 매핑된 리전 endpoint + 주권 정책. 두 키 모두 **동일 리전**으로 해석
- **Side Effect**: Redis 매핑 캐시(TTL 초 단위) 조회·갱신
- **에러**: 매핑 부재 → 거부, 캐시 미스 → strong-consistency 경로 폴백
- 상세 흐름: ARD §5.2

### 7.3.2 mapping_version (drift·롤백) (P1)

FR-RGN-02 (매핑 버전 추적). 매핑 변경 시 `mapping_version` 증가·이력 보존으로 drift 감지·롤백 지원.

### 7.3.3 PHI 리전 경계 보장 (P1)

FR-RGN-03 (PHI 리전 밖 미이동). 해석된 리전 외 storage/엔드포인트로의 데이터 이동을 정책(OPA)으로 차단. (§6.1·§6.5 연계)

### 7.3.4 리전 재지정·override + audit (P2)

FR-RGN-04 (relocation, 재동의·감사). 매핑 재지정 시 감사 로그(§7.9)·재동의(consent, FR-COMP-02)를 강제한다.

- **운영 중 변경 주체**: 운영자 override + **클리닉 자가 변경(EzServer Console, 운영 중)** 이 모두 본 경로를 탄다 — 클리닉이 접속할 GW 리전을 **운영 중에도 변경** 가능(§2.3.1·§7.3.6·Roadmap §2.4).
- **부수효과(설계 시 처리)**: (a) **기존 PHI는 옛 리전 storage에 잔류** — 자동 이관 없음(데이터 이관은 별도·v1.0 범위 밖; 옛 객체는 옛 리전 참조). (b) **국경 간이면 재동의·주권 재평가**(FR-COMP-02). (c) **in-flight 업로드/세션**은 발급 주체(CleverSpace/AXS) 측에서 옛 리전으로 완료, 전환은 신규부터. (d) `mapping_version`++ · strong-consistency 전파(§7.3.1/2)로 즉시 반영. → **라우팅·운영은 무중단**이나 데이터 이관·동의는 별도 처리.

### 7.3.5 GeoDNS 연계 (P1)

Route 53 GeoDNS로 Edge(EzServer)를 최근접 GW 리전에 연결한다. 호스트명은 §4.5.1 참조. **GeoDNS·고정 egress IP·K8s 배치는 인프라 담당 영역**이며, 본 SRS는 *GW가 전제하는 연계 계획·요구*만 기술한다(§3.1·§2.6).

- **단계화(§2.7.1)**: **v1.0(단일 리전)에서도 클라이언트는 apex(`gw.vatech.com`)만** 호출하고, apex가 그 단일 리전을 가리킨다(GeoDNS 백엔드 1개). **2차(gw/1.2)에 백엔드를 N리전으로 늘리면** apex 라우팅이 자동으로 최근접 리전 분배로 동작 — **클라이언트·헤더 변경 없음**. 즉 GeoDNS는 v1.0부터 *구성상 존재*하되 라우팅 대상이 1개일 뿐이다(멀티리전-ready).

**비목표(Will Not Do)**: 멀티 리전 _동시 운영_(FR-RGN-05)는 **gw/1.2(2차)**. v1.0은 **단일 리전만 배포**한다 — 단 위 단계화대로 멀티리전-ready로 설계한다(§2.7.1).

### 7.3.6 GW 리전 카탈로그·조회 (P1)

GW가 **운영 중인 리전 목록**을 조회 API로 제공한다 — 클라이언트(EzServer Console 등)가 온보딩·운영 중 region 선택지를 표시·선택하기 위함이다.

- **API**: `GET /v1/regions` — 운영 리전 목록(region_id·표시명·endpoint·status[active/draining/planned]). 호스트 §4.5.1.
- **DB**: `region_catalog` 테이블(§6.4)이 SSOT — v1.0은 **단일 리전 1행**, 2차(gw/1.2)에 N행으로 확장(§2.7.1 멀티리전-ready). `clinic_region_mapping.region`은 이 카탈로그를 참조한다.
- **상태 전이**: `draining`(신규 등록 차단·기존 유지)·`planned`(목록 비노출) 등으로 점진 추가/회수 지원.

## 7.4 파일 업로드 — presigned 중계 (P1) — **GW 비발급**

**GW는 presigned URL을 발급하지 않고, 업로드 세션·storage를 소유하지 않는다.** 파일 업로드 presigned **발급 주체는 CleverSpace(경로②)·AXS(경로③)** 이며, GW는 발급 요청을 **중계(B/C bypass, §4.1.4)** 할 뿐이다. 파일 **바이트**는 발급 주체의 storage로 **직접** 업로드한다(GW 미경유, PHI control plane 미경유).

> **위임 경계**: 업로드 **세션(start→chunk→commit)·resumable/multipart·idempotency·checksum/ETag·완료처리(콜백+스토리지 이벤트)** 는 **발급 주체의 책임**이다 — CleverSpace presign은 **② Presigned One Pager**·CleverSpace OpenAPI, AXS presign·파일은 **④ Sub-SRS**·AXS 스냅샷이 정본. 본 SRS(GW)는 이를 정의하지 않는다.

**FR-SES 매핑(요구사항 명세)**: FR-SES-01~05(세션·presigned·resumable·멱등·무결성)는 **GW 직접 구현이 아니라 발급 주체(CleverSpace ②/AXS ④) 소유**다. GW 책임은 _중계_(§4.1.1 B/C 프록시·§7.5 connector)로 한정한다. FR-SES-06(멀티클라우드 presign broker)도 GW가 broker를 두지 않으므로 해당 없음.

**비목표(Will Not Do)**:

- **GW가 presigned를 직접 발급**(Region Signer·GW 소유 region storage·GW Upload Session) — **폐기**(2026-06-23 결정. 기존 경로①·ADR-03/04 철회). GW는 서명·세션·storage를 갖지 않는다.
- CleverSpace·AXS presign을 GW가 하나의 API로 통합·변환 — §4.1.4, B/C bypass(verbatim).

## 7.5 외부 연동·Connector 프레임워크 (P1)

GW는 외부 시스템 연동을 **플러그형 connector(adapter)** 로 추상화하고, connector별 **egress 정책·endpoint allowlist**로 외부 통신을 통제한다.

> **경계**: AXS connector의 *연동 의미·OAuth·Org-ID 매핑·Webhook 이벤트 상세*는 **④ Straumann AXS Sub-SRS**. 본 절은 *프레임워크와 egress 통제*만 정의한다.

### 7.5.1 Connector 프레임워크 (P1)

FR-INT-01 (adapter 플러그형 등록).

- **Output**: 신규 connector를 설정 기반으로 등록(코드 변경 최소)
- **라우팅**: §4.1.2 target-routed proxy를 따른다 — connector 등록 = **레지스트리 1행**(논리 ID(예 `axs`)→host + trust profile `external` + egress allowlist). 내부 proxy(B)와 **동일 라우팅 메커니즘**이며 trust profile만 `external`이다. 신규 외부 연동(DS Core/3Shape 등) 확장 시 경로 네임스페이스·GW 코드 변경 없이 레지스트리 등록만으로 추가(NFR-SCL §6.3.5).
- **Side Effect**: connector 토큰 저장·갱신은 §7.1.3 위임

### 7.5.2 AXS connector (P1)

FR-INT-02 (Straumann AXS OAuth2·proxy·**파일/presign API bypass**의 _프레임워크 적용 지점_). AXS presign·파일 요청 body는 **AXS OpenAPI 그대로 통과**(§4.1.4 경로③) — GW가 발급하거나 해석·변환하지 않음. E2E 동작 요구만 본 절에 두고, 상세 계약은 ④.

> **AXS = GW의 첫 연동 구현 대상**(CleverSpace보다 **선행** — PRD §12·Roadmap §3.5, 2026-06 회의 재확인). 범용 proxy·Webhook 구조(§4.1.1·§7.6)를 외부 서비스로 먼저 검증한 뒤 CleverSpace 연동을 진행한다. 스펙 작성 순서(③ baseline 후 ④)와 구현 착수 순서(Straumann 먼저)는 별개다.

### 7.5.3 egress 정책 + endpoint allowlist (P1)

FR-INT-03 (허용 대상만 외부 통신). allowlist 외 egress는 OPA로 차단(§6.5).

**비목표(Will Not Do)**: 추가 connector(DS Core/3Shape, FR-INT-04)는 **gw/1.1**(설정 추가로 확장).

### 7.5.4 프록시 복원력 — 타임아웃·재시도·업스트림 오류 (P1)

FR-INT-05 (target-routed proxy(§4.1.2)의 **동기 전달 구간** 복원력 — 타임아웃·재시도·서킷·오류 매핑). 동기 프록시(B/C)는 Webhook **비동기 큐(A·재시도/DLQ, §7.6.3)와 다른 레그**다 — 응답을 기다리는 호출자가 있으므로 큐잉이 아니라 **deadline·즉시 오류**로 다룬다. 수치(타임아웃·재시도·서킷 임계)는 upstream SLA·인프라 입력 의존 **TBD**(Appendix B #25, 주간회의 7/2 R4).

- **타임아웃 계층(핵심).** GW는 *서버*이자 *클라이언트*다. **`GW upstream 총 deadline < downstream 클라이언트 타임아웃`** 이어야 한다 — 아니면 클라이언트가 먼저 포기해도 GW는 upstream 응답을 계속 기다려 **고아 요청·커넥션/워커 점유·재시도 증폭**이 생긴다. GW는 클라이언트보다 **먼저 504를 반환**해 결정적 오류를 준다.
  - **per-upstream 레지스트리(`upstream_registry`) 설정**: `connect_timeout_ms`(TCP+TLS 핸드셰이크, 짧게)·`response_timeout_ms`(응답 대기)·`total_deadline_ms`(전체 예산). upstream·작업 유형별로 다르게(값 TBD). 대용량 파일은 **presigned 직결**(GW 미경유, §4.1.4)이라 본 deadline은 control·metadata 중심.
  - **클라이언트 조기 절단 → upstream 호출 취소**(cancellation 전파)로 자원 회수.
  - **클라이언트 타임아웃 인지.** HTTP는 클라이언트 타임아웃을 표준 전달하지 않는다 — GW는 연결 close로 *사후*에만 안다. "GW가 먼저 504"를 보장하려면 값을 *사전*에 알아야 하므로, v1.0은 **(A) 계약값 합의**(EzServer↔GW, SRS 명시)를 기본으로 하고, 클라이언트가 **선택적 `Vatech-Timeout-Ms` 헤더(상대값)** 를 보내면 GW가 내부 deadline을 `now + min(헤더, 설정값)`으로 클램프한다(B). 헤더는 **상대 timeout**(클록 동기 불필요 — gRPC `grpc-timeout`·Envoy `x-envoy-expected-rq-timeout-ms` 선례)이며, "deadline"은 GW 내부 절대시각 개념으로 구분한다. 합의 방식·헤더 채택은 TBD(Appendix B #25, 7/2 R4-D10).
- **재시도 정책(보수적).** GW는 **타겟당 단일 upstream(레지스트리 1행)** 을 중계하는 verbatim relay라 — 로드밸런싱 풀처럼 _다른 인스턴스로_ 넘길 대상이 없다 — 재시도를 **최소화**한다. 기본은 **연결 수립 실패(요청 바이트 전송 전)에 한해 1회 재시도**(요청이 upstream에 도달 전이라 POST 포함 전 메서드 안전; HAProxy 기본·nginx 1.9.13+ 비멱등 보호와 같은 보수적 입장). **응답 타임아웃(요청 전송 후)·upstream 5xx는 GW 재시도 안 함** — upstream이 이미 처리했을 수 있어 멱등이라도 위험. **애플리케이션 레벨 재시도는 클라이언트가 소유**한다(idempotency key·업무 의미를 클라이언트가 가장 잘 안다). (옵션: 멱등 GET류의 응답 전 타임아웃 재시도 추가 가능하나 v1.0 비포함 권장.) 재시도 활성 시 지수 백오프+jitter+retry budget으로 폭주를 막는다. 소유·범위 결정은 R4-D5(값 TBD).
- **서킷 브레이커(per upstream).** 연속 실패 임계 초과 시 회로 개방 → **빠른 실패 `503`(+`Retry-After`)**, 반열림 탐침으로 복구. v1.0 기본 포함(임계·복구 파라미터 TBD; 구현 부담 시 일부 gw/1.1로 이월 — 7/2 R4 결정).
- **상태 지역성(멀티 서버).** 서킷·재시도·타임아웃의 **런타임 상태(open/closed·실패 카운터)는 pod-local in-memory**이며 **GW pod 간 공유하지 않는다**(DB·Redis·GW간 동기화 미사용) — 각 pod가 자기 관측 기반으로 보호하는 것이 표준(Resilience4j·Envoy per-instance)이고, hot-path에 원격 상태 의존을 두면 빠른 실패 목적과 모순된다. **공유 대상은 설정값뿐**(`upstream_registry`의 임계·타임아웃·on/off, pod별 읽어 캐시). 별도 복원력 컴포넌트를 두지 않고 `ROUTER`/`CONN` 데이터 경로의 in-process 행위로 구현한다(§2.2).
- **업스트림 오류 → 클라이언트 매핑(상세 표 §7.7.4).** **GW 생성 오류**(`502` 연결 실패 / `504` 타임아웃 / `503` 서킷·일시불가)는 **GW 표준 error envelope**, **upstream 자체 4xx/5xx**는 **verbatim 통과**(body 미변형). **`Vatech-Error-Origin: gateway|upstream`** 마커로 책임을 구분하고, GW 생성 시 `Vatech-Upstream-Latency-Ms` 등 관측 헤더를 부가한다.
- **관측(§6.3.2 연계).** 로그/메트릭에 `upstreamLatencyMs`·`upstreamStatus`·`retryCount`·`timeout`(bool)·`circuitState`를 남겨 장애 시 원인(어느 upstream·타임아웃·서킷)을 즉시 식별한다.

- **에러**: upstream 연결 불가 → `502`(`Vatech-Error-Origin: gateway`), deadline 초과 → `504`, 서킷 개방/일시 불가 → `503`(+`Retry-After`). upstream 자체 오류 → 원응답 **verbatim 통과**(`Vatech-Error-Origin: upstream`). 비멱등 요청은 재시도 없이 즉시 반환.

## 7.6 Webhook 수신·이벤트 분배 (P1)

GW는 외부 이벤트의 **단일 수신·분배점**이다(ADR-09). 방화벽 뒤 Edge(EzServer)는 inbound가 불가하므로, GW가 대신 수신·검증·멱등 처리 후 대상별로 분배한다. 서비스별 개별 수신을 금지하여 서명·IP·멱등 검증의 분산을 막는다.

### 7.6.1 유연 수신 엔드포인트 (P1)

FR-WH-01 (외부 이벤트 수신면 — **provider별 전용 호스트** `{provider}.webhook.gw.vatech.com`, §4.5.1). **발신자 식별은 Host/SNI**(레지스트리 `inbound_host`)로 하며 상대 source IP에 의존하지 않는다. **경로·형식은 provider 규약을 수용하는 유연·레지스트리 기반**이며 GW가 강제하지 않는다(§4.1.3). GW는 _누가 보냈는지_ 만 검증하고 payload는 소비자가 해석한다.

- **Input**: 외부(AXS 등) 이벤트 — HTTPS POST
- **Output**: 즉시 `2xx` ACK(§7.6.3)
- **에러**: 미지원 provider → 404, 페이로드 형식 오류 → 400

### 7.6.2 수신 검증 (P1)

FR-WH-02 (**식별** = Host/SNI → 레지스트리 `inbound_host`로 provider·검증 시크릿 선택; **인증** = HMAC 서명 + timestamp replay 방지; source IP allowlist는 **옵션·방어심층**). **호스트명은 식별이지 인증이 아니다** — 신뢰는 HMAC으로 보장한다.

- **에러**: 미등록 Host/서명 불일치/timestamp 만료 → 401·거부(부정 호출 차단). IP allowlist 사용 시 미허용 → 거부(옵션)
- **검증 config 관리**: provider별 `inbound_host`·`sig_scheme`·`secret_ref`(KMS 참조)·`source_ip_allowlist`(**CIDR 목록**, 옵션)는 **관리 API `/admin/v1/webhook-providers`(§7.9.1)로 등록·갱신**한다. **편리한 입력 UI(CIDR 검증·일괄 입력 등)는 ③-C Console**(GW는 API 계약까지).

### 7.6.3 빠른 ACK + 내부 큐 (A · SQS) (P1)

FR-WH-04 (검증 직후 `2xx` 즉시 응답, 처리는 **내부 비동기 큐(A)** 로 위임 — 재시도·백오프·DLQ). **내부 큐 기본 = Amazon SQS**(서버리스·IRSA·DLQ 내장, 순서/dedup 필요 시 SQS FIFO; 대안 Amazon MQ, §3.1.2). 이 큐는 **GW 내부 버퍼**이며, 클리닉으로의 마지막 구간 전달은 §7.6.6 엣지(B·MQTT)가 담당한다 — **둘은 별개 레그**다. **큐에서 꺼내(consume) 대상으로 발행하는 주체는 Webhook Dispatcher(§7.6.7)** 다 — 큐는 스스로 push하지 않는다.

- **Side Effect**: 큐(SQS) 적재. 처리 실패 N회 → DLQ 이동·알람

### 7.6.4 멱등 처리 (P1)

FR-WH-03 (`eventId` dedup — 중복 수신 1회만 반영).

- **에러/경계**: 동일 `eventId` 재수신 → 저장된 결과 반환(중복 처리 0)

### 7.6.5 클라우드 분배 — HTTP push (P1)

FR-WH-05 (클라우드 대상에 내부망 HTTP push, 순서 보존). **클라우드 수신 대상은 CleverLab만**(갈래 B·현 시점 보류, §1.2). **CleverSpace는 webhook 수신 대상이 아니다**(B 프록시·presigned 백엔드 — 대상 아님으로 확정, §2.3.6). 대상별 시나리오는 §2.3.6.

- **TBD — CleverLab 갈래 B 활성화 여부·시점**(PM/제품). 본 절은 *HTTP push 메커니즘*만 정의하고, 활성화 시 받을 이벤트(오더·확정 결과)는 ④에서 확정한다(Appendix B #16). (CleverSpace는 대상 아님 — 조사 불요.)

### 7.6.6 Edge 분배 — EzServer MQTT 역방향 (B) (P1)

FR-WH-06 (EzServer로 **MQTT QoS1·persistent**, 토픽=클리닉 단위). 오프라인 시 버퍼 후 재전달. b1(pilot)에 forward + 역방향 포함(AXS pilot 일정). **엣지 전달(B)에 SQS를 쓰지 않는다** — EzServer는 방화벽 뒤라 inbound 불가하고 **outbound 지속 구독(subscribe)으로 push받아야** 하므로 MQTT가 필수다(SQS 폴링·자격 배포는 부적합). 발행 주체는 **Webhook Dispatcher(§7.6.7)** 이며, EzServer가 브로커에 구독해 push받는다. **브로커 후보 = AWS IoT Core / Amazon MQ**(방화벽 뒤 엣지·cert 인증·fleet 규모). 제품·운영 주체 **TBD**(§3.1.2·Appendix B #4). 내부 큐(A·SQS, §7.6.3)와 **별개 레그**다(A=SQS pull 버퍼, B=MQTT push — 역할·서비스 분리).

### 7.6.7 Webhook Dispatcher — 분배 워커(SQS consumer) (P1)

FR-WH-07 (수신과 분배를 잇는 **Webhook Dispatcher**). §7.6.3 큐(A·SQS)에 적재된 이벤트를 **소비(consume)** 해 대상별로 발행하는 GW 컴포넌트다 — 큐는 스스로 push하지 못하므로, Webhook Dispatcher가 §7.6.5(HTTP push)·§7.6.6(MQTT) 전달을 수행한다.

- **구현 = GW와 동일 코드베이스의 별도 worker Deployment(ADR-12)** — HTTP 서버 없이 SQS consumer만 실행. API tier와 **독립 스케일(SQS 큐depth, KEDA)·장애 격리**하되 코드·도메인 모델·커넥터·시크릿을 공유(드리프트 0, 단일 검증 스택). v1.0은 고정 replica로 시작, 볼륨 증가 시 오토스케일. (서버리스 Lambda 대안은 로직·DB·시크릿·egress 중복과 2nd 런타임 검증 부담으로 반려 — ADR-12.)
- **동작**: SQS pull → **대상 해석**(`org_mapping` Org-ID→Clinic → `clinic_region_mapping`→region → `delivery_channel`→채널·엔드포인트, §6.4·§7.3) → Edge면 **MQTT publish(IoT Core, §7.6.6)** / 클라우드면 **HTTP push(§7.6.5)** → 발행 성공 시 메시지 삭제. **교차 리전**(수신 리전 ≠ 대상 리전) 전달 포함.
- **멱등·신뢰성**: `eventId` dedup(§7.6.4)으로 중복 발행 방지. 발행 실패 → **재시도·백오프, N회 초과 → DLQ·알람**(§7.6.3). 처리 단위 멱등이라 at-least-once 소비에도 중복 부작용 0.
- **에러**: 대상 미해석(매핑 부재) → DLQ·알람. MQTT/HTTP 발행 실패 → 재시도 후 DLQ.

**비목표(Will Not Do)**: 본 절은 *수신·분배 프레임*만 정의한다. AXS 이벤트의 _의미·매핑(Org-ID↔ClinicID 등)_ 상세는 ④ Sub-SRS. 경로 B(CleverOne→CleverSpace 직결)는 Webhook 분배로 흡수 후 EOS(§2.8).

## 7.7 API 버전 호환성 게이트 (P1)

구버전 클라이언트(CleverOne/EzServer)가 확장된 CleverSpace API를 인식하지 못해 발생하는 **원인불명 실패를 제거**한다(ADR-07). originator(`Vatech-*`)와 경유 홉(`Vatech-Via`)을 분리 판정하여 *가장 낮은 버전 기준*으로 호환성을 게이팅한다.

> **경계**: 제품측(CleverOne/EzServer의 헤더 부착, CleverSpace의 well-known 적용) 변경 상세는 **① API 호환성 One Pager**. 본 절은 *GW 게이트의 판정·공시·매트릭스 집행*만 정의한다. 1단계는 GW 신설 전에도 기존 경로(서버 직접 판정)에서 즉시 적용(ADR-07).

### 7.7.1 Vatech-\* 식별 헤더 표준 (P1)

FR-COMPAT-01 (`Vatech-Product`·`Version`·`OS`·`Clinic-Id`·`Via` 파싱, originator 식별).

- **필수성**: `Vatech-*` 식별 헤더 + 표준화된 `User-Agent`는 **모든 제품(CleverOne·EzServer 등)의 모든 요청에 필수**다(2026-06 회의 — 전 제품 강제). 클라이언트는 **공용 라이브러리**로 부착을 표준화한다(제품별 구현 상세·라이브러리는 ① One Pager·③-P-\* 영역, 본 SRS는 GW 집행만).
- **originator vs 경유 홉(분리·누적)**: `Vatech-Product`/`Version`/`OS`는 **요청을 시작한 주체(originator)** 의 권위 소스다. 경유 중계 홉(EzServer 등)은 **자기 자신을 `Vatech-Via`에 누적**하고(홉이 여럿이면 콤마 누적), `User-Agent`는 **직전 송신자**(예 EzServer)를 싣는다. 예: CleverOne→EzServer→GW이면 `Vatech-Product: CleverOne` + `Vatech-Via: EzServer/x` + `User-Agent: EzServer/x`. 머신 판정은 전용 헤더로 하고 `User-Agent`는 로그·관측·하위호환용이다. 규칙 상세는 Roadmap §5·§5.1.
- **Input**: 요청 헤더(originator 권위 `Vatech-*` + 경유 홉 `Vatech-Via` + 직전 송신자 `User-Agent`)
- **Output**: 식별된 originator 제품·버전·OS·클리닉 (다중 홉 시 originator·경유 홉 버전을 모두 확보 → 더 낮은 버전 기준 게이팅 §7.7)
- **에러**: 필수 헤더 누락 → 표준 오류(§7.7.4)

### 7.7.2 well-known 런타임 버전 공시 (P1)

FR-COMPAT-02 (API/기능별 최소 클라이언트 버전을 런타임 공시·캐시).

- **경로**: `/.well-known/<env>/server-configuration.json` (env별 구분). 스키마 상세는 OpenAPI(§4.1)·① One Pager와 동기화
- **샘플·작성 가이드**: `design/well-known/`(`server-configuration.sample.json` + `README.md`) — 담당 개발자가 호환성 매트릭스에서 값 채움

### 7.7.3 서버 버전 체크 — validate-limits 사전검증 (P1)

FR-COMPAT-03 (요청 전 버전 게이팅).

- **Output**: 지원 시 통과 / 미지원 시 차단

### 7.7.4 오류코드 매핑·fallback (P1)

FR-COMPAT-04 (미지원 시 표준 오류코드 + "업데이트 필요" fallback 안내).

**프록시(B/C) 업스트림 오류 매핑(§7.5.4 연계).** GW가 *생성*하는 오류와 upstream이 _돌려준_ 오류를 구분한다 — 전자는 GW 표준 envelope, 후자는 verbatim 통과. `Vatech-Error-Origin` 헤더로 책임 주체를 표시한다.

| 상황 | HTTP | 본문 | `Vatech-Error-Origin` |
| --- | --- | --- | --- |
| upstream 연결 실패(거부·DNS·TLS) | `502` Bad Gateway | GW envelope(`UPSTREAM_UNREACHABLE`) | `gateway` |
| upstream 응답 지연 — GW deadline 초과 | `504` Gateway Timeout | GW envelope(`UPSTREAM_TIMEOUT`) | `gateway` |
| 서킷 개방 / upstream 일시 불가 | `503` Service Unavailable(+`Retry-After`) | GW envelope(`UPSTREAM_UNAVAILABLE`) | `gateway` |
| 라우팅 실패(`Vatech-Target` 누락/미등록/allowlist 외) | `400`/`404`/`403` | GW envelope | `gateway` |
| upstream이 자체 4xx/5xx 응답 | upstream 원 코드 | **upstream body verbatim**(GW 미변형) | `upstream` |
| 클라이언트 조기 절단 | (응답 없음) | — GW가 upstream 호출 취소 | — |

> **원칙**: GW 생성 오류만 GW envelope를 쓰고, upstream 응답은 코드·body를 **그대로 통과**(verbatim bypass 일관성, §4.1.2-3). 호출자는 `Vatech-Error-Origin`으로 "GW가 못 갔다(gateway)" vs "대상이 거부했다(upstream)"를 구분한다. 자동 재시도는 멱등 요청·연결/pre-response 타임아웃 한정(§7.5.4).

### 7.7.5 호환성 매트릭스 단일 소스 (P1)

FR-COMPAT-05 (매트릭스를 단일 소스로 동결, 빌드/CI 반영·검증). 매트릭스 확정본은 ① 산출물과 동기화(§2.8).

> **SSOT = 소스 파일(DB 아님).** 호환성 매트릭스는 **릴리스에 묶인 정적 설정**이라 **레포 소스(① One Pager 동기화)를 SSOT로 두고, 빌드/CI로 `/.well-known/{env}/server-configuration.json` 생성·공시**한다(런타임 조회는 파일/캐시). **DB 테이블로 두지 않는다**(런타임 임의 변경이 버전 게이팅을 깨는 것 방지 — `compat_matrix` 테이블 폐기, 2026-07-01). 긴급 클라이언트 버전 차단이 필요하면 일반 테이블이 아니라 **Config push(§7.8.4)** 로 처리한다.

**비목표(Will Not Do)**: 클라이언트 자동 업데이트·강제 설치는 본 게이트 범위 밖(클라이언트 제품 영역).

## 7.8 Fleet 운영·Config (P1)

10만대 규모 디바이스 운영을 1급 서브시스템으로 다룬다(ADR-06). 본 v1.0은 가시성·긴급 정지·중앙 config의 *기본 기능*을 제공한다.

### 7.8.1 디바이스 heartbeat·상태 가시성 (P1)

FR-FLEET-01 (health 수집).

- **Output**: 디바이스 상태·health 대시보드용 지표(관리 API §7.9 / Console ③-C)

### 7.8.2 kill-switch — 긴급 정지 (P1)

FR-FLEET-02 (즉시 정지).

- **Trigger**: 운영자가 디바이스/그룹 긴급 정지
- **Side Effect**: 해당 디바이스 작업 즉시 차단(revocation 경로 연계 §7.2.4)

### 7.8.3 upload 성공률·오류 분포 지표 (P2)

FR-FLEET-03 (지표 노출).

### 7.8.4 중앙 Config push/pull (P1)

FR-CFG-01 (타겟팅 원격 적용).

- **Input**: config 페이로드 + 타겟(디바이스/그룹/리전)
- **Output**: 원격 적용. 디바이스는 pull 또는 push 수신
- **에러**: 적용 실패 시 이전 config 유지·재시도

**비목표(Will Not Do)**: config rollout/카나리(FR-FLEET-04)는 **gw/1.1**, 10만대 운영 최적화(FR-FLEET-05)는 **v2.0**.

## 7.9 관리·감사·컴플라이언스 (P1)

운영자 관리 기능은 **MVP 경량**으로 구현한다(심도 정책). UI 상세는 ③-C, 본 절은 *관리 API·권한·감사·컴플라이언스 규칙*을 정의한다.

> **경계**: 관리 화면·플로우(매핑·클리닉·상태·온보딩 UI)는 **③-C GW Console Sub-SRS**. 본 절은 Console이 호출하는 *관리 API와 정책*만.

### 7.9.1 테넌트·키·디바이스 관리 API (P1)

FR-ADM-01 (CRUD API, MVP 경량). Console(③-C)이 호출. 테넌트·키·디바이스에 더해 **분배 지식 레지스트리 관리** 포함 — Org-ID↔ClinicID 매핑(`/admin/v1/org-mappings`)·webhook provider(`/admin/v1/webhook-providers`)·Vatech-Target upstream(`/admin/v1/upstreams`). 전체 스키마는 Swagger.

### 7.9.2 운영자 RBAC (P1)

FR-ADM-02 (권한 분리, 경량). 역할별 수행 가능 기능 제한(§6.5). 운영자 인증=OneID(§7.1.4).

- **Console 사용자 역할 = Admin + C/S.** **Admin**=전체 관리·매핑 교정(override). **C/S(현장 설치 담당)**=설치 후 **클리닉 GW 등록 확인** 등 조회 위주(§2.3.1). **역할 정의·화면·세부 권한은 ③-C GW Console Sub-SRS**에서 확정 — 본 SRS는 관리 API·역할 존재까지.
- **에러**: 권한 외 호출 → 403

### 7.9.3 감사 로그 — append-only (P1)

FR-AUD-01 (변조 방지·보존).

- **Side Effect**: 모든 관리 변경(operator id·timestamp·before/after·IP)을 append-only로 기록
- **경계/보존**: 보존 기간은 TBD(§6.4, 책임자 ❓, 마감 ❓, 영향: §6.4·§7.9.3)

### 7.9.4 data classification tagging (P1)

FR-COMP-01 (분류 태깅 → OPA 게이팅, 경량).

### 7.9.5 cross-border consent tracking (P1)

FR-COMP-02 (국경 간 동의 추적, v1.0~v2.0). 리전 재지정(§7.3.4) 시 재동의 연계.

**비목표(Will Not Do)**: 고급 감사 분석·리포트 자동화는 본 v1.0 범위 밖(MVP 경량 유지).

---

## Appendix A. Decision Log

| 일시 | 결정 사항 | 채택안 | 비교 대안 | 채택 이유 | 결정자 | 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-06-08 | 디바이스 인증 | DPoP + HW키 | mTLS | 10만대 부담·키추출 위협 | Scott | ADR-01 |
| 2026-06-08 | Control plane 상태 | soft-state | full stateless | cache TTL·mapping_version | Scott | ADR-02 |
| 2026-06-15 | 버전 호환 | 헤더+well-known+매트릭스 | 클라이언트 버전 미전달 방치 | 원인불명 실패 제거 | Scott | ADR-07 |
| 2026-06-15 | 인증 2면 | 디바이스 머신 + OneID 공존 | 단일 인증면 | 무인/사람 신원 성질 다름 | Scott | ADR-08 |
| 2026-06-15 | Webhook | 단일 수신·분배(HTTP/MQTT) | 서비스별 개별 수신 | 검증 분산·Edge inbound 불가 | Scott | ADR-09 |
| 2026-06-15 | 라우팅 키 | device↔clinic↔region 통합 | 이원화 | 동일 리전 귀결 | Scott | ADR-10 |
| 2026-06-23 | 라우팅 모델 | target-routed proxy(`Vatech-Target` 유무로 GW-own/proxy 구분, proxy는 verbatim) | 경로 네임스페이스 라우팅 / 투명 프록시 / 클라이언트 지정 upstream | upstream 무한 확장을 설정(레지스트리 1행) 기반으로 — 코드·경로 변경 0(NFR-SCL), 내부·외부 단일 규칙 | PM/아키텍트(**CCB 승인 2026-06-25**) | ADR-11 |
| 2026-06-23 | 리전 구축 단계화 | **1차 단일 리전(gw/1.0) → 2차 멀티 리전(gw/1.2)**, 단 v1.0부터 멀티리전-ready 설계 | 처음부터 멀티 리전 / 단일 리전 고정(확장 시 재작업) | 리스크·비용 낮추되 2차 확장을 재설계 없이(설정·배포 증분). 기존 "gw/1.0 흡수 여부 TBD"(B#7) 종결 | PM/아키텍트 | §2.7.1·§4.5.1·§7.3.5 |
| 2026-06-30 | Webhook Dispatcher(분배 워커) | **별도 worker Deployment**(GW와 동일 코드베이스·HTTP 없이 SQS consumer만, 독립 스케일 KEDA·장애 격리) | 기존 GW 모듈 in-process(부하·스케일 결합) / 서버리스 Lambda(로직·DB·시크릿·egress 중복, 2nd 런타임 검증 부담) | 코드·도메인·커넥터·시크릿 공유(드리프트 0·단일 검증 스택) + API와 독립 스케일·격리. webhook은 버스트성이라 분배만 큐depth로 확장 | 아키텍트/GW 리드 | ADR-12 · §2.2·§2.3.6·§7.6.7 |

> 전체 ADR(01~11)·근거는 ARD §2. 본 표는 SRS 차원 핵심 결정 요약. **ADR-11은 ARD §2에 기재(v0.10) · CCB 승인 완료(2026-06-25)**(Appendix B #13). **라우팅 방식 4안 다기준 비교·결정 표는 §4.1.2**(헤더 vs 경로 vs 서브도메인 vs 클라이언트 지정).

## Appendix B. TBD·미결 항목 추적

> baseline 전 닫아야 할 결정 항목. 본문 각 절의 TBD를 한 곳에 모은 추적표(본문이 정본, 본 표는 인덱스). 설계 단계의 단순 버전·도구 TBD(§3·§4.4)는 묶어 1행으로 둔다.

### B-1. 완료·확정 (닫힌 결정 — 참고용. 번호는 추적 보존)

| # | 항목 | 결정 | 본문 |
| --- | --- | --- | --- |
| 7 | 멀티 Region·멀티클라우드 gw/1.0 흡수 | **1차 단일 / 2차(gw/1.2) 멀티 리전, v1.0 멀티리전-ready**(2026-06-23). 잔여=2차 구축 *시점*만 | §2.7.1 |
| 10 | CCB 명단·승인자 | **승인=Scott(실장·총괄)·Raymond(GW 백엔드 리드) 확정**; QA·보안·인프라 사안별 옵저버. **PM은 미지정(별도 지정 가능) — 'Scott=PM' 아님**(Scott=현재 전체 관리자/실장) | §8·§9 |
| 17 | 클리닉 GW 등록 주체 | **확정(2026-06-25): EzServer(클리닉당 1개)가 LMP Clinic-ID 수신 시 자동·무조건 GW 등록**(연동 무관). CleverOne 대안 폐기 | §2.3.1·§7.3 |
| 19 | 디바이스 정의·연결 모델 | **확정(2026-06-25): GW 관점 디바이스=EzServer**(물리 영상장비는 EzServer 뒤·GW 비대상, 직접 연결 없음). Agenda #1 종결 | §1.4·§2.3.2·§7.1·§7.2·ADR-08 |
| 20 | GW 배포 클라우드 | **확정(2026-06-25): AWS 전용**(비AWS GW 없음·AWS 미지원국은 가까운 AWS GW 접속, 주권 storage=Provider MinIO 중계). 비AWS 포터블 배포(§2.1.2 초안) 폐기 | §2.1.1·§3.1.2 |
| 21 | GW Console 사용자 역할 | **확정(2026-06-25): Admin + C/S**(C/S=설치 후 클리닉 등록 확인). 화면·세부 권한은 ③-C Console Sub-SRS 위임 | §7.9.2·§2.3.1 |
| 22 | 업로드·presigned 모델 | **확정(2026-06-23): GW 비발급·중계만**(발급=CleverSpace②/AXS③). `/v1/uploads`·리전 Signer·Upload Session 폐기 | §4.1.4·§7.4·ADR-03/04 |
| 23 | DNS apex 호스트명 | **확정(Scott, 2026-06-24): `gw.vatech.com`**(클라이언트 유일 호스트, GeoDNS apex) | §4.5.1 |
| 13 | 라우팅 모델 ADR-11 (target-routed proxy) | **CCB 승인 완료(2026-06-25)** · ARD 기재(v0.10). 잔여(구현)=클라이언트 `Vatech-Target` 부착(③-P-\*, 결정 아님) | §4.1.1·§4.1.2·§7.5·Appendix A·ARD §2 |

### B-2. 미결 (열린 TBD — baseline 전/설계 단계에 닫을 항목)

| # | 항목 | 본문 | 책임자 | 마감 | 영향 |
| --- | --- | --- | --- | --- | --- |
| 1 | v1.0 목표 RPS·동시 세션(fleet 규모) | §5.1·5.2 | 인프라(규모 PL 입력) | 설계 착수 전 | §3.1·§7.1·§7.4 |
| 2 | 공개 엔드포인트 DNS 잔여 — apex는 확정(#23). 인증서·GeoDNS 구성·리전 내부 호스트 + **Webhook provider별 호스트 `{provider}.webhook.gw.vatech.com` 명시 등록**(와일드카드 DNS 미사용, TLS는 `*.webhook…` 와일드카드 cert 가능) | §4.5.1·§7.6.1·§7.6.2 | 인프라/플랫폼팀 | 배포 구성 착수 전 | §1.7.1·§3.1·§7.3.5·§7.6.1·①②④·③-C |
| 3 | 경로 B EOS 시점 | §2.8·§7.6 | PM(제품) | ① One Pager 확정 시 | §7.6·① |
| 4 | 엣지(B) MQTT 브로커 제품·운영 주체 — 후보 AWS IoT Core / Amazon MQ. (내부 큐 A=SQS는 §3.1.2, 별개) | §3.1.2·§7.6 | 운영조직/인프라(미정) | ③-P-EZ 착수 전 | §7.6·§3.1.2·ARD |
| 5 | 감사·consent 보존 기간 | §6.4·§7.9.3·§7.9.5 | 품질/법무 | baseline 전 | §6.5 |
| 6 | OpenAPI·DBML (`docs/specs/design/`) | §1.5·§4.1·§6.4 | GW(본인) | dev-chain-design 작성 후 | §7 전반 |
| 8 | 호환성 매트릭스 확정본 | §2.8·§7.7.5 | ① One Pager | ① 확정 시 | §7.7 |
| 9 | RTO/RPO·유지보수 윈도우 | §6.3.1·§6.8 | 인프라 | 설계 단계 | §6 |
| 11 | 인증(IEC 62304/13485) 일정·준비물 | §6.13·§6.14 | 품질/마케팅 | 추후 | — |
| 12 | 인프라·런타임 상세 버전(도구·노드) | §3·§4.4 | 인프라/개발 | 설계 단계 | §3 |
| 14 | 로그 포맷(필드·상관키·레벨) 검토 확정 + **수집 에이전트 선택**(권장: Fluent Bit 로그 + ADOT trace/metric; 단일 파이프라인 시 OTel Collector). 앱 계약=stdout JSON+OTel 고정, 수집층은 인프라 선택 | §6.3.2 | 인프라(취합·분석·수집층)+GW(생성) | 설계 단계 | §6.2·§6.3.2·③-I |
| 15 | 전역데이터 복제 토폴로지 세부(primary 위치·단일 vs multi-primary·충돌) — "PostgreSQL 원본+리전 복제 / Redis 캐시" 모델·구분 원칙은 고정, 복제 세부만 미정 | §2.1.1·§6.4 | PM/아키텍트+인프라 | gw/1.2 설계 | §7.3·§6.4·§6.3.1 |
| 16 | Webhook 클라우드 분배 — **CleverLab 갈래 B 활성화 여부·시점**(CleverSpace=대상 아님 확정). EzServer(갈래 A) 역방향 대상 이벤트 목록 | §2.3.6·§7.6.5·§7.6.6 | PM/제품+GW(④) | ④ 상세설계 | §7.6·④·§2.1·§2.2 |
| 18 | 관계형 DB 관리형 제품 — **엔진=PostgreSQL 확정·제품=Aurora PostgreSQL 권장**(처음부터; RDS-first 비권장, 비용 델타 ~20%·저QPS라 작음). **인프라 비준만 남음** | §3.1.2·§2.1.1 | 인프라/아키텍트 | v1.0 배포 구성 착수 전 | §2.1.1·§6.3·§7.3 |
| 24 | **개발·테스트·운영 환경 구축** — dev 에뮬레이터/스텁(EPI·CleverSpace presign·OneID·LMP)·AXS sandbox 자격(↔#6)·staging(운영 유사 축소)·dev/staging AWS 계정·sandbox egress EIP. 책임·일정 | §3.1·§3.4·§3.5 | 인프라/개발 | **dev: AXS 개발 착수 전** · staging: pilot 전 | §3·§7.5·④ |
| 26 | **IaC 도구 확정** — 현 baseline=Terraform(ARD §4.5·§6.6.2)인데 실무·권장=**CDK**(AWS 전용·TS 스택 정합·CloudFormation 네이티브). 확정 시 ARD §4.5·SRS §6.6.2 정합 | §6.6.2·§6.3.3 | 인프라(③-I)+GW | 환경 구축 착수 전 | §3·§6·④ |
| 25 | **프록시 타임아웃·재시도·서킷 수치 + v1.0 서킷 포함 범위** — `connect`/`response`/`total_deadline_ms`(per-upstream, `GW deadline < 클라이언트 타임아웃`)·재시도 상한/백오프/budget·서킷 임계·복구. 정책 골격은 §7.5.4·§7.7.4 확정, **수치·서킷 v1.0 범위가 미결**(upstream SLA·인프라 입력 의존) | §7.5.4·§7.7.4·§5.5·§4.1.2-6 | GW+인프라(+AXS SLA) | 프록시 구현 착수 전 | §7.5·§6.3.4·④ |

## 8 Change Management Process

- 변경 분류: Minor(문구) / Major(요구사항·NFR 수치·아키텍처)
- **CCB(Change Control Board)**
  - **핵심(승인)**: 실장(총괄) — **Scott** · GW 백엔드 리드 — **Raymond**. **PM은 미지정 — 별도 PM 지정 시 CCB에 추가**('Scott=PM'은 미확정, Scott은 현재 전체 관리자/실장)
  - **옵저버(사안별)**: QA 리드·보안·인프라 — Major 변경 검토 시 필요에 따라 참여(고정 명단 없음, v1.0)
  - **확대**: 필요 시 CCB에 인원 추가(실장 합의)
- 절차: PR(영향 평가: §·Swagger·DBML·일정) → Major는 CCB(핵심 2인) 승인 → Appendix A 1줄 추가 → baseline 시 release tag

## 9 Document Approvals

본 SRS는 baseline 통과 시 인수자·일시를 본 절에 기록한다. (현재 골격 — 미승인)

| 역할                 | 인수자   | 승인 일시 |
| -------------------- | -------- | --------- |
| 실장·총괄 (CCB 승인) | Scott    | —         |
| PM (CCB·미지정)      | (TBD)    | —         |
| GW 백엔드 리드 (CCB) | Raymond  | —         |
| QA 리드 (옵저버)     | (사안별) | —         |
| 보안 (옵저버)        | (사안별) | —         |
| 인프라 (옵저버)      | (사안별) | —         |

---

## 변경 이력

| 일시 | 변경 사항 | 작성자 |
| --- | --- | --- |
| 2026-06-17 | 골격 v0.1 — SRS v3.3 고정 항목 전체 배치, PRD/ARD/요구사항 명세(FR/NFR·ADR) 기반 초안·TBD·❓확인 표기 | (작성자 ID 미지정) |
| 2026-06-17 | §1.1·§1.2 확정(범위·목적 추천안 확정, 초안 경고 제거), §7.1·§7.3·§7.6 본문 상세화(Input/Trigger/Output/Side Effect·에러·비목표) | (작성자 ID 미지정) |
| 2026-06-17 | 1단계 — §7.4(업로드 세션·Presigned)·§7.5(Connector)·§7.7(버전 호환 게이트) 상세화. ②·④·① 경계 주석 명시 | (작성자 ID 미지정) |
| 2026-06-17 | 2단계 — §7.2(디바이스 레지스트리·온보딩)·§7.8(Fleet·Config)·§7.9(관리·감사·컴플라이언스) 상세화. §7 전 절 본문 완료(③-C 경계 명시) | (작성자 ID 미지정) |
| 2026-06-17 | 3~6장 정밀화 — §5(Throughput/Concurrent TBD 4항목·Response Time 대안 검토 박스·종속 관계), §6.1(Safety 5질문), §6.2(보안 8항목 표), §6.3.1(가용성 상세), §6.4(DB 무결성·보존 TBD) | (작성자 ID 미지정) |
| 2026-06-17 | 자체 검증 — §7 순서 복구(7.1~7.9)·중복 스텁(7.5·7.7·7.8·7.9) 제거. §4.5.1 공개 엔드포인트(DNS) 제안 추가(GW API·Webhook·Console 호스트, TBD 인프라 확정) | (작성자 ID 미지정) |
| 2026-06-17 | §8 CCB 구성 조정(PM+GW 백엔드 리드 핵심 2인, QA·보안·인프라 사안별 옵저버), §9 승인자 QA 리드 → 옵저버 | (작성자 ID 미지정) |
| 2026-06-17 | §5 범위 경계 명시(서버/노드 규모·용량 산정은 인프라 IaC 영역, GW SRS 범위 밖) + §5.1·5.2 책임자 인프라 담당(규모 수치 PL 입력)으로 확정 | (작성자 ID 미지정) |
| 2026-06-17 | 자체 검증 심화 — FR/NFR 전수 대조(전 FR ID §7 매핑·MIG v2.0 비목표 확인), NFR-SCL 갭 보강(§6.3.5 Scalability 추가), 교차 참조·비목표 버전 정합 확인. Appendix B(TBD 추적표 12항목) 추가 | (작성자 ID 미지정) |
| 2026-06-22 | §4.1.1 API 정의 전략(3버킷: GW 고유 API/프록시 라우트/Egress 커넥터) + §4.1.2 라우팅·API 설계 규칙(서버측 라우트, 클라이언트 지정 upstream 금지=SSRF, Vatech-\* 한정, 정책 체인, 고유 API 컨벤션) 추가 | (작성자 ID 미지정) |
| 2026-06-22 | §4.1.2 규칙 2 보강 — 경로/호스트 1차 라우팅 명시 + `Vatech-Target`(논리 서비스 ID·allowlist·선택/예약, v1.0 미사용 가능) 헤더 표준화, 임의 라우팅 헤더 신설 금지 | (작성자 ID 미지정) |
| 2026-06-22 | §4.1.1 표에 "방향/신뢰경계" 열 추가 — B(inbound·내부 trusted 프록시) vs C(outbound·외부 untrusted 연동) 구분 명확화, presigned 비경유 경로 명시 | (작성자 ID 미지정) |
| 2026-06-22 | §4.1.1 A버킷에 ③-C Console이 호출하는 Backoffice/관리 API 포함(§7.9·§7.8) 명시 — UI=③-C / API=GW 경계 가시화 | (작성자 ID 미지정) |
| 2026-06-22 | §4.1.4 업로드·Presigned 경로 구분(① `/v1/uploads`·Region Signer / ② CleverSpace B bypass / ③ AXS C bypass) · §7.4·§7.5.2 경계·비목표 정리 — AXS/CS presign을 GW가 통합 추상화하지 않음 | (작성자 ID 미지정) |
| 2026-06-22 | §4.1.3-1 Webhook 수신 경로 표기 정합화 — `POST /webhooks/{provider}` → `POST /v1/webhooks/{provider}` (§4.1.2-5·§4.5.1·§7.6.1·OpenAPI와 `/v1` 프리픽스 통일) | (작성자 ID 미지정) |
| 2026-06-22 | §2.3 Overall Operation 확장 — 동작 개요를 시나리오 7종(2.3.1~2.3.7: 온보딩·인증·리전·업로드 경로①·외부연동 경로③·Webhook·버전호환)으로 재작성, 각 시나리오 설명 + mermaid 시퀀스 다이어그램 추가. 액터를 §2.1·§2.2 컴포넌트와 정합, §4.1.4 경로 구분·`/v1/webhooks` 반영. 상세 시퀀스는 ARD §5 위임 유지 | (작성자 ID 미지정) |
| 2026-06-22 | 디바이스 토큰 갱신 정책 명시 — §7.1.1 Trigger/Output에 "갱신=client_credentials 재발급, refresh token 미발급"(RFC 6749 §4.4.3) 명문화 + Will Not Do에 `refresh_token` grant 미도입 사유 추가, §2.3.2 다이어그램에 재발급 loop·refresh 미사용 note 반영. 단명+즉시 revocation 모델 보존 | (작성자 ID 미지정) |
| 2026-06-22 | §4.1.2 라우팅 규칙 보강 — 규칙 1에 handle(A)/bypass(B/C) 정적 결정 + A 예약 네임스페이스 reserved-segment 규율 추가, 규칙 2를 가드형으로 재작성(`Vatech-Target`=대안 라우터 아닌 일관성 가드: 있으면 경로 파생 target과 일치 검증·불일치 400, 없어도 경로로 라우팅 성립, per-route만 필수 가능·전역 의무화 아님) + `Vatech-Target`(라우팅 선택) vs `Vatech-*` 식별 헤더(호환 필수) 구분 명시 | (작성자 ID 미지정) |
| 2026-06-23 | §8·§9 CCB 명단 확정 — 핵심: Scott(PM)·Raymond(GW 백엔드 리드); QA·보안·인프라는 사안별 옵저버, 필요 시 CCB 확대. Appendix B #10 완료 | (작성자 ID 미지정) |
| 2026-06-23 | **라우팅 모델 전환(ADR-11) — target-routed proxy 채택.** §4.1.1 3버킷 → 2면(GW 고유 API / 레지스트리 라우팅 프록시, B·C=trust profile) 재구성, §4.1.2 규칙 전면 개정(`Vatech-Target` 유무로 면 구분·v1.0 proxy 필수·논리 ID enum만·SSRF 가드·verbatim 전달·정책은 path 검사·region 직교 조합). §4.1.4 경로②③를 `Vatech-Target` proxy로, §2.3.5 다이어그램·§7.5.1 connector(레지스트리 일반화)·§4.1.3 표현 갱신. Appendix A ADR-11 + Appendix B #13(ARD 기재·클라이언트 헤더 적응). 이전 "경로 네임스페이스 1차 + Vatech-Target 가드"(2026-06-22) 결정을 대체 | (작성자 ID 미지정) |
| 2026-06-23 | 2026-06 회의 결정 반영 — (1) Straumann 선행 구현 명시(§7.5.2), (2) CleverLab↔AXS 갈래 B 현 시점 제외(§1.2 Will Not Do·§2.1·④ \_status·Roadmap §3.7.2 정합) — 외부 cloud 연동 일반 역량은 유지, (3) `Vatech-*`+`User-Agent` 전 제품 강제·공용 라이브러리·originator/Via 누적(§7.7.1), (4) 로그 취합·분석 인프라 소유·로그 포맷 검토 TBD(§6.3.2·Appendix B #14) | (작성자 ID 미지정) |
| 2026-06-23 | §2.1.1 배포 토폴로지 신설 — 멀티 서버(Multi-AZ HA) + 멀티 리전 다이어그램 추가. inbound 안정 endpoint 1개 vs outbound NAT EIP 다수 구분, AXS egress IP whitelist=고정 EIP 합집합(증설 시 협의), Webhook 멀티 인스턴스 수신(공개 호스트 1·공유 idempotency·매핑 기반 교차 리전 분배) 설명. §2.6 "고정 egress IP" → 고정 EIP 집합으로 명확화 | (작성자 ID 미지정) |
| 2026-06-23 | 데이터 공유·토폴로지 명시 — §2.1.1에 전역 control-plane SSOT 노드 추가 + "데이터 공유·토폴로지" 절(멀티 서버=리전 내 DB/Redis 공유·무상태 pod / 멀티 리전=전역 일관 라우팅·식별 데이터 vs 리전 로컬 운영 데이터 / PHI 미저장). §6.4 데이터 토폴로지 항목 추가, Appendix B #15(저장소 구현 gw/1.2 TBD·구분 원칙 고정) | (작성자 ID 미지정) |
| 2026-06-23 | Webhook 분배 표현 단순화 — §2.1 맥락도 `EZ→GW`를 `EZ↔GW`(상행 API·하행 MQTT) 양방향으로 변경 + 양방향 화살표 의미·"분배 상세 §2.3.6" 노트 추가, §2.2 컴포넌트도에 동일 캡션. 수신→분배 fan-out 상세는 §2.3.6 시퀀스를 단일 정본으로 유지(맥락도·컴포넌트도엔 미전개) | (작성자 ID 미지정) |
| 2026-06-23 | §2.1.1 Webhook inbound 수정 — 외부는 region 비인지이므로 **단일 webhook ingress(provider별 1개)로 수신 후 우리가 Org-ID→Clinic→리전 매핑으로 분배(교차 리전)**, GeoDNS가 inbound 대상 리전을 정하지 않음을 명시. 다이어그램의 `AXS→GeoDNS→리전 LB` 오해 수정(단일 ingress→임의 리전 GW→매핑 분배). 외부 서비스 일반화(AXS는 한 예, C 프로파일 공통·ADR-11) | (작성자 ID 미지정) |
| 2026-06-23 | §2.1.1 Webhook ingress 정정 — provider별 호스트 불필요(**단일 공개 호스트 + 경로 `/v1/webhooks/{provider}`로 구분**, §4.5.1·§7.6.1과 일치), 수신 ingress가 **전역 매핑 DB에 연결**되어 내용으로 리전 판정, 다이어그램을 **A로만 → 대상 리전 A·B 양쪽 재분배 + GLOBAL 매핑 조회 에지**로 수정 | (작성자 ID 미지정) |
| 2026-06-23 | §2.1.1 저장소 역할 명시 — 다이어그램·본문에 **PostgreSQL=원본(전역데이터 리전 간 복제/sync)·Redis=리전 빠른 조회 캐시(로컬 PG cache-aside·TTL·mapping_version 무효화)** 추가. STA/STB 라벨에 PostgreSQL 복귀(복제본+리전로컬)·GLOBAL=PostgreSQL 원본·sync 에지 라벨 갱신. Appendix B #15를 복제 세부(primary 위치·multi-primary·충돌)로 좁힘(모델은 고정) | (작성자 ID 미지정) |
| 2026-06-23 | §2.1.1 Webhook Receiver를 **GW 전역 계층(GTIER) 서브그래프로 박스화**(전역 SSOT와 함께) — GW의 일부이되 리전 비종속 별도 박스로 가시화. (GW 바깥 별도 서버로 두지 않음 — §4.1.1 A면·§2.2·§7.6 정합) | (작성자 ID 미지정) |
| 2026-06-23 | §2.2 재작성 — §2.1의 GW를 확대한 도로 변경(컴포넌트 분해 → 외부 연결형). 규칙: §2.1 외부 전부 등장 + 각 외부 ≥1 내부 컴포넌트 연결(1개 권장), common 컴포넌트는 미연결 허용. GW를 **GW core / Webhook ingress 두 부분**으로 분할(Webhook Receiver·큐·MQTT는 ingress로 이동, INTEG=Connector만). 분배 런타임은 §2.3.6 위임 | (작성자 ID 미지정) |
| 2026-06-23 | §2.1 맥락도에 **Webhook Receiver sub-tier 박스** 반영 — GW를 GWBOX 서브그래프(GW core + Webhook Receiver)로 분할, AXS의 외부 연동(egress)=GW core / Webhook(인바운드)=Webhook Receiver로 분리 표기(GW 내부 별도 면, 외부 서버 아님). 노트 갱신 | (작성자 ID 미지정) |
| 2026-06-23 | §2.1 Webhook 분배 경로 명시 — `AXS → Webhook Receiver →(MQTT)→ EzServer`(하행) + `→(HTTP push)→ CleverSpace`(클라우드) 엣지 추가. 하행 MQTT를 GW core(EZ↔GW)에서 **Webhook Receiver 출발로 이동**(EZ→GW는 API 상행만). 분배 대상=매핑(§7.3), 상세 §2.3.6 | (작성자 ID 미지정) |
| 2026-06-23 | Webhook 분배 대상별 시나리오 명시 — §2.3.6에 EzServer(갈래A 역방향)·CleverLab(갈래B 보류)·CleverSpace(**미확정 TBD**) 표 추가. 클라우드 분배 대상을 §2.1·§2.2 다이어그램에서 CleverSpace → **CleverLab(갈래B·보류)** 로 정정(CleverSpace webhook 엣지 제거 — 구체 시나리오 미확인). §7.6.5에 대상 미확정·조사 항목 TBD 명시, Appendix B #16 추가 | (작성자 ID 미지정) |
| 2026-06-23 | API 호출 경로 동일성 명확화 — §2.1 다이어그램의 `GW→upstream` 엣지를 **모두 동일 스타일(target-routed proxy)** 로 통일(CS·OID·CLAB·AXS), AXS는 라벨만 `C·외부(OAuth·고정 egress IP)`로 구분(기존 `GW<-->외부 연동(egress)` 특이 표기 제거). Webhook(이벤트 인바운드)만 별개 흐름으로 분리. §2.1 노트·§2.3 헤더·§2.3.5에 "CleverSpace=B/AXS=C, 경로 동일·trust profile만 다름" 명시 | (작성자 ID 미지정) |
| 2026-06-23 | §2.2·§2.1.1에 경로 동일성 적용 — §2.2 재구성: VatechAPIGateway를 **GW core + Webhook ingress 두 부분**(GW core 내부=plane 상세), 바깥(외부·엣지)은 §2.1과 동일. **Router/PEP 컴포넌트 추가** — 모든 upstream(CS·CLAB·AXS)이 `ROUTER` 동일 경유, AXS만 `CONN`(OAuth·egress) 추가(C). Webhook(AXS→WH→EZ/CLAB)만 별개. §2.1.1에 "egress whitelist·Webhook은 외부(C) 한정, 내부(B)는 동일 proxy·내부망" 명시 | (작성자 ID 미지정) |
| 2026-06-23 | ARD 동기화 — ARD(v0.10)에 **ADR-11(target-routed proxy)** + **Router/PEP 컴포넌트** 등록(SRS §2.2·§4.1과 일치). SRS Appendix A 주석·Appendix B #13을 "ARD 기재 완료·CCB 확인 대기"로 갱신 | (작성자 ID 미지정) |
| 2026-06-23 | §2 정합 점검 polish — §2.2 규칙에 CleverOne(EZ 경유) 예외 명시, §2.3.6 시퀀스 클라우드 par 분기에 "CleverLab 보류·CleverSpace TBD" 라벨/노트, §2.3.6 표 EzServer 역방향을 "capability=b1(WH-06)·이벤트 목록만 ④ TBD"로 정리(§7.6.6·ARD v0.9와 정합) | (작성자 ID 미지정) |
| 2026-06-23 | **리전 구축 단계화 결정** — §2.7.1 신설(1차 단일 리전/2차 멀티 리전, v1.0부터 멀티리전-ready 설계 요건 표). §4.5.1 DNS를 apex-우선(클라이언트는 apex만, 리전 호스트 예약)으로 사전 설계, §7.3.5·§6.3.1·§2.1.1에 단계화 반영. Appendix A 결정 로그 + B#7 종결(흡수 TBD → 단일 우선 결정) | (작성자 ID 미지정) |
| 2026-06-23 | CleverSpace webhook 혼동 정리 — **클라우드 webhook 수신=CleverLab만(갈래B 보류), CleverSpace는 webhook 대상 아님으로 확정**(TBD 해소). §2.1·§2.2·§2.3.6(표/시퀀스/정리)·§4.1.3·§7.6.5·Appendix B#16에서 "CleverSpace/CleverLab" 묶음·CleverSpace TBD 제거. Roadmap §2.7.1 다이어그램(CS 엣지 제거)·§2.7.3 표도 CleverLab 단일로 정합 | (작성자 ID 미지정) |
| 2026-06-23 | CleverLab 방향 정합(Roadmap §2.6과 일치) — CleverLab을 **GW 프록시 대상(B)에서 제외**하고 **갈래B 클라우드 클라이언트(보류): CleverLab→GW→AXS** + webhook 수신(GW→CleverLab)으로 정정. §2.1·§2.2 다이어그램 엣지 방향 변경, §4.1.1 B목록에서 제외·주석, 외부표·노트 갱신. (이전 'GW→CleverLab 프록시 B'가 Roadmap의 'CleverLab→GW'와 방향 충돌이던 것 해소) | (작성자 ID 미지정) |
| 2026-06-23 | 다이어그램 차이 정리(선택 2건) — §2.1에 "control plane context, 데이터plane presigned·minio·리전별CS 생략(§2.3.4/§2.3.5/§4.1.4/§2.1.1 참조)" 주석 추가. Roadmap §2.7.1 '이벤트 라우터' → 'Webhook 이벤트 라우터'(SRS Router/PEP와 명칭 충돌 제거) | (작성자 ID 미지정) |
| 2026-06-23 | **GW presigned 직접 발급 시나리오 폐기** — 결정: 서명 주체=CleverSpace(②)·AXS(③), GW는 **중계만**. §2.3.4를 'CleverSpace presigned 중계'로 교체, §7.4를 '중계·위임(GW 비발급)'으로 재작성, §4.1.4를 2경로(②③)로 축소(경로①·Region Signer·GW Upload Session/Storage 철회·ADR-03/04 폐기). §2.2 Data Plane 컴포넌트(SES·Presign·Signer) 제거, §1.4 용어·§2.3 액터·§2.4·§2.5·§2.7·§4.4·§5.2·§6.3.3 등 산재 참조 정리. FR-SES는 삭제 않고 'GW 비소유·발급주체(②/④) 소유, GW 중계'로 재분류 | (작성자 ID 미지정) |
| 2026-06-24 | Webhook 수신 엔드포인트를 **유연·레지스트리 기반**으로 재정의 — `/v1/webhooks/{provider}`를 *확정 계약*에서 **기본 관례(예시)** 로 강등. GW는 스키마·경로를 강제하지 않고 provider 규약을 수용(어떤 인바운드든), **발신자 검증·라우팅만** 하며 payload는 소비자가 해석. §4.1.3·§7.6.1·§2.1.1·§2.3.6·§4.5.1·§4.1.2-5 + API명세·OpenAPI·ARD·Roadmap 반영 | (작성자 ID 미지정) |
| 2026-06-24 | DB·API를 '분배 지식' 모델로 보강 — DBML에 `org_mapping`(Org-ID↔ClinicID 라우팅 키)·`webhook_provider`(유연 수신 config)·`upstream_registry`(Vatech-Target proxy)·`delivery_channel`(분배 채널) 추가, `webhook_event`에 external_org_id·clinic_id·region 추가. OpenAPI에 `/admin/v1/{org-mappings,webhook-providers,upstreams}` 관리 API + 스키마 추가. API명세 §2 엔터티·SRS §6.4·§7.9.1·§4.1.3-4 반영. (GW=분배자, DB=어디로 분배할지의 지식) | (작성자 ID 미지정) |
| 2026-06-24 | 분배 매핑은 **온보딩 자가 등록**으로 채움(Admin 교정만) — §2.3.1을 '온보딩(클리닉/클라이언트 등록 + 디바이스 enrollment)'으로 확장(클리닉 등록·리전 자가선택·OneID 인증 다이어그램 추가). OpenAPI `/v1/clinics`·`/v1/clinics/{id}/org-bindings` 신설, `/admin/v1/org-mappings`를 교정(override)으로 강등. §7.3·DBML(crm/org_mapping/delivery_channel)·API명세 반영. region UI=제품(③-P-CO), GW=등록·검증·저장 | (작성자 ID 미지정) |
| 2026-06-24 | 클리닉 등록 주체·토폴로지 명시 — 클리닉=CleverOne 다수+EzServer 1개. **등록 주체 EzServer Console(잠정)·CleverOne 대안 TBD**(§2.3.1 텍스트·다이어그램·§7.3·Appendix B #17). Roadmap §4·§2.4 정합 | (작성자 ID 미지정) |
| 2026-06-24 | 운영 중 리전 변경 + 리전 카탈로그 — §7.3.4에 **클리닉 자가 리전 변경(운영 중, EzServer Console)** + 부수효과(기존 PHI 잔류·재동의·in-flight) 명시, §7.3.6 **GW 리전 목록 조회 API**(`GET /v1/regions`) 신설. OpenAPI `GET /v1/regions`·`PUT /v1/clinics/{id}/region` + `Region` 스키마, DBML `region_catalog` 테이블(+region FK), API명세·§6.4·§2.3.1 반영 | (작성자 ID 미지정) |
| 2026-06-24 | Redis 키스페이스 카탈로그 신설 — `design/redis/redis-keyspace.md`(키 패턴·자료형·TTL·용도·cache/휘발 구분·PG 재구성 출처). **Redis=SSOT 아님(캐시+휘발)** 원칙 명시. §3.1.2·§6.4·design/README에서 참조 | (작성자 ID 미지정) |
| 2026-06-24 | DNS apex 호스트명 확정 — **`gw.vatech.com`(apex)=확정(Scott)**, §4.5.1 제목 '제안' 제거·표 '확정' 표기·TBD 블록을 확정+잔여(인증서·GeoDNS 구성·리전 내부 호스트 등록=인프라)로 교체. Appendix B #2를 'apex 확정·잔여 인프라 등록'으로 갱신 | (작성자 ID 미지정) |
| 2026-06-24 | §2.3 도입부에 스코프 노트 추가 — **운영자/Console 인증 흐름(로그인·세션·토큰 refresh·RBAC UI)은 §2.3 비정의**, Console UI=③-C Sub-SRS·인증=OneID(OIDC) 위임(ADR-08)·GW는 OneID 토큰 검증+관리 API RBAC(§7.9)만 소유 명시(기존 §1.2·§7.9·§4.1.1 경계와 정합) | (작성자 ID 미지정) |
| 2026-06-24 | §2.3 이후 정합 점검 후속 수정 — (1) §2.1 line 181 스테일 참조 `§2.3.4(경로①)`→`(경로②)`(§2.3.4=CleverSpace presigned 중계와 일치), (2) ADR-11 2면+trust profile 재구성에 따른 잔존 용어 정리 — §2.3.6 `A버킷`→`A면(GW 고유 API)`·§4.1.1 `C버킷`→`C·외부 프로파일`·`B버킷 성격`→`B·내부 프로파일 성격`. 의미 변경 없음(라벨 A/B/C 유지) | (작성자 ID 미지정) |
| 2026-06-24 | §3.1.2 SW 환경을 **EKS 정합**으로 재정리 — 'EKS 정합 원칙'(관리형 우선·IRSA 정적시크릿 미사용·§2.1.1 데이터 토폴로지 정합·포터블 대안 병기) 추가. DB→RDS/Aurora PostgreSQL(전역=Aurora Global Database), 캐시→ElastiCache(리전별·교차복제 안 함), 큐→SQS(+FIFO)/Amazon MQ, MQTT→IoT Core/Amazon MQ(주체 TBD), 시크릿→KMS·Secrets Manager+CSI/External Secrets, 이미지→ECR, **인그레스 AWS LB Controller(ALB/NLB)·egress NAT 고정EIP·관측 ADOT→CloudWatch/AMP·AMG** 항목 추가. 엔진 동일(포터블 대안 유지) | (작성자 ID 미지정) |
| 2026-06-24 | 메시징 2-레그 명확화 — **A. 내부 비동기 큐=Amazon SQS**(GW 내부 버퍼·재시도·DLQ, §7.6.3) / **B. 엣지 전달=MQTT**(방화벽 뒤 EzServer outbound 구독·push, AWS IoT Core 후보, §7.6.6). 둘은 별개 레그임을 §3.1.2·§4.4 표(메시지 큐 'RabbitMQ 권장'→'SQS 기본'·MQTT Broker→IoT Core)·§7.6.3·§7.6.6·§2.2 다이어그램(WHQ)·§2.3 액터표·§2.3.6 시퀀스(Q 라벨)에 일괄 반영. B에 SQS 비사용 사유(inbound 불가·지속 구독·자격배포 부적합) 명시 | (작성자 ID 미지정) |
| 2026-06-24 | §3.4.2 개발 환경 도구 — 개발 표준을 **Claude Code**로 명시(`Cursor·VS Code` → `Claude Code(개발 표준)·VS Code`) | (작성자 ID 미지정) |
| 2026-06-24 | §3.6.1 Location of Outputs — 개인 작성 폴더 경로 언급 제거, 문서 위치를 공식 저장소(Azure Repos `vt-api-gateway/docs/specs/`, 설계 산출물 `docs/specs/design/`)로만 표기 | (작성자 ID 미지정) |
| 2026-06-24 | **Webhook 발신자 식별을 provider별 전용 호스트로 전환** — source IP 기반 식별이 불안정(상대 egress 미통제)하므로 **`{provider}.webhook.gw.vatech.com`(Host/SNI)로 식별**, source IP allowlist는 옵션·방어심층으로 강등. **식별(Host)≠인증(HMAC+timestamp)** 원칙 명문화. **와일드카드 DNS 미사용**(엄격 관리·명시 등록, 추가는 연단위 드묾), TLS는 와일드카드 cert 허용. §2.1.1·§4.1.3·§4.5.1·§7.6.1·§7.6.2·Appendix B#2 + DBML(`webhook_provider.inbound_host` 1차 식별 키)·OpenAPI(WebhookProvider.inboundHost·webhook 설명)·인증보안 위협표 반영 | (작성자 ID 미지정) |
| 2026-06-25 | §2.3.6 Webhook 시퀀스·설명에 provider별 호스트 식별 적용 — 도입부(provider 호스트 push·발신자 식별=수신 Host vs 목적지=매핑 분리·Host≠인증), 시퀀스 POST 대상을 `axs.webhook.gw.vatech.com`으로·검증 단계를 'Host/SNI 식별→시크릿 선택·HMAC·timestamp(IP 옵션)'로, Note를 '미등록 Host→404·인증 실패→401'로 갱신 | (작성자 ID 미지정) |
| 2026-06-25 | §3.1.2에 **DB 선택 근거** 노트 추가 — Aurora PostgreSQL=PostgreSQL 호환, 채택 이유=멀티 리전 전역 복제(Aurora Global Database, §2.1.1), v1.0 단일 리전은 RDS도 충분, 호환성 단서, 포터블 대안=자가호스트 PostgreSQL | (작성자 ID 미지정) |
| 2026-06-25 | §2.1.1 다이어그램에 DB 제품 명시 — GLOBAL/STA/STB 노드를 `PostgreSQL`→**`Aurora PostgreSQL`**(Global DB primary/복제본)·`Redis`→**`Redis(ElastiCache)`**로, 복제 엣지를 `Aurora Global DB 복제/sync`로 표기. 캡션 bullet 추가(제품·근거 §3.1.2·v1.0은 RDS도 가능·둘 다 PG 호환) | (작성자 ID 미지정) |
| 2026-06-25 | **DB 제품 = 권장·확정 TBD로 정리(옵션 A)** — 엔진=PostgreSQL 확정, 관리형 제품(Aurora 권장 vs RDS)은 미확정. §3.1.2에 **Aurora PostgreSQL vs RDS for PostgreSQL 비교표** 추가 + 근거 노트를 '권장·확정 TBD'로, §2.1.1 다이어그램 노드를 `PostgreSQL(Aurora 권장·확정 TBD)`로 완화, 캡션·DB bullet에 'Appendix B #18·인프라 확정' 반영, **Appendix B #18 신설**(인프라/아키텍트, 멀티 리전 설계 전). 개발계획서 §5도 동일 표기. (RDS도 교차 리전 복제 가능하나 Aurora Global DB가 저지연·관리형으로 우수) | (작성자 ID 미지정) |
| 2026-06-25 | DB 권장 **강화 — "처음부터 Aurora PostgreSQL"** — 전환 비대칭성(Aurora 단일→글로벌=마이그레이션 0 vs RDS→Aurora=플랫폼 마이그레이션·재검증) + 비용 델타 **~20%·저QPS라 작음**·통제 제품 재검증/IaC 이중구축 회피를 §3.1.2 근거(3)(4)·비교표(전환·비용 행)·결론·DB bullet·§2.1.1 캡션·Appendix B #18·개발계획서 §5에 반영. RDS-first 비권장 명시(인프라 비준은 유지) | (작성자 ID 미지정) |
| 2026-06-25 | 문구 정리 — §3.1.2 DB 근거 노트에서 슬로건성 문장("PostgreSQL을 안 쓰는 게 아니라…") 제거하고 결정·권장·근거(1~4)만 유지. §2.1.1 단일 리전 안내 문장의 캐주얼 톤 정리. (불필요 설명 제거, 의미 변경 없음) | (작성자 ID 미지정) |
| 2026-06-25 | Webhook IP allowlist 관리 명확화 — 신뢰=HMAC(주)·IP allowlist=옵션 재확인. §7.6.2에 검증 config(`inbound_host`·`sig_scheme`·`secret_ref`·`source_ip_allowlist`) **관리 API `/admin/v1/webhook-providers`(§7.9.1), UI=③-C** 명시. allowlist 형식을 **CIDR 목록**으로 DBML·OpenAPI에 명확화(관리 API·데이터는 기정의 — 신규 아님) | (작성자 ID 미지정) |
| 2026-06-25 | §1.4 용어에 **LMP(LicenseManager) = Clinic-ID 발급원** 정의 추가(§2.3.1 온보딩 자동 등록의 LMP 약어 명시) | (작성자 ID 미지정) |
| 2026-06-26 | 잔재 전수 점검·정리 — §2.7 gw/1.2 "멀티클라우드 presign·**signer 확장**" → "멀티 리전 활성화(Aurora Global DB·GeoDNS)", §2.7.1 금지 노트의 "멀티클라우드 presign broker ready" 제거(GW 비소유·FR-SES-06 해당없음·line 1290과 일치), §2.1 노트 "비-AWS minio·디바이스→storage" → "AWS 미지원국 Provider MinIO·EzServer→발급주체 storage". signer/Upload Session/포터블 잔재 0 확인 | (작성자 ID 미지정) |
| 2026-07-01 | **`compat_matrix` DB 테이블 폐기 — 호환성 매트릭스는 파일 SSOT** — 릴리스 커플링 정적 설정이라 소스 파일(① One Pager 동기화)→빌드/CI로 well-known JSON 생성·공시(§7.7.5)로 일원화, DB 미저장(런타임 게이팅 훼손 방지·긴급 차단은 Config push §7.8.4). DBML `compat_matrix` 제거(16→15 테이블)·§6.4.2 조감도 OPS에서 제거·§6.4 저장유형·§7.7.5 명확화. well-known 샘플의 폐기 경로(`/v1/uploads/{id}/commit`)를 `region.change`로 교체 | (작성자 ID 미지정) |
| 2026-07-01 | **§6.4.1 org_mapping 경계·`provider` 관리 정리** — org_mapping=얇은 식별자 매핑(공통 조각)임을 명시(암묵 가정 3·가드레일·"구조 다른 provider=전용 테이블 분기, 실패 아님"). `provider`는 정규 토큰(소문자)·enum 금지, provider 레지스트리 FK/‌target_id 통합은 R8 결정으로 등록. Agenda R8에 org_mapping 경계·provider 관리·Device 1:N vs 1:1 확인 추가 | (작성자 ID 미지정) |
| 2026-07-01 | **§6.4.1 데이터 관계 ERD + region 모델 A안 확정(회의 확인 예정 R8)** — Clinic·Device·외부 Org 관계를 mermaid ERD + 기본/확장/미래(점선) 계층도로 명시. **A안: region SSOT=Clinic, device는 clinic 파생** → **DBML `device.region`·`region_mapping` 제거·`device.clinic_id`(FK·nullable)+인덱스 추가**, **OpenAPI `Device`에서 region 제거·clinicId 추가**. Clinic↔Device 1:N(현 1:1=EzServer). 외부 Org-ID=확장((provider,external_org_id)→clinic, AXS만); 신규 provider=org_mapping 확장 or 신규 테이블+추가 개발. DBML 컴파일 검증(17→16 테이블). 미결: clinic 전용 테이블 분리·clinic-less device region(미래) | (작성자 ID 미지정) |
| 2026-06-30 | **§2.1.1 Webhook Ingress 위치 정정 + path 잔재 제거** — Webhook Ingress 컴퓨트를 전역 계층(GTIER)에서 **각 리전 GW pods**로 옮겨 그림(컴퓨트=리전, 전역=DNS 호스트+매핑 데이터만). 다이어그램 재작성(전역=Route53 DNS+SSOT / 리전=LB·pods(API+Webhook Ingress)·저장소·NAT, webhook=DNS→리전→매핑→분배(교차 가능)), 노드 라벨 간소화. **단일↔멀티 리전 전환 명문화**(DNS 단일 지정→GeoDNS 전역·데이터 단일→복제, Ingress는 항상 리전). path 기반 잔재(`공개 호스트 1개·provider별 등록 경로 /webhooks/axs`·`단일 webhook ingress`) 제거 → **provider별 전용 호스트(DNS)** 로 통일 | (작성자 ID 미지정) |
| 2026-06-30 | **GW 다이어그램 색 위계 정립(§2.1·§2.1.1·§2.2)** — 4단 일관 체계: **연두 박스=GW 범위** · **연파랑 박스=GW core·Webhook Ingress**(§2.2 CORE/WHTIER, §2.1.1 WHIN) · **흰 카드+파란 테두리=우리가 만드는 세부 컴포넌트**(서비스·GW pod) · **회색=managed 인프라/데이터**(SQS·DB·NAT·LB) · 외부=기본. plane 그룹(Control/Data/Integration)은 투명 처리(노랑 제거). §2.1→§2.2 줌인 관계를 색으로 연결. **범례를 mermaid 다이어그램으로 만들어 3개 다이어그램 각각 아래 배치**(글 색-나열은 다이어그램과 중복·drift라 통합 제거, 뉘앙스 1줄만 §2.1에 유지) | (작성자 ID 미지정) |
| 2026-06-30 | **Webhook 명칭 통일** — tier 명칭이 §2.1='Webhook Receiver' vs §2.2='Webhook ingress'로 불일치(내부 컴포넌트와도 충돌)하던 것을 **tier='Webhook Ingress'** 로 통일(§2.1·§2.1.1·§2.2 다이어그램·본문), 내부 컴포넌트는 **'Webhook Receiver'(수신·검증·ACK·적재) + 'Webhook Dispatcher'(분배 워커)** 로 분리 정의. §2.1 노트에 'Ingress=Receiver+SQS+Dispatcher' 정의 추가 | (작성자 ID 미지정) |
| 2026-06-30 | **Webhook 분배 워커 명시(ADR-12)** — SQS를 소비해 MQTT/HTTP로 발행하는 주체가 불명확하던 것을 **별도 worker Deployment**(동일 코드베이스·SQS consumer·독립 스케일/격리)로 확정. §7.6.7 신설(FR-WH-07: consume·대상 해석·publish·재시도/DLQ), §7.6.3 포인터, §2.2 다이어그램(WHQ→SQS+분배워커 DISP), §2.3.6 시퀀스(DISP consumer), §2.2 액터표, Appendix A ADR-12. 대안(in-process·Lambda) 반려 사유 기록. OpenAPI/DBML 영향 없음(런타임 컴포넌트) | (작성자 ID 미지정) |
| 2026-06-29 | **CCB 역할 교정 — 'Scott=PM' 철회** — Scott은 **실장(전체 관리자/총괄)** 이며 PM은 미확정(별도 지정 가능). §8 핵심 승인을 'PM Scott'→'실장(총괄) Scott + PM 미지정', §9 표에 '실장·총괄'·'PM(미지정·TBD)' 분리, Appendix B #10을 '승인=Scott(실장)·Raymond 확정 / PM 미지정'으로 정정 | (작성자 ID 미지정) |
| 2026-06-29 | **IaC 도구 = CDK 권장(확정 TBD)** — §6.6.2에서 baseline `Terraform`과 실무 CDK의 불일치 표면화, AWS 전용·TS 스택 정합 근거로 CDK 권장 노트 추가(인프라 ③-I 비준·ARD §4.5 정합 = Appendix B #26, 7/2 R5). §6.6.2 stack 줄에서 IaC 항목 분리 | (작성자 ID 미지정) |
| 2026-06-29 | **프록시(B/C) 에러·타임아웃·복원력 정책 신설** — §7.5.4(FR-INT-05: 타임아웃 계층 `GW deadline < 클라이언트 타임아웃`·per-upstream 레지스트리 타임아웃·**연결실패 한정 보수적 재시도**(앱 재시도는 클라이언트 소유·타겟당 upstream 1개)·서킷 브레이커·클라 절단 시 upstream 취소)·§7.7.4(업스트림 오류 매핑표: 연결실패 502/타임아웃 504/서킷 503 = GW envelope, upstream 자체 4xx/5xx = verbatim 통과, `Vatech-Error-Origin` 마커)·§4.1.2 규칙6·§5.5·§6.3.4 반영. OpenAPI에 ProxyError·타임아웃 레지스트리 필드. 수치·v1.0 서킷 범위 = Appendix B #25(7/2 R4) | (작성자 ID 미지정) |
| 2026-06-29 | §4.1.2에 **라우팅 방식 비교·결정 표(ADR-11)** 추가 — 4안(헤더 `Vatech-Target` / 경로 프리픽스 `/axs/…` / 서브도메인 / 클라이언트 지정) × 11기준(관례·verbatim·A↔프록시 구분·경로충돌·클라 비용·SSRF·DNS/TLS·멀티리전·**확장성·유지보수/장애대응**·관측) 비교. 정직 평가: 헤더는 verbatim·배타구분·apex·클라 최소변경에 우수하나 **운영/장애대응·관례는 경로/서브도메인이 우위**(헤더는 커스텀이라 표준 로그·엣지 제어에 추가 설정) → "헤더 전부 우수"는 아님, **트레이드오프로 7/2 회의 재평가 안건(R1)** 상정. Appendix A ADR-11 노트에 비교표 링크 | (작성자 ID 미지정) |
| 2026-06-29 | **잘못된 N/A(기존과 동일) 교정** — "기존과 동일"은 N/A가 아니라 스펙(정확한 링크/복사, 모르면 TBD; spec-standard 규칙 갱신). §3.4.1 `N/A(기존 개발 PC와 동일)`→"특별 HW 요구 없음·표준 개발 PC", §3.5.1 `N/A(클라우드…)`→"운영 §3.1.1 HW 동일(축소본)" 링크. 정당한 N/A(③-C 정의·기능상 무관·64bit 기본)는 유지 | (작성자 ID 미지정) |
| 2026-06-26 | §6.9 사이트 적용 요구사항 현행화 — 낡은 "리전별 signer·비-AWS MinIO(v1.2)" 제거(signer 폐기·GW AWS 전용 반영). 리전 주권(clinic→region·PHI 미이동)·**AWS 미지원국=가까운 AWS GW 접속+Provider MinIO 중계**·apex DNS·멀티리전 staging으로 재작성 | (작성자 ID 미지정) |
| 2026-06-26 | §1.4 용어에 **OTel(OpenTelemetry)·ADOT** 추가(관측성 표준·AWS 수집기) | (작성자 ID 미지정) |
| 2026-06-26 | §6.3.2에 **관측 수집층 권장 패턴(힌트)** — 앱 계약=stdout JSON+OTel 계측(고정), 수집 에이전트=인프라 선택. 권장: **Fluent Bit(로그)+ADOT(trace/metric)**, OTel은 traceId 위해 필수·Fluent Bit와 역할 분리(경쟁 아님). Appendix B #14에 수집 에이전트 선택 포함. 최종 결정=인프라 | (작성자 ID 미지정) |
| 2026-06-26 | §6.3.2에 **구조화 로그 구조(요구)** 정의 — JSON 한 줄·필수 필드(ts·level·traceId/spanId·requestId·tenant/clinic·actor·action·result·latency·errorCode)·상관키(OTel traceId + Vatech-\* originator/Via §7.7)·레벨·PHI/시크릿 금지·인프라 취합 소유. §3.1.2 Pino는 도구만(구조는 §6.3.2)으로 정리. 정확한 필드 확정은 Appendix B #14 | (작성자 ID 미지정) |
| 2026-06-26 | §1.4 용어에 **PHI** 추가(환자 식별 건강정보·GW 본문 미저장·주권/consent 대상·dev/test 더미만). §1.4 용어 ❓마커 갱신(PHI 해소) | (작성자 ID 미지정) |
| 2026-06-26 | **환경 구분(개발·테스트·운영) 정리** — §3.1에 **환경 매트릭스**(차원별 dev/test/prod: DB·캐시·큐·AXS·EzServer·CleverSpace·OneID·LMP·PHI·egress) 추가. §3.4에 **개발 의존성 대체(에뮬레이터/스텁) + AXS 우선 개발 경로**(AXS sandbox·EPI 에뮬레이터·CleverSpace presign 스텁·OneID/LMP 스텁·webhook simulator), §3.5에 **staging(운영 유사 축소)·더미 PHI·sandbox EIP·E2E 게이트**. Appendix B #24(환경 구축 책임·일정) 신설. PHI는 운영만 실데이터 | (작성자 ID 미지정) |
| 2026-06-26 | **캐시 엔진 Redis→Valkey** — Redis 오픈소스 종료(2024 초)·AWS는 **ElastiCache for Valkey**(Redis 호환·저비용) 제공. §1.4 Valkey 용어 추가, §3.1.2 캐시·§2.1.1 다이어그램(Valkey(ElastiCache))·캡션·§6.4·design/redis 키스페이스 상단 노트(엔진=Valkey, 키스페이스·파일명 동일) 갱신. 인라인 'Redis'는 'Redis 호환(=Valkey)'으로 §1.4가 포괄. 개발계획서 §5(v0.9) 정합 | (작성자 ID 미지정) |
| 2026-06-25 | §2.1 다이어그램 그룹핑 개선 — AXS(외부)와 우리 클라우드를 **'연동 서비스(GW upstream)' 한 카테고리로 묶고 내부(B)·외부(C) 하위 그룹**으로 재구성(대칭화·ADR-11 trust profile 가시화). 노드 ID·엣지 불변 | (작성자 ID 미지정) |
| 2026-06-25 | §2.2 외부 그룹핑을 §2.1과 일치 — 외부 노드를 **CLINIC + 연동 서비스(내부 B/외부 C)** 동일 구조로 묶음("GW 바깥은 §2.1과 완전 동일" 규칙 충족). 내부 컴포넌트(GWBOX)·엣지·노드 ID 불변 | (작성자 ID 미지정) |
| 2026-06-25 | §2.2 GW core 요청 파이프라인(PEP 체인) 연결 추가 — `COMPAT→ROUTER`(끊김 보완)·`ROUTER⇢RGN`(region)·`ROUTER⇢OPA`(정책). cross-cutting/관리(Registry·Enrollment·Config·Fleet·Audit)는 미연결 유지. '그리는 규칙' 노트 갱신 | (작성자 ID 미지정) |
| 2026-06-25 | **ADR-11 CCB 승인 완료(오늘 회의)** — Appendix A 주석·결정 로그 행·Appendix B #13을 'CCB 승인(2026-06-25)'으로 갱신, #13을 B-2(미결)→B-1(완료)로 이동. 잔여=클라이언트 `Vatech-Target` 부착(구현·③-P, 결정 아님). ARD ADR-11 행도 'CCB 승인' | (작성자 ID 미지정) |
| 2026-06-25 | Appendix B 재구성 — **B-1 완료·확정 / B-2 미결** 2구획 분리(번호 보존). 완료=#7·#10·#17·**#19(디바이스=EzServer)**·**#20(GW AWS 전용)**·**#21(Console Admin+C/S)**·#22(업로드 GW 비발급)·#23(apex DNS) 신설/이동. 미결=#1~#6·#8·#9·#11~#16·#18(11건) | (작성자 ID 미지정) |
| 2026-06-25 | **디바이스 = EzServer 확정(Scott, Agenda #1 종결)** — "GW 관점의 '디바이스'는 물리 HW가 아니라 EzServer"로 통일. §1.4 용어 정의 추가, §2.3.1(2)/§2.3.2/§7.1.1/§7.2 헤딩·본문·시퀀스 participant(의료 디바이스→EzServer)·§2.1·§2.2 다이어그램(디바이스 직접 연결 `DEV→GW`/`DEV→AUTH` 제거 → `DEV→EZ`, 물리장비=EzServer 뒤·GW 비대상; Device Registry→EzServer Registry)·ADR-08·actor표(§2.3/§2.5/§4) 갱신. DBML `device` 테이블=EzServer 주석(컬럼 리네이밍은 LLD) | (작성자 ID 미지정) |
| 2026-06-25 | **C/S 등록 확인 + Console 사용자 역할(회의 결정)** — 자동 등록 후 C/S(현장 설치 담당)가 GW Console에서 클리닉 정상 등록을 확인. Console 사용자=**Admin + C/S**(§7.9.2), 확인 UI·역할 세부 권한은 **③-C Console Sub-SRS**. §2.3.1에 C/S 확인 노트 추가 | (작성자 ID 미지정) |
| 2026-06-25 | **클리닉 등록 = EzServer 자동·무조건 확정(회의 결정)** — EzServer가 LMP Clinic-ID 수신 시 자동으로 GW에 Clinic-ID 전송·등록, **외부 연동 무관 무조건 등록**. §2.3.1 텍스트·시퀀스(LMP→EzServer→GW)·§7.3 정합, 등록 주체 EzServer로 확정(Appendix B #17 종결, CleverOne 대안 폐기). org_mapping은 연동 시에만 | (작성자 ID 미지정) |
| 2026-06-25 | **GW 배포 = AWS 전용 확정(회의 결정)** — AWS 미지원 국가도 별도 GW 없이 **가장 가까운 AWS 리전 GW에 접속**(GeoDNS); 주권용 storage(MinIO)는 **Provider 제공·GW 중계만**(GW storage 비호스팅). 직전(같은 날) 검토했던 포터빌리티 레이어를 **롤백** — **§2.1.2(비AWS·포터블 배포) 삭제**, §3.1.2를 AWS-native로 복귀(**SQS·IoT Core·IRSA·Aurora·ElastiCache·EKS·ECR·ALB/Route53·CloudWatch/ADOT**), §3.1.1·§3.3·§4.4·§7.6.3(A·SQS)·§7.6.6(B·IoT Core/Amazon MQ)·§2.1.1(AWS 전용 노트)·§7.3.5·Appendix B #4·개발계획서 §5 정합. §3.1.2 오브젝트 스토리지는 'GW 비호스팅·Provider storage(AWS=S3/비AWS국=MinIO) 중계' | (작성자 ID 미지정) |
