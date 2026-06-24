# VT API Gateway — 6/25 주간회의 Agenda

타입: [확정] 기결정 공식 확정/승인 · [논의] 방향 결정 필요 · [정보] 추가 입력·자료 확보
결정 칸: 잠정안(`?` = 회의에서 확정)

## A. 결정 안건 (이번 회의에서 확정)

| # | 항목 | 타입 | 설명 / 묻는 것 | 출처 | 결정(잠정) |
| --- | --- | --- | --- | --- | --- |
| 1 | 디바이스 정의·연결 모델 (확인) | [논의] | ARD §5는 디바이스가 GW에 직접 연결(무인 장비 머신 인증)되는 것처럼 보이는데, 그간 논의는 EzServer 경유였음 → 실제는 어느 쪽인가? (단순 확인) | ARD §5 | EzServer 경유만, 직접 연결 없음? |
| 2 | 업로드·스토리지 모델 정합 | [확정] | 개발계획서는 "업로드 세션"·S3/MinIO·"리전 signer"를 GW 범위로 둠. 합의는 GW 비발급·중계만(발급=CleverSpace/AXS) → 확정 방향. SRS/ARD는 이미 후자, 개발계획서만 정합 필요 | 개발계획서 §2·§5 | GW 비발급·중계 확정, 개발계획서 수정? |
| 3 | 라우팅 모델 ADR-11 + 헤더 적용 | [확정] | Vatech-Target 유무로 GW-API vs 프록시 구분 — 헤더 있으면 GW가 모든 API를 정의하지 않고 Vatech-Target 값(예: axs, cleverspace)으로 실제 전달 대상 서버를 결정해 그대로 중계, 없으면 GW 자체 API 호출. CCB 승인 + GW 클라이언트(EzServer, CleverOne 경유)의 Vatech-Target 부착 적응. 식별/버전 헤더는 Roadmap §5에서 이미 확정 | SRS Appx B #13 · Roadmap §5 | CCB 승인 → baseline 반영? |
| 4 | Webhook 클라우드 분배 | [논의] | CleverLab 갈래B 활성화 여부·시점 (CleverSpace는 대상 아님 확정) | SRS Appx B #16 | v1.0 제외, GW Open 후 결정? |
| 5 | 클리닉 GW 등록 주체 | [논의] | EzServer Console(잠정) vs CleverOne(각 PC); 클리닉=CleverOne 다수+EzServer 1개 | SRS Appx B #17 | EzServer Console(잠정) 유지? |

## B. 확인·액션 (결정 아님 — 상태확인/액션아이템)

| # | 항목 | 타입 | 설명 / 묻는 것 | 출처 | 결정(잠정) |
| --- | --- | --- | --- | --- | --- |
| 6 | AXS sandbox 자격증명 | [정보] | sandbox endpoint·OAuth client를 스트라우만이 제공해야 TC-01~04 가능 — 확보 시점 확정됐나? pilot(08-15) 블로커 | AXS 테스트환경 §4 | Straumann과 계약/제공 후? |

## C. 배정·이연 (담당·기한만 배정, 이번 회의 결정 불가)

| # | 항목 | 타입 | 설명 / 묻는 것 | 출처 | 결정(잠정) |
| --- | --- | --- | --- | --- | --- |
| 7 | 경로 B EOS 시점 | [논의] | 레거시 경로 종료 시점 | SRS Appx B #3 | ① One Pager 확정 시? |
| 8 | v1.0 목표 RPS·동시 세션 | [정보] | fleet 규모 수치 — 인프라/규모 PL 입력 | SRS Appx B #1 | 인프라/규모 PL 입력 후 확정? |
| 9 | RTO/RPO·유지보수 윈도우 | [정보] | 가용성 목표 — 인프라 | SRS Appx B #9 | 인프라 설계 단계 확정? |
| 10 | 감사·consent 보존 기간 | [정보] | 법정 보존 기간 — 품질/법무 | SRS Appx B #5 | 법정 기준(법무 확인) 후? |
| 11 | 호환성 매트릭스 확정본 | [정보] | One Pager 산출 의존 | SRS Appx B #8 | ① One Pager 확정 시? |

> 회의 불요(참고): SRS Appx B #6·#12·#14(LLD 자체 처리), #4·#15(gw/1.2·LLD 이연), #7·#10(이미 결정), #11(추후), #2 DNS apex(`gw.vatech.com` 확정).
