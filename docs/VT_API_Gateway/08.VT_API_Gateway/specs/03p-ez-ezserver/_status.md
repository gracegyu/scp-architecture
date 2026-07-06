# ③-P-EZ — EzServer GW 적응 (3·4단계)

- 상태: 미작성 (GW SRS 계약 안정화 후 1차 초안 → EzServer 팀 인계)
- 문서 유형: Engineering One Pager
- 범위: GW 경유 전환(3단계), ClinicID 포함·Region 인지(4단계). (AXS 갈래 A presigned 직접 업로드는 ④와 연계, Rust 전면 재개발은 후속 별도 트랙)
- 입력(spec_refs): ③ GW SRS(§4.5·§7.3·§7.6.6 MQTT·**§7.8.1 fleet heartbeat**), Roadmap §4, 실행 할당표, EzServer PMS SRS
- **필수 반영 항목(GW→EzServer 가이드)**:
  - **Fleet heartbeat**: EzServer는 `POST /v1/fleet/heartbeat`(GW SRS §7.8.1·design/openapi)를 **주기적으로 능동 호출**해야 한다. GW는 병원 방화벽 뒤의 EzServer를 폴링할 수 없으므로 생존 보고는 device→GW push가 유일하다. 호출 주기는 응답의 `nextIntervalSeconds`를 따르고(중앙 config로 하달), 본문에 appVersion·health metrics(디스크·큐·성공률)를 선택 포함한다. 정본 기본 주기·오프라인 임계값은 GW SRS Appendix B #34에서 확정.
  - **MQTT 하행 구독(범용 레일)**: EzServer는 브로커에 **outbound 지속 구독**으로 자기 클리닉 프리픽스 **`gw/clinic/{clinicId}/#`** 를 구독한다(GW SRS §7.6.6). **v1.0은 `webhook` stream만 처리**(AXS 이벤트 분배)하고 **모르는 stream은 무시**한다(미래 `announce`/`command`/`config` 추가 시 재구독·재배포 불요·forward-compat). QoS1·persistent(오프라인 버퍼). authz(cert/policy)로 **자기 클리닉 토픽만** 접근. 브로커 제품(IoT Core/Amazon MQ)·토픽 문법 매핑은 GW SRS Appendix B #4 확정 후.
- 작성 모델: GW 소유자 1차 초안 → EzServer 팀 인계
- TBD: MQTT 역방향(Edge 분배) 운영 주체 — ③ §7.6 TBD 연동
- 공식 등록처: TBD (제품 repo / VKS — 인계 시 결정)
