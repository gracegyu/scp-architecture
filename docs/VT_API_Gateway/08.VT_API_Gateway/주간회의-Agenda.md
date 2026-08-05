# VT API Gateway — 6/25 주간회의 Agenda

- 이번 주 진행
  - ③ GW SRS 본문 정합화 계속(§1~§7, baseline 전) — 이번 주 upload·webhook·인프라 결정 반영
  - 라우팅 모델 전환: 3버킷 → ADR-11 target-routed proxy(`Vatech-Target` 유무로 GW고유 API/프록시 구분, verbatim bypass, 신규 upstream=레지스트리 1행)
  - 업로드 모델 변경: GW presigned 비발급 확정 — `/v1/uploads`·리전 Signer 폐기, 발급 주체=CleverSpace(②)·AXS(③), GW는 중계(bypass)만
  - Webhook 재정의: 유연 수신 + upstream별 전용 호스트(`{target}.webhook.gw.vatech.com`)로 발신자 식별(Host/SNI), 식별≠인증(HMAC); 클라우드 수신=CleverLab만(CleverSpace 대상 아님)
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
- 논의 사항 (GW SRS 작성하면서 생긴 질문) | # | 항목 | 타입 | 설명 / 묻는 것 | 출처 | 결정 | | --- | --- | --- | --- | --- | --- | | 1 | 디바이스 정의·연결 모델 (확인) | [논의] | ARD §5는 디바이스가 GW에 직접 연결(무인 장비 머신 인증)되는 것처럼 보이는데, 그간 논의는 EzServer 경유였음 → 실제는 어느 쪽인가? (단순 확인) | ARD §5 | (결정) GW입장에서 Device=EzServer | | 2 | 업로드·스토리지 모델 정합 | [확정] | 개발계획서는 "업로드 세션"·S3/MinIO·"리전 signer"를 GW 범위로 둠. 합의는 GW 비발급·중계만(발급=CleverSpace/AXS) → 확정 방향. SRS/ARD는 이미 후자, 개발계획서만 정합 필요 | 개발계획서 §2·§5 | GW 비발급·중계 확정, 개발계획서 수정 | | 3 | 라우팅 모델 ADR-11 | [확정] | Vatech-Target 유무로 GW-API vs 프록시 구분 — 헤더 있으면 GW가 모든 API를 정의하지 않고 Vatech-Target 값(예: axs, cleverspace)으로 실제 전달 대상 서버를 결정해 그대로 중계, 없으면 GW 자체 API 호출. CCB 승인 + GW 클라이언트(EzServer, CleverOne 경유)의 Vatech-Target 부착 적응. 식별/버전 헤더는 Roadmap §5에서 이미 확정 | | CCB 승인 → baseline 반영 | | 4 | Webhook 클라우드 분배 | [논의] | CleverLab 갈래B 활성화 여부·시점 (CleverSpace는 대상 아님 확정) | | v1.0 제외, GW Open 후 결정 | | 5 | ~~클리닉 GW 등록 주체~~ | [확정] | **확정(6/25): EzServer가 LMP Clinic-ID 수신 시 자동·무조건 GW 등록**(연동 무관). CleverOne 대안 폐기 | §2.3.1 | 완료 | | 6 | AXS sandbox 자격증명 | [정보] | sandbox endpoint·OAuth client를 스트라우만이 제공해야 TC-01~04 가능 — 확보 시점 확정됐나? pilot(08-15) 블로커 | AXS 테스트환경 §4 | Straumann과 계약/제공 후? | | 7 | 경로 B EOS 시점 | [논의] | 레거시 경로 종료 시점 | | ① One Pager 확정 시? | | 8 | v1.0 목표 RPS·동시 세션 | [정보] | fleet 규모 수치 — 인프라/규모 PL 입력 | | 인프라/규모 PL 입력 후 확정? | | 9 | RTO/RPO·유지보수 윈도우 | [정보] | 가용성 목표 — 인프라 | | 인프라 설계 단계 확정? | | 10 | 감사·consent 보존 기간 | [정보] | 법정 보존 기간 — 품질/법무 | | 법정 기준(법무 확인) 후? | | 11 | 호환성 매트릭스 확정본 | [정보] | One Pager 산출 의존 | | ① One Pager 확정 시? |
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
  - 참조 카탈로그 정비(제품별 references 재편) · 공통 규칙(authoring·comments·git-commit·markdown) 정합
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
  - **R4. 프록시(B/C) 에러·타임아웃 정책 (결정 필요)** — GW가 다른 서버(AXS·CleverSpace 등)로 요청을 중계할 때 **연결 실패·네트워크 일시 장애·응답 지연**을 어떻게 처리할지가 정의돼 있지 않던 공백을 채움. 회의에서는 **아래 골격 확인 + 표의 수치·서킷 v1.0 범위만 결정**하면 됨. _(이 안건은 SRS 없이 이 문서만으로 결정 가능하게 정리했다. 셀 안의 `§…`·Appendix 번호는 결정 후 반영할 SRS 위치 표시일 뿐, 결정에는 불필요.)_
    - **정책 골격(이미 SRS 초안에 반영 · 확인용)**:
      - 타임아웃 계층(핵심): GW는 서버이자 upstream의 클라이언트 → **`GW 총 deadline < 클라이언트 타임아웃`**. 아니면 클라이언트가 먼저 끊어도 GW는 계속 기다려 **고아 요청·자원 점유·재시도 증폭** → GW가 먼저 504 반환해 결정적 오류 제공.
      - 재시도(보수적): GW는 **연결 수립 실패(전송 전)만 1회**(전 메서드 안전) — 응답 타임아웃·5xx는 재시도 안 함. 타겟당 upstream 1개라 풀 재시도 이점이 없고, 앱 레벨 재시도는 클라이언트 소유(D5).
      - 오류 매핑: GW가 만든 오류(대상에 못 감: 연결실패 502 / 응답 지연 504 / 서킷 차단 503)는 GW 표준 본문으로, **대상 서버 자체 오류(4xx/5xx)는 원응답을 그대로 통과**(GW가 안 바꿈). `Vatech-Error-Origin: gateway|upstream` 헤더로 책임 구분.
    - **결정 항목 (설명 · 추천안 — 승인/조정 요청)**:

      | # | 결정 항목 | 설명 (왜 필요한가) | 추천안 | 비고·근거 |
      | --- | --- | --- | --- | --- |
      | D1 | `connect_timeout` (per-upstream) | TCP+TLS 핸드셰이크 대기 시간 — upstream 도달 불가를 빠르게 502로 | **3초** | 짧게 잡아 장애 빠른 감지 |
      | D2 | `response_timeout` (per-upstream) | 연결 후 upstream 응답 대기 — 초과 시 504 | **기본 10초**, 외부(AXS)는 SLA 반영 개별값 | 대용량 파일은 presigned 직결(GW 미경유)이라 제외 |
      | D3 | `total_deadline` (per-upstream) | 프록시 호출 전체 예산 — **클라이언트 타임아웃보다 작아야 함** | **클라이언트 타임아웃의 ≤80%** (예 클라 30초 → GW 15~20초) | 불변식 `GW < 클라` 보장 |
      | D4 | 클라이언트(EzServer) 타임아웃 확정 | D3 상한의 근거 — EzServer→GW 호출 타임아웃 값을 명시·고정해야 GW deadline을 그보다 작게 잡음 | **30초로 명시·고정** (EzServer팀 확인) | 미확정 시 D3 산정 불가. 인지 방식은 D10 |
      | D10 | 클라이언트 타임아웃 **인지 방식** | HTTP는 클라이언트 타임아웃을 기본 전달 안 함 — GW는 클라이언트가 끊을 때(연결 close)만 _사후_ 감지. "GW가 먼저 504" 보장하려면 값을 *사전*에 알아야 함 → (A) 계약값 합의 / (B) timeout 헤더 전파 | **하이브리드**: v1.0=(A) SRS 계약값 합의(EzServer↔GW 우리 소유로 충분) + 선택적 **`Vatech-Timeout-Ms` 헤더(상대값) 있으면 GW가 내부 deadline=`now + min(헤더, 설정)`으로 클램프(B)**. 연결 close→upstream 취소는 공통 안전망 | 헤더는 **상대 timeout**(gRPC `grpc-timeout`·Envoy `x-envoy-expected-rq-timeout-ms` 선례, 클록 동기 불필요). "deadline"=GW 내부 절대시각 개념. 외부·3rd-party(CleverLab 등) 확장 대비 |
      | D5 | 재시도 **소유·범위** | GW가 재시도할지 / 클라이언트가 할지 + 어떤 실패만 | **GW는 연결 수립 실패(요청 전송 전)만 1회**(전 메서드 안전). 응답 타임아웃·5xx 재시도 안 함. **앱 레벨 재시도는 클라이언트(EzServer) 소유** | 타겟당 upstream 1개라 풀 재시도 이점 없음 + verbatim relay. HAProxy 기본과 동일. 비멱등 POST 0회 |
      | D6 | 재시도 폭주 방지 (재시도 활성 시) | 재시도가 오히려 부하를 키우는 것 방지 | **D5 권장(1회)이면: retry budget 전체의 10%만**(백오프·jitter 불필요 — 1회라 늘릴 간격이 없음). **재시도를 다회로 넓히면: 지수 백오프+jitter 추가** | D5에서 재시도 횟수 결정에 종속 |
      | D7 | 서킷 브레이커 v1.0 포함 여부 | 한 upstream 장애가 GW 전체로 전파되는 것 차단(빠른 실패 503) | **v1.0 포함(경량)** — 연속 5실패 또는 10초 창 50% 실패율 → open, 30초 후 half-open | 부담 시 임계만 보수적, 미루면 gw/1.1 |
      | D8 | 503 `Retry-After` 부여 | 서킷 open·일시 불가 시 클라이언트에 재시도 시점 안내 | **포함** | 클라이언트 재시도 정렬 |
      | D9 | 오류 매핑·`Vatech-Error-Origin` 헤더 | 장애 시 "GW가 못 갔다" vs "대상 서버가 거부했다"를 호출자(EzServer)가 구분 → 원인 추적·대응 분기 | **확정**: GW 생성 오류=502/504/503+GW 표준 본문(`Vatech-Error-Origin: gateway`), 대상 서버 자체 4xx/5xx=원응답 그대로 통과(`origin: upstream`) | 위 '정책 골격' 오류 매핑과 동일 |

    - **용어 풀이(D6)** — 재시도를 "켰을 때" 그 재시도가 오히려 장애를 키우지 않게 하는 안전장치:
      - **지수 백오프(exponential backoff)**: 재시도 간격을 점점 늘림(예 200ms→400ms→800ms). 과부하 upstream에 즉시 재시도를 퍼붓지 않고 회복할 틈을 줌 — _너무 빨리 다시 두드리지 않기_.
      - **jitter(지터·무작위 흔들기)**: 백오프 간격에 랜덤을 더함(예 200ms → 150~250ms 랜덤). upstream이 살아나는 순간 수많은 클라이언트가 _동시에_ 재시도해 다시 죽이는 떼몰림(thundering herd)을 분산 — _다 같이 동시에 두드리지 않기_.
      - **retry budget 전체의 10%**: 재시도를 전체 요청의 10%까지만 허용(예 1,000건 중 재시도 ≤100건). 횟수 제한(1회)만으론 upstream 완전 다운 시 모든 요청이 재시도돼 트래픽이 2배가 됨 → 비율 상한으로 폭주 차단 — _너무 많이 두드리지 않기_(Envoy retry budget 방식).
      - **D5 권장(연결 실패만 1회)이면**: 1회라 늘릴 간격이 없어 **지수 백오프는 불필요**, jitter도 단일 지연이라 거의 무의미. **retry budget만 유효**(개별은 1회라도 전체가 동시에 연결 실패하면 합산 트래픽이 2배 → 비율 상한은 의미 있음). 백오프·jitter는 **재시도를 다회로 넓힐 때만** 필요하다.
    - **용어 풀이(D7 서킷 브레이커)** — 전기 차단기처럼, upstream(AXS)이 죽었을 때 그쪽 길을 잠시 끊어 장애가 GW 전체로 번지는 걸 막는 장치. 없으면 죽은 AXS를 매 요청마다 타임아웃까지 기다리느라 GW 커넥션·워커가 고갈됨.
      - **3가지 상태**: **closed(닫힘=정상)** 평소처럼 전달 / **open(열림=차단)** AXS로 안 보내고 **즉시 503**(기다림 0) / **half-open(반열림=탐침)** 요청 1개만 보내 살았는지 확인 → 성공 시 closed 복귀, 실패 시 다시 open. (차단기처럼 "열림=끊김"이라 직관과 반대.)
      - **"연속 5실패 또는 10초 창 50% 실패율 → open"** = _언제 차단할지_: 연속 5번 실패하거나 최근 10초 요청의 절반 이상이 실패하면 차단으로 전환.
      - **"30초 후 half-open"** = _언제 회복을 시험할지_: 차단 후 30초간은 즉시 503(AXS 쉬게 둠), 30초 뒤 요청 하나로 살아났는지 떠봄.
      - 흐름: 정상(closed) → 장애 감지 → 차단(open, 30초 즉시 실패) → 30초 후 탐침(half-open) → 살았으면 복귀 / 아니면 다시 차단.
      - **상태 공유(멀티 서버)**: 서킷 런타임 상태(open/closed·카운터)는 **각 GW pod 메모리(공유 안 함)** — DB·Redis·GW간 동기화 미사용. 각 pod가 자기 관측으로 보호하는 게 표준(Resilience4j·Envoy). **공유되는 건 설정값뿐**(임계·타임아웃 = `upstream_registry`/DB, pod별 캐시). 별도 컴포넌트 없이 `ROUTER`/`CONN` in-process(§2.2·§7.5.4).

  - **R5. IaC 도구 확정 — CDK vs Terraform (결정 필요)** — 문서엔 `IaC = Terraform`(ARD §4.5·SRS §6.6.2)으로 적혀 있으나 팀 실무는 **AWS CDK**. 모순 해소 + 확정 필요. **권장 = CDK** (AWS 전용 전제에서 CDK 우위).
    - **비교표 (CDK vs Terraform)**:

      | 기준 | AWS CDK **(권장)** | Terraform |
      | --- | --- | --- |
      | 멀티클라우드 | △ AWS 전용 | ◎ 멀티클라우드 — **그러나 우리는 AWS 전용(6/25)이라 이점 무의미** |
      | 작성 언어 | ◎ **TypeScript** = GW(NestJS/TS)와 동일 언어 → 개발자가 인프라 코드도 읽고 기여 | △ HCL(별도 언어 학습) |
      | AWS 신규 서비스 대응 | ◎ AWS 1st-party·즉시 반영(CloudFormation) | ○ provider 업데이트 대기 가능 |
      | 드리프트·롤백 | ◎ CloudFormation 네이티브(자동 롤백) | ○ state 기반(별도 관리) |
      | 조직 실무·역량 | ◎ 기존 사용 | △ 신규 도입 |
      | 모듈 생태계·멀티계정 | ○ Constructs | ◎ 성숙한 모듈·state·멀티계정 오케스트레이션 |

    - **핵심 논리**: Terraform을 고르는 가장 큰 이유 = 멀티클라우드인데 **AWS 전용이면 그 이유가 사라진다**. 남는 비교에서 CDK가 **언어 일관성(TS)·AWS 네이티브·조직 역량**으로 우위. (Terraform의 모듈·state 강점은 AWS 전용 + TS 스택에선 일관성에 밀림.)
    - **결정 요청**: ① IaC 도구 = CDK 확정? ② 확정 시 ARD §4.5·SRS §6.6.2 정합(Terraform→CDK) ③ 최종 표준은 인프라(③-I) 소유 확인.

  - **R6. GW SRS 리뷰어 목록 확정 (회의에서 작성)** — ③ GW SRS(+OpenAPI·DBML) **PR 7/9 시작 전**에 리뷰어를 지정해야 리뷰가 공백 없이 진행된다. SRS가 걸치는 **영역별로 리뷰어를 배정**한다. 아래 표의 이름 칸을 회의에서 채운다(총괄 2인은 CCB 기확정, 나머지는 영역 담당 지명).

    | 영역 | 리뷰 포인트 | 리뷰어 |
    | --- | --- | --- |
    | 총괄·승인(CCB) | baseline 승인 | **Scott(실장·총괄)·Raymond(GW 리드)** · **PM=미지정(별도 지정 가능)** |
    | 아키텍처·라우팅 | ADR(특히 ADR-11 R1 재평가)·3-plane·§2 | **Thomas** (외 추가 가능 — 복수 아키텍트) |
    | 인증·보안 | §7.1·§6.2·§6.5·PHI·데이터 주권 | (보안 담당) — ❓ |
    | 인프라(③-I) | §3.1·배포·EIP·IaC(R5)·환경 구축 | **Jack** |
    | DB·데이터 모델 | §6.4·DBML·보존기간(#5) | **GW 팀(작성자) = Raymond** — 자체 소유(별도 DBA 없음). 보존기간(#5)만 법무/품질 입력 |
    | API 계약 | §4·§7·OpenAPI 정합·에러 계약 | **GW 팀(작성자) = Raymond** — 자체 소유(총괄과 동일). _외부_ 적합성 검토는 소비자 ③-P |
    | 제품 적응 ③-P-EZ (EzServer) | 클라이언트·클리닉 등록 주체 영향 | ❓ (담당 1인 이상) |
    | 제품 적응 ③-P-CS (CleverSpace) | presigned·B 프록시 영향 | ❓ (담당 1인 이상) |
    | 제품 적응 ③-P-CO (CleverOne) | Vatech-\* 헤더·경유 전환 영향 | ❓ (담당 1인 이상) |
    | 제품 적응 ③-P-OID (OneID) | 인증 연계 영향 | ❓ (담당 1인 이상) |
    | QA·검증 | §3.6·테스트·호환성 매트릭스 | **James** |
    - **산출**: 영역×이름 확정 명단 → PR 리뷰어로 지정. 미정(❓) 영역은 담당 지명 요청. (리뷰어는 영역별 1인 이상, 동일인 복수 영역 가능)

  - **R7. 스펙 ↔ GW 구현 진행 전략 (결정 필요)** — **전제(고정): GW의 통합·테스트 가능한 완성은 ④ AXS 연동까지 필요**하다(AXS=첫 연동, 이것 없이 개발·E2E 테스트 불가). 따라서 **GW 구현은 ④ AXS Sub-SRS baseline 이후 착수**가 필수다(core 일부는 ③ baseline 후 선행 가능하나 통합·테스트는 ④ 후). → 쟁점은 _나머지 스펙(③-C·③-P·③-I)을 구현과 병행할지(1안) vs 선완료할지(2안)_.
    - **1안 — ④ baseline 직후 구현 착수 + ③-C·③-P·③-I 스펙 병행** (그 스펙 종료는 뒤로 늘어남)
    - **2안 — ③-C·③-P·③-I까지 전 스펙 완료 후 구현 착수**

      | 항목           | 1안 (④ 후 구현 + 나머지 스펙 병행) | 2안 (전 스펙 완료 후 구현)       |
      | -------------- | ---------------------------------- | -------------------------------- |
      | 구현 착수      | ④ AXS baseline 직후(이른 편)       | ③-C·③-P·③-I까지 완료 후(더 늦음) |
      | 재작업 리스크  | ↑ ③-C/③-P/③-I 미확정 위 일부 구현  | ↓ 스펙 안정 후 구현              |
      | IEC 62304 추적 | 스펙·구현 동시 → 추적 부담         | baseline 후 구현 → 깔끔          |
      | 전체 납기      | 빠름                               | 느림                             |

    - **공통 전제**: 어느 안이든 **구현 시작점 = ④ AXS baseline**(둘의 차이는 ③-C/③-P/③-I 스펙을 병행하느냐 선완료하느냐). **구현 기간은 미정 — SRS 확정 후 재산정**(gantt의 `③ GW SRS + 구현` 섹션에 _기간 미정_ 막대로 표기).
    - **pilot 8/15 영향**: 구현이 ④ baseline(현 gantt ~8월 초) 이후라 **pilot 8/15는 어느 안이든 매우 빠듯**(2안은 사실상 불가). → pilot 일정 자체를 R7과 함께 재검토 필요(개발계획서 정합).
    - **검토 의견**: AXS 의존이 고정이므로 **1안(④ 후 구현 착수, 나머지 스펙 병행)** 이 현실적. 2안은 납기 지연을 감수. 단 **구현 기간·pilot은 SRS 확정 후 재산정**.

  - **R8. 데이터 모델 관계(ERD) 확인 (SRS §6.4.1)** — Clinic·Device·외부 Org 관계를 ERD로 정리(SRS §6.4.1). 회의에서 확인 요청.

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

    - **확정 사항(A안)**: ① **기본=Clinic·Device / 확장=외부 Org-ID**(연동 시만) ② **Clinic↔Device 1:N**(현 1:1=EzServer), `device.clinic_id` nullable ③ **region SSOT=Clinic, device는 clinic 파생**(device.region·region_mapping 제거) ④ 외부 Org-ID=(provider, org_id)→clinic, AXS 송신·webhook 분배에 사용 ⑤ 신규 provider=org_mapping 확장 or 신규 테이블+추가 개발(기본 불변).
    - **DBML·OpenAPI 반영 완료** — 회의에서 관계·카디널리티 **확인/승인** 요청.
    - **org_mapping 경계(확인)**: org_mapping = **얇은 식별자 매핑**(공통 조각)일 뿐, provider별 인증·webhook·payload는 이미 분리(connector·webhook_provider·④). **구조 다른 provider = 전용 테이블+로직(설계된 분기)** — "만능 표" 아님.
    - **미결(확인 요청)**: ① EzServer=클리닉당 1개 확정?(Device 1:N 유지 vs 1:1 UNIQUE 강제) · ③ clinic-less device(미래) region 처리 · ⑤ **policy.tenant 범위**(clinic 단위+전역기본 NULL·device 배제 확인).
    - **→ 해소·갱신(2026-07-06 · device-중심 정체성 정립)**: SRS §1.2에 **GW=범용 API GW · 호출 주체=device · clinic=device의 선택적 그룹**을 정의(현재 EzServer/AXS/CleverSpace + 미래 다수 provider·비-EzServer·clinic-less 확장성). 이로써 위 미결이 다음으로 정리됨:
      - **① Device 1:N 모델 유지**(1:1 UNIQUE 강제 안 함) — device=주체, clinic 선택적. 현 EzServer=클리닉당 1개는 운영 사실일 뿐, 모델 제약 아님.
      - **③ clinic-less device region = 미래 확장점 확정**(지금 미정의 — 등장 시 자체 region/global, §1.2 Will Not Do·Appendix B #33).
      - **⑤ policy 스코프 = device-중심 확정(device→clinic→global)** — 구 'device 배제'를 **대체**. `policy.tenant`(clinic 하드 FK) → **`scope_type{global\|clinic\|device}+scope_id`**. clinic=clinic-bound device의 **상한(ceiling)**, device는 그 안에서 narrowing(§7.5.3, deny-by-default). _device 단위 policy는 clinic-less/예외용 — v1.0은 clinic+global만 사용._
      - **org_mapping 경계**: 얇은 식별자 매핑(clinic-키) 유지, device-스코프는 미래 확장점(#33). region A안(②③ SSOT=clinic)·nullable·1:N는 **불변**.
      - 반영 완료: SRS §1.2·§1.4·§6.4.1·§7.5.3·Appendix B #32/#33 · DBML(`policy_scope`)·db-jsonb · ARD v0.25.
    - **해결됨(보고)**: ② 전용 `clinic` 테이블 = **`clinic_region_mapping`을 `clinic`으로 승격 확정**(C안, 2026-07-01) · ④ **`connector`(아웃바운드)/`provider`(인바운드) 분리 유지 확정**(통합 안 함); `provider` 표기는 정규 토큰·enum 금지(레지스트리 FK는 선택).

  - **R9. 온보딩/enrollment 모델 확인 (대부분 "확인만" · ⑤ 인증방식만 CCB/보안 sign-off 권장)** — 이번 주 SRS 정합화에서 온보딩·enrollment을 아래로 구체화·통합했다. 회의에서는 **"이렇게 하면 되냐" 확인**(변경 없으면 확정). ⑤ private_key_jwt는 인증 아키텍처 결정이라 보안/CCB 승인이 좋다.
    - **① 온보딩 = enrollment 단일 흐름 (2분할 폐기)** — 기존 "(1) 클리닉 등록 + (2) enrollment"를 없애고 **EzServer enroll이 clinic·초기 region까지 흡수**(별도 클리닉 등록 API·흐름 없음). enrollment=최초 1회(재설치 시 재-enroll 회전), **region *변경*은 별개**(§7.3.4).
    - **② region 기본 = GeoDNS 최근접(v1.0=서울) + C/S override** — enroll 요청이 GeoDNS로 도달한 리전이 기본 region이고, **현장 C/S가 다른 region을 선택**할 수 있다.
    - **③ 활성화 = C/S 승인 게이트** — enroll 완료 디바이스=`pending`(인증 불가) → **현장 설치 담당 C/S가 GW Console 승인**(설치 확인+region 확정) → `active`. **승인 주체=C/S 본인**(Admin 아님), C/S에 승인 write 권한(③-C).
    - **④ 부트스트랩 = LM 라이선스·Clinic-ID** — 공장 토큰/OOB 미도입. 사람(C/S) 승인이 신뢰 앵커라 Clinic-ID 위·변조 가짜 등록을 현장 검증으로 차단.
    - **⑤ 디바이스 인증 = 비대칭 `private_key_jwt`(ADR-13 · 공유 secret 폐지)** — enroll 키페어(개인키=디바이스 보유)로 서명, GW가 공개키(`device.client_public_key`)로 검증. **공유 client_secret 발급·배포·회전 없음**. 이미 만드는 키페어를 인증에 재사용(자격 일원화). **← 인증 아키텍처 결정이라 보안/CCB 확인 권장.**
    - **확인 포인트**: ①~④ 이대로 확정? · ⑤ private_key_jwt(공유 secret 폐지) 보안 승인? · **재설치 회전도 C/S 승인**으로 충분?
    - **문서 반영 위치**: SRS §2.3.1(단일 흐름)·§7.1.1·§7.2·§7.3·§7.9.2 · ARD §5.1·ADR-13 · OpenAPI(`enroll/complete`=pending+clinic·region 확립 / `PATCH devices`=승인 / `TokenRequest`=private_key_jwt) · DBML(device 통합·`client_public_key`) · 요구사항 FR-ENR-\*·FR-AUTH-01.

- 공유 사항 — 스펙 작성 순서 (SRS PR 이후 후속 스펙)
  - ③ GW SRS(+OpenAPI·DBML)를 한 PR로 baseline. **③ PR 시작(7/9)에 ①·②(One Pager)와 ④(AXS 전체 Sub-SRS, 2주)를 동시 착수**(병행). ③-C·③-P·③-I는 ③ baseline 이후 — **③-I는 GW 1주 초안 → 인프라 담당 완성**. 각 스펙은 **작성 → PR(리뷰·수정) → baseline** 생애주기.
  - 막대 색: **작성=기본 · PR=강조(밝은색) · ◆=baseline/마일스톤 · 회색=완료 · 빨강=외부 선결**. **pilot 8/15는 개발계획서(착수 품의·미승인) 내부 목표**(외부 확정 요구 아님). **AXS sandbox 자격은 스펙 작성엔 불요·E2E·pilot 직전에 필요**라 그 시점에 배치(확보 TBD).
  - **`③ GW SRS + 구현` 섹션에 `GW 구현 1안·2안` 막대를 둘 다 표기 → R7에서 택일.** 1안=④ AXS baseline 후 즉시(스펙 병행) / 2안=전 스펙 완료 후. 둘 다 ④ AXS 연동(첫 연동·테스트 필수) 이후·**기간 미정**(SRS 확정 후 재산정).
  - 어느 제품·단계에 무슨 문서인지는 Roadmap §4 표, 스펙 단위·유형 정본은 PRD §12.1. **본 gantt 정본 = [개발 Roadmap 결정 §3.9](<VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>)** (수정 시 그쪽을 먼저).

  ```mermaid
  gantt
      title 스펙 생애주기(작성→PR→baseline) + GW 구현 — 기간 잠정
      dateFormat YYYY-MM-DD
      axisFormat %m/%d
      todayMarker stroke-width:3px,stroke:#d33,opacity:0.6

      section ③ GW SRS + API/DBML + GW 구현 (계약 SSOT → 구현)
      SRS 본문 작성            :done, srsw, 2026-06-15, 14d
      OpenAPI·DBML 작성·정합   :active, designw, 2026-06-19, 20d
      PR 리뷰·수정(본문+스키마) :active, srspr, 2026-07-09, 14d
      baseline v1.0 (통합)     :milestone, srsbl, after srspr, 0d
      GW 구현 (R7 채택=1안) — ④ AXS baseline 후·스펙 병행 :active, impl1, after axsbl, 45d
      GW 구현 2안(반려) — 전 스펙 완료 후 :crit, impl2, after conbl infbl oidw, 45d

      section ① API 호환성 One Pager (③ PR 시 동시 착수)
      작성                  :op1w, 2026-07-09, 7d
      PR 리뷰·수정          :active, op1pr, after op1w, 7d
      baseline              :milestone, op1bl, after op1pr, 0d

      section ② Presigned One Pager (③ PR 시 동시 착수)
      작성                  :op2w, 2026-07-09, 7d
      PR 리뷰·수정          :active, op2pr, after op2w, 7d
      baseline              :milestone, op2bl, after op2pr, 0d

      section ④ AXS Sub-SRS (③ PR 시 ①②와 동시 착수)
      작성 (전체 Sub-SRS)    :axsw, 2026-07-09, 14d
      PR 리뷰·수정          :active, axspr, after axsw, 14d
      baseline              :milestone, axsbl, after axspr, 0d
      AXS sandbox 자격 확보(E2E·pilot 선결·시점 TBD) :crit, cred, 2026-07-28, 14d
      AXS pilot             :milestone, pilot, 2026-08-15, 0d

      section ③-C GW Console Sub-SRS
      작성                  :conw, after srsbl, 14d
      PR 리뷰·수정          :active, conpr, after conw, 14d
      baseline              :milestone, conbl, after conpr, 0d

      section ③-P 제품 적응 (GW 초안 후 제품팀 인계)
      EzServer 초안         :ezw, after srsbl, 14d
      CleverSpace 초안      :csw, after ezw, 7d
      CleverOne 초안        :cow, after csw, 7d
      OneID 초안            :oidw, after cow, 7d

      section ③-I 인프라 IaC 계획서
      GW 담당 초안          :infw1, after srsbl, 7d
      인프라 담당 완성       :infw2, after infw1, 14d
      PR 리뷰·수정          :active, infpr, after infw2, 14d
      baseline              :milestone, infbl, after infpr, 0d
  ```

- 이월 논의 사항 (6/25 미결 — 계속) | # | 항목 | 타입 | 상태 | | --- | --- | --- | --- | | 4 | Webhook 클라우드 분배(CleverLab 갈래B) | [논의] | v1.0 제외 — Open 후 결정 | | 6 | AXS sandbox 자격증명(Straumann 제공) | [정보] | pilot(08-15) 블로커 — 확보 시점? | | 7 | 경로 B EOS 시점 | [논의] | ① One Pager 확정 의존 | | 8 | v1.0 목표 RPS·동시 세션 | [정보] | 인프라/규모 PL 입력 대기 | | 9 | RTO/RPO·유지보수 윈도우 | [정보] | 인프라 설계 단계 | | 10 | 감사·consent 보존 기간 | [정보] | 법무 확인 대기 | | 11 | 호환성 매트릭스 확정본 | [정보] | ① One Pager 의존 |

# 7/2 주간회의 결정사항

- R1. 라우팅 방식 재평가
  - C안(서브도메인 방식)으로 결정했어. 유지보수/장애대응이 편하고 provider 추가시 인프라 확장은 큰 문제가 아니라고 했어.
  - 이에 Thomas가 걱정이 있어. CleverOne에서 CleverSpace등 Cloud로 가는 모든 통신은 EzServer를 통하는데, EzServer는 nginx로 r-proxy 방식으로 설정하여 어떻게 서브도메인으로 필요한 접속을 하냐는 것이야.
    - 나는 EzServer로 접속해서도 axs.gw.vatech.com으로 접속하도록 할 수 있다고 생각했는데 어때?
    - 그래서 내가 방안을 마련하기로 했어.
  -  C(sub domain) 형태로 가면 CleverOne 에서 EzServer/GW를 통해서 AXS API를 사용하는 방법을 검토한다. 전규현/ Raymond 
    - 방안
      - CleverOne에서 EzServer간은 A방안으로 하고, EzServer와 GW는 C안으로 하는 방안도 있다. (Scott의견)
      - nginx 확장을 구현해서 GW 연결과 내부 API 호출을 분리하는 방안도 있다. (Raymond의견)
      - 아니면 우리가 Rust로 GW를 직접 만드는 방안도 있는데, Thomas는 이미 nginx(+php)로 EzServer를 만들어서 Rust로 새로 개발하면 공수가 크다고 했어.
      - nginx로 간단히 해결 되면 좋고, 이구간에서는 A방안을 써도 되고, 가장 좋은 방법을 찾아야해.
  - 문제가 없는지 어느 방법이 있는지?
- R3. 수집 에이전트 확정
  - Grafana Alloy로 사용한다. 이렇게 SRS에 반영해야 해
  - **→ 반영완료(2026-07-02)**: SRS §1.4 용어·§3.1.2·§6.3.2 수집 에이전트=Grafana Alloy. 앱 계약(stdout JSON+OTel) 불변.

- R4. 프록시(B/C) 에러·타임아웃 정책
  - GW단에서 timeout을 처리하지 않고, infra(istio나 솔루션을 붙여서)에서 조정하므로 추후 결정한다.
  - Provider 연결은 timeout 처리가 필요하다. 다시 정리한다.
  - retry도 istio에서 처리하므로 GW에서 하지 않는다.
  - 서킷브레이커도 infra(istio)에서 처리한다.
  - 따라서, infra에서 제공하는 것은 GW가 할 필요가 없어. GW에서 꼭 지원해야 하는 것들만 남겨서 정리하면 돼. 그 항목의 추천안은 유지하면 돼. 이렇게 SRS 새로 정리해줘.
  - **→ 반영완료(2026-07-02)**: §7.5.4 재작성 — **분담**: ① **GW→provider 연결 timeout(connect 3s·response 10s/AXS SLA·total_deadline<클라, D1~D3)은 GW 책임**(GW가 AXS 등에 직접 연결하는 HTTP 클라이언트라 자기 호출 bound) · ② **재시도·서킷은 istio egress**(D5~D8) · ③ GW 앱레벨=오류 정규화·멱등·취소(D9). DBML/OpenAPI: retry_policy·circuit_breaker만 제거, 연결 timeout 컬럼 유지. Appendix B #25=①값+②istio 분담.

- R5. IaC 도구 확정
  - Terraform으로 확정한다.
    - k8s Deployment는 기능별로 잘게 쪼갠다. (GWcore, Webhook Receiver, Webhook Dispatcher 각각)

- R6. GW SRS 리뷰어 목록 확정 | 영역 | 리뷰 포인트 | 리뷰어 | | --- | --- | --- | | 총괄·승인(CCB) | baseline 승인 | **Scott(실장·총괄,PM)·Raymond(GW 리드)** | | 아키텍처·라우팅 | ADR(특히 ADR-11 R1 재평가)·3-plane·§2 | **Thomas** (외 추가 가능 — 복수 아키텍트) | | 인증·보안 | §7.1·§6.2·§6.5·PHI·데이터 주권 | (보안 담당) — Scott | | 인프라(③-I) | §3.1·배포·EIP·IaC(R5)·환경 구축 | **Jack** | | DB·데이터 모델 | §6.4·DBML·보존기간(#5) | **GW 팀(작성자) = Raymond** — 자체 소유(별도 DBA 없음). 보존기간(#5)만 법무/품질 입력 | | API 계약 | §4·§7·OpenAPI 정합·에러 계약 | **GW 팀(작성자) = Raymond** — 자체 소유(총괄과 동일). *외부* 적합성 검토는 소비자 ③-P | | 제품 적응 ③-P-EZ (EzServer) | 클라이언트·클리닉 등록 주체 영향 | Thomas (담당 1인 이상) | | 제품 적응 ③-P-CS (CleverSpace) | presigned·B 프록시 영향 | 고형용/ Larry | | 제품 적응 ③-P-CO (CleverOne) | 경유 전환 영향 | 탁수용/ Nick | | 제품 적응 ③-P-OID (OneID) | 인증 연계 영향 | 서유진 / Jin | | QA·검증 | §3.6·테스트·호환성 매트릭스 | **정우혁/ James_ES** |
  - **→ 반영완료(2026-07-02)**: SRS §9 Document Approvals에 영역별 리뷰어 표 추가 + §8·§9·Appendix B #10에 **Scott=PM 겸임** 반영.

- R7. 스펙 ↔ GW 구현 진행 전략
  - **1안으로 결정** — ④ AXS Sub-SRS baseline **직후 구현 착수 + ③-C·③-P·③-I 스펙 병행**(2안=전 스펙 완료 후 착수는 납기 지연으로 반려).
  - 구현 시작점=④ AXS baseline(고정, 첫 연동·E2E 필수). 구현 기간=미정(SRS 확정 후 재산정). pilot 8/15는 재검토.
  - 반영: `specs/00-execution-allocation.md` "구현 착수 전략" 섹션 신설 · 위 gantt에 1안 채택 표기.

- R9. 온보딩/enrollment 모델 확인
  - EzServer 에서 private key 분실시 재발급 과정이 필요하다.
  - License 등록과정에서 GW 온보딩을 하게 하는 방안을 검토한다. (최대한 편리하게)
  - EzServer내에서 private 키를 안전하게 보관/백업할 방법이 필요하다.
  - 이런 것이 SRS에 다 반영되었나? 또는 OnePager에서 구체적으로 작성하면 되나?
  - 분실 시 재발급 과정은 GW SRS에 있어야 하지 않나?
  - **→ 반영완료(2026-07-02)**: 상당 부분 이미 SRS에 있었고 '개인키 분실 복구'로 명확화. **분실 복구=재-enroll 회전**(§7.2.7, 유일 경로·백업 복원 없음)·**개인키 백업(export) 미도입**(§7.2.6, 디바이스 비이탈)·**at-rest 안전 보관=EzServer(③-P-EZ) OnePager**·라이선스 등록 시 자동 enroll 편의(§2.3.1). GW SRS에 재발급 과정 있음(§7.2.7).

# VT API Gateway — 7/9 주간회의 Agenda

- 논의 사항 (7/2 결정 → 적용 방법 확정 · 신규 결정 요청)
  - **R1. 무인 장비(EzServer)의 GW 인증 방식 확정 — private_key_jwt(공개키) vs OneID (중요 · 결정·재확인)** — **결론: OneID에는 무인 장비용 머신 인증 수단이 없다 — 사실상 후보가 못 된다. private_key_jwt(공개키)로 확정한다.** 되돌리기 어려운 기반 결정이라 CCB 재확인을 받는다.
    - (결정) 이대로 결정한다.
    - **왜 OneID로는 안 되나** — 무인 장비가 OneID에서 토큰을 받을 grant는 **ROPC(user id/pw를 토큰 엔드포인트로 직접 전송)** 뿐이다(Authorization Code=브라우저·사람 필요, client_credentials=OneID가 제품에만 발급). 그런데 OneID v1.0은 **외부 머신에 ROPC를 제공하지도 않고**(사용자·제품용 IdP), 설령 켠다 해도 **EzServer가 id/pw(=공유 secret)를 저장해두고 자동 로그인**하는 편법이 된다:
      - 10만 대에 **공유 secret 상주·매 로그인 전송** → private_key_jwt가 없애려던 유출면 부활.
      - **ROPC는 MFA 불가**(OAuth 2.1에서 제거된 grant).
      - 고객 IdP에 **device를 사용자 계정으로 등록**(계정계 오염) + OneID **1계정=1테넌트**라 **clinic-less device 불가**(현 전제와 충돌).
    - **private_key_jwt** — enrollment 때 device가 키페어를 생성해 **공개키만 GW에 등록**(개인키 비반출), 이후 서명한 JWT assertion으로 인증. 공유 secret이 없고, 폐기는 GW denylist로 즉시, SE/TPM·DPoP로 v1.1 확장(ADR-01).
    - **비교**:

      | 기준               | **private_key_jwt (추천)**                | OneID (ROPC)                               |
      | ------------------ | ----------------------------------------- | ------------------------------------------ |
      | 자격 성격          | 비대칭 키페어·개인키 비반출·GW엔 공개키만 | 공유 secret(id/pw)을 device에 저장·전송    |
      | 최초 주입          | enrollment 온디바이스 키생성(비밀 배포 0) | 10만 대에 비번 배포·관리                   |
      | MFA                | 해당없음(서명 기반)                       | 불가(ROPC)                                 |
      | 계정 모델          | device=머신 신원                          | 고객 IdP에 device 계정(오염)·1계정=1테넌트 |
      | clinic-less device | 가능(현 전제 유지)                        | 불가(전제 변경 필요)                       |
      | 폐기(kill-switch)  | GW denylist 즉시(§7.2.4)                  | OneID 계정 정지 왕복                       |
      | 리전 주권/장애격리 | GW 리전 로컬 검증                         | OneID 중앙 가용성 종속                     |
      | 표준·미래          | RFC 7523·SE/TPM·DPoP(ADR-01)              | ROPC=OAuth 2.1 삭제·확장 경로 없음         |

    - **"OneID 재사용이 더 싸지 않나"** — 아니다. OneID에 device용 grant/서비스계정을 신설하고 10만 대 비번 배포·계정계 오염을 감수해야 한다. private_key_jwt verify는 GW 설계(§7.1.1)에 이미 반영·외부 의존 0.
    - **결정 = private_key_jwt.** (OneID는 이론상 계정 생성+비번 저장+ROPC 활성으로 구성이야 가능하나, OneID 기능 신설·clinic-less 전제 폐기·보안 격하를 요구해 **실질 불가**. 전제를 바꿔도 공유secret·MFA·계정오염·중앙의존은 그대로라 결론 불변.) **파생**: OneID는 GW 인증에서 제거 → `oneid` upstream·③-P-OID도 데이터 경로 없는 잔재라 제거(내부 프록시 대상=CleverSpace만), OneID는 고객 로그인 제품으로만 잔존(전 문서 정리 완료).
    - **성격**: [결정·재확인] — 이견 없으면 ADR-13(private_key_jwt) 확정. 변경 시 §7.1.1·§2.3.1(enrollment)·DBML(device)·clinic-less 전제 재검토. 근거=OneID SRS §1.2·§2.5.

  - **R2. GW Console 사용자 인증·역할 관리 — MS365/Entra 연동(기본안) vs 자체 DB (결정 요청)** — Console 로그인 사용자 관리 방식을 확정한다.
    - (결정) A방안으로 확정한다.
      - SSO만(Authentication) MS365를 사용하고, 권한관리(Authorization)는 GW 자체적으로 한다.
      - 기본적으로 모든 직원은 로그인은 되지만 권한이 없으면 볼 수가 없다.
      - Admin이 일일이 권한을 부여해야 한다.
      - CS직원은 모든 Clinic의 관리권한이 부여된다.
    - **전제(오해 정정 공유)**: **OneID = 고객(클리닉·랩·개인) 신원 제품**(테넌트=고객). **GW Console 사용자 = 우리 직원**(Admin·현장 C/S)이라 **OneID 대상이 아니다** → Console 사람 인증은 별도 IdP.

      | 기준             | **A. MS365/Entra OIDC 연동 (기본안·추천)** | B. GW 자체 user DB              |
      | ---------------- | ------------------------------------------ | ------------------------------- |
      | 인증             | Entra OIDC(직원 SSO·MFA)                   | GW가 user·비밀번호 관리         |
      | 오프보딩         | **자동**(퇴사=Entra 비활성→접근 차단)      | 수동                            |
      | 비밀번호 관리    | 없음(Entra)                                | GW 부담(리셋·정책·보안)         |
      | 역할(Admin/C-S)  | Entra App Role/Group→토큰 claim            | GW user 테이블                  |
      | 별도 user 테이블 | **불요**                                   | 필요(풀 CRUD)                   |
      | 의존             | Entra 앱 등록(IT 협조)                     | 없음(자립)                      |
      | 구축량           | OIDC 연동                                  | user CRUD·비번·리셋·감사 풀스택 |

    - **역할 관리(A안)**: "누가 Admin/C-S냐"는 **Entra에서 App Role/Group 배정** → 토큰 claim으로 GW RBAC(§7.9.2). **별도 user 테이블 불요.** 인증=Entra, 인가=claim.
    - **하위 결정 — C/S를 담당 클리닉에 한정하나?** 한정하면("C/S X는 클리닉 A·B만 승인") Entra가 그 매핑을 모르므로 **GW에 작은 (operator↔clinic) 매핑 테이블**만 추가(역할은 여전히 Entra). 한정 안 하면 GW 테이블 0.
    - **추천 = A(Entra)**: IdP 재구현 회피·직원 SSO·자동 오프보딩. DBML은 (클리닉 범위 한정 없으면) **무변경**.
    - **확인 필요(Entra 선결)**: (a) **C/S 인력이 Vatech MS365/Entra 디렉터리에 있는지**(현장 설치·해외법인·협력사 직원 포함 여부) — 없으면 게스트 초대/별도 등록 필요 → A안 전제 흔들림. (b) **Entra 앱 등록·App Role/Group·admin consent·redirect URI는 tenant admin 권한**이라 **MS365/Entra 담당(IT)에 요청** 필요(담당자·절차·리드타임 확인). _이 IT 의존은 이점의 대가 — 오프보딩·MFA·비번정책을 IT가 담당._ → Appendix B #40.
    - **성격**: [논의·결정] — A/B 택일 + C/S 클리닉 범위 여부. 확정 시 §7.1.4(사람 인증 재정의)·§7.9.2(RBAC 역할 원천)·§2.3(운영자 로그인 시나리오)·verify 엔드포인트 일반 OIDC화·(조건부)DBML/API 반영. Appendix B #38. **(디바이스 인증 방식(공개키 vs OneID) 결정·OneID 전면 제거 배경은 위 R1 참조.)**

  - **R3. Enrollment 시 수집할 LMP clinic 정보 필드 확정 (논의·결정)** — clinicId만으로 enroll은 되지만 `clinic` 테이블에 id만 있으면 Console에서 사람이 식별하기 어렵다. enroll 때 LMP가 주는 clinic 정보를 함께 받아 record를 보강한다. **회의 결정 = 어느 필드를 수집·저장할지** (저장 구조·API·DB는 이미 반영).
    - (결정) 수집하기로 한다.
      - 하지만 LMP의 Clinic 정보가 바뀌어도, VAG에 sync 하지 않는다.
    - **LMP 제공(원문 확인)**: `licenseapi.yaml` `GET /licenses` 응답 `clinic` = {`name`·`address`·`phone`·`countyCode`(국가 ISO 3166)·`website`}. EzServer가 enroll 시 전달 → GW `clinic` 저장. LMP 변경 시 `PATCH /v1/clinics/{clinicId}`(device 자가 동기화·self-only)로 갱신.
    - **추천안 = LMP가 주는 전부 수집**(name·country*code·address·phone·website) — LMP 응답에 공짜로 함께 오고, 이름·국가=식별, 주소·전화=C/S 연락에 유용, **환자 PHI 아님(clinic 업무정보)**. *(최소안 = name + country*code, 식별만.)*
    - **유의**: LMP `country_code`(clinic 국가) ≠ GW `region`(배포 리전) — 별개 컬럼.
    - **성격**: [논의·결정] — **수집 필드셋만 승인**(추천=전부). DBML(clinic 5컬럼 고정 필드)·OpenAPI(`ClinicInfo`·enroll·`PATCH /v1/clinics/{clinicId}`)·§2.3.1은 **선반영 완료(필드셋 TBD)**. 잔여 확인(EzServer/LMP·③-P-EZ): 신규 클리닉 시 정보 시점·실제 형식.

  - **R4. Enrollment 승인 flow — v1.0 우선순위 (논의·결정)** — enroll 승인에는 **두 flow가 공존**한다(택일 아님 — 둘 다 장기적으로 필요). v1.0에 **무엇을 먼저** 넣을지 정한다.
    - (결정)
      - 이번에는 A안으로 확정한다.
      - 당장 B안을 고려하지는 않는다. 왜냐하면 현재 LMP는 문제가 있어서 LMP 재개발이 이루어질 예정이다.
      - B안은 LMP 재개발이 이루어진 후에 적용할 것이다.
      - SRS에는 B안을 유지할 수 있지만, 추후 LMP 재개발시 적용한다고 명시해줘.
    - **A. C/S 수동 승인** — C/S가 Console에서 승인. **모든 device 커버**(LMP 미등록·비-EzServer 포함) → **항상 필요(보편·fallback)**. LMP 변경 0·지금 동작. 단 설치마다 수동(현장 번거로움 — 이전 회의 우려).
    - **B. 제3자(LMP) 서명 검증 자동승인** — **LMP가 라이선스 검증 후 attestation을 서명("제3자 서명")** → EzServer가 enroll에 실어 전달 → GW가 **LMP 공개키(JWKS)로 검증** → 자동 active(C/S 수동 생략·확장성↑). 단 **LMP 라이선스 등록 device만** 대상.
    - **왜 둘 다**: B가 있어도 **LMP 경로 밖 device**는 A로 승인해야 함 → **A=보편/fallback · B=LMP 등록 device 편의**. 그래서 §2.3.1에 **두 flow 모두 기록**(지원 시점만 TBD).

      | 기준      | **A. C/S 수동 승인** | **B. 제3자(LMP) 서명 자동승인**                           |
      | --------- | -------------------- | --------------------------------------------------------- |
      | 커버 범위 | **모든 device**      | LMP 라이선스 등록 device만                                |
      | C/S 부담  | 설치마다 수동        | 없음(자동)                                                |
      | LMP 변경  | 불요                 | **필요**(제3자 서명 발급·크로스팀·Roadmap 추가·별도 설계) |
      | 검증 키   | —                    | GW가 **LMP JWKS**(런타임 fetch+캐시)로 검증               |
      | 지금 동작 | ✅                   | ❌(LMP 개발 후)                                           |

    - **A/B enroll 승인 시퀀스** (참석자용 · 정본 §2.3.1):

      **A. C/S 수동 승인 (v1.0)**

      ```mermaid
      sequenceDiagram
          autonumber
          participant D as EzServer (디바이스)
          participant GW as GW (Enrollment)
          participant CS as C/S (Console)
          participant DB as clinic·device DB
          D->>GW: POST /v1/enroll/start (LM 라이선스 · Clinic-ID)
          GW->>GW: 부트스트랩 검증 · nonce 발급
          GW-->>D: nonce challenge
          D->>D: 키페어 생성 · nonce 개인키 서명 · 공개키
          D->>GW: POST /v1/enroll/complete (nonceSignature, clientPublicKey)
          GW->>GW: 서명·공개키 검증
          GW->>DB: clinic upsert · device 등록 (status=pending)
          GW-->>D: Accepted (status=pending · 승인 대기)
          CS->>GW: GW Console 승인 (설치 확인 · region 확정)
          GW->>DB: status pending→active
          Note over CS,GW: C/S 수동 승인 = 신뢰 게이트 · 모든 device 커버
      ```

      **B. 제3자(LMP) 서명 자동승인 (gw/1.1+ · 조건부)**

      ```mermaid
      sequenceDiagram
          autonumber
          participant D as EzServer (디바이스)
          participant LMP as LMP (제3자 서명자)
          participant GW as GW (Enrollment)
          participant DB as clinic·device DB
          D->>LMP: 설치 시 라이선스 검증 요청
          LMP->>LMP: Cryptlex 검증 · attestation JWT 서명(clinicId·exp·aud=GW)
          LMP-->>D: 서명된 licenseAttestation
          D->>D: 키페어 생성 · nonce 개인키 서명
          D->>GW: POST /v1/enroll/complete (+ licenseAttestation)
          GW->>LMP: LMP JWKS fetch (미보유·만료 시)
          GW->>GW: JWKS 캐시 · attestation 검증 + 서명·공개키 검증
          GW->>DB: clinic upsert · device 등록 (status=active)
          GW-->>D: Accepted (status=active · C/S 승인 생략)
          Note over GW,LMP: LMP JWKS로 검증(런타임 fetch+캐시) · LMP 경로 밖 device는 A안
      ```

    - **v1.0 결정(택1)**: **A 먼저** / B 먼저 / A+B 동시. **추천 = A 먼저(v1.0) · B는 gw/1.1**(제3자 서명은 바텍 LMP 개발·크로스팀·Roadmap 추가). enroll payload에 `licenseAttestation` optional 예약 완료(B 전환 완충).
    - **abuse 방지(공통)**: rate-limit(IP/서브넷)·미승인 pending TTL 만료·nonce.
    - **검토 후 제외 — C. OneID(클리닉 사용자) 인가**: 클리닉 고객이 OneID 로그인(Authorization Code)으로 enroll을 승인하는 방식도 검토했으나 제외 — ① 여전히 **사람(고객) 개입**이라 B의 무인 자동 이점이 없음(C/S 부담을 고객에 전가) · ② **OneID 커버리지 의존**(미가입 클리닉은 A 폴백) · ③ 라이선스 정당성이 아니라 **'고객 의도'만 증명**(약함) · ④ **'OneID는 GW 미사용' 결정을 되돌려 enroll에 OneID 통합점 부활**. → 무-C/S 순수 원격 self-service 온보딩 수요가 생기면 재검토.
    - **성격**: [논의·결정] — v1.0 우선순위. B 상세(LMP 제3자 서명 개발·claims·JWKS·EzServer 릴레이)=Appendix B #42·B안 설계 One Pager. **확인**: LMP가 제3자 서명 attestation 발급 가능한지(ES 라이선스/ELM 팀).

  - **R5. 라우팅 방식 재평가 방안** — GW edge = **C안(서브도메인)** 확정 · CleverOne→EzServer 내부구간 = **A+C 채택**.
    - (결정) A+C안으로 확정한다.
    - **전제**: GW edge(EzServer→GW) = **C안(서브도메인)** `{target}.gw.vatech.com` 확정(운영/로그/LB/WAF 가시성은 공개 edge에서 확보). 남은 결정 = **내부구간(CleverOne→EzServer)** 에서 target을 EzServer에 전달하는 방식(A/B/C). 표기 = `내부구간 + edge`(edge는 항상 C).
    - **비교 (항목별 · A+C → B+C → C+C)**:

      | 기준 | **A+C (헤더) — 채택** | B+C (경로 prefix) | C+C (내부도 서브도메인) |
      | --- | --- | --- | --- |
      | CleverOne 호출 | `http(s)://<ezserver>/...` + 헤더 `Vatech-Target: axs` | `http(s)://<ezserver>/gw/axs/...` | `https://axs.gw.vatech.com/...` |
      | split-horizon DNS(로컬 DNS/hosts 조작) | **불요** | **불요** | **필요**(또는 forward-proxy) |
      | nginx | **순정** | **순정** | **확장 필요**(CONNECT 모듈 `ngx_http_proxy_connect_module` 또는 Squid/Envoy) |
      | EzServer 헤더 주입·가공(L7) | ◎ 가능 | ◎ 가능 | ✕ (CONNECT 터널이라 통과만) |
      | provider 추가 시 EzServer | **무변경**(제네릭 `$http_vatech_target`) | **무변경**(제네릭 `$target` 경로) | (split-horizon 유지) |
      | CleverOne 변경 | **헤더 1개**(기존 `Vatech-Target` 재활용 → 최소) | URL에 `/gw/{target}/` 경로 규약 신설 | proxy 설정 or DNS 의존 |
      | 기존 결정(ADR-11 `Vatech-Target`) 정합 | **◎ 재활용** | △ 새 규약 | — |
      | HTTP/HTTPS(self-signed) 인바운드 수용 | ◎ `listen 80`+`443` 둘 다 | ◎ 둘 다 | 터널(E2E TLS) |
      | 평문 구간(LAN) 노출 | 평문(토큰/PHI 노출 주의) | 평문(동일) | 터널(암호화) |

    - **결정: `A+C` 채택** — CleverOne→EzServer = **A안(헤더 `Vatech-Target`)**, EzServer→GW = **C안(서브도메인)**.
      - **근거**: split-horizon·nginx 확장 불요(순정) · 헤더 가공 가능 · provider 추가 시 EzServer 무변경 · **기존 `Vatech-Target` 헤더 재활용**(클라 변경 최소·ADR-11 정합). 헤더명 = **`Vatech-Target`**(X- prefix 미사용, RFC 6648).
      - `C+C`는 split-horizon 또는 forward-proxy(모듈)+헤더 불가라 배제 · `B+C`는 되지만 새 URL 경로 규약이라 A보다 열위.
      - **역할 정리**: `Vatech-Target`은 폐기가 아니라 **내부구간 target 지시 키**로 유지 → **EzServer가 서브도메인으로 변환** → **GW edge는 Host/SNI(서브도메인)로 라우팅**. (버전 호환용 `Vatech-*` 식별 헤더는 별도.)
    - **적용 방법 (EzServer nginx — A+C · 순정)**:

      ```nginx
      # 내부(A: Vatech-Target 헤더) → GW edge(C: 서브도메인) 브리징. 순정 nginx.
      resolver 8.8.8.8 1.1.1.1;                        # 변수 proxy_pass 런타임 해석 → 공인 DNS(루프 방지)

      map $http_vatech_target $gw_target {             # target 검증(SSRF 방어)·제네릭
          default              "";                     # 형식 위반 → 빈값
          "~^[a-z0-9-]{1,40}$" $http_vatech_target;    # 소문자·숫자·하이픈만 허용(provider 추가해도 무변경)
      }

      server {
          listen 80;                                   # 평문 HTTP(대부분)
          listen 443 ssl;                              # 자체 HTTPS(self-signed, 켜진 경우)
          ssl_certificate     /etc/ezserver/tls/self.crt;      # 443용(self-signed)
          ssl_certificate_key /etc/ezserver/tls/self.key;

          location / {
              if ($gw_target = "") { return 400; }             # Vatech-Target 없음/형식 위반 → 400
              proxy_pass          https://$gw_target.gw.vatech.com$request_uri;  # C: {target}.gw.vatech.com
              proxy_ssl_server_name on;
              proxy_ssl_name      $gw_target.gw.vatech.com;    # 아웃바운드 SNI
              proxy_set_header    Host $gw_target.gw.vatech.com;# Host(GW가 라우팅)
              proxy_ssl_verify    on;                          # GW 공인 인증서 검증(중간자 방지)
              proxy_ssl_trusted_certificate /etc/ssl/certs/ca-certificates.crt;
              proxy_connect_timeout 3s;                        # (프록시 타임아웃은 §7.5.4/R8)
              # 버전 호환용 Vatech-* 식별 헤더(Product/Version/OS/Clinic-Id/Via)는 그대로 전달
          }
      }
      ```

      - **동작**: CleverOne이 `Vatech-Target: axs` 헤더로 EzServer 호출(평문/HTTPS 무관) → EzServer가 헤더값을 `axs.gw.vatech.com`으로 변환해 **HTTPS로 GW 전달**(HTTP→HTTPS 브리징). EzServer 자체 HTTPS-off와 무관(아웃바운드는 nginx가 클라이언트로 HTTPS 개시, cert 설치 불요).
      - **보안**: 평문 LAN 구간에 토큰/PHI가 실리면 노출 — 민감 트래픽은 그 구간 HTTPS 권장(기존 운영 자세라 별도 판단).

    - **SRS 반영 예정(확정 후)**: ADR-11(라우팅 = **edge 서브도메인** · `Vatech-Target`은 내부 hop 변환 키로 유지) · §4.5.1(`{target}.gw.vatech.com` + `*.gw.vatech.com` 와일드카드 cert + GeoDNS 와일드카드) · §4.1.2(라우팅 방식) · §4.1.4(업로드 target 지정) · webhook 서브도메인과 일관성 명시.

  - **R6. 외부 연동 대상(AXS·CleverSpace 등)의 공식 명칭 확정 — DB·API·Console·커뮤니케이션 공통 용어 (명칭 승인)** — **결정 = GW가 대신 호출·수신하는 외부 연동 서버(예 AXS·CleverSpace)를 부르는 공식 용어**를 정한다. 이 명칭은 **DB 테이블·API 필드·GW Console UI·앞으로의 팀 커뮤니케이션에서 모두 동일하게** 쓰이므로 한번 정하면 파급이 크다(그래서 지금 못박는다). **계기**: 이 대상의 라우팅·아웃바운드 자격·인바운드 webhook 수신을 담던 **3개 표(upstream_registry·connector·webhook_provider)를 1개로 병합**(1:1 facet·중복 토큰·미연결 해소, 등록=1 레코드)하며 **엔터티/용어 이름**을 확정해야 했다. 4개 후보 비교 후 **일단 `upstream`으로 정했다** — 회의에서 최종 승인 또는 변경.
    - (결정) target으로 확정한다.
      - 마켓팅, CS 직원들이 이해하기 쉬운용어다.
    - **이름 후보 비교**:

      | 후보 | 장점 | 단점 |
      | --- | --- | --- |
      | **`upstream`(채택)** | 회의 어법 그대로(_"신규 upstream=레지스트리 1행"_)·업계 표준(GW가 라우팅하는 backend)·내부/외부 backend 다 포괄·클라이언트(CleverOne) 자연 배제·컴포넌트(External Connector)와 충돌 없음 | 인바운드 webhook facet엔 살짝 아웃바운드 뉘앙스 |
      | `target` | 문서 어휘(target-routed proxy·`Vatech-Target`)와 일치 | 회의에선 target=라우팅 키(헤더값), upstream=서버로 구분 → 엔터티엔 upstream이 정확 |
      | `integration`(연동) | 양방향·내부/외부 다 포괄·"연동" 자연 | 회의 미사용·다소 추상적 |
      | `provider` | 익숙(webhook에서 유래) | **webhook 유래뿐**·CleverSpace 등 내부 backend엔 부적합·OAuth "provider"와 과적재 |

    - **확정(잠정)**: 표명=**`upstream`**(엔터티), PK=**`target_id`**(=Vatech-Target 값=서브도메인 라벨). FK(org_mapping·webhook_event·policy)=`target_id`. "CleverSpace를 등록한다 = **upstream 1 레코드 추가**"로 표현.
    - **SRS 반영 완료**: DBML(Table `upstream`)·OpenAPI(`Upstream`·`/admin/v1/upstreams`)·db-jsonb(#upstream)·redis(`gw:cache:upstream`)·SRS §6.4·§7.5·§7.6·§7.9·§2.3.4·ERD·API명세·③-C·ARD 전부 정합.
    - **이번 회의에서 다른 이름으로 바뀌면** 그때 일괄 재반영(단순 rename). 결정만 주면 됨.

  - **R7. Webhook payload(환자정보 PHI 포함 가능) 저장·보존·접근 방식 결정 (중요)** — `webhook_event`가 수신하는 이벤트 **본문(payload)** — AXS `patient.created` 등 **환자정보(PHI) 포함 가능** — 을 **어디에(위치)·얼마나(보존기간)·어떻게 보호(마스킹·접근통제)** 보관할지 확정. (PHI라 컴플라이언스에 직결되는 게 이 안건의 무게.)
    - (결정) 일정기간 보관한다.
      - S3가 아니고 DB에 보관한다.
      - 보관할때는 복호화가능하도록 암호화해서 저장한다.
      - GW console에서 조회할 때 환자정보는 masking 해서 표시한다.
      - 삭제는 당분간 고려하지 않는다.
    - **배경(references 스펙 확인 결과)**:
      - v1.0 webhook 소스 = **AXS 단독**(CleverSpace=webhook 대상 아님 확정 · CleverLab=갈래B 보류).
      - AXS payload = **JSON**, 수 KB(알림 메타데이터 — 큰 영상은 webhook 아님·presigned). **환자 PHI 포함**: `patient.created/updated`에 이름·생년월일·성별·patientId, file 이벤트에 storageUri·파일메타.
      - GW는 payload를 **opaque·verbatim**(해석·수정 안 함)으로 다루며, store-and-forward 버퍼는 이미 **SQS(리전 로컬)**.
    - **핵심 논점**: 쟁점은 "payload가 너무 큰가"가 **아니라** "**payload에 환자 PHI가 들어온다**"는 점. GW 대전제(§6.4 "GW는 PHI 미저장")를 **"webhook에서는 PHI를 전이(transient) 경유하고 persist를 최소화한다"** 로 정교화해야 함(리전 로컬·암호화·짧은 TTL·복제 금지·콘솔 비노출).
    - **결정 항목 (3)**:

      | #    | 결정 항목                       | 옵션                                                               | **추천안**            |
      | ---- | ------------------------------- | ------------------------------------------------------------------ | --------------------- |
      | R7-1 | dispatch 후에도 payload를 보관? | (a) **일정기간 보관**(디버깅·재생·감사) / (b) SQS 전이만·사후 폐기 | **(a) 일정기간 보관** |
      | R7-2 | 보관 장소                       | **S3(리전 로컬·참조)** vs PG DB(jsonb 컬럼)                        | **S3**                |
      | R7-3 | Console 상세 뷰의 환자정보      | **redact(마스킹)+접근통제** vs 원문 노출                           | **redact+접근통제**   |

    - **R7-2 비교 (S3 vs DB) — 추천 = S3**:

      | 기준 | **S3(리전 로컬·참조) — 추천** | PG DB(jsonb 컬럼) |
      | --- | --- | --- |
      | PHI/데이터 주권 | 리전 로컬·SSE 암호화·TTL·**복제 안 함** → 안전 | 통제 DB에 PHI 상주. **글로벌 복제 시 국경 넘김**·리전 로컬이어도 PHI scope 확대 |
      | Console 검색/필터 | 메타데이터(이미 `webhook_event` 컬럼: provider·clinic·state·eventType·기간)로 **충분**, 본문은 단건 fetch | 본문 내부 검색까지 가능 = **환자 신원 검색 = PHI 부채**(원치 않음) |
      | payload 포맷 | **무관**(blob — 미래 비-JSON provider 수용) | **JSON 가정**(opaque 철학과 상충) |
      | 보존 관리 | lifecycle 규칙 **자동 TTL**·암호화 기본(관리형·부담 적음) | 수동 정리 잡 필요 |
      | 단순성 | claim-check 참조·orphan 관리(경미) | 원자적·단일 저장소(가장 단순) |
      | 대전제 정합 | **"GW는 PHI 미저장" 유지**(전이만) | 대전제 약화 |
      - **추천 근거 요약**: payload가 **환자 PHI**를 담고 GW가 **opaque(포맷 무관)** 로 다루므로, **검사 안 한 외부 PHI를 복제되는 통제 DB에 원문 저장하지 않는다**가 핵심. Console 요구(검색/필터)는 **PHI-free 메타데이터 컬럼으로 이미 충족**되고, 본문은 단건 조회(참조 fetch)로 족하다. "S3가 번거롭다"는 우려는 SQS가 이미 in-flight 본문을 들고 있고 S3 lifecycle이 자동이라 실제 부담은 작다.
      - **DB(jsonb)가 정당화되는 조건**: `webhook_event`가 **엄격히 리전-로컬(비복제)** 이고 조직이 리전 PG의 PHI 보관을 허용하며 최대 단순성/검색성을 원할 때 — 절충 대안(짧은 TTL·접근통제 필수).

    - **R7-1 보존기간(TTL)**: 디버깅·재생·감사 목적이므로 **짧게**(초안 예: 7~30일). 정확한 값은 감사·consent 보존정책(Appendix B #5)과 함께 확정.
    - **R7-3**: redact = Console 화면 표시 시 환자정보 **마스킹**(전달 본문은 verbatim 불변). 운영자 디버깅은 허용하되 환자 신원 불필요 노출을 막는 데이터 최소화(§6.4). 접근통제 = 역할(Admin/C-S)별 payload 열람 권한.
    - **SRS 반영 예정(확정 후)**: DBML `webhook_event.payload_ref` 주석(본문=리전 S3·claim-check 참조·관계형 DB 미저장) · **`event_type` 컬럼 추가 검토**(Console 필터) · §6.4(webhook PHI 전이·최소 persist로 정교화) · §7.6(store-and-forward 본문 보관·TTL) · Appendix B(보존기간·본 결정 로그).

  - **R8. [조사] 호주 AXS 연동 실태 — 시나리오(A/B/C)·Org-ID 취득 경로 (이번 회의 확정 불요)** — AXS webhook 분배·아웃바운드 호출의 라우팅 키인 **외부 Org-ID(Straumann Organization-ID)를 각 클리닉이 어떻게 갖게 되는가**와, 호주 현장에 **어떤 시나리오가 실제 존재하는가**를 확인한다. GW는 `org_mapping`(로컬 매핑)만 채우지만, 그 전에 "그 클리닉의 AXS 조직이 우리 연동과 연결돼 Org-ID가 존재"해야 하는데 그 취득 경로가 미확인이다(§2.3.4 「연동 링크·org_mapping 생애주기」는 GW 공통 레일만 규정).
    - (결정) A,B,C case를 우리가 전부 cover 한다.
      - 가입 API를 활용한다.
      - 우리가 Straumann 가입도 한다. 이때 필요한 정보는? AXS 문서를 보고 필요한 정보를 개발자(나)에게 알려줘야 한다. 스펙에 기입되어야 한다.
      - 우리가 AXS 가입도 한다. 이때 필요한 정보는? AXS 문서를 보고 필요한 정보를 개발자(나)에게 알려줘야 한다. 스펙에 기입되어야 한다.
    - **① 시나리오 (클리닉 전제 상태)**:

      | 상태  | Straumann 가입(`customerNumber`) | AXS org 존재 | 온보딩이 해야 할 일                                                                         |
      | :---: | :------------------------------: | :----------: | ------------------------------------------------------------------------------------------- |
      | **A** |                ✓                 |      ✓       | Vatech 이미 연동이면 **org-binding만** / 아니면 `link`→동의→org-binding                     |
      | **B** |                ✓                 |      ✗       | **AXS org 확보**(생성·개통 방식=확인 대상) → `link` → org-binding                           |
      | **C** |                ✗                 |      ✗       | **범위 밖** — Straumann 가입은 클리닉↔Straumann 영업 과정(우리 SW 무관) · 가입하면 B로 합류 |
      - **C 취급(권고)**: 전제 미충족이라 AXS 연동 자체 불가(AXS=Straumann 플랫폼). flow로 만들지 않되 **"범위 밖·가입 시 B 수렴"으로 경계만 명시**(추후 "비고객은?" 재질문 차단).
      - **opt-in 전제(중요)**: AXS 연동은 **선택** — **가맹(A/B)이어도 연동 안 하는 클리닉은 `[3]` 자체를 건너뜀**(org*mapping 없음·enroll 등 정상·새 처리 불요). 위 A/B/C는 *연동하는\_ 클리닉의 전제 상태다. 조사 시 **"연동 안 함" 비율**도 함께 파악하면 EzServer가 link flow를 얼마나 자주 타는지 가늠에 도움.

    - **② 묻는 것 (조사 질문)**: A/B/C **분포**(대부분 A? B 상당? C 무시 가능?) · **B의 AXS org 확보 방식**(`link`가 자동 생성/개통 vs Straumann 별도 개통 — 핵심 미지) · A의 **Vatech 기연동 여부** · `customerNumber` **취득 경로**(설치 입력/LMP/포털·_“Straumann 고객이면 있다”는 가정_) · consent 주체·타이밍.
    - **③ 상태 B(연결 필요) 절차는? (어디서·누가·어떤 UI)**:
      - AXS **별도 콘솔/포털**에서 조직 담당자가 발급·동의하는가? (out-of-band)
      - **GW가 AXS API로** 대행하는가? — _우리 조사(AXS Organization API)_: `POST /v1/organization/integration/link`(`customerNumber` + 우리 Client ID) → `organizationId` + **조직 관리자 동의**(status `PENDING`→`APPROVED`). 즉 **조직 자체는 Straumann 고객**이고 우리는 그 조직에 우리 연동을 **"연결(link)"** 만 한다(생성 아님). 보조 API `.../check`(연결 확인)·`.../unlink`(해제)·`.../{customerNumber}/info`(region·country).
      - **EzServer Console에서** 그 연결을 트리거하는 **UI를 제공**해야 하나? (customerNumber 입력·동의 상태 표시·완료 시 org-binding 자동 등록 등)
    - **부가 요청**: Straumann과 **계약·sandbox 제공 시 Tech support(기술 질의) 채널**도 함께 확보 요청 — 위 절차·동의 흐름·`customerNumber` 취득 방법은 Straumann에 직접 확인해야 정확하다. (AXS sandbox 자격은 이월 #6과 연계)
    - **④ 누가·언제까지·회신처**: **드라이브=Raymond(GW 리드)** · 입력원=**호주 영업/현장·Straumann 파트너십 담당**(계약·연동 실태)+**EzServer팀(③-P-EZ)**(customerNumber 취득). **회신처=④ `_status` TBD**.
    - **⑤ 비차단·기한**: **GW API는 이미 A/B 모두 수용**(org-bindings 수렴 + 미연동의 `link`=프록시 레일·**신규 GW 엔드포인트 불요**) → **GW baseline 안 막힘**; 막히는 것 = **EzServer AXS flow(③-P-EZ)·④ 집필**. 따라서 **④ 집필·EzServer AXS 착수 전(= AXS pilot 8/15 역산·7월 말 sandbox 자격 확보 전)** 회신.
    - **성격/산출**: [정보·조사] — **이번 회의 확정 불요**, 정할 것은 **"누가·언제까지 알아오나"**. 확정 시 **④ AXS Sub-SRS**에 구체화(상태 A/B/C 판정·링크 트리거 주체·UI 소유). **미확정 시 차주 이월**(아래 이월 논의 사항에 등재 예정). 근거: 참조-카탈로그 §3 AXS_docs `organization.yml`·Integration_guide + `references/Straumann연동/AXS_docs/openapi/organization.yml`(link/check/unlink/info·consent PENDING→APPROVED).

  - **R9. 호환성 매트릭스 저작·배포 구조 확정 — 원본 YAML → CI → 서빙 JSON (SSOT·앱 배포와 분리) (2건 · 추천안 있음)** — GW가 공시하는 버전 호환성 매트릭스(§7.7.2·§7.7.5)의 **저작·배포 구조**를 확정한다(런타임 게이팅 로직 아님). **현재 설계 = 원본 `compat-matrix.yaml`(git·PR 편집·SSOT) → CI 컴파일 → env별 `server-configuration.json` 생성 → S3 발행 → GW 런타임 read+cache**(앱 재배포와 분리). 이 **YAML→JSON 2단계 컴파일**은 전제로 두고, 아래 **2건**(소스 repo·CI 토폴로지 / 원본 포맷)만 결정한다. (샘플=`design/well-known/`·S3 참조.)
    - (결정) aml 로 관리하고 secret manager 에 등록해서 관리한다. (S3에 저장하지 않는다)
      - azure pipeline에서 AWS CLI 를 사용해서 yaml을 json으로 변경해서 등록한다.
      - yaml은 vt-api-gateway repo에서 관리한다.

    - **결정 1 — 소스 repo 위치 + CI 토폴로지** (추천 = **A. `vt-api-gateway` 단일 repo + path-scoped**)

      | 기준 | **A. vt-api-gateway 단일 repo + path 분기 (추천)** | B. 신규 config 전용 repo | C. 기존 es-gitops 재활용 |
      | --- | --- | --- | --- |
      | 관리 부담 | 작은 발행 잡 1개 추가(검증→렌더→S3)·**path 분기는 CI 1급 기능** | repo 신설·CI 셋업 별도(한 파일 위해 과함) | 신설 없음(기존 GitOps) |
      | 관심사 분리 | path로 논리 분리 | 물리 분리(가장 깔끔) | 물리 분리 |
      | 오너십 | **GW팀 단일** | GW팀(새 repo) | **인프라(Jack) — 앱데이터 혼재·경계 흐림** |
      | 앱 재배포 회피 | ◎ `config/**` 제외 | ◎ 애초 분리 | ◎ 분리 |
      | 앱+매트릭스 동시 변경(1 PR) | ◎ 원자적 가능 | △ cross-repo | △ cross-repo |
      | 신규 repo | 불요 | 필요 | 불요 |
      - **추천 근거(A)**: 발행 잡이 작고(검증+렌더+S3 업로드) path 분기가 표준이라 **단일 repo가 가장 단순·저비용 + GW팀 단일 오너십**. "두 개의 대등한 CI"가 아니라 **큰 배포 파이프라인 1개 + 작은 발행 잡 1개**다. 강한 물리 분리가 꼭 필요하면 **C(es-gitops·신설 없음)** 가 차선이나 인프라 repo에 앱데이터가 섞임. **B(신규 repo)는 파일 하나 위해 과함.** 최종 CI 토폴로지는 **③-I(인프라) 소유**.

    - **결정 2 — 원본 포맷 YAML vs JSON** (추천 = **YAML**) — _2단계 자체는 확정, 원본 포맷만 택일._

      | 기준                        | **YAML (추천)**            | JSON        |
      | --------------------------- | -------------------------- | ----------- |
      | 주석("이 하한 버전인 이유") | ◎ 가능(감사·인수인계)      | ✕ 불가      |
      | 편집성                      | ◎ 노이즈 적음              | △ 쉼표·괄호 |
      | 포맷 수                     | 원본 yaml / 서빙 json(2종) | 1종(json)   |
      | 서빙본과 형태               | 다름(컴파일)               | 거의 같음   |
      - **추천 근거**: 매트릭스는 "왜 이 버전이 하한인가"를 주석으로 남기는 가치가 크고, §7.7.3 3단계 정책 등 **풍부한 저작 모델**을 담기 좋아 **YAML**. 단일 포맷을 선호하면 JSON 원본도 유효(생성 단계는 동일하게 필요).

    - **성격/산출**: [논의·결정 요청] — 결정 1=방향(단일 repo) 승인(최종 토폴로지는 ③-I) · 결정 2=택일. 확정 시 §7.7.5·Appendix B #8 반영. _(값·3단계 스키마 확정은 ① One Pager 소관, 별개.)_

  - **R10. GW 배포 토폴로지 — 관리(admin) API를 별도 Deployment로 분리할지 (3-way → 4-way) (결정 요청 · 추천 = 4-way)** — 7/2 R5에서 GW 소프트웨어(**단일 코드베이스**)를 **기능별 Deployment**로 쪼개기로 확정했다(현 **3-way**: `GW core` · `WH Receiver` · `WH Dispatcher`). 그런데 **운영자·Console용 관리 API(`/v1/admin/*`)가 지금은 `GW core` 안에 포함**돼 있다. 이 admin API를 **별도 Deployment(`Admin API`)로 떼어 4-way로 갈지** 정한다. **이는 배포/네트워크 토폴로지 결정이며, API 계약(`/v1/admin/*` 경로)은 어느 쪽이든 불변**이다(데이터도 PostgreSQL을 공유 — 서비스·데이터 분리가 아니라 배포·노출면 분리).
    - (결정) admin 과 core는 분리한다. 4way로 결정한다. 이에 따라서 SRS에 관련된 부분을 모두 수정한다.

    - **왜 admin이 다른가**: 트래픽 = 운영자 **일/주**(사람·저볼륨) · 노출면 = **내부/Console 전용**(공개 device edge·webhook 호스트에서 도달 금지) · 권한 = **kill-switch·config publish·payload break-glass(PHI 열람)** 등 최고위험. device 인증·target proxy hot path(머신·대량·공개)와 프로파일이 근본적으로 다르다 → **제어평면(admin) / 데이터평면(proxy·webhook) 분리**는 게이트웨이 표준 패턴.

    - **회의 입력(중요)**:
      - **인프라 담당 의견**: K8s에서 **Deployment 단위는 작을수록 좋다**(독립 스케일·롤링 업데이트·리소스 격리·블라스트 반경 축소) → **4-way 유리**.
      - **되돌리기 비용(lock-in)**: 지금 3-way로 합쳐 두고 **나중에 4-way로 쪼개면**, 그때는 **코드 결합 해소 + 배포 토폴로지 재검증(IEC 62304 통제 소프트웨어)** 비용이 든다. 계약은 안 바뀌어도 프로세스·검증은 다시 해야 하므로 **처음부터 4-way가 안전·저렴**.

    - **제안 토폴로지(4-way)** — admin을 내부 전용 노출면으로 격리:

    ```mermaid
    flowchart TB
        subgraph PUB["공개 노출면 (외부 도달)"]
          CORE["GW core<br/>device 인증·target proxy·enroll·well-known"]
          WHR["WH Receiver<br/>webhook 수신·HMAC·ACK"]
        end
        subgraph INT["내부 전용 노출면 (Console·VPC 내부)"]
          ADM["Admin API (← 분리 대상)<br/>/v1/admin/* · operator(Entra) · kill·config·break-glass"]
          WHD["WH Dispatcher<br/>SQS consumer·클리닉 분배"]
        end
        DEV["EzServer 디바이스<br/>100k·머신"] --> CORE
        UP["AXS 등 upstream"] -->|webhook| WHR
        OPR["운영자 Console<br/>일/주·사람"] --> ADM
        WHR --> Q[("SQS")] --> WHD
        CORE --- DB[("PostgreSQL · 공유")]
        ADM --- DB
        WHR --- DB
        WHD --- DB
    ```

    - _현재 3-way_: 위 `Admin API` 박스가 **`GW core` 안에 포함**(admin이 device/proxy와 같은 **공개 노출면·같은 프로세스**). _4-way_: `Admin API`를 떼어 **내부 전용**으로.

    - **항목별 비교 (3-way vs 4-way)**:

      | 항목 | 3-way (admin ⊂ core) | 4-way (admin 분리) | 유리 |
      | --- | --- | --- | --- |
      | 스케일 | admin 저볼륨이라 무방 | admin 최소 파드 상주 | — (스케일은 결정 근거 약함) |
      | 노출면·보안 | admin이 공개 core와 동거 → 내부전용 격리 어려움 | admin **내부전용 ingress·NetworkPolicy** 분리 | **4-way** |
      | 블라스트 반경 | device hot path 장애·공격이 admin에 파급 | 특권 admin 격리(상호 차단) | **4-way** |
      | 배포 케이던스 | Console 기능 변경마다 core 재배포 | admin 독립 배포(core 안정 불교란) | **4-way** |
      | 운영 무빙파츠 | Deployment 3개 | 4개(같은 이미지·한계비용 소소) | ○ 3-way(소폭) |
      | 인프라 비용(컴퓨트) | admin이 core 파드에 흡수 → 추가 ~0 | 전용 파드(HA 최소 2·**저사양**·admin 저QPS) 상시 → **소액↑** | ○ 3-way(소폭·**delta 작음**) |
      | 인프라 선호(작은 단위) | 큰 단위 | **작은 단위**(인프라 권장) | **4-way** |
      | 향후 변경 용이성 | 나중 분리 시 결합 해소+재검증 필요 | 이미 분리(전환 비용 0) | **4-way** |
      | IEC 62304 재검증 | 3→4 전환 시 토폴로지 재검증 1회 발생 | 지금 1회로 끝 | **4-way** |
      | API 계약 영향 | 없음 | 없음 | — |

    - **추천 = 4-way(admin 분리)**. 대가는 **Deployment +1(운영 항목 소폭↑) + 전용 파드 소액 컴퓨트 비용**인데, **같은 코드베이스·이미지**라 한계비용이 작고(admin 저QPS라 파드도 저사양), **인프라가 작은 단위를 선호**하며, **나중 분리 시의 재검증 비용을 회피**한다. 핵심 근거는 스케일·비용이 아니라 **보안 노출면·블라스트 반경·재검증 회피**이고, 비용 델타는 이 이점을 뒤집을 만큼 크지 않다.
    - **성격/산출**: [논의·결정 요청] — 4-way 승인 시 §2.1.1 서술·다이어그램·Appendix B #26(배포 단위)·③-I IaC(Deployment/ingress/NetworkPolicy)에 반영. **최종 배포 토폴로지는 ③-I(인프라) 소유**(R9 CI 토폴로지와 동일 원칙).

  - **R11. [신규 기능] 클라이언트 SW 인벤토리 — 클리닉별 설치 SW 버전·OS 가시성 (기능 추가 확인 + `Vatech-Instance-Id` 도입 여부 결정)** — "각 클리닉에 어떤 제품·버전이 깔려 있는지" 파악난이 **오랜 숙원**이었다. GW가 이미 **전 요청 필수로 받는 `Vatech-*` 헤더**(FR-COMPAT-01·§7.7.1: `Vatech-Product`·`Version`·`OS`·`Clinic-Id`)를 **영속(persist)** 하면 **추가 수집 없이** 클리닉별 SW 인벤토리를 만들 수 있다. **이미 ③ SRS(§7.8.5·FR-FLEET-06)·DBML(`client_inventory`)·API(`GET /v1/admin/clinics/{clinicId}/clients`)에 반영**했고, 본 안건은 (1) 기능 추가 확인 + (2) 미래 정밀 식별 헤더 결정이다.
    - (결정) 이 기능을 GW에 넣는다.
      - 단, 이 기능은 정식으로 추후 개발되는 새로운 LMP에 들어갈 기능이다. LMP는 update 기능도 있으므로 궁합이 더 잘 맞는다.
      - 하지만 GW에는 이 기능을 간이로 넣는다. 새로운 LMP 이전에 충분히 역할을 할 수 있다.
      - 식별을 위한 Instance-ID는 고려하지 않고 일단 수집한다.
        - (참고) EzServer는 Scan 기능을 이용해서 Clinic 내의 client PC를 수집하고 HW 고유 정보를 이용해서 식별 정보를 모으고 있다. 하지만 이정보를 중앙에서 집중 관리하는 기능은 없다. 추후 신규 LMP에서 제대로 수집 관리를 할 예정이다.
          - EzServer Client 식별 정보가 있어도 GW 호출시 어느 client가 호출한 것인지는 알기 어려워서 현재는 이 정보 활용이 어렵다.

    - **동작**: `CleverOne → EzServer → GW` 체인에서 GW가 보는 **originator SW**(CleverOne 등)를 관측·기록. EzServer 자신은 device(heartbeat 버전·OS). **Console**: Clinic 선택 → EzServer 정보 + **앞단 클라 목록(버전·OS)**.
    - **식별 id 없음 전제**: 앞단 클라는 안정 식별자가 없다(헤더에 instance-id 없음·GW의 peer는 EzServer라 클라 IP 미가시). → **(clinic, product, version, os) 튜플 + last_seen**. 버전 업 = 새 튜플·옛 튜플 정체(업그레이드/제거 추정). **버전 presence는 얻지만 설치 대수는 못 센다.**
    - **비용**: 헤더는 이미 오므로 캡처가 저렴(요청마다 쓰지 않게 Redis seen-set throttle). 클라 주장값이라 **관측용(authz 아님)**·PHI/PII 없음.

    - **결정 2건**:
      1. **기능 추가 승인** — 위 v1.0 캡처 + 조회 API 포함(리치 Console 대시보드는 ③-C). _(반대·범위 조정 의견 수렴.)_
      2. **미래 표준 헤더 `Vatech-Instance-Id` 도입 여부** — 클라가 생성하는 **안정 install GUID**를 헤더 표준에 추가할지. 도입 시 per-instance 인벤토리·**정확한 설치 대수**·정밀 업그레이드 추적이 가능하나 **전 제품 클라이언트 변경**(공용 라이브러리·① One Pager·③-P)이 필요. **도입 안 함도 유효**(튜플 presence로 충분하면).

      | 관점       | 튜플 모델 (현재·id 없음)                    | +`Vatech-Instance-Id` (미래)              |
      | ---------- | ------------------------------------------- | ----------------------------------------- |
      | 얻는 것    | 클리닉별 **버전 presence**·구버전 잔존 여부 | + **정확 설치 대수**·per-instance 추적    |
      | 정확도     | last_seen recency(제거 추정)                | 인스턴스 확정(정밀)                       |
      | 클라 변경  | 없음(기존 헤더 재사용)                      | **전 제품 클라 변경**(헤더 부착)          |
      | 프라이버시 | product/version/os만                        | install GUID 추가(단말 식별성↑·정책 검토) |
      | 비용·시점  | v1.0 즉시                                   | gw/1.1+·표준 협의                         |

    - **성격/산출**: [기능 추가 확인 + 결정] — (1) 승인 시 현행 반영 유지(§7.8.5·`client_inventory`·조회 API·③-C UI) · (2) `Vatech-Instance-Id` **도입/미도입** 결정 → 도입 시 ① One Pager 헤더 표준·③-P 클라 반영·gw/1.1 인벤토리 확장, 미도입 시 튜플 모델 확정(§7.8.5에 결론 기록). Appendix B #48.

- 공유 사항 (결정 아님 · 정보 공유)
  - **S1. GW→각 EzServer(클리닉) 범용 하행(downlink) 레일 확보** — webhook 역방향 분배를 위해 만든 **MQTT 하행 채널**(EzServer가 방화벽 뒤에서 outbound 지속 구독, §7.6.6)은, 사실상 **중앙(GW)에서 각 클리닉 edge로 능동 전달하는 최초의 수단**이다. 토픽을 `gw/clinic/{clinicId}/{stream}` 로 두어 **`{stream}` 확장점을 예약**했다(EzServer는 `#` 구독·미지 stream 무시·forward-compat).
    - **지금**: `webhook`(AXS 이벤트 분배) **하나만 구현**.
    - **미래 활용 가능(예약·미구현)**: `announce`(클라이언트 새 버전 설치 안내·프로모션·공지) · `command`(kill-switch 등 즉시 명령) · `config`(원격 설정 하달) 등. 새 용도는 **발행자 추가만**으로 수용(레일·EzServer 구독 불변).
    - **의미**: 지금은 안 쓰더라도 **"중앙에서 fleet으로 뭔가 내려보내는" 다양한 미래 수요를 무구조변경으로 담을 레일**을 확보. 확장점 예약 비용≈0, 기능은 미구현(YAGNI 준수).
    - **결정 필요 없음** — 공유만. 구체 활용(공지/명령 등)은 수요 발생 시 별도 안건화.

  - **S2. 프로젝트 일정(Gantt) — 주간 참고 스냅샷** — 스펙 생애주기(작성→PR→baseline)+GW 구현 타임라인. **정본=[개발 Roadmap 결정 §3.9](<VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>)** (수정은 그쪽 먼저). 아래는 7/9 기준 스냅샷 — 매주 최신본으로 갱신.
    - (결정) Gantt 및 담당자로 수정하기로 했어.
      - AXS연동은 당장은 CleverOne은 고려하지 않고, Straumann의 IO Scanner 만 1차로 고려한다.
        - IO Scanner와 EzServer 연동 방식은 아직 정해지지 않았다. 추후 정해질 예정.
        - 이를 고려하여 먼저 작성할 Spec을 먼저 완료한다. 관련 없는 Spec은 최대한 뒤로 미룬다.
        - 이 내용은 SRS의 1.2에도 언급이 되어야 하고(우선 개발할 내용) 2.7에도 적용해야 해.
          - v1.0에는 IO Scanner 연동만 들어가는 거지.
          - CleverOne 연동은 v1.0 이후 버전에 적절한 곳에 넣으면 돼.
      - 아래 제품의 Spec은 내가 초안을 쓰지 않고 개발 담당자가 직접 작성한다. 나는 GW 스펙을 제공하여 표준만 알려주면 된다.
        - CleverOne Spec 은 담당자(Nick)가 작성한다.
        - EzServer Spec 은 Thomas가 작성한다.
      - Straumann 연동 목표일정은 협의중인데, 잠정적으로 10월 중으로 한다.
        - 일단 10월안에 출시 가능한 일정으로 역산하여 Gantt를 업데이트 한다.
        - 나는 SectionView 프로젝트를 병행 진행해야 해서 100% 투입은 어려워. 이것도 고려해줘.
    - 막대 색: 작성=기본 · PR=강조 · ◆=baseline/마일스톤 · 회색=완료 · 빨강=외부 선결. **③ GW SRS PR 시작=7/9**. 구현=R7 **1안**(④ AXS baseline 후·스펙 병행)·기간 미정(SRS 확정 후 재산정). pilot 8/15는 재검토(R7).

    ```mermaid
    gantt
        title 스펙 생애주기(작성→PR→baseline) + GW 구현 — 기간 잠정
        dateFormat YYYY-MM-DD
        axisFormat %m/%d
        todayMarker stroke-width:3px,stroke:#d33,opacity:0.6

        section ③ GW SRS + API/DBML + GW 구현 (계약 SSOT → 구현)
        SRS 본문 작성            :done, srsw, 2026-06-15, 14d
        OpenAPI·DBML 작성·정합   :active, designw, 2026-06-19, 20d
        PR 리뷰·수정(본문+스키마) :active, srspr, 2026-07-09, 14d
        baseline v1.0 (통합)     :milestone, srsbl, after srspr, 0d
        GW 구현 (R7 채택=1안) — ④ AXS baseline 후·스펙 병행 :active, impl1, after axsbl, 45d

        section ① API 호환성 One Pager (③ PR 시 동시 착수)
        작성                  :op1w, 2026-07-09, 7d
        PR 리뷰·수정          :active, op1pr, after op1w, 7d
        baseline              :milestone, op1bl, after op1pr, 0d

        section ② Presigned One Pager (③ PR 시 동시 착수)
        작성                  :op2w, 2026-07-09, 7d
        PR 리뷰·수정          :active, op2pr, after op2w, 7d
        baseline              :milestone, op2bl, after op2pr, 0d

        section ④ AXS Sub-SRS (③ PR 시 ①②와 동시 착수)
        작성 (전체 Sub-SRS)    :axsw, 2026-07-09, 14d
        PR 리뷰·수정          :active, axspr, after axsw, 14d
        baseline              :milestone, axsbl, after axspr, 0d
        AXS sandbox 자격 확보(E2E·pilot 선결·시점 TBD) :crit, cred, 2026-07-28, 14d
        AXS pilot             :milestone, pilot, 2026-08-15, 0d

        section ③-C GW Console Sub-SRS
        작성                  :conw, after srsbl, 14d
        PR 리뷰·수정          :active, conpr, after conw, 14d
        baseline              :milestone, conbl, after conpr, 0d

        section ③-P 제품 적응 (GW 초안 후 제품팀 인계)
        EzServer 초안         :ezw, after srsbl, 14d
        CleverSpace 초안      :csw, after ezw, 7d
        CleverOne 초안        :cow, after csw, 7d

        section ③-I 인프라 IaC 계획서
        GW 담당 초안          :infw1, after srsbl, 7d
        인프라 담당 완성       :infw2, after infw1, 14d
        PR 리뷰·수정          :active, infpr, after infw2, 14d
        baseline              :milestone, infbl, after infpr, 0d
    ```

    - **스펙 작성 테이블 — 제품별 개발 항목 종합 (제품 × 단계)** · 정본=[Roadmap §4](<VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>) (수정은 그쪽 먼저)
      - **각 셀 앞 이모지 = 그 항목을 다루는 스펙의 작성 진행**: ✅ baseline · 🟢 PR · 🟡 작성중 · ⬜ 미작성 (— = 해당 없음)

      | 제품 | 1단계(호환성) | 2단계(presigned) | 3단계(GW 일원화) | 4단계(멀티리전) | 5단계(Straumann) | 후속 | 스펙 산출물(단위·유형) |
      | --- | --- | --- | --- | --- | --- | --- | --- |
      | **CleverSpace** | ⬜ 서버 버전 체크·well-known·오류코드 | ⬜ presigned 발급 신규 | ⬜ GW 경유 수신 정합 | ⬜ 멀티 Region 구축 | — | — | ① OnePager · ② OnePager · ③-P-CS |
      | **CleverOne** | ⬜ Vatech-\* 헤더·well-known·fallback | ⬜ 업로드 흐름 연계 | ⬜ Direct→GW 경유 | ⬜ Region 선택 UI(대안)·ClinicID | — | — | ① · ② · ③-P-CO OnePager |
      | **EzServer(EZ)** | ⬜ 헤더 대리 전달 | ⬜ 전송 로직(presigned 직접) | ⬜ GW 경유 전환 | ⬜ ClinicID·Region·클리닉 등록(잠정) | ⬜ AXS 연동(갈래A)·presigned 직접 | ⬜ Rust 재개발 | ①·②·③-P-EZ·④(갈래A) |
      | **CleverLab** | — | — | — | — | ⬜ AXS 오더·상태·확정(갈래B)·presigned | — | ④ Sub-SRS(갈래B) |
      | **VatechAPIGateway** | — | — | 🟡 본체·라우팅·인증·호환·presigned 중계·경로B 흡수 | 🟡 Region 분배·HA(K8s)·Route53·Postgres | ⬜ AXS OAuth 중계·Org-ID·온보딩·인바운드·고정IP | — | **③ SRS 🟡** · ④ connector ⬜ |
      | **GW Console** | — | — | — | ⬜ Admin Web Console(③-C) | ⬜ 온보딩·Org-ID 관리 화면 | — | ③-C Sub-SRS |
      | **인프라** | ⬜ 단일 Region | — | ⬜ 단일 Region GW | ⬜ Route53·K8s·비-AWS minio | ⬜ AXS 고정IP·샌드박스 | — | ③-I IaC 계획서 |
      | **외부(Straumann AXS)** | — | — | — | — | ⬜ API·OAuth·샌드박스·자격증명(선결) | — | ④ 입력(외부 제공) |
      | **LMP(License Portal, 바텍)** | — | — | — | — | — | ⬜ (조건부) 제3자 서명 attestation | **enroll B안 시만**·ES 라이선스팀(R9·#42) |

      > 현재 착수된 스펙은 **③ VatechAPIGateway SRS + OpenAPI/DBML(🟡·PR 7/9 목표)** 뿐 — 그래서 GW의 3·4단계 셀만 🟡. 나머지는 ③ PR/baseline 후 착수(순서·의존=[Roadmap §3.9]).

  - **S3. 버전 호환성 매트릭스 — 원본(YAML)·생성물(JSON) 샘플 공유** — 클라이언트가 "자기가 호환되는지 스스로 판단"하도록 API/기능별 최소 클라이언트 버전·오류코드·fallback을 공개(§7.7.2·FR-COMPAT). **2단계 구조**: 개발자는 **원본 `compat-matrix.yaml`을 편집**(PR)하고, **CI가 env별 `server-configuration.json`을 생성→S3 발행**, GW는 런타임에 S3에서 읽어 게이팅·`/.well-known/{env}/server-configuration.json` 서빙. **정본 샘플·가이드 = `specs/03-srs-gateway/design/well-known/`**(`compat-matrix.sample.yaml` + `server-configuration.sample.json` + `README.md`).
    - **(A) 원본 — 개발자가 편집하는 것** `compat-matrix.yaml` (주석·이유 기록 가능, `Vatech-Product`별 최소 버전):

      ```yaml
      apis:
        - id: region.change # 안정 식별자(불변)
          path: /v1/clinics/{clinicId}/region
          minClientVersion: { EzServer: '2.1.0' }
          errorCode: COMPAT_CLIENT_TOO_OLD
          fallback: '클라이언트 업데이트가 필요합니다.'
        - id: region.resolve
          path: /v1/region/resolve
          minClientVersion: { CleverOne: '1.2.0' }
          errorCode: COMPAT_CLIENT_TOO_OLD
          fallback: '클라이언트 업데이트가 필요합니다.'
      features:
        - id: presignedUpload
          minClientVersion: { CleverOne: '1.3.0', EzServer: '2.1.0' }
          errorCode: COMPAT_FEATURE_UNSUPPORTED
          fallback: '현재 버전에서 지원하지 않는 기능입니다.'
      # schemaVersion·env·serverVersion·generatedAt 는 CI가 주입(여기 안 적음)
      ```

    - **(B) 생성물 — CI가 만들어 S3에 올리는 서빙본** `server-configuration.json`(경로 `/.well-known/<env>/server-configuration.json`·env별 분리·버전 프리픽스 없음):

      ```json
      {
        "schemaVersion": "1.0",
        "env": "production",
        "serverVersion": "gw/1.0.0.0",
        "generatedAt": 1718000000000,
        "compatibility": {
          "apis": [
            {
              "id": "region.change",
              "path": "/v1/clinics/{clinicId}/region",
              "minClientVersion": { "EzServer": "2.1.0" },
              "errorCode": "COMPAT_CLIENT_TOO_OLD",
              "fallback": "클라이언트 업데이트가 필요합니다."
            },
            {
              "id": "region.resolve",
              "path": "/v1/region/resolve",
              "minClientVersion": { "CleverOne": "1.2.0" },
              "errorCode": "COMPAT_CLIENT_TOO_OLD",
              "fallback": "클라이언트 업데이트가 필요합니다."
            }
          ],
          "features": [
            {
              "id": "presignedUpload",
              "minClientVersion": { "CleverOne": "1.3.0", "EzServer": "2.1.0" },
              "errorCode": "COMPAT_FEATURE_UNSUPPORTED",
              "fallback": "현재 버전에서 지원하지 않는 기능입니다."
            }
          ]
        }
      }
      ```

    - **왜 2단계(원본→생성)인가**: 서빙 JSON엔 **손으로 넣으면 안 되는 자동 필드**(`generatedAt`·`serverVersion`·`schemaVersion`·해시)가 있고, **env별(production/staging/unstable) 값이 다를 수 있어** 원본 1개→env별 N개 생성 + **CI 스키마 검증**이 필요하다. 그래서 "서빙 JSON을 직접 손편집"은 안 하고 원본에서 생성한다(과설계 아님·필수).
    - **관리 구조·포맷 결정은 → R5** (소스 repo 위치+CI 토폴로지·원본 포맷 YAML/JSON). 본 S3는 샘플·구조 공유용.
    - **관리 방식(§7.7.5)**: 서빙 JSON은 **손편집 아님**(원본→CI 생성→S3). GW는 런타임 read+cache라 **매트릭스만 바뀌면 앱 재배포 0**(`config/**` path-scoped 발행 파이프라인). S3는 **CI만 쓰기**, Console은 **읽기 전용 뷰어**.
    - **논의 씨앗**: 현재 스키마는 `minClientVersion` 이분법(미만=거부)만 표현 → **§7.7.3의 3단계 반응(major=차단/minor=경고/patch=무시)은 아직 스키마에 없음** → 값 확정(① One Pager) 시 tier/경고 필드 도입 검토. **이번 주는 형식·구조 공유가 목적**(값·스키마 확정은 ①).

- 이월 논의 사항 (6/25·7/2 미결 — 계속) | # | 항목 | 타입 | 상태 | | --- | --- | --- | --- | | 4 | Webhook 클라우드 분배(CleverLab 갈래B) | [논의] | v1.0 제외 — Open 후 결정 | | 6 | AXS sandbox 자격증명(Straumann 제공) | [정보] | pilot(08-15) 블로커 — 확보 시점? (R4 Tech support 채널과 함께 요청) | | 7 | 경로 B EOS 시점 | [논의] | ① One Pager 확정 의존 | | 8 | v1.0 목표 RPS·동시 세션 | [정보] | 인프라/규모 PL 입력 대기 | | 9 | RTO/RPO·유지보수 윈도우 | [정보] | 인프라 설계 단계 | | 10 | 감사·consent 보존 기간 | [정보] | 법무 확인 대기 | | 11 | 호환성 매트릭스 확정본 | [정보] | ① One Pager 의존 |
  - **차주 이월 후보**: R4(AXS Org-ID 취득 경로·절차)가 이번 회의에서 확정/조사경로 미정이면 다음 주 이월 논의에 등재.

# VT API Gateway — 7/16 주간회의 Agenda

> 7/9 스냅샷(위 「7/9 주간회의」)은 **그대로 보존**(그 회의에서 공유한 정본). 아래는 **7/9 결정을 반영한 7/16 최신 스냅샷**이며, 틀(논의/공유/이월)은 7/9와 동일하다.

- 논의 사항 (7/9 결정 → 적용/후속 · 신규 결정 요청)
  - **R1. IO(IntraOral) Scanner ↔ EzServer 연동 방식 확정 (선결·중요)** — v1.0 범위를 **Straumann IO Scanner**로 좁혔으나(7/9), **IO Scanner와 EzServer가 어떻게 연동되는지 미정**이다. 이는 **③-P-EZ EzServer 스펙·④ AXS 시나리오·GW E2E의 최대 선결**이라 조기 확정이 필요하다. **정할 것 = 방식·결정 주체·기한**(미정 시 아래 이월 논의로).
    - (결정) 아직 협의 중
  - **R2. Straumann 연동 목표일정 확정 — 잠정 10월 중** — 10월 출시 역산 Gantt(아래 S2)를 **확정/조정**한다. Raymond는 **SectionView 병행(부분투입)** 이라 이를 반영한 기간이며, 착수 후 재산정.
    - (결정) 10월 중으로 production 연동 완료
    - 9월 중으로 개발 환경 연동 완료 (IOScanner, EzServer 수정, GW가 AXS 연동)
      - Infra 구축 및 자동배포는 8월에 되어야 한다.
  - **R3. sub-Spec 초안 작성** - Infra Sub Spec 은 Raymond가 기본 Diagram 을 그려주면 Detail한 거는 Jack 이 작성한다.
  - (결정) EzServer 연동 Spec의 초안 작성은 Raymond가 해서 Thomas 에게 전달한다.

- 공유 사항 (결정 아님 · 정보 공유)
  - **S1. v1.0 전략 조정 반영 — Straumann IO Scanner 우선 (7/9 결정)** — v1.0 AXS 연동 = **IO Scanner만**, **CleverOne 연동은 post-v1.0**로 이관. GW 기본(호환성·인증·라우팅·target 프록시)은 originator 무관 공통이라 **v1.0 포함**. **스펙 초안 담당(7/16 R3 갱신)**: CleverOne=**Nick** · **EzServer 연동 Spec 초안=Raymond 작성→Thomas 전달·완성** · **③-I Infra Sub-Spec=Raymond 기본 diagram→Jack detail 작성**. **반영 완료**: SRS §1.2·§2.7 · ④/③-P-EZ/③-P-CO seed · 정본 Roadmap §3.9.
    - **단계 개요(0~5 · 0단계 신설 공유)** — v1.0(IO Scanner 우선)으로 **0단계(IO Scanner↔EzServer 수집·선결·수집 제품/방식 R1 미정)** 를 앞에 신설(기존 1~5 번호·정의 불변): **0** IO Scanner↔EzServer 수집(v1.0 선결·R1) · **1** API 호환성 · **2** presigned · **3** GW 일원화 · **4** 멀티 Region · **5** Straumann(AXS). 정본=Roadmap §3.1·§4.
    - **⚠ 스펙 단위(원문자) ≠ 로드맵 단계(숫자)** — 원문자(①②③④·③-C·③-P·③-I)는 **스펙 문서 번호(불변)**, 0~5는 **진행 단계**. 매핑: **①→1단계 · ②→2단계 · ③→3·4단계(GW 본체) · ④→5단계(Straumann) · ③-P-EZ→각 단계+0단계(IO 수집·R1)**. 예) **④ AXS Sub-SRS = 5단계**(4단계 아님), v1.0은 IO Scanner scope. 0단계(IO Scanner→EzServer 수집)는 ④가 아니라 ③-P-EZ/R1 소관.
  - **S2. 프로젝트 일정(Gantt) — 7/16 스냅샷** — 스펙 생애주기(작성→PR→baseline)+GW 구현 타임라인. **정본=[개발 Roadmap 결정 §3.9](<VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>)** (수정은 그쪽 먼저·동기화 완료). **7/9 대비 변경**: v1.0 범위=IO Scanner로 축소 · 각 스펙 **작성/PR 분리** · CleverOne·②Presigned·CleverSpace=**deferred(post-v1.0)** 섹션 · **담당 표기**.
    - 막대 색: 작성=기본 · PR=강조 · ◆=baseline/마일스톤 · 빨강=외부/미정 선결. **선결(빨강)**: IO Scanner↔EzServer 연동방식(미정·R1)·AXS sandbox 자격(Straumann). **목표=10월 출시**(역산·잠정). **병행 별도 프로젝트**: `SectionView Module 구현`(7/13~2주·Raymond·**GW 아님**)을 별도 섹션 `▷ 병행`에 **다른 색(crit)** 으로 표기 — GW 일정과 자원 경합(부분투입) 가시화용.

    ```mermaid
    gantt
        title v1.0 = Straumann IO Scanner 연동 — 10월 출시 목표(역산·잠정) · 7/9 결정 반영
        dateFormat YYYY-MM-DD
        axisFormat %m/%d
        todayMarker stroke-width:3px,stroke:#d33,opacity:0.6

        section ③ GW SRS + API/DBML (계약 SSOT · Raymond·부분투입)
        작성 (본문+OpenAPI·DBML)       :done, srsw, 2026-06-15, 28d
        PR 리뷰·수정                  :active, srspr, 2026-07-13, 2026-07-23
        baseline v1.0                 :milestone, srsbl, after srspr, 0d

        section ① API 호환성 One Pager (GW 기본 — v1.0 포함)
        작성                          :op1w, 2026-07-14, 10d
        PR 리뷰·수정                  :op1pr, after op1w, 7d
        baseline                      :milestone, op1bl, after op1pr, 0d

        section ④ AXS Sub-SRS (=5단계 Straumann · v1.0=IO Scanner scope · R1 후 착수 · Raymond)
        작성 (IO Scanner scope · R1 후) :axsw, 2026-07-21, 21d
        PR 리뷰·수정                  :axspr, after axsw, 14d
        baseline                      :milestone, axsbl, after axspr, 0d
        AXS sandbox 자격(Straumann·선결) :crit, cred, 2026-08-18, 21d

        section ③-P-EZ EzServer 연동 스펙 (초안 Raymond→Thomas · R3)
        IO Scanner↔EzServer 연동방식 확정(미정·선결·R1) :crit, ezm, 2026-07-21, 21d
        초안 (Raymond)→Thomas          :ezw, after ezm, 21d
        PR 리뷰·수정                  :ezpr, after ezw, 14d
        baseline                      :milestone, ezbl, after ezpr, 0d

        section ③-I 인프라 IaC (AppConfig·4-way·egress · R3: Raymond diagram→Jack)
        Raymond 기본 diagram 초안       :infw1, after srsbl, 7d
        Jack detail 작성               :infw2, after infw1, 14d
        PR 리뷰·수정                  :infpr, after infw2, 14d
        baseline                      :milestone, infbl, after infpr, 0d
        Infra 구축·자동배포 완료(8월·R2) :milestone, infra8, 2026-08-31, 0d

        section ③-C GW Console (v1.0 최소 — 온보딩·Org 관리)
        작성                          :conw, after srsbl, 14d
        PR 리뷰·수정                  :conpr, after conw, 14d
        baseline                      :milestone, conbl, after conpr, 0d

        section GW 구현 → E2E → 출시 (Raymond 부분투입·SectionView 병행)
        GW 구현 (IO Scanner MVP)        :active, impl, after axsbl, 50d
        AXS E2E (sandbox)              :e2e, after impl, 14d
        개발환경 연동 완료(9월·R2)       :milestone, dev9, 2026-09-30, 0d
        v1.0 production 연동 완료(10월·R2) :milestone, rel, 2026-10-31, 0d

        section v1.0 이후 (deferred · post-v1.0)
        CleverOne 연동 스펙 작성 (Nick) :codef, after rel, 14d
        ② Presigned One Pager 작성     :pdef, after rel, 14d
        CleverSpace 적응 작성 (③-P-CS)  :csdef, after rel, 14d

        section ▷ 병행 · 별도 프로젝트 (GW 아님)
        SectionView Module 구현 (Raymond 병행) :crit, sv, 2026-07-13, 2026-07-23
    ```

  - **S3. ③ GW SRS PR 등록·리뷰 대응 현황 (정보 공유)** — ③ GW SRS(+OpenAPI·DBML)를 `vt-api-gateway` 레포 `docs/gw-srs-initial` 브랜치 **PR로 등록(7/13)**. 리뷰 코멘트 **38 스레드 전부 대응 완료** · **PR 리뷰 완료 목표 = 7/23**.
    - **리뷰어**: Scott·Thomas·Jack·Eric·Larry·James + CodeReviewAgent(자동리뷰 2회).
    - **성격**: 대부분 **문서·계약 정합/서술 명확화** — 아키텍처·데이터 모델 변경 없음. SRS·OpenAPI 반영은 **로컬 완료·검증 통과**(redocly valid·SRS 코드펜스 정합), **금일 일괄 push 예정**.
    - **주요 반영**: 프록시 남용·SSRF 방어와 신뢰경계(§4.1.2) · 온보딩 실패 시 기존(레거시) usecase 지속성·rollback(§2.8) · 경로 B EOS workaround(§2.8) · Region Resolver 계약 정합(`ClinicResolution` 신설·§7.3.1) · Aurora Global DB write-forwarding 감안(§2.1.1·gw/1.2).
    - **남은 절차**: 필수 리뷰어(Scott·Thomas) 재승인 → **baseline v1.0**(7/23 리뷰 완료 후).
    - **[크로스팀 · R1 연계]** Thomas의 프록시 남용 우려 검토 결과 — GW에 인증하는 주체가 EzServer라 `client→EzServer` 내부 구간 인증은 GW 신뢰경계 밖·**EzServer(③-P-EZ) 계층 소관**으로 정리(내부망 무신뢰 강화 여부는 EzServer 위협모델 판단). EzServer 스펙(R1·Thomas)에서 다룰 항목.

  - **S4. 스펙 작성 테이블 — 제품별 개발 항목 종합 (제품 × 단계) · 매주 스냅샷** · 정본=[Roadmap §4](<VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>) (수정은 그쪽 먼저)
    - **각 셀 앞 이모지 = 그 항목을 다루는 스펙의 작성 진행**: ✅ baseline · 🟢 PR · 🟡 작성중 · ⬜ 미작성 (— = 해당 없음)

      | 제품 | 0단계(IO Scanner 수집·v1.0 선결·R1) | 1단계(호환성) | 2단계(presigned) | 3단계(GW 일원화) | 4단계(멀티리전) | 5단계(Straumann) | 후속 | 스펙 산출물(단위·유형) |
      | --- | --- | --- | --- | --- | --- | --- | --- | --- |
      | **CleverSpace** | — | ⬜ 서버 버전 체크·well-known·오류코드 | ⬜ presigned 발급 신규 | ⬜ GW 경유 수신 정합 | ⬜ 멀티 Region 구축 | — | — | ① OnePager · ② OnePager · ③-P-CS |
      | **CleverOne**(post-v1.0) | — | ⬜ Vatech-\* 헤더·well-known·fallback | ⬜ 업로드 흐름 연계 | ⬜ Direct→GW 경유 | ⬜ Region 선택 UI(대안)·ClinicID | — | — | ① · ② · ③-P-CO OnePager |
      | **EzServer(EZ)** | ⬜ IO Scanner 데이터 수신(방식 R1·미정) | ⬜ 헤더 대리 전달 | ⬜ 전송 로직(presigned 직접) | ⬜ GW 경유 전환 | ⬜ ClinicID·Region·클리닉 등록(잠정) | ⬜ IO Scanner 연동·AXS(갈래A)·presigned 직접 | ⬜ Rust 재개발 | ①·②·③-P-EZ(초안 Raymond→Thomas)·④(갈래A) |
      | **IO Scanner(Straumann 장비·수집 제품 미정)** | ⬜ 스캔 데이터→EzServer 유입(수집 제품·방식 R1·미정) | — | — | — | — | (AXS 워크플로 대상) | — | R1 확정 후 ③-P-EZ(수신)·④(AXS scope) |
      | **CleverLab** | — | — | — | — | — | ⬜ AXS 오더·상태·확정(갈래B)·presigned | — | ④ Sub-SRS(갈래B) |
      | **VatechAPIGateway** | — | 🟢 ↳3단계 흡수(호환 게이트·§7.7) | 🟢 ↳3단계 흡수(presigned 중계·§4.1.4) | 🟢 본체·라우팅·인증·호환·presigned 중계·경로B 흡수 | 🟢 Region 분배·HA(K8s)·Route53·Postgres | ⬜ AXS OAuth 중계·Org-ID·온보딩·인바운드·고정IP | — | **③ SRS 🟢(단일·전 단계 통합)** · ④ connector 🟡 |
      | **GW Console** | — | — | — | — | ⬜ Admin Web Console(③-C) | ⬜ 온보딩·Org-ID 관리 화면 | — | ③-C Sub-SRS |
      | **인프라** | — | ⬜ 단일 Region | — | ⬜ 단일 Region GW | ⬜ Route53·K8s·비-AWS minio | ⬜ AXS 고정IP·샌드박스 | — | ③-I IaC 계획서(초안 Raymond diagram→Jack) |
      | **외부(Straumann AXS)** | — | — | — | — | — | ⬜ API·OAuth·샌드박스·자격증명(선결) | — | ④ 입력(외부 제공) |
      | **LMP(License Portal, 바텍)** | — | — | — | — | — | — | ⬜ (조건부) 제3자 서명 attestation | **enroll B안 시만**·ES 라이선스팀(R9·B-42) |

      > **7/16 진행**: ③ GW SRS(+OpenAPI·DBML) = **🟢 PR(7/13~7/23)** → baseline 후 나머지 착수 · **① One Pager = 🟡 작성 착수(7/14)** · **④ AXS Sub-SRS = R1(IO Scanner↔EzServer 방식) 결정 후 다음 주(~7/21) 착수**(그 전 착수 시 재작업 위험). **0단계(IO Scanner 수집)** = v1.0 선결·수집 제품/방식 미정(R1). v1.0 범위 = **Straumann IO Scanner** 한정 → **CleverOne 연동 post-v1.0 deferred**. 순서·의존 = [Roadmap §3.9].

- 이월 논의 사항 (6/25·7/2·7/9 미결 — 계속)

  | #    | 항목                                   | 타입        | 상태                                                         |
  | ---- | -------------------------------------- | ----------- | ------------------------------------------------------------ |
  | 4    | Webhook 클라우드 분배(CleverLab 갈래B) | [논의]      | v1.0 제외 — Open 후 결정                                     |
  | 6    | AXS sandbox 자격증명(Straumann 제공)   | [정보]      | pilot·E2E 블로커 — 확보 시점?                                |
  | 7    | 경로 B EOS 시점                        | [논의]      | 리뷰서 workaround·지속성 확정(§2.8) — EOS *시점*만 PM/① 미정 |
  | 8    | v1.0 목표 RPS·동시 세션                | [정보]      | 인프라/규모 PL 입력 대기                                     |
  | 9    | RTO/RPO·유지보수 윈도우                | [정보]      | 인프라 설계 단계                                             |
  | 10   | 감사·consent 보존 기간                 | [정보]      | 법무 확인 대기                                               |
  | 11   | 호환성 매트릭스 확정본                 | [정보]      | ① One Pager 의존                                             |
  | 신규 | IO Scanner↔EzServer 연동 방식          | [논의·선결] | 미정 → 이번 주 R1로 승격                                     |
  - **차주 이월 후보**: R1(IO Scanner↔EzServer 연동 방식)·R2(목표일정) 미확정 시 다음 주 이월.

# VT API Gateway — 7/23 주간회의 Agenda

> 7/16 스냅샷(위 「7/16 주간회의」)은 **그대로 보존**. 아래는 **7/23 최신 스냅샷**이며, 틀(논의/공유/이월)은 이전 주와 동일하다. **Gantt(S1)·스펙 작성 테이블(S2)은 매주 상시 포함**한다.

- 이번 주 진행
  - **③ GW SRS baseline v1.0 동결 완료(7/20)** — PR #11766 리뷰 51개 스레드 전부 resolve → **Complete(squash 병합)**. **tag `spec-v1.0`**(commit `275d153`)·문서 0.9→1.0. DBML 11→13 테이블·데이터 토폴로지 2-클러스터·clinic_id 불변·리전 endpoint 미노출·target secret write-only 등 반영. **계약(SRS·OpenAPI·DBML) SSOT 동결** → 이후 변경은 CCB→새 SHA.
  - **후속 조치(baseline 동결에 따른)**: (1) **하위 스펙 승격 unblock** — ③ 동결로 ③-C Console·④ AXS·③-P-EZ·③-I가 ③ 정본 SHA(`spec-v1.0`)를 참조해 정식 집필/baseline 진행 가능
  - **③-I Infra IaC 구축 계획서 초안 작성·인계(Raymond→Jack)** — GW SRS에서 인프라 요구 12영역 추출 + 전체 인프라 다이어그램. 각 영역에 `🔧 Jack 상세` 표시(구체 리소스·Terraform·사이징은 Jack 완성). DB/클러스터/스키마 명명 선결(권장안 명시). **정본을 `vt-api-gateway-infra`(브랜치 `docs/iac-plan-draft`)로 이관해 Jack 인계** (scp `specs/03i-infra/`는 리다이렉트 stub). 이후 상세·PR·baseline은 Jack.
  - **③-P-EZ EzServer GW 적응 OnePager 초안 작성(Raymond→EzServer 팀)** — GW SRS 추출 + **기존 EzServer suite 코드 분석**(nginx/EAP/ELM/EPI(Rust)/WebConsole). 기능 블록 **WS-1~8**(라우팅·인증·MQTT하행·업로드·heartbeat·로컬콘솔·하위호환·IO Scanner)로 구조화, 각 블록에 착지 컴포넌트·현황격차·`🔧 Thomas 상세` 명시. private_key_jwt 신규개발·presigned/MQTT 재활용 가능·EzServer 로컬 온보딩 콘솔 등 분석 결과 반영. IO Scanner 의존부=TBD(R1). `specs/03p-ez-ezserver/EzServer-GW적응-OnePager.md`.
  - **GW 구현 = 2단계 병행 착수 결정** — ③ baseline 동결(7/20)로 **GW 독립 코어(P0~P6·P10·④ 무관)를 7/21부터 선행 구현 착수**, **AXS 연동부(P7~P12)는 ④ AXS 연동 Spec 완성 후** 진행하는 2단계 병행으로 확정. 1단계는 로컬 backing 서비스+외부 더블로 인프라·AXS 없이 자립(재작업 리스크 0)이라 10월 출시 역산에 완충. 구현 계획 확정(착수 게이트 반영). 상세=S1 Gantt·공유.

- 논의 사항 (이번 주)
  - (결정) 0단계 IO Scanner는 잠시 보류하고, 1,2,3단계를 먼저 진행한다.
    - CleverSpace, CleverOne의 Sub Spec을 Raymond 이 초안을 작성해서 담당팀에 전달한다. (다음주중)
    - Straumann과 ES가 원하는 프로세스가 다른다.
      - Straumann : IO-Scanner -> AXS -(webhook)-> GW -> EzServer (고객이 연동 설정을 안하면 EzServer는 IO-Scanner 결과를 못받아서 문제)
      - ES : IO-Scanner -> EzServer -> GW -> AXS
      - Straumann과 얘기 중인데 쉽지 않다. Straumann은 기존에 자신들이 구축해 놓은 프로세스를 그대로 따르기를 원하지만 그러면 ES(VT)에 손해다. 협상중인데 쉽지 않다.
  - (결정) AWS 환경은 dev, qa, staging, prod 을 사용한다.
    - dev, qa는 같은 계정 사용하고 namespace로 분리한다. 단일 Region
    - stag 별도 - 단일 Region
    - prod는 region 별로 분리
    - 환경 파일은 template만 git에 올린다.
      - 각 환경별 .env는 Jack이 각각 작성한다.
      - 개발시에는 .env.template를 만들어서 Jack이 어떻게 설정해도 잘 동작하도록 해야 한다.
      - 로컬용 .env는 개발자가 만들어서 사용한다.

- 공유 사항 (결정 아님 · 정보 공유 · 매주 상시)
  - **S1. 프로젝트 일정(Gantt) — 7/23 스냅샷** — 스펙 생애주기(작성→PR→baseline)+GW 구현 타임라인. **정본=[개발 Roadmap 결정 §3.9](<VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>)** (수정은 그쪽 먼저·동기화 완료). **7/9 대비 변경**: v1.0 범위=IO Scanner로 축소 · 각 스펙 **작성/PR 분리** · CleverOne·②Presigned·CleverSpace=**deferred(post-v1.0)** 섹션 · **담당 표기**. · **7/16 회의 반영(순서 재조정)**: ③-I Infra·③-P-EZ EzServer 초안 **7/20 Raymond 착수** · **IO Scanner(④)·GW Console 연기**.
    - 막대 색: 작성=기본 · PR=강조 · ◆=baseline/마일스톤 · 빨강=외부/미정 선결. **선결(빨강)**: IO Scanner↔EzServer 연동방식(미정·R1)·AXS sandbox 자격(Straumann). **목표=10월 출시**(역산·잠정). **병행 별도 프로젝트**: `SectionView Module 구현`(7/13~2주·Raymond·**GW 아님**)을 별도 섹션 `▷ 병행`에 **다른 색(crit)** 으로 표기 — GW 일정과 자원 경합(부분투입) 가시화용.
    - **GW 구현 = 2단계 병행 착수(신규)** — ③ GW SRS baseline 동결(7/20·`spec-v1.0`)로 **계약이 고정된 GW 독립 부분은 ④ AXS·인프라 완성을 기다리지 않고 7/21부터 선행 구현**한다.
      - **1단계 — GW 독립 코어(7/21~·④ 무관)**: 플랫폼 토대·데이터 모델·인증(device/operator)·enrollment·레지스트리/region·호환성 게이트·target 프록시·fleet(= P0~P6·P10). 계약이 ③ SRS·DBML로 고정돼, 로컬 backing 서비스(Postgres·Valkey·SQS·MQTT·KMS 로컬 대체)+외부 시스템 더블로 unit/e2e가 **로컬 자립** → AXS·인프라 없이 진행.
      - **2단계 — AXS 연동(④ 연동 Spec 완성 후)**: External Connector·AXS 커넥터 실연동·webhook 수신/분배·sandbox 전구간 E2E(= P7~P12). **④ AXS Sub-SRS**(연동 Spec)와 Straumann sandbox 자격 확보 후 착수·완결.
      - 두 단계는 **스펙 집필과 병행**(위 Gantt에 `1단계`·`2단계` 막대 분리). 근거=7/2 R7(1안): 구현 시작점=④ AXS baseline이나 _core 일부는 ③ baseline 후 선행 가능_. **1단계 선행은 재작업 리스크 0**이며 10월 출시 역산에 완충.

    ```mermaid
    gantt
        title v1.0 = Straumann IO Scanner 연동 — 10월 출시 목표(역산·잠정) · 7/9 결정 반영
        dateFormat YYYY-MM-DD
        axisFormat %m/%d
        todayMarker stroke-width:3px,stroke:#d33,opacity:0.6

        section ③ GW SRS + API/DBML (계약 SSOT · Raymond·부분투입)
        작성 (본문+OpenAPI·DBML)       :done, srsw, 2026-06-15, 28d
        PR 리뷰·수정                  :active, srspr, 2026-07-13, 2026-07-20
        baseline v1.0 (7/20 월 확정)     :milestone, srsbl, after srspr, 0d

        section ① API 호환성 One Pager (연기 · GW 기본 — v1.0 포함)
        작성 (2주 더 연기·8월 초)       :op1w, 2026-08-03, 10d
        PR 리뷰·수정                  :op1pr, after op1w, 7d
        baseline                      :milestone, op1bl, after op1pr, 0d

        section ④ AXS Sub-SRS (=5단계 Straumann · v1.0=IO Scanner scope · 연기·7/16 · Raymond)
        작성 (IO Scanner scope·연기·EzServer 초안 후) :axsw, after ezw, 21d
        PR 리뷰·수정                  :axspr, after axsw, 14d
        baseline                      :milestone, axsbl, after axspr, 0d
        AXS sandbox 자격(Straumann·선결) :crit, cred, 2026-08-18, 21d

        section ③-P-EZ EzServer 연동 스펙 (초안 Raymond 7/20 착수→EzServer 팀 · R3·7/16)
        IO Scanner↔EzServer 연동방식 확정(미정·선결·R1) :crit, ezm, 2026-07-21, 21d
        초안 Raymond(IO Scanner+기본 GW연동)→EzServer팀 :ezw, 2026-07-20, 21d
        PR 리뷰·수정                  :ezpr, after ezw, 14d
        baseline                      :milestone, ezbl, after ezpr, 0d

        section ③-I 인프라 IaC (초안 Raymond diagram 7/20 착수→Jack detail · R3·7/16)
        초안 Raymond(diagram+요구추출)→Jack detail :infw, 2026-07-20, 21d
        PR 리뷰·수정                  :infpr, after infw, 14d
        baseline                      :milestone, infbl, after infpr, 0d
        Infra 구축·자동배포 완료(8월·R2) :milestone, infra8, 2026-08-31, 0d

        section ③-C GW Console (연기·후순위 — 온보딩·Org 관리)
        작성 (연기·후순위)              :conw, after axsbl, 14d
        PR 리뷰·수정                  :conpr, after conw, 14d
        baseline                      :milestone, conbl, after conpr, 0d

        section GW 구현 → E2E → 출시 (2단계 병행 · Raymond 부분투입·SectionView 병행)
        1단계 GW 독립 코어 (③ 고정·④무관·P0~P6·P10·7/21 착수) :active, implindep, 2026-07-21, 45d
        2단계 AXS 연동 (P7~P12·④ 연동 Spec draft 후)   :implaxs, after axsw, 40d
        AXS E2E (sandbox)              :e2e, after implaxs, 14d
        개발환경 연동 완료(9월·R2)       :milestone, dev9, 2026-09-30, 0d
        v1.0 production 연동 완료(10월·R2) :milestone, rel, 2026-10-31, 0d

        section v1.0 이후 (deferred · post-v1.0)
        CleverOne 연동 스펙 작성 (Nick) :codef, after rel, 14d
        ② Presigned One Pager 작성     :pdef, after rel, 14d
        CleverSpace 적응 작성 (③-P-CS)  :csdef, after rel, 14d

        section ▷ 병행 · 별도 프로젝트 (GW 아님)
        SectionView Module 구현 (Raymond 병행) :crit, sv, 2026-07-13, 2026-07-23
    ```

  - **S2. 스펙 작성 테이블 — 제품별 개발 항목 종합 (제품 × 단계) · 매주 스냅샷** · 정본=[Roadmap §4](<VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>) (수정은 그쪽 먼저)
    - **각 셀 앞 이모지 = 그 항목을 다루는 스펙의 작성 진행**: ✅ baseline · 🟢 PR · 🟡 작성중 · ⬜ 미작성 (— = 해당 없음)

      | 제품 | 0단계(IO Scanner 수집·v1.0 선결·R1) | 1단계(호환성) | 2단계(presigned) | 3단계(GW 일원화) | 4단계(멀티리전) | 5단계(Straumann) | 후속 | 스펙 산출물(단위·유형) |
      | --- | --- | --- | --- | --- | --- | --- | --- | --- |
      | **CleverSpace** | — | ⬜ 서버 버전 체크·well-known·오류코드 | ⬜ presigned 발급 신규 | ⬜ GW 경유 수신 정합 | ⬜ 멀티 Region 구축 | — | — | ① OnePager · ② OnePager · ③-P-CS |
      | **CleverOne**(post-v1.0) | — | ⬜ Vatech-\* 헤더·well-known·fallback | ⬜ 업로드 흐름 연계 | ⬜ Direct→GW 경유 | ⬜ Region 선택 UI(대안)·ClinicID | — | — | ① · ② · ③-P-CO OnePager |
      | **EzServer(EZ)** | ⬜ IO Scanner 데이터 수신(방식 R1·미정·TBD) | 🟡 헤더 대리 전달 | 🟡 전송 로직(presigned 직접) | 🟡 GW 경유 전환 | 🟡 ClinicID·Region·클리닉 등록(잠정) | 🟡 AXS(갈래A)·presigned 직접(IO Scanner 세부=TBD) | ⬜ Rust 재개발 | **🟡 ③-P-EZ One Pager 초안 작성됨**(Raymond→EzServer 팀) — `specs/03p-ez-ezserver/EzServer-GW적응-OnePager.md` · ④(갈래A) |
      | **IO Scanner(Straumann 장비·수집 제품 미정)** | ⬜ 스캔 데이터→EzServer 유입(수집 제품·방식 R1·미정) | — | — | — | — | (AXS 워크플로 대상) | — | R1 확정 후 ③-P-EZ(수신)·④(AXS scope) |
      | **CleverLab** | — | — | — | — | — | ⬜ AXS 오더·상태·확정(갈래B)·presigned | — | ④ Sub-SRS(갈래B) |
      | **VatechAPIGateway** | — | 🟢 ↳3단계 흡수(호환 게이트·§7.7) | 🟢 ↳3단계 흡수(presigned 중계·§4.1.4) | 🟢 본체·라우팅·인증·호환·presigned 중계·경로B 흡수 | 🟢 Region 분배·HA(K8s)·Route53·Postgres | ⬜ AXS OAuth 중계·Org-ID·온보딩·인바운드·고정IP | — | **③ SRS 🟢(단일·전 단계 통합)** · ④ connector 🟡 |
      | **GW Console** | — | — | — | — | ⬜ Admin Web Console(③-C) | ⬜ 온보딩·Org-ID 관리 화면 | — | ③-C Sub-SRS |
      | **인프라** | — | — | — | 🟡 단일 Region GW | 🟡 Route53·K8s·비-AWS minio | 🟡 AXS 고정IP·샌드박스 | — | **🟡 ③-I IaC 구축 계획서 초안 완료·인계**(Raymond diagram+SRS추출→Jack 상세) — 정본 `vt-api-gateway-infra`(브랜치 `docs/iac-plan-draft`) |
      | **외부(Straumann AXS)** | — | — | — | — | — | ⬜ API·OAuth·샌드박스·자격증명(선결) | — | ④ 입력(외부 제공) |
      | **LMP(License Portal, 바텍)** | — | — | — | — | — | — | ⬜ (조건부) 제3자 서명 attestation | **enroll B안 시만**·ES 라이선스팀(R9·B-42) |

      > **7/23 진행(7/16 회의 반영)**: ③ GW SRS = **PR 코멘트 접수 오늘(7/16)까지 → 다음주 월요일(7/20) 마무리·baseline v1.0(0.9→1.0)** · **③-I Infra·③-P-EZ EzServer 초안 = 7/20 Raymond 착수** · **① One Pager(2주 더·8월 초)·④ AXS(IO Scanner)·③-C GW Console = 연기** · **0단계(IO Scanner 수집)** = 선결·방식 R1 미정. v1.0 = **Straumann IO Scanner** 한정(CleverOne = post-v1.0). 순서·의존 = [Roadmap §3.9]. · **(C) 압축**: GW 구현을 ④ AXS _draft_ 후 착수 + **구현 기간 40d로 단축** → 구현 ~10/10·E2E ~10/24(**10/31 목표 이내**).

  - **S3. GW 구현 현황 — Phase·Task 스냅샷 (7/23·매주 갱신)** — ③ baseline 동결(7/20) 후 **7/21 1단계(GW 독립 코어) 구현 착수**. 정본 진척 = 각 Task PR merge 이력. 매 Task 완료 시 갱신.
    - **상태 범례**: ✅ 완료(main merge) · 🟡 부분완료(외부 선결로 일부 잔여) · 🟢 리뷰중(PR) · 🟠 구현중 · ⬜ 대기 · 🔴 외부 선결 대기. **표기 규칙**: Phase 내 전 Task 상태가 같으면 1행으로 묶고, 상태가 다르거나 **금주에 변화가 있으면** Task별로 펼친다.

      | Phase | Task | 설명 | 상태 | 비고 |
      | --- | --- | --- | --- | --- |
      | **P0 플랫폼 스캐폴드** | T-PLAT-0-1 | NestJS 모노레포·4-way 빌드타겟(core/admin/receiver/dispatcher)·libs/common | ✅ 완료 | PR #11971 merge |
      | ″ | T-PLAT-0-1b | 로컬 개발환경(docker-compose: PG×2·Valkey·SQS·MQTT·KMS 로컬대체)·Testcontainers·인프라 스모크 | ✅ 완료 | PR #11971 |
      | ″ | T-PLAT-0-1c | 헥사고날 포트/어댑터(Queue·Kms·ConfigStore·Mqtt)·계약 테스트 | ✅ 완료 | PR #11971 |
      | ″ | T-PLAT-0-1d | 외부 시스템 더블(LMP·Entra OIDC·AXS·CleverSpace·웹훅 발신·엣지 MQTT) | ✅ 완료 | PR #11971 |
      | ″ | T-PLAT-0-2 | Prisma 2-datasource(전역/리전)·DBML→schema 동기화 파이프라인 | ✅ 완료 | PR #11974 merge · CodeReviewAgent 반영 |
      | ″ | T-PLAT-0-3 | 관측(Pino+OTel)·표준 에러 envelope | ✅ 완료 | PR #11980 merge · pre-pr-review가 계약(errorCode) 선제 정합 |
      | ″ | T-PLAT-0-4 | ConfigService·IRSA·liveness/readiness·graceful shutdown | ✅ 완료 | PR #11982 merge |
      | ″ | T-PLAT-0-5 | CI 파이프라인·Dockerfile | 🟡 부분완료 | PR #11994 merge · Dockerfile 4타겟·의존성 스캔·CI 게이트 완료 / 🔴 배포(main→DEV·tag prefix)는 Jack Azure 템플릿 수령 후 |
      | ″ | T-PLAT-0-6 | 레포 온보딩 README | ✅ 완료 | PR #11995 merge |
      | **P1 데이터 모델·마이그레이션** | T-DATA-1-1 | 전역 백본 스키마·초기 마이그레이션(enum 8·테이블 10·FK) | ✅ 완료 | PR #12006 merge · risk:migration |
      | ″ | T-DATA-1-1b | 전역 관계 raw-SQL 제약(NULLS NOT DISTINCT·부분유니크) | ✅ 완료 | PR #12008 merge · 실 DB 23505 검증 |
      | ″ | T-DATA-1-2 | 리전 로컬 스키마·마이그레이션(audit·fleet·webhook_event·bytea) | ✅ 완료 | PR #12009 merge · FK 0·bytea·실 DB 검증 |
      | ″ | T-DATA-1-3 | KMS envelope 암호화 헬퍼(payload/자격 round-trip) | ✅ 완료 | PR #12011 merge · AES-256-GCM·실 KMS 검증 |
      | ″ | T-DATA-1-4 | Redis 키스페이스 헬퍼(nonce·jti·rate-limit·idempotency) | ✅ 완료 | PR #12012 merge · 실 Valkey 검증·incrRate 원자화 |
      | ″ | T-DATA-1-5 | audit_log append-only 프리미티브(트리거·AuditService) | ✅ 완료 | PR #12016 merge · replica 우회까지 차단 |
      | ″ | T-DATA-1-6 | region_catalog 시드(서울·default·self-heal) | ✅ 완료 | PR #12018 merge |
      | ″ | T-DATA-1-7 | 시드·테스트 데이터 인프라(prisma db seed·Factory·E2E 반복성 하네스) | ✅ 완료 | PR #12040 merge · full e2e 68·reset 통합 4 · **→ P1 완료** |
      | **P2 인증 토대** | T-AUTH-2-1 | private_key_jwt 검증→RS256 access token(`POST /v1/auth/token`)·JWKS 결정·키회전 대비 | ✅ 완료 | PR #12094 merge · 검증 4종·실 curl·독립리뷰 High 0 |
      | ″ | 2-2~2-5 | jti 1회소비·rate-limit·revocation / operator Entra OIDC·RBAC | ⬜ 대기 | 1단계(다음=2-2) |
      | **P3 enrollment·디바이스 생애주기** | 전체 | enroll start/complete·상태머신·재-enroll·C/S 승인·kill | ⬜ 대기 | 1단계 |
      | **P4 레지스트리·region resolution** | 전체 | Region Resolver·ClinicResolution·mapping_version·PHI OPA 경계 | ⬜ 대기 | 1단계 |
      | **P5 호환성 게이트** | 전체 | Vatech-\* 파싱·well-known·AppConfig·semver 3단계 | ⬜ 대기 | 1단계(compat 값=① One Pager 후) |
      | **P6 target-routed 프록시/라우팅** | 전체 | 서브도메인·verbatim·PEP 체인·SSRF fail-closed·타임아웃 | ⬜ 대기 | 1단계(실 AXS 왕복 E2E만 ④ 후) |
      | **P7 External Connector·AXS** | 전체 | OAuth2 cc·egress 고정IP·OPA egress·org-binding·presigned 중계 | ⬜ 대기 | 🔴 2단계·④ AXS 실연동 후 |
      | **P8 webhook 수신(Receiver)** | 전체 | HMAC·멱등·ACK·KMS 암호화 저장·SQS enqueue | ⬜ 대기 | 2단계(골격 로컬 더블 선행 가능) |
      | **P9 webhook 분배·MQTT(Dispatcher)** | 전체 | SQS consumer·대상해석·MQTT QoS1 하행·DLQ | ⬜ 대기 | 2단계 |
      | **P10 fleet·중앙 config·inventory** | 전체 | heartbeat·fleet_state·online 파생·config(gw.\*)·inventory | ⬜ 대기 | 1단계 |
      | **P11 Admin API·audit·컴플라이언스** | 전체 | 전 CRUD·RBAC 생애주기·break-glass·audit 전면 | ⬜ 대기 | 2단계(webhook slice=P8 후) |
      | **P12 E2E·하드닝** | 전체 | AXS sandbox E2E·compat E2E·부하·HA/KEDA 검증 | ⬜ 대기 | 🔴 2단계·④ AXS sandbox 실자격 |

      > **금주 구현 요약** — 이번 주는 **① 플랫폼·환경 토대(P0)를 완성**하고 **② 데이터 모델(P1)을 거의 마무리**했다.
      >
      > - **P0(완료)**: 단일 코드베이스에서 4개 앱(core·admin·receiver·dispatcher)이 빌드되는 뼈대, 로컬 개발환경(Docker 한 번에 DB·Redis·큐·MQTT·KMS 6종), 공통 운영기능(환경설정·헬스체크·무중단 종료·로그/추적·표준 에러 응답), Docker 이미지·CI 게이트까지 세웠다. → 이제 개발자가 `make dev-up` 한 번으로 로컬에서 서비스를 띄우고 테스트할 수 있다.
      > - **P1(진행·거의 완료)**: DB 스키마와 마이그레이션(전역/리전 **2개 클러스터**·13테이블), 그리고 데이터 공용 부품 — 암호화(KMS envelope)·캐시키(Redis)·**변조 불가 감사로그**·기본 리전 시드 — 을 구현했다. 남은 건 시드 러너(1-7) 하나로, 이걸 끝내면 P1 완료.
      > - **데이터 모델의 적용 범위**: 데이터 계층은 **4개 앱이 공유하는 하나의 공통 자산**이다(앱별로 나뉘지 않음). DB(전역 `gw_global`·리전 `gw_regional`)와 Prisma 스키마·공용 헬퍼는 `libs/common`에 **한 벌만** 두고 core·admin·receiver·dispatcher가 함께 쓴다 — **4-way는 노출하는 API·역할만 다를 뿐 데이터 모델/DB는 동일하게 공유**한다.
      > - **다음**: P1 마무리 → 인증(P2)·enrollment(P3)·레지스트리/region(P4) 순으로 실제 GW 기능 착수(모두 ④ AXS 없이 선행 가능). AXS 연동부(P7~)는 2단계.
      >
      > \*(참고: 진척=41 Task 중 17 완료+1 부분(**P0·P1 완료·P2 착수**=T-AUTH-2-1, 0-5만 배포부 잔여). 7/22 spec-v1.0.1 정합화 — 규칙 불변, 인가/설정의 구현 엔진만 조정, 완료분 영향 없음. 매 Task는 구현자와 분리된 독립 리뷰어의 pre-PR 검토를 거친다.)

- 이월 논의 사항 (6/25·7/2·7/9 미결 — 계속)

  | #    | 항목                                   | 타입        | 상태                                                         |
  | ---- | -------------------------------------- | ----------- | ------------------------------------------------------------ |
  | 4    | Webhook 클라우드 분배(CleverLab 갈래B) | [논의]      | v1.0 제외 — Open 후 결정                                     |
  | 6    | AXS sandbox 자격증명(Straumann 제공)   | [정보]      | pilot·E2E 블로커 — 확보 시점?                                |
  | 7    | 경로 B EOS 시점                        | [논의]      | 리뷰서 workaround·지속성 확정(§2.8) — EOS *시점*만 PM/① 미정 |
  | 8    | v1.0 목표 RPS·동시 세션                | [정보]      | 인프라/규모 PL 입력 대기                                     |
  | 9    | RTO/RPO·유지보수 윈도우                | [정보]      | 인프라 설계 단계                                             |
  | 10   | 감사·consent 보존 기간                 | [정보]      | 법무 확인 대기                                               |
  | 11   | 호환성 매트릭스 확정본                 | [정보]      | ① One Pager 의존                                             |
  | 신규 | IO Scanner↔EzServer 연동 방식          | [논의·선결] | 미정 → 이번 주 R1로 승격                                     |
  - **차주 이월 후보**: R1(IO Scanner↔EzServer 연동 방식)·R2(목표일정) 미확정 시 다음 주 이월.

# VT API Gateway — 7/30 주간회의 Agenda

> 7/23 스냅샷(위 「7/23 주간회의」)은 **그대로 보존**. 아래는 **7/30 최신 스냅샷(틀)** 이며, 틀(논의/공유/이월)은 이전 주와 동일하다. **Gantt(S1)·스펙 작성 테이블(S2)은 매주 상시 포함**한다. _※ 이 문서는 7/30 회의 전 준비한 **프레임**으로, `(프레임)` 표시 항목은 회의 시 확정한다._

- 이번 주 진행 _(프레임 · 7/30 회의 시 확정)_
  - **(7/23 결정 반영) 0단계 IO Scanner 보류 → 1·2·3단계 우선 진행**
    - Straumann↔ES 데이터 흐름 방향(IO Scanner→AXS→GW→EzServer vs IO Scanner→EzServer→GW→AXS) 협상 지속 → **IO Scanner 연동(0단계·④ AXS scope) 잠시 보류**.
    - 그 사이 계약이 고정된 **1(호환성)·2(presigned)·3(GW 일원화)단계**를 먼저 진행.
  - **(7/23 결정 반영) CleverSpace·CleverOne OnePager 2개 = Raymond 작성(7/27 병행 착수)**
    - 각 문서가 **1·2·3단계(호환성+presigned+GW 일원화)를 통합**.
    - presigned는 **CleverSpace(발급 API 신규)·CleverOne(이용) 양쪽**이 변경(직접 연동 금지·GW 경유) → **별도 Presigned One Pager 없이** 두 제품 OnePager에 포함.
    - **①호환성·②presigned 별도 문서 폐지 → 딱 2개 문서**.
    - CleverOne은 연동 *구현*은 post-v1.0이나 **OnePager는 지금** 작성(Nick→Raymond).
    - → S1 Gantt·S2 표 반영.
  - **(7/23 결정 반영) AWS 환경 = dev·qa·stag·prod 4계층**
    - dev·qa = 동일 계정·namespace 분리·단일 Region
    - stag = 별도·단일 Region
    - prod = Region별 분리
    - 환경 파일은 **template만 git** (각 환경 `.env`=Jack 작성 / 로컬 `.env`=개발자 / `.env.template`=Jack이 어떤 값이든 동작하도록 유지)
  - **(프레임) GW 구현 진척** — 1단계 GW 독립 코어에서 **금주 5개 Phase(P2~P6)를 완결**(상세·검증 4종 = S3)
    - **P2 인증 완결** — device 면(private_key_jwt→RS256 토큰·jti 1회 소비·검증후 정본 clientId rate-limit·revocation denylist·deviceAuth Guard)과 operator 면(Entra OIDC 검증+confused-deputy 방어·JIT operator·RBAC deny-by-default·`/v1/admin/me`)의 양 인증면 완비
    - **P3 enrollment 완결** — enroll 개시/완료(nonce 서명·공개키 검증→device pending·clinic upsert)·device 생애주기 상태머신·재-enroll 회전·C/S 승인·kill 즉시 폐기·미승인 pending 자동만료
    - **P4 레지스트리·region resolution 완결** · **P5 호환성 게이트 완결**(Vatech-\* 파싱→400·well-known 매트릭스 서빙·semver 3단계 게이팅) · **P6 target-routed 프록시 완결**(서브도메인 라우터·SSRF fail-closed·PEP 체인 401/403·verbatim bypass·D1~D3 타임아웃·취소 전파·Idempotency-Key)
    - 1단계 잔여 = **P10 fleet·config·inventory** / 2단계(P7~P12) = ④ AXS 연동 후
    - **⚠ region-silo(R2·spec-v1.0.5) 머지 후 일부 완료분 재작업 예정**(P4 전체·P1/P3/P6 리전 해석 단계 — 상세 S3)

- 논의 사항 (이번 주) _(프레임 · 신규 안건 회의 시 추가)_
  - **R2. GW 저장소 — 결정: 리전 완전 분리 (region silo) ✔ 확정(7/30)**
    - **리전 완전 분리 채택** — 각 리전이 **독립 스택**(자기 DB·전부 리전 로컬). **전역 일관/Global DB 미도입.** 근거: 베트남·중국 등 **리전 간 데이터 이동이 원천 봉쇄**되는 국가에서 전역 공유는 리스크가 큼 → **원천 봉쇄가 안전**. Global DB는 필요 시 후행 재설계(지금 안 만듦).
    - **적용 범위 = gw/1.2까지 스펙이 리전 완전 독립.**
    - **리전별 DB = PostgreSQL RDS 확정** (분리라 Global DB 기능 불필요 → Aurora 불요).
    - **payload(PHI)는 리전 DB에 저장** — 리전 독립이라 교차 복제 우려 없음 → **S3·DynamoDB 외부화 불요**(관계형 DB 컬럼 유지).
    - **클리닉 리전 변경 = Migration으로 지원**(투명 자동전환 아님). **지금 전부 구현 안 함 — gw/1.2 이후 요구사항 재수집 후 보강.**
    - **Webhook = AXS에 리전별 처리 요청**(AXS가 리전별로 발신). **AXS 미지원 시에만** global receiver가 forwarding하는 **보완책** → **SRS에 참고안으로 포함**.
    - **Global APEX(gw.vatech.com)·GeoDNS 불요** — 리전별 구축이라 **DNS에 리전 정보 포함**(region-specific host). **zone은 `gw.<도메인>` 하나만 위임받아 그 안에서 리전을 라벨로 관리**(`<svc>.<region>.gw.<도메인>`·예 `api.apne2.gw.vatech.com`) → 리전 추가 시 회사 apex 밑 재위임 불요(Jack 인프라 리뷰). **dev도 동일 형태**(`api.apne2.gw.dev.ezcld.net`)라 dev↔prod 호스트 규약 일치.
    - **GW Console = 리전별 스위치 관리**(불편 수용). 이때 **auth/authz 재검토** 필요 — 상세는 **③-C GW Console 스펙**, SRS는 언급만.
    - **진행 상황(7/30 · 스펙 반영 완료)**: 결정에 따라 **SRS(§2.1.1·§2.3.9 리전 마이그레이션·§3.1.2·§4.5.1·§7.3·§7.6·§7.6.3 등)·DBML·OpenAPI·env-reference·well-known·크로스팀 handoff(EzServer·인프라) 전면 개정 완료**. 리뷰에서 나온 Jack 인프라 지적(DNS zone 스킴 정련·중국 별도 파티션 defer·리전 DR 주권 제약·Region Directory 무결성·RDS 프로비저닝 등)과 자동 코드리뷰 11라운드를 **전건 반영**, **현재 미해결 코멘트 0**.
    - **남은 것 = 리뷰 승인뿐** — 필수 리뷰어 **Jack·Scott·Teddy 승인 대기**(승인 후 머지·태그 `spec-v1.0.5`). 구현(P1 데이터모델) 재작업은 머지 후 구현 세션 인계.
    - **PR**: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/12207
  - **R2-1. 호주 first-open 리전 전략 — 서울 임시 홈 vs 처음부터 호주 리전 (신규·결정 요청)**
    - **배경**: 호주에서 GW를 먼저 오픈. v1.0=단일 리전인데 region silo(R2)라 클리닉 데이터·PHI는 홈 리전에 갇힘.
    - **핵심 물음**:
      - (a) 호주 클리닉을 **서울 리전에 임시로** 올리고 나중에 호주 리전 신설 후 **통째 이전**할 것인가, (b) **처음부터 호주 리전(ap-southeast-2)** 에 올릴 것인가?
      - **호주 PHI 데이터 residency 규제상 서울 임시 홈이 허용되는가?** (허용 안 되면 (b) 강제 — silo 취지와도 일치)
      - (a)라면 이전 시점·계획은? 이전 = 데이터 이관 + EzServer 재설정 + **AXS webhook 콜백 변경** + device 인증서 재발급의 크로스-org 커트오버.
    - **지금 대비할 것(어느 쪽이든)**:
      - **AXS webhook 콜백을 클리닉(org)별로 세분화 요청** — 나중 이전 시 콜백 URL만 바꾸면 되게(리전 단위 콜백이면 리전 통째 이전만 가능).
      - `clinic_id` 리전-불변 유지(스펙 반영 완료) — 이전해도 클리닉 정체성·AXS 재온보딩 불요.
      - 임시 홈을 쓸 경우 **최소화 롤아웃**(곧 자기 리전 생길 곳은 임시 홈 회피).
    - **결정**: first-open 리전 (a/b) · 이전 계획 유무 · AXS 콜백 세분화 요청 여부.
    - (결정) 서울은 개발용, 호주리전은 먼저 오픈한다.
  - **R3. 제품 OnePager(③-P) 인계 현황·방식 확정 — CleverSpace·CleverOne(신규 전달) + EzServer(수령 확인)**
    - **배경**: 7/23 결정대로 CleverSpace·CleverOne OnePager 초안(각 **1·2·3·4단계 통합**·①호환성·②Presigned 흡수)을 **7/27 작성 완료**. EzServer 초안(③-P-EZ)은 **지난주 Teddy에게 공유**.
    - **문제**:
      - CleverSpace·CleverOne: 초안이 **작성자 개인 작업 공간**에 있어 담당팀 공유 불가 + **Teams 파일 전송 금지** → 전달 경로 없음.
      - EzServer: 공유는 했으나 **담당(Teddy)이 PR 생성·수령했다는 확인이 없음** → 인계가 실제 landing 됐는지 미확인.
    - **결정할 것 (등록처·공유 채널)** — OnePager는 mermaid 다이어그램·표 포함이라 **`.md` 원본 fidelity가 중요**(VKS 페이지 본문은 MD 온전 보존 불가):
      - ① **각 제품팀 git repo에 PR로 인계 (추천·EzServer 선례)** — `.md` 원본 그대로 · mermaid/표 렌더 · 리뷰/이력 확보 (Azure DevOps `ezserver_suite/doc/onepager`식·target branch)
      - ② VKS를 쓰면 **페이지 본문 붙여넣기가 아니라 `.md` 파일 첨부**로 (본문 붙여넣기는 MD 손실)
    - **확인할 것 (EzServer)**: Teddy가 `ezserver_suite/doc/onepager/gw_adaptation`에서 PR 생성·리뷰 착수했는지. 안 됐으면 재전달·경로 재확인 → CS/CO 인계에 ①안(각 팀 repo 접근) 적용 가능한지 여기서 함께 판단.
    - **함께 확정**: 소유·리뷰어(CleverSpace=고형용/Larry · CleverOne=탁수용/Nick · EzServer=Teddy·Thomas) · 리뷰 일정.
    - **확정 후 실행**: 등록처 이관 → 원본 redirect stub → 실행 할당표 `인계` 갱신 → (파일 아닌) 링크만 통지.
    - **연계**: S1 Gantt · S2 표.
    - (결정)
      - CleverSpace(git) onepager 전달할 경로(docs폴더)를 Scott이 전달해준다.
        - CleverSpace는 어느 Repo지? 
      - CleverOne(svn) onepager: SharePoint에 폴더를 만들어서 인계한다.
        - https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Forms/AllItems.aspx?id=%2Fsites%2Fes%2FProjectDoc%2FClever%20One%2Fsrs%2FOnePager&p=true&ga=1
        - 하위폴더를 정해야 한다. 
  - (결정) R4 - vatech.com은 쓰지 말자. 별도의 Domain을 사용하자.
    - vatech.com은 Email 도메인이니 건드리지 말자. 우리가 관리하기 어렵고, 혼란이 있을 수 있다.
    - 별도 도메인 지정 예정. 문서에 vatech.com을 사용한 것은 <도메인>으로 모두 바꿔야 한다.
  - **(이월·계속) Straumann ↔ ES IO Scanner 데이터 흐름 협상**
    - Straumann은 기존 프로세스(IO Scanner→AXS→GW→EzServer) 유지를 원하나 **ES(VT)에 불리**(고객이 연동 설정 안 하면 EzServer가 결과 미수신).
    - ES 안(IO Scanner→EzServer→GW→AXS)과 절충 협상 중.
    - **결정 시 이월-R1(IO Scanner↔EzServer 연동 방식)·④ AXS scope 착수 조건 확정.**
    - (결정) 다음주 논의 예정
  - **(프레임) AWS 환경 분리 후속**
    - 계정/네트워크 · ESO/Parameter Store 경로 · `.env.template` 항목 확정(Jack·Raymond).
    - ③-I Infra 계획서와 정합.
  - **(공유·결정 아님) 멀티리전 webhook 정합화 (SRS)** — 기존 SRS의 멀티리전 webhook 흐름이 절마다 엇갈려(일부 주권 위반) 이를 정정. §2.3.6을 **region 내 분배 / 교차리전 분배(receiver-forward)** 로 분리하고 §2.2·§7.6.3·§7.6.7 불일치 정정, §7.6.8에 단계화(**v1.0 단일 리전·gw/1.2 멀티리전**) 명시. **v1.0 무영향**. SRS 브랜치 PR로 반영(spec-v1.0.3).
    - **→ R2(리전 완전 분리)로 갱신(7/30)**: 이 정합화 구조(§2.3.6 분배 2-경로·§7.6.8 단계화)는 유지되나 모델이 바뀜 — **교차리전 receiver-forward는 fallback 참고안으로 격하**(1차 = AXS 리전별 발신), silo라 대표 수신점의 **home 리전 discovery는 미해결 과제(TBD)**로 명시(§2.3.6.2 노트). §7.6.6/§7.6.7도 '자기 리전 브로커 발행·런타임 clinic→region 해석 제거'로 재정리. **spec-v1.0.3 정합화는 region-silo 개편(spec-v1.0.5·PR #12207)에 흡수됨.**
  - _(신규 안건은 회의에서 추가)_

- 공유 사항 (결정 아님 · 정보 공유 · 매주 상시)
  - **S1. 프로젝트 일정(Gantt) — 7/30 스냅샷** — 스펙 생애주기(작성→PR→baseline)+GW 구현 타임라인. **정본=[개발 Roadmap 결정 §3.9](<VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>)** (수정은 그쪽 먼저 · 아래 7/23→7/30 변경은 **정본 §3.9 동기화 완료**). **7/23 대비 변경**: ① **0단계 IO Scanner·④ AXS = 보류**(Straumann 협상) · ② **③-P-CS CleverSpace·③-P-CO CleverOne OnePager 2개 = Raymond·7/27 병행 착수**(각 **1·2·3단계 통합**·**①호환성·②Presigned One Pager 폐지→두 제품 OnePager에 흡수**·CleverOne Nick→Raymond) · ③ **1·2·3단계 우선**.
    - 막대 색: 작성=기본 · PR=강조 · ◆=baseline/마일스톤 · 빨강=외부/미정 선결. **선결(빨강)**: IO Scanner↔EzServer 연동방식(**보류·R1**)·AXS sandbox 자격(Straumann). **목표=10월 출시**(역산·잠정 — ④ AXS/IO Scanner 보류로 **2단계 일정·출시일 재검토 대상**). **병행 별도 프로젝트**: `SectionView Module 구현`(7/13~2주·Raymond·**GW 아님**·완료)은 `▷ 병행` 섹션에 표기.
    - **GW 구현 = 2단계 병행(유지)** — 1단계 GW 독립 코어(P0~P6·P10)는 ③ baseline 고정으로 **정상 진행**(IO Scanner 보류 영향 없음). 2단계 AXS 연동(P7~P12)만 ④ AXS 보류에 연동되어 **후행**.
    - (결정)
      - GW Console v1.0 최소기능으로 앞으로 당겨서 진행한다. 전규현/ Raymond
      - GW Console
        - MS Entra로 연동
        - infra
          - istio로 admin api 접근권한 제어
          - 페이지접근도 ZeroTrust 에서만 접근 가능하게한다.

    ```mermaid
    gantt
        title v1.0 = Straumann IO Scanner 연동 — 10월 출시 목표(역산·잠정) · 7/23 결정(IO Scanner 보류·1·2·3단계 우선) 반영
        dateFormat YYYY-MM-DD
        axisFormat %m/%d
        todayMarker stroke-width:3px,stroke:#d33,opacity:0.6

        section ③ GW SRS + API/DBML (계약 SSOT · baseline v1.0 동결)
        작성 (본문+OpenAPI·DBML)       :done, srsw, 2026-06-15, 28d
        PR 리뷰·수정                  :done, srspr, 2026-07-13, 2026-07-20
        baseline v1.0 (7/20 확정·spec-v1.0.1 정합화 7/22) :milestone, done, srsbl, 2026-07-20, 0d

        section GW 구현 → E2E → 출시 (③ SRS 완료 직후 착수 · 2단계 병행 · Raymond 부분투입)
        1단계 GW 독립 코어 (③ 고정·④무관·P0~P6·P10·진행중) :active, implindep, 2026-07-21, 45d
        2단계 AXS 연동 (P7~P12·④ AXS 보류 해제 후)   :implaxs, after implindep, 40d
        AXS E2E (sandbox)              :e2e, after implaxs, 14d
        개발환경 연동 완료(9월·R2)       :milestone, dev9, 2026-09-30, 0d
        v1.0 production 연동 완료(10월·R2·재검토) :milestone, rel, 2026-10-31, 0d

        section ③-I 인프라 IaC (초안 Raymond diagram→Jack detail · PR 7/21 생성·진행중 · AWS dev·qa·stag·prod)
        초안 Raymond(diagram+요구추출)→Jack :done, infw, 2026-07-20, 1d
        PR 생성·리뷰·Jack detail(7/21 생성·진행중) :active, infpr, 2026-07-21, 21d
        baseline                      :milestone, infbl, after infpr, 0d
        Infra 구축·자동배포 완료(8월·R2) :milestone, infra8, 2026-08-31, 0d

        section ③-P-EZ EzServer 연동 스펙 (초안 Raymond 7/20 착수→EzServer 팀 · IO Scanner부=보류)
        초안 Raymond(기본 GW연동)→EzServer팀 :active, ezw, 2026-07-20, 21d
        PR 리뷰·수정                  :ezpr, after ezw, 14d
        baseline                      :milestone, ezbl, after ezpr, 0d

        section ③-P-CS CleverSpace OnePager (1·2·3단계 통합=호환성+presigned발급+GW경유 · ①②흡수 · Raymond)
        초안 Raymond(1·2·3단계 통합·7/27 병행 착수)→CleverSpace팀 :active, cssub, 2026-07-27, 14d
        PR 리뷰·수정                  :cspr, after cssub, 14d
        baseline                      :milestone, csbl, after cspr, 0d

        section ③-P-CO CleverOne OnePager (1·2·3단계 통합=헤더+presigned이용+GW경유 · ①②흡수 · Nick→Raymond·7/27 병행 착수)
        초안 Raymond(1·2·3단계 통합·CS와 병행)→CleverOne팀 :active, cosub, 2026-07-27, 14d
        PR 리뷰·수정                  :copr, after cosub, 14d
        baseline                      :milestone, cobl, after copr, 0d

        section ④ AXS Sub-SRS · IO Scanner (보류 — 7/23 결정: 0단계 IO Scanner 보류·Straumann 협상)
        IO Scanner↔EzServer 연동방식 확정(보류·선결·R1) :crit, ezm, after cosub, 21d
        작성 (IO Scanner scope · Straumann 협상 후) :axsw, after ezm, 21d
        PR 리뷰·수정                  :axspr, after axsw, 14d
        baseline                      :milestone, axsbl, after axspr, 0d
        AXS sandbox 자격(Straumann·선결) :crit, cred, 2026-08-18, 21d

        section ③-C GW Console (연기·후순위 — 온보딩·Org 관리)
        작성 (연기·후순위)              :conw, after axsbl, 14d
        PR 리뷰·수정                  :conpr, after conw, 14d
        baseline                      :milestone, conbl, after conpr, 0d

        section v1.0 이후 (deferred · post-v1.0)
        CleverOne 연동 *구현* (스펙은 지금·구현 post-v1.0) :codef, after rel, 14d

        section ▷ 병행 · 별도 프로젝트 (GW 아님)
        SectionView Module 구현 (Raymond·완료) :done, sv, 2026-07-13, 2026-07-30
    ```

  - **S2. 스펙 작성 테이블 — 제품별 개발 항목 종합 (제품 × 단계) · 매주 스냅샷** · 정본=[Roadmap §4](<VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>) (수정은 그쪽 먼저)
    - **각 셀 앞 이모지 = 그 항목을 다루는 스펙의 작성 진행**: ✅ baseline · 🟢 PR · 🟡 작성중 · ⬜ 미작성 (— = 해당 없음)

      | 제품 | 0단계(IO Scanner 수집·**보류**·R1) | 1단계(호환성) | 2단계(presigned) | 3단계(GW 일원화) | 4단계(멀티리전) | 5단계(Straumann) | 후속 | 스펙 산출물(단위·유형) |
      | --- | --- | --- | --- | --- | --- | --- | --- | --- |
      | **CleverSpace** | — | 🟡 서버 버전 체크·well-known·오류코드 | 🟡 presigned 발급 API 신규 | 🟡 GW 경유 수신 정합 | ⬜ 멀티 Region 구축 | — | — | **🟡 ③-P-CS CleverSpace OnePager(1·2·3단계 통합·①②③-P-CS 단일화) 초안 = Raymond**(7/27 병행 착수→CleverSpace 팀) |
      | **CleverOne**(OnePager 지금·연동 구현 post-v1.0) | — | 🟡 Vatech-\* 헤더·well-known·fallback | 🟡 presigned 업로드 이용 | 🟡 Direct→GW 경유 | ⬜ Region 선택 UI(대안)·ClinicID | — | — | **🟡 ③-P-CO CleverOne OnePager(1·2·3단계 통합·①②③-P-CO 단일화) 초안 = Raymond**(Nick→Raymond·7/27 병행 착수→CleverOne 팀) |
      | **EzServer(EZ)** | ⬜ IO Scanner 데이터 수신(방식 R1·**보류**·TBD) | 🟡 헤더 대리 전달 | 🟡 전송 로직(presigned 직접) | 🟡 GW 경유 전환 | 🟡 ClinicID·Region·클리닉 등록(잠정) | 🟡 AXS(갈래A)·presigned 직접(IO Scanner 세부=TBD) | ⬜ Rust 재개발 | **🟡 ③-P-EZ One Pager 초안 작성됨**(Raymond→EzServer 팀) — `specs/03p-ez-ezserver/EzServer-GW적응-OnePager.md` · ④(갈래A) |
      | **IO Scanner(Straumann 장비·수집 제품 미정)** | ⬜ 스캔 데이터→EzServer 유입(**보류**·수집 제품·방식 이월-R1·미정·Straumann 협상) | — | — | — | — | (AXS 워크플로 대상) | — | 이월-R1 확정 후 ③-P-EZ(수신)·④(AXS scope) |
      | **CleverLab** | — | — | — | — | — | ⬜ AXS 오더·상태·확정(갈래B)·presigned | — | ④ Sub-SRS(갈래B) |
      | **VatechAPIGateway** | — | 🟢 ↳3단계 흡수(호환 게이트·§7.7) | 🟢 ↳3단계 흡수(presigned 중계·§4.1.4) | 🟢 본체·라우팅·인증·호환·presigned 중계·경로B 흡수 | 🟢 리전 라벨 호스트·Region Directory·HA(K8s)·Route53·RDS(리전 단일) | ⬜ AXS OAuth 중계·Org-ID·온보딩·인바운드·고정IP | — | **③ SRS ✅ baseline(spec-v1.0.4)** · region-silo `spec-v1.0.5` PR 리뷰중 · ④ connector ⬜(보류) |
      | **GW Console** | — | — | — | — | ⬜ Admin Web Console(③-C) | ⬜ 온보딩·Org-ID 관리 화면 | — | ③-C Sub-SRS(연기) |
      | **인프라** | — | — | — | 🟡 dev·qa·stag(단일 Region)·prod(Region별) | 🟡 Route53·K8s·비-AWS minio | 🟡 AXS 고정IP·샌드박스 | — | **🟡 ③-I IaC 구축 계획서 — PR 7/21 생성·진행중**(Raymond diagram+SRS추출→Jack 상세) — 정본 `vt-api-gateway-infra`(브랜치 `docs/iac-plan-draft`) · **AWS 4계층(7/23)** |
      | **외부(Straumann AXS)** | — | — | — | — | — | ⬜ API·OAuth·샌드박스·자격증명(선결·**협상중**) | — | ④ 입력(외부 제공) |
      | **LMP(License Portal, 바텍)** | — | — | — | — | — | — | ⬜ (조건부) 제3자 서명 attestation | **enroll B안 시만**·ES 라이선스팀(R9·B-42) |

    - **스펙 문서 등록처·경로·baseline (SSOT)** — 각 제품 스펙 정본의 Repo·경로·태그. _(미정 = R3에서 등록처 확정 · OnePager는 담당팀 baseline 시 tag 부여)_

      | 단위 | 스펙 문서 | Repo (Azure DevOps) | 경로 | baseline tag |
      | --- | --- | --- | --- | --- |
      | **③ GW** | SRS(+OpenAPI·DBML·UnitTCL) | `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway` | `docs/specs/SRS.md` · `docs/specs/design/`(openapi·dbml) · `docs/specs/UnitTCL.md` | **`spec-v1.0.4`**(최신 baseline) · region-silo `spec-v1.0.5`(PR 리뷰중) |
      | **③-C GW Console** | Sub-SRS | `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console` (별도 repo·GW 소유→이관) | 미작성(신규 repo·경로 TBD) | 미작성(연기) |
      | **④ AXS** | Sub-SRS | 〃 vt-api-gateway (GW 소유) | `docs/specs/04-subsrs-straumann-axs/` | 미작성(보류) |
      | **③-I 인프라** | IaC 구축계획서 | `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-infra` | `docs/IaC-구축계획서.md` | 미부여(계획서·PR 진행) |
      | **③-P-EZ EzServer** | GW적응 OnePager | `https://dev.azure.com/ewoosoft/ezserver/_git/ezserver_suite` (branch `v6.5.x`) | `doc/onepager/gw_adaptation/Confidential_gw_adaptation_onepager.md` | 미부여(EzServer 팀 baseline 예정·R3 확인) |
      | **③-P-CS CleverSpace** | GW적응 OnePager | **미정 (R3 결정)** | 초안=작성자 개인 repo(SSOT 아님) | — |
      | **③-P-CO CleverOne** | GW적응 OnePager | **미정 (R3 결정)** | 초안=작성자 개인 repo(SSOT 아님) | — |
      | **③-P-LMP LMP** | OnePager(조건부) | **미정 (ES 라이선스팀?)** | — | — |
      | **CleverLab** | ④ Sub-SRS(갈래B) | 미정 (보류) | — | — |

      > **7/30 진행(7/23·오늘 결정 반영)**
      >
      > - **0단계 IO Scanner·④ AXS = 보류**(Straumann↔ES 데이터 흐름 협상) → **1·2·3단계 우선**.
      > - **③-P-CS CleverSpace·③-P-CO CleverOne OnePager 2개**(각 1·2·3단계=호환성+presigned+GW일원화 통합) **= Raymond·7/27 병행 착수**(deferred→active · CleverOne Nick→Raymond → 담당팀 전달).
      > - **①호환성·②Presigned One Pager 별도 미작성 → 두 제품 OnePager에 흡수**(딱 2개 문서 · presigned=CleverSpace 발급 API+CleverOne 이용, 둘 다 GW 경유라 양쪽 변경).
      > - ③ GW SRS = **baseline v1.0 동결(7/20)·spec-v1.0.1 정합화(7/22)**.
      > - ③-I Infra = **PR 7/21 생성·진행중**(Jack 상세) · ③-P-EZ EzServer 초안 = Raymond 진행중.
      > - **AWS 환경 4계층(dev·qa·stag·prod)** 결정 반영.
      > - CleverOne OnePager는 지금 작성(연동 *구현*만 post-v1.0).
      > - 순서·의존 = [Roadmap §3.9].

  - **S3. GW 구현 현황 — Phase·Task 스냅샷 (7/30·매주 갱신)** — 1단계(GW 독립 코어) 구현 진행중. 매 Task 완료 시 갱신. _(7/30 프레임 시작값 = 7/23 상태 · 주중 Task 완료 시 갱신)_
    - **진행 단계** — 스펙(분석/설계)과 구현을 분리해 진행한다. 스펙은 HLD로 baseline 동결됐고 현재 구현(LLD 병행) 중이다. 구현이 끝이 아니라, QA 인계 전 개발팀이 통합·시스템 테스트로 동작을 확증하는 단계가 남고, 이어 QA·운영이 있다.
      - **스펙 — 분석/설계(HLD)**: SRS·DBML·OpenAPI·TCL baseline v1.0 동결 · 정합화(v1.0.1~v1.0.4) 지속 · LLD는 구현과 병행
      - **구현(LLD 병행)** — _구현 단계 내 진척 ≈ 57%(코딩 Task 37/65 · region-silo 재작업으로 분모·분자 재산정 예정)_: 1단계 코어 **P0~P6 완료** · P10 예정 / 2단계 AXS 연동(P7~P12)은 ④ 연동 Spec 후 · Task별 검증 4종(unit·e2e·curl·DB)
      - **⚠ region-silo(R2·spec-v1.0.5) 재작업 예정분**: 아래 ✅완료 중 **P1 T-DATA-1-1(전역/리전 2-DB)·1-6(region_catalog 시드) · P3 T-ENR-3-2(GeoDNS default region 배정) · P4 전체(Region Resolver·GET /v1/regions·PUT /me/region·region 카탈로그 CRUD) · P6 T-PXY-6-2의 region 해석 단계**는 리전 완전 분리로 **삭제·단일화 대상**이다(단일 datasource·region=배포 상수·Region Directory·리전 변경=마이그레이션). 완료 이력은 보존하되, **스펙 PR(#12207) 머지 후 구현 세션에서 재작업**(구현세션 알림 v1.0.5).
      - **개발 통합·검증(QA 인계 전)**: 통합 테스트 · 시스템 E2E(실 계약: AXS·CleverSpace·EzServer) · 성능·부하 · HA·복원력 · 보안 검토 → 동작 확증 후 QA 인계
      - **QA**: 릴리스 회귀 · QA TCL · V&V 산출물(IEC 62304 / ISO 13485)
      - **운영·릴리스**: staging/prod 배포(인프라) · AXS pilot
    - **상태 범례**: ✅ 완료(main merge) · 🟡 부분완료(외부 선결로 일부 잔여) · 🟢 리뷰중(PR) · 🟠 구현중 · ⬜ 대기 · 🔴 외부 선결 대기. **표기 규칙**: Phase 내 전 Task 상태가 같으면 1행으로 묶고, 상태가 다르거나 **금주에 변화가 있으면** Task별로 펼친다.

      | Phase | Task | 설명 | 상태 | 비고 |
      | --- | --- | --- | --- | --- |
      | **P0 플랫폼 스캐폴드** | 0-1~0-4·0-6 | 4-way 스캐폴드·로컬환경·포트어댑터·더블·Prisma 파이프라인·관측·에러·Config·헬스·README | ✅ 완료 | PR #11971~11995 merge |
      | ″ | T-PLAT-0-5 | CI 파이프라인·Dockerfile | 🟡 부분완료 | PR #11994 merge · CI·스캔 완료 / 🔴 배포(main→DEV·tag prefix)는 Jack Azure 템플릿 수령 후 |
      | **P1 데이터 모델·마이그레이션** | T-DATA-1-1~1-5 | 전역/리전 스키마·raw-SQL 제약·KMS envelope·Redis 키스페이스·audit append-only | ✅ 완료 | PR #12006~12016 merge |
      | ″ | T-DATA-1-6 | region_catalog 시드(서울·default·self-heal) | ✅ 완료 | PR #12018 merge |
      | ″ | T-DATA-1-7 | 시드·테스트 데이터 인프라(prisma db seed·Factory·**E2E 반복성 하네스**) | ✅ 완료 | PR #12040 merge · **→ P1 완료** |
      | **P2 인증 토대** | T-AUTH-2-1 | private_key_jwt 검증→RS256 access token(`POST /v1/auth/token`)·키회전 대비 | ✅ 완료 | PR #12094 merge · 검증 4종·실 curl |
      | ″ | T-AUTH-2-2 | jti 1회소비(재사용 401)·rate-limit(검증후 정본 clientId·표적 lockout 차단)·revocation denylist(즉시 401) | ✅ 완료 | PR #12106 merge · unit 48·e2e 8/8(실 Valkey: replay·rate-limit 429@#31·revocation) |
      | ″ | T-AUTH-2-3 | deviceAuth Guard(per-controller·GW access token RS256 검증)+@CurrentDevice | ✅ 완료 | PR #12138 merge · unit 16·e2e 5/5(무토큰/위조/revoked 401) |
      | ″ | T-AUTH-2-4 | operator Entra OIDC 검증(confused-deputy 방어)+JIT operator(첫 SSO) | ✅ 완료 | PR #12141 merge · unit 26·e2e 6/6(OIDC mock+실 DB) |
      | ″ | T-AUTH-2-5 | operator_role RBAC(deny-by-default)+GET /v1/admin/me | ✅ 완료 | PR #12143 merge · unit 12·e2e 6/6 · **→ P2 완료**(device+operator 양면) |
      | **P3 enrollment·디바이스 생애주기** | T-ENR-3-1 | enroll 개시(부트스트랩·nonce challenge·IP rate-limit)·`POST /v1/enroll/start` | ✅ 완료 | PR #12158 merge · unit 10·e2e 5/5 |
      | ″ | T-ENR-3-2 | 서명·공개키 검증→device(pending)·clinic upsert·GeoDNS default region 배정·client_id 발급·`POST /v1/enroll/complete` | ✅ 완료 | PR #12166 merge · unit 24·e2e 7/7(재-enroll 회전·1회용·서명불일치)·curl·DB/Valkey |
      | ″ | T-ENR-3-3 | device 생애주기 상태머신(§7.2.3)·재-enroll 회전 시 옛 credential 폐기(denylist) | ✅ 완료 | PR #12168 merge · unit(전 전이·revoke on/off/실패)·e2e 재-enroll denylist |
      | ″ | T-ENR-3-4 | 승인 slice: PATCH 전이(승인·정지·재개·폐기)+kill(→revoked·denylist 전파)·RBAC(cs) (Admin) | ✅ 완료 | PR #12169 merge · unit 326·e2e 7/7·curl cross-app(kill→토큰 401) |
      | ″ | T-ENR-3-5 | 미승인 pending 기본 7일 후 자동 만료(background sweep·config·스팸 방지) | ✅ 완료 | PR #12171 merge · unit 5·e2e 4(경계·null created_at) · **→ P3 완료** |
      | **P4 레지스트리·region resolution** | T-REG-4-1 | Region Resolver(device/clinic→region·ADR-10)·mapping_version CAS·버전 조건부 캐시 | ✅ 완료 | PR #12173 merge · unit 11·e2e 5(CAS·H1 stale 방지) |
      | ″ | T-REG-4-2 | ClinicResolution(GET /v1/clinics/me·region·hosts·주권 phiEgress=false·self 격리)·GET /v1/regions(planned 제외) | ✅ 완료 | PR #12177 merge · unit(매퍼·폴백·주권불변)·e2e 5(self 404·무토큰 401·draining 노출) |
      | ″ | T-REG-4-3 | clinic 정보 보정(PATCH /me·ISO countryCode·self 격리)·접속 리전 재지정(PUT /me/region·mapping_version CAS·PHI-free audit·현재동일 no-op) | ✅ 완료 | PR #12185 merge · unit 32·e2e 8(self격리·audit_log·no-op)·curl·DB/audit 조회 · core 최초 regional Prisma+Audit 배선 |
      | ″ | T-REG-4-4 | PHI region-boundary 앱 내부 PDP(deny-by-default·coarse target 인가·리전경계·egress fail-closed·presigned guardrail·OPA는 gw/1.1+ 예약) | ✅ 완료 | PR #12187 merge · unit 42·통합 8(정책해석·리전경계·egress) · PEP 배선=P6 |
      | ″ | T-REG-4-5 | admin region 카탈로그 CRUD(isDefault 정확히1·참조/default 삭제 409)·operator clinic 리전 교정 | ✅ 완료 | PR #12191 merge · unit 29·e2e 22(RBAC·CRUD·audit) · **→ P4 완결** |
      | **P5 호환성 게이트** | T-CFG-5-1 | Vatech-\* 식별 헤더 파싱 미들웨어(originator vs Via·필수/semver 검증→400·CompatContext 부착) | ✅ 완료 | PR #12194 merge · unit 19·e2e 4(400 envelope·스코프) |
      | ″ | T-CFG-5-2 | well-known 매트릭스 서빙(`GET /.well-known/{env}/…`·ESO 마운트·경로탈출 차단·fail-closed 503) | ✅ 완료 | PR #12198 merge · unit 16·e2e 7·curl·DB미사용 |
      | ″ | T-CFG-5-3 | semver 3단계 게이팅(major 차단/minor 경고/patch 무시)·`@CompatGate` guard·worst-of | ✅ 완료 | PR #12200 merge · unit 26 · **→ P5 완결**(실 엔드포인트 배선은 매트릭스 값 확정 후) |
      | **P6 target-routed 프록시** | T-PXY-6-1 | 서브도메인 Host 라우터·target allowlist·SSRF fail-closed(업스트림=레지스트리만) | ✅ 완료 | PR #12203 merge · unit 27(SSRF 벡터·fail-closed) |
      | ″ | T-PXY-6-2 | PEP 체인(auth 401→PDP 403→region)·verbatim bypass(host 교체·target verbatim)·외부 토큰/헤더 유출 차단 | ✅ 완료 | PR #12208 merge · unit 555·e2e 프록시 왕복·전체 182 회귀0 |
      | ″ | T-PXY-6-3 | 프록시 복원력 — D1~D3 타임아웃(connect/response/total)·취소 전파·Vatech-Timeout-Ms 클램프·에러 정규화(502/503/504)·Idempotency-Key soft-state | ✅ 완료 | PR #12213 merge · unit 602·e2e 프록시 9(멱등 replay·principal 격리 실 Valkey 키)·전체 182 회귀0·독립리뷰 High2/Med2 반영 · **→ P6 완결**(실 AXS 왕복 E2E만 ④ 후) |
      | **P7 External Connector·AXS** | 전체 | OAuth2 cc·egress 고정IP·앱 PDP egress·org-binding·presigned 중계 | ⬜ 대기 | 🔴 2단계·④ AXS 실연동 후(보류) |
      | **P8 webhook 수신(Receiver)** | 전체 | HMAC·멱등·ACK·KMS 암호화 저장·SQS enqueue | ⬜ 대기 | 2단계(골격 로컬 더블 선행 가능) |
      | **P9 webhook 분배·MQTT(Dispatcher)** | 전체 | SQS consumer·대상해석·MQTT QoS1 하행·DLQ | ⬜ 대기 | 2단계 |
      | **P10 fleet·중앙 config·inventory** | 전체 | heartbeat·fleet_state·online 파생·config(gw.\*)·inventory | ⬜ 대기 | 1단계 |
      | **P11 Admin API·audit·컴플라이언스** | 전체 | 전 CRUD·RBAC 생애주기·break-glass·audit 전면 | ⬜ 대기 | 2단계(webhook slice=P8 후) |
      | **P12 E2E·하드닝** | 전체 | AXS sandbox E2E·compat E2E·부하·HA/KEDA 검증 | ⬜ 대기 | 🔴 2단계·④ AXS sandbox 실자격 |

      > **금주 구현 요약(7/30 · 주중 진척 반영)** — 1단계 GW 독립 코어에서 **P2~P6 다섯 Phase를 완결**했다. **P2 인증**: device 면(2-1 private_key_jwt→RS256 토큰, 2-2 jti 1회 소비·검증후 정본 clientId rate-limit·revocation denylist, 2-3 deviceAuth Guard)에 operator 면(2-4 Entra OIDC+confused-deputy 방어+JIT, 2-5 RBAC deny-by-default+`/v1/admin/me`)을 더해 양 인증면을 완비. **P3 enrollment**: 개시/완료(3-1·3-2)에 이어 device 생애주기 상태머신·재-enroll 회전 옛 credential 폐기(3-3)·C/S 승인 slice+kill 즉시 denylist 전파(3-4)·미승인 pending 자동만료(3-5)로 종료. **P4 레지스트리·region resolution**: Region Resolver(mapping_version CAS·버전 조건부 캐시·4-1)·ClinicResolution+GET /v1/regions(4-2)·PATCH /me+PUT /me/region(4-3)·PHI region-boundary 앱 내부 PDP(4-4)·admin region 카탈로그 CRUD(4-5)로 완결. **P5 호환성 게이트**: Vatech-\* 파싱→400(5-1)·well-known 매트릭스 서빙(5-2)·semver 3단계 게이팅 guard(5-3). **P6 target-routed 프록시**: 서브도메인 라우터+SSRF fail-closed(6-1)·PEP 체인(auth 401→PDP 403→region)+verbatim bypass(6-2)·아웃바운드 복원력(6-3 D1~D3 타임아웃·취소 전파·에러 정규화·Idempotency-Key)로 완결. 모든 엔드포인트 Task에 **검증 4종(unit·e2e[실 DB·Valkey]·curl 왕복·DB/Valkey 조회)** 과 **E2E 반복성 하네스**(clean-slate·seed·FLUSHDB)를 적용했고, 보안 민감 Task(프록시·인증)는 **독립 적대적 pre-PR 리뷰**로 검증했다.
      >
      > - **데이터 모델의 적용 범위**: 데이터 계층은 **4개 앱이 공유하는 하나의 공통 자산**이다(앱별로 나뉘지 않음). DB(전역 `gw_global`·리전 `gw_regional`)와 Prisma 스키마·공용 헬퍼는 `libs/common`에 **한 벌만** 두고 core·admin·receiver·dispatcher가 함께 쓴다.
      > - **다음**: region-silo(R2·spec-v1.0.5·PR #12207) 머지 후 **일부 완료분 재작업**(P4 전체·P1/P3/P6 리전 해석 단계 → 단일 datasource·region=배포 상수·Region Directory·리전 변경=마이그레이션) → 1단계 잔여 **P10 fleet·config·inventory**. AXS 연동부(P7~P12)는 2단계(④ AXS 보류 해제 후).

  - **S4. 스펙 게시본 — Project wiki 자동 미러 가동 (비개발자도 스펙 열람 가능)** — 스펙 문서 관리 표준(§9 게시·참조)의 **project wiki 자동 미러**를 vt-api-gateway 에 구현·가동했다. 이제 **Git 접근·개발 라이선스가 없는 비개발자(기획·PM·QA·외주)도 스펙을 열람**할 수 있다(개발자는 Git `docs/` 정본 직접 열람).
    - **정본↔게시본 분리(baseline 불변)**: 정본은 Git(`docs/specs/`) 그대로 두고, 게시본은 **읽기전용 단방향 미러**. main 병합 시 전용 파이프라인 `.azure-pipelines/docs-wiki.yml`(PAT 인증)이 `es-platforms.wiki/vt-api-gateway/` 하위로 자동 push → **drift 없음**. wiki 직접 편집 금지(편집은 Git 정본에서만).
    - **왜 project wiki 인가**: code wiki 는 Basic 이상만 열람되지만 **project wiki 는 Stakeholder(무료)도 열람 가능** → 비개발 열람 보장(표준 §9 상단).
    - **게시 확인(SRS 예)**: [SRS 게시본](https://dev.azure.com/ewoosoft/es-platforms/_wiki/wikis/es-platforms.wiki/549/SRS) — `docs/specs/*.md`(SRS·UnitTCL·design·Sub-SRS)만 미러(openapi.yaml·dbml·`references/` 벤더 사본은 제외·중첩 구조 유지).
    - **비개발자 열람 온보딩(표준 §9.3)**: 대상자를 조직에 **Stakeholder(무료)** 로 초대 + 프로젝트 **Readers** 부여 → 회사 계정 로그인 후 게시본 URL 열람. (안 보이면 Access level=Stakeholder·Readers 소속 확인 — code wiki·Repos 는 Stakeholder 제한, project wiki 만 열람 가능.)
    - **재사용**: 동일 파이프라인 패턴을 타 repo(③-C Console·③-I infra 등)에도 적용 가능(제품별 하위 폴더 격리). 표준 정본 = `스펙 문서 관리 표준 (저장·리뷰·참조).md` §9.1(검증 완료 패턴).

  - **S5. CI 회귀 게이트 완성 — 모든 PR이 실 DB/Valkey 통합 e2e 검증 (품질 인프라)** — 그동안 **루트 CI 파이프라인이 미등록**이라 `lint·build·unit·e2e`가 CI 에서 한 번도 안 돌았고(도는 건 devsecops gitleaks/trivy 스캔뿐), 통합 e2e 15 스위트는 `RUN_DB_INTEGRATION` 게이트라 **CI 에서 전부 스킵**되던 회귀 공백이 있었다. 이를 해소했다.
    - **활성화**: e2e 하네스(globalSetup)가 CI 에서 백킹 서비스(Testcontainers)를 기동·엔드포인트 주입·부팅 시크릿(GW 서명키) 생성·migrate/seed 를 자동 수행 → **실 DB/Valkey 통합 e2e 가 CI 에서 실제 실행**(파이프라인 yml 변경 없음). Jack 의 **Node 24·es-base 마이그레이션(PR #12163)과 통합**.
    - **게이트화**: 파이프라인 `vt-api-gateway-ci` 등록 + **main 브랜치 정책(Build validation·Required)** 추가 → **모든 PR 이 lint·build(4타겟)·unit(342)·통합 e2e(121)·dep-scan 을 통과해야 머지**. devsecops 4종(gitleaks/trivy)과 함께 5개 필수 게이트.
    - **검증**: CI 실측 green(Node 24·build 48736 — 전 게이트 통과). **효과**: 회귀 그물망이 로컬 전용에서 **CI 전면**으로 확대(baseline 통제 품질 강화). **참고**: PR 당 CI ~15~20분(Testcontainers e2e 포함).

- 이월 논의 사항 (6/25·7/2·7/9 미결 — 계속)

  | # | 항목 | 타입 | 상태 |
  | --- | --- | --- | --- |
  | 4 | Webhook 클라우드 분배(CleverLab 갈래B) | [논의] | v1.0 제외 — Open 후 결정 |
  | 6 | AXS sandbox 자격증명(Straumann 제공) | [정보] | pilot·E2E 블로커 — 확보 시점?(협상중) |
  | 7 | 경로 B EOS 시점 | [논의] | 리뷰서 workaround·지속성 확정(§2.8) — EOS *시점*만 PM·CS/CO OnePager 미정(①흡수) |
  | 8 | v1.0 목표 RPS·동시 세션 | [정보] | 인프라/규모 PL 입력 대기 |
  | 9 | RTO/RPO·유지보수 윈도우 | [정보] | 인프라 설계 단계 — failover 요건은 R2(저장소 전역일관 vs 리전분리·Q3) 결정과 연계 |
  | 10 | 감사·consent 보존 기간 | [정보] | 법무 확인 대기 |
  | 11 | 호환성 매트릭스 확정본 | [정보] | CleverSpace/CleverOne OnePager 의존(①폐지·흡수) — 초안 7/27 작성·확정값은 담당팀 baseline 후 |
  | 14 | 관측성 앱↔인프라 계약 확정 — ①로그 필드 스키마(현행 pino 기본 필드 ↔ §6.3.2 최소셋 매핑·Appendix B #14) ②메트릭 export 배선(OTLP reader→Grafana Alloy 엔드포인트) | [논의·설계] | **추후 확정** — 트리거=③-I 관측 스택 구축 or P6 프록시 착수(먼저). Raymond 초안(필드 매핑표+엔드포인트 요구)→Jack(인프라) 비동기 합의. **앱 계약(stdout JSON+OTel·redaction) 이미 구현·무블로킹** |
  | 이월-R1 | IO Scanner↔EzServer 연동 방식 | [논의·선결] | **보류(7/23 결정)** — 이번 주 논의 「Straumann↔ES 데이터 흐름 협상」 결과에 종속(결정 시 이월-R1·④ AXS scope 착수 조건 확정) |
  - **차주 이월 후보**: 이월-R1(IO Scanner↔EzServer 연동 방식·**보류**)·이월-R2(목표일정·출시일 재검토) 미확정 시 다음 주 이월.

# VT API Gateway — 8/6 주간회의 Agenda

> 7/30 스냅샷(위 「7/30 주간회의」)은 **그대로 보존**. 아래는 **8/6 최신 스냅샷(틀)** 이며, 틀(논의/공유/이월)은 이전 주와 동일하다. **Gantt(S1)·스펙 작성 테이블(S2)은 매주 상시 포함**한다. _※ 이 문서는 8/6 회의 전 준비한 **프레임**으로, `(프레임)` 표시 항목은 회의 시 확정한다._

- 이번 주 진행 _(프레임 · 8/6 회의 시 확정 · 상세·수치는 아래 논의 R#/공유 S# 한 곳에만)_
  - **(8/3 완료) region-silo(R2) — 스펙 + 구현 코드 재작업 모두 완료** → 규모·검증 상세 = 공유 S5 · 구현현황 = S3
  - **(확정) R2-1** — 호주 first-open · 서울=dev · 대량 이전 없음 → 공유 S5
  - **(확정) R3·R4·R5** — 제품 OnePager 인계 방식 · GW 도메인 별도 · GW Console v1/v2 분리 → 공유 S5
  - **(8/3 완료) GW 구현 1단계 완성** — 코어 P0~P6 + **P10 완결**(heartbeat·ConfigService·inventory·admin 조회·PR #12363·12364·12366·12368) → **2단계 P8 webhook Receiver 골격 완료**(head-start·로컬 더블 — 8-1·8-2·8-3·실연동 ④ 후) → 구현현황 = S3
  - **(진행 중 실무) AWS 환경 분리** — 계정/네트워크·ESO/Parameter Store 경로·`.env.template`(Jack·Raymond·③-I) · 이번 주 GW_REGION dev 프로비저닝 진행
  - **(잔여) EzServer OnePager 수령 확인** · 보류·선결(IO Scanner=`이월-R1`)은 이월 표 참조

- 논의 사항 (이번 주 · 신규 논의/결정 안건)
  - **신규 논의 안건 없음** — 이번 주 확정분(R2·R2-1·R3·R4·R5) = 진행 요약 + 공유 S5 · 진행 중 실무(AWS 환경 분리)는 이번 주 진행 · 보류·선결(IO Scanner↔EzServer = `이월-R1` 등)은 아래 「이월 논의 사항」 표 참조.
  - _(회의 중 신규 안건 발생 시 여기 추가)_

- 공유 사항 (결정 아님 · 정보 공유 · 매주 상시)
  - **S1. 프로젝트 일정(Gantt) — 8/6 스냅샷** — 스펙 생애주기(작성→PR→baseline) + GW 구현 타임라인.
    - **정본** = [개발 Roadmap 결정 §3.9](<VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>) (수정은 그쪽 먼저 · 7/23→7/30 변경은 정본 §3.9 동기화 완료).
    - **7/30→8/6 변경**:
      - region-silo(R2): 스펙 PR #12207/#12231 머지 + **구현 코드 재작업 PR #12241 머지(8/3) 완료**(단일 datasource·리전 API 삭제·139 files −3,853줄)
      - P6 프록시 완결(6-1~6-3)
      - R2-1 확정(서울=dev·호주 먼저 오픈)
    - **직전 7/23→7/30 변경 유지**:
      - 0단계 IO Scanner·④ AXS = 보류(Straumann 협상)
      - ③-P-CS CleverSpace·③-P-CO CleverOne OnePager 2개 = Raymond·7/27 병행 착수(각 1·2·3단계 통합 · ①호환성·②Presigned One Pager 폐지→두 제품 OnePager에 흡수 · CleverOne Nick→Raymond)
      - 1·2·3단계 우선
    - **막대 색**: 작성=기본 · PR=강조 · ◆=baseline/마일스톤 · 빨강=외부/미정 선결
    - **선결(빨강)**: IO Scanner↔EzServer 연동방식(**보류·R1**) · AXS sandbox 자격(Straumann)
    - **목표 = 10월 출시**(역산·잠정 — ④ AXS/IO Scanner 보류로 **2단계 일정·출시일 재검토 대상**)
    - **병행 별도 프로젝트**: `SectionView Module 구현`(7/13~2주·Raymond·**GW 아님**·완료)은 `▷ 병행` 섹션에 표기
    - **GW 구현 = 2단계 병행(유지)** — 1단계 GW 독립 코어(P0~P6·P10)는 ③ baseline 고정으로 **정상 진행**(IO Scanner 보류 영향 없음). 2단계 AXS 연동(P7~P12)만 ④ AXS 보류에 연동되어 **후행**.
    - (결정)
      - GW Console v1.0 최소기능으로 앞으로 당겨서 진행한다. 전규현/ Raymond
      - GW Console
        - MS Entra로 연동
        - infra
          - istio로 admin api 접근권한 제어
          - 페이지접근도 ZeroTrust 에서만 접근 가능하게한다.

    ```mermaid
    gantt
        title v1.0 = Straumann IO Scanner 연동 — 10월 출시 목표(역산·잠정) · 7/23 결정(IO Scanner 보류·1·2·3단계 우선) 반영
        dateFormat YYYY-MM-DD
        axisFormat %m/%d
        todayMarker stroke-width:3px,stroke:#d33,opacity:0.6

        section ③ GW SRS + API/DBML (계약 SSOT · baseline v1.0 동결)
        작성 (본문+OpenAPI·DBML)       :done, srsw, 2026-06-15, 28d
        PR 리뷰·수정                  :done, srspr, 2026-07-13, 2026-07-20
        baseline v1.0 (7/20 확정·spec-v1.0.1 정합화 7/22) :milestone, done, srsbl, 2026-07-20, 0d

        section GW 구현 → E2E → 출시 (③ SRS 완료 직후 착수 · 2단계 병행 · Raymond 부분투입)
        1단계 GW 독립 코어 (③ 고정·④무관·P0~P6·P10·진행중) :active, implindep, 2026-07-21, 45d
        2단계 AXS 연동 (P7~P12·④ AXS 보류 해제 후)   :implaxs, after implindep, 40d
        AXS E2E (sandbox)              :e2e, after implaxs, 14d
        개발환경 연동 완료(9월·R2)       :milestone, dev9, 2026-09-30, 0d
        v1.0 production 연동 완료(10월·R2·재검토) :milestone, rel, 2026-10-31, 0d

        section ③-I 인프라 IaC (① 초안+PR=Raymond → ② Jack 상세·리뷰·수정(PR #11973 병합 7/27) → 계획서 병합=완료·baseline tag 불요 · AWS dev·qa·stag·prod)
        ① 초안+PR (Raymond·diagram+요구추출) :done, infw, 2026-07-20, 2d
        ② Jack 상세작성·리뷰·수정 (PR #11973 병합 7/27) :done, infpr, 2026-07-21, 6d
        ③ 계획서 PR 병합 완료 (baseline tag 불요·living doc) :milestone, infbl, 2026-07-27, 0d
        Infra 구축·자동배포 완료(8월·R2) :milestone, infra8, 2026-08-31, 0d

        section ③-P-EZ EzServer 연동 스펙 (① 초안+PR=Raymond → ② Teddy 상세·리뷰·수정 → ③ baseline · IO Scanner부=보류)
        ① 초안+PR (Raymond·기본 GW연동) :done, ezw, 2026-07-20, 5d
        ② Teddy 상세작성·리뷰·수정 :active, ezpr, after ezw, 14d
        ③ baseline :milestone, ezbl, after ezpr, 0d

        section ③-P-CS CleverSpace OnePager (① 초안+PR=Raymond → ② CleverSpace팀(Larry) 상세·리뷰·수정 → ③ baseline)
        ① 초안+PR (Raymond·PR #12239·EzCloud) :done, cssub, 2026-07-27, 5d
        ② CleverSpace팀(Larry) 상세작성·리뷰·수정 :active, cspr, after cssub, 14d
        ③ baseline :milestone, csbl, after cspr, 0d

        section ③-P-CO CleverOne OnePager (① 초안+인계=Raymond·SharePoint → ② CleverOne팀(Nick) 상세·리뷰·수정 → ③ baseline)
        ① 초안+인계 (Raymond·SharePoint gw_adaptation) :done, cosub, 2026-07-27, 5d
        ② CleverOne팀(Nick) 상세작성·리뷰·수정 :active, copr, after cosub, 14d
        ③ baseline :milestone, cobl, after copr, 0d

        section ④ AXS Sub-SRS · IO Scanner (보류 — 7/23 결정: 0단계 IO Scanner 보류·Straumann 협상)
        IO Scanner↔EzServer 연동방식 확정(보류·선결·R1) :crit, ezm, after cosub, 21d
        작성 (IO Scanner scope · Straumann 협상 후) :axsw, after ezm, 21d
        PR 리뷰·수정                  :axspr, after axsw, 14d
        baseline                      :milestone, axsbl, after axspr, 0d
        AXS sandbox 자격(Straumann·선결) :crit, cred, 2026-08-18, 21d

        section ③-C GW Console v1.0 (Flow 최소기능·MS Entra·Istio admin·ZTNA · 9월 착수·전규현/Raymond)
        v1.0 최소 스펙+구현 (Flow 동작 최소·9월 착수) :conv1, 2026-08-10, 28d
        v1.0 최소기능 완료             :milestone, conv1m, after conv1, 0d
        section ③-C GW Console v2 (온보딩·Org 관리 화면 등 확장 — 후속)
        v2 확장 스펙+구현 (10월 중순 착수) :conv2, 2026-9-25, 28d
        baseline/확장 완료             :milestone, conv2m, after conv2, 0d

        section v1.0 이후 (deferred · post-v1.0)
        CleverOne 연동 *구현* (스펙은 지금·구현 post-v1.0) :codef, after rel, 14d

        section ▷ 병행 · 별도 프로젝트 (GW 아님)
        SectionView Module 구현 (Raymond·완료) :done, sv, 2026-07-13, 2026-07-30
    ```

  - **S2. 스펙 작성 테이블 — 제품별 개발 항목 종합 (제품 × 단계) · 매주 스냅샷** · 정본=[Roadmap §4](<VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>) (수정은 그쪽 먼저)
    - **각 셀 앞 이모지 = 그 항목을 다루는 스펙의 작성 진행**: ✅ baseline · 🟢 PR · 🟡 작성중 · ⬜ 미작성 (— = 해당 없음)

      | 제품 | 0단계(IO Scanner 수집·**보류**·R1) | 1단계(호환성) | 2단계(presigned) | 3단계(GW 일원화) | 4단계(멀티리전) | 5단계(Straumann) | 후속 | 스펙 산출물(단위·유형) |
      | --- | --- | --- | --- | --- | --- | --- | --- | --- |
      | **CleverSpace** | — | 🟡 서버 버전 체크·well-known·오류코드 | 🟡 presigned 발급 API 신규 | 🟡 GW 경유 수신 정합 | ⬜ 멀티 Region 구축 | — | — | **🟢 ③-P-CS CleverSpace OnePager 인계(PR #12239·EzCloud `docs/onepager/gw_adaptation`)** — CleverSpace 팀(Larry) 검토 |
      | **CleverOne**(OnePager 지금·연동 구현 post-v1.0) | — | 🟡 Vatech-\* 헤더·well-known·fallback | 🟡 presigned 업로드 이용 | 🟡 Direct→GW 경유 | ⬜ Region 선택 UI(대안)·ClinicID | — | — | **🟢 ③-P-CO CleverOne OnePager 인계(SharePoint gw_adaptation)** — CleverOne 팀(Nick) 검토 · 담당=Nick·작성=Raymond |
      | **EzServer(EZ)** | ⬜ IO Scanner 데이터 수신(방식 R1·**보류**·TBD) | 🟡 헤더 대리 전달 | 🟡 전송 로직(presigned 직접) | 🟡 GW 경유 전환 | 🟡 ClinicID·Region·클리닉 등록(잠정) | 🟡 AXS(갈래A)·presigned 직접(IO Scanner 세부=TBD) | ⬜ Rust 재개발 | **🟡 ③-P-EZ One Pager 초안 작성됨**(Raymond→EzServer 팀) — `specs/03p-ez-ezserver/EzServer-GW적응-OnePager.md` · ④(갈래A) |
      | **IO Scanner(Straumann 장비·수집 제품 미정)** | ⬜ 스캔 데이터→EzServer 유입(**보류**·수집 제품·방식 이월-R1·미정·Straumann 협상) | — | — | — | — | (AXS 워크플로 대상) | — | 이월-R1 확정 후 ③-P-EZ(수신)·④(AXS scope) |
      | **CleverLab** | — | — | — | — | — | ⬜ AXS 오더·상태·확정(갈래B)·presigned | — | ④ Sub-SRS(갈래B) |
      | **VatechAPIGateway** | — | 🟢 ↳3단계 흡수(호환 게이트·§7.7) | 🟢 ↳3단계 흡수(presigned 중계·§4.1.4) | 🟢 본체·라우팅·인증·호환·presigned 중계·경로B 흡수 | 🟢 리전 라벨 호스트·Region Directory·HA(K8s)·Route53·RDS(리전 단일) | ⬜ AXS OAuth 중계·Org-ID·온보딩·인바운드·고정IP | — | **③ SRS ✅ baseline(spec-v1.0.4)** · region-silo `spec-v1.0.5` PR 리뷰중 · ④ connector ⬜(보류) |
      | **GW Console** | — | — | — | — | 🟡 Admin Web Console v1.0 최소(MS Entra·Istio admin 제어·ZTNA 페이지 접근) | ⬜ 온보딩·Org-ID 관리 화면(v2) | — | ⬜ ③-C Sub-SRS v1.0 최소기능 **9월 착수 예정**(R5 당김 결정·전규현/Raymond) |
      | **인프라** | — | — | — | 🟢 dev·qa·stag(단일 Region)·prod(Region별) | 🟢 Route53·K8s·비-AWS minio | 🟢 AXS 고정IP·샌드박스 | — | **🟢 ③-I IaC 구축 계획서 — PR #11973 병합(7/27)·Jack 상세 반영**(Raymond diagram+SRS추출→Jack) — 정본 `vt-api-gateway-infra` · **baseline tag 불요**(living doc) · **AWS 4계층** · **+ 8/4 KMS 키 토폴로지 provisioning ask**(spec-v1.0.7·handoff-infra 항목5 — 리전별 CMK `gw-payload`/`gw-target-cred`·pod별 grant·dev payload CMK 선생성) |
      | **외부(Straumann AXS)** | — | — | — | — | — | ⬜ API·OAuth·샌드박스·자격증명(선결·**협상중**) | — | ④ 입력(외부 제공) |
      | **LMP(License Portal, 바텍)** | — | — | — | — | — | — | ⬜ (조건부) 제3자 서명 attestation | **enroll B안 시만**·ES 라이선스팀(R9·B-42) |

    - **스펙 문서 등록처·경로·baseline (SSOT)** — 각 제품 스펙 정본의 Repo·경로·태그. _(미정 = R3에서 등록처 확정 · OnePager는 담당팀 baseline 시 tag 부여)_

      | 단위 | 스펙 문서 | Repo (Azure DevOps) | 경로 | baseline tag |
      | --- | --- | --- | --- | --- |
      | **③ GW** | SRS(+OpenAPI·DBML·UnitTCL) | `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway` | `docs/specs/SRS.md` · `docs/specs/design/`(openapi·dbml) · `docs/specs/UnitTCL.md` | **`spec-v1.0.4`**(최신 baseline) · region-silo `spec-v1.0.5`(PR 리뷰중) |
      | **③-C GW Console** | Sub-SRS | `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-console` (별도 repo·GW 소유→이관) | 미작성(신규 repo·경로 TBD) | 미작성(연기) |
      | **④ AXS** | Sub-SRS | 〃 vt-api-gateway (GW 소유) | `docs/specs/04-subsrs-straumann-axs/` | 미작성(보류) |
      | **③-I 인프라** | IaC 구축계획서 | `https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway-infra` | `docs/IaC-구축계획서.md` | **PR #11973 병합(7/27)** · baseline tag 불요(living doc) |
      | **③-P-EZ EzServer** | GW적응 OnePager | `https://dev.azure.com/ewoosoft/ezserver/_git/ezserver_suite` (branch `v6.5.x`) | `doc/onepager/gw_adaptation/Confidential_gw_adaptation_onepager.md` | 미부여(EzServer 팀 baseline 예정·R3 확인) |
      | **③-P-CS CleverSpace**(=EzCloud) | GW적응 OnePager | `ezicloud/ezcloud`(https://dev.azure.com/ewoosoft/ezicloud/_git/ezcloud) | `docs/onepager/gw_adaptation/CleverSpace-GW적응-OnePager.md` | **PR #12239**([링크](https://dev.azure.com/ewoosoft/ezicloud/_git/ezcloud/pullrequest/12239))·팀 baseline 예정 |
      | **③-P-CO CleverOne** | GW적응 OnePager | SharePoint `ProjectDoc/Clever One/srs/OnePager/gw_adaptation`([문서](https://vatechcorp.sharepoint.com/:t:/s/es/IQC500caygYpS78euV2xO5WyAfzZF2kbz_09J20UbackH2k?e=tQLWOJ) · [폴더](https://vatechcorp.sharepoint.com/sites/es/ProjectDoc/Forms/AllItems.aspx?id=%2Fsites%2Fes%2FProjectDoc%2FClever%20One%2Fsrs%2FOnePager%2Fgw%5Fadaptation&viewid=5a018594%2D6322%2D4139%2Db7ee%2De9dd4aa4d23a&p=true&ga=1)) | 〃(SVN 제품·git 아님) | — (SharePoint·team baseline) |
      | **③-P-LMP LMP** | OnePager(조건부) | **미정 (ES 라이선스팀?)** | — | — |
      | **CleverLab** | ④ Sub-SRS(갈래B) | 미정 (보류) | — | — |

      > **8/6 진행(7/30 반영)**
      >
      > - **0단계 IO Scanner·④ AXS = 보류**(Straumann↔ES 데이터 흐름 협상) → **1·2·3단계 우선**.
      > - **③-P-CS CleverSpace·③-P-CO CleverOne OnePager 2개**(각 1·2·3단계=호환성+presigned+GW일원화 통합) **= Raymond·7/27 병행 착수**(deferred→active · CleverOne Nick→Raymond → 담당팀 전달).
      > - **①호환성·②Presigned One Pager 별도 미작성 → 두 제품 OnePager에 흡수**(딱 2개 문서 · presigned=CleverSpace 발급 API+CleverOne 이용, 둘 다 GW 경유라 양쪽 변경).
      > - ③ GW SRS = **baseline v1.0 동결(7/20)·spec-v1.0.1 정합화(7/22)**.
      > - ③-I Infra = **PR #11973 병합 완료(7/27)**(Jack 상세·baseline tag 불요·living doc) · ③-P-EZ EzServer 초안 = Raymond→Teddy 상세.
      > - **AWS 환경 4계층(dev·qa·stag·prod)** 결정 반영.
      > - CleverOne OnePager는 지금 작성(연동 *구현*만 post-v1.0).
      > - 순서·의존 = [Roadmap §3.9].

  - **S3. GW 구현 현황 — Phase·Task 스냅샷 (8/6·매주 갱신)** — 1단계 코어 완료 · 2단계 P8 착수.
    - **어디까지 왔나 (8/6)**: 1단계 코어(P0~P6·P10) 구현 완료. 2단계는 **P8 골격 완료(8-1·8-2·8-3) + P9 골격 app-side 완료(9-1·9-2·9-3 소비·분배·DLQ·무유실)** — 로컬 더블 기준, 실연동은 ④ AXS 후. **다음 = P11 Admin CRUD**(④ 무관·자율 진행 중). **P7·P12·P9-KEDA/IoT는 ④ AXS·인프라 선결로 대기.** 구현 다음 통합·검증·QA 단계가 이어진다.
    - 매 Task 완료 시 갱신 · _8/6 프레임 시작값 = 7/30 상태 · **8/3 region-silo 재작업 머지(PR #12241 → `9146ae3`) 반영**_
    - **진행 단계** — 스펙(분석/설계)과 구현을 분리해 진행한다. 스펙은 HLD로 baseline 동결됐고 현재 구현(LLD 병행) 중이다. 구현이 끝이 아니라, QA 인계 전 개발팀이 통합·시스템 테스트로 동작을 확증하는 단계가 남고, 이어 QA·운영이 있다.
      - **스펙 — 분석/설계(HLD)**: SRS·DBML·OpenAPI·TCL baseline v1.0 동결 · 정합화(v1.0.1~v1.0.4) 지속 · LLD는 구현과 병행
      - **구현(LLD 병행)** — _구현 단계 내 진척(코딩 Task) · region-silo 재작업(8/3·PR #12241) 완료로 **P4 대부분 삭제·단일화** → Task 집합 축소·재산정 예정_: 1단계 코어 **P0~P6·P10 완료 + region-silo 재작업 완료** · 2단계 **P8 골격 완료(8-1·8-2·8-3)·P9 착수(9-1)** / P7·P11·P12는 ④ 연동 Spec 후 · Task별 검증 4종(unit·e2e·curl·DB)
      - **✅ region-silo(R2·spec-v1.0.5/1.0.6) 재작업 완료(8/3·PR #12241 머지 `9146ae3`)**: 아래 ✅완료 중 **P1 T-DATA-1-1(전역/리전 2-DB)·1-6(region_catalog 시드) · P3 T-ENR-3-2(GeoDNS default region 배정) · P4 전체(Region Resolver·GET /v1/regions·PUT /me/region·region 카탈로그 CRUD) · P6 T-PXY-6-2의 region 해석 단계**가 리전 완전 분리로 **삭제·단일화됨**(단일 datasource·region=배포 상수·Region Directory·리전 변경=마이그레이션·ClinicResolution=리전 echo·하드 FK). **완료 이력은 아래 표에 보존**(당시 PR 기준)하되 현행 코드는 단일 datasource. 검증: unit 534·e2e 157·CI green(build 20260803.1)·`verify-spec`/`verify-ci` 게이트 신설.
      - **개발 통합·검증(QA 인계 전)**: 통합 테스트 · 시스템 E2E(실 계약: AXS·CleverSpace·EzServer) · 성능·부하 · HA·복원력 · 보안 검토 → 동작 확증 후 QA 인계
      - **QA**: 릴리스 회귀 · QA TCL · V&V 산출물(IEC 62304 / ISO 13485)
      - **운영·릴리스**: staging/prod 배포(인프라) · AXS pilot
    - **상태 범례**: ✅ 완료(main merge) · 🟢 리뷰중(PR) · 🟠 구현중 · ⬜ 대기 · 🔴 외부 선결 대기. **표기 규칙**: **7/30 이전 완료분 = Phase 단위 묶음 · 7/30 이후 구현(region-silo 재작업) = Task 단위 전개 · 미착수 = Phase 단위.**

      **① 7/30 이전 완료 — Phase 단위 (묶음)**

      | Phase | Task 범위 | 상태 | 대표 PR |
      | --- | --- | --- | --- |
      | **P0 플랫폼 스캐폴드** | 0-1~0-6 (4-way 스캐폴드·로컬환경·포트어댑터·더블·Prisma·관측·에러·Config·헬스·README·**CI·Dockerfile**) | ✅ 완료 | #11971~11995 · **CI=`azure-pipelines.yml`(우리)** · **CD=`.azure-pipelines/`(Jack·devsecops 4앱+promote)** |
      | **P1 데이터 모델·마이그레이션** | 1-1~1-7 (스키마·raw-SQL 제약·KMS envelope·Redis 키스페이스·audit append-only·시드 하네스) | ✅ 완료 → **8/3 단일 datasource 재작업(②)** | #12006~12040 |
      | **P2 인증 토대** | 2-1~2-5 (device private_key_jwt→RS256 + operator Entra OIDC·RBAC) | ✅ 완료 | #12094~12143 |
      | **P3 enrollment·생애주기** | 3-1~3-5 (개시/완료·상태머신·재-enroll 회전·C/S 승인·kill·pending 자동만료) | ✅ 완료 → **region 배정 삭제(②)** | #12158~12171 |
      | **P4 레지스트리·region resolution** | 4-1~4-5 (Resolver·ClinicResolution·PATCH/PUT me·PHI PDP·카탈로그 CRUD) | ✅ 완료 → **region-silo로 대부분 삭제·단일화(②)** | #12173~12191 |
      | **P5 호환성 게이트** | 5-1~5-3 (Vatech-\* 파싱→400·well-known 서빙·semver 게이팅) | ✅ 완료 | #12194~12200 |
      | **P6 target-routed 프록시** | 6-1~6-3 (라우터·SSRF·PEP 체인·verbatim bypass·복원력) | ✅ 완료 → **region 해석 단계 삭제(②)** | #12203~12213 |

      > **T-PLAT-0-5 확정(8/3)**: 우리 CI(`azure-pipelines.yml`·lint/build/unit/e2e/scan)+Dockerfile **완료** · 배포(CD)는 Jack `.azure-pipelines/`(devsecops 4앱+promote-qa/prod) **별도 소관·운영 중**(dev 배포됨). 옛 "🔴 배포 Jack 템플릿 수령 후" blocker 해소 → **P0 전체 ✅**.

      **② 7/30~8/3 구현 — Task 단위 (풀기) · region-silo 재작업(R2·PR #12241 머지 `9146ae3`)**

      | Task | 내용 | 상태 | 검증 |
      | --- | --- | --- | --- |
      | 스키마·마이그레이션 | 전역/리전 2-DB → **단일 datasource** · baseline squash · 하드 FK · NULLS NOT DISTINCT · audit append-only 트리거 | ✅ 완료(8/3) | migrate deploy·정적/실DB e2e |
      | config·리전 상수 | `GW_REGION` 배포 상수 · `DATABASE_URL` 단일 · `GW_PUBLIC_HOST` · 앱별 단일 PrismaService | ✅ 완료 | config unit |
      | API·런타임 | **Region Resolver·GET/PUT `/v1/regions`·region_catalog CRUD·GeoDNS 배정 삭제** · ClinicResolution=리전 echo · proxy PEP region 해석 제거 | ✅ 완료 | e2e·curl |
      | 테스트·감사 | e2e/unit 재정합(**534/157**) · 9-파티션 전수 정독 감사 · 폐기개념 grep 0 · **CI e2e 401 회귀 수정**(token aud=config 동기화) | ✅ 완료 | 검증 4종·CI green |
      | 게이트·문서 | `make verify-spec`·`verify-ci` 신설 · README 드리프트 정정(#12348) | ✅ 완료 | — |

      **②-b P10 fleet·config·inventory — Task 단위 (8/3 완결 · 1단계 마무리)**

      | Task | 내용 | 상태 | PR |
      | --- | --- | --- | --- |
      | 10-1 heartbeat | POST /v1/fleet/heartbeat·fleet_state upsert·nextIntervalSeconds·device_id=토큰 subject·metrics 미저장 | ✅ 완료 | #12363 |
      | 10-2 ConfigService | 중앙 config(gw.*) 실효 resolve(device>clinic>region>global)·pull 엔드포인트·configVersion는 gw/1.1 이월 | ✅ 완료 | #12364 |
      | 10-3 inventory | 클라 SW 인벤토리 튜플 presence·os sentinel·Redis SET NX throttle·fire-and-forget | ✅ 완료 | #12366 |
      | 10-4 admin 조회 | GET /v1/admin/fleet·/clients·/clinics/{id}/clients·online 파생·cursor 엔벨로프·RBAC | ✅ 완료 | #12368 |

      **②-c P8 webhook 수신(Receiver) — Task 단위 (8/3~ · 골격 3종 완료 · 2단계 head-start · 로컬 더블)**

      | Task | 내용 | 상태 | PR |
      | --- | --- | --- | --- |
      | 8-1 HMAC 검증·골격 | Host/inbound_host 식별(→404)·HMAC+timestamp 검증(replay 방지·timestamp-binding)·Receiver 골격·즉시 202 ACK | ✅ 완료 | #12369 |
      | 8-2 멱등·payload 암호화 | eventId 멱등(PK·P2002 dedup·중복 0)·store-then-ack·**payload 전용 CMK envelope 암호화·평문 미저장**(키 §7.1.3.1 분리·Jack 승인·spec-v1.0.7) | ✅ 완료 | #12411 |
      | 8-3 SQS enqueue | 저장 후 eventId claim-check 적재(body=eventId만·재시도·store→ACK→enqueue·isNew만) | ✅ 완료 | #12414 |

      > **P8 비고**: 2단계 head-start(④ AXS 실연동 전 로컬 더블로 선행) · **dev 실검증 = Jack payload CMK provisioning 후**(배포-시점 의존) · 8-3 후 실연동은 ④ 후.

      **②-d P9 webhook 분배(Dispatcher) — Task 단위 (8/4~ · 골격 app-side 3종 완료 · 2단계 head-start · 로컬 더블)**

      | Task | 내용 | 상태 | PR |
      | --- | --- | --- | --- |
      | 9-1 SQS 소비·대상해석·DLQ | SQS(eventId) 소비→**(target_id,external_org_id) 복합키** org_mapping→clinic→payload 복호→MQTT publish(gw/clinic/{clinicId}/webhook·qos1)→dispatched · 미해석=**발행 전 fail-closed dead_letter**(교차클리닉 오분배 차단) · 멱등 | ✅ 완료 | #12420 |
      | 9-2 MQTT QoS1·verbatim | 하행 발행 정형화: 토픽 화이트리스트 검증(위험문자 거부·fail-closed·리전 미포함)·QoS1·원 payload verbatim | ✅ 완료 | #12434 |
      | 9-3 DLQ·재전달·멱등 | attempt-cap 백오프→dead_letter·eventId 멱등(중복발행0)·브로커 장애 SQS 잔류 무유실(오프라인 publish 무한 hang 수정=timeout) | ✅ 완료 | #12437 |
      | 9-4 KEDA 오토스케일 | SQS depth 스케일·graceful drain | 🟠 인프라(③-I) | KEDA config=Jack·app graceful drain 별건 |
      | 9-5 device IoT 프로비저닝 | Thing/cert·enroll 확장 | ⬜ 대기 | ④ AXS/IoT Core |

      > **P9 비고**: full-loop(수신→저장→분배→Mosquitto 구독자 더블)을 로컬로 그린(9-1) · 동반 = **런타임 dep 분류 가드 신설**(소스 devDep import 시 CI 실패·GATE 1b) · dev 실검증·실연동은 ④ AXS 후.

      **②-e P11 Admin API·레지스트리·audit — Task 단위 (8/5~ · ④ 무관·자율 진행 · 코어 P0~P6 인증/DB 위에 관리면 축조)**

      | Task | 내용 | 상태 | PR |
      | --- | --- | --- | --- |
      | 11-1 targets CRUD | 연동 대상(라우팅+아웃바운드 자격+인바운드 webhook) 통합 1레코드 CRUD · write-only 자격/시크릿→**KMS wrap**(target-cred 전용 CMK)·응답은 KMS 참조 포인터만(**원문·암호문 미노출**) · 종속(매핑·정책·이벤트) 삭제 **409** · 부재보존 병합(운영 필드 조용한 소실 차단) | ✅ 완료 | #12441 |
      | 11-2a policies CRUD | 인가 정책(deny-by-default 허용 SSOT) 등록/조회/삭제·**자연키 upsert**(동시경합 1행 원자성)·부재보존 병합·targetId FK 400·scopeId 형식검증·감사 | ✅ 완료 | #12443 |
      | 11-2b config·org-mappings | 중앙 config(PUT 멱등·version 값변경시만++·updated_by 서버강제·NULLS NOT DISTINCT)·Org-ID↔ClinicID 매핑(복합PK·mapping_version++·이중 FK 400·복합키 커서)·감사 | ✅ 완료 | #12444 |
      | 11-3 operators·RBAC 생애주기 | 운영자 역할 승인/거부/회수·access-requests·**마지막 admin 회수 409**(lock-out 방지·v1.0.10) | ⬜ 대기 | — |
      | 11-4 webhook-events + break-glass | 이벤트 메타 조회·단건·**본문 열람(break-glass·복호·masking·감사)** | ⬜ 대기 | — |
      | 11-5 audit 전면 커버리지 | GET /v1/admin/audit(필터·커서)·전 write 경로 감사 누락 점검 | ⬜ 대기 | — |
      | 11-6 데이터 분류·크로스보더 동의 | 분류 태깅·동의 태그(컴플라이언스) | ⬜ 대기 | — |

      > **P11 비고**: ④ AXS 실연동과 무관한 **관리·레지스트리·감사면**이라 자율 진행 중(코어 P0~P6 인증/RBAC/DB 완료가 선결이라 지금 가능). 11-1 이 target-cred CMK(§7.1.3.1 키 #3·payload 키와 별개)·secret-ref 코덱(libs/common 승격·admin write·receiver read 계약 단일화)을 도입 — Jack `alias/gw-target-cred-<region>` prod provisioning 후속.

      **③ 2단계 — Phase 단위 (대기)**

      | Phase | 범위 | 상태 | 비고 |
      | --- | --- | --- | --- |
      | **P7 External Connector·AXS** | OAuth2 cc·egress 고정IP·앱 PDP egress·org-binding·presigned 중계 | ⬜ 대기 | 🔴 2단계·④ AXS 실연동 후(보류) |
      | **P11 Admin API·audit·컴플라이언스** | 전 CRUD·RBAC 생애주기·break-glass·audit 전면 | 🟡 진행(11-1 완료·②-e) | ④ 무관·자율 진행 중 |
      | **P12 E2E·하드닝** | AXS sandbox E2E·compat E2E·부하·HA/KEDA 검증 | ⬜ 대기 | 🔴 2단계·④ AXS sandbox 실자격 |

      > **직전 주(7/30) 구현 요약 · P2~P6 완결** — 1단계 GW 독립 코어에서 **P2~P6 다섯 Phase를 완결**했다. **P2 인증**: device 면(2-1 private_key_jwt→RS256 토큰, 2-2 jti 1회 소비·검증후 정본 clientId rate-limit·revocation denylist, 2-3 deviceAuth Guard)에 operator 면(2-4 Entra OIDC+confused-deputy 방어+JIT, 2-5 RBAC deny-by-default+`/v1/admin/me`)을 더해 양 인증면을 완비. **P3 enrollment**: 개시/완료(3-1·3-2)에 이어 device 생애주기 상태머신·재-enroll 회전 옛 credential 폐기(3-3)·C/S 승인 slice+kill 즉시 denylist 전파(3-4)·미승인 pending 자동만료(3-5)로 종료. **P4 레지스트리·region resolution**: Region Resolver(mapping_version CAS·버전 조건부 캐시·4-1)·ClinicResolution+GET /v1/regions(4-2)·PATCH /me+PUT /me/region(4-3)·PHI region-boundary 앱 내부 PDP(4-4)·admin region 카탈로그 CRUD(4-5)로 완결. **P5 호환성 게이트**: Vatech-\* 파싱→400(5-1)·well-known 매트릭스 서빙(5-2)·semver 3단계 게이팅 guard(5-3). **P6 target-routed 프록시**: 서브도메인 라우터+SSRF fail-closed(6-1)·PEP 체인(auth 401→PDP 403→region)+verbatim bypass(6-2)·아웃바운드 복원력(6-3 D1~D3 타임아웃·취소 전파·에러 정규화·Idempotency-Key)로 완결. 모든 엔드포인트 Task에 **검증 4종(unit·e2e[실 DB·Valkey]·curl 왕복·DB/Valkey 조회)** 과 **E2E 반복성 하네스**(clean-slate·seed·FLUSHDB)를 적용했고, 보안 민감 Task(프록시·인증)는 **독립 적대적 pre-PR 리뷰**로 검증했다. (region-silo 재작업 상세는 위 ② Task 테이블 참조.)

  - **S3-1. 커버리지 현황 (구현과 분리 · merged=unit+e2e 합산 · 8/5 측정·post-T-ADM-11-1 · 매 Task 완료 시 갱신)** — 커버리지 스윕(1·2·3순위 101 케이스·PR #12372) 후 실측, 이후 Task마다 재측정. 정본 기준 = **merged**(단위+통합 합산).

    | 스코프 | Statements | Branches | Functions | Lines |
    | --- | --- | --- | --- | --- |
    | **① 전역 (merged)** | **95.97%** | **91.32%** | **92.16%** | **95.64%** |
    | **② 보안 도메인 (merged)** | **98.56%** | **95.99%** | **100%** | **98.46%** |
    | **③ 핵심 보안 파일 16개 (merged·개별)** | — | **각 100%** | — | — |
    | _참고: 전역 (unit-only)_ | 77.73% | 83.02% | 72.15% | 78.73% |
    | **CI 게이트 floor — ① 전역** | 92 | 87 | 88 | 92 |
    | **CI 게이트 floor — ② 보안** | 95 | 89 | 95 | 95 |
    | **CI 게이트 floor — ③ 핵심파일(개별·branch)** | — | **90** | — | — |

    - **추천 기준값 (= 위 표의 'CI 게이트 floor' 행 · 회귀 방지 하한)**:
      - _① 전역 · ② 보안(합산)_: 재앙적 회귀 catch용 하한(달성치 대비 여유 有). 달성치 상승 시 floor 도 올려 개선을 잠금(**ratchet**).
      - _③ 핵심 파일(개별·branch ≥90)_: **규범적(실질 요구수준)** — 합산이 못 잡는 단일 파일의 보안 분기 공백을 차단. 현재 16개 전부 100%. 미커버는 (A)도달가능→테스트 / (B)도달불가→`istanbul ignore`+실증근거로만 처리(숫자 치팅 금지·적대 감사로 부당 ignore 색출·수정).
      - _수준_: 업계 통상(라인 ~80% · 분기 70~80%가 "양호")보다 높음 · 가장 엄격한 **Branch 를 전역 91.3 / 보안 96.0% 달성**.
      - _한계_: %는 필요조건일 뿐 — 본 스윕은 **적대적 mutation testing**(방어 로직 역전 → 테스트 red 확인)으로 회귀 포착력까지 검증.

    - **CI 게이트·조회**:
      - **게이트(차단)**: CI `GATE: merged coverage floor (unit+e2e)` 스텝이 전역/보안 8개 값 중 하나라도 floor 미달이면 **비-0 종료 → PR 머지 차단**(required check). _실증: 빌드 49327이 이 게이트에서 실패해 막혔다가 수정 후 통과._
      - **조회 — 로그**: PR → **CI verify** → **`Verify gates`** 잡 → **`GATE: merged coverage floor (unit+e2e)`** 스텝 로그에 Coverage summary + floor 대조표 출력.
      - **조회 — UI**: 빌드 **Coverage 탭**(`PublishCodeCoverageResults`·cobertura) — %·파일별·추세 시각화.
      - **로컬 재현**: `make coverage-merged`.

    - **범례**:
      - **지표(4열)** — "해당 요소 중 테스트가 1회 이상 실행한 비율(%)":
        - **Statements(구문)**: 실행 가능한 개별 구문의 실행 비율(기본 지표·코드 대부분에 대응).
        - **Branches(분기)**: `if`/`switch`/삼항/`&&`·`||`·`??` 조건 분기의 **각 방향(true·false)** 실행 비율 — **가장 엄격**, "정상만 타고 오류·fail-closed 경로 미검증" 공백을 드러냄(보안 척도).
        - **Functions(함수)**: 정의된 함수·메서드 중 1회 이상 호출된 비율.
        - **Lines(라인)**: 실행 가능한 소스 라인의 실행 비율(Statements 와 유사·물리 라인 기준).
      - **스코프 — 점점 좁고 엄격한 3단계(포함관계·중복 아님: 전역 ⊃ 보안 도메인 ⊃ 핵심 파일)**:
        - **① 전역**: 앱 전체(`apps/**` + `libs/**`) **합산** — "레포 전반이 안 무너졌나". 가장 넓고 느슨.
        - **② 보안 도메인**: 6개 보안 폴더(`auth`·`authz`·`enroll`·`proxy`·`webhooks`·`crypto`) **합산** — ①의 부분집합. PHI·자격증명·게이팅 민감 경로라 **전역보다 높은 floor**.
        - **③ 핵심 보안 파일**: ② 안의 **보안 결정 파일을 파일별(개별)로** 검사(합산 아님·branch floor **≥90**). **왜 별도인가**: 합산(①②)은 자잘한 covered 코드가 많으면 **한 파일의 보안 분기 공백을 가릴 수 있다** — 파일별 게이트라야 "auth.service 하나가 무너져도" 잡는다. 미커버 중 **도달불가 방어 분기는 `istanbul ignore`+근거로 제외**해 reachable 기준으로 관리. **대상 목록**: `auth.service`·`device-token.verifier`·`signing-key.provider`(토큰 발급·검증), `hmac.guard`·`json-path`(webhook 인증·파싱), `kms-envelope`(PHI 암호화), `egress-allowlist`·`pdp.service`·`policy-resolution`(인가·SSRF), `enroll.service`·`enroll-complete.service`·`enroll-ip`·`pending-expiry.job`(enrollment·nonce), `proxy.service`·`router`·`proxy-timeout`(프록시 라우팅·타임아웃).
        - **참고: 전역(unit-only)**: 단위 테스트만의 수치. 컨트롤러·가드·미들웨어·local 어댑터가 0%로 잡혀(그 계층은 e2e로 커버) 낮음 — merged 가 정본임을 보이는 대조치.
      - **merged**: unit + e2e(실 DB/Valkey) 합산(nyc) — 두 실행을 합쳐야 "실제 실행·검증된" 라인이 정직하게 집계됨. 현재 테스트 규모 = **unit 841**(receiver store/sqs·dispatcher consumer 신규 포함) · e2e 는 webhook 저장·enqueue·**분배 full-loop(SQS→Mosquitto 구독자)** 포함. _표의 % 는 8/4 스윕 실측 기준값(이후 소규모 Task 델타는 자잘하며, 보안 per-file floor 유지)._

  - **S4. 리전 자동 결정(country→region) 스펙 반영 (정보 공유)**
    - 온보딩 시 EzServer가 **리전을 직접 고르지 않고**, Region Directory의 리전별 담당 국가(`countries`) 매핑으로 **자기 클리닉의 나라(LMP 라이선스/Clinic-ID)에 맞는 리전을 자동 결정**(R6).
    - 지연(GeoDNS) 추천이 아니라 **주권상 결정적 매핑** + C/S 승인 검증.
    - **v1.0은 production 단일(호주)이라 자명 → 실효는 gw/1.2 멀티리전**(당장 blocker 아님).
    - 반영: SRS §2.3.1(온보딩·다이어그램)·§7.3.6(Region Directory `countries` 필드·규칙·JSON 샘플)·§7.3.1 + EzServer handoff · spec-v1.0.6(미커밋·누적).

  - **S5. 이번 주 완료·확정 상세 (참고 · 논의 대상 아님 · 진행 요약의 근거)**
    - **(8/3 완료) R2. GW 저장소 = 리전 완전 분리 — 스펙 + 구현 코드 모두 완료** _(결정 상세는 7/30 스냅샷 R2)_
      - **스펙**: SRS·DBML·OpenAPI·env-reference·well-known·크로스팀 handoff 전면 개정 + 자동 코드리뷰 11라운드·Jack 인프라 리뷰 전건 반영(미해결 0) → PR #12207 머지(`a0d1600`·`spec-v1.0.5`) + #12231 머지(`9cc08fa`·`spec-v1.0.6`)(7/30). **변경 규모 = 12 files · +477 / −676 라인(순 −199)** — SRS +281/−253 · OpenAPI +57/−254 · DBML +32/−53 · UnitTCL +28/−62 · 기타(env-reference·well-known·handoff 등) +79/−54.
      - **구현 코드**: PR #12241 머지(`9146ae3`·8/3) — 전역/리전 2-DB→단일 datasource·region=배포 상수·Region Resolver/리전 API(GET·PUT `/v1/regions`)/region_catalog CRUD 삭제·하드 FK·ClinicResolution=리전 echo. **변경 규모 = 139 files · +1,685 / −5,538 라인(순 −3,853)** — 앱 소스 65f · 테스트 46f · 설정·문서 23f · 마이그레이션/생성물 5f. 대량 삭제 = 2-DB·resolver·리전 API 복잡도 제거.
      - **검증**: unit 534 · e2e 157 · CI green(build 20260803.1) · `verify-spec`/`verify-ci` 게이트 신설 · README 드리프트 정정(PR #12348). 후속 = IP Spec Index·체크박스 갱신.
      - **PR**: [구현 #12241](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/12241) · [스펙 #12207](https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/12207)
    - **R2-1. 호주 first-open 리전 전략 — ✔ 확정**
      - v1.0 production 리전 = **호주 멜버른(ap-southeast-4·`apse4`)** · **서울(apne2) = 비-prod 전용**(dev·test·staging). 호주 클리닉을 서울에 임시로 두지 않음. _(8/4 ③-I 확정: 비용 우위로 시드니 ap-southeast-2 대신 멜버른 ap-southeast-4 — spec-v1.0.8 교정)_
      - region silo라 production은 리전별 독립 스택 1개씩(서울 production은 추후 추가 가능).
      - '서울 임시 홈 → 호주 이전'(리전 통째·대량 이전) 시나리오 없음 — 호주 클리닉은 처음부터 호주 리전 온보딩(PHI residency).
      - 스펙 영향: SRS §2.3.9 호주 임시-홈 예시 v1.0 제외(gw/1.2 재홈 역량만 존치)·기준 리전=호주 멜버른(dev=서울) — spec-v1.0.6 + 리전 라벨 apse4 교정 spec-v1.0.8.
      - 유지: AXS webhook 콜백 org(클리닉)별 세분화 요청 계속.
    - **R3. 제품 OnePager(③-P) 인계 — ✔ 방식 확정**
      - CleverSpace(=EzCloud·git): PR 인계 완료 — `ezicloud/ezcloud`·`docs/onepager/gw_adaptation/CleverSpace-GW적응-OnePager.md`(정정본)·**PR #12239**(`d3f676a0`)·통지 Larry(고형용).
      - CleverOne(svn): SharePoint 폴더 인계 완료 — `ProjectDoc/Clever One/srs/OnePager/gw_adaptation`(작성 Raymond)·통지 Nick(탁수용).
      - EzServer: Teddy 수령·PR 착수 확인(`ezserver_suite/doc/onepager/gw_adaptation`).
    - **R4. GW 도메인 별도(vatech.com 미사용) — ✔ 확정**
      - vatech.com은 이메일 도메인이라 GW 관리 어렵고 혼란 소지 → GW는 별도 도메인(구체 도메인 지정 예정·③-I).
      - 스펙 반영(완료·미커밋): GW 호스트 예시 `…gw.vatech.com` 34곳 → `gw.<도메인>` 플레이스홀더. `vks.vatech.com`·이메일 `@vatech.com`은 유지.
    - **R5. GW Console v1/v2 분리 · v1.0 최소기능 선행 — ✔ 확정(전규현/Raymond)**
      - Console이 있어야 온보딩·디바이스 승인 Flow가 돎 → v1.0 = Flow 동작 최소 스펙으로 착수 앞당김(v2 후속).
      - v1.0 범위: 인증=MS Entra · Istio admin API 접근제어 · 페이지 접근 ZTNA.
      - 소유=전규현/Raymond · 일정 v1.0 9월 착수(~28d)·v2 10월 중순(~10/15).

- 이월 논의 사항 (6/25·7/2·7/9 미결 — 계속)

  | # | 항목 | 타입 | 상태 |
  | --- | --- | --- | --- |
  | 4 | Webhook 클라우드 분배(CleverLab 갈래B) | [논의] | v1.0 제외 — Open 후 결정 |
  | 6 | AXS sandbox 자격증명(Straumann 제공) | [정보] | pilot·E2E 블로커 — 확보 시점?(협상중) |
  | 7 | 경로 B EOS 시점 | [논의] | 리뷰서 workaround·지속성 확정(§2.8) — EOS *시점*만 PM·CS/CO OnePager 미정(①흡수) |
  | 8 | v1.0 목표 RPS·동시 세션 | [정보] | 인프라/규모 PL 입력 대기 |
  | 9 | RTO/RPO·유지보수 윈도우 | [정보] | 인프라 설계 단계 — failover 요건은 R2(저장소 전역일관 vs 리전분리·Q3) 결정과 연계 |
  | 10 | 감사·consent 보존 기간 | [정보] | 법무 확인 대기 |
  | 11 | 호환성 매트릭스 확정본 | [정보] | CleverSpace/CleverOne OnePager 의존(①폐지·흡수) — 초안 7/27 작성·확정값은 담당팀 baseline 후 |
  | 14 | 관측성 앱↔인프라 계약 확정 — ①로그 필드 스키마(현행 pino 기본 필드 ↔ §6.3.2 최소셋 매핑·Appendix B #14) ②메트릭 export 배선(OTLP reader→Grafana Alloy 엔드포인트) | [논의·설계] | **추후 확정** — 트리거=③-I 관측 스택 구축 or P6 프록시 착수(먼저). Raymond 초안(필드 매핑표+엔드포인트 요구)→Jack(인프라) 비동기 합의. **앱 계약(stdout JSON+OTel·redaction) 이미 구현·무블로킹** |
  | 이월-R1 | IO Scanner↔EzServer 연동 방식 | [논의·선결] | **보류(7/23 결정)** — 이번 주 논의 「Straumann↔ES 데이터 흐름 협상」 결과에 종속(결정 시 이월-R1·④ AXS scope 착수 조건 확정) |
  - **차주 이월 후보**: 이월-R1(IO Scanner↔EzServer 연동 방식·**보류**)·이월-R2(목표일정·출시일 재검토) 미확정 시 다음 주 이월.
