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
    - **R4. 프록시(B/C) 에러·타임아웃 정책 (결정 필요)** — GW가 다른 서버(AXS·CleverSpace 등)로 요청을 중계할 때 **연결 실패·네트워크 일시 장애·응답 지연**을 어떻게 처리할지가 정의돼 있지 않던 공백을 채움. 회의에서는 **아래 골격 확인 + 표의 수치·서킷 v1.0 범위만 결정**하면 됨. *(이 안건은 SRS 없이 이 문서만으로 결정 가능하게 정리했다. 셀 안의 `§…`·Appendix 번호는 결정 후 반영할 SRS 위치 표시일 뿐, 결정에는 불필요.)*
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
            | D10 | 클라이언트 타임아웃 **인지 방식** | HTTP는 클라이언트 타임아웃을 기본 전달 안 함 — GW는 클라이언트가 끊을 때(연결 close)만 *사후* 감지. "GW가 먼저 504" 보장하려면 값을 *사전*에 알아야 함 → (A) 계약값 합의 / (B) timeout 헤더 전파 | **하이브리드**: v1.0=(A) SRS 계약값 합의(EzServer↔GW 우리 소유로 충분) + 선택적 **`Vatech-Timeout-Ms` 헤더(상대값) 있으면 GW가 내부 deadline=`now + min(헤더, 설정)`으로 클램프(B)**. 연결 close→upstream 취소는 공통 안전망 | 헤더는 **상대 timeout**(gRPC `grpc-timeout`·Envoy `x-envoy-expected-rq-timeout-ms` 선례, 클록 동기 불필요). "deadline"=GW 내부 절대시각 개념. 외부·3rd-party(CleverLab 등) 확장 대비 |
            | D5 | 재시도 **소유·범위** | GW가 재시도할지 / 클라이언트가 할지 + 어떤 실패만 | **GW는 연결 수립 실패(요청 전송 전)만 1회**(전 메서드 안전). 응답 타임아웃·5xx 재시도 안 함. **앱 레벨 재시도는 클라이언트(EzServer) 소유** | 타겟당 upstream 1개라 풀 재시도 이점 없음 + verbatim relay. HAProxy 기본과 동일. 비멱등 POST 0회 |
            | D6 | 재시도 폭주 방지 (재시도 활성 시) | 재시도가 오히려 부하를 키우는 것 방지 | **D5 권장(1회)이면: retry budget 전체의 10%만**(백오프·jitter 불필요 — 1회라 늘릴 간격이 없음). **재시도를 다회로 넓히면: 지수 백오프+jitter 추가** | D5에서 재시도 횟수 결정에 종속 |
            | D7 | 서킷 브레이커 v1.0 포함 여부 | 한 upstream 장애가 GW 전체로 전파되는 것 차단(빠른 실패 503) | **v1.0 포함(경량)** — 연속 5실패 또는 10초 창 50% 실패율 → open, 30초 후 half-open | 부담 시 임계만 보수적, 미루면 gw/1.1 |
            | D8 | 503 `Retry-After` 부여 | 서킷 open·일시 불가 시 클라이언트에 재시도 시점 안내 | **포함** | 클라이언트 재시도 정렬 |
            | D9 | 오류 매핑·`Vatech-Error-Origin` 헤더 | 장애 시 "GW가 못 갔다" vs "대상 서버가 거부했다"를 호출자(EzServer)가 구분 → 원인 추적·대응 분기 | **확정**: GW 생성 오류=502/504/503+GW 표준 본문(`Vatech-Error-Origin: gateway`), 대상 서버 자체 4xx/5xx=원응답 그대로 통과(`origin: upstream`) | 위 '정책 골격' 오류 매핑과 동일 |

        - **용어 풀이(D6)** — 재시도를 "켰을 때" 그 재시도가 오히려 장애를 키우지 않게 하는 안전장치:
            - **지수 백오프(exponential backoff)**: 재시도 간격을 점점 늘림(예 200ms→400ms→800ms). 과부하 upstream에 즉시 재시도를 퍼붓지 않고 회복할 틈을 줌 — *너무 빨리 다시 두드리지 않기*.
            - **jitter(지터·무작위 흔들기)**: 백오프 간격에 랜덤을 더함(예 200ms → 150~250ms 랜덤). upstream이 살아나는 순간 수많은 클라이언트가 *동시에* 재시도해 다시 죽이는 떼몰림(thundering herd)을 분산 — *다 같이 동시에 두드리지 않기*.
            - **retry budget 전체의 10%**: 재시도를 전체 요청의 10%까지만 허용(예 1,000건 중 재시도 ≤100건). 횟수 제한(1회)만으론 upstream 완전 다운 시 모든 요청이 재시도돼 트래픽이 2배가 됨 → 비율 상한으로 폭주 차단 — *너무 많이 두드리지 않기*(Envoy retry budget 방식).
            - **D5 권장(연결 실패만 1회)이면**: 1회라 늘릴 간격이 없어 **지수 백오프는 불필요**, jitter도 단일 지연이라 거의 무의미. **retry budget만 유효**(개별은 1회라도 전체가 동시에 연결 실패하면 합산 트래픽이 2배 → 비율 상한은 의미 있음). 백오프·jitter는 **재시도를 다회로 넓힐 때만** 필요하다.
        - **용어 풀이(D7 서킷 브레이커)** — 전기 차단기처럼, upstream(AXS)이 죽었을 때 그쪽 길을 잠시 끊어 장애가 GW 전체로 번지는 걸 막는 장치. 없으면 죽은 AXS를 매 요청마다 타임아웃까지 기다리느라 GW 커넥션·워커가 고갈됨.
            - **3가지 상태**: **closed(닫힘=정상)** 평소처럼 전달 / **open(열림=차단)** AXS로 안 보내고 **즉시 503**(기다림 0) / **half-open(반열림=탐침)** 요청 1개만 보내 살았는지 확인 → 성공 시 closed 복귀, 실패 시 다시 open. (차단기처럼 "열림=끊김"이라 직관과 반대.)
            - **"연속 5실패 또는 10초 창 50% 실패율 → open"** = *언제 차단할지*: 연속 5번 실패하거나 최근 10초 요청의 절반 이상이 실패하면 차단으로 전환.
            - **"30초 후 half-open"** = *언제 회복을 시험할지*: 차단 후 30초간은 즉시 503(AXS 쉬게 둠), 30초 뒤 요청 하나로 살아났는지 떠봄.
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
    - **R6. GW SRS 리뷰어 목록 확정 (회의에서 작성)** — ③ GW SRS(+OpenAPI·DBML) **PR 7/6 시작 전**에 리뷰어를 지정해야 리뷰가 공백 없이 진행된다. SRS가 걸치는 **영역별로 리뷰어를 배정**한다. 아래 표의 이름 칸을 회의에서 채운다(총괄 2인은 CCB 기확정, 나머지는 영역 담당 지명).

        | 영역 | 리뷰 포인트 | 리뷰어 |
        | --- | --- | --- |
        | 총괄·승인(CCB) | baseline 승인 | **Scott(실장·총괄)·Raymond(GW 리드)** · **PM=미지정(별도 지정 가능)** |
        | 아키텍처·라우팅 | ADR(특히 ADR-11 R1 재평가)·3-plane·§2 | **Thomas** (외 추가 가능 — 복수 아키텍트) |
        | 인증·보안 | §7.1·§6.2·§6.5·PHI·데이터 주권 | (보안 담당) — ❓ |
        | 인프라(③-I) | §3.1·배포·EIP·IaC(R5)·환경 구축 | **Jack** |
        | DB·데이터 모델 | §6.4·DBML·보존기간(#5) | **GW 팀(작성자) = Raymond** — 자체 소유(별도 DBA 없음). 보존기간(#5)만 법무/품질 입력 |
        | API 계약 | §4·§7·OpenAPI 정합·에러 계약 | **GW 팀(작성자) = Raymond** — 자체 소유(총괄과 동일). *외부* 적합성 검토는 소비자 ③-P |
        | 제품 적응 ③-P-EZ (EzServer) | 클라이언트·클리닉 등록 주체 영향 | ❓ (담당 1인 이상) |
        | 제품 적응 ③-P-CS (CleverSpace) | presigned·B 프록시 영향 | ❓ (담당 1인 이상) |
        | 제품 적응 ③-P-CO (CleverOne) | Vatech-* 헤더·경유 전환 영향 | ❓ (담당 1인 이상) |
        | 제품 적응 ③-P-OID (OneID) | 인증 연계 영향 | ❓ (담당 1인 이상) |
        | QA·검증 | §3.6·테스트·호환성 매트릭스 | **James** |

        - **산출**: 영역×이름 확정 명단 → PR 리뷰어로 지정. 미정(❓) 영역은 담당 지명 요청. (리뷰어는 영역별 1인 이상, 동일인 복수 영역 가능)
    - **R7. 스펙 ↔ GW 구현 진행 전략 (결정 필요)** — **전제(고정): GW의 통합·테스트 가능한 완성은 ④ AXS 연동까지 필요**하다(AXS=첫 연동, 이것 없이 개발·E2E 테스트 불가). 따라서 **GW 구현은 ④ AXS Sub-SRS baseline 이후 착수**가 필수다(core 일부는 ③ baseline 후 선행 가능하나 통합·테스트는 ④ 후). → 쟁점은 *나머지 스펙(③-C·③-P·③-I)을 구현과 병행할지(1안) vs 선완료할지(2안)*.
        - **1안 — ④ baseline 직후 구현 착수 + ③-C·③-P·③-I 스펙 병행** (그 스펙 종료는 뒤로 늘어남)
        - **2안 — ③-C·③-P·③-I까지 전 스펙 완료 후 구현 착수**

            | 항목 | 1안 (④ 후 구현 + 나머지 스펙 병행) | 2안 (전 스펙 완료 후 구현) |
            | --- | --- | --- |
            | 구현 착수 | ④ AXS baseline 직후(이른 편) | ③-C·③-P·③-I까지 완료 후(더 늦음) |
            | 재작업 리스크 | ↑ ③-C/③-P/③-I 미확정 위 일부 구현 | ↓ 스펙 안정 후 구현 |
            | IEC 62304 추적 | 스펙·구현 동시 → 추적 부담 | baseline 후 구현 → 깔끔 |
            | 전체 납기 | 빠름 | 느림 |

        - **공통 전제**: 어느 안이든 **구현 시작점 = ④ AXS baseline**(둘의 차이는 ③-C/③-P/③-I 스펙을 병행하느냐 선완료하느냐). **구현 기간은 미정 — SRS 확정 후 재산정**(gantt의 `③ GW SRS + 구현` 섹션에 *기간 미정* 막대로 표기).
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
        - **해결됨(보고)**: ② 전용 `clinic` 테이블 = **`clinic_region_mapping`을 `clinic`으로 승격 확정**(C안, 2026-07-01) · ④ **`connector`(아웃바운드)/`provider`(인바운드) 분리 유지 확정**(통합 안 함); `provider` 표기는 정규 토큰·enum 금지(레지스트리 FK는 선택).

    - **R9. Enroll 승인 주체 = C/S 확인 (확인만 · 결정 이미 반영)** — Scott 방향대로 **디바이스 enrollment 승인을 C/S 본인이 한다**로 구체화해 문서에 반영했다. 회의에서는 **"이렇게 하면 되냐" 확인만** 요청(변경 없으면 그대로 확정).
        - **배경**: GW 관리자(Admin)가 승인을 기다릴 수 없음 → **현장 설치를 담당한 C/S가 설치 + GW Console 승인까지 본인이 수행**(설치자가 곧 승인자). 이 사람 승인이 부트스트랩 신뢰 앵커라, LM 라이선스·Clinic-ID만으로 부족한 위·변조 가짜 등록을 현장 검증으로 차단한다(별도 공장 토큰/OOB 불요).
        - **흐름(반영됨)**: enroll(LM 라이선스·Clinic-ID 검증 + nonce·fingerprint 바인딩) → `device.status=pending`(인증 불가) → **C/S가 GW Console에서 승인** → `active`. 재설치·키 회전 시에도 동일 C/S 승인.
        - **문서 반영 위치**: SRS §2.3.1(2)·§7.2.3·§7.2.5·§7.9.2 · ARD §5.1 · OpenAPI(`enroll/complete`=202 pending, `PATCH /v1/devices/{id}`=승인 전이) · DBML(`device.pending`, `enrollment_token` 폐기) · 요구사항명세 FR-ENR-01·02.
        - **확인 포인트**: ① 승인 주체 = **C/S 본인**(Admin 아님) 맞나? · ② C/S에게 **GW Console 승인 권한(write)** 부여 맞나? · ③ **재설치 회전도 C/S 승인** 통과로 충분한가?

- 공유 사항 — 스펙 작성 순서 (SRS PR 이후 후속 스펙)
    - ③ GW SRS(+OpenAPI·DBML)를 한 PR로 baseline. **③ PR 시작(7/6)에 ①·②(One Pager)와 ④(AXS 전체 Sub-SRS, 2주)를 동시 착수**(병행). ③-C·③-P·③-I는 ③ baseline 이후 — **③-I는 GW 1주 초안 → 인프라 담당 완성**. 각 스펙은 **작성 → PR(리뷰·수정) → baseline** 생애주기.
    - 막대 색: **작성=기본 · PR=강조(밝은색) · ◆=baseline/마일스톤 · 회색=완료 · 빨강=외부 선결**. **pilot 8/15는 개발계획서(착수 품의·미승인) 내부 목표**(외부 확정 요구 아님). **AXS sandbox 자격은 스펙 작성엔 불요·E2E·pilot 직전에 필요**라 그 시점에 배치(확보 TBD).
    - **`③ GW SRS + 구현` 섹션에 `GW 구현 1안·2안` 막대를 둘 다 표기 → R7에서 택일.** 1안=④ AXS baseline 후 즉시(스펙 병행) / 2안=전 스펙 완료 후. 둘 다 ④ AXS 연동(첫 연동·테스트 필수) 이후·**기간 미정**(SRS 확정 후 재산정).
    - 어느 제품·단계에 무슨 문서인지는 Roadmap §4 표, 스펙 단위·유형 정본은 PRD §12.1. **본 gantt 정본 = [개발 Roadmap 결정 §3.9](<VT API Gateway — PRD (v2)/VT API Gateway — 개발 Roadmap 결정.md>)** (수정 시 그쪽을 먼저).

    ```mermaid
    gantt
        title 스펙 생애주기(작성→PR→baseline) + GW 구현 — 기간 잠정·일정 약속 아님
        dateFormat YYYY-MM-DD
        axisFormat %m/%d
        todayMarker stroke-width:3px,stroke:#d33,opacity:0.6

        section ③ GW SRS + API/DBML + GW 구현 (계약 SSOT → 구현)
        SRS 본문 작성            :done, srsw, 2026-06-15, 14d
        OpenAPI·DBML 작성·정합   :done, designw, 2026-06-19, 17d
        PR 리뷰·수정(본문+스키마) :active, srspr, 2026-07-06, 14d
        baseline v1.0 (통합)     :milestone, srsbl, after srspr, 0d
        GW 구현 1안 — ④ AXS baseline 후(스펙 병행) :active, impl1, after axsbl, 45d
        GW 구현 2안 — 전 스펙 완료 후 :active, impl2, after conbl infbl oidw, 45d

        section ① API 호환성 One Pager (③ PR 시 동시 착수)
        작성                  :op1w, 2026-07-06, 7d
        PR 리뷰·수정          :active, op1pr, after op1w, 7d
        baseline              :milestone, op1bl, after op1pr, 0d

        section ② Presigned One Pager (③ PR 시 동시 착수)
        작성                  :op2w, 2026-07-06, 7d
        PR 리뷰·수정          :active, op2pr, after op2w, 7d
        baseline              :milestone, op2bl, after op2pr, 0d

        section ④ AXS Sub-SRS (③ PR 시 ①②와 동시 착수)
        작성 (전체 Sub-SRS)    :axsw, 2026-07-06, 14d
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


