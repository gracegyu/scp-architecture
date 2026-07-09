# ③-P-EZ — EzServer GW 적응 (3·4단계)

> **이 파일의 역할 = 승격용 구조화 씨앗(seed).** ③ SRS 작업 중 이 문서로 갈 내용을 **최종 목차에 대응되게** 미리 정리해 둔다(발견 즉시 캡처·인사이트 유실 방지). 정식 Sub-SRS/문서 집필은 **의존하는 ③ SRS 절이 baseline된 뒤 승격**한다 — 몰아쓰기가 아니라 "옮겨 붙이고 살 붙이기". 승격 트리거: ① ③ 해당 절 동결 + ② 소유권 확정(GW 공통 아님) + ③ 레포/템플릿 존재. 근거: ③이 흔들리는 동안 자식 문서를 미리 쓰면 개명·재번호가 수십 절로 번져 유지면이 폭발한다.

- 상태: 미작성 (GW SRS 계약 안정화 후 1차 초안 → EzServer 팀 인계)
- 문서 유형: Engineering One Pager
- 범위: GW 경유 전환(3단계), ClinicID 포함·Region 인지(4단계). (AXS 갈래 A presigned 직접 업로드는 ④와 연계, Rust 전면 재개발은 후속 별도 트랙)
- 입력(spec_refs): ③ GW SRS(§2.3.0·§4.1.2·§4.5.1 라우팅(A+C)·§4.5·§7.3·§7.6.6 MQTT·**§7.8.1 fleet heartbeat**·§7.7.1 Vatech-* 헤더), Roadmap §4·§5.1, 실행 할당표, EzServer PMS SRS
- **필수 반영 항목(GW→EzServer 가이드)**:
  - **Fleet heartbeat**: EzServer는 `POST /v1/fleet/heartbeat`(GW SRS §7.8.1·design/openapi)를 **주기적으로 능동 호출**해야 한다. GW는 병원 방화벽 뒤의 EzServer를 폴링할 수 없으므로 생존 보고는 device→GW push가 유일하다. 호출 주기는 응답의 `nextIntervalSeconds`를 따르고(중앙 config로 하달), 본문에 appVersion·health metrics(디스크·큐·성공률)를 선택 포함한다. 정본 기본 주기·오프라인 임계값은 GW SRS Appendix B #34에서 확정.
  - **MQTT 하행 구독(범용 레일)**: EzServer는 브로커에 **outbound 지속 구독**으로 자기 클리닉 프리픽스 **`gw/clinic/{clinicId}/#`** 를 구독한다(GW SRS §7.6.6). **v1.0은 `webhook` stream만 처리**(AXS 이벤트 분배)하고 **모르는 stream은 무시**한다(미래 `announce`/`command`/`config` 추가 시 재구독·재배포 불요·forward-compat). QoS1·persistent(오프라인 버퍼). authz(cert/policy)로 **자기 클리닉 토픽만** 접근. 브로커 제품(IoT Core/Amazon MQ)·토픽 문법 매핑은 GW SRS Appendix B #4 확정 후.
  - **라우팅 변환 (A+C · 순정 nginx) — 7/9 R5 확정**: EzServer(nginx 리버스 프록시)는 CleverOne→EzServer 내부 구간의 **`Vatech-Target: {label}` 헤더(A안)** 를 읽어 **`{label}.gw.vatech.com` 서브도메인 + HTTPS(C안)** 로 GW에 전달한다(GW SRS §2.3.0·§4.1.2·§4.5.1·ADR-11). **순정 nginx + 제네릭 `map`**(라벨→서브도메인)만으로 구현 — split-horizon DNS·커스텀 모듈 불요. **내부 평문 HTTP → 외부 HTTPS 브리징**. **허용 라벨 화이트리스트 map** 권장(미허용 라벨 차단·GW도 미등록 라벨은 404로 SSRF 방어). AXS 경로(§4.1.4 경로③)는 URL·body **verbatim** 전달.
    - **헤더 규약**(GW SRS §2.3.0·§7.7.1·Roadmap §5.1): originator `Vatech-Product`/`Version`/`OS`(=CleverOne)는 **그대로 relay**, EzServer는 자신을 **`Vatech-Via: EzServer/{ver}`** 에 누적하고 `User-Agent: EzServer/{ver}` 부착. GW 인증 **`Authorization: Bearer <device 토큰>`** 은 EzServer가 붙인다. **외부(AXS)로는 내부 `Vatech-*` 를 보내지 않는다**(GW가 AXS OAuth·Organization-ID로 교체).
    - nginx 스케치(예시·확정은 인계 시):
      ```nginx
      map $http_vatech_target $gw_host {        # Vatech-Target 헤더 → GW 서브도메인
          default      "";                       # 미허용 라벨 = 차단
          axs          axs.gw.vatech.com;
          cleverspace  cleverspace.gw.vatech.com;
      }
      # if ($gw_host = "") { return 421; }       # 미허용 차단
      # proxy_pass https://$gw_host;  proxy_ssl_server_name on;  proxy_set_header Host $gw_host;
      # proxy_set_header Vatech-Via "EzServer/<ver>";  # originator Vatech-* 는 통과
      ```
- 작성 모델(**7/9 변경**): **Thomas(EzServer 팀)가 직접 작성** — GW(Raymond)는 **표준 계약만 제공**(§2.3.0 헤더·§4.5.1 라우팅·§7.7 COMPAT·§7.8.1 fleet·§7.6.6 MQTT), 초안 미작성. **v1.0 = Straumann IO(IntraOral) Scanner 연동(갈래A) 우선**(CleverOne 무관분 후행) · **IO Scanner↔EzServer 연동 방식 미정**(추후 확정 — 확정 후 해당 부분 구체화).
- TBD: MQTT 역방향(Edge 분배) 운영 주체 — ③ §7.6 TBD 연동
- 공식 등록처: TBD (제품 repo / VKS — 인계 시 결정)
