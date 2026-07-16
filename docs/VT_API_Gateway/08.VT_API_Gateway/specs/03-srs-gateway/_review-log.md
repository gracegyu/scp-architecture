# ③ GW SRS — 리뷰 코멘트 추적 (_review-log)

> **작업용 문서**. 각 스레드=시간순 대화(cid·↳parent). `다음 답변(초안)`=미게시 답변. 반영=vt-api-gateway PR 브랜치.

- **PR**: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/11766
- **리뷰어**: Scott·Thomas(필수)·Jack·James·Larry·Eric · 우리=전규현
- **최종 fetch**: 2026-07-15 · thread 33

---

## C-01 · docs/specs/SRS.md:2278 · [thread 79265]
- **[민진우(Thomas) · 2026-07-13T04:59 · cid 79265.1]**

  > From CodeReviewAgent(v0.4.1),
  > Appendix A Decision Log의 ADR-13 행이 공개키 컬럼을 `device.fingerprint`로 표기하고 있으나, 이 컬럼은 문서 전반(§1.4·§7.1.1·§7.2.6·DBML)에서 `device.client_public_key`로 명칭이 정정되었습니다. DBML 주석에도 "구 명칭 'fingerprint'을 정확화"라고 명시되어 있어, 본문 중 유일하게 남은 옛 명칭입니다. 구현자가 존재하지 않는 컬럼(`fingerprint`)을 참조하지 않도록 `device.client_public_key`로 통일해야 합니다.

- **[전규현(우리) · 2026-07-14T00:05 · cid 79265.2 ↳1]**

  > 맞습니다. Appendix A ADR-13 행의 device.fingerprint는 본문·DBML에서 이미 client_public_key로 정정된 컬럼의 옛 명칭입니다. 존재하지 않는 컬럼을 참조하지 않도록 그 행을 device.client_public_key로 통일하겠습니다.

- 조치: Appendix A ADR-13 행 device.fingerprint → device.client_public_key — 확정 후 반영
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-02 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:2247 · [thread 79266]
- **[민진우(Thomas) · 2026-07-13T04:59 · cid 79266.1]**

  > From CodeReviewAgent(v0.4.1),
  > `Target` 스키마의 timeout 예시값이 서로 모순됩니다. `connectTimeoutMs`(D1)=3000 + `responseTimeoutMs`(D2)=10000 = 13000ms 인데 `totalDeadlineMs`(D3)=12000ms 입니다. §7.5.4의 D1~D3 모델상 total_deadline은 프록시 호출 총 예산이므로, 연결에 3s를 쓰면 응답은 9s만에 잘려 D2(10s 응답 대기)가 실제로는 도달할 수 없게 됩니다. 예시값은 최소한 `connect + response ≤ total_deadline` 불변식을 만족하도록 조정하는 편이 좋습니다(예: total_deadline 14000 이상 또는 response_timeout 축소).

- **[전규현(우리) · 2026-07-14T00:06 · cid 79266.2 ↳1]**

  > 맞습니다. 예시값이 connect(3000)+response(10000)=13000 > total(12000)이라 §7.5.4의 connect+response ≤ total_deadline 불변식을 어깁니다. 예시를 불변식에 맞게 조정하겠습니다(예: totalDeadlineMs 14000). 이 수치는 예시이고 실제 값은 target SLA·§7.5.4·LLD 소관임을 함께 명시하겠습니다.

- 조치: OpenAPI Target 예시 timeout 조정(connect+response ≤ total, 예 total 14000)+예시임 명시 — 확정 후 반영
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-03 · docs/specs/SRS.md:924 · [thread 79267]
- **[민진우(Thomas) · 2026-07-13T04:59 · cid 79267.1]**

  > From CodeReviewAgent(v0.4.1),
  > "발행은 CI/ops 흐름이라 ... 별도 번호(§2.3.8)를 주지 않고 본 절에 함께 둔다"라고 서술하지만, 실제로 §2.3.8("운영자·Console 인증")이 다른 주제로 존재합니다. 매트릭스 발행 흐름에 부여하지 않겠다고 언급한 번호(§2.3.8)가 이미 별개 절에 사용되고 있어 독자가 혼동할 수 있습니다. 해당 괄호 참조를 삭제하거나 "별도 하위 절을 만들지 않는다" 정도로 표현을 완화하는 것이 좋습니다.

- **[전규현(우리) · 2026-07-14T00:06 · cid 79267.2 ↳1]**

  > 맞습니다. 매트릭스 발행 흐름에 '§2.3.8을 주지 않는다'고 썼는데 §2.3.8이 다른 주제(운영자·Console 인증)로 실재해 혼동됩니다. 해당 괄호 참조를 삭제하거나 '별도 하위 절을 만들지 않는다'로 완화하겠습니다.

- 조치: §924 §2.3.8 자기참조 삭제/완화 — 확정 후 반영
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-04 · docs/specs/SRS.md:1052 · [thread 79268]
- **[민진우(Thomas) · 2026-07-13T04:59 · cid 79268.1]**

  > From CodeReviewAgent(v0.4.1),
  > 참조 표기 오타 — "FR-SES-06 해당 없음, §7.4·§7.4 FR-SES 매핑."에서 `§7.4`가 중복되어 있습니다(`§7.4·§7.4`). 하나로 정리하는 편이 좋습니다.

- **[전규현(우리) · 2026-07-14T00:13 · cid 79268.2 ↳1]**

  > 오타 맞습니다. '§7.4·§7.4' 중복을 하나로 정리하겠습니다.

- 조치: §1052 §7.4·§7.4 → §7.4 — 확정 후 반영
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-05 · (파일 미지정·일반) · [thread 79269]
- **[민진우(Thomas) · 2026-07-13T04:59 · cid 79269.1]**

  > From CodeReviewAgent(v0.4.1),
  > ## Code Review (Other)
  >
  > 이 PR은 실행 코드가 아니라 GW의 SRS(③)와 dev-chain-design 산출물(DBML·OpenAPI·Redis 키스페이스·well-known 샘플·db-jsonb·api-surface 매트릭스)을 placeholder에서 정본 초안으로 이관하는 대규모 문서 커밋입니다. 전반적으로 완성도와 내부 일관성이 높습니다. 특히 상태/스코프 enum이 DBML과 OpenAPI 사이에서 완전히 일치하고(device_status·webhook_state·target_profile·region_status·audit_result·operator_status·grant_status·operator_role_type·policy_scope·config_scope), Appendix B의 미결 항목 번호(1~48)도 중복·누락 없이 정합합니다. `client_id`(gwc_+22자=26자)·`device_id`(UUIDv7) 같은 식별자 규격의 수치도 내부적으로 맞습니다. DBML의 nullable UNIQUE(NULL distinct) 문제나 OpenAPI의 미참조 컴포넌트 등 잠재적 지적사항은 각 파일에 LLD 주석·설계 의도로 명시되어 있어 리뷰 지침에 따라 제외했습니다.
  >
  > 교차 절 관점에서 확인이 필요한 사항:
  >
  > - **환자 데이터 삭제·감사(Change History 2025-12-23 규정)**: GW는 PHI 영상 본문을 저장/삭제하지 않으므로(presigned 직결·GW 미경유) 이 규정의 직접 대상은 아닙니다. 다만 webhook payload(PHI 포함 가능)는 `webhook_event.payload_encrypted`로 암호화 저장되며 "삭제 당분간 미고려"(Appendix B #36)로 남아 있습니다. 현재는 삭제 경로 자체가 없어 위반은 아니지만, 향후 payload purge/retention을 구현할 때 "관리자 승인 필수·감사 필수필드 기록·QA 통보 및 별도 테스트" 규정을 반드시 반영해야 하므로 이를 Appendix B #36의 결정 근거에 명시해 두는 것을 권장합니다. (payload 열람 break-glass는 이미 `webhook.payload.view` 감사로 잘 처리되어 있습니다.)
  >
  > - **Admin API 노출면과 OpenAPI `servers`**: OpenAPI `servers`가 apex `gw.vatech.com` 하나뿐인데 `/v1/admin/*`는 §4.5.1·§6.6.2상 공개 edge에서 도달 불가한 내부 전용 호스트(`admin.gw.vatech.com`)로 서빙됩니다. 단일 spec·code-first 설계상 의도된 것이고 문서에 서술돼 있으나, 계약을 소비하는 Console 개발자 혼동을 줄이려면 `servers`에 내부 host를 추가하거나 admin 태그 설명에 호스트 분리를 명시하는 것이 좋습니다.
  >
  > - **§7.1.2(FR-AUTH-02, 사내 호출자 JWT 발급·검증)에 대응하는 OpenAPI 엔드포인트 부재**: device는 `/v1/auth/token`(private_key_jwt), operator는 Entra OIDC로 커버되지만 "사내 서비스 호출자용 JWT 발급/검증" 경로는 OpenAPI에 정의가 없습니다. §7.1.1과의 중복으로 인한 의도적 위임인지, 아니면 누락인지 확인이 필요합니다.
  >
  > 라인 코멘트로 지적한 4건(옛 컬럼명 `device.fingerprint` 잔존, Target timeout 예시값 모순, §2.3.8 자기참조 혼동, §7.4 중복 오타) 외의 구조적 결함은 발견되지 않았습니다.
  >
  > 4 line-specific finding(s) were posted as inline comments.

- **[전규현(우리) · 2026-07-14T00:13 · cid 79269.2 ↳1]**

  > 세 가지 모두 반영하겠습니다.
  >
  > (a) payload 보존·삭제 — 맞습니다. 현재는 삭제 경로 자체가 없어 위반은 아니지만, 향후 purge/retention을 구현할 때 2025-12-23 규정(관리자 승인 필수·감사 필수필드 기록·QA 통보 및 별도 테스트)을 반드시 따르도록 Appendix B #36 결정 근거에 명시해 두겠습니다. payload 열람 break-glass는 이미 webhook.payload.view 감사로 처리되고 있습니다.
  >
  > (b) OpenAPI servers·Admin 호스트 — /v1/admin/*이 내부 전용 host(admin.gw.vatech.com)로 서빙되는 점이 servers(apex 하나)에서 드러나지 않아 Console 개발자가 혼동할 수 있습니다. admin 태그 설명에 '내부 전용 host(admin.gw.vatech.com) 서빙·공개 edge 도달 불가'를 명시하고, 필요 시 servers에 내부 host 항목을 추가하겠습니다.
  >
  > (c) §7.1.2 사내 호출자 JWT — 의도적 위임이며 누락이 아닙니다. §7.1.2는 'JWT 발급·무상태 검증 역량'을 기술한 것이고, 실제 발급 엔드포인트는 §7.1.1의 /v1/auth/token(device private_key_jwt)으로 수렴합니다. 사내 호출자 중 EzServer는 그 device 인증을 쓰고, CleverOne은 EzServer를 경유(CleverOne→EzServer→GW)하므로 GW에 직접 인증하지 않으며, 사람 운영자는 §7.1.4(Entra)입니다. 즉 별도 토큰 엔드포인트가 필요한 제3의 인증 경로는 없습니다. 다만 §7.1.2 문구가 '사내 서비스용 JWT 발급'이라 독립 경로처럼 읽히니, '발급=§7.1.1로 수렴, 검증=control plane 무상태(엔드포인트 아님)'로 서술을 명확히 하겠습니다.

- 조치: (a) Appendix B #36 근거에 2025-12-23 규정 명시 · (b) OpenAPI admin 태그(+필요 시 servers)에 내부 host 명시 · (c) §7.1.2 서술 명확화(발급=§7.1.1 수렴·검증=무상태·별도 엔드포인트 없음) — 확정 후 반영
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-06 · docs/specs/SRS.md:1440 · [thread 79271]
- **[민진우(Thomas) · 2026-07-13T05:12 · cid 79271.1]**

  > From CodeReviewAgent(v0.4.1),
  > §5.5의 `presigned URL TTL: 5~15분(§7.4.2)` 항목이 **존재하지 않는 하위 절 §7.4.2**를 참조한다. §7.4는 presigned 발급을 target(CleverSpace/AXS)에 위임하면서 하위 절(7.4.1~7.4.5)이 모두 제거된 flat 절이 되었는데, 옛 번호 참조만 남았다. 더구나 §7.4는 "GW는 presigned를 발급하지 않는다"고 명시하므로, presigned URL TTL(5~15분)을 GW의 성능 요구로 §5.5에 두고 §7.4.2로 연결하는 것은 위임 원칙과도 모순된다. TTL이 발급 주체(② One Pager/④) 소유임을 반영해 항목을 옮기거나 참조를 정정해야 한다(같은 §7.4.2 dangling 참조가 §6.1 line 1461에도 있음).

- **[전규현(우리) · 2026-07-14T00:13 · cid 79271.2 ↳1]**

  > 맞습니다. §7.4는 발급을 target에 위임하며 하위 절이 없어 §7.4.2는 dangling이고, presigned TTL을 GW 성능요구로 두는 것도 위임 원칙과 어긋납니다. TTL은 발급 주체(② One Pager/AXS④) 소유임을 반영해 항목을 옮기거나 참조를 정정하겠습니다.

- 조치: §5.5 presigned TTL의 §7.4.2 dangling 정정·발급주체 소유로 이동 — 확정 후 반영
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-07 · docs/specs/SRS.md:1461 · [thread 79272]
- **[민진우(Thomas) · 2026-07-13T05:12 · cid 79272.1]**

  > From CodeReviewAgent(v0.4.1),
  > §6.1의 안전 규칙 "객체 키·메타데이터에도 PHI를 담지 않는다(§7.4.2)"가 **존재하지 않는 §7.4.2**를 참조한다. §7.4에는 객체 키/메타데이터를 다루는 하위 절이 없다(GW가 storage·서명을 소유하지 않으므로). PHI 비저장 규칙은 안전성 크리티컬 항목이므로, 실재하는 절(§6.4 / §7.3.3 등)로 참조를 정정해야 traceability가 유지된다.

- **[전규현(우리) · 2026-07-14T00:14 · cid 79272.2 ↳1]**

  > 맞습니다. §7.4엔 객체키/메타데이터 하위 절이 없어 §7.4.2는 dangling입니다. 안전성 크리티컬 규칙이라 실재 절(§6.4/§7.3.3)로 참조를 정정해 traceability를 유지하겠습니다.

- 조치: §6.1 안전규칙 §7.4.2 → §6.4/§7.3.3 — 확정 후 반영
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-08 · docs/specs/SRS.md:1476 · [thread 79273]
- **[민진우(Thomas) · 2026-07-13T05:12 · cid 79273.1]**

  > From CodeReviewAgent(v0.4.1),
  > §6.2 보안 8항목 표의 Integrity 행이 **존재하지 않는 §7.4.5(checksum/ETag)·§7.4.4(idempotency)**를 참조한다. §7.4는 하위 절이 없고, 무결성·멱등은 §7.4 "위임 경계"상 발급 주체(CleverSpace②/AXS④) 책임으로 명시돼 있다. 같은 행의 `§7.6.4`(멱등)·`§7.6.2`(HMAC)는 실재하지만 `§7.4.4`·`§7.4.5`는 dangling이므로 참조를 제거·정정해야 한다.

- **[전규현(우리) · 2026-07-14T00:14 · cid 79273.2 ↳1]**

  > 맞습니다. 무결성·멱등은 §7.4 위임 경계상 발급 주체(CleverSpace②/AXS④) 책임이고 §7.4.4·§7.4.5는 dangling입니다. 같은 행의 §7.6.4·§7.6.2는 실재하니 §7.4.4·§7.4.5 참조만 제거·정정하겠습니다.

- 조치: §6.2 Integrity 행 §7.4.4/§7.4.5 dangling 제거 — 확정 후 반영
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-09 · docs/specs/SRS.md:2227 · [thread 79274]
- **[민진우(Thomas) · 2026-07-13T05:12 · cid 79274.1]**

  > From CodeReviewAgent(v0.4.1),
  > §7.9.1 관리 API 열거에 §7.8.5(line 2209)가 정의한 **전 클리닉 횡단 조회 `GET /v1/admin/clients`가 누락**되어 있다. §7.9.1은 클리닉 드릴다운 `GET /v1/admin/clinics/{clinicId}/clients`만 나열하는데, §7.8.5는 두 엔드포인트(횡단 + 드릴다운)를 모두 정의하며 "특정 버전 미만 클리닉 전체" 업그레이드 캠페인의 핵심은 횡단 API다. 관리 API 정본 절(§7.9.1)에도 `GET /v1/admin/clients`를 함께 명시해야 OpenAPI 계약과 정합한다(Appendix B #48도 드릴다운만 언급).

- **[전규현(우리) · 2026-07-14T00:14 · cid 79274.2 ↳1]**

  > 맞습니다. §7.8.5가 정의한 전 클리닉 횡단 조회 GET /v1/admin/clients가 §7.9.1 관리 API 열거에서 빠졌습니다. 업그레이드 캠페인의 핵심이라 §7.9.1에 추가해 OpenAPI 계약과 정합시키겠습니다(Appendix B #48도 함께 갱신).

- 조치: §7.9.1에 GET /v1/admin/clients 추가·Appendix B #48 갱신 — 확정 후 반영
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-10 · docs/specs/SRS.md:1342 · [thread 79276]
- **[민진우(Thomas) · 2026-07-13T05:12 · cid 79276.1]**

  > From CodeReviewAgent(v0.4.1),
  > §4.4 Software Interface 표가 캐시를 `Redis | 구현 시 확정`으로 적었으나, §3.1.2·§1.4·§6.4는 캐시 엔진을 **Valkey(Amazon ElastiCache for Valkey)로 이미 "채택/확정"**했다. 제품명(Redis vs Valkey)과 확정 상태("구현 시 확정" vs 이미 채택)가 다른 절과 어긋난다. §1.4가 정의한 "Redis(호환)=Valkey" 관례를 감안해도, 확정 사항을 미확정처럼 적어 혼동을 준다 — §3.1.2와 동일하게 `ElastiCache for Valkey(확정)`로 통일하는 것이 좋다.

- **[전규현(우리) · 2026-07-14T00:16 · cid 79276.2 ↳1]**

  > 맞습니다. §3.1.2·§1.4·§6.4는 캐시 엔진을 Valkey(Amazon ElastiCache for Valkey)로 확정했는데 §4.4 표만 'Redis | 구현 시 확정'이라 어긋납니다. §4.4를 'ElastiCache for Valkey(확정)'로 통일하겠습니다.

- 조치: §4.4 캐시 'Redis/구현 시 확정' → 'ElastiCache for Valkey(확정)' — 확정 후 반영
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-11 · docs/specs/SRS.md:2294 · [thread 79278]
- **[민진우(Thomas) · 2026-07-13T05:12 · cid 79278.1]**

  > From CodeReviewAgent(v0.4.1),
  > Appendix B #20이 "비AWS 포터블 배포(**§2.1.2** 초안) 폐기"라며 §2.1.2를 참조하지만 본 문서에는 §2.1.2가 없다(§2.1 → §2.1.1 → §2.2). 폐기된 초안 절 번호를 가리키는 dangling 참조라 독자가 근거를 찾을 수 없다. 참조를 삭제하거나 "구 §2.1.2 초안(현재 삭제)" 정도로 표기하는 것이 좋다.

- **[전규현(우리) · 2026-07-13T23:58 · cid 79278.2 ↳1]**

  > 동의합니다. Appendix B #20의 '§2.1.2 초안' 참조는 현재 문서에 없는 절 번호를 가리키는 dangling 참조입니다(§2.1 → §2.1.1 → §2.2). 해당 참조를 삭제하거나 '구 §2.1.2 초안(현재 삭제)' 정도로 표기해 독자가 근거를 찾을 수 있게 정정하겠습니다.

- 조치: Appendix B #20의 §2.1.2 dangling 참조 삭제 또는 '구 §2.1.2 초안(삭제됨)'로 표기 — 확정 후 반영
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-12 · (파일 미지정·일반) · [thread 79279]
- **[민진우(Thomas) · 2026-07-13T05:12 · cid 79279.1]**

  > From CodeReviewAgent(v0.4.1),
  > ## Code Review (Other) — Update 1
  >
  > 이 증분 diff는 SRS.md를 placeholder에서 2,388줄 규모의 정본 초안으로 이관하는 대규모 문서 커밋이다. 전반적 완성도·내부 일관성은 [Previous Review]가 평가한 대로 높으며, 이번 리뷰는 이전에 지적되지 않은 **신규 결함**만 보고한다.
  >
  > **[Previous Review] findings 처리 결과 — 해소된 항목 없음.** 이번 diff는 SRS.md만 변경하므로 OpenAPI(vt-api-gateway.openapi.yaml)의 Target timeout 예시 모순은 그대로이고, SRS.md 내부의 세 지적(ADR-13 행의 옛 컬럼명 `device.fingerprint` 잔존 line 2278 · §2.3.7의 §2.3.8 자기참조 혼동 line 924 · §2.7.1의 `§7.4·§7.4` 중복 오타 line 1052)도 현재 본문에 그대로 존재해 **미해소** 상태다(리뷰 지침에 따라 상세는 재기술하지 않음).
  >
  > **신규 결함의 공통 뿌리 — §7.4 하위 절 제거로 인한 orphan 참조.** 이번에 가장 눈에 띈 구조적 문제는, presigned 발급을 target에 위임하기로 결정하면서(§4.1.4·ADR-03/04 철회) §7.4가 하위 절(7.4.1~7.4.5) 없는 flat 절로 축약되었는데, 그 옛 번호를 가리키는 상향 참조가 §5.5·§6.1·§6.2에 남아 있다는 점이다(line 1440·1461·1476). 이는 단순 링크 깨짐을 넘어, presigned TTL·checksum·객체키 PHI 규칙 같은 항목을 여전히 "GW 소유(§7.4.x)"로 귀속시켜 §7.4의 위임 원칙과 모순을 일으킨다 — IEC 62304 추적성 통제 문서에서 요구사항 귀속·cross-reference 정합은 중요하므로 우선 정정 대상으로 본다.
  >
  > 그 외 관리 API 열거 누락(§7.9.1이 §7.8.5의 횡단 `GET /v1/admin/clients` 미포함), 캐시 제품·확정 상태 표기 불일치(§4.4), 폐기 근거의 dangling 절 참조(§2.1.2)를 라인 코멘트로 지적했다. 모두 문서 정합·traceability 수준의 문제이며, 아키텍처·계약 자체를 바꾸는 결함은 발견되지 않았다. 참고로 Appendix B의 결정 로그 주석에 나타나는 OpenAPI operation 수치(#6=55 ops / #47=42 / #48=45)가 서로 다르나, 이는 서로 다른 시점의 스냅샷 breadcrumb로 판단되어 라인 지적에서는 제외했다.
  >
  > 6 line-specific finding(s) were posted as inline comments.

- **[전규현(우리) · 2026-07-14T00:17 · cid 79279.2 ↳1]**

  > §7.4 dangling 등 재지적 사항은 각 라인 스레드(C-05·06·07 등)에서 처리하겠습니다. op 수치는 정본(redocly 기준·Appendix B #6=55)이 맞고, 결정로그 주석의 42·45는 작성 중 시점 스냅샷이라 현재 수치로 정합·정리하겠습니다.

- 조치: Appendix B 결정로그 op 수치(42·45) → 현재 55로 정합/정리 — 확정 후 반영
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-13 · docs/specs/SRS.md:239 · [thread 79385]
- **[임건혁(Jack) · 2026-07-13T06:34 · cid 79385.1]**

  > @<B62326D5-BE2F-6C22-BDD5-19CE8D112C90> @<8A8E7F25-5884-64CC-9CD9-804A85DF8F64> @<E616BABA-1CD7-6573-A367-AFAF4633BD3C> 현재 EKS 네트워크 구성 상 AWS Regional NAT Gateway를 사용 예정이고 해당 기능은 NAT Gateway의 ip가 고정 되지 않습니다. 외부 클라이언트 연동시 IP whitelist 방식만 지원하는 클라이언트가 있으면 비용 감수하더라도 ip 고정 NAT Gateway 사용이 필요합니다.

- **[전규현(우리) · 2026-07-13T23:48 · cid 79385.2 ↳1]**

  > 맞습니다. SRS도 같은 요구를 이미 담고 있습니다 — 외부(C) target이 IP whitelist를 요구하면 egress는 pod별 임시 IP가 아니라 AZ/리전별 NAT의 고정 EIP 집합이어야 한다는 요구입니다(§2.1.1·§7.5.3·§2.6·FR-INT-03). 다만 지적하신 대로 AWS Regional NAT Gateway의 기본 IP는 비고정이라, 이 요구를 실현하려면 말씀하신 고정 IP(EIP) 기반 NAT가 필요합니다. 비용을 감수하고 그렇게 provisioning하는 데 동의합니다.
  >
  > 대신 비용을 제한하기 위해 고정-IP egress는 전역이 아니라 IP whitelist가 필요한 대상(외부 C·requireStaticEgressIp)에만 선택 적용하고, 나머지(내부 B·IP 고정 불필요 대상)는 표준 NAT를 쓰겠습니다. SRS도 이미 '고정 egress whitelist는 외부(C) 한정'으로 범위를 두고 있습니다(§2.1.1). 실제 NAT 토폴로지(EIP 기반 NAT·대상별 라우팅)와 비용은 ③-I 소관이고, SRS는 '요구 대상엔 고정 egress IP' 요구까지만 기술합니다.
  >
  > 문서엔 이 인프라 함의가 분명해지도록 'Regional NAT Gateway 기본 IP는 비고정 → requireStaticEgressIp 대상은 고정 IP(EIP) egress로 provisioning(비용 수반·③-I)'이라는 한 줄을 §2.1.1(또는 §7.5.3)에 덧붙이겠습니다.

- **[임건혁(Jack) · 2026-07-14T02:06 · cid 79385.3 ↳1]**

  > @<B62326D5-BE2F-6C22-BDD5-19CE8D112C90> Regional NAT Gateway도 고정 ip를 할당할 수 있는 대신 새로운 az로 워크로드 확장시 인프라의 수동 개입이 필요합니다. AZ를 추가하는 빈도가 흔하지 않고 손이 많이 가는 작업은 아니기에 그대로 진행하셔도 됩니다. 다만 Straumann에 ip 허용 요청할때 각 prod 리전의 NAT Gateway에 붙은 IP를 전부 요청해주시면 됩니다. 해당 클라이언트에서 등록 ip 개수를 제한하는 경우가 있다면 말씀 부탁드립니다.

- **[전규현(우리) · 2026-07-15T01:02 · cid 79385.4 ↳1]**

  > 감사합니다. 그대로 진행하겠습니다 — Regional NAT Gateway 방식으로 두고, 새 AZ 확장 시 수동 IP 추가가 드물게 필요하다는 점 인지했습니다. Straumann whitelist 요청 시 각 prod 리전 NAT Gateway의 egress IP를 전부 제출하겠습니다. AXS 문서를 확인하니 IP whitelist(및 등록 IP 개수 제한) 언급이 없고, AXS의 'whitelist'는 애플리케이션(client) 승인이라 IP 기반이 아닙니다 — 즉 문서상 개수 제한은 없습니다. prod 리전도 소수라 리전당 egress IP가 몇 개 수준이어서 제한 우려는 낮습니다. 향후 IP whitelist를 요구하는 다른 target이 생기면 그때 개수 제한을 확인하겠습니다.
  >
  > GW SRS에는 '고정·유한·열거 가능한 egress IP 집합을 whitelist에 등록한다'는 논리 요구까지만 두고, NAT Gateway 구성·AZ 확장 시 IP 추가·리전별 IP 목록 같은 구체 구현은 ③-I(Infra Sub-스펙)에 정리하겠습니다.

- 조치: §2.1.1 NAT note 논리화(구체=③-I)·Straumann whitelist에 전 prod 리전 egress IP 등록·**AXS 문서상 IP whitelist/개수 제한 없음(확인 완료)**·NAT/AZ 구체=③-I seed
- 반영: 반영완료(로컬)·Jack에 재답변 게시함(수긍 대기)
- 상태: Resolved

## C-14 · docs/specs/SRS.md:1103 · [thread 79387]
- **[임건혁(Jack) · 2026-07-13T06:53 · cid 79387.1]**

  > @<B62326D5-BE2F-6C22-BDD5-19CE8D112C90> @<8A8E7F25-5884-64CC-9CD9-804A85DF8F64> Aurora Postgres 15 버전 기준으로 커뮤니티 지원이 2027년 11월, Aurora DB는 2028년 2월 29일입니다. 가능하면 17 버전 사용을 권장하고 현재 사용중이거나 사용 예정인 Extension 등이 17 버전에서의 지원 여부는 리스트업 후 검토해보겠습니다.

- **[전규현(우리) · 2026-07-13T23:37 · cid 79387.2 ↳1]**

  > 좋습니다. 말씀하신 EOL 여유를 고려해 엔진 버전을 PostgreSQL 17로 올리겠습니다. 10월 릴리스 이후 다년 운영을 감안하면 15(커뮤니티 2027-11·Aurora 2028-02 EOL)보다 17이 지원 런웨이가 넉넉합니다. SRS의 '15.x 확정'을 '17.x'로 갱신하겠습니다(§3.1.2·§4.4·Appendix B #18). Aurora PostgreSQL·Global Database가 17을 지원하는 것도 확인해 반영하겠습니다.
  >
  > Extension 17 호환은 말씀하신 대로 리스트업·검토 결과에 따르겠습니다. Prisma·스키마 자체는 버전 영향이 거의 없고, 혹시 특정 Extension이 17에서 미지원이면 그때 대안(마이너 조정 또는 대체)을 함께 정하겠습니다. 정확한 마이너 버전과 Extension 확정은 인프라/LLD 소관으로 두겠습니다.

- 조치: §3.1.2·§4.4·Appendix B #18 'PostgreSQL 15.x → 17.x' 갱신 · Aurora/Global DB 17 지원 확인 · Extension 17 호환 검토 결과 반영(인프라/Jack) — 확정 후 반영
- 반영: 반영완료(로컬·미push)
- 상태: Resolved

## C-15 · docs/specs/SRS.md:1112 · [thread 79389]
- **[임건혁(Jack) · 2026-07-13T06:55 · cid 79389.1]**

  > @<B62326D5-BE2F-6C22-BDD5-19CE8D112C90> @<8A8E7F25-5884-64CC-9CD9-804A85DF8F64> @<E616BABA-1CD7-6573-A367-AFAF4633BD3C> 
  > 모니터링 스택은 Loki, Tempo, Mimir (Prometheus full compatible) 사용 및 중앙 Grafana에서 대시보드 + 알람 처리하고 있습니다.

- **[전규현(우리) · 2026-07-14T00:17 · cid 79389.2 ↳1]**

  > 공유 감사합니다. §6.3.2를 실제 중앙 스택에 맞춰 갱신하겠습니다 — GW는 구조화 로그(Pino)·OTel로 생성·노출하고, 중앙 수집·저장은 Loki·Tempo·Mimir(Prometheus 호환) + 중앙 Grafana(대시보드·알람)로 명시하겠습니다. 수집 에이전트·백엔드 세부는 인프라(③-I) 소관으로 둡니다.

- 조치: §6.3.2 백엔드 스택을 Loki·Tempo·Mimir·중앙 Grafana로 갱신 — 확정 후 반영
- 반영: 반영완료(로컬·미push)
- 상태: Resolved

## C-16 · docs/specs/SRS.md:233 · [thread 79434]
- **[김성훈(Scott) · 2026-07-13T10:30 · cid 79434.1]**

  > ### Webhook 수신·저장·분배 순서가 데이터 주권 요구와 충돌합니다.
  >
  > - GeoDNS는 **호출자(AXS) 최근접 리전**으로만 분기하며 대상 리전을 정하지 않음 (SRS §2.1.1, L326 / L261).
  > - 수신 GW가 HMAC 검증 직후 **PHI 포함 payload를 리전 로컬 DB에 암호화 저장**하고 즉시 2xx ACK (§7.6.3, L1983–1990).
  > - **대상 리전 판정은 큐 이후 Dispatcher가 수행**하며 교차 리전 전달 포함 (§7.6.7, L2026).
  >
  > 따라서 멀티 리전(gw/1.2)에서 **수신 리전 ≠ 클리닉 매핑 리전**이면, PHI가 매핑 리전 밖 DB에 at-rest 저장됩니다.
  > → FR-RGN-03 (§6.1, L1461 "PHI를 매핑된 리전 밖으로 내보내지 않으며")과 직접 충돌하며, "v1.0을 재설계 없이 멀티 리전으로 확장"(§6.3.1, L1491) 주장의 성립을 깹니다.
  >
  > **예시:** 서울 매핑 클리닉 → AXS(EU/US)가 `patient.created`(환자명·생년월일) 발신 → GeoDNS가 US/EU GW로 라우팅 → 해당 리전 DB에 PHI 저장 → 이후 서울로 교차 분배. 한국 환자 PHI가 US/EU에 잔류.
  >
  > ### 권고 해법 (택1, 상단 권장)
  > 1. **(권장) 리전을 발신 target 콜백 설정으로 전파** — 통합 설정 시 선택된 리전을 AXS에 **리전(또는 클리닉)별 콜백 URL**로 등록해 AXS가 **대상 리전 endpoint로 직접 발신**. 최근접-수신·교차-저장 자체가 발생하지 않음. 교차 리전 지연 없음. (레지스트리 `inbound_host`를 리전별로 확장 — §7.6.2.)
  > 2. **수신 리전에서 저장 전 대상 판정 → 대상 리전으로 위임** — 매핑은 전역 일관(L332)이라 수신 리전에서 조회 가능. payload를 로컬 저장하지 않고 대상 리전 DB/SQS/KMS로 넘긴 뒤 ACK. 단 "빠른 ACK p95<100ms"(L1439)와의 교차 리전 지연 trade-off를 §7.6.3에 명시 필요.
  > 3. (fallback) 수신 리전 임시 저장을 허용하되 **주권 등가 리전군 내로 GeoDNS 대상을 제약** + 처리 후 즉시 삭제 — 잔류·복잡도 부담으로 비권장.
  >
  > ### 요청 사항
  > §7.6.3 / §2.1.1에 **"payload는 대상(매핑) 리전에서만 at-rest 저장한다"** 는 요구를 명문화하고, 위 1안(권장)의 콜백 리전 전파를 §7.6.2 레지스트리 모델에 반영해 주십시오.

- **[전규현(우리) · 2026-07-13T23:24 · cid 79434.2 ↳1]**

  > 문서를 확인해 보니 말씀하신 대로였습니다. AXS webhook 구독(`POST /v1/webhook/subscribe`)의 요청 본문은 events·callbackUrl·hmac 세 필드뿐이고 organizationId가 없습니다. 인증도 파트너 단위 client_credentials 하나여서, 구독과 콜백은 통합 파트너 기준으로 이벤트 타입별 콜백 하나가 붙을 뿐이고 조직 구분은 전달되는 payload의 organizationId로만 옵니다. 게다가 AXS 서버가 US·EU 리전만 있어 발신도 그 두 곳에서 나옵니다. 그래서 클리닉별 리전 콜백을 등록하는 옵션①은 AXS로는 불가능합니다.
  >
  > 대신 옵션②를 기본 메커니즘으로 채택하겠습니다. 단일 콜백으로 이벤트를 받은 수신 GW가 payload의 organizationId로 클리닉과 매핑 리전을 조회한 뒤, 로컬에 저장하기 전에 대상 리전으로 넘겨 거기서 at-rest 저장·처리하고 응답하는 방식입니다. 수신 리전에는 PHI를 영속 저장하지 않고 경유만 시킵니다. 한국 클리닉이라면 AXS(US/EU)에서 발신되어 우리 US/EU 수신부가 서울로 넘기는 흐름이 되는데, 이 교차 리전 전달은 AXS 구조상 사실상 불가피합니다. 다만 그 구간이 ACK 경로에 들어가므로 '즉시 2xx·p95<100ms' 목표는 교차 리전인 경우의 여유를 §7.6.3에 함께 적겠습니다.
  >
  > payload를 at-rest로 저장하는 곳은 대상(매핑) 리전뿐이라는 원칙은 §7.6.3·§2.1.1·FR-RGN-03에 그대로 못박겠습니다. 옵션①은 나중에 조직별 콜백을 지원하는 다른 target이 생기면 최적화로 열어두되, 현재 설계 기준은 옵션②입니다. v1.0은 단일 리전이라 지금은 원칙과 리전-ready 설계만 반영하고, 실제 다중 리전 집행은 gw/1.2에서 진행하겠습니다.
  >
  > 확인 부탁합니다.

- **[김성훈(Scott) · 2026-07-15T11:52 · cid 79434.3 ↳1]**

  > gw/1.2 에서 진행 하는 것으로 알겠습니다. 감사합니다.

- 조치: §7.6.7 대상 리전 판정을 저장 前(수신 시점)으로 · §7.6.3 옵션② 위임·불변식·교차리전 ACK 여유 · §2.1.1 수신≠대상 시 경유·대상 리전만 at-rest · FR-RGN-03 링크 · Appendix B 주권 결정(옵션①=미래 target 노트) — 확정 후 반영
- 반영: 반영완료(로컬·미push) · **Scott 수긍(gw/1.2 진행 확인)**
- 상태: Resolved

## C-17 · docs/specs/SRS.md:1732 · [thread 79435]
- **[김성훈(Scott) · 2026-07-13T10:34 · cid 79435.1]**

  > ### private_key_jwt assertion 재사용 방지
  >
  > - jti 소비 기록 부재
  > Redis 키스페이스 용도 목록은 nonce·rate-limit·idempotency·JWKS·webhook dedup만 열거하고 assertion jti 일회성 소비가 없습니다(SRS.md:1104·1627, design/README.md:23).
  > DBML은 token_denylist(jti, exp)를 gw/1.1로 명시 연기(dbml:94)합니다.
  > 토큰 발급 side effect(SRS.md:1731)에도 jti 저장이 없습니다.
  > → 탈취된 assertion이 exp 이내 반복 사용 가능하다는 지적은 타당합니다.
  >
  > **권고** : iss / sub=client_id / 정확한 aud / 짧은 exp / iat / 고유 jti / 허용 알고리즘(공개키 alg 고정)을 명시하고, jti를 SET NX EX로 일회 소비.
  > RFC 7523 프로파일 고정. 이 지적은 RFC 7523 §3 권고와 정합합니다.

- **[전규현(우리) · 2026-07-14T00:18 · cid 79435.3 ↳1]**

  > 맞습니다. 현재 Redis 용도에 assertion jti 일회 소비가 없어 탈취된 assertion이 exp 이내 재사용될 수 있습니다. RFC 7523 프로파일(iss·sub=client_id·정확한 aud·짧은 exp·iat·고유 jti·허용 alg 고정)을 §7.1.1에 명시하고, jti를 Redis SET NX EX로 일회 소비하도록 추가하겠습니다(키스페이스에 jti 소비 항목 신설). 이는 gw/1.1로 연기된 token_denylist(폐기 목록)와는 별개의 재사용 방지 통제입니다.

- 조치: §7.1.1 RFC 7523 claim 프로파일 + jti 일회 소비(Redis SET NX EX) 추가·redis-keyspace에 jti 항목 신설 — 확정 후 반영
- 반영: 반영완료(로컬·미push)
- 상태: Resolved

## C-18 · docs/specs/SRS.md:1763 · [thread 79436]
- **[김성훈(Scott) · 2026-07-13T10:37 · cid 79436.1]**

  > ### Entra 토큰 검증 조건이 JWKS·subject 확인에 그침
  >
  > issuer, tenant, audience, delegated scope 및 ID token 거부 조건을 정의하지 않습니다.
  > 구현자가 서명만 검사하면 다른 리소스용 토큰을 Admin API가 받아들이는 confused-deputy 문제가 생길 수 있습니다.
  >
  > 단일 tenant, 정확한 iss, aud=GW Admin API, 필수 scope, tid/oid, 사용자 토큰만 허용하고 app-only·ID token은 거부한다고 해야 합니다.
  > Microsoft도 API가 자신을 대상으로 발급된 access token인지 검증하도록 요구합니다
  > - Access token validation (https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  > - Claims validation (https://learn.microsoft.com/en-us/entra/identity-platform/claims-validation).

- **[전규현(우리) · 2026-07-14T00:18 · cid 79436.3 ↳1]**

  > 맞습니다. Entra 토큰 검증이 서명·subject 확인에 그쳐 confused-deputy 위험이 있습니다. §7.1.4에 단일 tenant·정확한 iss·aud=GW Admin API·필수 scope·tid/oid 확인, 그리고 사용자 access token만 허용하고 app-only·ID token은 거부하는 조건을 명문화하겠습니다(MS access token/claims validation 가이드와 정합).

- 조치: §7.1.4 Entra 토큰 검증 조건(iss·tenant·aud·scope·tid/oid·app-only/ID token 거부) 명문화 — 확정 후 반영
- 반영: 반영완료(로컬·미push)
- 상태: Resolved

## C-19 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:1833 · [thread 79437]
- **[김성훈(Scott) · 2026-07-13T10:43 · cid 79437.1]**

  > ### 문제
  > SRS는 디바이스 인증을 "OAuth2 client_credentials + private_key_jwt (RFC 7521/7523)"로 다층 선언
  > (§7.1.1 L1718·L1722·L1727, Appendix B 결정 L2278)하지만, OpenAPI의 실제 계약은 OAuth2가 아닙니다:
  >
  > - `application/json` 요청 (openapi L87) — 표준은 `application/x-www-form-urlencoded` (RFC 6749 §4.4.2)
  > - camelCase `clientId`·`clientAssertion`·`clientAssertionType` (L1835·L1840–1848) — 표준은 snake_case
  > - **`grant_type=client_credentials` 필수 필드 전면 부재** (L1833–1856)
  > - 응답도 비표준 — `accessToken`·`expiresAt`(ms) (L1857–1868), OAuth2 `access_token`·`token_type`·`expires_in` 없음
  >
  > 표준 OAuth2 클라이언트 라이브러리와 호환되지 않으며, 통제 문서(IEC 62304) 관점에서 **선언(claim)과 인터페이스 계약의 불일치**는 추적성 결함입니다.
  >
  > 이미 private_key_jwt(RFC 7523)를 채택했으므로 wire format만 표준화하면 됩니다.

- **[전규현(우리) · 2026-07-13T23:33 · cid 79437.2 ↳1]**

  > 지적 정확합니다. §7.1.1과 OpenAPI가 "OAuth2 client_credentials + RFC 7521/7523"을 표방하면서도 실제 /v1/auth/token 계약은 표준 형태가 아니었습니다(application/json·camelCase·grant_type 없음·응답 accessToken/expiresAt(ms)). 이미 private_key_jwt(RFC 7523)를 인증 방식으로 택했으니 인증 메커니즘은 그대로 두고 wire format만 표준으로 맞추겠습니다.
  >
  > 요청은 application/x-www-form-urlencoded로 바꾸고 grant_type=client_credentials, client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer, client_assertion=<서명 JWT>(및 선택 scope)를 받습니다. client_id는 assertion의 sub에서 도출하므로 별도 필드는 선택으로 둡니다. 응답은 access_token·token_type: Bearer·expires_in(초)로 표준화합니다. 문서 전반은 시간을 Unix ms로 쓰지만, 이 엔드포인트는 표준 상호운용 경계라 OAuth2 관례대로 expires_in(상대 초)을 예외로 두겠습니다.
  >
  > RFC 7523·ADR-13(비대칭 private_key_jwt) 결정 자체는 그대로이고, 변경은 OpenAPI TokenRequest/TokenResponse와 §7.1.1 서술·예시에 한정됩니다. 아직 구현 착수 전이라 소비자(EzServer) 영향도 작습니다.

- 조치: OpenAPI /v1/auth/token content-type→x-www-form-urlencoded · TokenRequest(grant_type·client_assertion_type·client_assertion·선택 scope, client_id 선택) · TokenResponse(access_token·token_type·expires_in 초) · 예시 갱신 · §7.1.1 서술 정합 — 확정 후 반영
- 반영: 반영완료(로컬·미push)
- 상태: Resolved

## C-20 · docs/specs/SRS.md:1727 · [thread 79438]
- **[김성훈(Scott) · 2026-07-13T10:48 · cid 79438.1]**

  > 여기서 선언한 "OAuth2 client_credentials + RFC 7523"과 실제 OpenAPI TokenRequest(L1833)의 계약이 불일치. 정합화 코멘트는 openapi.yaml L1833 참조.

- **[전규현(우리) · 2026-07-13T23:34 · cid 79438.2 ↳1]**

  > 앞의 comment와 같은 사안입니다. openapi.yaml L1833(C-19) 스레드에서 wire format을 OAuth2 표준(form-urlencoded·grant_type·client_assertion·access_token/expires_in)으로 맞추기로 했고, §7.1.1의 "OAuth2 client_credentials + RFC 7523" 선언도 그 표준 계약과 일치하도록 서술·예시를 갱신하겠습니다.

- 조치: §7.1.1 선언 ↔ OpenAPI 계약 정합(C-19 연동)
- 반영: 반영완료(로컬·미push)
- 상태: Resolved

## C-21 · docs/specs/SRS.md:1862 · [thread 79449]
- **[고형용(Larry) · 2026-07-13T13:31 · cid 79449.1]**

  > ## PreSigned Region 책임 경계가 모호합니다.
  > - 1862L: FR-RGN-03 (PHI 리전 밖 미이동). 해석된 리전 외 storage/엔드포인트로의 데이터 이동을 정책(OPA)으로 차단. (§6.1·§6.5 연계)
  > - 1890L: **GW는 presigned URL을 발급하지 않고, 업로드 세션·storage를 소유하지 않는다.** 파일 업로드 presigned **발급 주체는 CleverSpace(경로②)·AXS(경로③)** 이며, GW는 발급 요청을 **중계(B/C bypass, §4.1.4)** 할 뿐이다. 파일 **바이트**는 발급 주체의 storage로 **직접** 업로드한다(GW 미경유, PHI control plane 미경유).
  > - 1321L: > **GW가 하지 않는 일**: presigned **직접 발급(서명)**·업로드 **세션 소유**·region **storage 소유** — **GW 범위 아님**. CleverSpace/AXS presign 스키마를 GW가 통합·변환하지도 않는다. GW는 발급 요청을 **중계**하고 정책(인증·버전·egress)만 적용한다.
  >
  > GW가 "리전 외 Storage/Endpoint 이동 차단"이 명시되어있어서, GW 책임은 Presigned URL 발급 요청 전 단계의 리전 등 라우팅으로 한정하고, CleverSpace는 GW가 해석한 리전에 맞는 presigned url을 발급해야 한다로 변경 제안드립니다.

- **[전규현(우리) · 2026-07-13T23:35 · cid 79449.2 ↳1]**

  > 동의합니다. 지적하신 대로 GW는 storage·presigned·리전 storage를 소유하지 않으니 "리전 밖 이동을 GW가 차단한다"는 표현은 정확하지 않습니다. GW는 파일 바이트를 보지도 않으므로 이미 발급된 URL을 사후에 막을 수단이 없습니다. 그래서 책임 경계를 제안하신 방향으로 정리하겠습니다.
  >
  > GW의 책임은 발급 요청 전 단계로 한정합니다. 클리닉의 매핑 리전을 해석하고, 그 리전을 발급 주체(CleverSpace②/AXS③)에게 전달하며, 인증·버전·egress 정책만 적용합니다. presigned URL은 발급 주체가 GW가 해석한 리전에 맞춰 발급하고, 파일 바이트는 그 storage로 직접 올라갑니다(GW 미경유). 즉 리전 준수는 '바이트 차단'이 아니라 '발급 단계에서 올바른 리전으로 라우팅·발급'으로 보장합니다.
  >
  > 추가로, GW가 중계하는 발급 응답의 리전·호스트가 해석한 리전과 다르면 거부하는 정도의 guardrail은 둘 수 있으나 이는 보조 수단이고, 1차 보장은 발급 주체가 리전을 준수하는 것입니다. GW가 CleverSpace로 해석 리전을 어떻게 전달할지(헤더/파라미터)는 ② CleverSpace 계약에서 확정하겠습니다. FR-RGN-03(§1862)·§7.4 서술을 이 경계에 맞게 정정하겠습니다.

- 조치: FR-RGN-03/§1862 재서술(업로드 경로=발급 단계 라우팅으로 리전 보장·'바이트 차단' 표현 제거) · §7.4 책임 경계 명시(GW=리전 해석·전달·정책 / 발급주체=리전 맞춤 발급) · GW→발급주체 리전 전달 방식=② CleverSpace 계약 · (선택)중계 응답 리전 검증 guardrail=LLD — 확정 후 반영
- 반영: 반영완료(로컬·미push·Larry 합의 대기)
- 상태: Active

## C-22 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:1 · [thread 79505] ★리뷰어 대기
- **[민진우(Thomas) · 2026-07-14T01:52 · cid 79505.1]**

  > 이 spec 문서는 타계열사 (EVN, VFR 등)에서 볼일이 있지 않을까요?
  > 있다면 영문으로도 제공을 하는 건 어떤가요?

- 답변(게시본):

좋은 지적 감사합니다. 다만 한/영 이중언어 SRS를 함께 유지하면 SSOT가 둘이 되어 drift 위험이 커, 본 문서는 한국어를 SSOT로 유지하겠습니다. 타계열사(EVN·VFR 등)가 참조할 경우 요즘 AI 번역 품질이 높으니 한국어 원본을 받아 AI로 번역해 보시는 것을 권장합니다 — 우리가 번역본을 별도 유지하면 원본과 drift가 생기고 유지 부담도 커집니다.

번역 제공 여부·범위는 SRS baseline에서 결정할 사안이 아니라 계열사 조율 차원의 관리 결정이므로, 실제 수요가 생기면 관리자(PM/조직) 판단으로 진행하는 것이 맞다고 봅니다. 본 스레드는 SRS 변경 사항이 없어 여기서 정리(Resolve)하겠습니다.

- 조치: SRS 변경 없음 — 한국어 SSOT 유지·번역=온디맨드(수요처 AI)·제공 여부는 관리(PM/조직) 결정(baseline 밖)
- 반영: 답변·Resolve 권장(SRS 밖·조치 없음)
- 상태: Resolved

## C-23 · docs/specs/SRS.md:1678 · [thread 79527] ★리뷰어 대기
- **[민진우(Thomas) · 2026-07-14T03:17 · cid 79527.1]**

  > 하나의 target에 대한 production 외 staging/test/dev 환경에 대한 domain 은 어떻게 되나요? 그리고, 각 환경과 연계되는 AXS 환경은 어떻게 될까요? 
  > webhook url 도 함께 고려 부탁드립니다.

- 답변(게시본):

  AXS 환경 매핑은 이미 §3.3(환경 표)에 있습니다 — dev→AXS sandbox(unstable, ESIP-14)/미수령 시 mock, test·staging→sandbox, prod→production. 비-prod 도메인·webhook URL은 §4.5.1에 '환경-한정 네임스페이스' 규칙을 보강했습니다: prod 호스트 구조를 env-한정으로 복제(예 {env}.gw.vatech.com·{target}.webhook.{env}…), 각 GW 환경의 target 레지스트리가 대응 AXS 환경을 가리키고 AXS는 그 env의 webhook URL로 구독합니다. 구체 도메인 문자열·zone·인증서·환경 프로비저닝은 ③-I(Appendix B #24·#2), AXS 환경별 자격은 ④/target config로 둡니다 — GW SRS는 논리 규칙까지입니다.

- 조치: §4.5.1에 환경-한정 도메인/webhook URL 규칙 note 추가·§3.3 AXS 환경 매핑 참조·구체=③-I(#24·#2)·④ — 반영
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-24 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:1733 · [thread 79534]
- **[민진우(Thomas) · 2026-07-14T04:24 · cid 79534.1]**

  > webhooks.md 문서에는 키가 Signature로 되어 있습니다.
  > 여기도 Signature로 해야 하지 않을까요? 
  > ```suggestion
  >       name: Signature
  > ```

- **[전규현(우리) · 2026-07-15T01:07 · cid 79534.2 ↳1]**

  > 맞습니다. AXS webhooks.md와 DBML(webhook_provider.sig_scheme) 모두 헤더명이 Signature인데 OpenAPI webhookHmac만 X-Signature로 어긋나 있었습니다. OpenAPI를 Signature로 맞췄습니다. webhook 헤더명은 target별 레지스트리(sig_scheme) 값이라 target마다 다를 수 있고, AXS의 실제 값이 Signature입니다.

- 조치: OpenAPI webhookHmac 헤더 X-Signature→Signature(DBML·AXS와 정합) — 반영
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-25 · docs/specs/SRS.md:2006 · [thread 79556] ★리뷰어 대기
- **[민진우(Thomas) · 2026-07-14T05:23 · cid 79556.1]**

  > mqtt 서버의 주소/포트 정보가 명시가 되어 있지 않아 보입니다.
  > 추가로 mqtt 프로토콜(native or over websocket, TLS 여부)의 버전 등도 명시를 해야 하지 않을까 합니다.

- 답변(게시본):

  MQTT 서버 주소·포트는 브로커 제품(#4·③-I) 확정 사항이라 SRS에 고정 값을 박지 않고, GW가 region resolution·enrollment config로 EzServer에 하달합니다(§7.6.6 'endpoint 획득'에 이미 규정 — 리전별·브로커별로 다르고 인프라 소유이기 때문). 프로토콜은 §7.6.6에 논리 요구를 보강했습니다: TLS 필수·QoS1·persistent·cert 인증은 스펙 불변 요구, MQTT 버전(3.1.1/5.0)·전송(native TCP/over-WebSocket)은 브로커 제품 확정 시 결정합니다. 구체 endpoint·버전·전송은 ③-I 소관입니다.

- 조치: §7.6.6에 프로토콜·전송·보안 논리 요구 note 추가(TLS·QoS1·persistent·cert 불변·버전/전송/endpoint=#4·③-I) — 반영
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-26 · docs/specs/SRS.md:1983 · [thread 79558]
- **[민진우(Thomas) · 2026-07-14T05:31 · cid 79558.1]**

  > 예를 들어 AXS에서 받은 webhook payload는 GW 통해서 변형없이 그대로 EzServer로 전달되나요?
  > 혹시, 다른 format이라면 wrapper format 에 대한 메시지 정의가 필요할 거 같습니다.

- **[전규현(우리) · 2026-07-15T01:08 · cid 79558.2 ↳1]**

  > AXS webhook payload는 GW가 해석·변형하지 않고 opaque verbatim으로 둡니다(§7.6.1). 다만 EzServer 하행(MQTT)에서는 EzServer가 어떤 target·이벤트인지 알아야 하므로 GW가 얇은 envelope(target·eventId·eventType·clinicId·ts + 원 payload)로 감싸 전달합니다 — 원 payload는 그 안에 변형 없이 담깁니다. 즉 wrapper는 있으나 내용 변형은 없습니다. envelope 정의를 §7.6.6에 명시했습니다(필드 상세=LLD).

- 조치: §7.6.6에 하행 envelope 정의 추가(원 payload verbatim·GW 메타만 래핑) — 반영
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-27 · docs/specs/SRS.md:1059 · [thread 79570] ★리뷰어 대기
- **[김기영(Eric) · 2026-07-14T05:46 · cid 79570.1]**

  > 호환 포기로 경로 B(CleverOne이 EzServer를 거치지 않고 CleverSpace와 연동하는 경우)가 EOS 되는 경우의 Workaround가 궁금합니다.

- 답변(게시본):

  경로 B가 EOS되어도 해당 사용자의 기능이 사라지는 게 아니라, 표준 GW 경유 경로(CleverOne→EzServer→GW→target)로 이관하는 것이 workaround입니다 — 직결(CleverOne↔CleverSpace)만 폐지되고 동일 기능은 GW 경로로 보존됩니다(GW 도입 취지). §2.8에 이 workaround를 명시했습니다. EOS 시점·이관 계획·고객 안내는 PM(제품, Appendix B-3)·③-P(CleverOne/CleverSpace 팀) 소관입니다.

- 조치: §2.8 호환 포기 bullet에 'workaround=GW 경유 이관·기능 보존' 명시·시점/계획=PM#3·③-P — 반영
- 반영: 반영완료(로컬·미push)
- 상태: Resolved

## C-28 · docs/specs/SRS.md:552 · [thread 79571] ★리뷰어 대기
- **[민진우(Thomas) · 2026-07-14T05:57 · cid 79571.1]**

  > 이런 경우에 대비해야할 필요가 있을지 검토 부탁드립니다.
  >
  > EzServer와 같은 network에 있는 아무 client 에서 헤더에 Vatech-Target: axs 혹은 cleverspace 등을 넣어서 호출하면 axs, cleverspace의 공격을 GW 를 통해서 하게 되는데요. GW가 공격의 Proxy 역할을 할 수도 있지 않을까 합니다.

- 답변(게시본):

 맞습니다 — EzServer는 클리닉 내부망 전제라 이 시나리오는 '이미 내부망에 들어온 공격자'를 가정합니다. 구조적으로 보면 GW에 인증하는 주체가 EzServer 자신이라, GW ingress 인증만으로는 EzServer 상류(client→EzServer) 트래픽의 출처를 가려낼 수 없습니다. 즉 이 구간은 GW가 관측할 수 없는 지점이라, 인증을 EzServer 계층(③-P-EZ)에서 함께 다뤄야 하는 부분입니다. 내부망을 계속 신뢰할지 zero-trust로 강화할지는 EzServer 위협모델에서 정하면 되고, 어느 쪽이든 GW 통제는 그대로입니다. GW는 이 구간이 뚫려도 blast radius를 제한합니다: 목적지를 등록 target으로 고정(임의 host SSRF 차단)·scope·rate-limit. 그리고 target 자체 인증·입력검증이 최종 방어선입니다. 정리하면 GW·EzServer가 계층을 나눠 막는 구조이며, §4.1.2에 이 신뢰경계를 명시했습니다.

- 조치: §4.1.2 note 신뢰경계 반영 — GW 인증 주체=EzServer(디바이스)라 (client→EzServer) 구간은 GW 관측 밖·EzServer 계층(③-P-EZ)에서 인증(계층 분담); 내부망 무신뢰 전환 여부=③-P-EZ 위협모델(GW 통제 불변); GW는 목적지 고정·scope·rate-limit로 blast radius 제한, target 자체 인증이 최종 방어선
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-29 · docs/specs/SRS.md:28 · [thread 79585]
- **[김기영(Eric) · 2026-07-14T06:48 · cid 79585.1]**

  > 경로 B와 동일(유사)한 경우가 더 있는지 문의드립니다.

- **[전규현(우리) · 2026-07-15T01:12 · cid 79585.2 ↳1]**

  > 경로 B(CleverOne이 EzServer를 거치지 않고 CleverSpace와 직접 연동)가 확인된 우회 패턴입니다. 그 외 흐름은 모두 EzServer→GW를 경유합니다(CleverOne→EzServer→GW). 현재 SRS 범위에서 경로 B 외의 GW-우회 직결은 식별되지 않았으나, 레거시 직결 경로가 더 있는지는 제품/현장팀과 확인해 있으면 동일 방침(GW 경유로 수렴·해당 직결 deprecate)으로 처리하겠습니다.

- 조치: 경로 B 외 우회 없음 확인·추가 발견 시 §2.8 반영(제품/현장팀 확인) — 문서 변경 없음
- 반영: 답변(팀 확인 병행)
- 상태: Resolved

## C-30 · docs/specs/SRS.md:515 · [thread 79586] ★리뷰어 대기
- **[김기영(Eric) · 2026-07-14T06:52 · cid 79586.1]**

  > GW 온보딩 Fail시의 Rollback 또는 Workaround가 있는지 확인이 필요합니다. (정확히는 GW 온보딩이 실패하여도 기존 Usecase는 정상 동작하는지가 궁금합니다.)

- 답변(게시본):

**결론:** GW 온보딩이 실패해도 **기존(레거시) usecase는 정상 동작**합니다. 단, GW 신규 기능 자체는 온보딩 성공이 전제입니다.

먼저 용어를 맞추면, 여기서 **"기존 usecase" = GW 도입 전부터 돌던 레거시(비-GW) 흐름**입니다 — 현행 CleverOne↔CleverSpace 직결(경로 B), 현행 EzServer↔CleverSpace.

**1. 레거시 흐름 — 온보딩과 무관하게 계속 동작**
- GW 온보딩에 의존하지 않음 → 온보딩이 실패해도 레거시 경로로 계속 동작(EOS 전까지 병행·회귀 없음).
- 즉 온보딩 실패가 기존 서비스를 중단시키지 않습니다.

**2. GW 신규 기능(AXS 연동·GW 경유 라우팅) — 온보딩 성공이 전제**
- 온보딩이 실패하면 GW는 못 씁니다(레거시 fallback이 없는 net-new 클리닉·GW 전용 기능 포함).
- 단 enroll은 **비파괴·멱등** → 실패해도 device는 `pending`에 머물 뿐(활성 바인딩·토큰 미생성 · pending은 TTL 자동 만료). 깨진 상태가 남지 않습니다.

**Rollback / Workaround**
- 되돌릴 부분 커밋이 없어 **별도 rollback 불요**, **재시도로 복구**합니다.

**참고:** 경로 B EOS로 GW 경유로 완전 이관한 뒤에는 GW가 런타임 의존이 됩니다 — 그건 온보딩이 아니라 **GW HA(≥2 복제·Multi-AZ·§6.3.1)** 로 보장합니다.

§2.8에 이 구분을 확정 반영했습니다.

- 조치: §2.8 '온보딩 실패 시 기존 흐름 지속성·rollback' bullet 명확화 — '기존 usecase=레거시(비-GW) 흐름' 정의 + (1)레거시=GW 비의존 (2)GW 신규 기능=온보딩 성공 전제·enroll 비파괴 멱등(재시도 복구) 구분; 이관 후 런타임 의존=GW HA(§6.3.1)
- 반영: 반영완료(로컬·미push)
- 상태: Resolved

## C-31 · docs/specs/SRS.md:550 · [thread 79587]
- **[김기영(Eric) · 2026-07-14T06:54 · cid 79587.1]**

  > GW 도입시, 기존 User 관점에서 환경 세팅 및 Usecase 등이 달라지는게 있는지 확인이 필요합니다.

- **[전규현(우리) · 2026-07-15T01:13 · cid 79587.2 ↳1]**

  > 하위호환이 원칙입니다(§2.8). 기존 사용자의 기존 usecase(EzServer→CleverSpace/CleverOne 경유)는 그대로 동작하며, GW는 앞단에 삽입되어 EzServer가 GW를 경유하도록 라우팅합니다. 새로 생기는 것은 GW 온보딩(enroll)과 AXS 연동뿐이고 기존 흐름 계약은 바뀌지 않습니다. 예외는 경로 B(CleverOne↔CleverSpace 직결)로 deprecate→EOS 대상이라 해당 사용자는 GW 경유로 이관해야 합니다(시점=PM·#3). 구체 환경 세팅 변화·전환 절차는 §2.5·§2.8 + ③-P(EzServer/CleverOne) 스펙에서 정리합니다.

- 조치: 기존 §2.8/§2.5로 답변·필요 시 §2.8에 '기존 usecase 불변·GW=앞단 삽입' 한 줄 보강 검토
- 반영: 답변
- 상태: Resolved

## C-32 · (파일 미지정·일반) · [thread 79669] ★리뷰어 대기
- **[김기영(Eric) · 2026-07-14T14:25 · cid 79669.1]**

  > 해당 SRS에 대한 QA팀 전략 Draft 이며 참조 부탁드립니다.
  > Comment 작성한 부분은 제외했으며, James와 추가 논의 예정입니다.
  >
  > [QA Strategy on 260714]
  > . 목적 : GW 도입시 CleverSpace, CleverOne, EzServer (+AXS)와의 (하위) 호환성을 중점적으로 체크하여야 함 (기존 Usecase들이 제대로 동작하는지)
  >
  > . Test 환경 : 아래와 같이 User 환경을 구분하여 진행하여야 함
  >   - 기존 User : 기존 환경 유지한 상태(EzServer, CleverOne, CleverSpace) → GW 온보딩 → AXS 연동
  >   - 신규 User : 클리닉 온보딩 새로 진행 (EzServer 설치 → LMP 라이센스 → GW 온보딩 → AXS 연동)
  >
  > . Test Coverage (SRS 2.5 및 기존 Test 참조)
  >   - SRS 2.5의 6가지 경우
  >   - 기존 Test (James)
  >   - Additional : 경로 B의 경우에는 "호환 포기" 시점이 명확하지 않아 일단 동작 확인이 필요함
  >     * 경로 A (일반적) : CleverOne이 EzServer를 통해 CleverSpace와 연동
  >     * 경로 B (예외) : CleverOne이 EzServer를 거치지 않고 CleverSpace와 연동하는 경우 (혹은 유사한 경우가 더 있는지 확인 필요)
  >
  > [사전 확인 & 협의]
  > . 하위 호환성 검증을 위해 기존 제품들의 Test Version 협의(또는 정책)가 필요함 (직전 버전, 그 이전 버전 등) (SRS 2.5 참조)
  > . GW 도입 전, 현재 검증 방식에 대한 확인이 필요함 (James)
  >   - 멀티 서버 / 멀티 리전 등 고려해서 QA 하는지
  >      * GW 1.0은 단일 리전만 지원
  >   - Test Environment : Dev, Test/Staging, PROD 중 어떤 환경에서 QA 하는지

- 답변(게시본):

공유 감사합니다. QA 전략 방향이 SRS와 잘 맞습니다. 대응되는 SRS 앵커와, 적어주신 열린 질문 중 SRS가 이미 정한 것들을 정리해 드립니다.

**방향 정합성**
- 목적(하위호환·기존 usecase 동작 확인): §2.8(기존 usecase 불변)과 일치합니다. 특히 "온보딩 실패 시에도 기존 usecase가 동작하는지"는 §2.8에 확정 반영했습니다 — 레거시 흐름은 GW에 비의존이라 계속 동작하고, GW 신규 기능만 온보딩 성공이 전제입니다.
- Test 환경 구분(기존 User: 기존 환경 → GW 온보딩 → AXS / 신규 User: EzServer 설치 → LMP → GW 온보딩 → AXS): §2.3.1 온보딩 여정과 정확히 일치합니다.
- 경로 A/B: §2.3.0(경로 A 골격)·§2.8(경로 B)에 정의돼 있습니다.

**열린 질문 중 SRS가 이미 정한 것**
- 경로 B "호환 포기 시점": SRS는 EOS 시점을 PM(제품)이 확정하도록 두었습니다(§2.8). 즉 QA가 "일단 동작 확인"하는 것이 맞고, 폐지 전까지 경로 B는 계속 동작해야 합니다(경로 B의 대체 workaround = GW 경유 이관, §2.8).
- "유사한 경우가 더 있는지": 경로는 A(EzServer 경유)·B(직결) 두 갈래로 정의돼 있고(§2.3.0·§4.1.2), 그 외 라우팅은 미등록=404로 차단됩니다.
- 멀티 서버 / 멀티 리전 QA: GW v1.0은 단일 리전(서울)이라 v1.0 QA는 단일 리전 기준입니다. 멀티 리전은 gw/1.2(§2.7.1·§7.3.5). 단 멀티 서버(리전 내 Multi-AZ 복제·HA)는 v1.0부터 대상입니다(§6.3.1).
- 테스트 환경(Dev / Test-Staging / PROD): §3.1 환경 매트릭스를 참조하세요 — PHI는 PROD만 실데이터, Dev·Test는 더미만(§6.4·§6.5), E2E 게이트=§3.6.2. AXS는 dev/test=sandbox·prod=production, EzServer는 dev=에뮬레이터입니다.
- 기존 제품 Test Version 정책(직전/그 이전 버전): 버전 호환은 §7.7(버전 게이팅)과 호환 매트릭스(클라이언트 × API 최소버전)로 관리하며, 매트릭스 확정본은 ① 운영 호환성 매트릭스에 의존합니다(Appendix B-8). QA의 "테스트 버전 협의"는 이 매트릭스 대상 버전과 맞추면 됩니다.

QA 전략 자체는 QA(James·Eric) 소관이라 SRS 변경은 없고, 위 앵커로 상호 참조만 맞췄습니다. James와의 추가 논의에서 SRS에 반영할 점이 나오면 반영하겠습니다.

- 조치: 정보성(QA 전략 Draft 공유)·QA(James·Eric) 소관 → SRS 변경 없음. 전략 방향↔SRS 앵커 매핑(§2.8·§2.3.1·§2.3.0·§3.1·§7.7·§6.3.1·Appendix B-8), 열린 질문 중 SRS 확정분 회신. James 추가 논의 결과 반영 대기
- 반영: 답변(정보성·QA 소관·SRS 변경 없음)
- 상태: Resolved

## C-33 · docs/specs/SRS.md:323 · [thread 79671] ★리뷰어 대기
- **[임건혁(Jack) · 2026-07-15T00:36 · cid 79671.1]**

  > @<B62326D5-BE2F-6C22-BDD5-19CE8D112C90> @<E616BABA-1CD7-6573-A367-AFAF4633BD3C> 
  > https://docs.aws.amazon.com/ko_kr/AmazonRDS/latest/AuroraUserGuide/aurora-global-database-write-forwarding-apg.html
  > 현재 VPC 구성상 Aurora Global Database 사용시 쓰기 forward를 활성화 하고 리전별 앱들은 해당 리전의 엔드포인트를 사용하면 되는데 사용자 지정 함수나 사용자 정의 프로시저를 지원하지 않는 등 제약이 있습니다. 또한 Aurora Global Database여도 쓰기는 primary region의 DB로 전달되기 때문에 secondary 리전 앱에서 쓰기 작업을 수행할 경우 latency가 상당 부분 증가하므로 감안 부탁드립니다. Global Database로 멀티리전에서 성능상 이득을 볼 수 있는 부분은 Read만 가능합니다.

- 답변(게시본):

좋은 검토 감사합니다. 지적하신 write-forwarding 특성은 GW 데이터 구분과 정합적이라, gw/1.2 멀티 리전 설계에 그대로 반영하겠습니다.

GW는 데이터를 두 부류로 나눕니다(§2.1.1·§6.4):

**① 전역 일관 데이터 — 매핑·레지스트리·정책·JWKS**
- 핫패스는 **읽기**이고 **쓰기는 드뭅니다**(운영자·enroll 시점). → 리전 로컬 read endpoint로 저지연 조회하고, write-forwarding latency는 저빈도 쓰기에만 걸려 수용 가능합니다. GW는 Global DB에서 *쓰기 확장*을 기대하지 않습니다(말씀하신 "이득은 Read"와 일치).

**② PHI·운영 데이터 — webhook payload·audit**
- **리전 로컬**입니다(데이터 주권 FR-RGN-03 — PHI는 대상 리전에만 at-rest). → 애초에 다른 리전으로 forwarding하지 않으므로 데이터 핫패스에 교차 리전 쓰기 latency가 없습니다.

**③ custom function / stored procedure 미지원 제약**
- GW는 **code-first(Prisma/NestJS)** 로 비즈니스 로직이 앱 계층에 있고 stored procedure·DB custom function을 쓰지 않습니다. → 실질 영향이 없습니다.

**정리**
- v1.0은 단일 리전(서울)이고 멀티 리전은 gw/1.2입니다. write-forwarding·primary 배치·리전별 엔드포인트 등 구체 설계는 ③-I 인프라(Appendix B-15) 소관으로 두되, 위 특성을 §2.1.1에 명시적으로 감안 note로 남겼습니다.

- **[임건혁(Jack) · 2026-07-16T04:08 · cid 79671.3 ↳1]**

  > ② PHI·운영 데이터가 리전 로컬이면, 이 DB는 Aurora Global Postgres db가 아닌 별도의 db가 뜨는 건지 여쭙습니다.

- 다음 답변(초안):

네, 맞습니다 — 정확히는 별도 클러스터입니다. Global DB는 클러스터(스토리지) 단위로 복제해 특정 테이블만 뺄 수 없어서, 저장소를 둘로 나눕니다: 전역 일관 클러스터(Aurora Global DB·매핑·정책 등 non-PHI·복제)와 리전 로컬 클러스터(webhook_event(payload=PHI)·audit·fleet·복제 안 함). 불변식은 'PHI는 교차 리전 복제되는 클러스터에 두지 않는다'입니다.

audit·fleet도 리전 로컬이라 리전 로컬 클러스터는 어차피 필요하므로, payload는 그 DB에 관계형으로 그대로 둡니다(현행 webhook_event.payload_encrypted 유지·별도 스토어 불요). 대신 리전 로컬 테이블은 전역 테이블로 하드 FK를 걸 수 없어 soft reference(값 보유 + 앱레벨 무결성)로 정리했습니다(DBML 반영).

이 내용은 §2.1.1 본문·다이어그램에 정리했고, v1.0은 단일 리전이라 단순 구성으로 시작합니다. 실제 인스턴스 구성·사이징·비용은 ③-I와 협의하겠습니다. 감사합니다.
- 조치: §2.1.1(note·캡션·다이어그램)에 '저장소 2분(전역 Global DB 클러스터 / 리전 로컬 클러스터)' + 불변식 명시. payload는 리전 로컬 관계형 유지(audit·fleet가 어차피 리전 로컬이라 별도 스토어 불요·현행 payload_encrypted)·S3/DynamoDB는 후속 옵션. 인스턴스·비용=③-I 협의. webhook_event(target·clinic·region)·fleet_state(device) 하드 FK→soft ref(cross-cluster 불가)·DBML 데이터클래스 범례 추가. Jack 후속(cid 79671.3) 답변 간결화
- 반영: 반영완료(로컬·미push)·Jack 후속 답변 게시 대기
- 상태: Active


## C-34 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:2543 · [thread 79681] ★리뷰어 대기(자동리뷰)
- **[민진우(Thomas) · 2026-07-15T01:17 · cid 79681.1]**

  > From CodeReviewAgent(v0.4.1),
  > `Clinic` 스키마가 SRS가 규정한 Region Resolver 출력 계약과 어긋난다. SRS §7.3.1은 `GET /v1/clinics/me`의 출력을 **"(`Clinic`, OpenAPI)"** 로 명시하며 `regionDisplayName`·`endpoint`·`status`(active/draining/planned)·`cacheTtlSeconds`·`hosts`(apex·webhookHostPattern)·`sovereigntyPolicy`(dataResidencyRegion·phiEgressAllowed·crossBorder·storage…)를 반환한다고 규정하고, §2.3.3의 시퀀스 주석("region(ID·표시명·endpoint·status) + clinicId·mappingVersion·cacheTtl + 주권 정책")도 동일하다. 그러나 이 `Clinic` 스키마(= `GET /v1/clinics/me`·`GET /v1/admin/clinics/{clinicId}` 공통 응답)에는 `clinicId·region·name·countryCode·address·phone·website·mappingVersion·createdAt·updatedAt`만 있고 위 resolver 전용 필드가 하나도 없다. `endpoint`·`displayName`·`status`는 별도 `Region` 스키마에만 존재하고, `cacheTtlSeconds`·`sovereigntyPolicy`·`hosts`는 어느 스키마에도 정의돼 있지 않다. 즉 SRS가 `Clinic`로 서빙하겠다고 한 데이터 주권·캐시 TTL·엔드포인트 정보를 현재 OpenAPI 계약으로는 전달할 수 없다 — resolver 응답 필드를 `Clinic`에 보강하거나 별도 resolver 응답 스키마를 신설하고 §7.3.1의 "(`Clinic`, OpenAPI)" 참조를 그쪽으로 정정해야 한다.

- 답변(게시본):

정확한 지적 감사합니다. SRS↔OpenAPI 계약 드리프트가 맞아, resolver 출력 전용 스키마를 신설해 정정했습니다.

**수정 내용**
- **`ClinicResolution` 스키마 신설** — `Clinic`(레코드)을 `allOf`로 합성한 뒤 resolver 출력 필드를 추가: `regionDisplayName`·`endpoint`·`status`(active/draining/planned)·`cacheTtlSeconds`·`hosts`(`apex`·`webhookHostPattern`)·`sovereigntyPolicy`(`dataResidencyRegion`·`phiEgressAllowed`·`crossBorder`·`storage{hostedBy·kind·regionBound}`).
- **`GET /v1/clinics/me`** 응답을 `Clinic` → `ClinicResolution`으로 교체(device-self = Region Resolver 출력, §7.3.1).
- **`Clinic`** 은 순수 레코드로 정리 — `GET /v1/admin/clinics/{clinicId}`(운영자 레코드 조회)·`ClinicResolution`의 베이스로만.
- **SRS §7.3.1**의 `(Clinic, OpenAPI)` 참조를 `(ClinicResolution, OpenAPI)`로 정정.

**결과**: 요구사항↔인터페이스 추적성이 맞춰졌고(레코드 vs 런타임 해석 분리), redocly lint valid(기존 5 warnings 동일)입니다. `endpoint` 예시는 §4.5.1 규약(`gw-<region>.vatech.com`)으로 맞췄습니다(관련: C-37).

- 조치: ClinicResolution 스키마 신설(allOf Clinic+resolver 필드)·GET /v1/clinics/me 응답 교체·Clinic 설명 정리·SRS §7.3.1 참조 (Clinic)→(ClinicResolution) 정정. redocly valid(5 warn)·fence 52
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-35 · docs/specs/SRS.md:2322 · [thread 79682] ★리뷰어 대기(자동리뷰)
- **[민진우(Thomas) · 2026-07-15T01:17 · cid 79682.1]**

  > From CodeReviewAgent(v0.4.1),
  > Appendix B #42가 enroll B안(LMP 자동승인)의 예약 필드를 **"`EnrollStartRequest.licenseAttestation` optional 필드 예약 완료(OpenAPI·v1.0 미사용)"** 로 기재하나, 실제 OpenAPI는 이 필드를 `EnrollCompleteRequest`에 두었다(`EnrollCompleteRequest.licenseAttestation`, nullable·예약). `EnrollStartRequest` 스키마에는 `bootstrap`·`serial`만 있고 `licenseAttestation`이 없다. §2.3.1의 B안 시퀀스도 `POST /v1/enroll/complete (nonceSignature, clientPublicKey, licenseAttestation)`로 **complete 단계**에서 attestation을 제출하도록 그려져 있어(nonce 서명·공개키와 함께 검증) OpenAPI 배치가 옳고, Appendix B #42의 `EnrollStartRequest.licenseAttestation` 표기가 오기다. baseline 추적표는 개발자가 예약 필드를 찾는 근거이므로 `EnrollCompleteRequest.licenseAttestation`으로 정정해야 한다.

- 답변(게시본):

맞습니다 — 오기 정정했습니다.

- Appendix B #42의 예약 필드 경로를 **`EnrollStartRequest.licenseAttestation` → `EnrollCompleteRequest.licenseAttestation`** 으로 수정.
- 근거: attestation은 nonce 서명·공개키와 함께 **complete 단계**에서 제출·검증됩니다(§2.3.1 B안 시퀀스 `POST /v1/enroll/complete`). OpenAPI 배치(`EnrollCompleteRequest.licenseAttestation`)가 옳고 추적표 문구가 틀렸던 것입니다.

baseline 추적표가 예약 필드를 찾는 근거이므로 실제 스키마 경로에 맞췄습니다.

- 조치: SRS Appendix B #42 예약필드 경로 오기 정정 EnrollStartRequest→EnrollCompleteRequest(+complete 단계 제출 근거 §2.3.1). fence 52
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-36 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:2336 · [thread 79683] ★리뷰어 대기(자동리뷰)
- **[민진우(Thomas) · 2026-07-15T01:18 · cid 79683.1]**

  > From CodeReviewAgent(v0.4.1),
  > `WebhookEnvelope.eventType`를 `required`(line 2328)로 두고 **"이벤트 유형(분배 라우팅 키)"** 로 설명한 것이 GW의 분배 설계와 모순된다. SRS §7.6.1은 "**목적지 라우팅은 `event_type`이 아니라 `org_mapping`** 이 결정한다"고 못 박고, `event_type_path` 미추출 시 event_type은 `null`(관측·필터용 부가정보)이라고 규정한다(§4.1.3도 "목적지 결정 = 매핑이다"). 실제 같은 파일의 `WebhookEvent.eventType`도 `nullable: true`다. 이 envelope가 "확정 계약 아님·논리 예시"임을 감안해도, eventType을 "분배 라우팅 키"로 규정하고 필수 필드로 만든 것은 (a) 실 라우팅 키(`org_mapping`→org id)와 모순되고 (b) event_type이 null일 수 있다는 §7.6.1 규정과도 어긋나 구현자를 event_type 기반 분배로 오도할 수 있다. 설명을 "관측·필터용 이벤트 유형(라우팅 키 아님·null 가능)"으로 고치고 required에서 빼는 것이 맞다.

- 답변(게시본):

맞습니다 — §7.6.1과 모순이라 정정했습니다.

- `WebhookEnvelope.eventType`을 **required에서 제거**하고 **`nullable: true`** 로 변경.
- 설명을 **"관측·필터용 이벤트 유형(라우팅 키 아님·`event_type_path` 미추출 시 null·§7.6.1)"** 으로 수정하고, 목적지 라우팅은 `org_mapping`(externalOrgId→clinicId→region)이 결정함을 명시(§7.6.1·§4.1.3).

이로써 `WebhookEvent.eventType`(이미 nullable)과도 일관되고, 구현자를 event_type 기반 분배로 오도할 여지가 없어졌습니다.

- 조치: WebhookEnvelope.eventType required 제거·nullable:true·설명 '관측/필터용(라우팅 키 아님·null 가능·§7.6.1)'로 수정. redocly valid
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-37 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:2612 · [thread 79684] ★리뷰어 대기(자동리뷰)
- **[민진우(Thomas) · 2026-07-15T01:18 · cid 79684.1]**

  > From CodeReviewAgent(v0.4.1),
  > `Region.endpoint` 예시 `https://apne2.internal.gw.vatech.com`가 SRS §4.5.1이 정의한 리전 내부 호스트 네이밍 규약과 다른 스킴을 쓴다. §4.5.1은 리전별 내부 엔드포인트를 `gw-<region>.vatech.com`(예: `gw-apne2.vatech.com`)으로 예약한다고 명시(line 1365·1384)하는데, OpenAPI는 `{region}.internal.gw.vatech.com` 형태를 예시로 든다. 둘 다 내부·인프라 소유 예시이나 같은 대상(리전 내부 엔드포인트)에 서로 다른 네이밍 규약이 공존해 혼동을 준다 — §4.5.1 규약(`gw-<region>.vatech.com`)에 맞춰 예시를 통일하는 것이 좋다. (경미)

- 답변(게시본):

맞습니다 — 예시를 §4.5.1 규약으로 통일했습니다.

- `Region.endpoint` 예시를 **`https://apne2.internal.gw.vatech.com` → `https://gw-apne2.vatech.com`** 로 수정하고, §4.5.1(`gw-<region>.vatech.com`·GeoDNS 백엔드·인프라 소유·클라이언트 미노출) 참조를 description에 명시.
- 앞서 신설한 `ClinicResolution.endpoint`도 동일 규약(`gw-apne2.vatech.com`)으로 맞춰, 리전 내부 엔드포인트 예시가 문서 전체에서 일관됩니다.

- 조치: Region.endpoint 예시 apne2.internal.gw.vatech.com→gw-apne2.vatech.com(§4.5.1 규약)·description 보강. ClinicResolution.endpoint도 동일 규약. redocly valid
- 반영: 반영완료(로컬·미push)
- 상태: Active

## C-38 · (파일 미지정·일반) · [thread 79685] ★리뷰어 대기(자동리뷰)
- **[민진우(Thomas) · 2026-07-15T01:18 · cid 79685.1]**

  > From CodeReviewAgent(v0.4.1),
  > ## Code Review (Other) — Update 2
  >
  > 이 증분 diff는 (1) 이전 리뷰가 SRS.md에 지적한 6건의 dangling cross-reference를 수정하고, (2) placeholder였던 **OpenAPI(약 2,638줄)** 와 **Redis 키스페이스 카탈로그(신규)** 를 정본 초안으로 채워 넣은 대규모 커밋이다. 이번 리뷰는 이전에 지적되지 않은 신규 결함만 보고했다.
  >
  > **[Previous Review] findings 처리 결과 — 6건 전부 해소.** ① §5.5의 presigned TTL 참조는 `§7.4.2`→`§7.4`로(line 1440 인근), ② §6.1 PHI 비저장 규칙은 `§7.4.2`→`§6.4·§7.4`로, ③ §6.2 Integrity 행은 `§7.4.5/§7.4.4`→`§7.4·§7.6.4·§7.6.2`(실재 절)로, ④ §7.9.1 관리 API 열거에 횡단 `GET /v1/admin/clients`가 추가되어(드릴다운과 병기), ⑤ §4.4 캐시 항목이 `Redis|구현 시 확정`→`Valkey(ElastiCache for Valkey)|확정`으로, ⑥ Appendix B #20이 `§2.1.2 초안 폐기`→`구 §2.1.2 초안(현재 삭제)`으로 각각 정정되어 §7.4 위임 원칙과 정합해졌다. 또한 이전 리뷰가 "미해소"로 남겨 둔 항목 중 **ADR-13 행의 옛 컬럼명 `device.fingerprint`도 `device.client_public_key`로 교정**되었고(현 본문에 `device.fingerprint`·`§7.4·§7.4` 중복 문자열 모두 부재), 이전에 거론된 **OpenAPI Target timeout 예시**도 현재 `Target` 스키마 예시(connect 3000 / response 10000 / total 14000 — connect+response ≤ total, 그리고 §7.5.4의 클라이언트 30s 대비 ≤24s 불변식 충족)로 내부 일관성을 갖췄다.
  >
  > **신규 결함의 공통 뿌리 — SRS ↔ OpenAPI 계약 드리프트.** 이전 리뷰는 SRS 내부 절 번호 정합에 집중했고, 이번에 새로 편입된 OpenAPI가 SRS 본문의 규정과 어긋나는 지점이 신규 결함의 축이다. 가장 중요한 것은 **§7.3.1 Region Resolver 출력 계약**으로, SRS는 `GET /v1/clinics/me`가 `Clinic` 스키마로 리전 표시명·endpoint·상태·cacheTtl·주권 정책·hosts까지 반환한다고 규정하지만 OpenAPI `Clinic` 스키마는 순수 clinic 레코드(이름·주소·연락처 + region + mappingVersion)일 뿐이라 그 데이터를 서빙할 수 없다 — 통제 문서(IEC 62304)의 요구사항↔인터페이스 추적성 관점에서 우선 정정 대상이다. 그 밖에 baseline 추적표(Appendix B #42)의 예약 필드 경로 오기(`EnrollStartRequest`→실제 `EnrollCompleteRequest`), Webhook 수신 envelope의 eventType을 "분배 라우팅 키"로 규정한 설계 모순, 리전 내부 호스트 예시 네이밍 불일치를 라인 코멘트로 지적했다. 모두 문서·계약 정합 수준의 문제이며 아키텍처·데이터 모델 자체를 바꾸는 결함은 발견되지 않았다.
  >
  > **참고(지적 제외).** OpenAPI의 `ProxyError`·`Target*` 응답·`Vatech-*` 헤더가 정의만 되고 미참조인 점은 프록시 경로가 bypass라 OpenAPI에 정의되지 않기 때문이며 파일 주석이 "redocly no-unused-components 경고는 의도된 것"이라고 명시하므로(리뷰 지침상 주석이 해당 이슈를 명시적으로 인지한 경우 제외) 지적에서 뺐다. Redis 키스페이스 카탈로그는 SRS §3.1.2·§6.4·§2.1.1·§7.x의 캐시/휘발 상태 모델과 대체로 정합하며(폐기 denylist·jti 소비·webhook dedup·compat는 AppConfig 위임 등), 재구성 출처(SSOT) 표기도 일관되어 신규 결함으로 볼 만한 항목은 발견하지 못했다.
  >
  > 4 line-specific finding(s) were posted as inline comments.

- 답변(게시본):

총평 감사합니다. 이전 리뷰 6건(dangling cross-reference) 해소와 ADR-13 컬럼명·Target timeout 예시 정합 확인 감사합니다. 이번 라인 지적 4건은 모두 반영했습니다.

- **§7.3.1 Region Resolver 계약 드리프트**: `ClinicResolution` 스키마를 신설(`Clinic` allOf + resolver 필드: regionDisplayName·endpoint·status·cacheTtlSeconds·hosts·sovereigntyPolicy)하고 `GET /v1/clinics/me` 응답을 교체, §7.3.1 참조를 정정했습니다. (요구사항↔인터페이스 추적성 확보)
- **Appendix B-42 예약 필드 경로 오기**: `EnrollStartRequest` → `EnrollCompleteRequest.licenseAttestation`으로 정정(§2.3.1 complete 단계 제출과 일치).
- **WebhookEnvelope.eventType 설계 모순**: required 제거·nullable·"관측/필터용(라우팅 키 아님·null 가능)"으로 수정(§7.6.1 org_mapping 라우팅과 정합).
- **Region.endpoint 네이밍 불일치**: §4.5.1 규약 `gw-<region>.vatech.com`으로 예시 통일.

아키텍처·데이터 모델 자체 결함이 없다는 평가와, ProxyError·Target*·Vatech-* 미참조가 verbatim bypass 의도임을 인지해 지적에서 제외해 주신 점 확인했습니다. 위 수정은 redocly lint valid(기존 5 warnings 동일)이며, 로컬 반영 후 일괄 push 예정입니다.

- 조치: 정보성(Update 2 총평·아키텍처 결함 없음). 라인 지적 4건(C-34~C-37) 반영 확인 회신. SRS/OpenAPI 추가 변경 없음
- 반영: 답변(정보성·수정 없음)
- 상태: Active

## C-39 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:2658 · [thread 79748] ★리뷰어 대기(자동리뷰)
- **[민진우(Thomas) · 2026-07-15T07:04 · cid 79748.1]**

  > From CodeReviewAgent(v0.4.1),
  > `Region.endpoint`(line 2658)는 설명에서 "리전 내부 엔드포인트(§4.5.1 gw-<region>.vatech.com…**클라이언트 미노출**)"이라고 명시하지만, 이 `Region` 스키마는 **deviceAuth로 보호되는 `GET /v1/regions`**(line 218–220, security=`deviceAuth`)의 응답 배열 요소다. 즉 "클라이언트에 노출하지 않는다"고 표기한 리전 내부 호스트를 클라이언트(device)에게 그대로 반환한다. 같은 값이 `ClinicResolution.endpoint`(line 2576)에도 있어 deviceAuth `GET /v1/clinics/me`로도 노출되고, SRS §7.3.1 output(SRS.md line 1864)도 `endpoint`를 resolver 출력에 포함시켜 §4.5.1(SRS.md line 1373 "리전 내부 엔드포인트 … 클라이언트엔 노출하지 않음")와 정면으로 모순된다. 특히 `ClinicResolution.hosts`(line 2583)는 "공개 호스트 참고 — 모두 GeoDNS라 리전 불변"만 담아 리전-특정 내부 호스트를 일부러 배제했는데, `endpoint`가 바로 그 배제 대상(리전 고정 내부 호스트)을 노출한다. 이는 이번 diff에서 이전 리뷰 지적(§7.3.1 Clinic 계약 미비)을 `ClinicResolution` 신설로 해소하는 과정에서 새로 유입된 모순이다 — GeoDNS apex로만 접속시키려는 설계 의도를 device가 우회할 수 있으므로, `endpoint`를 device-facing 응답에서 제거하거나 "클라이언트 미노출" 표기를 정정해 일관화해야 한다.

- 답변(초안):

**결론:** 지적대로 §4.5.1("리전 내부 호스트=클라이언트 미노출")과 모순이라, device-facing 응답에서 리전 내부 `endpoint`를 제거했습니다.

**수정**
- `ClinicResolution`·`Region` 스키마에서 `endpoint`(내부 `gw-<region>.vatech.com`) 필드 제거. device는 공개 apex(`hosts.apex`)/GeoDNS로 라우팅하므로 리전 내부 endpoint가 불필요합니다.
- SRS §7.3.1 resolver 출력·§2.3.3 시퀀스·§7.3 intro에서도 `endpoint` 제거, "라우팅은 공개 apex/GeoDNS, 리전 내부 endpoint 미노출(§4.5.1)"을 명시.

이렇게 하면 디바이스는 공개 GeoDNS apex 하나로만 접속하게 되어 리전을 우회할 수 없고, §4.5.1 불변식과 다시 일치합니다. 수정 후 OpenAPI는 redocly lint를 정상 통과하며, 기존 경고 5건 외에 새로 생긴 것은 없습니다.

- 조치: ClinicResolution·Region에서 endpoint 제거(required 조정)·SRS §7.3.1/§2.3.3/§7.3 endpoint 제거·apex/GeoDNS 라우팅 명시
- 반영: 반영완료(로컬)·게시됨(최신 smoothed본)
- 상태: Active

## C-40 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:2259 · [thread 79749] ★리뷰어 대기(자동리뷰)
- **[민진우(Thomas) · 2026-07-15T07:04 · cid 79749.1]**

  > From CodeReviewAgent(v0.4.1),
  > `postAdminTargets`(line 1282)의 요청 본문 스키마 `Target`은 아웃바운드 OAuth 자격·인바운드 HMAC 시크릿을 **`credentialRef`(line 2259)·`secretRef`(line 2295) = KMS 참조(`kms://alias/…`·"원문 미저장")** 로만 받는다. 그러나 SRS §2.3.4는 "**자격·시크릿은 KMS에 저장하고 DB엔 참조만 둔다**"(SRS.md line 757)라고 하면서 등록 시퀀스(SRS.md line 767–768)에서 운영자가 POST 본문에 **실 자격·secret**을 실어 보내고(`[egress·OAuth 자격]`·`[… sig_scheme·secret …]`) **GW가 이를 KMS에 저장해 `credential_ref`·`secret_ref`를 생성**("GW->>KMS: 자격·시크릿 저장")한다고 규정한다. 즉 계약상 원문 secret을 제출할 입력 필드가 스키마에 전혀 없어, SRS가 기술한 "GW가 raw secret을 수신→KMS 저장" 흐름을 현재 OpenAPI로는 표현할 수 없다. 스키마에 write-only 원문 자격/secret 입력 필드를 추가하거나, 반대로 "운영자가 KMS에 사전 적재 후 참조만 전달"하는 모델로 §2.3.4 시퀀스(GW가 KMS에 저장하는 부분)를 정정해 SRS↔OpenAPI를 정합화해야 한다.

- 답변(초안):

지적하신 대로 계약(`Target` 스키마)에 원문 secret을 받을 입력이 없어서, "운영자가 원문을 제출하면 GW가 KMS에 저장한다"는 §2.3.4 흐름을 스키마가 그대로 표현하도록 고쳤습니다.

`Target` 스키마에 원문을 넣는 write-only 입력 필드를 새로 뒀습니다. OAuth 원문 자격은 `credential`(object), HMAC 원문 시크릿은 `secret`(string)으로 받는데, 둘 다 write-only여서 응답으로는 절대 돌려주지 않고 DB에도 원문을 남기지 않습니다. 운영자가 이 값을 실어 보내면 GW가 즉시 KMS에 저장하고, 그 참조인 `credentialRef`·`secretRef`를 만들어 DB에 둡니다. 그래서 이 두 참조 필드는 read-only로 명확히 표시했습니다.

SRS §2.3.4에도 "원문은 write-only 입력으로 제출하고 GW가 KMS에 저장한 뒤 참조만 read-only로 남긴다"는 문장을 덧붙여, 스키마와 본문이 같은 이야기를 하도록 맞췄습니다.

정리하면 §2.3.4가 규정하던 'GW가 원문 secret을 받아 KMS에 저장하고 참조를 생성'하는 흐름을 이제 OpenAPI가 그대로 표현합니다. redocly lint도 통과합니다.

- 조치: OpenAPI Target에 write-only credential·secret 입력 추가·Ref readOnly 명시·SRS §2.3.4 포인터. redocly valid
- 반영: 반영완료(로컬)·게시됨(최신 서술문본)
- 상태: Active

## C-41 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:1734 · [thread 79750] ★리뷰어 대기(자동리뷰)
- **[민진우(Thomas) · 2026-07-15T07:04 · cid 79750.1]**

  > From CodeReviewAgent(v0.4.1),
  > `webhookHmac` 보안 스킴(line 1731~)은 `name: Signature`(line 1734)로 서명 헤더명을 `Signature`로 선언하지만, 바로 아래 설명(line 1738)은 "(여기 `X-Signature`는 예시)"라며 다른 헤더명을 든다. 헤더명이 target 규약(`sig_scheme`)마다 다르다는 취지는 이해되나, 같은 블록에서 스킴 선언값(`Signature`)과 설명의 예시(`X-Signature`)가 불일치해 구현·툴링(OpenAPI 클라이언트 생성 등)에 혼동을 준다 — 예시 헤더명을 `Signature`로 맞추거나 설명 문구를 정정해 일치시키는 것이 좋다. (경미)

- 답변(초안):

맞습니다 — 스킴 선언(`name: Signature`)과 설명 예시(`X-Signature`)가 어긋나 정정했습니다.

- 설명의 `X-Signature` 예시를 제거하고, **`name: Signature`가 v1.0(AXS) 기본값**임을 명시.
- 헤더명이 target `sig_scheme`에 따라 달라질 수 있다는 취지는 유지하되, 선언값과 설명이 일치하도록 문구를 정리했습니다.

이렇게 스킴 선언과 설명, 그리고 툴링 생성이 서로 어긋나지 않도록 맞췄고, 수정 후에도 OpenAPI는 redocly lint를 정상 통과합니다.

- 조치: webhookHmac 설명의 X-Signature 예시 제거·name: Signature 기본값 일관화. redocly valid
- 반영: 반영완료(로컬)·게시됨(최신 smoothed본)
- 상태: Active

## C-42 · (파일 미지정·일반) · [thread 79751] ★리뷰어 대기(자동리뷰)
- **[민진우(Thomas) · 2026-07-15T07:04 · cid 79751.1]**

  > From CodeReviewAgent(v0.4.1),
  > ## Code Review (Other) — Update 3
  >
  > 이번 증분 diff는 placeholder였던 **SRS.md(약 2,400줄)** 와 **OpenAPI(약 2,684줄)** 를 정본 초안으로 채워 넣으면서, 특히 이전 리뷰가 지적한 SRS↔OpenAPI 계약 드리프트 4건을 정면으로 손본 커밋이다.
  >
  > **[Previous Review] findings 처리 결과 — 4건 전부 해소.** ① §7.3.1 Region Resolver 출력 계약: `Clinic` 스키마에 resolver 필드가 없던 문제를 **`ClinicResolution` 스키마 신설**(`allOf: Clinic` + `regionDisplayName`·`endpoint`·`status`·`cacheTtlSeconds`·`hosts`·`sovereigntyPolicy`)로 해소하고 `GET /v1/clinics/me`가 이를 반환하도록, SRS §7.3.1 output도 "(`ClinicResolution`, OpenAPI)"로 정정. ② Appendix B #42의 예약 필드 경로 오기: 이제 SRS·OpenAPI 모두 **`EnrollCompleteRequest.licenseAttestation`**(complete 단계·nullable 예약)으로 일치. ③ `WebhookEnvelope.eventType`: `nullable: true`로 바뀌고 `required`에서 제외(`[eventId]`만)됐으며 설명도 "관측·필터용(**라우팅 키 아님**·null 가능)"으로 교정 — 목적지 라우팅=`org_mapping` 규정과 정합. ④ `Region.endpoint` 예시: `https://gw-apne2.vatech.com`로 바뀌어 §4.5.1의 `gw-<region>.vatech.com` 네이밍 규약과 통일.
  >
  > **신규 결함 — 여전히 SRS↔OpenAPI 계약 정합이 축.** 이전 리뷰 findings를 고치는 과정과 신규 스키마 확장에서 새 모순이 유입됐다. 가장 중요한 것은 **리전 내부 `endpoint`의 노출 모순**으로, 이전 리뷰 #1을 해결하며 추가한 `ClinicResolution`/`Region` 스키마가 "클라이언트 미노출"로 규정된 리전 내부 호스트를 device-facing(`GET /v1/regions`·`GET /v1/clinics/me`) 응답에 담아 §4.5.1·§7.3.1·§4.5.1 간 자기모순을 만든다 — 통제 문서(IEC 62304) 요구사항↔인터페이스 추적성 관점에서 우선 정정 대상이다. 두 번째는 **`target` 시크릿 제출 경로의 계약 공백**으로, §2.3.4가 "GW가 raw secret을 받아 KMS에 저장"한다고 규정하는데 `Target` 스키마는 KMS *참조* 필드만 있어 원문 제출을 표현할 수 없다. 세 번째는 `webhookHmac` 스킴의 헤더명 선언/예시 불일치(경미)다.
  >
  > 세 건 모두 문서·계약 정합 수준의 문제이며, 아키텍처·데이터 모델 자체를 바꾸는 결함이나 build 차단성 결함은 발견되지 않았다. 나머지 광범위한 신규 API(운영자 RBAC·정책·리전·config·webhook 조회 등)와 provenance 테이블·SRS 본문 규정은 상호 대체로 정합하며, 프록시 미정의 컴포넌트(`ProxyError`·`Target*`)의 미참조는 파일 주석이 "redocly `no-unused-components` 경고는 의도된 것"으로 명시(리뷰 지침상 제외)하므로 지적에서 뺐다.
  >
  > 3 line-specific finding(s) were posted as inline comments.

- 답변(초안):

총평 감사합니다. 이전 리뷰에서 지적된 계약 드리프트 4건(Region Resolver 출력·예약 필드 경로·eventType·endpoint 예시)이 해소된 것으로 확인해 주셔서 감사하고, 이번에 새로 짚어주신 세 가지도 모두 반영했습니다.

먼저 리전 내부 endpoint 노출 문제는, device-facing 응답에서 그 필드를 아예 빼는 방향으로 정리했습니다. `Region`과 `ClinicResolution`에서 리전 내부 endpoint를 제거하고, 디바이스는 공개 apex(GeoDNS)로만 접속하도록 해 §4.5.1의 '내부 호스트 미노출' 원칙과 다시 일치시켰습니다.

target 시크릿 제출 경로는, 운영자가 원문을 write-only로 제출하면 GW가 KMS에 저장하고 참조를 만드는 흐름을 스키마가 표현하도록 고쳤습니다. `Target`에 write-only인 `credential`·`secret` 입력 필드를 두고, 기존 `credentialRef`·`secretRef`는 GW가 생성하는 read-only 참조로 명시해 §2.3.4 규정과 계약이 일치합니다.

마지막으로 webhookHmac 스킴은 설명의 `X-Signature` 예시를 없애고 선언값 `Signature`(v1.0 AXS 기본값)로 통일했습니다.

세 건 모두 문서·계약 정합 수준이라는 평가에 동의하며, 프록시 미정의 컴포넌트의 미참조가 verbatim bypass 의도임을 인지해 지적에서 제외해 주신 점도 확인했습니다. 위 수정은 모두 로컬에 반영해 두었고, 일괄 push 예정입니다.

- 조치: 정보성(Update 3 총평·아키텍처 결함 없음). 라인 지적 3건(endpoint 노출/target secret/webhookHmac) 반영 확인 회신. 추가 문서 변경 없음
- 반영: 반영완료(로컬)·게시됨(Update 3 ack·최신본)
- 상태: Active

## C-43 · docs/specs/SRS.md:2019 · [thread 79842] ★리뷰어 대기(정지홍(Teddy))
- **[정지홍(Teddy) · 2026-07-15T14:50 · cid 79842.1]**

  > EzServer, GW, MQTT 최초 연동 이후 MQTT 서버 장애로 연동 실패 시의 처리 방안에 대해 문의드립니다.

- 답변(초안):

좋은 질문입니다. 최초 연동 이후 MQTT 서버(브로커)가 장애를 겪어도 이벤트가 유실되지 않도록 두 겹으로 설계돼 있습니다.

먼저 아직 EzServer로 발행되기 전 단계라면, 이벤트는 GW 내부 큐(SQS)에 그대로 남아 있습니다. Webhook Dispatcher가 발행을 시도하다 브로커에 닿지 못하면 재시도·백오프를 하고, 정해진 횟수를 넘기면 DLQ로 보내며 알람을 올립니다(§7.6.7·§7.6.3). 즉 브로커가 복구될 때까지 큐에서 대기할 뿐 사라지지 않습니다.

이미 발행된 하행 메시지는 MQTT를 QoS1·persistent로 쓰기 때문에, 연결이 끊겼다가 EzServer가 다시 붙으면 브로커에 버퍼돼 있던 메시지가 재전달됩니다. EzServer는 자기 리전 브로커로 자동 재접속하고(persistent 세션), 재접속·백오프 정책 자체는 EzServer 쪽(③-P-EZ) 몫입니다. 브로커 자체의 이중화·failover는 관리형 브로커(AWS IoT Core / Amazon MQ)가 담당하며 인프라(③-I) 소관입니다.

재전달이 일어나도 eventId 기반 멱등 처리(§7.6.4) 덕분에 중복으로 두 번 반영되는 일은 없습니다. 정리하면 브로커 장애의 최악 상황은 '유실'이 아니라 '전달 지연 + 지속 실패 시 DLQ·알람'이고, 이 내용을 §7.6.6에 '연결·브로커 장애 시 처리(무유실)' 항목으로 명시해 두었습니다.

- 조치: §7.6.6에 '연결·브로커 장애 시 처리(무유실)' note 추가 — 발행 전=SQS 재시도·DLQ, 발행 후=QoS1·persistent 재전달, 재접속=③-P-EZ·브로커 HA=③-I·멱등
- 반영: 반영완료(로컬)·게시됨
- 상태: Resolved

## C-44 · docs/specs/SRS.md:1846 · [thread 79844] ★리뷰어 대기(정지홍(Teddy))
- **[정지홍(Teddy) · 2026-07-15T14:57 · cid 79844.1]**

  > 최초 연동한 clinic_id가 변경 되는 경우에 대해 처리 방안 문의드립니다.

- 답변(초안):

좋은 질문입니다. 먼저 설계 관점을 말씀드리면, clinic_id는 LMP가 발급하는 Clinic-ID를 그대로 쓰는 '정체성 앵커'여서, 값을 제자리에서 바꾸는(rename) 것을 구조적으로 지원하지 않도록 설계돼 있습니다. clinic_id는 clinic 레코드의 PK이면서 device·webhook 이벤트·org 매핑 등이 참조하는 기준이고, 분배 MQTT 토픽(gw/clinic/{clinicId}/webhook)에도 값이 그대로 들어갑니다. 그래서 이 값을 바꾸려면 여러 참조와 라우팅·저장된 스냅샷을 한꺼번에 갈아야 하므로, 애초에 '제자리 변경'을 열어두지 않았습니다(rename API도 없습니다).

그래서 운영 중 실제로 바뀌는 것은 clinic_id가 아니라 그 클리닉의 region(relocation·§7.3.4)이나 이름·주소 같은 정보(PATCH)입니다. 재설치·키 회전(§7.2.7)도 회전 게이트에서 '동일 clinic_id'를 요구하므로 디바이스 키가 바뀌어도 clinic_id는 유지됩니다.

만약 LMP가 같은 클리닉에 아예 다른 Clinic-ID를 새로 발급하는 상황이라면, GW는 이를 'id 변경'이 아니라 새로운 클리닉으로 인식합니다 — 새 clinic 레코드가 생기고 해당 EzServer는 새 Clinic-ID로 재-enroll하며, 기존 clinic_id에 딸린 매핑·정책·device 바인딩은 자동으로 옮겨가지 않습니다. 이 내용을 §7.3에 'clinic_id 불변(정체성 앵커)'로 명시해 두었습니다.

한 가지 여쭙고 싶습니다. clinic_id가 바뀌는 구체적인 시나리오가 실제로 있는지(예: 라이선스 재발급·클리닉 병합 등), 그리고 그런 경우 기존 클리닉의 데이터(매핑·정책·이력) 연속성이 꼭 필요한지 알려주시면 좋겠습니다. 지금 설계는 '새 id = 새 클리닉(자동 이관 없음)'을 전제로 하는데, 연속성이 요구되는 실제 사례가 있다면 별도의 이관 절차(운영/마이그레이션)로 다루는 방안을 함께 논의하겠습니다.

- 조치: §7.3에 'clinic_id 불변(정체성 앵커)' note 추가 + Teddy에게 확인질문(clinic_id 변경 실제 시나리오·데이터 연속성 요구 여부 — 있으면 이관 절차 별도 논의). 구조상 rename 미지원(자연키·다참조)임을 답변에 명시
- 반영: 반영완료(로컬)·게시됨(확인질문 포함·최신본)
- 상태: Active

## C-45 · docs/specs/SRS.md:1898 · [thread 79896] ★리뷰어 대기(자동리뷰 Update 4)
- **[민진우(Thomas) · 2026-07-16T03:43 · cid 79896.1]**

  > From CodeReviewAgent(v0.4.1),
  > §7.3.6 조회 API 설명이 여전히 **`endpoint`를 `GET /v1/regions` 출력에 포함**시킨다("운영 리전 목록(region_id·표시명·**endpoint**·status…)"). 이는 이번 변경에서 이전 리뷰 지적(리전 내부 endpoint 노출)을 해소하며 **`Region`/`ClinicResolution` 스키마에서 `endpoint`를 제거**하고 §2.3.3(line 734 "라우팅은 공개 apex/GeoDNS, **리전 내부 endpoint는 미노출**")·§7.3.1(line 1866 output이 `hosts`=`apex`·`webhookHostPattern`만, endpoint 없음)·§4.5.1(리전별 내부 호스트 `gw-<region>.vatech.com` "**클라이언트엔 노출하지 않음**")로 통일한 것과 정면으로 모순된다. 게다가 `GET /v1/regions`는 **deviceAuth(클라이언트 대면)** 라(OpenAPI `getRegions` security=`deviceAuth`), 이 문구는 바로 그 "클라이언트에 노출하면 안 되는 리전 내부 endpoint"를 다시 device 응답 계약에 되살린다. 실제로 device는 항상 공개 apex/GeoDNS로만 접속하고 리전 선택은 서버측 `clinic.region` 배정으로 처리되므로 device-facing 리전 목록에 endpoint는 개념적으로도 불필요하다. endpoint 제거 수정이 §7.3.6에서 누락되었으므로, 이 문구에서 `endpoint`를 삭제해 OpenAPI `Region` 스키마·§4.5.1·§7.3.1과 정합화해야 한다(통제 문서 요구사항↔인터페이스 추적성).

- 다음 답변(초안): (미작성)
- 조치: 
- 반영: 대기
- 상태: Active

## C-46 · docs/specs/SRS.md:656 · [thread 79897] ★리뷰어 대기(자동리뷰 Update 4)
- **[민진우(Thomas) · 2026-07-16T03:43 · cid 79897.1]**

  > From CodeReviewAgent(v0.4.1),
  > §2.3.1이 온보딩 시 리전 선택 주체를 **"C/S는 현장에서 `GET /v1/regions` 선택지로 다른 region을 지정"**(line 683 시퀀스 노트도 동일)이라고 기술하나, `GET /v1/regions`는 OpenAPI에서 **`deviceAuth`(디바이스 토큰)** 로만 접근하는 device 대면 엔드포인트다(provenance 표 line 491도 "device 공개"로 명시). 반면 C/S는 **운영자=`operatorAuth`(직원 IdP/Entra)** 이고, enroll 시점의 device는 `pending`이라 아직 토큰이 없어 어느 쪽도 이 endpoint를 정상 호출할 수 없다. 운영자용 리전 목록은 이번에 신설된 **`GET /v1/admin/regions`(operatorAuth·getAdminRegions)** 이므로, C/S 동작에 device 대면 endpoint를 귀속시킨 것은 인증 스킴 모델(§4.1.2-5 "인증 스킴을 전 오퍼레이션에 명시")과 어긋난다 — C/S 리전 선택은 `GET /v1/admin/regions`로 정정하는 것이 정합적이다. (경미)

- 다음 답변(초안): (미작성)
- 조치: 
- 반영: 대기
- 상태: Active

## C-47 · docs/specs/SRS.md:2329 · [thread 79898] ★리뷰어 대기(자동리뷰 Update 4)
- **[민진우(Thomas) · 2026-07-16T03:43 · cid 79898.1]**

  > From CodeReviewAgent(v0.4.1),
  > Appendix B #48이 산출물 상태를 "redocly valid·**DBML 11**"로 표기하나, 바로 위 #6(line 2328)은 "**DBML 13 테이블**(dbml2sql OK)"로 적고 있어 테이블 수가 상충한다. 더욱이 #48 자체가 **신규 `client_inventory` 테이블**을 추가했으므로 13 → 14가 되어야 하며 "11"은 어느 기준으로도 맞지 않는다. 상태 주석(비규범)이지만 통제 문서의 내부 정합성 차원에서 수치를 하나로 맞춰야 한다. (경미)

- 다음 답변(초안): (미작성)
- 조치: 
- 반영: 대기
- 상태: Active

## C-48 · (파일 미지정·일반) · [thread 79899] ★리뷰어 대기(자동리뷰 Update 4)
- **[민진우(Thomas) · 2026-07-16T03:43 · cid 79899.1]**

  > From CodeReviewAgent(v0.4.1),
  > ## Code Review (Other) — Update 4
  >
  > 이번 증분 diff는 직전 커밋 메시지("리뷰 후속 반영 — 리전 endpoint 미노출·target secret write-only·webhookHmac·MQTT 장애·clinic_id 불변")대로 **[Previous Review]의 3건을 모두 해소**했다. ① **Region.endpoint 노출** — `Region`·`ClinicResolution` 스키마에서 `endpoint`를 제거하고 `hosts`(공개 apex·webhook 패턴, GeoDNS라 리전 불변)로 대체, §2.3.3·§7.3.1 output도 "리전 내부 endpoint 미노출"로 정정해 §4.5.1과 정합화. ② **target 시크릿 제출 경로 공백** — `Target` 스키마에 write-only `credential`·`secret` 입력 필드를 추가하고(원문→KMS 저장, `credentialRef`·`secretRef`는 read-only 참조만) §2.3.4 등록 시퀀스 서술도 "원문 write-only 제출 → GW가 KMS 저장" 흐름으로 일치. ③ **webhookHmac 헤더명 불일치** — `X-Signature` 예시를 제거하고 "`name: Signature`는 v1.0(AXS) 기본값이며 헤더명은 `sig_scheme`마다 다를 수 있다"로 설명을 교정.
  >
  > **신규 결함은 모두 문서·계약 정합 수준**이며, 아키텍처·데이터 모델을 바꾸거나 build(redocly)를 막는 결함은 없다. 가장 중요한 것은 **endpoint 제거 수정의 누락 지점(§7.3.6 line 1898)** 으로, 나머지 전 문서·OpenAPI가 "리전 내부 endpoint 미노출"로 통일된 가운데 device-facing `GET /v1/regions` 출력 서술에만 `endpoint`가 잔존해 이전 리뷰가 지적한 노출 모순을 부분적으로 되살린다 — 통제 문서 추적성 관점에서 우선 정정 대상이다. 나머지 두 건(C/S의 device 대면 `GET /v1/regions` 귀속·auth 스킴 불일치, DBML 테이블 수 표기 상충)은 경미하다.
  >
  > **추가 관찰(라인 미지정·개선 제안).** OpenAPI 여러 스키마(`Target`·`ConfigEntry`·`Policy`·`OrgMapping`·`Region` 등)의 `createdAt`·`updatedAt`·`version`·`updatedBy`가 설명 텍스트로만 "서버 설정·읽기 전용"이라 명시될 뿐 OpenAPI `readOnly: true` 키워드가 없다(같은 파일의 `credentialRef`·`secretRef`는 올바르게 `readOnly: true` 사용). upsert 계약(예 `postAdminTargets`·`putAdminConfig`·`postAdminPolicies`)이 동일 스키마를 요청 본문으로 재사용하므로, 코드젠 클라이언트에는 이 서버 관리 필드들이 입력 가능 필드로 노출된다(서버가 무시하므로 보안 결함은 아니나 계약 명확성 저하). 추후 code-first 승계 시 `readOnly: true`로 일원화 권장. 또한 프록시 미참조 컴포넌트(`ProxyError`·`Target*` 응답·`Vatech*` 헤더)의 redocly `no-unused-components` 경고는 파일 주석이 "의도된 것"으로 명시하므로 리뷰 지침에 따라 지적에서 제외했다.
  >
  > 3 line-specific finding(s) were posted as inline comments.

- 다음 답변(초안): (미작성)
- 조치: 
- 반영: 대기
- 상태: Active
---

## 인덱스 (위치·상태)
> 상태 = Azure DevOps 스레드 값(Active/Pending/Resolved/Won't fix/Closed). 우리 반영상태는 각 항목 `반영` 필드 참조.
- C-01 · docs/specs/SRS.md:2278 · `Active`
- C-02 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:2247 · `Active`
- C-03 · docs/specs/SRS.md:924 · `Active`
- C-04 · docs/specs/SRS.md:1052 · `Active`
- C-05 · (파일 미지정·일반) · `Active`
- C-06 · docs/specs/SRS.md:1440 · `Active`
- C-07 · docs/specs/SRS.md:1461 · `Active`
- C-08 · docs/specs/SRS.md:1476 · `Active`
- C-09 · docs/specs/SRS.md:2227 · `Active`
- C-10 · docs/specs/SRS.md:1342 · `Active`
- C-11 · docs/specs/SRS.md:2294 · `Active`
- C-12 · (파일 미지정·일반) · `Active`
- C-13 · docs/specs/SRS.md:239 · `Resolved`
- C-14 · docs/specs/SRS.md:1103 · `Resolved`
- C-15 · docs/specs/SRS.md:1112 · `Resolved`
- C-16 · docs/specs/SRS.md:233 · `Resolved`
- C-17 · docs/specs/SRS.md:1732 · `Resolved`
- C-18 · docs/specs/SRS.md:1763 · `Resolved`
- C-19 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:1833 · `Resolved`
- C-20 · docs/specs/SRS.md:1727 · `Resolved`
- C-21 · docs/specs/SRS.md:1862 · `Active`
- C-22 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:1 · `Resolved`
- C-23 · docs/specs/SRS.md:1678 · `Active`
- C-24 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:1733 · `Active`
- C-25 · docs/specs/SRS.md:2006 · `Active`
- C-26 · docs/specs/SRS.md:1983 · `Active`
- C-27 · docs/specs/SRS.md:1059 · `Resolved`
- C-28 · docs/specs/SRS.md:552 · `Active`
- C-29 · docs/specs/SRS.md:28 · `Resolved`
- C-30 · docs/specs/SRS.md:515 · `Resolved`
- C-31 · docs/specs/SRS.md:550 · `Resolved`
- C-32 · (파일 미지정·일반) · `Resolved`
- C-33 · docs/specs/SRS.md:323 · `Active`
- C-34 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:2543 · `Active`
- C-35 · docs/specs/SRS.md:2322 · `Active`
- C-36 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:2336 · `Active`
- C-37 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:2612 · `Active`
- C-38 · (파일 미지정·일반) · `Active`
- C-39 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:2658 · `Active`
- C-40 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:2259 · `Active`
- C-41 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:1734 · `Active`
- C-42 · (파일 미지정·일반) · `Active`
- C-43 · docs/specs/SRS.md:2019 · `Resolved`
- C-44 · docs/specs/SRS.md:1846 · `Active`
- C-45 · docs/specs/SRS.md:1898 · `Active`
- C-46 · docs/specs/SRS.md:656 · `Active`
- C-47 · docs/specs/SRS.md:2329 · `Active`
- C-48 · (파일 미지정·일반) · `Active`