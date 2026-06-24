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

| 용어                  | 본 문서에서의 의미                                         | 비고               |
| --------------------- | ---------------------------------------------------------- | ------------------ |
| GW (VatechAPIGateway) | 모든 연동이 단일 경유하는 control plane                    | 본 SRS의 대상 제품 |
| PEP                   | Policy Enforcement Point — 요청 시점 인증·정책 집행 지점   | §7.1               |
| originator            | 요청을 _시작한_ 주체(`Vatech-*` 헤더의 권위 소스)          | §7.7               |
| `Vatech-Via`          | 요청을 _경유한_ 중계 홉(예: EzServer)                      | originator와 분리  |
| Edge                  | 클리닉 현장의 EzServer (방화벽 뒤, inbound 불가)           | §7.6               |
| soft-state            | 완전 stateless가 아닌, cache TTL·mapping_version 기반 상태 | ADR-02             |
| Region Signer Agent | **폐기(2026-06-23)** — GW는 presigned 직접 발급·서명 안 함(발급=upstream CleverSpace/AXS, GW 중계) | §4.1.4·§7.4 |
| ClinicID↔Org-ID       | 클리닉 식별자와 외부(AXS) 조직 식별자 매핑                 | §7.3 / ④           |
| 경로 B (Path B)       | CleverOne → CleverSpace 직접 연동(EzServer 미경유)         | Deprecated 대상    |

> ❓확인 — 추가로 등록할 용어(예: PHI, allowlist) 또는 사내 공유 용어집 링크 여부.

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
        EZ["EzServer (Edge)"]
        DEV["의료 디바이스"]
    end
    subgraph GWBOX["VatechAPIGateway (본 SRS 대상)"]
        GW["GW core<br/>인증·라우팅·region·외부 연동"]
        WHR["Webhook Receiver<br/>단일 수신·분배 (sub-tier)"]
    end
    subgraph CLOUD["우리 클라우드"]
        CS["CleverSpace (멀티 Region)"]
        CLAB["CleverLab"]
        OID["OneID"]
    end
    AXS["Straumann AXS (외부)"]
    R53["Route 53 GeoDNS"]
    CONSOLE["GW Console (③-C)"]

    CO --> EZ
    EZ -->|"API 요청 (상행)"| GW
    DEV --> GW
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
```

| 외부 시스템 | 역할 |
| --- | --- |
| CleverOne / EzServer | 사내 호출자. EzServer는 Edge(방화벽 뒤, inbound 불가) |
| CleverSpace | 멀티 Region 백엔드(데이터 경로 대상) |
| OneID | 사람·클리닉·사내 호출자 인증(OIDC) |
| Straumann AXS | 외부 연동 대상. Webhook 수신·presigned 연동 |
| CleverLab | 우리 클라우드 기공소 PMS. GW의 **프록시 대상이 아니라 갈래 B 클라우드 클라이언트**(CleverLab→GW→AXS) + AXS 이벤트 webhook 수신처. **CleverLab↔AXS 직접 연동(갈래 B)은 현 시점 범위 외/보류**(§1.2·④ — 외부 cloud 연동 일반 역량은 유지) |
| Route 53 GeoDNS | EzServer를 최근접 GW Region에 연결 |
| GW Console | Admin Web(③-C Sub-SRS) — 관리 API 호출 |

> 상세 인터페이스는 §4. **Webhook Receiver는 GW 내부의 별도 sub-tier**(외부 서버 아님 — A면 GW 고유 API, §4.1.1·§7.6.1). **API 호출 경로는 대상에 무관하게 동일하다** — `CleverOne→EzServer→GW→CleverSpace` 든 `…→GW→AXS` 든 모두 **GW를 단일 경유하는 target-routed proxy**(ADR-11, 경로 B 제거). 차이는 **trust profile뿐**: 내부(B=CleverSpace·OneID, 통과+정규화 신원) vs 외부(C=AXS, GW가 OAuth·고정 egress IP 추가). 그래서 다이어그램의 `GW→upstream` 화살표는 같은 종류이고, AXS만 라벨이 `C·외부`다. **CleverLab은 GW가 호출하는 프록시 대상이 아니라**, 클라우드↔클라우드 외부 연동(갈래 B)에서 **GW를 호출하는 클라이언트**다(CleverLab→GW→AXS) — 현 시점 **보류**(§1.2).
>
> **유일하게 다른 건 Webhook(이벤트 인바운드)** — AXS는 결과 이벤트를 GW로 _밀어 보내고_, GW가 **Webhook Receiver**로 받아 방화벽 뒤 **EzServer는 MQTT(하행, 갈래 A 역방향)**·**클라우드는 HTTP push**로 분배한다(대상=Org-ID→Clinic→리전 매핑, §7.3). 클라우드 수신 대상은 **CleverLab(갈래 B·보류)뿐**이며, **CleverSpace는 webhook 수신 대상이 아니다**(B 프록시·presigned 백엔드일 뿐 — 다이어그램엔 *API 호출 대상*으로만 그린다). 대상별 시나리오는 §2.3.6. AXS의 **외부 연동(egress)은 GW core**, **Webhook(인바운드)은 Webhook Receiver**로 들어와 방향이 반대다. 멱등·교차 리전 등 분배 상세는 **§2.3.6·§7.6**.
>
> **본 도는 control plane(정보 경로) context다** — **대용량 데이터의 presigned 직접 업로드(EzServer/디바이스→storage, GW 미경유)·비-AWS minio·리전별 CS 노드는 생략**했다(Roadmap §2.6은 데이터 plane까지 함께 그림). 데이터 경로는 §2.3.4(경로①)·§2.3.5(경로③)·§4.1.4, 멀티 리전·minio는 §2.1.1·§3.1.2 참조. ❓확인 — 누락된 외부 시스템 여부(예: 결제·알림 등).

### 2.1.1 배포 토폴로지 — 멀티 서버·멀티 리전 (egress·Webhook)

GW는 두 축으로 다중화된다: **멀티 서버**(한 리전 내 Multi-AZ K8s 복제본 — HA·수평 확장, §6.3.1) 와 **멀티 리전**(서울·미주 등, gw/1.2·§7.3.5). 두 경우 모두 **inbound는 안정 endpoint 하나**(리전별 LB, GeoDNS 뒤)로 수렴하지만 **outbound(egress)는 NAT EIP 다수**로 나간다 — **inbound IP ≠ egress IP**. GW pod는 **무상태(soft-state, ADR-02)** 라 DB·Redis를 pod마다 두지 않는다 — **같은 리전 pod는 동일 저장소를 공유**하고, 라우팅·식별 데이터는 **전역 일관**으로 둔다(데이터 토폴로지는 다이어그램 아래 참조).

> **v1.0은 단일 리전(예: 서울)만 실제 배포**한다(§2.7.1). 아래 다이어그램의 **멀티 리전(A·B)은 2차(gw/1.2) 목표 토폴로지**이며, v1.0 설계가 이를 *ready*로 갖춘다 — **구조(데이터 토폴로지·Region Resolver·apex DNS·egress 집합)는 동일하고 리전 수만 1→N**이다. v1.0을 보려면 리전 1개(예: RA)만 두고 GeoDNS·apex가 그것을 가리킨다고 읽으면 된다(전역 SSOT는 단일 리전 내 존재, 2차에 복제 추가).

```mermaid
flowchart TB
    EZ["EzServer / CleverOne / 디바이스"]
    R53["Route 53 GeoDNS<br/>(최근접 리전 라우팅)"]
    EZ --> R53

    subgraph GTIER["GW 전역 계층 (리전 비종속 · GW의 일부)"]
        WHIN["Webhook Receiver — 유연 수신 (Integration Plane)<br/>공개 호스트 1개 · provider별 등록 경로(예: /webhooks/axs)<br/>발신자 검증·멱등 후 매핑으로 리전 판정"]
        GLOBAL[("전역 일관 데이터 SSOT — PostgreSQL 원본<br/>매핑 · 레지스트리 · Org-ID↔ClinicID · 정책 · compat · JWKS<br/>→ 리전으로 복제/sync")]
    end

    subgraph RA["GW Region A (서울) · Multi-AZ HA = 멀티 서버"]
        LBA["Ingress LB<br/>안정 endpoint A (inbound 1)"]
        GA1["GW pod (무상태)"]
        GA2["GW pod (무상태)"]
        STA[("Region A 저장소 = pod 공유<br/>PostgreSQL: 전역데이터 복제본 + 리전로컬(audit·in-flight queue)<br/>Redis: 빠른 조회 캐시(로컬 PG에서·멱등·nonce)")]
        NATA["NAT GW<br/>고정 egress EIP set A (outbound 다수)"]
        LBA --> GA1
        LBA --> GA2
        GA1 --- STA
        GA2 --- STA
        GA1 --> NATA
        GA2 --> NATA
    end

    subgraph RB["GW Region B (미주) · Multi-AZ HA = 멀티 서버"]
        LBB["Ingress LB<br/>안정 endpoint B (inbound 1)"]
        GB1["GW pod (무상태)"]
        GB2["GW pod (무상태)"]
        STB[("Region B 저장소 = pod 공유<br/>PostgreSQL: 전역데이터 복제본 + 리전로컬(audit·in-flight queue)<br/>Redis: 빠른 조회 캐시(로컬 PG에서·멱등·nonce)")]
        NATB["NAT GW<br/>고정 egress EIP set B (outbound 다수)"]
        LBB --> GB1
        LBB --> GB2
        GB1 --- STB
        GB2 --- STB
        GB1 --> NATB
        GB2 --> NATB
    end

    R53 --> LBA
    R53 --> LBB

    STA -.->|"전역데이터 복제/sync<br/>(strong-consistency·mapping_version)"| GLOBAL
    STB -.->|"전역데이터 복제/sync"| GLOBAL

    EXT["외부 서비스 (예: AXS)<br/>region 비인지"]
    NATA ==>|"GW→외부 egress (우리가 호출)"| EXT
    NATB ==>|"GW→외부 egress"| EXT
    EXT -.->|"IP whitelist 요구 시 = EIP set A ∪ B<br/>(고정·열거·증설 시 협의)"| NATA
    EXT -.-> NATB

    EXT ==>|"Webhook (region 미지정)"| WHIN
    WHIN -.->|"Org-ID→Clinic→리전 매핑 조회"| GLOBAL
    WHIN ==>|"대상 = 리전 A"| RA
    WHIN ==>|"대상 = 리전 B (교차 리전)"| RB
```

> **일반화**: 아래는 **외부 서비스(C 프로파일) 공통** 규칙이며, **AXS는 한 예**다(향후 DS Core/3Shape 등 동일). egress IP whitelist·단일 webhook ingress·리전 분배는 provider에 무관하게 같은 방식으로 적용된다(ADR-11 레지스트리 모델과 일관).
>
> **B(내부) vs C(외부) 적용 범위**: **API 호출 경로는 내부(CleverSpace 등)·외부(AXS) 동일**(GW target-routed proxy, §2.1·§4.1.2). 본 절의 **고정 egress IP whitelist·Webhook 수신은 외부(C) 한정** 사항이다 — 내부(B) upstream은 같은 GW proxy를 타되 **내부망**이라 egress 고정 IP whitelist가 불필요하고, (현재) GW로 Webhook을 발신하지 않는다. 즉 §2.1.1이 외부(C) 토폴로지를 다루는 것이지, 내부 호출이 다른 경로라는 뜻이 아니다.

- **egress IP whitelist = 고정 EIP 집합(멀티 IP).** 외부 서비스(예: AXS)가 IP whitelist를 요구하면, 화이트리스트 대상은 GW가 _외부를 호출_ 할 때의 egress IP다. pod별 임시 IP가 아니라 **AZ/리전별 NAT의 고정 EIP**여야 하고, 멀티 리전이면 **전 리전 집합의 합집합(A ∪ B …)** 이며 유한·열거 가능해야 한다(FR-INT-03·§7.5.3·§2.6).
- **리스크/제약**: 오토스케일·새 AZ·**리전 증설은 egress IP를 늘리므로**, egress를 **고정 EIP 풀로 핀(pin)** 하고 외부(예: Straumann)와 **whitelist를 협의·갱신(리드타임)** 해야 한다. EIP 풀 provisioning·고정은 인프라(③-I) 책임(§2.6·§7.3.5).
- **Webhook 수신은 단일 호스트, region 분배는 우리 몫.** 외부 서비스(AXS 등)는 **region을 모르고**, **provider마다 호스트를 따로 둘 필요도 없다** — **단일 공개 호스트 하나**로 모든 provider를 받되, **경로/형식은 provider별 등록(레지스트리)으로 유연**하다(기본 관례 `…/webhooks/<provider>`는 예시·확정 아님 — GW는 발신자 검증·라우팅만, payload 비해석; §4.1.3·§7.6.1). 수신 ingress(Webhook Receiver, §2.2)는 **전역 매핑(DB/캐시)에 연결**되어 webhook 내용(Org-ID 등)으로 **대상 클리닉의 리전을 판정**하고(§7.3 매핑·전역 일관), **대상 리전(A·B …)으로 재분배**한다(수신 리전 ≠ 대상 리전이면 **교차 리전 전달**). 즉 **region 결정은 외부도 GeoDNS도 아니라 수신 ingress의 매핑 조회**다. `eventId` 멱등 dedup은 인스턴스 공유 저장소(Redis)로 전역 보장(ADR-02·§7.6.4). 인바운드 검증(외부 source IP allowlist·HMAC·timestamp, §7.6.2)은 egress whitelist와 **방향이 반대**다. 수신→분배 흐름 상세는 **§2.3.6·§7.6**.
  - **GeoDNS는 inbound webhook의 대상 리전을 정하지 않는다** — GeoDNS는 _호출자 위치_ 기준이라 외부의 고정 위치에선 늘 한 리전으로 귀결될 뿐이고, _처리 리전은 클리닉 소속(매핑)_ 이 정한다. 단일 호스트가 어느 리전 GW로 해석되든, 그 **수신 GW가 매핑 조회 후 대상 리전으로 재분배**한다.

#### 데이터 공유·토폴로지 (멀티 서버·멀티 리전)

- **멀티 서버(리전 내) = 데이터 공유.** GW pod는 **무상태(soft-state, ADR-02)** 이며 **DB·Redis를 pod마다 두지 않는다.** 같은 리전의 모든 pod가 **동일한 리전 DB(PostgreSQL HA)·Redis를 공유**하므로 어느 pod가 처리하든 세션·멱등·캐시가 공유된다. "멀티 서버 = 데이터 분리"가 **아니다**.
- **멀티 리전 = 데이터 부류를 나눈다.**
  - **(전역 일관) 라우팅·식별 데이터** — device/clinic↔region 매핑·레지스트리·Org-ID↔ClinicID·정책(OPA)·compat matrix·JWKS. **모든 리전이 같은 답을 내야** 한다(예: B 리전에 떨어진 Webhook이 "클리닉 X는 A 리전 소속"임을 알아야 분배 가능). 따라서 **전역 일관**으로 둔다 — soft-state 캐시 + 변경 시 strong-consistency 경로·`mapping_version`(ADR-02·§7.3.1·§7.3.2).
  - **(리전 로컬) 운영 데이터** — audit log(발생 리전)·in-flight webhook/queue. **리전마다 다르며** 합쳐서 전체다.
  - **PHI는 어느 store에도 미저장**(§6.4) — 데이터 주권은 "PHI **바이트**를 매핑된 리전 storage로 라우팅"의 문제이지 GW DB 내용 분리가 아니다(§7.3.3). 전역 데이터는 PHI 미포함 control-plane 메타라 **리전 간 복제 가능**.
- **저장소 역할(PostgreSQL / Redis).** **PostgreSQL = 원본(SSOT).** 전역 일관 데이터는 **리전 간 복제/sync**(원본 → 리전 복제본), 리전 로컬 데이터(audit·in-flight queue)는 리전 전용. **Redis = 빠른 조회 캐시(리전마다).** Redis끼리 직접 복제하기보다 **각 리전이 로컬 PostgreSQL에서 캐시(cache-aside)** 하고 **TTL·`mapping_version`으로 무효화**해 일관성을 맞춘다(멱등 키·nonce 같은 휘발 상태는 리전 Redis 로컬). 즉 일관성의 근거는 _PostgreSQL 복제 + 캐시 무효화_ 다.
- **전역데이터 복제 토폴로지 세부**(원본 primary 위치·단일 vs multi-primary·충돌 처리)는 gw/1.2 설계 결정(Appendix B #15)이나, 위 **"PostgreSQL 원본+리전 복제 / Redis 리전 캐시" 모델과 "전역 일관/리전 로컬" 구분 원칙은 버전과 무관하게 고정**이다.

> 배포·NAT·EIP·GeoDNS 구성은 **인프라(③-I)** 소유이며, 본 SRS는 _GW가 전제하는 요구_ 만 기술한다(§3.1·§7.3.5·§2.6).

## 2.2 Overall System Configuration (전체 시스템 구성)

ARD §3·§4의 **3-Plane(Control / Data / Integration)** 구성을 따른다. 컴포넌트 도출 기준 = _plane(책임 영역) + 배포 단위_. **본 도는 §2.1과 같은 그림에서 GW 쪽을 확대한 것**이며(외부 시스템은 §2.1과 동일), GW를 **GW core + Webhook ingress** 두 부분으로 나눈다.

```mermaid
flowchart LR
    %% 외부 시스템 — §2.1과 동일 (VatechAPIGateway 바깥은 §2.1과 완전히 같음)
    CO["CleverOne"]
    DEV["의료 디바이스"]
    EZ["EzServer (Edge)"]
    OID["OneID"]
    CS["CleverSpace (멀티 Region)"]
    CLAB["CleverLab"]
    AXS["Straumann AXS (외부)"]
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
                DREG["Device Registry / Lifecycle"]
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
        subgraph WHTIER["Webhook ingress (단일 수신·분배)"]
            WH["Webhook Receiver<br/>검증·멱등·매핑 분배"]
            WHQ["내부 큐 + MQTT Broker"]
            WH --> WHQ
        end
    end

    %% API 호출 — 대상 무관 동일 경로(target-routed proxy). 차이는 trust profile뿐
    CO --> EZ
    EZ -->|"API 요청 (상행)"| COMPAT
    DEV -->|"인증"| AUTH
    OIDI -->|"인증 연계 (B·내부)"| OID
    ROUTER -->|"프록시 (B·내부)"| CS
    ROUTER -->|"프록시 (C·외부)"| AXS
    ROUTER -.->|"외부(C) 시 OAuth·고정 egress IP"| CONN
    %% CleverLab은 프록시 대상 아님 — 갈래B 클라우드 클라이언트(보류): CleverLab→GW→AXS
    CLAB -.->|"갈래B 보류: CleverLab→GW→AXS"| ROUTER
    CONSOLE -.-> ADM
    R53 -.-> RGN

    %% Webhook(이벤트 인바운드)은 API 호출과 별개 — 현재 AXS만. 클라우드 수신=CleverLab만(갈래B 보류), CleverSpace는 대상 아님(§2.3.6)
    AXS ==>|"Webhook 인바운드"| WH
    WHQ ==>|"MQTT (하행)"| EZ
    WHQ ==>|"HTTP push (갈래B·보류)"| CLAB
```

> **그리는 규칙**: §2.2는 §2.1과 같은 그림에서 **GW 쪽만 확대**한 것이다 — **VatechAPIGateway 바깥(외부 시스템·엣지)은 §2.1과 동일**, 안쪽을 **`GW core`(Control/Data/Integration plane) + `Webhook ingress` 두 부분**으로 펼친다. 각 외부는 GW 내부 컴포넌트와 **1개 이상 연결**(가장 깔끔하게 1개), **common 컴포넌트**(Device Registry·Enrollment·Config·Fleet·OPA·Audit)는 가독성을 위해 **미연결**. (**예외**: CleverOne은 §2.1처럼 **EzServer를 경유**해 GW에 닿으므로 GW 내부 컴포넌트에 직접 연결하지 않는다 — `CO→EZ→GW`.) **API 호출은 대상 무관 동일 경로**(`ROUTER` = target-routed proxy, ADR-11) — CleverSpace·OneID = B(내부 프록시 대상), AXS = C(외부, `ROUTER`가 `CONN`으로 OAuth·고정 egress IP 추가). **CleverLab은 프록시 대상이 아니라 갈래B 클라우드 클라이언트**(CleverLab→GW→AXS, 보류) — GW를 _호출하는_ 쪽이다. **Webhook(이벤트)만 별개** — 현재 AXS만 GW로 발신; 클라우드 수신 대상=**CleverLab만**(갈래B 보류), **CleverSpace는 webhook 대상 아님**(§2.3.6). 수신→분배 런타임은 **§2.3.6**이 정본.

> **🔍 대안 검토 — 디바이스 인증 방식** (ADR-01)
>
> - 채택안: DPoP + 하드웨어 키(SE/TPM)
> - 대안: mTLS — 10만대 운영 부담·물리 키추출 위협 미해결로 반려
> - 상세·재검토 조건: ARD ADR-01. (본 SRS는 결정을 참조하며, 핵심 결정 로그는 Appendix A)

> 핵심 아키텍처 결정은 ARD ADR-01~10에 확정. 본 SRS는 이를 참조하고 Appendix A에 결정 로그로 연결한다.

## 2.3 Overall Operation (전체 동작방식)

GW의 주요 동작을 **시나리오별 개요(overview)** 로 정리한다. 본 절은 흐름의 골격만 보이며, **상세 시퀀스·예외·재시도 정책은 ARD §5가 정본**이다. 전체 시스템 맥락은 §2.1(제품 조망)·§2.2(3-Plane 구성)을, 단계별 아키텍처 배경은 [개발 Roadmap 결정 §2.6 (배경)](https://vks.vatech.com/x/r9iSEg)을 참조한다.

시퀀스의 참여자(액터)는 §2.1 외부 시스템·§2.2 컴포넌트와 일치한다.

| 액터 | 의미 (출처) |
| --- | --- |
| 의료 디바이스 / CleverOne / EzServer(Edge) | 사내·현장 호출자(§2.1·§2.5). EzServer는 방화벽 뒤 Edge |
| GW | 본 SRS 대상. 내부 컴포넌트(Auth·Region Resolver·Connector·Webhook Receiver·내부 큐/MQTT)는 §2.2 |
| OneID / CleverSpace / CleverLab | 우리 클라우드 백엔드(§2.1) |
| Straumann AXS / AXS S3 | 외부 플랫폼·외부 스토리지(§2.1, 경로③·§4.1.4) |
| upstream storage(S3/MinIO) | CleverSpace·AXS 등 **발급 주체 소유** 객체 스토리지 — presigned 직접 업로드 대상(§4.1.4·§7.4) |

> **본 절 시나리오 ↔ §7 기능·§4.1.4 경로 매핑**: 온보딩(§7.2)·인증(§7.1)·리전(§7.3)·파일 업로드 경로②(§7.4·§4.1.4②)·외부 연동 경로③(§7.5·§4.1.4③)·Webhook(§7.6·§4.1.3)·버전 호환(§7.7).
>
> **API 호출 경로는 대상 무관 동일**(`…→GW→upstream` target-routed proxy, ADR-11): CleverSpace(B 내부)·AXS(C 외부)는 **같은 경로**이고 trust profile만 다르다(C는 OAuth·egress 추가). 그래서 **§2.3.5(외부 연동)는 CleverSpace에도 그대로 적용되는 일반 proxy 흐름**이며, AXS를 예로 들었을 뿐 GW 동작은 동일하다. CleverSpace presign(경로②)에 **별도 시나리오를 두지 않는 이유는 경로가 달라서가 아니라**, 그 계약이 GW 밖(② One Pager·CleverSpace OpenAPI)에 있고 GW는 verbatim bypass(B)만 하기 때문이다(§4.1.4②).

### 2.3.1 온보딩 — 클리닉/클라이언트 등록 + 디바이스 enrollment — FR-RGN-\* · FR-ENR-\*

온보딩은 두 단계다: (1) **클리닉/클라이언트 등록**(최초 설치 시 region 선택 → GW 등록, 매핑 자가 생성) → (2) 그 클리닉의 **디바이스 enrollment**(머신 신뢰 부트스트랩). 분배 매핑(clinic→region·Org-ID)은 **Admin이 일일이 넣지 않고 온보딩 시 자연히 채워지며**, Admin은 잘못된 것의 **교정(override, FR-RGN-04)** 만 한다.

#### (1) 클리닉/클라이언트 온보딩·리전 등록

클리닉 최초 설치 시 **운영자가 OneID로 인증**하고 **클라이언트 UI에서 region을 선택**해 GW에 클리닉을 등록한다. GW는 자가 선언된 region을 **검증(allowlist·정책)** 후 `clinic_region_mapping`·`delivery_channel`에 저장한다(이 클리닉이 어느 region인지·webhook을 어디로 보낼지 확정). **외부 연동(AXS 등)을 켤 때** 그 provider의 Org-ID(Straumann 온보딩에서 발급, §2.3.5·④)를 등록하면 `org_mapping`에 (provider, Org-ID)→clinic이 채워져 webhook 분배 대상이 자연히 결정된다. **등록 주체는 클리닉당 1개인 EzServer의 Console(잠정안)** — 클리닉은 **CleverOne 다수 + EzServer 1개**라 클리닉당 1회 등록이 자연스럽다. **각 CleverOne(PC)에서 하는 대안도 가능하며 주체는 TBD**(③-P-EZ 잠정 / ③-P-CO 대안, Appendix B #17). UI는 제품, GW는 등록 API·검증·저장을 소유. **region은 운영 중에도 EzServer Console에서 변경 가능**(FR-RGN-04·§7.3.4 재동의·감사) — 선택지는 `GET /v1/regions`(§7.3.6)로 제공.

```mermaid
sequenceDiagram
    autonumber
    participant OP as 클리닉 운영자 (EzServer Console 잠정 · CleverOne 대안)
    participant OID as OneID
    participant GW as GW (Onboarding/Region)
    participant DB as 전역 매핑 DB
    OP->>OID: 운영자 인증 (OIDC)
    OID-->>OP: 신원 토큰
    OP->>GW: 클리닉 등록 — Clinic-ID + 선택한 region (OneID 인증)
    GW->>GW: region 검증(allowlist·정책) · Clinic-ID 확정
    GW->>DB: clinic_region_mapping · delivery_channel 저장
    GW-->>OP: 등록 완료 (이 클리닉 = 해당 region)
    Note over OP,DB: 외부 연동(AXS) 연결 시 provider별 Org-ID 등록 → org_mapping (§2.3.5·④)
    Note over GW,DB: 매핑은 온보딩 자가 등록 · Admin은 교정만(override, FR-RGN-04) — 일괄 수기 설정 아님
    Note over OP,GW: 등록 주체 TBD — EzServer Console(잠정, 클리닉당 1회) vs CleverOne(각 PC) (Appendix B #17)
```

#### (2) 디바이스 enrollment

신뢰할 수 없는 디바이스를 부트스트랩 신뢰(공장 토큰/OOB 일회 코드)로 검증해 allowlist에 등록하고 자격을 발급한다. nonce challenge로 replay를 막고, device fingerprint를 바인딩한다(등록된 클리닉 소속). 상세는 §7.2.5·§7.2.6, 흐름은 ARD §5.1.

```mermaid
sequenceDiagram
    autonumber
    participant D as 의료 디바이스
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

### 2.3.2 디바이스 인증·토큰 발급 — FR-AUTH-01/05

등록된 디바이스가 작업 전 단명 access token을 발급받는다. lifecycle·allowlist를 확인하고, claim(`deviceId`·`region`·`aud`·`TTL`)을 강제 바인딩한다. revoked 디바이스는 캐시 TTL과 무관하게 즉시 차단(§7.2.4). **갱신은 refresh token이 아니라 동일 `client_credentials` 재발급**으로 처리한다(§7.1.1 — 단명+즉시 revocation 모델). 상세는 §7.1.1.

```mermaid
sequenceDiagram
    autonumber
    participant D as 의료 디바이스
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

외부(AXS)가 GW 단일 엔드포인트로 이벤트를 push하면, GW가 검증·멱등 후 즉시 ACK하고 대상별로 분배한다(store-and-forward, ADR-09). 클라우드는 HTTP push, 방화벽 뒤 Edge(EzServer)는 MQTT QoS1 역방향. 목적지는 송신 host가 아니라 Org-ID↔ClinicID 매핑(§7.3)으로 결정한다. 수신 계약은 A버킷, payload는 외부 참조(§4.1.3). 상세는 §7.6.

```mermaid
sequenceDiagram
    autonumber
    participant AXS as Straumann AXS
    participant WH as GW (Webhook Receiver)
    participant Q as 내부 큐
    participant CL as 클라우드 대상 (CleverLab·갈래B 보류)
    participant EZ as EzServer (Edge, 방화벽 뒤)
    AXS->>WH: POST {provider 등록 경로} (HMAC·timestamp·eventId)
    WH->>WH: 서명·IP allowlist·timestamp 검증 · eventId 멱등 dedup
    WH-->>AXS: 2xx ACK (즉시)
    WH->>Q: 적재 (재시도·백오프·DLQ)
    par 클라우드 대상 = CleverLab만 (갈래B 보류)
        Q->>CL: HTTP push (내부망)
    and Edge 대상 (갈래A 역방향, b1)
        Q->>EZ: MQTT QoS1 (EZ outbound 구독)
    end
    Note over WH,EZ: 미지원 provider → 404 · 검증 실패 → 401 · 목적지=매핑(§7.3)
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

- 7.1 인증·토큰 (디바이스 머신 인증 + OneID 연계)
- 7.2 디바이스 레지스트리·온보딩
- 7.3 리전·라우팅·주권 (라우팅 키 통합)
- 7.4 파일 업로드 — presigned 중계(GW 비발급)
- 7.5 외부 연동·Connector 프레임워크
- 7.6 Webhook 수신·이벤트 분배
- 7.7 API 버전 호환성 게이트
- 7.8 Fleet 운영·Config
- 7.9 관리·감사·컴플라이언스

## 2.5 User Classes and Characteristics (사용자 계층과 특징)

| 계층                            | 사용 빈도 | 주 사용 기능              | 권한                 | 중요도 |
| ------------------------------- | --------- | ------------------------- | -------------------- | ------ |
| 의료 디바이스                   | 상시      | 인증·파일 업로드(upstream presign)·config   | 머신(디바이스 scope) | 핵심   |
| 사내 호출자(EzServer/CleverOne) | 상시      | 인증·라우팅·Webhook 수신  | 서비스(OneID)        | 핵심   |
| 외부 플랫폼(AXS)                | 이벤트 시 | Webhook·connector         | 외부(OAuth2)         | 핵심   |
| 운영자/Admin                    | 일/주     | 관리 API·매핑·kill-switch | RBAC                 | 중요   |
| 인프라/DevOps                   | 배포 시   | IaC·관측·로그             | 시스템               | 중요   |

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
| gw/1.2 | 멀티 리전·멀티클라우드 presign·signer 확장 | 4단계(후행 시) |
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

> **금지**: 단일 리전을 전제한 하드코딩(리전 고정 endpoint·단일 DB 가정·apex 없이 리전 호스트 직접 노출 등)으로 2차에 재작업이 생기지 않게 한다. 멀티클라우드 presign(FR-SES-06)도 동일 원칙 — v1.0은 단일 클라우드(S3)지만 broker 추상화는 ready(§6.3.3).

## 2.8 Backward compatibility (하위 호환성)

GW 본체는 신규 구축이나, **기존 클라이언트(구버전 CleverOne/EzServer)와 경로 B**에 대한 호환 정책이 필요하다.

- 호환 대상: 구버전 클라이언트 — well-known·오류코드 fallback으로 흡수(§7.7)
- 호환 포기: 경로 B는 **Deprecated 후 EOS** (시점 TBD — §2.8, 책임자 ❓, 마감 ❓, 영향: §7.6·① One Pager)
- 호환 매트릭스(클라이언트×API 최소버전): TBD — ① 운영 호환성 매트릭스 확정본 의존

---

# 3 Environment (환경)

## 3.1 Operating Environment (운영 환경)

### 3.1.1 Hardware Environment

서비스(클라우드) — AWS EKS(Kubernetes) 노드. 사양 상세는 인프라 담당 IaC. (TBD: 노드 타입·수)

### 3.1.2 Software Environment

GW가 동작하는 소프트웨어 스택. 근거·전체 표는 [ARD §4.5 기술 스택](<../../VT API Gateway — ARD (아키텍처).md>). 버전 `TBD`는 설계 단계 확정.

- **언어 / 런타임**: TypeScript · Node.js LTS (버전 TBD)
- **프레임워크**: NestJS (DDD 모듈 · TDD)
- **ORM / 마이그레이션**: **Prisma** (권장 — 아래 근거) · 스키마는 DBML(dev-chain-design)에서 파생
- **관계형 DB**: PostgreSQL 15.x — 레지스트리·매핑·토큰메타·정책·감사
- **캐시**: Redis — region 매핑 TTL·nonce·rate-limit·idempotency·JWKS. **Redis는 SSOT 아님**(캐시+휘발 상태). 키스페이스 정본: `design/redis/redis-keyspace.md`
- **메시지 큐**: RabbitMQ(권장) / SQS — Webhook 비동기 분배·재시도·DLQ(§7.6.3)
- **MQTT 브로커**: Edge(EzServer) 역방향 분배(QoS1·persistent, §7.6.6)
- **오브젝트 스토리지**: S3(리전) / MinIO(온프렘) — presigned 업로드 직결(§7.4, GW 미경유)
- **정책 엔진**: OPA — allowlist·region·scope·egress 판단
- **시크릿 / 키 관리**: KMS / Secrets Manager (enrollment·PKI는 Vault 검토)
- **컨테이너 / 오케스트레이션**: Docker · Kubernetes(EKS)
- **관측성**: OpenTelemetry · 구조화 로그(Pino) — PHI·시크릿 미기록(§6.2)
- **API 문서**: `@nestjs/swagger` code-first (`/api-docs`, §1.7.1)

> **ORM 추천 — Prisma.** 근거: (1) control plane은 저(低) QPS·CRUD 중심(PRD §10)이라 Prisma의 타입 안전·DX 이점이 크고 복잡 쿼리 한계의 영향이 작다, (2) **DBML → Prisma schema**로 이어지는 설계 산출물 흐름과 마이그레이션 일원화에 부합(`design/dbml/`), (3) 사내 NestJS 표준·ARD §4.5에서 이미 `◎ Prisma`로 채택. 대안: TypeORM(NestJS 친화이나 유지보수 리스크)·Drizzle/Kysely(SQL-first·경량이나 배터리 적음)는 _복잡 쿼리·세밀한 SQL 제어가 핵심이 될 때만_ 재검토(결정 변경 시 ADR 추가).

## 3.2 Product Installation and Configuration (제품 설치 및 설정)

Helm Chart 기반 배포(인프라 담당). 환경 변수는 KMS/Secrets Manager. 상세 TBD.

## 3.3 Distribution Environment (배포 환경)

### 3.3.1 Master Configuration

Docker 이미지(컨테이너). 빌드 산출물·태깅 절차 TBD.

### 3.3.2 Distribution Method

Azure Pipelines CI/CD → 컨테이너 레지스트리 → EKS 배포.

### 3.3.3 Patch/Update Method

롤링 배포(K8s). 카나리·롤백 정책은 FR-FLEET-04(v1.1) 참조. 상세 TBD.

## 3.4 Development Environment (개발 환경)

### 3.4.1 Hardware Environment

N/A(기존 개발 PC와 동일)

### 3.4.2 Software Environment

Node.js / NestJS / Prisma / PostgreSQL(local) / Docker / Cursor·VS Code. 버전 TBD(설계 단계).

## 3.5 Test Environment (테스트 환경)

### 3.5.1 Hardware Environment

N/A(기존과 동일)

### 3.5.2 Software Environment

AXS `unstable` 테스트 환경 전제(④ Sub-SRS). 단위(Jest)·E2E·부하 테스트 도구 TBD.

## 3.6 Configuration Management (형상관리)

### 3.6.1 Location of Outputs

- 소스코드: Azure Repos `vt-api-gateway` (es-platforms)
- 문서: 본 SRS는 작성은 `scp-architecture`, 공식 리뷰·baseline은 `vt-api-gateway/docs/specs/`

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

> 결정 근거·반려 대안(경로 네임스페이스 라우팅 / 투명 프록시 / 클라이언트 지정 upstream)은 **ADR-11(라우팅 모델: target-routed proxy)** 참조(ARD에 정식 기재 — Appendix B 추적). 본 절은 SRS 차원 규칙 요약.

### 4.1.3 Webhook API 정의 방침

Webhook은 두 면(§4.1.1) 어느 쪽에도 깔끔히 떨어지지 않는 **하이브리드**다 — *수신 엔드포인트*는 GW 수신면(외부가 `Vatech-Target` 없이 직접 POST — 단 **경로·스키마는 provider 규약 수용·유연**, GW 비강제), *이벤트 payload 스키마*는 C(외부 소유·참조만), *분배*는 내부 경로(클라우드 HTTP push·Edge MQTT)다. 단순 host 기반 프록시가 아니라 **수신→검증→멱등→ACK→매핑 기반 분배**의 store-and-forward 모델이다(§7.6). 따라서 API를 "전부 새로 정의"하지 않고, **GW가 소유하는 면만 정의하고 나머지는 참조**한다. 추후 §7.6 상세화 시 아래 4가지를 구분해 작성한다.

1. **수신 엔드포인트 = 유연·레지스트리 기반 수신기 (GW가 스키마·경로를 강제하지 않음).** GW가 소유·정의하는 것은 _수신 동작(발신자 검증→멱등→ACK→매핑 기반 분배)_ 이지 **제공자의 요청 스키마·경로가 아니다** — provider의 API 규약은 provider가 정하고, GW는 **어떤 형태의 인바운드 요청이든 수용**한다(해석 주체는 GW가 아니라 소비자).
   - **경로/형식은 provider별 등록(레지스트리)으로 유연**하게 둔다. 기본 관례는 `…/webhooks/<provider>`(예시)이나 **확정 계약이 아니며**, provider가 요구하는 경로/포맷을 등록해 수용한다. 호스트는 §4.5.1.
   - **provider 식별·검증**: 등록된 라우트 + 서명(provider별 HMAC)·소스 IP allowlist·timestamp로 _누가 보냈는지_ 확인한다. 미등록/검증 실패 → 거부(`401`/`404`).
   - **payload는 GW가 해석하지 않는다** — 검증·라우팅에 필요한 **최상위 식별자(provider·eventId·org 식별자 등)만** 추출하고 본문은 그대로 통과(opaque). 본문 스키마를 GW가 정의/재정의하지 않는다.
   - **응답**: 즉시 `2xx` ACK(§7.6.3). 에러 `400`(형식)·`401`(서명·IP·timestamp).
   - OpenAPI에는 _수신·ACK envelope_ 만 최소 표기하고, 경로는 기본 관례로 **예시**하되 provider별로 가변임을 명시한다(payload는 opaque/`$ref`).

2. **이벤트 payload 스키마 = 정의하지 않고 참조한다 (C버킷).** AXS 등 외부 소유. 정본은 **④ Sub-SRS + AXS OpenAPI 스냅샷**(`references/axs-openapi/`). GW는 검증(HMAC·멱등)에 필요한 **최상위 식별 필드(eventType·eventId·org 식별자 등)만 알면** 되고, 그 외는 분배 시 통과시킨다.
3. **분배 경로 = REST API로 노출하지 않는다 (내부).**
   - 클라우드 대상(**CleverLab** — 갈래 B 수신처; CleverSpace는 webhook 대상 아님): **받는 쪽 백엔드의 OpenAPI**가 정본(B버킷 성격, 내부망 HTTP push). GW는 그 API를 호출할 뿐 정의하지 않는다.
   - Edge(EzServer): **MQTT QoS1**(§7.6.6) — REST가 아니므로 OpenAPI 대상이 아니다. 토픽 네이밍·payload·QoS·retain 규약은 별도(AsyncAPI 또는 §7.6 표)로 기술한다.
4. **목적지 결정 = 매핑이다, 송신 host가 아니다.** payload의 식별자(예 AXS Org-ID)를 ClinicID로 매핑(`org_mapping` 테이블, §6.4)하고 ClinicID→region(§7.3)→분배 채널(`delivery_channel`)로 대상 client를 정한다. GW는 본문을 해석하지 않고 이 라우팅 키만 본다. 매핑 규칙 상세는 ④ Sub-SRS.

> **정의 산출물 배치**: 수신 엔드포인트는 GW 단일 OpenAPI(`design/openapi/vt-api-gateway.openapi.yaml`)에 다른 GW 고유 API와 **함께** 둔다(code-first 단일 `/api-docs`와 일관). 외부 payload는 `$ref`로 분리 참조, MQTT 분배는 OpenAPI 밖(AsyncAPI/규약 문서). 별도 `webhook.openapi.yaml`로 쪼개지 않는다 — 같은 서비스가 노출하는 한 면이기 때문.

### 4.1.4 업로드·Presigned 경로 구분

파일 전송은 **control plane(API 면)** 과 **data plane(바이트 경로)** 을 분리해 이해한다. **GW는 presigned를 발급하지 않는다** — 발급 주체는 upstream(CleverSpace·AXS)이고 GW는 발급 요청을 **중계(bypass)** 만 한다. 파일 **바이트**는 어느 경로든 발급 주체 storage로 **직접** 업로드(GW 미경유).

> **폐기(2026-06-23 결정)**: 이전 \"경로①(GW Region Signer가 우리 리전 storage용 presigned 직접 발급, `/v1/uploads`)\"는 **철회**되었다. GW는 서명·세션·storage를 소유하지 않는다. 아래 ②③만 유효하며, 번호는 기존 참조 보존을 위해 그대로 둔다.

#### 두 가지 업로드 경로 (둘 다 GW 중계·bypass)

| #   | 대상                                  | presign·업로드 **요청 API** (control)                              | presign **발급 주체** | GW 역할                                                       | OpenAPI 정본          |
| --- | ------------------------------------- | ------------------------------------------------------------------ | --------------------- | ------------------------------------------------------------- | --------------------- |
| **②** | **CleverSpace 등 사내 백엔드** presign·파일 API | **B 프록시** — `Vatech-Target: cleverspace`, upstream 경로 verbatim(§4.1.2) | **CleverSpace**       | **verbatim bypass** — 요청/응답 body 그대로 통과, GW 해석·변환·서명 **없음** | CleverSpace OpenAPI   |
| **③** | **Straumann AXS** 등 외부 presign·파일 API   | **C 프록시** — `Vatech-Target: axs`, upstream 경로 verbatim(§4.1.2)     | **AXS**(외부)         | **verbatim bypass** + OAuth2·egress allowlist(§7.5)           | ④ Sub-SRS + AXS 스냅샷 |

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

의료 디바이스와는 네트워크(REST/TLS) 인터페이스만. 직접 제어하는 HW 없음 → `None`.

## 4.4 Software Interface (소프트웨어 인터페이스)

| 구성요소                        | 버전                       | 용도                                                                                      |
| ------------------------------- | -------------------------- | ----------------------------------------------------------------------------------------- |
| OneID (OIDC)                    | TBD                        | 사람·클리닉·사내 호출자 인증                                                              |
| Straumann AXS API               | OpenAPI 스냅샷(2026-06-16) | 외부 연동(④)                                                                              |
| PostgreSQL                      | 15.x                       | 레지스트리·매핑·토큰메타·정책·감사                                                        |
| Redis                           | TBD                        | region 캐시·nonce·rate-limit·idempotency·JWKS                                             |
| 메시지 큐 (RabbitMQ 권장 / SQS) | TBD                        | Webhook 비동기 분배·재시도·백오프·DLQ(§7.6.3). 선정 기준은 전달 보증·포터빌리티(ARD §4.5) |
| 오브젝트 스토리지 (S3 / MinIO)  | TBD                        | 발급 주체(CleverSpace/AXS) storage — presigned 직접 업로드(GW 미경유, §4.1.4·§7.4)            |
| MQTT Broker                     | TBD                        | Edge(EzServer) 분배(QoS1)                                                                 |
| OPA                             | TBD                        | allowlist·region·scope·egress 판단                                                        |

## 4.5 Communication Interface (통신 인터페이스)

- 프로토콜: HTTPS(TLS 1.2+). Webhook 수신=HTTPS POST. Edge 분배=MQTT(QoS1·persistent).
- 보안: Bearer JWT(사내), OAuth2 client_credentials(디바이스·AXS), Webhook HMAC 서명·IP allowlist·timestamp.
- 동기화: idempotency key(업로드 commit·Webhook eventId), 재시도·백오프·DLQ.
- presigned: 디바이스→리전 storage 직결(GW 미경유).

### 4.5.1 공개 엔드포인트(DNS) — 제안

DNS 호스트는 *클라이언트가 접속하는 외부 계약*이므로 본 SRS에 기록한다. 단, **DNS 발급·관리는 인프라/플랫폼팀 소유**이므로 아래는 제안이며 확정 대기다.

| 용도 | 제안 호스트 | 비고 |
| --- | --- | --- |
| GW API (GeoDNS apex) | `gw.vatech.com` | **클라이언트가 호출하는 유일한 호스트.** Route 53 GeoDNS로 최근접 리전 라우팅(§7.3.5). **v1.0(단일 리전)에서도 apex를 사용** — apex가 단일 리전을 가리키고, 2차에 백엔드만 N개로 늘린다 |
| Webhook 수신 | `https://gw.vatech.com/webhooks/<provider>` (기본 관례·예시) | 단일 호스트, **경로/형식은 provider별 등록으로 유연**(§7.6.1·§4.1.3) — 확정 계약 아님 |
| 리전별 엔드포인트(내부) | `gw-<region>.vatech.com` (예: `-apne2`) | GeoDNS 백엔드·내부/운영용. **v1.0부터 네이밍 규칙 예약**(단일 리전 1개만 실재), 2차에 N개로 확장. 클라이언트엔 노출하지 않음 |
| GW Console | `console.gw.vatech.com` | **③-C 영역** — 본 SRS는 참조만. 확정은 ③-C Sub-SRS |

> **멀티리전-ready DNS (§2.7.1).** v1.0이 단일 리전이라도 **클라이언트는 처음부터 apex(`gw.vatech.com`)만** 사용한다(리전 호스트 직접 노출 금지). 그래야 2차 리전 추가 시 **클라이언트·헤더 변경 없이 GeoDNS 백엔드만 늘려** 멀티 리전이 활성화된다. 즉 v1.0에서 apex→단일 리전 1:1이고, 2차에 apex→GeoDNS→N리전으로 _DNS 구성만_ 바뀐다. (apex 없이 단일 리전 호스트를 클라이언트에 박으면 2차에 클라이언트 재배포가 필요 — 금지.)

- **TBD**: 위 호스트명 확정
  - 미결 이유: DNS·인증서·GeoDNS 구성은 인프라/플랫폼팀 결정 사항
  - 결정 책임자: ❓ (인프라/플랫폼팀)
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

NestJS 모듈(bounded context) 분리·TDD. 구조화 로그·OpenTelemetry. (NFR-MNT/OBS)

- **로그 취합·분석은 인프라 담당 영역**(2026-06 회의) — GW는 구조화 로그(Pino)·trace(OpenTelemetry)를 **생성·노출**하고, 중앙 수집·저장·분석 파이프라인은 인프라가 구성한다(③-I). **로그 포맷(필드·상관관계 키·레벨)은 검토 중(TBD)** — 확정 시 GW·인프라 합의(영향: §6.2 PHI·시크릿 미기록 제약 준수, Appendix B #14).

### 6.3.3 Portability (이식성)

IaC 환경 재현으로 이식 대비. (presign broker는 GW가 두지 않음 — 발급 주체별 storage, §7.4)

### 6.3.4 Reliability (신뢰성)

Webhook 전달 보증(QoS1·재시도·DLQ), 업로드 idempotency. MTBF 목표 TBD.

### 6.3.5 Remaining Attributes (나머지 특성)

- Scalability — 플랫폼·테넌트·리전 추가가 **설정 기반(코드 변경 최소)** 으로 확장(NFR-SCL). connector(§7.5.1)·리전(§7.3)·테넌트(§7.9.1)는 설정 등록으로 추가
- Interoperability — 표준 OAuth2/OIDC/OpenAPI/Webhook 준수. 그 외 `None`.

## 6.4 Logical Database Requirements (데이터베이스 요구사항)

- ERD: [DBML — `vt-api-gateway.dbml`](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/docs/specs/design/dbml/vt-api-gateway.dbml). 신규 테이블의 컬럼·타입·인덱스·relation은 DBML(dev-chain-design)이 SSOT
- 저장 정보 유형: 디바이스 레지스트리, device/clinic↔region 매핑, 토큰 메타, 정책(OPA 입력), 감사 로그, **분배 지식 레지스트리** — Org-ID↔ClinicID(`org_mapping`, webhook 라우팅 키)·webhook provider 수신 config(`webhook_provider`)·Vatech-Target upstream(`upstream_registry`)·분배 채널(`delivery_channel`)·**GW 운영 리전 카탈로그(`region_catalog`, §7.3.6)**. **PHI 본문은 미저장**(presigned 직결)
- 캐시: Redis(region 매핑 TTL·nonce·rate-limit·idempotency·JWKS·webhook dedup). **Redis = 캐시(PG 재구성 가능) + 휘발 상태(nonce·멱등·dedup·rate-limit·lock)이며 SSOT 아님.** 키 패턴·TTL·재구성 출처는 키스페이스 카탈로그 `design/redis/redis-keyspace.md`(DBML과 나란한 설계 산출물)
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

BE = NestJS + DDD + TDD, DB = PostgreSQL, ORM = Prisma, IaC = Terraform, CI = Azure Pipelines. (ARD §4.5)

## 6.7 Memory Constraints (메모리 제한 사항)

None

## 6.8 Operations (운영 요구사항)

- (대화형) 운영자 kill-switch(FR-FLEET-02)·매핑 재지정(FR-RGN-04)
- (무인) 토큰 자동 갱신·secret 회전(FR-AUTH-03/04)
- 백업/복구 RTO/RPO TBD(인프라 담당)

## 6.9 Site Adaptation Requirements (사이트 적용 요구사항)

리전별 signer·storage 구성(주권). 비-AWS는 MinIO(v1.2). 상세 TBD.

## 6.10 Internationalization Requirements (다국어 지원 요구사항)

GW는 무인 control plane으로 UI 문자열 거의 없음. 시간은 Unix ms(UTC), 통화 무관. 운영자 메시지 다국어는 ③-C Console 영역. 본 SRS는 `N/A(기능상 해당 없음)` 수준.

## 6.11 Unicode Support (유니코드 지원)

UTF-8(메타데이터·로그). 이모지 처리 대상 아님.

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

GW는 **두 개의 인증면(surface)을 분리·공존**시킨다(ADR-08): 무인 디바이스의 **머신 인증**과 사람·클리닉·사내 호출자의 **OneID(OIDC) 인증**. 두 면은 성질이 달라 단일 인증면으로 묶지 않으며, 디바이스↔신원 매핑으로 연결된다.

### 7.1.1 디바이스 머신 인증 (P1)

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

## 7.2 디바이스 레지스트리·온보딩 (P1)

GW는 무인 디바이스를 **레지스트리**로 관리하고, 신뢰할 수 없는 디바이스를 신뢰 가능한 상태로 전환하는 **온보딩(enrollment)** 절차를 제공한다. 온보딩 = enrollment token 발급 = allowlist 등록이며, 등록된 디바이스만 인증(§7.1.1)·작업이 허용된다. 상세 흐름은 ARD §5.1.

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

GW는 모든 데이터 경로를 **단일 리전으로 고정**하여 데이터 주권(PHI 리전 밖 미이동)을 보장한다. 라우팅 키는 **device·clinic 양쪽을 동일 resolver가 수용**한다(ADR-10) — 디바이스는 클리닉에 소속되어 같은 리전으로 귀결된다. **리전 매핑은 클리닉 온보딩 시 자가 등록으로 생성**(운영자 OneID 인증·region 선택 → GW 검증, §2.3.1 — 등록 주체는 EzServer Console 잠정·CleverOne 대안, TBD)되고, Org-ID 매핑은 **외부 연동 연결 시 provider별 등록**(§2.3.5)으로 채워진다 — 운영자 일괄 수기 설정이 아니라 온보딩 산물이며, 오설정은 §7.3.4(FR-RGN-04)로 교정한다.

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

## 7.6 Webhook 수신·이벤트 분배 (P1)

GW는 외부 이벤트의 **단일 수신·분배점**이다(ADR-09). 방화벽 뒤 Edge(EzServer)는 inbound가 불가하므로, GW가 대신 수신·검증·멱등 처리 후 대상별로 분배한다. 서비스별 개별 수신을 금지하여 서명·IP·멱등 검증의 분산을 막는다.

### 7.6.1 유연 수신 엔드포인트 (P1)

FR-WH-01 (외부 이벤트 단일 수신면, 호스트는 §4.5.1). **경로·형식은 provider 규약을 수용하는 유연·레지스트리 기반**이며 GW가 강제하지 않는다 — 기본 관례 `…/webhooks/<provider>`는 예시일 뿐 확정 계약이 아니다(§4.1.3). GW는 _누가 보냈는지_ 만 검증하고 payload는 소비자가 해석한다.

- **Input**: 외부(AXS 등) 이벤트 — HTTPS POST
- **Output**: 즉시 `2xx` ACK(§7.6.3)
- **에러**: 미지원 provider → 404, 페이로드 형식 오류 → 400

### 7.6.2 수신 검증 (P1)

FR-WH-02 (HMAC 서명 · 소스 IP allowlist · timestamp replay 방지).

- **에러**: 서명 불일치/IP 미허용/timestamp 만료 → 401·거부(부정 호출 차단)

### 7.6.3 빠른 ACK + 내부 큐 (P1)

FR-WH-04 (검증 직후 `2xx` 즉시 응답, 처리는 내부 큐로 위임 — 재시도·백오프·DLQ).

- **Side Effect**: 큐 적재. 처리 실패 N회 → DLQ 이동·알람

### 7.6.4 멱등 처리 (P1)

FR-WH-03 (`eventId` dedup — 중복 수신 1회만 반영).

- **에러/경계**: 동일 `eventId` 재수신 → 저장된 결과 반환(중복 처리 0)

### 7.6.5 클라우드 분배 — HTTP push (P1)

FR-WH-05 (클라우드 대상에 내부망 HTTP push, 순서 보존). **클라우드 수신 대상은 CleverLab만**(갈래 B·현 시점 보류, §1.2). **CleverSpace는 webhook 수신 대상이 아니다**(B 프록시·presigned 백엔드 — 대상 아님으로 확정, §2.3.6). 대상별 시나리오는 §2.3.6.

- **TBD — CleverLab 갈래 B 활성화 여부·시점**(PM/제품). 본 절은 *HTTP push 메커니즘*만 정의하고, 활성화 시 받을 이벤트(오더·확정 결과)는 ④에서 확정한다(Appendix B #16). (CleverSpace는 대상 아님 — 조사 불요.)

### 7.6.6 Edge 분배 — EzServer MQTT 역방향 (P1)

FR-WH-06 (EzServer로 MQTT QoS1·persistent, 토픽=클리닉 단위). 오프라인 시 버퍼 후 재전달. b1(pilot)에 forward + 역방향 포함(AXS pilot 일정).

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

### 7.7.5 호환성 매트릭스 단일 소스 (P1)

FR-COMPAT-05 (매트릭스를 단일 소스로 동결, 빌드/CI 반영·검증). 매트릭스 확정본은 ① 산출물과 동기화(§2.8).

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

FR-ADM-02 (권한 분리, 경량). 역할별 수행 가능 기능 제한(§6.5).

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
| 2026-06-23 | 라우팅 모델 | target-routed proxy(`Vatech-Target` 유무로 GW-own/proxy 구분, proxy는 verbatim) | 경로 네임스페이스 라우팅 / 투명 프록시 / 클라이언트 지정 upstream | upstream 무한 확장을 설정(레지스트리 1행) 기반으로 — 코드·경로 변경 0(NFR-SCL), 내부·외부 단일 규칙 | PM/아키텍트(CCB 확인 대기) | ADR-11 |
| 2026-06-23 | 리전 구축 단계화 | **1차 단일 리전(gw/1.0) → 2차 멀티 리전(gw/1.2)**, 단 v1.0부터 멀티리전-ready 설계 | 처음부터 멀티 리전 / 단일 리전 고정(확장 시 재작업) | 리스크·비용 낮추되 2차 확장을 재설계 없이(설정·배포 증분). 기존 "gw/1.0 흡수 여부 TBD"(B#7) 종결 | PM/아키텍트 | §2.7.1·§4.5.1·§7.3.5 |

> 전체 ADR(01~11)·근거는 ARD §2. 본 표는 SRS 차원 핵심 결정 요약. **ADR-11은 ARD §2에 기재 완료(v0.10) · CCB 확인 대기**(Appendix B #13).

## Appendix B. TBD·미결 항목 추적

> baseline 전 닫아야 할 결정 항목. 본문 각 절의 TBD를 한 곳에 모은 추적표(본문이 정본, 본 표는 인덱스). 설계 단계의 단순 버전·도구 TBD(§3·§4.4)는 묶어 1행으로 둔다.

| # | 항목 | 본문 | 책임자 | 마감 | 영향 |
| --- | --- | --- | --- | --- | --- |
| 1 | v1.0 목표 RPS·동시 세션(fleet 규모) | §5.1·5.2 | 인프라(규모 PL 입력) | 설계 착수 전 | §3.1·§7.1·§7.4 |
| 2 | 공개 엔드포인트 DNS 호스트명 | §4.5.1 | 인프라/플랫폼팀 | 배포 구성 착수 전 | §1.7.1·§3.1·§7.3.5·§7.6.1·①②④·③-C |
| 3 | 경로 B EOS 시점 | §2.8·§7.6 | PM(제품) | ① One Pager 확정 시 | §7.6·① |
| 4 | MQTT 브로커 운영 주체 | §2.6·§7.6 | 운영조직(미정) | ③-P-EZ 착수 전 | §7.6·ARD |
| 5 | 감사·consent 보존 기간 | §6.4·§7.9.3·§7.9.5 | 품질/법무 | baseline 전 | §6.5 |
| 6 | OpenAPI·DBML (`docs/specs/design/`) | §1.5·§4.1·§6.4 | GW(본인) | dev-chain-design 작성 후 | §7 전반 |
| 7 | ~~멀티 Region·멀티클라우드 gw/1.0 흡수 여부~~ → **결정(2026-06-23): 1차 단일 리전 / 2차(gw/1.2) 멀티 리전, v1.0은 멀티리전-ready 설계**(§2.7.1·Appendix A). 잔여: 멀티 리전 *구축 시점*만 일정에 따라 | §2.7.1 | PM/아키텍트 | 2차 일정 | §7.3·§7.4·§4.5.1 |
| 8 | 호환성 매트릭스 확정본 | §2.8·§7.7.5 | ① One Pager | ① 확정 시 | §7.7 |
| 9 | RTO/RPO·유지보수 윈도우 | §6.3.1·§6.8 | 인프라 | 설계 단계 | §6 |
| 10 | CCB 명단·승인자 | §8·§9 | PM | **확정(2026-06-23)** | 변경관리 — Scott(PM)·Raymond(GW 백엔드 리드) |
| 11 | 인증(IEC 62304/13485) 일정·준비물 | §6.13·§6.14 | 품질/마케팅 | 추후 | — |
| 12 | 인프라·런타임 상세 버전(도구·노드) | §3·§4.4 | 인프라/개발 | 설계 단계 | §3 |
| 13 | ADR-11(라우팅 모델: target-routed proxy) — **ARD 기재 완료(v0.10)**; 남은 것은 **CCB 승인** + **클라이언트 `Vatech-Target` 부착 적응**(③-P-\*) | §4.1.1·§4.1.2·§4.1.4·§7.5·Appendix A·ARD §2 | PM(CCB 승인) · 제품팀(헤더 부착) | baseline 전 | §4.1·§7.5·OpenAPI·③-P-CS/CO/EZ(헤더 부착)·① |
| 14 | 로그 포맷(필드·상관키·레벨) 검토 확정 | §6.3.2 | 인프라(취합·분석) + GW(생성) | 설계 단계 | §6.2·§6.3.2·③-I |
| 15 | 전역데이터 복제 토폴로지 세부(원본 primary 위치·단일 vs multi-primary·충돌 처리) — "PostgreSQL 원본+리전 복제 / Redis 리전 캐시" 모델·"전역 일관/리전 로컬" 구분 원칙은 고정, 복제 세부만 미정 | §2.1.1·§6.4 | PM/아키텍트 + 인프라 | gw/1.2 설계 | §7.3·§6.4·§6.3.1 |
| 16 | Webhook 클라우드 분배 — **CleverLab 갈래 B 활성화 여부·시점**(CleverSpace는 대상 아님으로 **확정**). EzServer(갈래 A) 역방향 대상 이벤트 목록 확정 | §2.3.6·§7.6.5·§7.6.6 | PM/제품 + GW(④) | ④ 상세설계 | §7.6·④·§2.1·§2.2 |
| 17 | 클리닉 GW 등록 주체 — **EzServer Console(잠정, 클리닉당 1회)** vs CleverOne(각 PC). 클리닉=CleverOne 다수+EzServer 1개 | §2.3.1·§7.3 | PM/제품 | ③-P 착수 전 | §2.3.1·③-P-EZ·③-P-CO·Roadmap §4 |

## 8 Change Management Process

- 변경 분류: Minor(문구) / Major(요구사항·NFR 수치·아키텍처)
- **CCB(Change Control Board)**
  - **핵심(승인)**: PM — **Scott** · GW 백엔드 리드 — **Raymond**
  - **옵저버(사안별)**: QA 리드·보안·인프라 — Major 변경 검토 시 필요에 따라 참여(고정 명단 없음, v1.0)
  - **확대**: 필요 시 CCB에 인원 추가(PM 합의)
- 절차: PR(영향 평가: §·Swagger·DBML·일정) → Major는 CCB(핵심 2인) 승인 → Appendix A 1줄 추가 → baseline 시 release tag

## 9 Document Approvals

본 SRS는 baseline 통과 시 인수자·일시를 본 절에 기록한다. (현재 골격 — 미승인)

| 역할                 | 인수자   | 승인 일시 |
| -------------------- | -------- | --------- |
| PM (CCB)             | Scott    | —         |
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
