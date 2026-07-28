# VT API Gateway — 실행 할당표 (조정 인덱스)

> 제품 적응 스펙의 **소유자·진행 상태 트래커**(내부 작업 문서, 비공유).
> *무엇을·어느 단계에* 바꾸는지(작업 내용)는 [개발 Roadmap 결정 §4 (제품×단계)](<../VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>)가 정본이며, 본 문서는 중복 서술하지 않고 *누가·어느 GW 앵커에 의존·현재 상태*만 추적한다.

## 원칙 (계약 vs 적응)

- **③ [GW SRS](03-srs-gateway/SRS.md)가 계약(contract)의 단일 SSOT**다. GW가 노출하는 외부 인터페이스(§4)·기능 동작(§7)만 정의한다.
- 다른 제품(CleverSpace·CleverOne·EzServer·Infra)의 변경은 **계약을 소비하는 적응(adaptation)** 이며, 각 제품 소유자가 자기 산출물로 책임진다.
- **드리프트 방지**: 제품 산출물은 GW 계약을 *재정의하지 않고* GW SRS의 §앵커를 *참조*만 한다.
- **작성 모델**: GW 소유자가 각 제품 산출물의 **1차 초안**을 작성한 뒤 해당 제품 담당자에게 **인계**하여 확정한다. (소유권은 인계 후 담당자에게 이전)

## 실행 할당표 — 소유자·앵커·상태 트래커

> 작업 내용(제품×단계)은 [Roadmap §4](<../VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>) 참조. 본 표는 소유자·의존 앵커·상태만.

| 단위 | 제품 | 산출물 형식 | 최종 소유자 | 의존 GW 앵커 | 상태 |
|------|------|-------------|-------------|--------------|------|
| ③ | VatechAPIGateway | SRS (메인, 계약 정본) | GW (본인) | — | 작성 중 |
| ③-C | GW Console | Sub-SRS | GW (본인)→이관 | §7.9 | 미작성 |
| ③-P-CS | CleverSpace | One Pager (1·2·3·4단계 통합·①②흡수) | CleverSpace 팀 | §2.3.5·§7.4·§7.7·§4.5.1·§7.3 | **초안 작성중**(Raymond·2026-07-27·완료 후 CleverSpace 팀 인계) |
| ③-P-CO | CleverOne | One Pager (1·2·3·4단계 통합·①②흡수) | CleverOne 팀 | §7.7.1·§2.3.0·§7.4·§7.3 | **초안 착수**(Nick→Raymond·2026-07-27·OnePager 지금·연동 구현 post-v1.0) |
| ③-P-EZ | EzServer | One Pager | EzServer 팀 | §4.5·§7.3·§7.6.6 | **인계** (ezserver_suite `doc/onepager/gw_adaptation`·target `v6.5.x`·2026-07-21) |
| ③-P-LMP | LMP (License Portal) | One Pager (조건부) | LMP/ELM 팀(ES)→이관 | §2.3.1 B·§7.1.1·§7.1.4 | **초안**(조건부·R9서 B 채택 시) |
| ③-I | Infra | IaC 구축 계획서(기능 스펙 아님) | 인프라 담당 | §3.1·§4.5.1·§7.3.5 | 미작성 |

> 형식은 변경 크기로 결정한다(일률 One Pager 아님): 단순 적응은 티켓으로 충분할 수 있다. **CleverSpace·CleverOne은 7/23 결정으로 각각 One Pager 1개(1·2·3·4단계 통합·①호환성·②Presigned One Pager 흡수)로 확정** — 멀티 Region(4단계)이 커지면 해당 절만 Sub-SRS로 승격 가능.

### 스펙 문서 등록처·경로·baseline (SSOT)

각 spec 정본의 Repo·경로·baseline 태그. **인계·baseline 시 갱신.** _(미정 = 등록처 미확정 — 7/30 Agenda R3에서 결정 · OnePager는 담당팀 baseline 시 tag 부여)_

| 단위 | 스펙 문서 | Repo (Azure DevOps) | 경로 | baseline tag |
| --- | --- | --- | --- | --- |
| **③** GW | SRS(+OpenAPI·DBML·UnitTCL) | `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway` | `docs/specs/SRS.md` · `docs/specs/design/`(openapi·dbml) · `docs/specs/UnitTCL.md` | **`spec-v1.0.2`** (35c87ab) |
| **③-C** GW Console | Sub-SRS | `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console` (별도 repo·GW 소유→이관) | 미작성(신규 repo·경로 TBD) | 미작성(연기) |
| **④** AXS | Sub-SRS | 〃 vt-api-gateway (GW 소유) | `docs/specs/04-subsrs-straumann-axs/` | 미작성(보류) |
| **③-I** 인프라 | IaC 구축계획서 | `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-infra` | `docs/IaC-구축계획서.md` | 미부여(계획서·PR 진행) |
| **③-P-EZ** EzServer | GW적응 OnePager | `https://dev.azure.com/ewoosoft/ezserver/_git/ezserver_suite` (branch `v6.5.x`) | `doc/onepager/gw_adaptation/Confidential_gw_adaptation_onepager.md` | 미부여(EzServer 팀 baseline 예정·R3 확인) |
| **③-P-CS** CleverSpace | GW적응 OnePager | **미정 (R3 결정)** | 초안=작성자 개인 repo(SSOT 아님) | — |
| **③-P-CO** CleverOne | GW적응 OnePager | **미정 (R3 결정)** | 초안=작성자 개인 repo(SSOT 아님) | — |
| **③-P-LMP** LMP | OnePager(조건부) | **미정 (ES 라이선스팀?)** | — | — |

## 구현 착수 전략 (7/2 R7 = 1안 확정)

- **구현 시작점 = ④ AXS Sub-SRS baseline 이후**(고정). AXS가 첫 연동이라 이것 없이는 통합·E2E 테스트가 불가하므로, GW 구현은 ④ baseline 후 착수한다(core 일부는 ③ baseline 후 선행 가능하나 통합·테스트는 ④ 후).
- **채택 = 1안**: **④ baseline 직후 구현 착수 + ③-C·③-P·③-I 스펙을 구현과 병행**(그 스펙 종료는 뒤로 늘어남). *2안(전 스펙 완료 후 착수)은 납기 지연이 커 반려.*
- **재작업 리스크 관리**: ③-C/③-P/③-I 미확정 위에서 일부 구현하므로, 계약 SSOT(③ SRS §4·§7)에 고정된 부분부터 구현하고 미확정 영역은 스펙 확정까지 보류한다(드리프트 방지 원칙, 위).
- **구현 기간·pilot(8/15)**: 구현 기간은 **미정 — SRS 확정 후 재산정**. pilot 8/15는 어느 안이든 빠듯해 R7과 함께 재검토(개발계획서 정합). IEC 62304 추적은 스펙·구현 동시 진행이라 추적 부담↑ → PR·변경이력로 관리.

## 제품별 등장 단위 (cross-unit 맵)

한 제품은 여러 스펙 단위에 걸쳐 등장한다. 각 담당자는 자기 제품이 나오는 모든 단위를 확인한다.

| 제품 | ① 호환성 | ② Presigned | ③-P* 적응 | ④ AXS |
|------|:---:|:---:|:---:|:---:|
| CleverSpace | ✓(well-known) | ✓(발급 신규) | ✓(③-P-CS) | — |
| CleverOne | ✓(헤더·fallback) | ✓(업로드 연계) | ✓(③-P-CO) | — |
| EzServer | ✓(헤더 대리) | ✓(전송 로직) | ✓(③-P-EZ) | ✓(갈래 A) |
| Infra | 단일 Region | — | ✓(③-I) | 고정 IP·샌드박스 |

> 상태 범례: 미작성 / 초안(GW 1차) / 인계 / 리뷰 / baseline

## CI/CD 파이프라인 소유 · Jack(인프라) 조율

> **왜 여기 있나**: 7/9 준비 중 R6/R6.1로 Agenda에 올렸다가, "앱 CI 산출물=앱팀 소유, 인프라=기반 제공"은 **표준 결론이라 회의 논의 가치가 낮다**고 판단 → Agenda에서 빼고 **실행 트래커(본 문서)로 이관**(2026-07-07). **Jack과 협의 확정(2026-07-21)** — 아래.

**✅ 확정 (2026-07-21 Jack 협의)**
- **Jack 제공**: Azure Flow로 **CI/CD 전체 구축 완료** + **pipeline 템플릿**(거의 복붙 수준) + service connection·ECR·ArgoCD/배포 자동화·agent pool.
- **GW(본인) 완성**: Jack **템플릿을 앱 특화로 완성**(build·unit·e2e·lint·스캔·이미지) + **`Dockerfile`** + `azure-pipelines-config.yml`(매트릭스 발행). "GW가 백지에서 작성"이 아니라 **템플릿 완성**.
- **브랜치·배포 모델(확정)**: `main`만 유지 + 단명 **`feat/*` → PR → main** → **DEV 자동배포**. **TEST/PROD = tag prefix로 자동배포**(prefix 규칙=Jack 공지). 환경 브랜치 없음.
- **PR 자기승인**: `main` 정책에서 **"Allow requestors to approve their own changes"** 허용으로 변경(Jack 공지). 초기 개발 편의 → *prod 전 강화 검토*.

- **소유 요약**: CI/CD 플랫폼·템플릿·배포 자동화 = Jack / 앱 pipeline(템플릿 완성)·Dockerfile·매트릭스 발행 = GW.
- **타이밍**: CI 골격(build·test)은 **조기**(코드 생기면), 배포 파이프라인은 **첫 E2E 배포 시점(개발 중반)** 에 세운다(구현 착수=④ AXS baseline 후·7/2 R7). **인프라 기반은 그 전에 준비돼야 함**(의존).
- **작성 전략(위상)**: `Dockerfile`은 **인프라 무관·조기 작성**(승인 base 이미지만 후속 `FROM` 교체) / `azure-pipelines.yml`은 **build·test 골격 조기 + 배포 트리거만 Jack 전제(ECR·ArgoCD·manifest 위치) 확정 후** 채운다. 구체 stage/레이어는 구현 착수 시 코드 repo 파일·README로 둔다(planning 문서에 선반영 금지·drift 방지).

### Jack에게 확인·요청할 것 (구현 착수 전)

- [ ] **Provisioning**: service connection(ECR/S3)·ECR·S3 버킷+IAM(CI-only write)·ArgoCD 앱 등록·agent pool 생성·부여
- [ ] **(선택) 표준 템플릿 제공?** 파이프라인/`Dockerfile` 스켈레톤·승인 base 이미지 (있으면 GW는 앱 특화 부분만 채움)
- [ ] **배포 manifest 위치 관례**: `es-gitops`(GW는 이미지 태그·값만 PR 기여) vs `vt-api-gateway`(app chart 동봉·CI 렌더) — 어느 쪽?
- [ ] **rollout 트리거 방식**: `es-gitops`에 태그 bump PR / ArgoCD Image Updater / API 중?

> 위 manifest 위치·rollout 방식이 정해져야 `azure-pipelines.yml`의 "배포 트리거" 단계가 확정된다. (연계: SRS §7.7.5 매트릭스 발행 파이프라인·③-I 인프라.)
> **상태(2026-07-21)**: **Jack 협의 완료** — Azure Flow CI/CD·pipeline 템플릿·배포 자동화(merge→dev·tag prefix→test/prod) 구축됨. **남은 확인**: (1) tag prefix 정확 규칙(Jack 공지 대기) (2) Jack 템플릿 전달받아 앱 특화 완성 (3) PR 자기승인 정책 변경 적용. manifest 위치/rollout은 Jack의 ArgoCD 자동화로 해소.
