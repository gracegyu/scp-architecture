# 6월 4일 회의록 — API 호환성 + VatechAPIGateway 통합

> 이 문서는 회의 내용을 빠짐없이 정리한 **회의록**(초안)이다. 리뷰 후 이를 바탕으로 **Roadmap·아키텍처 중심의 새 보고서**를 작성한다. 기존 `API호환성_방안비교_보고서.md`(호환성 중심)는 그대로 두고, 새 보고서를 별도로 만든다.

---

## 1. 회의 결론(방향)

- API 호환성 방안과 **VatechAPIGateway 개발**을 하나의 과제로 **통합**한다.
- 새 보고서의 **근본 목적은 VatechAPIGateway의 완성**이며, 그 과정에서 **API 버전 호환성 문제도 함께 해결**한다.
- 새 보고서는 두 입력 문서(`API호환성_방안비교_보고서.md`, `Straumann-Vatech_AXS연동_분석보고서.md`)의 **단순 합집합이 아니다.** 두 문서의 기본 아키텍처에는 모두 동의하며, 그 위에 이번 회의 결과를 반영해 **Roadmap과 아키텍처를 새로 정리**한다.

### 새 보고서의 성격

- 새 보고서는 **이 문서 하나로 개발 가이드가 완결**되어야 한다. Roadmap에는 **개발할 내용이 모두 포함**된다. 기존 문서(`API호환성_방안비교_보고서.md`, Straumann 분석 보고서)는 **꼭 필요할 때만 참고**하며, 새 보고서가 그 문서들을 읽어야만 이해되는 형태가 되어선 안 된다.
- 핵심은 **향후 개발할 Roadmap과 주요 아키텍처**의 심도 있는 정리다. API 버전 호환은 **장황한 배경 설명은 줄이되**, 개발 항목·결정·표준(헤더 등)은 **Roadmap 안에 실제 작업으로 빠짐없이 담는다**.
- **Roadmap**: 1~3단계 또는 1~4단계로 구성(몇 단계가 가장 적절한지 검토). **4단계 완료까지 6개월 내** 완료를 목표.
- 각 단계에서 개발할 내용을 **제품별로 모두** 정리하고, **표(Table)로 일목요연하게** 제시한다.
- Roadmap은 **가독성 있게 시각화**(다이어그램)한다.
- **Straumann 연동도 Roadmap에 포함**한다. 단, Straumann 연동이 **최소 몇 단계 이후에 가능한지** 분석해 적절한 시점에 배치한다.

---

## 2. 목표 아키텍처 (VatechAPIGateway 중심)

### 2.1 핵심 원칙 — 모든 연동은 GW를 통한다

- **명칭: VatechAPIGateway (이하 GW).** 향후 등장하는 모든 GW는 이것을 가리킨다.
- **EZ = EzServer.**
- 모든 연결은 **EZ → GW → 대상 서버** 경로를 따른다. 대상 서버는 CleverSpace, Straumann(AXS), 그 외 어떤 서버든 **예외 없이 GW를 경유**한다.
- 기존에 EzServer가 CleverSpace로 직접 연결하던 구간도 **GW를 통하도록 전환**한다(지난 결정).

### 2.2 EzServer의 역할 — Edge

- **EzServer는 앞으로도 Edge로 남는다(확정).** 클라우드로 흡수하는 대상이 아니라, 클리닉 현장의 표준 Edge 노드로 유지된다. 또한 EzServer를 **Rust로 새로 개발**하자는 의견도 나옴(Scott).
- **"Edge"의 의미(정리):** 엣지 컴퓨팅의 Edge — **데이터가 생기는 현장(클리닉)에 가장 가까운 노드**를 뜻하며 클라우드(중앙)의 반대다.
  - 위치: GW·CleverSpace는 클라우드(중앙), **EzServer는 각 클리닉 현장**(on-premise)에 설치되어 시스템의 가장자리에 위치.
  - 역할: CBCT/2D 영상·장비·PMS가 모두 현장에 있으므로 **현장에서 데이터를 처리·중계**한다. **무거운 데이터(CT)는 현장에 두고 presigned URL로 직접 전송**, GW에는 **메타데이터(정보)만** 올린다("데이터는 엣지, 제어/정보는 클라우드").
  - 구조: "모든 연결은 EZ → GW" 결정과 맞물려, EzServer는 **클리닉의 단일 진출입구**(표준 Edge 노드/에이전트)가 된다.
- **Rust 신규 개발과의 연결:** Rust는 단일 바이너리·저자원·고성능·메모리 안전이라 수백~수천 클리닉에 배포하는 **경량 Edge 런타임**에 적합. 즉 "Edge로 한다 = EzServer를 **현장용 경량 엣지 서버로 재정의하고 Rust로 새로 구현**한다"는 의미로 본다.
- **현황과 범위:** 현재 EzServer는 **PHP로 구현**되어 있고, 이미 **일부 기능은 Rust로 개발**된 상태다. 이번 방향은 EzServer를 **Rust로 완전 교체**(전면 재개발)하는 프로젝트다.
- **숙제(미결):** Rust 재개발 시 **기존 API를 그대로 포팅**할지, **API부터 재설계**할지 결정해야 한다(§5).

### 2.3 인증 — OneID(AuthServer) 연계

- GW는 **필요 시 AuthServer(OneID)를 경유**한다.
- 우선은 **인증 Verify 시점**에 GW가 OneID를 통하는 수준으로 본다.
- 단, OneID 연동은 인증 Verify에 **한정되지 않는다**. 토큰 발급·갱신, 권한·테넌트 조회 등 **추가 연동 지점이 더 있을 수 있으며**, **Roadmap 작성·상세 설계 단계에서 구체화**한다.

### 2.4 GW Console (관리용 Web Client)

- **Admin이 GW를 관리**하기 위한 **GW Console**이 필요하다.
- 간단한 **Web client 서비스** 형태로 구축한다.

### 2.5 데이터 전송 — 정보는 GW, 대용량 데이터는 presigned URL 직접 전송

- GW로는 **정보(메타데이터)만** 오간다.
- **Data**(이미지, CT)는 **presigned URL을 발급**받아 **EZ가 대상 스토리지로 직접 전송**한다.
- presigned URL **발급도 GW를 통해** 받는다(모든 API가 GW를 경유하므로 일관됨). 흐름: **EZ → GW → CleverSpace**.
- **현재 CleverSpace는 presigned URL 방식이 아니라 Direct 전송**으로 되어 있다 → presigned URL 방식 **신규 개발 필요**.
- 이에 따라 **EzServer의 데이터 전송 로직도 변경**되므로 **EZ 측 구현도 필요**(Roadmap 반영).

### 2.6 Region 분배 (GW의 추가 역할)

- GW는 단순 게이트웨이가 아니라 **요청을 적절한 Region으로 분배**하는 역할도 한다.
- CleverSpace를 **여러 Region에 구축**하고, GW가 요청을 보고 **알맞은 Region으로 분기**한다.
- 이를 위해 **EZ는 요청 시 ClinicID를 포함**해야 한다.
- GW는 **ClinicID별 사용 Region을 매핑하는 테이블**을 보유한다.

### 2.7 매핑 테이블 (Straumann 연구 참고)

- Straumann 연동 분석 때 매핑 테이블이 있었다: **Vatech ClinicID ↔ Straumann Organization-ID** 매핑으로 추정.
- 그 외 항목도 있었던 것으로 보임 → Straumann 보고서의 매핑/온보딩 항목 참고해 GW 매핑 테이블 설계에 반영(§참고).
- (참고: Straumann 보고서에서 Organization-ID는 DynamoDB에 등록·검증, EzServer 로컬에도 저장하는 구조였음.)
- **저장소 선정 주의:** Straumann 조사는 AWS 서버리스 전제라 DynamoDB를 썼지만, **DynamoDB는 AWS 전용**이라 AWS 미지원 환경(§2.11)에서 못 쓴다. GW가 멀티 리전·K8s·비-AWS까지 가야 하므로, 핵심 매핑/컨트롤플레인은 **이식성 있는 저장소**(PostgreSQL 등)를 원본으로 두고 **GW 메모리 캐시**로 읽는 구조가 적합하다(§5).

### 2.8 CleverOne Region 선택 UI

- CleverOne은 **최초 설치 후 접속 시** 어느 **Region의 CleverSpace**를 사용할지 **선택하는 UI**가 필요하다.
- **현재 미구현** → Roadmap의 적절한 단계(멀티 Region·GW Region 분배가 준비되는 시점)에서 **CleverOne에 Region 선택 UI를 개발**한다. 선택된 Region은 이후 요청의 라우팅 기준(ClinicID↔Region 매핑)과 연계된다.

### 2.9 고가용성(HA)과 멀티 리전

- GW는 **쿠버네티스**(Kubernetes)로 **HA 구축**.
- GW를 우선 **2개 거점**에 구축: **아시아(서울)**, **미주**.
- **구축 방식 변경(중요):** Straumann 연동 GW는 기존 분석에서 **AWS 서버리스**(API Gateway + Lambda)였으나, 이번 회의에서 **provisioned + 쿠버네티스**로 변경 결정. 따라서 Straumann 연동도 별도 서버리스가 아니라 **통합 VatechAPIGateway**(K8s)를 경유한다("모든 연동은 GW" 원칙과 일관).
- **AWS 비종속 이유:** AWS 미지원 국가(§2.11)에서는 그 지역 GW도 AWS에 올릴 수 없으므로, GW는 **클라우드 비종속**(K8s)으로 설계해 AWS·비-AWS 어디든 동일하게 배포한다.

### 2.10 글로벌 라우팅 (가까운 GW로 연결)

- GW를 멀티 Region에 설치하고, **DNS가 접속자의 위치·지연에 따라 가장 가까운 GW Region을 반환**하도록 한다(단일 도메인, GeoDNS 최근접 라우팅).
- **글로벌 라우팅은 AWS Route 53로 확정**한다. Route 53의 latency-based / geolocation routing으로 가까운 GW Region에 연결한다.
- latency vs geolocation 선택, 헬스체크·페일오버 정책 등 세부 옵션은 상세 설계 단계에서 정한다.

### 2.11 AWS 미지원 국가 대응

- **AWS를 지원하지 않는 나라**는 CleverSpace 대신 **별도 서버로 구축**하고, **S3 대신 minio**를 사용한다.
- **구성은 표준과 동일**하게 보며, 차이는 **스토리지(S3 → minio) 교체뿐**이다. 대상국별 추가 구성 차이는 현재 없음. minio도 S3 호환이라 presigned URL 방식이 그대로 동작한다.
- 이 변형도 **전체 아키텍처에 포함**한다.

### 2.12 클라이언트 식별 — 제품명·버전 전달 표준 (확정)

- 요청 시 **제품명 + 제품 버전**(+OS)을 함께 전달한다.
- 현황(기존 소스 분석): CleverOne은 **UserAgent에 제품명만**(`"CleverOne"`, 버전 없음) 싣고, EzServer→CleverSpace는 **client 버전 미전달**.
- **결정: 구조화된 전용 헤더(권위 소스) + User-Agent 표준화(병행).** 둘 중 택일이 아니라 역할을 나눈다.
  - **머신 판정**(버전 게이트·Region 라우팅·validate-limits)은 **전용 헤더**로 한다. UserAgent 파싱은 제품마다 포맷이 다르고 중간 경로에서 변형·가공될 수 있어 취약하므로, GW·CleverSpace가 판정에 쓰는 **권위 소스는 전용 헤더**다.
  - **User-Agent는 표준 포맷으로 유지**한다. 어디서나 로깅되어 관측·디버깅에 유용하고 기존 코드가 이미 세팅하므로 하위호환에도 이롭다. 버리지 않는다.

전용 헤더(벤더 프리픽스 `Vatech-`, RFC 6648에 따라 `X-` 미사용):

```
Vatech-Product:   CleverOne          # 제품명
Vatech-Version:   1.5.5              # 제품 버전(semver)
Vatech-OS:        Windows/11         # OS명/버전
Vatech-Clinic-Id: <ClinicID>         # GW Region 라우팅 키(§2.6)

User-Agent: CleverOne/1.5.5 (Windows 11; x64)   # 병행(로그·관측·하위호환)
```

> 프리픽스는 **제품 브랜드**인 `Vatech-`를 쓴다(회사는 Ewoosoft지만 외부 식별자는 Vatech가 일관). `X-` 접두는 RFC 6648에서 비권장되므로 붙이지 않는다(`X-Vatech-Product` 아님).

- **ClinicID를 같은 헤더 체계에 포함** → §2.6 Region 분배와 한 번에 해결.
- **GW가 단일 집행점**: EZ/CleverOne이 헤더를 싣고 GW가 읽어 라우팅·호환성·한도 판정 후 다운스트림에 정규화 전달. 경로 A에서 EZ는 **originating client 식별**도 함께 전달.
- **외부(Straumann 등)로는 내부 헤더를 보내지 않는다** — EZ↔GW↔CleverSpace 내부 식별용.
- 적용 지점(기존 소스): CleverOne `CleverOneInitializer.cpp`·`EzCloudController.cpp`, ESLinkageCloudPlatform `EzCloudLinker.cpp`·`OneIdLinker.cpp`(`strAgent` 확장), EzServer(EPI) 대리 전달.

---

## 3. Roadmap 작성 요구사항

- 단계 구성: **기간이 아니라 기능 응집도**로 나눈다. 6개월은 목표 기한일 뿐, 단계는 "딱 떨어지는 기능 묶음" 기준으로 구성한다.
- **추천: 3단계**(아래). EzServer 전면 재개발은 이 3단계에 **포함하지 않고** 별도 후속 트랙으로 둔다.
- 각 단계 산출물을 **제품별로 모두** 명시: **CleverOne / EzServer(EZ) / CleverSpace / OneID / VatechAPIGateway(+GW Console) / (Straumann AXS 연동)**.
- **표 + 시각화 다이어그램** 병행.
- **단계별 전체 아키텍처 다이어그램(mermaid)**: 각 단계마다 **그 시점의 전체 구조 다이어그램**을 보여주어, 단계가 진행되며 아키텍처가 **어떻게 바뀌는지** 한눈에 비교되도록 한다. 그 단계에서 **새로 추가/변경되는 요소를 색·강조로 구분**하고, 직전 단계 대비 **무엇이 달라졌는지**를 곁들인다(AS-IS → 단계1 → 단계2 → 단계3).
- **Straumann 진입 시점 = "가능한 가장 이른 시점"**: 최소 **GW가 나와야** 하며, 실질 선행 요건은 **GW + 인증(OneID) + presigned URL + Org-ID 매핑**이다. 따라서 2단계(데이터 경로) 완료 시점부터 **착수 가능**하며, 3단계와 **병렬 트랙**으로 진행할 수 있다. Roadmap에는 "가능 시점"으로 표기한다.
- **EzServer 전면 재개발(PHP → Rust)**: 위 3단계에서 **제외**한다. 3단계(VatechAPIGateway 완성) **이후의 별도 후속 트랙**으로 두고 설명은 간략히만. 핵심 의사결정(기존 API 포팅 vs API 재설계)은 §5의 **장기 숙제**로 남긴다.

### 3.0 단계 수 추천 — 3단계 (기능 응집 기준)

| 단계 | 기능 묶음(응집) | 핵심 산출물 | 의미 |
|------|-----------------|-------------|------|
| **1단계 — GW 기반 + 통합 식별·호환** | 제어/API 경로 | VatechAPIGateway 본체(모든 연동 EZ→GW 단일 경유), OneID 인증 Verify 연계, 기존 EZ→CleverSpace를 GW 경유로 전환, **Vatech-* 식별 헤더 표준**, validate-limits 사전검증·오류코드 매핑·호환성 매트릭스(GW 집행) | GW가 단일 경유점이 되고 **API 버전 호환 문제 해결**. (단일 Region에서 시작) |
| **2단계 — presigned 데이터 경로** | 데이터 경로 | CleverSpace **presigned URL 발급 신규 개발**(현재 Direct), EZ **전송 로직 변경**(presigned 직접 업로드), GW 경유 발급 흐름 | 대용량 데이터(CT·이미지) 경로 완성. **여기까지면 Straumann 착수 가능** |
| **3단계 — 멀티 Region·글로벌·운영** | 멀티리전/운영 | CleverSpace 멀티 Region, GW **Region 분배**(ClinicID↔Region 매핑·Postgres), **Route 53 GeoDNS** 최근접 라우팅, CleverOne **Region 선택 UI**, **GW HA(K8s, 서울·미주)**, **GW Console**, 비-AWS(minio) 변형 | **VatechAPIGateway 완성**(멀티리전·HA·관리) |
| (후속) EzServer 전면 재개발 | 별도 트랙 | PHP → Rust 전면 교체 | 3단계 이후 장기 과제(§5 숙제) |

> 3단계를 추천하는 이유: **(1) 제어·API 경로 → (2) 데이터 경로 → (3) 멀티리전·운영**이 서로 **의존 순서가 뚜렷하고 기능적으로 깔끔히 분리**된다. 1·2를 합치면 API 경로와 데이터 경로가 섞여 범위가 커지고, 3을 더 쪼개면(라우팅/HA/콘솔) 모두 "멀티리전 운영"이라는 한 묶음이라 인위적 분할이 된다. Straumann은 별도 단계가 아니라 **2단계 이후 병렬 트랙**으로 본다.

### 3.1 단계 배치 시 고려할 개발 항목(초안 — 보고서에서 확정)

| 영역 | 개발 항목(후보) |
|------|-----------------|
| VatechAPIGateway | GW 본체(모든 연동 단일 경유), 인증(OneID Verify) 연계, 라우팅/스로틀링 |
| GW — Region 분배 | ClinicID 기반 Region 매핑 테이블, 요청 분기 로직 |
| GW Console | Admin용 Web client(매핑·클리닉·상태 관리) |
| GW — 글로벌 라우팅 | IP 기반 가까운 GW 연결(CloudFlare/CloudFront 검토 결과 반영) |
| GW — HA | Kubernetes HA, 멀티 리전(서울·미주) |
| CleverSpace | presigned URL 발급 방식 신규 개발(현재 Direct 전송), 멀티 Region 구축 |
| EzServer(EZ) | GW 경유 전송 로직, presigned URL 직접 업로드, ClinicID 포함, 제품·버전 헤더 |
| CleverOne | Region 선택 UI, 제품·버전 헤더, (호환성) capability 인지 |
| OneID | GW 연계 인증 Verify |
| 비-AWS 국가 | 별도 서버 + minio(S3 대체) 구성 |
| Straumann(AXS) | GW를 통한 AXS 연동(Org-ID 매핑·온보딩·Pre-signed URL) — 선행 단계 충족 후 |

---

## 4. 새 보고서 입력 자료

- [`API호환성_방안비교_보고서.md`](API호환성_방안비교_보고서.md) — 호환성 방안(기본 아키텍처 동의).
- [`../Straumann연동/Straumann-Vatech_AXS연동_분석보고서.md`](../Straumann연동/Straumann-Vatech_AXS연동_분석보고서.md) — AXS 연동/Auth·API Gateway/Pre-signed URL/Org-ID 매핑(기본 아키텍처 동의).
- `0604-1.png`, `0604-2.png` — 회의 중 화이트보드 아키텍처(판독 어려움, 본 회의록 설명으로 대체).

---

## 5. 미결·검토 필요 항목 (보고서 작성 전 확정/조사)

| No. | 항목 | 내용 | 비고 |
|-----|------|------|------|
| 1 | EzServer Rust 재개발 방식 | PHP → Rust 전면 교체 시 **기존 API 그대로 포팅** vs **API부터 재설계** — **여기서 결정하지 않고 최종 보고서에도 장기 숙제로 계속 남긴다.** 최종 단계 이후 후속 단계로 배치. (EzServer가 Edge로 남는 것 자체는 확정) | 장기 숙제(미정) |
| 5 | presigned URL 흐름 | GW 경유 발급의 구체 시퀀스(EZ→GW→CleverSpace), CleverSpace 신규 개발 범위 | 설계 필요 |
| 6 | 비-AWS 국가 대응 | **현재는 표준 구성과 동일하게 본다** — 차이는 S3 → minio 교체뿐(별도 서버). 대상국별 추가 구성 차이는 없음 | 정리됨 |
| 7 | 매핑 테이블 스키마 | ClinicID↔Region, ClinicID↔Org-ID 외 추가 필드(Straumann 연구 참고) | 항목 정리 |
| 7-1 | GW 컨트롤플레인 저장소 | 매핑/등록 데이터 저장소 선정. DynamoDB는 AWS 전용이라 비-AWS 불가 → **PostgreSQL 등 이식성 DB + GW 메모리 캐시** 방향 검토 | 설계 결정 |
| 8 | Region 수/위치 | 초기 서울·미주 2개 외 확장 계획, CleverSpace 멀티 Region 구축 범위 | 확인 |
| 9 | Straumann 진입 단계 | **결정: 2단계(데이터 경로) 이후 착수 "가능"**, 3단계와 병렬 트랙. 선행 요건 = GW + 인증 + presigned + Org-ID 매핑 | 정리됨 |

---

## 6. 리뷰 포인트

- 위 §1~3의 결정/요구가 회의 의도와 일치하는지.
- **단계 수: 3단계로 확정**(§3.0), EzServer 재개발은 후속 트랙으로 제외.
- **Straumann: 2단계 이후 '가능 시점'으로 배치**(3단계와 병렬).
- §5에 남은 항목은 보고서에서 제안·분석으로 소화(별도 사전 결정 불필요).
