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
  -  **R3. sub-Spec 초안 작성** - Infra Sub Spec 은 Raymond가 기본 Diagram 을 그려주면 Detail한 거는 Jack 이 작성한다. 
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
  - **GW 구현 = 2단계 병행 착수 결정** — ③ baseline 동결(7/20)로 **GW 독립 코어(P0~P6·P10·④ 무관)를 7/21부터 선행 구현 착수**, **AXS 연동부(P7~P12)는 ④ AXS 연동 Spec 완성 후** 진행하는 2단계 병행으로 확정. 1단계는 로컬 backing 서비스+외부 더블로 인프라·AXS 없이 자립(재작업 리스크 0)이라 10월 출시 역산에 완충. 구현계획서(IP) v1.0 인수 완료(§3 착수 게이트 반영). 상세=S1 Gantt·공유.

- 논의 사항 (이번 주)
  - _(회의 시 작성)_

- 공유 사항 (결정 아님 · 정보 공유 · 매주 상시)
  - **S1. 프로젝트 일정(Gantt) — 7/23 스냅샷** — 스펙 생애주기(작성→PR→baseline)+GW 구현 타임라인. **정본=[개발 Roadmap 결정 §3.9](<VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>)** (수정은 그쪽 먼저·동기화 완료). **7/9 대비 변경**: v1.0 범위=IO Scanner로 축소 · 각 스펙 **작성/PR 분리** · CleverOne·②Presigned·CleverSpace=**deferred(post-v1.0)** 섹션 · **담당 표기**. · **7/16 회의 반영(순서 재조정)**: ③-I Infra·③-P-EZ EzServer 초안 **7/20 Raymond 착수** · **IO Scanner(④)·GW Console 연기**.
    - 막대 색: 작성=기본 · PR=강조 · ◆=baseline/마일스톤 · 빨강=외부/미정 선결. **선결(빨강)**: IO Scanner↔EzServer 연동방식(미정·R1)·AXS sandbox 자격(Straumann). **목표=10월 출시**(역산·잠정). **병행 별도 프로젝트**: `SectionView Module 구현`(7/13~2주·Raymond·**GW 아님**)을 별도 섹션 `▷ 병행`에 **다른 색(crit)** 으로 표기 — GW 일정과 자원 경합(부분투입) 가시화용.
    - **GW 구현 = 2단계 병행 착수(신규)** — ③ GW SRS baseline 동결(7/20·`spec-v1.0`)로 **계약이 고정된 GW 독립 부분은 ④ AXS·인프라 완성을 기다리지 않고 7/21부터 선행 구현**한다.
      - **1단계 — GW 독립 코어(7/21~·④ 무관)**: 플랫폼 토대·데이터 모델·인증(device/operator)·enrollment·레지스트리/region·호환성 게이트·target 프록시·fleet(= IP P0~P6·P10). 계약이 ③ SRS·DBML로 고정돼, 로컬 backing 서비스(Postgres·Valkey·SQS·MQTT·KMS 로컬 대체)+외부 시스템 더블로 unit/e2e가 **로컬 자립** → AXS·인프라 없이 진행.
      - **2단계 — AXS 연동(④ 연동 Spec 완성 후)**: External Connector·AXS 커넥터 실연동·webhook 수신/분배·sandbox 전구간 E2E(= IP P7~P12). **④ AXS Sub-SRS**(연동 Spec)와 Straumann sandbox 자격 확보 후 착수·완결.
      - 두 단계는 **스펙 집필과 병행**(위 Gantt에 `1단계`·`2단계` 막대 분리). 근거=7/2 R7(1안): 구현 시작점=④ AXS baseline이나 *core 일부는 ③ baseline 후 선행 가능*. **1단계 선행은 재작업 리스크 0**이며 10월 출시 역산에 완충. 상세 착수 게이트·Phase별 의존=구현계획서(IP) §3(`abc-dev-assistant/projects/vt-api-gateway`).

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

      > **7/23 진행(7/16 회의 반영)**: ③ GW SRS = **PR 코멘트 접수 오늘(7/16)까지 → 다음주 월요일(7/20) 마무리·baseline v1.0(0.9→1.0)** · **③-I Infra·③-P-EZ EzServer 초안 = 7/20 Raymond 착수** · **① One Pager(2주 더·8월 초)·④ AXS(IO Scanner)·③-C GW Console = 연기** · **0단계(IO Scanner 수집)** = 선결·방식 R1 미정. v1.0 = **Straumann IO Scanner** 한정(CleverOne = post-v1.0). 순서·의존 = [Roadmap §3.9]. · **(C) 압축**: GW 구현을 ④ AXS *draft* 후 착수 + **구현 기간 40d로 단축** → 구현 ~10/10·E2E ~10/24(**10/31 목표 이내**).

  - **S3. GW 구현 현황 — Phase·Task 스냅샷 (7/23·매주 갱신)** — ③ baseline 동결(7/20) 후 **7/21 1단계(GW 독립 코어) 구현 착수**. 정본 진척 = 구현계획서(IP) 체크박스(`abc-dev-assistant/projects/vt-api-gateway/ImplementationPlan.md`). 매 Task 완료 시 갱신.
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
      | ″ | T-DATA-1-6 | region_catalog 시드(서울·default) | ⬜ 대기 | |
      | ″ | T-DATA-1-7 | 시드·테스트 데이터 인프라(prisma db seed·Factory) | ⬜ 대기 | |
      | **P2 인증 토대** | 전체 | device private_key_jwt·JWKS·jti / operator Entra OIDC·RBAC | ⬜ 대기 | 1단계 |
      | **P3 enrollment·디바이스 생애주기** | 전체 | enroll start/complete·상태머신·재-enroll·C/S 승인·kill | ⬜ 대기 | 1단계 |
      | **P4 레지스트리·region resolution** | 전체 | Region Resolver·ClinicResolution·mapping_version·PHI OPA 경계 | ⬜ 대기 | 1단계 |
      | **P5 호환성 게이트** | 전체 | Vatech-* 파싱·well-known·AppConfig·semver 3단계 | ⬜ 대기 | 1단계(compat 값=① One Pager 후) |
      | **P6 target-routed 프록시/라우팅** | 전체 | 서브도메인·verbatim·PEP 체인·SSRF fail-closed·타임아웃 | ⬜ 대기 | 1단계(실 AXS 왕복 E2E만 ④ 후) |
      | **P7 External Connector·AXS** | 전체 | OAuth2 cc·egress 고정IP·OPA egress·org-binding·presigned 중계 | ⬜ 대기 | 🔴 2단계·④ AXS 실연동 후 |
      | **P8 webhook 수신(Receiver)** | 전체 | HMAC·멱등·ACK·KMS 암호화 저장·SQS enqueue | ⬜ 대기 | 2단계(골격 로컬 더블 선행 가능) |
      | **P9 webhook 분배·MQTT(Dispatcher)** | 전체 | SQS consumer·대상해석·MQTT QoS1 하행·DLQ | ⬜ 대기 | 2단계 |
      | **P10 fleet·중앙 config·inventory** | 전체 | heartbeat·fleet_state·online 파생·config(gw.*)·inventory | ⬜ 대기 | 1단계 |
      | **P11 Admin API·audit·컴플라이언스** | 전체 | 전 CRUD·RBAC 생애주기·break-glass·audit 전면 | ⬜ 대기 | 2단계(webhook slice=P8 후) |
      | **P12 E2E·하드닝** | 전체 | AXS sandbox E2E·compat E2E·부하·HA/KEDA 검증 | ⬜ 대기 | 🔴 2단계·④ AXS sandbox 실자격 |

      > **금주 요약**: **✅ P0(플랫폼·환경 토대) 완료**(0-1~0-6·0-5만 🟡 배포부 Jack 후속) → **P1(데이터 모델) 착수** — T-DATA-1-1 전역 초기 마이그레이션 merge(PR #12006·risk:migration). 이후 P1 잔여(1-1b raw-SQL·1-2 리전·1-3 KMS·1-4 Redis·1-5 audit·1-6/1-7 시드) → DAG 순서로 **P2·P3·P4 → P5·P6·P10**(1단계·④ 무관). **P7~P9·P11·P12는 2단계**(④ AXS Spec·Straumann sandbox 후). 41 Task 중 **14 완료 + 1 부분완료**(P1 진행: 1-1·1-1b·1-2·1-3·1-4·1-5 merge). **spec-v1.0.1 정합화**(7/22·`56ed7ef`): OPA→앱 내부 PDP·AppConfig→Parameter Store+LKG로 엔진만 변경(규칙 불변)·완료분 무관·P4~P7 도달 시 반영. **pre-pr-review 게이트 개정**(구현자와 분리된 **독립 리뷰어** + rv_prompt --run-cli + 재발패턴 체크리스트)이 T-DATA-1-1·1-1b에서 테스트 회귀·거짓green·통제문서 부정확을 사전 차단 — 자가리뷰 맹점 해소.

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
