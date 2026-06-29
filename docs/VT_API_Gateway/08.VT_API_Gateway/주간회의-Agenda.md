# VT API Gateway — 6/25 주간회의 Agenda

- 이번 주 진행
    - ③ GW SRS 본문 정합화 계속(§1~§7, baseline 전) — 이번 주 upload·webhook·인프라 결정 반영
    - 라우팅 모델 전환: 3버킷 → ADR-11 target-routed proxy(`Vatech-Target` 유무로 GW고유 API/프록시 구분, verbatim bypass, 신규 upstream=레지스트리 1행)
    - 업로드 모델 변경: GW presigned 비발급 확정 — `/v1/uploads`·리전 Signer 폐기, 발급 주체=CleverSpace(②)·AXS(③), GW는 중계(bypass)만
    - Webhook 재정의: 유연 수신 + provider별 전용 호스트(`{provider}.webhook.gw.vatech.com`)로 발신자 식별(Host/SNI), 식별≠인증(HMAC); 클라우드 수신=CleverLab만(CleverSpace 대상 아님)
    - 배포·데이터 토폴로지 신설(§2.1.1): 멀티서버·멀티리전·전역 일관 복제/리전 캐시·1차 단일→2차 멀티·apex DNS `gw.vatech.com` 확정. **GW는 AWS 전용 배포**(아래 결정)
      - (결정) GW는 AWS에만 배포하고 AWS 미지원국가도 GW접속은 가능하다.
        - AWS 미지원국가는 최대한 가까운 AWS GW를 배포한다.
        - AWS 미지원국가는 MinIO 정도만 제공하면 된다. MinIO도 GW가 제공하는 것이 아니라, Provider가 제공하는 것이다. GW는 중계만 한다. 
    - EKS 정합 스택 정리(AWS 전용): DB=PostgreSQL 확정(AWS=Aurora 권장)·ElastiCache·**SQS(A·내부 큐)**·MQTT 엣지(B·IoT Core/Amazon MQ)·IRSA. 스토리지는 **GW 비호스팅 — Provider(CleverSpace/AXS) 발급, GW 중계만**(AWS=S3 / AWS 미지원국=Provider MinIO). 메시징 2-레그(A=SQS / B=MQTT)
    - 분배 지식 DB·관리 API 추가(org_mapping·webhook_provider·upstream_registry·delivery_channel·region_catalog) + 온보딩 자동등록(EzServer, 아래 결정)
      - (결정) EzServer 설치 후, LMP Clinic ID를 받는 순간 GW로 Clinic ID를 전송해서 자동등록되게 한다.
        - 연동을 하지 않더라도 무조건 GW에 등록한다.
    - 디바이스 토큰 갱신=client_credentials 재발급(refresh token 미발급) 명문화
    - 문서 정합화: ARD(ADR-11·Router/PEP)·개발계획서(EKS 스택)·인증보안·Roadmap 동기화, Redis 키스페이스 카탈로그 신설, design(OpenAPI·DBML) SRS와 정합
    - 
- 논의 사항 (GW SRS 작성하면서 생긴 질문)
    | # | 항목 | 타입 | 설명 / 묻는 것 | 출처 | 결정 |
    | --- | --- | --- | --- | --- | --- |
    | 1 | 디바이스 정의·연결 모델 (확인) | [논의] | ARD §5는 디바이스가 GW에 직접 연결(무인 장비 머신 인증)되는 것처럼 보이는데, 그간 논의는 EzServer 경유였음 → 실제는 어느 쪽인가? (단순 확인) | ARD §5 | (결정) GW입장에서 Device=EzServer |
    | 2 | 업로드·스토리지 모델 정합 | [확정] | 개발계획서는 "업로드 세션"·S3/MinIO·"리전 signer"를 GW 범위로 둠. 합의는 GW 비발급·중계만(발급=CleverSpace/AXS) → 확정 방향. SRS/ARD는 이미 후자, 개발계획서만 정합 필요 | 개발계획서 §2·§5 | GW 비발급·중계 확정, 개발계획서 수정 |
    | 3 | 라우팅 모델 ADR-11 | [확정] | Vatech-Target 유무로 GW-API vs 프록시 구분 — 헤더 있으면 GW가 모든 API를 정의하지 않고 Vatech-Target 값(예: axs, cleverspace)으로 실제 전달 대상 서버를 결정해 그대로 중계, 없으면 GW 자체 API 호출. CCB 승인 + GW 클라이언트(EzServer, CleverOne 경유)의 Vatech-Target 부착 적응. 식별/버전 헤더는 Roadmap §5에서 이미 확정 |  | CCB 승인 → baseline 반영 |
    | 4 | Webhook 클라우드 분배 | [논의] | CleverLab 갈래B 활성화 여부·시점 (CleverSpace는 대상 아님 확정) |  | v1.0 제외, GW Open 후 결정 |
    | 5 | ~~클리닉 GW 등록 주체~~ | [확정] | **확정(6/25): EzServer가 LMP Clinic-ID 수신 시 자동·무조건 GW 등록**(연동 무관). CleverOne 대안 폐기 | §2.3.1 | 완료 |
    | 6 | AXS sandbox 자격증명 | [정보] | sandbox endpoint·OAuth client를 스트라우만이 제공해야 TC-01~04 가능 — 확보 시점 확정됐나? pilot(08-15) 블로커 | AXS 테스트환경 §4 | Straumann과 계약/제공 후? |
    | 7 | 경로 B EOS 시점 | [논의] | 레거시 경로 종료 시점 |  | ① One Pager 확정 시? |
    | 8 | v1.0 목표 RPS·동시 세션 | [정보] | fleet 규모 수치 — 인프라/규모 PL 입력 |  | 인프라/규모 PL 입력 후 확정? |
    | 9 | RTO/RPO·유지보수 윈도우 | [정보] | 가용성 목표 — 인프라 |  | 인프라 설계 단계 확정? |
    | 10 | 감사·consent 보존 기간 | [정보] | 법정 보존 기간 — 품질/법무 |  | 법정 기준(법무 확인) 후? |
    | 11 | 호환성 매트릭스 확정본 | [정보] | One Pager 산출 의존 |  | ① One Pager 확정 시? |
    - 타입: [확정] 기결정 공식 확정/승인 · [논의] 방향 결정 필요 · [정보] 추가 입력·자료 확보

# VT API Gateway — 7/2 주간회의 Agenda

- 이번 주 진행 (6/25 이후)
    - ③ GW SRS 본문 정합화 계속(baseline 전) — 6/25 결정(ADR-11·presigned 비발급·AWS 전용·자동등록) 본문 반영 마무리
    - 캐시 엔진 **Redis → Valkey**(ElastiCache for Valkey) 전환 — 라이선스·비용·호환성. 키스페이스 카탈로그·SRS·ARD·개발계획서 동기화
    - **환경 3종(dev/test/prod) 매트릭스** 정리(§3.1) + 개발 의존성·에뮬레이션(§3.4: AXS sandbox·EPI 클라이언트 에뮬레이터·스텁) + staging(§3.5)
    - **구조화 로그 구조 정의**(§6.3.2, JSON 필수 필드·상관관계 ID) + 수집층 권장 패턴(Fluent Bit=노드 로그 / ADOT=OTel 트레이스·메트릭, 역할 분리)
    - 용어 정합: 디바이스=EzServer(GW 관점)·LMP(LicenseManager, Clinic-ID 소스)·PHI·OTel·ADOT·Valkey(§1.4)
    - §6.9 사이트 적응(멀티리전·비-AWS국) 재작성 — 폐기된 GW signer·GW 스토리지 호스팅 잔재 제거(GW는 중계만)
    - **라우팅 방식 비교표 추가(§4.1.2, ADR-11)** — 단, 정직 재평가 결과 "헤더가 모든 면 우수"는 아님 → 아래 논의 R1로 상정
    - 참조 카탈로그 정비(제품별 references 재편) · `munto-dev-assistant → abc-dev-assistant` 리포 정합 · 공통 규칙(authoring·comments·git-commit·markdown) 어댑터 패턴 반영
    - 문서 품질: `N/A(기존과 동일)` 오용 교정(spec-standard + SRS) — "기존과 동일"은 N/A 아님 → 정확한 링크/복사/TBD

- 논의 사항 (7/2 신규)
    - **R1. 라우팅 방식 재평가 (중요 · 평가 요청)** — ADR-11에서 헤더(`Vatech-Target`)로 결정·CCB 승인했으나, **운영/장애대응·업계 관례 관점에서 경로 프리픽스가 더 유리**할 수 있어 회의에서 재평가받고자 함. 헤더가 "모든 면에서 우수"한 것은 아님(아래 표 — 트레이드오프).

        | 기준 | A. 헤더 `Vatech-Target` (현 결정) | B. 경로 프리픽스 `/axs/…` | C. 서브도메인 `axs.gw…` | D. 클라이언트 지정 host |
        | --- | --- | --- | --- | --- |
        | 업계 관례(일반성) | △ 덜 흔함(주로 버전·카나리) | ◎ **가장 흔함** | ○ 흔함 | ✕ 안티패턴 |
        | verbatim(upstream 원 path 보존) | ◎ host만 교체 | △ 프리픽스 strip(변환) 필요 | ◎ 그대로 | ◎ 그대로 |
        | GW 고유 API ↔ 프록시 구분 | ◎ 헤더 유무로 배타 | △ 둘 다 path라 경계 모호(예약 prefix 필요) | ◎ 호스트 분리 | △ 모호 |
        | 경로 충돌(우리 `/v1`·upstream 자체 path) | ◎ 없음 | △ 충돌 가능 | ◎ 없음 | ○ |
        | 클라이언트 적응 비용 | ◎ 헤더 1개 추가 | ○ 경로 프리픽스 부착 | △ base URL 변경 | ✕ |
        | 보안(SSRF·오픈 프록시) | ◎ 논리 ID·서버 레지스트리 | ◎ 서버 레지스트리 | ◎ | ✕ host 노출 |
        | DNS/TLS·인프라 비용 | ◎ 단일 apex | ◎ 단일 apex | △ upstream별 DNS·cert | ◎ |
        | 멀티 리전(GW 다리전 배포 + 리전별 upstream 선택) | ◎ 단일 apex 지오라우팅·리전은 `Clinic-Id`로 분리 | ◎ 동일(단일 apex·리전도 `Clinic-Id`) | △ 서브도메인×리전 host 폭증·DNS/cert↑ | △ |
        | **확장성(신규 연동 서버 추가)** | ◎ 레지스트리 1행+enum, 코드변경 0 | ○ prefix 예약·충돌관리 필요 | △ DNS·cert 추가 | ✕ |
        | **유지보수·장애대응**(표준 로그·LB/CDN/WAF에서 target 가시·제어) | **△ 커스텀 헤더 — 로그·엣지 제어에 추가 설정 필요** | **◎ URL에 target 노출 — 표준 도구로 추적·차단·rate-limit** | **◎ host 노출(표준 로그)** | △ |
        | 관측·정책(앱 내부 target 식별) | ◎ 단일 헤더 키 | ○ path 파싱 | ○ host 파싱 | △ |

        - **헤더(A) 우위**: verbatim 중계 · GW고유 API와 프록시 배타 구분 · 단일 apex · 클라이언트 최소 변경. (멀티 리전은 A·B 동률 — 리전은 어느 방식이든 `Clinic-Id`로 정함)
        - **경로(B)/서브도메인(C) 우위**: 업계 관례 · **운영/장애대응**(target이 URL/host에 그대로 보여 표준 로그·LB/CDN/WAF로 바로 추적·차단·rate-limit; 헤더는 커스텀이라 추가 설정 필요).
        - **확장성·보안**: A·B 비슷(둘 다 서버 레지스트리/설정 기반, SSRF 안전). C는 upstream마다 DNS·cert 부담.
        - **정직한 결론**: "헤더가 전부 우수"는 과장. **통합 모델 깔끔함(A) vs 운영 친화(B)** 의 트레이드오프다. 핵심 판단 = "verbatim·apex 단일화·A↔프록시 명확 구분"의 가치 ↔ "장애 시 표준 도구로 target 추적·제어"의 가치 중 무엇을 더 중히 둘 것인가. → **회의 결정 요청.** (절충안: 헤더 유지 + ALB/CDN 액세스 로그에 `Vatech-Target` 헤더 캡처 의무화 + 엣지 룰을 헤더 매칭으로 구성 → B의 운영 이점을 일부 흡수)
    - **R2. 캐시 엔진 Valkey 전환 확정** — Redis→Valkey 방향 승인 요청(라이선스·비용)
    - **R3. 수집 에이전트 확정** — Fluent Bit + ADOT 분리 패턴 인프라 비준(Appendix B #14)

- 이월 논의 사항 (6/25 미결 — 계속)
    | # | 항목 | 타입 | 상태 |
    | --- | --- | --- | --- |
    | 4 | Webhook 클라우드 분배(CleverLab 갈래B) | [논의] | v1.0 제외 — Open 후 결정 |
    | 6 | AXS sandbox 자격증명(Straumann 제공) | [정보] | pilot(08-15) 블로커 — 확보 시점? |
    | 7 | 경로 B EOS 시점 | [논의] | ① One Pager 확정 의존 |
    | 8 | v1.0 목표 RPS·동시 세션 | [정보] | 인프라/규모 PL 입력 대기 |
    | 9 | RTO/RPO·유지보수 윈도우 | [정보] | 인프라 설계 단계 |
    | 10 | 감사·consent 보존 기간 | [정보] | 법무 확인 대기 |
    | 11 | 호환성 매트릭스 확정본 | [정보] | ① One Pager 의존 |


