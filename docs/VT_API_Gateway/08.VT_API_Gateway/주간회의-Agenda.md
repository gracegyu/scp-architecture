# VT API Gateway — 6/25 주간회의 Agenda

- 이번 주 진행
    - ③ GW SRS 본문 정합화 계속(§1~§7, baseline 전) — 이번 주 upload·webhook·인프라 결정 반영
    - 라우팅 모델 전환: 3버킷 → ADR-11 target-routed proxy(`Vatech-Target` 유무로 GW고유 API/프록시 구분, verbatim bypass, 신규 upstream=레지스트리 1행)
    - 업로드 모델 변경: GW presigned 비발급 확정 — `/v1/uploads`·리전 Signer 폐기, 발급 주체=CleverSpace(②)·AXS(③), GW는 중계(bypass)만
    - Webhook 재정의: 유연 수신 + provider별 전용 호스트(`{provider}.webhook.gw.vatech.com`)로 발신자 식별(Host/SNI), 식별≠인증(HMAC); 클라우드 수신=CleverLab만(CleverSpace 대상 아님)
    - 배포·데이터 토폴로지 신설(§2.1.1): 멀티서버·멀티리전, 전역 일관(PostgreSQL 원본 복제)/리전 로컬(Redis 캐시); 1차 단일→2차 멀티리전, apex DNS `gw.vatech.com` 확정
    - EKS 정합 스택 재정리: 관리형(DB는 PostgreSQL 확정 / 제품은 Aurora 권장·단일 리전은 RDS 가능, 인프라 확정 예정)·ElastiCache·SQS·IoT Core·IRSA; 메시징 2-레그(A=SQS 내부 큐 / B=MQTT 엣지 전달)
    - 분배 지식 DB·관리 API 추가(org_mapping·webhook_provider·upstream_registry·delivery_channel·region_catalog) + 온보딩 자가등록(EzServer Console 잠정)
    - 디바이스 토큰 갱신=client_credentials 재발급(refresh token 미발급) 명문화
    - 문서 정합화: ARD(ADR-11·Router/PEP)·개발계획서(EKS 스택)·인증보안·Roadmap 동기화, Redis 키스페이스 카탈로그 신설, design(OpenAPI·DBML) SRS와 정합
    - 
- 논의 사항 (GW SRS 작성하면서 생긴 질문)
    | # | 항목 | 타입 | 설명 / 묻는 것 | 출처 | 결정 |
    | --- | --- | --- | --- | --- | --- |
    | 1 | 디바이스 정의·연결 모델 (확인) | [논의] | ARD §5는 디바이스가 GW에 직접 연결(무인 장비 머신 인증)되는 것처럼 보이는데, 그간 논의는 EzServer 경유였음 → 실제는 어느 쪽인가? (단순 확인) | ARD §5 | EzServer 경유만, 직접 연결 없음? |
    | 2 | 업로드·스토리지 모델 정합 | [확정] | 개발계획서는 "업로드 세션"·S3/MinIO·"리전 signer"를 GW 범위로 둠. 합의는 GW 비발급·중계만(발급=CleverSpace/AXS) → 확정 방향. SRS/ARD는 이미 후자, 개발계획서만 정합 필요 | 개발계획서 §2·§5 | GW 비발급·중계 확정, 개발계획서 수정? |
    | 3 | 라우팅 모델 ADR-11 | [확정] | Vatech-Target 유무로 GW-API vs 프록시 구분 — 헤더 있으면 GW가 모든 API를 정의하지 않고 Vatech-Target 값(예: axs, cleverspace)으로 실제 전달 대상 서버를 결정해 그대로 중계, 없으면 GW 자체 API 호출. CCB 승인 + GW 클라이언트(EzServer, CleverOne 경유)의 Vatech-Target 부착 적응. 식별/버전 헤더는 Roadmap §5에서 이미 확정 |  | CCB 승인 → baseline 반영? |
    | 4 | Webhook 클라우드 분배 | [논의] | CleverLab 갈래B 활성화 여부·시점 (CleverSpace는 대상 아님 확정) |  | v1.0 제외, GW Open 후 결정? |
    | 5 | 클리닉 GW 등록 주체 | [논의] | EzServer Console(잠정) vs CleverOne(각 PC); 클리닉=CleverOne 다수+EzServer 1개 |  | EzServer Console(잠정) 유지? |
    | 6 | AXS sandbox 자격증명 | [정보] | sandbox endpoint·OAuth client를 스트라우만이 제공해야 TC-01~04 가능 — 확보 시점 확정됐나? pilot(08-15) 블로커 | AXS 테스트환경 §4 | Straumann과 계약/제공 후? |
    | 7 | 경로 B EOS 시점 | [논의] | 레거시 경로 종료 시점 |  | ① One Pager 확정 시? |
    | 8 | v1.0 목표 RPS·동시 세션 | [정보] | fleet 규모 수치 — 인프라/규모 PL 입력 |  | 인프라/규모 PL 입력 후 확정? |
    | 9 | RTO/RPO·유지보수 윈도우 | [정보] | 가용성 목표 — 인프라 |  | 인프라 설계 단계 확정? |
    | 10 | 감사·consent 보존 기간 | [정보] | 법정 보존 기간 — 품질/법무 |  | 법정 기준(법무 확인) 후? |
    | 11 | 호환성 매트릭스 확정본 | [정보] | One Pager 산출 의존 |  | ① One Pager 확정 시? |
    - 타입: [확정] 기결정 공식 확정/승인 · [논의] 방향 결정 필요 · [정보] 추가 입력·자료 확보