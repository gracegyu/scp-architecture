**문서 정보**

| 항목           | 내용                                                                                                                                |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| 문서 유형      | 제품 요구사항 정의서 (PRD)                                                                                                          |
| 버전           | v2.2 (Roadmap 흡수)                                                                                                                 |
| 상태           | Draft — 검토·승인 후 상세 설계(ARD/HLD) 진입                                                                                        |
| 작성           | 김성훈 / Scott 실장 (ES 개발실)                                                                                                     |
| 사업 동인      | [VGBX-8906](https://vts.vatech.com/browse/VGBX-8906) · [VTWB-16535](https://vts.vatech.com/browse/VTWB-16535) (VT-Straumann 공진화) |
| 작업 추적      | ESIP-1 (Pillar) · [ESIP-2](https://vts.vatech.com/browse/ESIP-2) (v1.0) · 기획 [ESIP3](https://vts.vatech.com/browse/ESIP-3)        |
| 문서 ID        | ESIP-GW-PRD                                                                                                                         |
| 적용 제품 버전 | gw/1.0.0.0 (정규버전 Major)                                                                                                         |
| 분류           | 통제 문서 (Controlled · IEC 62304 / ISO 13485 대상)                                                                                 |
| 아키텍처       | [VT API Gateway — ARD (아키텍처)](<VT API Gateway — ARD (아키텍처).md>)                                                             |

## 0. 문서 통제 · 개정 이력 (Revision History)

Controlled document. Confluence page history = 변경 원장, 아래 개정 이력 = 통제 요약. '적용 제품 버전'으로 제품 버전(ES 4-seg / Jira fixVersion)과 결속하며, 릴리스 시 baseline을 동결한다. 승인은 위임전결(정규=품의 / 비정규=전결).

| 문서 버전 | 일자       | 작성  | 변경 내용                                                                              | 상태       |
| --------- | ---------- | ----- | -------------------------------------------------------------------------------------- | ---------- |
| v1.0      | 2026-06    | Scott | 초안 — 시나리오 2+ 외부 연동 프록시 GW                                                 | Superseded |
| v2.0      | 2026-06-08 | Scott | 외부 리뷰 반영 재정립 — 디바이스 통신 중앙화 control plane                             | Superseded |
| v2.1      | 2026-06-08 | Scott | v2 견적 6,940만 원 확정                                                                | Draft      |
| v2.2      | 2026-06-15 | Scott | ESMN Roadmap 흡수 — API 버전 호환성·OneID 인증면·Webhook Receiver·라우팅 키 통합 (§12) | Draft      |

## 1. 배경 및 목적

치과 전문 3D CT/Xray 의료장비 제조사의 SW 조직으로서, 촬영 결과물을 사내 Cloud 및 외부 장비·치료 플랫폼으로 전달·연동해야 한다. 현행 구조는 다음 한계를 가진다.

- 클라이언트의 레거시 **local host 통신 서버**에 인증·디바이스 관리가 없고, 사내 Cloud와 산발적 직접 연동된다.
- 파일이 direct 전송이라 글로벌 서비스임에도 **리전 확장이 불가**하다.
- config가 **local env 한정**이라 중앙 통제가 불가하다(의료 특성상 현장에서 손대기 어려움).

본 시스템의 목적: ① 모든 통신이 경유하는 **중앙 control plane**(인증·디바이스 관리·라우팅·config 중앙화), ② 파일은 **presigned URL**로 디바이스↔리전 직결(게이트웨이 무부하), ③ **디바이스–리전 매칭**으로 데이터가 필요 리전을 벗어나지 않음(데이터 주권), ④ 리전 이종성 수용(AWS·각국 클라우드·온프렘), ⑤ 내부·외부 클라우드 API 연동 확장, ⑥ 글로벌 HA active-active(soft-state 전제).

## 2. v1 → v2 변경 요약 (외부 리뷰 반영)

무게중심 이동: v1(외부 치료플랫폼 연동 프록시 GW) → **v2(전 세계 의료 디바이스 통신 중앙화 control plane)**. 외부 플랫폼 연동(Straumann AXS 등)은 v2의 Integration plane 첫 connector로 재배치.

- **인증**: mTLS 미채택 유지 → remote replay는 **DPoP**(sender-constrained token), 물리 키 추출은 **하드웨어(secure element/TPM) 키**로 대응. secret 자동 회전 + token claim hard binding 추가.
- **Control plane**: 완전 stateless가 아니라 **soft-state** 명시 — mapping versioning, cache TTL, 강한 일관성 경로 분리.
- **Enrollment**: nonce challenge, device fingerprint 바인딩, geo/velocity 이상탐지.
- **Presigned URL**: **Upload Session 추상화**(start → chunk URL → commit), idempotency key, checksum/ETag, 짧은 chunk TTL.
- **Region**: 디바이스 이전 대응 reassign/override API + audit(재동의·데이터 이전 포함).
- **Fleet 운영**: 별도 **1급 서브시스템**으로 승격(lifecycle/heartbeat/성공률/rollout/kill-switch).
- **Integration**: connector별 egress 정책 + endpoint allowlist, 임시 credential vs presigned 기준.
- **신규**: 레거시 **10만대 fleet 마이그레이션** 전략, clock skew 처리.

## 3. 이해관계자 (Stakeholders)

| 구분          | 역할                                                                |
| ------------- | ------------------------------------------------------------------- |
| 마케팅전략팀  | 전략 오너, 제휴 정의 (박지웅 팀장)                                  |
| 개발실 (ES)   | 설계·개발 (김성훈 / Scott 실장)                                     |
| 외부 플랫폼사 | Straumann (1차), DS Core / Envista / 3Shape (후속)                  |
| 사내 시스템   | Clever One / Clever Lab / CleverSpace / EzServer |
| 운영자        | 테넌트·키·로그·fleet 관리 (관리자 UI)                               |

## 4. 아키텍처 — 3-Plane

허가·열쇠는 중앙(control)에서 받되, 무거운 영상은 중앙을 거치지 않고 자국 리전 저장소로 직행한다.

| Plane | 역할 | 데이터 |
| --- | --- | --- |
| Control (글로벌 HA, **soft-state**) | allowlist 확인 → device→region 해석 → upload session 발급 → config push + fleet 운영 | 메타데이터만 · **PHI 미경유** |
| Data (리전 한정) | 디바이스 ↔ 리전 storage 직결(presigned/session) | 실제 영상 · **리전 밖 미이동(주권)** |
| Integration (north-south) | 내부/외부 클라우드 connector + egress 정책 | 안전 링크(presigned) pull |

soft-state: 완전 stateless 아님. region resolver cache TTL(초)·device→region `mapping_version`(drift·롤백). enrollment·revocation·region assignment는 **강한 일관성 경로**로 분리.

## 5. 핵심 설계 결정

### **5.1 인증 (디바이스 무인 인증)**

- OAuth2 client_credentials + 중앙 allowlist + OPA(allowlist·region·scope 검사). 사람 로그인 제거.
- **mTLS 미채택**(영업·10만대 운영 부담) → remote replay는 **DPoP**, 물리 키 추출은 **하드웨어 키(SE/TPM)**.
- secret 자동 회전 30~90일 + **dual-secret overlap window**(무중단 교체).
- token claim hard binding: `device_id`·`region`·`audience`·짧은 TTL.

### **5.2 Enrollment (온보딩)**

"자동"은 사람이 secret을 안 만진다는 뜻이지 등록 개방이 아니다. 문지기 = enrollment token, 그 발급 행위 자체가 allowlist 등록이다.

- 신뢰의 뿌리(강한 순서): ① 하드웨어 신원(SE/TPM + 제조사 attestation) ② 공장 주입 토큰 ③ OOB 일회성 코드(폴백). (지양: 설치 프로그램 공유 secret)
- 하드닝: nonce challenge(replay 방지) · device fingerprint 바인딩 · geo anomaly · device velocity check · rate limit.

### **5.3 파일 전송 — Upload Session**

- start upload(세션·region 해석·정책 검사) → chunk URLs 발급(리전 signer, 짧은 TTL 5~15분) → commit(무결성 확인).
- resumable/multipart 필수 · idempotency key · checksum(SHA256)/ETag. 세션은 chunk URL보다 길게 유지(느린 회선 재개).

### **5.4 리전 signer agent · Region 재지정 · Config · Fleet · Integration · 마이그레이션**

- **리전 signer agent**: 리전 자격증명·서명을 리전 내부 보관(blast radius 축소·주권). 온프렘은 outbound reverse 연결.
- **Region 재지정/relocation**: admin reassign/override API + 전 과정 audit. 데이터 이전·재동의(consent)와 묶어 컴플라이언스 절차로 처리.
- **Config 중앙화**: control plane이 디바이스 타겟팅 push/pull(레거시 local env 대체).
- **Fleet 운영(1급 서브시스템)**: lifecycle(pending→active→suspended→revoked) · config rollout/카나리 · **kill-switch** · heartbeat · upload 성공률 · 리전별 지표. *10만대 규모의 실질 난이도 1순위.*
- **Integration plane**: connector(adapter) 패턴 · connector별 egress 정책 + endpoint allowlist · pull model 우선 · 임시 credential vs presigned 기준 정의.
- **레거시 10만대 마이그레이션**: dual-run → 단계적 cutover(리전·고객군 카나리) → 레거시 폐기 · enrollment 백필 · clock skew(NTP 동기/허용오차).

## 6. 기능 요구사항 (Functional Requirements)

아래는 v1 PRD 요구사항(외부 연동·프록시·파일)으로 유효하다. v2 범위의 **디바이스 레지스트리·enrollment·fleet 운영·region resolver·upload session·마이그레이션** FR은 다음 개정에서 식별자(FR-DEV/FR-ENR/FR-FLEET/FR-RGN/FR-SES/FR-MIG)로 추가한다.

| ID                                              | 요구사항                                                         | 우선순위 |
| ----------------------------------------------- | ---------------------------------------------------------------- | -------- |
| FR-AUTH-01                                      | 외부 플랫폼별 OAuth2 인증 위임 처리                              | 필수     |
| FR-AUTH-02                                      | 사내 호출자(EzServer/Clever One)에 JWT 발급·검증                 | 필수     |
| FR-AUTH-03                                      | 외부 Access/Refresh Token 안전 저장·만료 전 자동 갱신            | 필수     |
| FR-AUTH-04                                      | 테넌트별 OAuth Client 자격증명 분리 보관                         | 필수     |
| FR-AUTH-05                                      | 토큰·시크릿 암호화 저장(at-rest), 평문 노출 금지                 | 필수     |
| FR-MT-01~03                                     | 테넌트(플랫폼×고객) 격리 · 라우팅 · 설정만으로 추가(코어 무변경) | 필수     |
| FR-PXY-01 / FR-FILE-01~02                       | 외부 규격 프록시·변환 · 대용량 파일 업로드 후 비동기 전달        | 필수     |
| FR-POL-01 / FR-ADM-01·04 / FR-AUD-01 / FR-HA-01 | 접근정책 · 관리 화면 · RBAC · 감사로그 · Multi-AZ 가용성         | 필수     |

## 7. 비기능 요구사항 (Non-Functional)

| ID            | 분류          | 우선순위                                                                                                               |
| ------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------- |
| NFR-SEC       | 보안          | 전 구간 TLS · 시크릿 암호화(KMS) · 최소 권한 IAM · 평문 로깅 금지 · **PII/환자정보 비저장**(파일 staging 후 즉시 정리) |
| NFR-PERF      | 성능          | 인증·프록시 오버헤드 p95 < 300ms(파일 제외) · 대용량 파일 비동기                                                       |
| NFR-AVA       | 가용성        | Multi-AZ 관리형 ≥ 99.9% · v2: 글로벌 HA active-active(soft-state)                                                      |
| NFR-SCL       | 확장성        | 플랫폼·테넌트·리전 추가가 설정 기반 O(1)                                                                               |
| NFR-OBS / MNT | 관측·유지보수 | 구조화 로그·메트릭·감사 분리 · IaC 환경 재현                                                                           |

## 8. 마일스톤 · 견적

| 단계           | 기간    | 산출물                                                  |
| -------------- | ------- | ------------------------------------------------------- |
| M1 설계·기반   | 1개월차 | HLD/LLD · 인증·라우팅 설계 · AXS 규격 분석 · IaC 골격   |
| M2 코어 구현   | 2개월차 | Auth/Token/Proxy/File/Policy · 관리자 UI·대시보드(경량) |
| M3 통합·안정화 | 3개월차 | AXS E2E 연동 · 감사·이중화(최소) · 부하·안정화          |

v2 견적 **6,940만 원으로 확정**(2026-06-08). 범위: control/data/integration plane + fleet 운영 + 멀티클라우드 presign brokering + 리전 signer + 레거시 10만대 마이그레이션 포함. 참고 — v1 초기 견적은 3개월 / 9.5MM / 약 7,040만 원. MM 상세 내역은 개발계획서(품의)에서 확정한다.

## 9. OSS vs 직접 구현

| 구분 | 내용 |
| --- | --- |
| OSS 활용 | Keycloak/Ory(OAuth2 AS) · Kong/APISIX/Envoy(엣지) · OPA(정책) · Vault(secret·PKI·enrollment) · MinIO(온프렘 S3) · OpenTelemetry · 글로벌 복제 DB(CockroachDB/Yugabyte) |
| 직접 구현 | 디바이스 레지스트리/lifecycle/allowlist · enrollment(+nonce·fingerprint·anomaly) · region resolver(+versioning) · upload session · presign broker(S3·Blob·GCS·MinIO) · 리전 signer agent · config 배포 · **fleet 운영** · connector+egress · 마이그레이션 툴링 · audit |
| 기존 GW 미사용 근거 | 디바이스–리전 매칭 + 멀티클라우드/온프렘 presign brokering + 중앙 config·fleet 운영 도메인 로직은 범용 API GW에 없음 |

## 10. 데이터 주권 · 컴플라이언스 · 리스크

- 데이터 주권: PHI는 control plane 미경유, presigned URL은 매핑 리전 endpoint만 지시, 객체 키·메타데이터에 PHI 미포함.
- 컴플라이언스: 국경 이동은 법적 근거·계약·동의가 기술보다 선행. **cross-border consent tracking** + **data classification tagging**(OPA 판단 근거) 시스템화.
- 규모/성능: 10만 디바이스·저동시성 → control plane QPS 낮음, 대역폭은 storage 위임. 난도는 fleet 운영.

## 11. 교차 링크

사업 동인: [VGBX-8906](https://vts.vatech.com/browse/VGBX-8906) · [VTWB-16535](https://vts.vatech.com/browse/VTWB-16535) · 작업 추적: [ESIP-1](https://vts.vatech.com/browse/ESIP-1) (Pillar) · [ESIP-2](https://vts.vatech.com/browse/ESIP-2) (v1.0) · 기획 [ESIP-3](https://vts.vatech.com/browse/ESIP-3) · 아키텍처: [VT API Gateway — ARD (아키텍처)](<VT API Gateway — ARD (아키텍처).md>) · 진척 보고: ESMN / 2026 개발실 PM / Platform/Infra (ESIP) / API Gateway

## 12. Roadmap 통합 (ESMN VatechAPIGateway Roadmap 흡수)

본 PRD의 디바이스 통신 중앙화 control plane(3-Plane)을 **골격**으로 유지하고, ESMN *VatechAPIGateway 구축 및 API 호환성 통합 Roadmap*(2026-06-11 SCServer 기술검토 회의)의 4개 요소를 v1.0 범위로 흡수한다. 상세 결정은 ARD §7, 요구사항은 요구사항 명세(COMPAT·WH·AUTH-08/09·RGN-06) 참조.

| 흡수 | 내용 | 위치 |
| --- | --- | --- |
| ① API 버전 호환성 | Vatech-\* 식별 헤더 · well-known 런타임 공시 · 오류코드 매핑/fallback · 호환성 매트릭스. GW 신설 전에도 즉시 적용(CleverSpace v1.3.0 대응) | ARD ADR-07 · FR-COMPAT |
| ② 사람 인증면 | 무인 디바이스 머신 인증(private_key_jwt·enrollment)과 별개로, **운영자(Console Admin·C/S)=사내 직원은 직원 IdP(MS365/Entra OIDC)로 인증** — 2면 공존 | ARD ADR-08 · FR-AUTH-08/09 |
| ③ Webhook Receiver | 외부 이벤트(AXS 등) 단일 수신·검증·분배. 클라우드=HTTP push, Edge(EzServer)=MQTT(QoS1) | ARD ADR-09 · FR-WH |
| ④ 라우팅 키 통합 | device→region(08)과 ClinicID→region(서비스 연동)을 device↔clinic↔region 단일 체계로 통합 | ARD ADR-10 · FR-RGN-06 |

본 흡수로 08 GW는 의료 디바이스(fleet)뿐 아니라 사내 클라우드 서비스(CleverOne·EzServer·CleverSpace) 간 연동·버전 호환까지 단일 control plane으로 수용한다.

**진행 방식(Roadmap 결정 반영).** ESMN Roadmap은 진행 시나리오를 **케이스 D로 확정**했다 — 1·2단계(API 호환성·presigned)는 **병행**, 3·4·5단계(GW 일원화·멀티 Region·Straumann)는 **통합 진행**. GW·Webhook은 **범용(다중 서비스) 구조로 설계**하되, GW 위 **첫 연동 구현은 Straumann → 이후 CleverSpace** 순이다. 본 PRD의 제품 버전 로드맵(v1.0→v1.2)과의 단계↔버전 매핑은 후속 정리한다.

### 12.1 Roadmap 단계별 스펙 문서 유형

Roadmap 5단계를 **One Pager 2 + SRS 1 + Sub-SRS 2**로 나누어 작성한다. 스펙 경계 ≠ 실행 경계 — 케이스 D는 ③·③-C·④를 통합 실행한다.

| # | Roadmap 단계 | 성격 | 스펙 문서 | 비고 |
| --- | --- | --- | --- | --- |
| ① | 1단계 API 호환성 | 기존 제품 수정 | Engineering One Pager | 즉시 착수, ②와 병행 |
| ② | 2단계 Presigned URL | 기존 경로 업그레이드 | Engineering One Pager | GW 선행 요건, ①과 병행 |
| ③ | 3+4단계 GW 일원화 + 멀티 Region | 신규 플랫폼 구축 | SRS | 프로젝트 기준 스펙. PEP·라우팅·Webhook 프레임·GeoDNS·매핑 API 등 |
| ③-C | 3+4단계 GW Console | ③ 플랫폼 **Admin Web** | Sub-SRS (③의 하위) | **4단계** 운영·온보딩 UI(매핑·클리닉·상태). 별도 레포. ③ 관리 API와 중복 금지 |
| ④ | 5단계 Straumann(AXS) | GW 위 외부 연동 | Sub-SRS (③의 하위) | ③ SRS와 중복 기술 금지. 승인·협의 단위 분리 |

> 배경·의사결정 기록(통제 문서 아님): [VT API Gateway — 개발 Roadmap 결정 (배경 문서)](<VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>). 케이스 A~D 비교·단계 의존성 분석의 원본이며, 결론은 본 §12·ARD §7로 흡수됨.
