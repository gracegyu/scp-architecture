# 인계 노트 — EzServer GW 적응 OnePager (③-P-EZ)

**From** Raymond(GW) → **To** EzServer 팀(Teddy·Thomas) · **Date** 2026-07-21
**대상 문서**: `EzServer-GW적응-OnePager.md`(이 노트와 같은 폴더) · **근거**: 7/16 주간회의 R3("EzServer 연동 Spec 초안=Raymond 작성→Thomas 전달·완성")

> 이 노트만 읽으면 OnePager를 어디까지 받았고, 무엇을 이어서 채워야 하며, 여러분 repo에 넣을 때 무엇을 맞춰야 하는지 파악됩니다.

---

## 1. 한 줄 요약

Raymond가 **① GW SRS에서 EzServer 개발 항목을 추출**하고 **② 기존 EzServer suite 코드(nginx/EAP/ELM/EPI(Rust)/WebConsole)를 분석**해, "**무엇을 · 어느 컴포넌트에서**" 까지 정리한 뼈대입니다. EzServer 팀은 각 작업 블록의 **`🔧 EzServer 팀 상세`(= "어떻게 구현")** 를 채워 완성하면 됩니다. 요구·착지 컴포넌트는 이미 정리돼 있습니다.

## 2. 받은 것 vs 채울 것

| | 내용 |
| --- | --- |
| **이미 정리됨(Raymond)** | 작업 블록 **WS-1~9** 분해 · 각 블록의 **착지 컴포넌트(파일 경로)** · **현황 격차**(신규 개발 vs 기존 확장) · GW SRS **앵커 매핑** · 데이터 흐름 다이어그램 · nginx config 예제 스케치 · 리스크 · **TBD 목록**(소유·확정 시점 포함) |
| **EzServer 팀이 채움** | 각 WS의 `🔧 EzServer 팀 상세`(설계·인터페이스·라이브러리·저장 방식·공수·순서) · 컴포넌트별 테스트 · IO Scanner 의존부(R1 확정 후) · 최종 baseline |

## 3. 작업 블록(WS) 개요 — 어디를 고치나

| 블록 | 기능 | 착지 컴포넌트 | 성격 |
| --- | --- | --- | --- |
| **WS-1** | 상행 라우팅·프록시(Bypass)·식별 헤더·내부 인증 | nginx(NGX)/Nginx Controller · EPI `http_client_factory` | 🆕 config + 🔧 헤더 |
| **WS-2** | 인증·온보딩(private_key_jwt·enroll·재-enroll) | EAP · EPI `generate_ezserver_id`·`post_clinics`·`post_auth_clients` · ELM | 🆕 서명 인프라 + 🔧 enroll |
| **WS-3** | 하행 이벤트 수신(Webhook/MQTT downlink) | EPI `upload_manager/mqtt_client`(rumqttc) | 🔧 확장 + 🆕 구독/envelope |
| **WS-4** | 대용량 업로드(presigned 직접) | EPI `upload_manager/` | 🔧 수정(발급주체 전환) |
| **WS-5** | Fleet heartbeat | EPI(신규 주기 task) | 🆕 신규 |
| **WS-6** | 로컬 온보딩 콘솔 | WebConsole `usePMSIntegration`·`PMSPanel`·`clients` | 🔧 패널·클라이언트 추가 |
| **WS-7** | 하위 호환·경로 B 이관 | nginx 라우팅 · EzServerLinker | 🔧 전환 |
| **WS-8** | IO Scanner 수집(0단계) | 미정 | ⬜ **TBD(R1)** |
| **WS-9** | 연동 등록(org-binding·AXS link 개시) | EPI/WebConsole | 🆕 신규 |

## 4. GW SRS 앵커 매핑 (계약 추적용)

각 WS가 소비하는 GW 계약 조항입니다. GW SRS는 **baseline v1.0 동결**(tag `spec-v1.0`·commit `275d153`, `vt-api-gateway/docs/specs/SRS.md`)이며, 이 SHA를 참조 기준으로 삼으세요.

- **WS-1**: §2.3.0 · §4.1.2 · §4.5.1 · §7.7.1 · ADR-11 (+ 오류 패스스루 §7.7.4 · 호환 경고 §7.7.3 · 타임아웃 §7.5.4)
- **WS-2**: §2.3.1 · §2.3.2 · §7.1.1 · §7.2 (차단상태 §7.2.4)
- **WS-3**: §7.6.6 · §2.3.6 (엣지 분배 §7.6.7 · ClinicResolution §7.3.1)
- **WS-4**: §2.3.5 · §4.1.4 · §7.4 (멱등키 §4.5)
- **WS-5**: §7.8.1
- **WS-6**: §2.3.1 [2]
- **WS-7**: §2.8
- **WS-9**: §2.3.4 · §7.3

## 5. 반드시 확정해야 할 TBD (미결)

| 항목 | 내용 | 소유·확정 시점 |
| --- | --- | --- |
| **IO Scanner↔EzServer 연동 방식** | 수집 제품·프로토콜·포맷·파이프라인(WS-8) — v1.0 우선 기능의 **선결** | 주간회의 R1 |
| **엣지 last-hop 분배 메커니즘** | 하행 envelope→클리닉 내 소비자(CleverOne/앱) 전달 방식(WS-3·§7.6.7) | EzServer + GW |
| **클라이언트 타임아웃 30s 확정** | GW deadline(≤24s) 역산 기준(§7.5.4 D4·Appendix B #25) — **EzServer 확인 필요** | EzServer |
| GW 라우팅 방식(A 헤더 vs B 경로) | nginx config 형태 결정 | 주간회의 R1 |
| 내부 구간 인증 수준 | client→EzServer 인증·zero-trust 여부 | EzServer 위협모델 |
| MQTT 브로커 endpoint·토픽 문법 | 브로커 제품(IoT Core/Amazon MQ) 확정 후 | ③-I 인프라 |
| 역방향 대상 이벤트 목록 | AXS가 통지할 이벤트·활성화 세부 | ④ AXS Sub-SRS |
| fleet heartbeat 기본 주기·오프라인 임계 | 정본 값 | GW SRS Appendix B |

> **선결 순위**: `IO Scanner 연동 방식(R1)` 이 v1.0 갈래 A 전체를 막습니다. 이게 확정돼야 WS-8과 WS-4/WS-3의 IO-Scanner-특정 세부가 열립니다.

## 6. 여러분 repo에 넣을 때 맞춰야 할 것 (repo intake)

관찰된 EzServer 팀 관례(`ezserver-pms-integration-onepager` 기준)에 맞추려면:

1. **⚠ 다이어그램 형식** — 이 OnePager는 **mermaid**(데이터 흐름 + nginx config)를 씁니다. 여러분의 `mdbuilder`(pandoc + wkhtmltopdf) 파이프라인은 **mermaid를 렌더하지 못합니다**. → **drawio + PNG로 재작성**하거나(여러분 관례: `*.drawio` + `*_diagrams_*.png`), mermaid를 사전 렌더해 이미지로 임베드해야 docx/pdf 빌드가 됩니다.
2. **파일명·빌드 등록** — 관례상 `Confidential_` 접두 + snake_case → 예 `Confidential_ezserver_gw_adaptation_onepager.md`. `mdbuilder.config.json`의 `docs[]`에 소스로 추가해야 docx/pdf 산출됩니다.
3. **언어** — 이 초안은 한국어입니다. 여러분 repo 문서·work item·PR이 영어이므로, intake 시 **영문화** 여부는 EzServer 팀이 판단하세요.
4. **브랜치·PR** — Azure DevOps `tasks/EZSV-####-*` 컨벤션. **EZSV work item 번호는 EzServer 팀이 생성**합니다(Raymond가 임의 부여하지 않음). 완성은 여러분 PR 리뷰 프로세스로.

## 7. 정본·소유권 이전

- **초안 SSOT(현재)**: `scp-architecture/.../specs/03p-ez-ezserver/EzServer-GW적응-OnePager.md`
- **인계 후 정본**: EzServer 팀이 지정하는 repo/위치(예 `ezserver-pms-integration-onepager` 또는 별도 repo). 확정되면 scp 원본은 **redirect stub**으로 바꿔 새 정본을 가리키게 합니다(GW의 IaC→`vt-api-gateway-infra`, SRS→`vt-api-gateway`와 동일 방식).
- **소유권**: 인계 후 ③-P-EZ 소유는 EzServer 팀(Teddy·Thomas)으로 이전(실행 할당표 `specs/00-execution-allocation.md`).

## 8. 첫 착수 제안 (EzServer 팀)

1. OnePager 정독 → 각 WS의 `🔧 EzServer 팀 상세`에 설계·공수 채우기(요구·착지 컴포넌트는 그대로 사용).
2. **R1(IO Scanner 연동 방식)** 조기 확정 — 갈래 A 선결.
3. **§7.5.4 D4 타임아웃 30s** 확정 회신(GW Appendix B #25를 닫음).
4. repo 위치 확정 → §6 관례로 intake(다이어그램 변환·파일명·mdbuilder 등록) → EZSV work item·브랜치·PR.

---

> 문의: Raymond(GW). GW 계약 조항 해석·앵커 확인은 GW SRS(baseline `spec-v1.0`)와 위 §4 매핑 참조.
