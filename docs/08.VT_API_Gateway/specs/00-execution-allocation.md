# VT API Gateway — 실행 할당표 (조정 인덱스)

> [개발 Roadmap 결정 §4 (제품×단계)](<../VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>)를 **실행 가능한 산출물 할당표**로 승격한 문서다.
> 3·4단계는 GW뿐 아니라 여러 제품의 동시 변경을 요구하므로, *누가·무엇을·어느 문서로* 책임지는지 한 곳에서 추적한다.

## 원칙 (계약 vs 적응)

- **③ [GW SRS](03-srs-gateway/SRS.md)가 계약(contract)의 단일 SSOT**다. GW가 노출하는 외부 인터페이스(§4)·기능 동작(§7)만 정의한다.
- 다른 제품(CleverSpace·CleverOne·EzServer·OneID·Infra)의 변경은 **계약을 소비하는 적응(adaptation)** 이며, 각 제품 소유자가 자기 산출물로 책임진다.
- **드리프트 방지**: 제품 산출물은 GW 계약을 *재정의하지 않고* GW SRS의 §앵커를 *참조*만 한다.
- **작성 모델**: GW 소유자가 각 제품 산출물의 **1차 초안**을 작성한 뒤 해당 제품 담당자에게 **인계**하여 확정한다. (소유권은 인계 후 담당자에게 이전)

## 실행 할당표 — 3·4단계 제품 적응

| 단위 | 제품 | 3단계(GW 일원화) | 4단계(멀티 Region) | 산출물 형식 | 최종 소유자 | 의존 GW 앵커 | 상태 |
|------|------|------------------|---------------------|-------------|-------------|--------------|------|
| ③ | VatechAPIGateway | 본체·라우팅·인증·호환 집행·presigned 중계·경로 B 흡수 | Region 분배·HA·Route 53·Postgres | **SRS (메인)** | GW (본인) | — (계약 정본) | 작성 중 |
| ③-C | GW Console | — | Admin Web Console | **Sub-SRS** | GW (본인)→이관 | §7.9 | 미작성 |
| ③-P-CS | CleverSpace | GW 경유 수신 정합 | **멀티 Region 구축** | **Sub-SRS**(멀티Region 큼) 또는 One Pager | CleverSpace 팀 | §4.5·§7.3·§7.6.5 | 미작성 |
| ③-P-CO | CleverOne | Direct→GW 경유 전환 | Region 선택 UI·ClinicID | One Pager | CleverOne(Nick) | §4.5·§7.1·§7.3 | 미작성 |
| ③-P-EZ | EzServer | GW 경유 전환 | ClinicID 포함·Region 인지 | One Pager | EzServer 팀 | §4.5·§7.3·§7.6.6 | 미작성 |
| ③-P-OID | OneID | GW 연계 토큰 검증 | (멀티 Region 인증 고려) | **티켓 또는 경량 One Pager** | OneID 팀 | §7.1.4 | 미작성 |
| ③-I | Infra | 단일 Region GW | Route 53·K8s HA·비-AWS MinIO·고정 egress IP | **IaC 구축 계획서**(기능 스펙 아님) | 인프라 담당 | §3.1·§4.5.1·§7.3.5 | 미작성 |

> 형식은 변경 크기로 결정한다(일률 One Pager 아님): CleverSpace 멀티 Region은 Sub-SRS급일 수 있고, OneID는 티켓으로 충분할 수 있다.

## 제품별 등장 단위 (cross-unit 맵)

한 제품은 여러 스펙 단위에 걸쳐 등장한다. 각 담당자는 자기 제품이 나오는 모든 단위를 확인한다.

| 제품 | ① 호환성 | ② Presigned | ③-P* 적응 | ④ AXS |
|------|:---:|:---:|:---:|:---:|
| CleverSpace | ✓(well-known) | ✓(발급 신규) | ✓(③-P-CS) | — |
| CleverOne | ✓(헤더·fallback) | ✓(업로드 연계) | ✓(③-P-CO) | — |
| EzServer | ✓(헤더 대리) | ✓(전송 로직) | ✓(③-P-EZ) | ✓(갈래 A) |
| OneID | (경로 B 유지) | — | ✓(③-P-OID) | — |
| Infra | 단일 Region | — | ✓(③-I) | 고정 IP·샌드박스 |

> 상태 범례: 미작성 / 초안(GW 1차) / 인계 / 리뷰 / baseline
