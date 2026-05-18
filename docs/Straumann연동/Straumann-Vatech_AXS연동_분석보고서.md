# Straumann-Vatech AXS 연동 요구사항 종합 분석

## 1. 양사 배경

| 항목 | Straumann | Vatech |
|------|-----------|--------|
| 매출 | CHF 26억 (2025) | 치과 영상장비 전문 |
| 시장 지위 | 글로벌 임플란트 시장 점유율 ~35%, 1위 | 3D 치과 영상장비 글로벌 판매 1위 |
| 핵심 사업 | 임플란트 + 디지털 생태계(AXS 플랫폼) | 영상장비(CBCT, 2D) + SW(EzDent-i, Clever One) |
| 전략 방향 | AXS를 중심으로 디지털 워크플로우 플랫폼화 | EzServer(On-premise) 기반 데이터 허브 + Clever Lab/Space(AWS) 클라우드 확장, 향후 Clever Orbit(클라우드 기반 EzServer) 예정 |

Straumann은 AXS 플랫폼을 단순 API가 아니라 **디지털 치과 생태계의 허브**로 포지셔닝하고 있다. 모든 제3자(스캐너, 영상장비, 랩)를 AXS로 연결시켜 **플랫폼 종속성**을 만드는 것이 핵심 전략이다.

---

## 2. Straumann 측 요구사항 정리

Straumann의 핵심 요구:

### A. 아키텍처 요구: Vatech Auth Server 구축 필수

- On-premise 디바이스(EzServer)가 AXS API에 **직접 연결하는 것을 불허**
- Vatech이 자체 **클라우드 기반 Auth Server(또는 API Gateway)**를 개발/운영해야 함
- Auth Server가 `client_id`/`client_secret`을 보관하고 AXS API 토큰 발급을 중계
- Desktop 앱은 민감한 자격증명에 접근 불가

### B. 인증 요구: OAuth 2.0 기반

- Auth Server가 AXS에서 토큰을 발급받아 on-premise 디바이스에 전달
- 토큰 유효기간 30분, Auth Server에서 주기적 갱신
- Auth Server 미운영 시 90일마다 재연결 필요
- `client_id`는 최소 연 1회 변경 → Auth Server 없으면 모든 디바이스 개별 업데이트 필요

### C. 파일 업로드: 3단계 프로세스

1. EzServer → Auth Server 경유 → AXS API `Create Document` 호출
2. AXS가 Pre-signed URL(S3) 반환
3. On-premise 디바이스가 해당 URL로 직접 업로드 (Auth Server 미경유)

### D. 클리닉 온보딩: 일회성 동의 프로세스

- Customer Number 입력 → Access 포털에서 승인 → Organization ID 생성
- 클리닉이 언제든 권한 철회 가능

### E. 데이터 흐름: 단방향만 지원

- EzServer → AXS 단방향 전송만 기본 지원
- AXS → EzServer 역방향은 Webhook으로 가능하나 별도 논의 필요
- 단, Webhook은 현재 논의 범위에서 **당장 필수가 아님** — 아래 상세 분석 참조

### F. Webhook 필요성 분석

Straumann 측이 언급한 Webhook(AXS→EzServer 방향)의 실질적 필요성:

| 시나리오 | 설명 | 필요도 | 대체 수단 |
|---------|------|--------|----------|
| 랩 오더 상태 변경 | 오더 상태(접수→진행중→완료) 알림 | 낮음 | AXS 웹 포털에서 직접 확인 |
| 기공물 확인 요청 | Clever Lab 디자인 완료 후 치과에 확인 요청 | 낮음 | AXS 웹/이메일 알림 |
| 치료 계획 회신 | CodiagnostiX 임플란트 계획을 EzServer로 전달 | 중간 | 현재 단방향만 논의 중이므로 1차 범위 밖 |
| 환자 데이터 동기화 | AXS 변경사항을 EzServer에 반영 | 낮음 | 회의록에서 양방향 Sync 미지원 명시 |

현재 논의 범위(EzServer→AXS 단방향)에서는 Webhook이 필수가 아니며, 클리닉 사용자가 AXS 웹 포털에서 직접 상태를 확인하는 방식으로 대체 가능하다.

**Webhook 구축 시 추가 비용 이슈**: Webhook 수신 자체는 AWS API Gateway로 간단하지만, 수신한 데이터를 **각 치과의 On-premise EzServer까지 전달하는 것이 실질적 과제**다. EzServer는 방화벽 뒤에 있어 외부에서 직접 Push가 불가능하므로, EzServer 측 Polling 또는 WebSocket 연결 유지 등 별도 메커니즘이 필요하다. 이는 EzServer 클라이언트 측 개발, 네트워크 환경별 테스트, 장애 대응 등 **상당한 추가 개발/운영 비용**을 수반한다. Clever Orbit(클라우드 기반 EzServer)이 출시되면 자연스럽게 해소되는 문제이므로, Webhook 구현은 Clever Orbit 이후로 미루는 것이 합리적이다.

---

## 3. Vatech(ES) 원래 제안과 그 한계

4/2 바텍 제안 문서에서 확인되는 원래 구상:

- **EzServer가 AXS API와 직접 연동** (중간 계층 없이)
- EzServer → AXS 단방향 데이터 전송 (환자정보, 영상데이터, 케이스 정보)
- 기존에는 호주 법인을 통해 **EzServer-SIRIOS 직접 연동**까지 논의
- Vatech의 핵심 요구: **"우리 서버(EzServer)가 AXS와 직접 통신"**

> **참고**: EzServer는 순수 On-premise 서버로 각 치과에 개별 설치된다. 클라우드 호스팅 옵션은 없으며, 향후 Clever Orbit 서비스에서 클라우드 기반으로 전환 예정이다. 따라서 Straumann이 말하는 "On-premise 디바이스"는 정확히 EzServer를 지칭한다.

이것이 4/30 회의에서 Straumann에 의해 거부되었다.

**Straumann이 이 제안을 수용할 가능성은 없다.** EzServer 직접 연결은 보안 관점에서 근본적인 문제가 있기 때문이다:

- 각 치과에 설치된 수백~수천 대의 EzServer에 `client_id`/`client_secret`을 배포해야 함
- 한 대라도 탈취되면 전체 자격증명이 노출되는 구조적 위험
- 연 1회 자격증명 변경 시 모든 EzServer를 개별 업데이트해야 하는 관리 불가능 문제
- 각 치과의 서로 다른 public IP에서 환자 데이터가 송출되므로 GDPR/개인정보 컴플라이언스 대응 불가
- Straumann이 수천 개의 IP와 디바이스를 개별 관리할 수 없음

이는 Straumann의 이기심이 아니라 **보안 업계 표준에 부합하는 정당한 거부**이며, 바텍의 원래 제안이 On-premise 특성을 충분히 고려하지 못한 측면이 있다. 따라서 중간 계층(Auth Server/API Gateway) 구축 자체는 불가피한 방향이다.

---

## 4. Straumann이 이런 요구를 하는 이유

### 기술적 명분 (표면적 이유)

- On-premise 디바이스에 `client_secret` 저장은 보안 위험 (역공학, 탈취)
- 자격증명 갱신 시 전체 디바이스 업데이트 불필요
- Public Client에서 환자 정보가 Public IP에 노출되는 것을 차단

### 실질적 이유 (전략적 의도)

| 이유 | 설명 |
|------|------|
| **Whitelist 기반 통제** | AXS 팀이 애플리케이션을 심사 후 whitelist에 등록해야 접근 가능. Straumann은 "누가 연결하는지"를 완전히 통제 |
| **보안 책임 전가** | Auth Server를 Vatech이 구축/운영하면, 보안 사고 시 책임이 Vatech에 귀속. Straumann은 "우리 정책대로 했다"고 면책 가능 |
| **운영 부담 집중** | 토큰 갱신, 자격증명 관리, 서버 가용성, 장애 대응 등 운영 부담이 모두 Vatech에 집중. 단, AWS 서버리스 채택 시 운영 부담은 대폭 경감 가능 |
| **플랫폼 종속 강화** | 모든 데이터가 AXS를 경유하게 되면 Vatech 고객이 자연스럽게 Straumann 생태계에 편입 |
| **표준화된 패턴 적용** | 모든 제3자에게 동일한 아키텍처를 요구하여 관리 복잡도를 낮춤 (Vatech만의 특별 대우 불가) |

---

## 5. 이 요구의 문제점 및 Vatech에 불리한 점

### 기술적 문제

| 항목 | 문제 |
|------|------|
| **추가 인프라** | Auth Server(사실상 API Gateway)는 기존 개발 계획에 없던 것. 설계/개발/운영 전체가 추가 비용 |
| **단일 장애점(SPOF)** | Auth Server 장애 시 모든 클리닉의 AXS 연동이 중단. 고가용성(HA) 구축 필수 |
| **지속적 운영 부담** | 토큰 갱신(30분 주기), 자격증명 로테이션(연 1회), 모니터링, 보안 패치 등 영구적 운영 비용 |
| **아키텍처 복잡도** | EzServer → Auth Server → AXS → Pre-signed URL → 직접 업로드 등 홉이 많아져 장애 포인트 증가 |
| **양방향 동기화 어려움** | Webhook 수신을 위해 Auth Server가 public endpoint를 노출해야 하는데, 추가 보안 고려 필요 |

### 사업적 불리함

| 항목 | 불리한 점 |
|------|----------|
| **비대칭 투자** | Straumann은 기존 API 제공만 하면 되고, VT/ES가 API Gateway + 연동 로직 전체를 개발/운영. 비용은 VT 부담, 개발은 ES 수행 |
| **종속성 심화** | AXS 정책이 바뀌면(API 버전업, 인증방식 변경 등) Vatech이 따라가야 함 |
| **데이터 주도권 상실** | 모든 환자 데이터가 AXS를 경유하므로, 장기적으로 Straumann이 데이터 주도권을 가짐 |
| **협상 레버리지 약화** | Auth Server를 구축하면 매몰 비용이 발생해 향후 협상에서 더 불리해짐 |
| **고객 인식** | 클리닉 입장에서는 Vatech 장비가 Straumann 생태계의 "주변기기"처럼 인식될 수 있음 |

---

## 6. 이 요구가 무리한가, 합리적인가?

### 합리적인 측면

- OAuth 2.0 Client Credentials + Backend Server 패턴은 **업계 표준**. AWS, Google Cloud, Microsoft 등 대부분의 클라우드 API가 on-premise 연동 시 유사한 구조를 요구
- On-premise 디바이스에 secret을 저장하지 않는 것은 **보안 관점에서 정당한 원칙**
- Pre-signed URL 업로드도 대용량 파일 처리의 **표준적 접근**
- Straumann이 Vatech에만 이런 요구를 하는 것이 아니라, 모든 제3자에게 동일한 정책을 적용할 가능성이 높음

### 무리한 측면

- 기존 계획에 없던 인프라를 추가로 요구하면서 **구체적인 기술 지원 방안(스펙, 가이드, 테스트 환경)이 없음**
- **단방향만 기본 지원**하면서 양방향 연동(AXS→EzServer)은 별도 논의로 미룸 → Vatech 고객에게 주는 실질적 가치가 제한적
- Clever Space(AWS 기반)가 이미 존재하지만, Auth Server 역할을 위해서는 별도의 인증/토큰 관리 모듈을 신규 개발해야 하므로 기존 인프라 활용 이점이 크지 않음
- **Auth Server 구축에 필요한 기술 문서가 부재** — 아래 상세 참조

### Auth Server 구축 가이드 부재 문제

Straumann은 Auth Server 구축을 필수 요구하면서, 정작 구축에 필요한 핵심 정보를 제공하지 않고 있다.

| 필요한 정보 | 제공 여부 |
|------------|----------|
| OAuth 토큰 발급 엔드포인트 (token URL) | 공개 문서에 없음 |
| Client Credentials Flow 파라미터 (grant_type, scope 등) | 미공개 |
| Auth Server ↔ AXS API 인터페이스 스펙 | 미제공 |
| 테스트/샌드박스 환경 | 제공 여부 불명 |
| Auth Server 보안 요건 (TLS 버전, IP whitelist 등) | 미공개 |
| SDK / 샘플 코드 | 없음 |
| Developer Portal 접근 | whitelist 등록 클라이언트만 가능 (403 Forbidden) |

즉, "Auth Server를 만들어라"라고 요구하면서 **어떻게 만들어야 하는지 알려주지 않는 상황**이다. 이는 Straumann 측에 기술 문서 및 개발 지원을 요청해야 하는 강력한 근거가 된다.

---

## 7. 사업적 역학: 양쪽 모두에게 가치가 있는 연동

Straumann이 "갑"의 위치에서 이런 제안을 하는 것은 맞지만, 양쪽 모두에게 가치가 있는 연동이다.

| Straumann 이득 | Vatech 이득 |
|---------------|------------|
| Vatech 장비 사용 클리닉이 AXS 생태계에 편입 → 사용자 기반 확대 | Straumann 사용 클리닉에 Vatech 장비 판매 기회 확대 |
| CBCT/2D 영상 데이터가 AXS로 유입 → 플랫폼 가치 증가 | Clever Lab-AXS 연동 시 기공소 워크플로우 차별화 |
| 경쟁 영상장비 대비 Vatech과의 독점적 연동 확보 가능 | Straumann의 글로벌 네트워크 활용 가능 |

CBCT 영상은 Straumann이 직접 제공하지 못하는 핵심 데이터이므로, Vatech의 협상 카드가 없는 것은 아니다.

---

## 8. 결론: 협상 구도와 현실적 판단

### EzServer 직접 연결은 불가능 → 중간 계층 구축은 불가피

3장에서 분석한 바와 같이 EzServer 직접 연결은 보안상 수용 불가하므로, API Gateway(Auth Server) 구축 자체는 피할 수 없다. 쟁점은 **"구축 여부"가 아니라 "구축 조건"**이다.

### Straumann이 부담하는 것과 Vatech이 부담하는 것

| 주체 | 부담 항목 | 비고 |
|------|----------|------|
| **Straumann** | AXS API 스펙 제공 (OAuth 엔드포인트, API 명세, 파라미터) | 거부 불가 — 연동하려면 반드시 제공해야 함 |
| | `client_id`/`client_secret` 발급 | 거부 불가 — 표준 등록 절차 |
| | Developer Portal 접근 권한 | 거부 불가 — 등록 후 기본 제공 |
| | 테스트/샌드박스 환경 | 거부 가능성 낮음 — API 제공자의 일반적 의무 |
| | 연동 과정 기술 문의 대응 | 최소한은 제공할 것 |
| **VT(Vatech)** | 개발/운영비 부담 | 장비 판매 이익의 수혜자로서 비용 부담 주체 |
| **ES(Ewoosoft)** | API Gateway 인프라 구축/운영 | SW 개발 자회사로서 실제 개발 수행 |
| | 연동 로직 개발 (Lambda 함수) | Straumann 스펙 기반으로 개발 |

개발은 ES가 수행하고, 비용은 VT가 부담한다. ES는 VT의 SW 개발 자회사이지만 재무는 별개이므로, VT가 비용을 책정/승인해야 ES가 착수할 수 있다. AWS 서버리스 아키텍처를 채택하면 운영 비용 자체도 월 $15~50 수준으로 부담이 크지 않다. Straumann에는 비용 분담이 아닌 **스펙/테스트 환경의 신속한 제공**을 요구하는 것이 실질적이다.

Straumann 입장에서도 Vatech이 자비로 API Gateway를 구축하므로 **반대할 이유가 전혀 없다**.

**핵심 전제 조건은 하나**: Straumann이 API 스펙과 인터페이스를 제공하는 것. 이것만 확보되면 나머지는 Vatech이 독립적으로 진행 가능하며, Vatech이 구축 의사를 밝히면 Straumann은 스펙을 제공할 수밖에 없다 — 그것이 그들이 원하는 구조이기 때문이다.

### Vatech의 방향: AWS API Gateway로 자체 구축

Straumann에 Auth Server 구축을 요청하는 것은 비현실적이다. Straumann이 제안한 구조 자체가 "Vatech이 만들어라"는 것이고, 그들이 대신 만들어줄 이유가 없다. 따라서 **Vatech이 AWS API Gateway 기반으로 직접 구축하는 것이 유일한 현실적 방향**이다.

단, 구축을 시작하려면 Straumann으로부터 반드시 받아야 하는 것들이 있다:

### Straumann에 요청해야 할 항목

| No. | 요청 항목 | 설명 | 없으면 개발 불가 |
|-----|----------|------|:---:|
| 1 | **Developer Portal 접근 권한** | 현재 403 Forbidden 상태. 등록/whitelist 승인 필요 | O |
| 2 | **OAuth 인증 스펙** | 토큰 엔드포인트 URL, Client Credentials Flow 파라미터(grant_type, scope 등), 토큰 응답 형식 | O |
| 3 | **AXS API 엔드포인트 명세** | 환자 생성/조회, 문서 업로드(Create Document), 케이스, 오더 등 전체 API 스펙 | O |
| 4 | **`client_id`/`client_secret` 발급** | 애플리케이션 등록 후 자격증명 발급 | O |
| 5 | **테스트/샌드박스 환경** | 실제 환자 데이터 없이 개발 중 검증 가능한 환경 | O |
| 6 | **IP whitelist 정책** | NAT Gateway 고정 IP를 사전 등록해야 하는지 여부 | O |
| 7 | **파일 업로드 스펙 상세** | Pre-signed URL 방식이 확정인지(회의에서는 "예: S3 URL"로 예시 수준 언급), 업로드 방식(단일 PUT/Multipart), URL 유효 시간, 파일 크기 제한, 업로드 완료 후 callback API 유무 등 | O |
| 8 | **Organization-ID 관리 정책** | 유실 시 Access 포털에서 재확인/재발급 가능 여부, 1개 클리닉에 복수 ID 가능 여부, 철회 후 재등록 시 동일 ID인지 여부 | O |
| 9 | **API Gateway 구축 가이드** (있다면) | Straumann이 제3자 연동을 위해 이미 가이드를 보유하고 있을 수 있음. 있다면 개발 기간을 더 단축할 수 있음 | - |
| 10 | **SDK / 샘플 코드** (있다면) | OAuth 인증, API 호출 예시 등. 있으면 도움이 되지만 없어도 스펙만 있으면 개발 가능 | - |

1~8번은 **없으면 개발을 시작할 수 없는 필수 항목**이다. 9~10번은 있으면 좋지만 없어도 진행 가능하다.

### 진행 단계

| 단계 | 내용 | 주체 | 선행 조건 |
|------|------|------|----------|
| **0. 호주 법인 논의 결과 확인** | 4/30 회의록 Action Item(5/15 기한)의 Straumann 재논의 결과를 호주 법인에 확인 | 호주 법인/ES | - |
| **1. 투자 판단** | 호주 시장에서의 사업적 가치(장비 판매 기여도) 대비 개발/운영 비용(ES 개발 인력, AWS 월 $15~50)을 정량적으로 평가하여 진행 여부 결정 | VT 경영진 | 0단계 완료 |
| **2. 구축 의사 전달** | Vatech → Straumann: "API Gateway 방식으로 구축하겠다. 위 1~6번 항목을 제공해달라" | 호주 법인/ES | 1단계에서 진행 결정 |
| **3. 스펙/환경 수령** | Straumann → Vatech: Portal 접근, OAuth 스펙, API 명세, 샌드박스, 자격증명 제공 | Straumann | 2단계 완료 |
| **4. AWS 인프라 구성** | API Gateway, Lambda, Secrets Manager, DynamoDB, NAT Gateway 프로비저닝 | ES | 3단계와 병행 가능 |
| **5. Lambda 개발** | 토큰 관리, 환자 동기화, 문서 업로드 등 Lambda 함수 개발 | ES | 3단계 완료 필수 |
| **6. 테스트** | 샌드박스 환경에서 E2E 검증 | ES | 4~5단계 완료 |
| **7. 운영 배포** | 프로덕션 전환 | ES | 6단계 완료 |

> **참고**: 0단계 — 4/30 회의록에서 호주 법인이 5/15까지 Straumann과 재논의 후 ES에 공유하기로 했으나, 현재 공유 여부 미확인. 진행 전 호주 법인 담당자에게 확인 필요.

### 기타 협상 시 요구 사항

| No. | 제안 | 근거 |
|-----|------|------|
| 1 | **Clever Orbit 출시와 연계한 단계적 접근** | Phase 1: API Gateway 최소 구현으로 EzServer→AXS 단방향 연동, Phase 2: Clever Orbit 출시 시 클라우드 간 직접 연동 + Webhook 수신으로 확장 |
| 2 | **데이터 소유권/활용 범위 명문화** | AXS에 업로드된 Vatech 장비 데이터의 소유권, 활용 범위, 삭제 권한 등을 계약서에 명시 |
| 3 | **비즈니스 우선순위 재평가** | 현재 호주 시장 장비 판매 지원 목적이므로, VT가 부담할 구축 비용 대비 실질 매출 효과를 정량적으로 검토 후 진행 여부 결정 |

---

## 9. 구현 방식 비교: 자체 Auth Server vs AWS API Gateway

Straumann이 요구하는 "Vatech Auth Server"를 구현하는 방식은 크게 두 가지다. 어느 방식이든 Straumann의 보안 요구(secret 미노출, 신뢰할 수 있는 Backend, 중앙 자격증명 관리)를 **동일하게 충족**한다. 차이는 Vatech 측의 개발/운영 부담이다.

### 두 방식의 아키텍처 비교

**방식 A: 자체 Auth Server 구축**

```
EzServer(각 치과) ──→ [Vatech Auth Server (EC2/ECS)] ──→ AXS API
                           │
                     자체 DB/KMS
                  (secret 보관, 토큰 캐싱)
```

- 서버 애플리케이션을 직접 개발 (Node.js, Java 등)
- EC2 또는 ECS 위에 배포
- 가용성(HA)을 위해 Multi-AZ, 로드밸런서, 오토스케일링 직접 구성
- DB(RDS 또는 자체)에서 secret 보관, 토큰 캐싱 직접 구현
- 24/7 서버 모니터링, 패치, 장애 대응 필요

**방식 B: AWS API Gateway + 서버리스 (권장)**

```
EzServer(각 치과) ──→ [AWS API Gateway] ──→ [Lambda] ──→ AXS API
                                               │
                                    Secrets Manager + DynamoDB
```

- Lambda 함수 수 개만 개발
- 인프라 프로비저닝/관리 불필요
- HA, 스케일링, 모니터링은 AWS가 기본 제공

### 항목별 상세 비교

#### 개발 비용

| 항목 | 자체 Auth Server | AWS API Gateway |
|------|-----------------|-----------------|
| 서버 애플리케이션 | 프레임워크 선정, API 라우팅, 에러 핸들링, 로깅 등 풀스택 개발 | 불필요 (API Gateway가 처리) |
| 인증/토큰 관리 | OAuth Client Credentials Flow 직접 구현, 토큰 캐싱 로직, 갱신 스케줄러 개발 | Lambda 함수 1개 (`token-manager`) |
| AXS API 중계 로직 | 각 엔드포인트별 프록시/변환 로직 직접 구현 | Lambda 함수 수 개 (엔드포인트별) |
| Secret 저장 | 암호화 저장소 설계/구현 (KMS 연동 또는 자체) | Secrets Manager API 호출 1줄 |
| HTTPS/TLS | 인증서 발급/갱신 관리 | API Gateway 기본 제공 |
| **예상 개발 기간** | **2~3개월** (서버 + 인프라 + 테스트) | **2~4주** (Lambda 함수 + 인프라 구성) |

#### 운영 비용

| 항목 | 자체 Auth Server | AWS API Gateway |
|------|-----------------|-----------------|
| 서버 비용 | EC2 최소 2대 (HA) × 24/7 상시 가동 → **월 $150~300+** | 요청 기반 종량제 → 트래픽 적으면 **월 $10 미만** |
| DB 비용 | RDS 또는 ElastiCache 상시 운영 → **월 $30~100+** | DynamoDB 온디맨드 → **월 $1 미만** |
| Secret 관리 | 자체 구현 유지보수 | Secrets Manager **월 $0.40** |
| 모니터링 | 별도 도구 도입 또는 자체 구축 | CloudWatch 기본 포함 |
| **월 예상 총비용** | **$200~500+** | **$15~50** (NAT Gateway 포함) |

#### 가용성(HA) / 장애 대응

| 항목 | 자체 Auth Server | AWS API Gateway |
|------|-----------------|-----------------|
| HA 구성 | Multi-AZ 배포, ALB, 오토스케일링 **직접 설계/구성** | AWS 기본 제공 (**99.95% SLA**) |
| 장애 발생 시 | 서버 장애 → 전체 클리닉 AXS 연동 중단. 운영팀이 직접 복구 | AWS 인프라 레벨에서 자동 복구. Lambda는 요청별 독립 실행 |
| 단일 장애점(SPOF) | EC2 인스턴스, DB 등 자체 관리 컴포넌트마다 SPOF 위험 | **SPOF 없음** — 모든 구성요소가 관리형/서버리스 |
| 패치/업데이트 | OS, 런타임, 라이브러리 패치를 운영팀이 직접 수행 | AWS가 인프라 패치 자동 처리 |
| 스케일링 | 트래픽 증가 시 수동 또는 오토스케일링 설정 필요 | Lambda 자동 스케일링 (동시 1,000건까지 기본) |

#### 보안

| 항목 | 자체 Auth Server | AWS API Gateway |
|------|-----------------|-----------------|
| Secret 보관 | 자체 암호화 설계 필요. 구현 실수 시 노출 위험 | Secrets Manager (AWS KMS 기반 암호화, 자동 로테이션) |
| 네트워크 보안 | 보안그룹, WAF 등 직접 구성 | API Gateway 기본 DDoS 방어, WAF 선택 적용 |
| 감사/로깅 | 직접 구현 | CloudTrail + CloudWatch 자동 기록 |
| IP 고정 (Straumann whitelist) | Elastic IP 직접 할당 | NAT Gateway로 고정 IP 확보 |

두 방식 모두 Straumann의 보안 요구를 충족하지만, 자체 구축은 보안 설계를 직접 해야 하므로 **구현 실수에 의한 보안 사고 위험**이 추가된다.

#### 유지보수 / 장기 운영

| 항목 | 자체 Auth Server | AWS API Gateway |
|------|-----------------|-----------------|
| AXS API 변경 대응 | 서버 코드 수정 → 빌드 → 배포 파이프라인 필요 | Lambda 함수 수정 → 즉시 배포 |
| 자격증명 로테이션 (연 1회) | 자체 로직으로 갱신, DB 업데이트, 서버 재시작 등 | Secrets Manager에서 값만 변경 (서버 재시작 불필요) |
| 운영 인력 | **전담 인력 필요** — 서버 모니터링, 장애 대응, 패치 | **전담 인력 불필요** — CloudWatch 알람으로 이상 시에만 대응 |
| Clever Orbit 전환 시 | 서버 아키텍처 재설계 가능성 | Lambda 함수 로직만 조정 (인프라 변경 없음) |

### Straumann 요구 충족 여부 비교

**두 방식 모두 Straumann의 모든 요구를 동일하게 충족한다:**

| Straumann 요구 | 자체 Auth Server | AWS API Gateway |
|---------------|-----------------|-----------------|
| On-premise에 secret 미저장 | O | O |
| 신뢰할 수 있는 Backend 경유 | O | O |
| 자격증명 중앙 관리 | O | O |
| 토큰 발급/갱신 중계 | O | O |
| Whitelist 가능한 고정 접점 | O (Elastic IP) | O (NAT Gateway IP) |

Straumann 입장에서는 두 방식의 차이가 없다. **차이는 전적으로 Vatech 내부의 개발/운영 효율성에 있다.**

### "단기 Auth Server → 중장기 API Gateway" 단계론은 불필요

4/30 회의록에서 "단기적으로는 Auth Server, 중장기적으로는 API Gateway 방식이 적합"이라는 의견이 있었다. 이는 **자체 구축을 전제로** 했을 때의 논리로, 자체 Auth Server는 빨리 만들 수 있지만 확장성이 없고, 자체 API Gateway는 범용적이지만 설계/개발에 시간이 더 걸린다는 판단이었다.

그러나 AWS API Gateway는 관리형 서비스로 이미 완성된 인프라이므로, 별도의 Auth Server를 먼저 만들고 나중에 전환할 이유가 없다. **처음부터 API Gateway 방식으로 구축해도 자체 Auth Server보다 개발 기간이 오히려 짧다.** 2단계로 나눠서 두 번 개발하는 것보다, 처음부터 AWS API Gateway로 한 번에 구축하는 것이 비용과 일정 모두에서 합리적이다.

### 결론: AWS API Gateway 방식 권장 이유

1. **개발 기간 대폭 단축**: 2~3개월 → 2~4주. Lambda 함수 수 개만 작성하면 됨
2. **HA 고민 해소**: AWS 기본 SLA 99.95%. 자체 이중화 구성 불필요
3. **운영 비용 1/10 이하**: 월 $200~500 → 월 $15~50 수준
4. **전담 운영 인력 불필요**: 서버 모니터링/패치/장애 대응을 AWS가 대행
5. **보안 사고 위험 감소**: 자격증명 관리를 Secrets Manager에 위임, 구현 실수 여지 제거
6. **향후 확장 용이**: Clever Orbit 전환, Webhook 추가 등에 인프라 변경 없이 Lambda만 추가

### AWS API Gateway 방식 상세 설계

#### 아키텍처

```
EzServer(각 치과) ──HTTPS──→ AWS API Gateway ──→ Lambda ──→ AXS API
                                                    │
                                                    ├──→ Secrets Manager (client_id/secret 보관)
                                                    └──→ DynamoDB (토큰 캐싱, TTL 30분)
```

#### 필요 AWS 구성요소

| 구성요소 | 역할 | Straumann 요구 충족 |
|---------|------|-------------------|
| **API Gateway** | EzServer 요청의 HTTPS 진입점, 요청 라우팅/스로틀링 | Public Client에 secret 미노출 |
| **Lambda** | OAuth 토큰 발급/갱신, AXS API 호출 중계 | 신뢰할 수 있는 Backend 역할 |
| **Secrets Manager** | `client_id`/`client_secret` 보관, 자동 로테이션 | 자격증명 중앙 관리, 연 1회 변경 대응 |
| **DynamoDB** | 발급받은 AXS 토큰 캐싱 (TTL 30분) | 서버리스, Lambda 간 캐시 공유, 저비용 |
| **NAT Gateway** | Lambda outbound 고정 IP 확보 | Straumann IP whitelist 대응 |
| **CloudWatch** | 로그/메트릭/알람 | 운영 모니터링 |

#### API Gateway + Lambda의 제약

| 제약 | 값 | 영향 |
|------|---|------|
| API Gateway 페이로드 제한 | 10 MB | CBCT 이미지(수백 MB~수 GB)는 통과 불가 |
| API Gateway 타임아웃 | 29초 | 대용량 업로드 시 시간 초과 |
| Lambda 최대 실행 시간 | 15분 | API Gateway 경유 시 29초로 제한됨 |

따라서 Lambda는 **작은 API 호출(환자 정보, 메타데이터)에 대한 Proxy 역할만** 수행한다. 대용량 영상 파일은 API Gateway를 경유하지 않고, Straumann의 S3 Pre-signed URL로 직접 전송한다.

#### 데이터 종류별 경로

| 데이터 종류 | 크기 | 경로 | Vatech AWS 경유 |
|-----------|------|------|:---:|
| 환자 정보 (JSON) | 수 KB | EzServer → API Gateway → Lambda → AXS API | O |
| 케이스 메타데이터 (JSON) | 수 KB | EzServer → API Gateway → Lambda → AXS API | O |
| Create Document 요청 (JSON) | 수 KB | EzServer → API Gateway → Lambda → AXS API | O |
| **CBCT/2D 영상 파일** | **수백 MB~GB** | **EzServer → Straumann S3 (Pre-signed URL 직접 업로드)** | **X** |

#### 요청 흐름

**일반 API 호출 (환자 정보 전송 등)**

1. EzServer → API Gateway: 환자 데이터 전송 요청
2. API Gateway → Lambda: 요청 전달
3. Lambda → DynamoDB: 캐싱된 AXS 토큰 조회
4. (토큰 만료 시) Lambda → Secrets Manager에서 자격증명 조회 → AXS OAuth 엔드포인트로 토큰 재발급 → DynamoDB에 저장 (TTL 30분)
5. Lambda → AXS API: Bearer 토큰 + Organization-ID 헤더로 API 호출
6. AXS API → Lambda → API Gateway → EzServer: 응답 반환

**파일 업로드 (CBCT/2D 영상)**

```
1. EzServer ──→ API Gateway → Lambda → AXS API: "Create Document" (메타데이터만, 수 KB)
2. AXS API → Lambda → API Gateway → EzServer: Straumann S3 Pre-signed URL 반환
3. EzServer ───── HTTPS 직접 전송 ─────→ Straumann S3 (Pre-signed URL)
   (Vatech API Gateway/Lambda를 경유하지 않음, 용량/시간 제한 없음)
```

영상 파일은 Vatech AWS를 경유하지 않으므로 Vatech S3나 CloudFront는 불필요하다.

#### EzServer ↔ API Gateway 인증

EzServer가 Vatech API Gateway에 접근할 때도 인증이 필요하다. 인증을 두 층으로 분리한다:

| 층 | 역할 | 방법 | 관리 대상 |
|---|------|------|----------|
| **1층: 출처 확인** | "Vatech EzServer인가?" | 공유 API Key (전체 EzServer 공통 1개) | Key 1개 |
| **2층: 클리닉 식별** | "어느 클리닉인가?" | Organization-ID (Straumann 온보딩 시 발급, 클리닉별 고유) | DynamoDB 등록 목록 |

클리닉별 API Key를 개별 발급/관리하는 방식은 수백~수천 클리닉 규모에서 관리 비용이 과도하다. 대신 **공유 API Key 1개 + Organization-ID 검증**으로 충분한 보안을 확보한다.

동작 방식:
1. API Gateway에서 공유 API Key 검증 (출처 확인)
2. Lambda에서 요청의 Organization-ID를 DynamoDB 등록 클리닉 목록과 대조 (미등록 시 거부)
3. 검증 통과 시 AXS API 호출

보안 수준 분석:
- API Key가 유출되어도 **유효한 Organization-ID 없이는 AXS 호출 불가**
- Straumann `client_id`/`client_secret`은 Secrets Manager에 보관되므로 **API Key 유출과 무관하게 안전**
- Key 로테이션이 필요하면 **1개만 변경**하면 됨 (클리닉별 개별 작업 불필요)
- 관리 대상이 API Key 1개 + DynamoDB 클리닉 목록이므로 운영 부담 최소

#### 클리닉 온보딩 및 Organization-ID 관리

**온보딩 프로세스** (클리닉당 1회):

1. 클리닉이 Straumann 고객이며 EzServer가 설치된 상태에서 "AXS 연동" 요청
2. Straumann Customer Number 입력 (Invoice에 기재된 번호)
3. Straumann Access 포털에 동의 요청 생성
4. 클리닉 관리자가 Access 포털에서 승인
5. **Organization-ID 생성** (이 시점에서 처음 발급. Customer Number과 별개)
6. EzServer에 Organization-ID 설정 + Vatech DynamoDB에 등록

> Customer Number(기존 Straumann 고객 식별자)와 Organization-ID(연동 동의 후 생성되는 매핑 ID)는 별개의 개념으로, 동의 이전에는 Organization-ID를 확인할 수 없다.

**Organization-ID 저장 및 사용**:

| 위치 | 용도 | 비고 |
|------|------|------|
| **EzServer (로컬)** | API 호출 시 자신의 클리닉 식별 값으로 전송 | 암호화 저장 필수 |
| **DynamoDB** | Lambda에서 요청의 Organization-ID 유효성 검증 (허용 목록) | 마스터 저장소 역할 겸함 |

**EzServer 복구 시 Organization-ID 복구 문제**: EzServer는 On-premise이므로 로컬 데이터의 백업/복구는 EzServer 운영 책임이다. 서버 교체, 디스크 장애, OS 재설치 등으로 Organization-ID가 유실되면 AXS 연동이 불가능해진다. 이를 위해 DynamoDB에 이중 저장하며, 유실 시 Vatech 측에서 해당 클리닉의 Organization-ID를 안내하여 재설정할 수 있는 복구 경로를 확보한다.

| 시나리오 | 대응 |
|---------|------|
| EzServer 장애/교체 | DynamoDB에서 해당 클리닉의 Organization-ID 조회 → EzServer에 재설정 |
| 클리닉 연동 해제 | Straumann Access 포털에서 철회 + DynamoDB 상태를 revoked로 변경 |
| Organization-ID 유실 (EzServer 로컬) | DynamoDB에서 복구 가능 |
| Organization-ID 유실 (DynamoDB 포함 전체) | Straumann Access 포털에서 재확인 가능 여부 미확인 → **Straumann에 확인 필요** |

#### Vatech AWS 보안 범위

영상 파일이 Vatech AWS를 통과하지 않으므로, Vatech의 보안 책임 범위는 **메타데이터(환자 정보)에 한정**된다. 이는 오히려 보안 측면에서 장점이다 — 환자 영상 데이터가 Vatech 클라우드에 저장되지 않으므로 데이터 유출 위험과 개인정보보호 책임이 줄어든다.

| 보안 항목 | 적용 방법 |
|----------|----------|
| 전송 암호화 | API Gateway HTTPS (TLS 1.2+) 기본 제공 |
| EzServer 인증 | API Gateway에서 API Key 또는 자체 인증 토큰 검증 |
| 로깅/감사 | CloudWatch + CloudTrail 자동 기록 |
| Lambda 데이터 잔류 방지 | Lambda는 stateless — 실행 종료 후 메모리 해제 |
| Pre-signed URL 보안 | 시간 제한 + HTTPS 암호화. Straumann이 생성/관리 |

#### 개발 범위 (Lambda 함수 목록)

| Lambda 함수 | 역할 |
|------------|------|
| `token-manager` | AXS OAuth 토큰 발급/갱신/캐싱 |
| `patient-sync` | 환자 정보 AXS 전송 |
| `document-upload` | Create Document 호출 → Pre-signed URL 반환 |
| `case-sync` | 케이스 정보 동기화 |
| `webhook-receiver` | (Clever Orbit 이후) AXS Webhook 수신 처리 — 현 단계에서는 제외 |

### 선행 조건: Straumann 제공 필요 항목

AWS 인프라는 준비 가능하나, AXS와 통신하는 **실제 연동 코드 작성을 위해 Straumann이 반드시 제공해야 하는 항목**:

| 항목 | 필요 이유 |
|------|----------|
| OAuth 토큰 엔드포인트 URL | Lambda에서 토큰 발급 요청 대상 |
| Client Credentials Flow 파라미터 | grant_type, scope, 인증 헤더 형식 등 |
| AXS API 전체 엔드포인트 스펙 | 환자/문서/케이스/오더 관련 API 명세 |
| 테스트/샌드박스 환경 | 개발 중 실제 환자 데이터 없이 검증 |
| IP whitelist 정책 상세 | NAT Gateway IP 사전 등록 필요 여부 |
| Webhook 스펙 (Clever Orbit 이후) | 이벤트 타입, 페이로드 형식, 서명 검증 방식 |

---

## 참고 문서

- [Confidential_Review of Vatech SW Integration with AXS Platform_260402.pdf](./Confidential_Review%20of%20Vatech%20SW%20Integration%20with%20AXS%20Platform_260402.pdf) — 4/2 바텍 제안
- [Vatech meeting 30th April 2026.pdf](./Vatech%20meeting%2030th%20April%202026.pdf) — 4/30 Straumann 발표 자료
- [AXS Cloud Integration - Technical Discussion_ES_'260430.pdf](./AXS%20Cloud%20Integration%20-%20Technical%20Discussion_ES_'260430.pdf) — ES 기술 논의 포인트
- [AXS 연동 회의_'260430_v0.9.pdf](./AXS%20%EC%97%B0%EB%8F%99%20%ED%9A%8C%EC%9D%98_'260430_v0.9.pdf) — 4/30 회의록
- [AXS API Developer Portal](https://developer.axs.straumann.com/api)
