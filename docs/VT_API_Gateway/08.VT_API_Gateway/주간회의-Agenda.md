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
      - **⑤ policy 스코프 = device-중심 확정(device→clinic→global)** — 구 'device 배제'를 **대체**. `policy.tenant`(clinic 하드 FK) → **`scope_type{global\|clinic\|device}+scope_id`**. clinic=clinic-bound device의 **상한(ceiling)**, device는 그 안에서 narrowing(§7.5.3, deny-by-default). *device 단위 policy는 clinic-less/예외용 — v1.0은 clinic+global만 사용.*
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

- R6. GW SRS 리뷰어 목록 확정 
  | 영역 | 리뷰 포인트 | 리뷰어 |
  | --- | --- | --- |
  | 총괄·승인(CCB) | baseline 승인 | **Scott(실장·총괄,PM)·Raymond(GW 리드)** |
  | 아키텍처·라우팅 | ADR(특히 ADR-11 R1 재평가)·3-plane·§2 | **Thomas** (외 추가 가능 — 복수 아키텍트) |
  | 인증·보안 | §7.1·§6.2·§6.5·PHI·데이터 주권 | (보안 담당) — Scott |
  | 인프라(③-I) | §3.1·배포·EIP·IaC(R5)·환경 구축 | **Jack** |
  | DB·데이터 모델 | §6.4·DBML·보존기간(#5) | **GW 팀(작성자) = Raymond** — 자체 소유(별도 DBA 없음). 보존기간(#5)만 법무/품질 입력 |
  | API 계약 | §4·§7·OpenAPI 정합·에러 계약 | **GW 팀(작성자) = Raymond** — 자체 소유(총괄과 동일). *외부* 적합성 검토는 소비자 ③-P |
  | 제품 적응 ③-P-EZ (EzServer) | 클라이언트·클리닉 등록 주체 영향 | Thomas (담당 1인 이상) |
  | 제품 적응 ③-P-CS (CleverSpace) | presigned·B 프록시 영향 | 고형용/ Larry |
  | 제품 적응 ③-P-CO (CleverOne) | 경유 전환 영향 | 탁수용/ Nick |
  | 제품 적응 ③-P-OID (OneID) | 인증 연계 영향 | 서유진 / Jin |
  | QA·검증 | §3.6·테스트·호환성 매트릭스 | **정우혁/ James_ES** |
  - **→ 반영완료(2026-07-02)**: SRS §9 Document Approvals에 영역별 리뷰어 표 추가 + §8·§9·Appendix B #10에 **Scott=PM 겸임** 반영.

- R7. 스펙 ↔ GW 구현 진행 전략 
  - **1안으로 결정** — ④ AXS Sub-SRS baseline **직후 구현 착수 + ③-C·③-P·③-I 스펙 병행**(2안=전 스펙 완료 후 착수는 납기 지연으로 반려).
  - 구현 시작점=④ AXS baseline(고정, 첫 연동·E2E 필수). 구현 기간=미정(SRS 확정 후 재산정). pilot 8/15는 재검토.
  - 반영: `specs/00-execution-allocation.md` "구현 착수 전략" 섹션 신설 · 위 gantt에 1안 채택 표기.

- R9. 온보딩/enrollment 모델 확인
  -  EzServer 에서 private key 분실시 재발급 과정이 필요하다.
  -  License 등록과정에서 GW 온보딩을 하게 하는 방안을 검토한다. (최대한 편리하게)
  -  EzServer내에서 private 키를 안전하게 보관/백업할 방법이 필요하다. 
  -  이런 것이 SRS에 다 반영되었나? 또는 OnePager에서 구체적으로 작성하면 되나?
  -  분실 시 재발급 과정은 GW SRS에 있어야 하지 않나?
  - **→ 반영완료(2026-07-02)**: 상당 부분 이미 SRS에 있었고 '개인키 분실 복구'로 명확화. **분실 복구=재-enroll 회전**(§7.2.7, 유일 경로·백업 복원 없음)·**개인키 백업(export) 미도입**(§7.2.6, 디바이스 비이탈)·**at-rest 안전 보관=EzServer(③-P-EZ) OnePager**·라이선스 등록 시 자동 enroll 편의(§2.3.1). GW SRS에 재발급 과정 있음(§7.2.7).

# VT API Gateway — 7/9 주간회의 Agenda

- 논의 사항 (7/2 결정 → 적용 방법 확정 · 신규 결정 요청)

  - **R1. 라우팅 방식 재평가 방안** — GW edge = **C안(서브도메인)** 확정 · CleverOne→EzServer 내부구간 = **A+C 채택**.
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
              proxy_connect_timeout 3s;                        # (프록시 타임아웃은 §7.5.4/R4)
              # 버전 호환용 Vatech-* 식별 헤더(Product/Version/OS/Clinic-Id/Via)는 그대로 전달
          }
      }
      ```
      - **동작**: CleverOne이 `Vatech-Target: axs` 헤더로 EzServer 호출(평문/HTTPS 무관) → EzServer가 헤더값을 `axs.gw.vatech.com`으로 변환해 **HTTPS로 GW 전달**(HTTP→HTTPS 브리징). EzServer 자체 HTTPS-off와 무관(아웃바운드는 nginx가 클라이언트로 HTTPS 개시, cert 설치 불요).
      - **보안**: 평문 LAN 구간에 토큰/PHI가 실리면 노출 — 민감 트래픽은 그 구간 HTTPS 권장(기존 운영 자세라 별도 판단).
    - **SRS 반영 예정(확정 후)**: ADR-11(라우팅 = **edge 서브도메인** · `Vatech-Target`은 내부 hop 변환 키로 유지) · §4.5.1(`{target}.gw.vatech.com` + `*.gw.vatech.com` 와일드카드 cert + GeoDNS 와일드카드) · §4.1.2(라우팅 방식) · §4.1.4(업로드 target 지정) · webhook 서브도메인과 일관성 명시.

  - **R2. Webhook payload 저장 방식 결정 (중요 · 결정 요청)** — `webhook_event`가 수신하는 이벤트 **본문(payload)** 을 어디에·어떻게 보관할지 확정.
    - **배경(references 스펙 확인 결과)**:
      - v1.0 webhook 소스 = **AXS 단독**(CleverSpace=webhook 대상 아님 확정 · CleverLab=갈래B 보류).
      - AXS payload = **JSON**, 수 KB(알림 메타데이터 — 큰 영상은 webhook 아님·presigned). **환자 PHI 포함**: `patient.created/updated`에 이름·생년월일·성별·patientId, file 이벤트에 storageUri·파일메타.
      - GW는 payload를 **opaque·verbatim**(해석·수정 안 함)으로 다루며, store-and-forward 버퍼는 이미 **SQS(리전 로컬)**.
    - **핵심 논점**: 쟁점은 "payload가 너무 큰가"가 **아니라** "**payload에 환자 PHI가 들어온다**"는 점. GW 대전제(§6.4 "GW는 PHI 미저장")를 **"webhook에서는 PHI를 전이(transient) 경유하고 persist를 최소화한다"** 로 정교화해야 함(리전 로컬·암호화·짧은 TTL·복제 금지·콘솔 비노출).
    - **결정 항목 (3)**:

      | # | 결정 항목 | 옵션 | **추천안** |
      | --- | --- | --- | --- |
      | R2-1 | dispatch 후에도 payload를 보관? | (a) **일정기간 보관**(디버깅·재생·감사) / (b) SQS 전이만·사후 폐기 | **(a) 일정기간 보관** |
      | R2-2 | 보관 장소 | **S3(리전 로컬·참조)** vs PG DB(jsonb 컬럼) | **S3** |
      | R2-3 | Console 상세 뷰의 환자정보 | **redact(마스킹)+접근통제** vs 원문 노출 | **redact+접근통제** |

    - **R2-2 비교 (S3 vs DB) — 추천 = S3**:

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
    - **R2-1 보존기간(TTL)**: 디버깅·재생·감사 목적이므로 **짧게**(초안 예: 7~30일). 정확한 값은 감사·consent 보존정책(Appendix B #5)과 함께 확정.
    - **R2-3**: redact = Console 화면 표시 시 환자정보 **마스킹**(전달 본문은 verbatim 불변). 운영자 디버깅은 허용하되 환자 신원 불필요 노출을 막는 데이터 최소화(§6.4). 접근통제 = 역할(Admin/C-S)별 payload 열람 권한.
    - **SRS 반영 예정(확정 후)**: DBML `webhook_event.payload_ref` 주석(본문=리전 S3·claim-check 참조·관계형 DB 미저장) · **`event_type` 컬럼 추가 검토**(Console 필터) · §6.4(webhook PHI 전이·최소 persist로 정교화) · §7.6(store-and-forward 본문 보관·TTL) · Appendix B(보존기간·본 결정 로그).

  - **R3. 연동 대상 테이블 병합 + 명칭 확정 (공유·명칭 승인 요청)** — AXS·CleverSpace·OneID 같은 **GW 연동 대상**의 라우팅·아웃바운드 자격·인바운드 webhook 수신을 담던 **3개 표(upstream_registry·connector·webhook_provider)를 1개 표로 병합**(1:1 facet·중복 토큰·미연결 해소, provider 등록=1 레코드). 병합 표의 **이름을 무엇으로 할지** 4개 후보를 비교했고 **일단 `upstream`으로 정했다**.
    - **이름 후보 비교**:

      | 후보 | 장점 | 단점 |
      | --- | --- | --- |
      | **`upstream`(채택)** | 회의 어법 그대로(*"신규 upstream=레지스트리 1행"*)·업계 표준(GW가 라우팅하는 backend)·내부/외부 backend 다 포괄·클라이언트(CleverOne) 자연 배제·컴포넌트(External Connector)와 충돌 없음 | 인바운드 webhook facet엔 살짝 아웃바운드 뉘앙스 |
      | `target` | 문서 어휘(target-routed proxy·`Vatech-Target`)와 일치 | 회의에선 target=라우팅 키(헤더값), upstream=서버로 구분 → 엔터티엔 upstream이 정확 |
      | `integration`(연동) | 양방향·내부/외부 다 포괄·"연동" 자연 | 회의 미사용·다소 추상적 |
      | `provider` | 익숙(webhook에서 유래) | **webhook 유래뿐**·CleverSpace 등 내부 backend엔 부적합·OAuth "provider"와 과적재 |
    - **확정(잠정)**: 표명=**`upstream`**(엔터티), PK=**`target_id`**(=Vatech-Target 값=서브도메인 라벨). FK(org_mapping·webhook_event·policy)=`target_id`. "CleverSpace를 등록한다 = **upstream 1 레코드 추가**"로 표현.
    - **SRS 반영 완료**: DBML(Table `upstream`)·OpenAPI(`Upstream`·`/admin/v1/upstreams`)·db-jsonb(#upstream)·redis(`gw:cache:upstream`)·SRS §6.4·§7.5·§7.6·§7.9·§2.3.4·ERD·API명세·③-C·ARD 전부 정합.
    - **이번 회의에서 다른 이름으로 바뀌면** 그때 일괄 재반영(단순 rename). 결정만 주면 됨.

  - **R4. AXS Org-ID 취득 경로·절차 (조사 — 이번 회의 확정 불요)** — AXS webhook 분배·아웃바운드 호출의 라우팅 키인 **외부 Org-ID(Straumann Organization-ID)를 각 클리닉이 어떻게 갖게 되는가**를 확인한다. GW는 `org_mapping`(로컬 매핑)만 채우지만, 그 전에 "그 클리닉의 AXS 조직이 우리 연동과 연결돼 Org-ID가 존재"해야 하는데 그 취득 경로가 미확인이다(§2.3.4 「연동 링크·org_mapping 생애주기」는 GW 공통 레일만 규정).
    - **묻는 것 (핵심 3택)**:
      1. 클리닉이 **이미 Straumann에 등록**돼 Org-ID를 보유하고 있나? (경우 A — 기존 AXS 고객)
      2. 아니면 EzServer 설치 시 **우리가 Straumann 등록/연결 절차를 대행**해 Org-ID를 발급·연결받아야 하나? (경우 B — 신규)
      3. **두 경우가 다 존재**하나? (일부 기존 고객 / 일부 신규 → GW는 양쪽 다 수용해야)
    - **경우 B라면 절차는? (어디서·누가·어떤 UI)**:
      - AXS **별도 콘솔/포털**에서 조직 담당자가 발급·동의하는가? (out-of-band)
      - **GW가 AXS API로** 대행하는가? — *우리 조사(AXS Organization API)*: `POST /v1/organization/integration/link`(`customerNumber` + 우리 Client ID) → `organizationId` + **조직 관리자 동의**(status `PENDING`→`APPROVED`). 즉 **조직 자체는 Straumann 고객**이고 우리는 그 조직에 우리 연동을 **"연결(link)"** 만 한다(생성 아님). 보조 API `.../check`(연결 확인)·`.../unlink`(해제)·`.../{customerNumber}/info`(region·country).
      - **EzServer Console에서** 그 연결을 트리거하는 **UI를 제공**해야 하나? (customerNumber 입력·동의 상태 표시·완료 시 org-binding 자동 등록 등)
    - **부가 요청**: Straumann과 **계약·sandbox 제공 시 Tech support(기술 질의) 채널**도 함께 확보 요청 — 위 절차·동의 흐름·`customerNumber` 취득 방법은 Straumann에 직접 확인해야 정확하다. (AXS sandbox 자격은 이월 #6과 연계)
    - **성격/산출**: [정보·조사] — **이번 회의 확정 불요**, "알아볼 경로(누구에게·어떻게 확인할지)"만 정하면 됨. 확정 시 **④ AXS Sub-SRS**에 구체화(경우 A/B 판정·링크 트리거 주체·UI 소유). **미확정 시 차주 이월**(아래 이월 논의 사항에 등재 예정). 근거 자료: 참조-카탈로그 §3 AXS_docs `organization.yml`·Integration_guide.

- 공유 사항 (결정 아님 · 정보 공유)

  - **S1. GW→각 EzServer(클리닉) 범용 하행(downlink) 레일 확보** — webhook 역방향 분배를 위해 만든 **MQTT 하행 채널**(EzServer가 방화벽 뒤에서 outbound 지속 구독, §7.6.6)은, 사실상 **중앙(GW)에서 각 클리닉 edge로 능동 전달하는 최초의 수단**이다. 토픽을 `gw/clinic/{clinicId}/{stream}` 로 두어 **`{stream}` 확장점을 예약**했다(EzServer는 `#` 구독·미지 stream 무시·forward-compat).
    - **지금**: `webhook`(AXS 이벤트 분배) **하나만 구현**.
    - **미래 활용 가능(예약·미구현)**: `announce`(클라이언트 새 버전 설치 안내·프로모션·공지) · `command`(kill-switch 등 즉시 명령) · `config`(원격 설정 하달) 등. 새 용도는 **발행자 추가만**으로 수용(레일·EzServer 구독 불변).
    - **의미**: 지금은 안 쓰더라도 **"중앙에서 fleet으로 뭔가 내려보내는" 다양한 미래 수요를 무구조변경으로 담을 레일**을 확보. 확장점 예약 비용≈0, 기능은 미구현(YAGNI 준수).
    - **결정 필요 없음** — 공유만. 구체 활용(공지/명령 등)은 수요 발생 시 별도 안건화. 

  - **S2. 프로젝트 일정(Gantt) — 주간 참고 스냅샷** — 스펙 생애주기(작성→PR→baseline)+GW 구현 타임라인. **정본=[개발 Roadmap 결정 §3.9](<VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>)** (수정은 그쪽 먼저). 아래는 7/9 기준 스냅샷 — 매주 최신본으로 갱신.
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
        OneID 초안            :oidw, after cow, 7d

        section ③-I 인프라 IaC 계획서
        GW 담당 초안          :infw1, after srsbl, 7d
        인프라 담당 완성       :infw2, after infw1, 14d
        PR 리뷰·수정          :active, infpr, after infw2, 14d
        baseline              :milestone, infbl, after infpr, 0d
    ```

- 이월 논의 사항 (6/25·7/2 미결 — 계속)
  | # | 항목 | 타입 | 상태 |
  | --- | --- | --- | --- |
  | 4 | Webhook 클라우드 분배(CleverLab 갈래B) | [논의] | v1.0 제외 — Open 후 결정 |
  | 6 | AXS sandbox 자격증명(Straumann 제공) | [정보] | pilot(08-15) 블로커 — 확보 시점? (R4 Tech support 채널과 함께 요청) |
  | 7 | 경로 B EOS 시점 | [논의] | ① One Pager 확정 의존 |
  | 8 | v1.0 목표 RPS·동시 세션 | [정보] | 인프라/규모 PL 입력 대기 |
  | 9 | RTO/RPO·유지보수 윈도우 | [정보] | 인프라 설계 단계 |
  | 10 | 감사·consent 보존 기간 | [정보] | 법무 확인 대기 |
  | 11 | 호환성 매트릭스 확정본 | [정보] | ① One Pager 의존 |
  - **차주 이월 후보**: R4(AXS Org-ID 취득 경로·절차)가 이번 회의에서 확정/조사경로 미정이면 다음 주 이월 논의에 등재.
