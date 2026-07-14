# ③ GW SRS — 리뷰 코멘트 추적 (_review-log)

> **작업용 문서**(드래프팅 repo). 정본 아님 · **vt-api-gateway로 이관하지 않음**. 반영 편집은 **vt-api-gateway PR 브랜치(`docs/gw-srs-initial`)** 에만. 코멘트는 **원문 그대로** 보존 · 답변/조치는 우리가 채움.

- **PR**: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/11766
- **리뷰어**: 필수 Scott·Thomas / 옵션 Jack·James·Larry·Nick
- **상태 범례**: `대기` · `답변` · `반영예정` · `반영완료` · `해결`(PR Resolved) · `보류`
- **최종 fetch**: 2026-07-14 · thread 21 (사람 리뷰어 Scott·Jack·Larry 코멘트 추가됨)

---

## C-01 · docs/specs/SRS.md:2278 · [thread 79265] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T04:59
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > Appendix A Decision Log의 ADR-13 행이 공개키 컬럼을 `device.fingerprint`로 표기하고 있으나, 이 컬럼은 문서 전반(§1.4·§7.1.1·§7.2.6·DBML)에서 `device.client_public_key`로 명칭이 정정되었습니다. DBML 주석에도 "구 명칭 'fingerprint'을 정확화"라고 명시되어 있어, 본문 중 유일하게 남은 옛 명칭입니다. 구현자가 존재하지 않는 컬럼(`fingerprint`)을 참조하지 않도록 `device.client_public_key`로 통일해야 합니다.

- 답변:

맞습니다. Appendix A ADR-13 행의 device.fingerprint는 본문·DBML에서 이미 client_public_key로 정정된 컬럼의 옛 명칭입니다. 존재하지 않는 컬럼을 참조하지 않도록 그 행을 device.client_public_key로 통일하겠습니다.
- 조치: Appendix A ADR-13 행 device.fingerprint → device.client_public_key — 확정 후 반영
- 상태: 답변(확정 대기)

## C-02 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:2247 · [thread 79266] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T04:59
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > `Target` 스키마의 timeout 예시값이 서로 모순됩니다. `connectTimeoutMs`(D1)=3000 + `responseTimeoutMs`(D2)=10000 = 13000ms 인데 `totalDeadlineMs`(D3)=12000ms 입니다. §7.5.4의 D1~D3 모델상 total_deadline은 프록시 호출 총 예산이므로, 연결에 3s를 쓰면 응답은 9s만에 잘려 D2(10s 응답 대기)가 실제로는 도달할 수 없게 됩니다. 예시값은 최소한 `connect + response ≤ total_deadline` 불변식을 만족하도록 조정하는 편이 좋습니다(예: total_deadline 14000 이상 또는 response_timeout 축소).

- 답변:

맞습니다. 예시값이 connect(3000)+response(10000)=13000 > total(12000)이라 §7.5.4의 connect+response ≤ total_deadline 불변식을 어깁니다. 예시를 불변식에 맞게 조정하겠습니다(예: totalDeadlineMs 14000). 이 수치는 예시이고 실제 값은 target SLA·§7.5.4·LLD 소관임을 함께 명시하겠습니다.
- 조치: OpenAPI Target 예시 timeout 조정(connect+response ≤ total, 예 total 14000)+예시임 명시 — 확정 후 반영
- 상태: 답변(확정 대기)

## C-03 · docs/specs/SRS.md:924 · [thread 79267] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T04:59
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > "발행은 CI/ops 흐름이라 ... 별도 번호(§2.3.8)를 주지 않고 본 절에 함께 둔다"라고 서술하지만, 실제로 §2.3.8("운영자·Console 인증")이 다른 주제로 존재합니다. 매트릭스 발행 흐름에 부여하지 않겠다고 언급한 번호(§2.3.8)가 이미 별개 절에 사용되고 있어 독자가 혼동할 수 있습니다. 해당 괄호 참조를 삭제하거나 "별도 하위 절을 만들지 않는다" 정도로 표현을 완화하는 것이 좋습니다.

- 답변:

맞습니다. 매트릭스 발행 흐름에 '§2.3.8을 주지 않는다'고 썼는데 §2.3.8이 다른 주제(운영자·Console 인증)로 실재해 혼동됩니다. 해당 괄호 참조를 삭제하거나 '별도 하위 절을 만들지 않는다'로 완화하겠습니다.
- 조치: §924 §2.3.8 자기참조 삭제/완화 — 확정 후 반영
- 상태: 답변(확정 대기)

## C-04 · docs/specs/SRS.md:1052 · [thread 79268] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T04:59
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > 참조 표기 오타 — "FR-SES-06 해당 없음, §7.4·§7.4 FR-SES 매핑."에서 `§7.4`가 중복되어 있습니다(`§7.4·§7.4`). 하나로 정리하는 편이 좋습니다.

- 답변:

오타 맞습니다. '§7.4·§7.4' 중복을 하나로 정리하겠습니다.
- 조치: §1052 §7.4·§7.4 → §7.4 — 확정 후 반영
- 상태: 답변(확정 대기)

## C-05 · (파일 미지정 · 일반 코멘트) · [thread 79269] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T04:59
- 코멘트(원문):

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

- 답변:

세 가지 모두 반영하겠습니다.

(a) payload 보존·삭제 — 맞습니다. 현재는 삭제 경로 자체가 없어 위반은 아니지만, 향후 purge/retention을 구현할 때 2025-12-23 규정(관리자 승인 필수·감사 필수필드 기록·QA 통보 및 별도 테스트)을 반드시 따르도록 Appendix B #36 결정 근거에 명시해 두겠습니다. payload 열람 break-glass는 이미 webhook.payload.view 감사로 처리되고 있습니다.

(b) OpenAPI servers·Admin 호스트 — /v1/admin/*이 내부 전용 host(admin.gw.vatech.com)로 서빙되는 점이 servers(apex 하나)에서 드러나지 않아 Console 개발자가 혼동할 수 있습니다. admin 태그 설명에 '내부 전용 host(admin.gw.vatech.com) 서빙·공개 edge 도달 불가'를 명시하고, 필요 시 servers에 내부 host 항목을 추가하겠습니다.

(c) §7.1.2 사내 호출자 JWT — 의도적 위임이며 누락이 아닙니다. §7.1.2는 'JWT 발급·무상태 검증 역량'을 기술한 것이고, 실제 발급 엔드포인트는 §7.1.1의 /v1/auth/token(device private_key_jwt)으로 수렴합니다. 사내 호출자 중 EzServer는 그 device 인증을 쓰고, CleverOne은 EzServer를 경유(CleverOne→EzServer→GW)하므로 GW에 직접 인증하지 않으며, 사람 운영자는 §7.1.4(Entra)입니다. 즉 별도 토큰 엔드포인트가 필요한 제3의 인증 경로는 없습니다. 다만 §7.1.2 문구가 '사내 서비스용 JWT 발급'이라 독립 경로처럼 읽히니, '발급=§7.1.1로 수렴, 검증=control plane 무상태(엔드포인트 아님)'로 서술을 명확히 하겠습니다.
- 조치: (a) Appendix B #36 근거에 2025-12-23 규정 명시 · (b) OpenAPI admin 태그(+필요 시 servers)에 내부 host 명시 · (c) §7.1.2 서술 명확화(발급=§7.1.1 수렴·검증=무상태·별도 엔드포인트 없음) — 확정 후 반영
- 상태: 답변(확정 대기)

## C-06 · docs/specs/SRS.md:1440 · [thread 79271] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T05:12
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > §5.5의 `presigned URL TTL: 5~15분(§7.4.2)` 항목이 **존재하지 않는 하위 절 §7.4.2**를 참조한다. §7.4는 presigned 발급을 target(CleverSpace/AXS)에 위임하면서 하위 절(7.4.1~7.4.5)이 모두 제거된 flat 절이 되었는데, 옛 번호 참조만 남았다. 더구나 §7.4는 "GW는 presigned를 발급하지 않는다"고 명시하므로, presigned URL TTL(5~15분)을 GW의 성능 요구로 §5.5에 두고 §7.4.2로 연결하는 것은 위임 원칙과도 모순된다. TTL이 발급 주체(② One Pager/④) 소유임을 반영해 항목을 옮기거나 참조를 정정해야 한다(같은 §7.4.2 dangling 참조가 §6.1 line 1461에도 있음).

- 답변:

맞습니다. §7.4는 발급을 target에 위임하며 하위 절이 없어 §7.4.2는 dangling이고, presigned TTL을 GW 성능요구로 두는 것도 위임 원칙과 어긋납니다. TTL은 발급 주체(② One Pager/AXS④) 소유임을 반영해 항목을 옮기거나 참조를 정정하겠습니다.
- 조치: §5.5 presigned TTL의 §7.4.2 dangling 정정·발급주체 소유로 이동 — 확정 후 반영
- 상태: 답변(확정 대기)

## C-07 · docs/specs/SRS.md:1461 · [thread 79272] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T05:12
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > §6.1의 안전 규칙 "객체 키·메타데이터에도 PHI를 담지 않는다(§7.4.2)"가 **존재하지 않는 §7.4.2**를 참조한다. §7.4에는 객체 키/메타데이터를 다루는 하위 절이 없다(GW가 storage·서명을 소유하지 않으므로). PHI 비저장 규칙은 안전성 크리티컬 항목이므로, 실재하는 절(§6.4 / §7.3.3 등)로 참조를 정정해야 traceability가 유지된다.

- 답변:

맞습니다. §7.4엔 객체키/메타데이터 하위 절이 없어 §7.4.2는 dangling입니다. 안전성 크리티컬 규칙이라 실재 절(§6.4/§7.3.3)로 참조를 정정해 traceability를 유지하겠습니다.
- 조치: §6.1 안전규칙 §7.4.2 → §6.4/§7.3.3 — 확정 후 반영
- 상태: 답변(확정 대기)

## C-08 · docs/specs/SRS.md:1476 · [thread 79273] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T05:12
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > §6.2 보안 8항목 표의 Integrity 행이 **존재하지 않는 §7.4.5(checksum/ETag)·§7.4.4(idempotency)**를 참조한다. §7.4는 하위 절이 없고, 무결성·멱등은 §7.4 "위임 경계"상 발급 주체(CleverSpace②/AXS④) 책임으로 명시돼 있다. 같은 행의 `§7.6.4`(멱등)·`§7.6.2`(HMAC)는 실재하지만 `§7.4.4`·`§7.4.5`는 dangling이므로 참조를 제거·정정해야 한다.

- 답변:

맞습니다. 무결성·멱등은 §7.4 위임 경계상 발급 주체(CleverSpace②/AXS④) 책임이고 §7.4.4·§7.4.5는 dangling입니다. 같은 행의 §7.6.4·§7.6.2는 실재하니 §7.4.4·§7.4.5 참조만 제거·정정하겠습니다.
- 조치: §6.2 Integrity 행 §7.4.4/§7.4.5 dangling 제거 — 확정 후 반영
- 상태: 답변(확정 대기)

## C-09 · docs/specs/SRS.md:2227 · [thread 79274] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T05:12
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > §7.9.1 관리 API 열거에 §7.8.5(line 2209)가 정의한 **전 클리닉 횡단 조회 `GET /v1/admin/clients`가 누락**되어 있다. §7.9.1은 클리닉 드릴다운 `GET /v1/admin/clinics/{clinicId}/clients`만 나열하는데, §7.8.5는 두 엔드포인트(횡단 + 드릴다운)를 모두 정의하며 "특정 버전 미만 클리닉 전체" 업그레이드 캠페인의 핵심은 횡단 API다. 관리 API 정본 절(§7.9.1)에도 `GET /v1/admin/clients`를 함께 명시해야 OpenAPI 계약과 정합한다(Appendix B #48도 드릴다운만 언급).

- 답변:

맞습니다. §7.8.5가 정의한 전 클리닉 횡단 조회 GET /v1/admin/clients가 §7.9.1 관리 API 열거에서 빠졌습니다. 업그레이드 캠페인의 핵심이라 §7.9.1에 추가해 OpenAPI 계약과 정합시키겠습니다(Appendix B #48도 함께 갱신).
- 조치: §7.9.1에 GET /v1/admin/clients 추가·Appendix B #48 갱신 — 확정 후 반영
- 상태: 답변(확정 대기)

## C-10 · docs/specs/SRS.md:1342 · [thread 79276] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T05:12
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > §4.4 Software Interface 표가 캐시를 `Redis | 구현 시 확정`으로 적었으나, §3.1.2·§1.4·§6.4는 캐시 엔진을 **Valkey(Amazon ElastiCache for Valkey)로 이미 "채택/확정"**했다. 제품명(Redis vs Valkey)과 확정 상태("구현 시 확정" vs 이미 채택)가 다른 절과 어긋난다. §1.4가 정의한 "Redis(호환)=Valkey" 관례를 감안해도, 확정 사항을 미확정처럼 적어 혼동을 준다 — §3.1.2와 동일하게 `ElastiCache for Valkey(확정)`로 통일하는 것이 좋다.

- 답변:

맞습니다. §3.1.2·§1.4·§6.4는 캐시 엔진을 Valkey(Amazon ElastiCache for Valkey)로 확정했는데 §4.4 표만 'Redis | 구현 시 확정'이라 어긋납니다. §4.4를 'ElastiCache for Valkey(확정)'로 통일하겠습니다.
- 조치: §4.4 캐시 'Redis/구현 시 확정' → 'ElastiCache for Valkey(확정)' — 확정 후 반영
- 상태: 답변(확정 대기)

## C-11 · docs/specs/SRS.md:2294 · [thread 79278] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T05:12
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > Appendix B #20이 "비AWS 포터블 배포(**§2.1.2** 초안) 폐기"라며 §2.1.2를 참조하지만 본 문서에는 §2.1.2가 없다(§2.1 → §2.1.1 → §2.2). 폐기된 초안 절 번호를 가리키는 dangling 참조라 독자가 근거를 찾을 수 없다. 참조를 삭제하거나 "구 §2.1.2 초안(현재 삭제)" 정도로 표기하는 것이 좋다.

- 답변:

동의합니다. Appendix B #20의 '§2.1.2 초안' 참조는 현재 문서에 없는 절 번호를 가리키는 dangling 참조입니다(§2.1 → §2.1.1 → §2.2). 해당 참조를 삭제하거나 '구 §2.1.2 초안(현재 삭제)' 정도로 표기해 독자가 근거를 찾을 수 있게 정정하겠습니다.
- 조치: Appendix B #20의 §2.1.2 dangling 참조 삭제 또는 '구 §2.1.2 초안(삭제됨)'로 표기 — 확정 후 반영
- 상태: 답변(확정 대기)

## C-12 · (파일 미지정 · 일반 코멘트) · [thread 79279] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T05:12
- 코멘트(원문):

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

- 답변:

§7.4 dangling 등 재지적 사항은 각 라인 스레드(C-05·06·07 등)에서 처리하겠습니다. op 수치는 정본(redocly 기준·Appendix B #6=55)이 맞고, 결정로그 주석의 42·45는 작성 중 시점 스냅샷이라 현재 수치로 정합·정리하겠습니다.
- 조치: Appendix B 결정로그 op 수치(42·45) → 현재 55로 정합/정리 — 확정 후 반영
- 상태: 답변(확정 대기)

## C-13 · docs/specs/SRS.md:239 · [thread 79385] · status=active 🆕
- 리뷰어: 임건혁(Jack) · 2026-07-13T06:34
- 코멘트(원문):

  > @<B62326D5-BE2F-6C22-BDD5-19CE8D112C90> @<8A8E7F25-5884-64CC-9CD9-804A85DF8F64> @<E616BABA-1CD7-6573-A367-AFAF4633BD3C> 현재 EKS 네트워크 구성 상 AWS Regional NAT Gateway를 사용 예정이고 해당 기능은 NAT Gateway의 ip가 고정 되지 않습니다. 외부 클라이언트 연동시 IP whitelist 방식만 지원하는 클라이언트가 있으면 비용 감수하더라도 ip 고정 NAT Gateway 사용이 필요합니다.

- 답변:

맞습니다. SRS도 같은 요구를 이미 담고 있습니다 — 외부(C) target이 IP whitelist를 요구하면 egress는 pod별 임시 IP가 아니라 AZ/리전별 NAT의 고정 EIP 집합이어야 한다는 요구입니다(§2.1.1·§7.5.3·§2.6·FR-INT-03). 다만 지적하신 대로 AWS Regional NAT Gateway의 기본 IP는 비고정이라, 이 요구를 실현하려면 말씀하신 고정 IP(EIP) 기반 NAT가 필요합니다. 비용을 감수하고 그렇게 provisioning하는 데 동의합니다.

대신 비용을 제한하기 위해 고정-IP egress는 전역이 아니라 IP whitelist가 필요한 대상(외부 C·requireStaticEgressIp)에만 선택 적용하고, 나머지(내부 B·IP 고정 불필요 대상)는 표준 NAT를 쓰겠습니다. SRS도 이미 '고정 egress whitelist는 외부(C) 한정'으로 범위를 두고 있습니다(§2.1.1). 실제 NAT 토폴로지(EIP 기반 NAT·대상별 라우팅)와 비용은 ③-I 소관이고, SRS는 '요구 대상엔 고정 egress IP' 요구까지만 기술합니다.

문서엔 이 인프라 함의가 분명해지도록 'Regional NAT Gateway 기본 IP는 비고정 → requireStaticEgressIp 대상은 고정 IP(EIP) egress로 provisioning(비용 수반·③-I)'이라는 한 줄을 §2.1.1(또는 §7.5.3)에 덧붙이겠습니다.
- 조치: §2.1.1/§7.5.3에 'Regional NAT 기본 IP 비고정 → requireStaticEgressIp 대상=고정 EIP egress·비용·③-I' 한 줄 명시 (요구 자체는 기존과 동일) — 확정 후 반영
- 상태: 답변(확정 대기)

## C-14 · docs/specs/SRS.md:1103 · [thread 79387] · status=active 🆕
- 리뷰어: 임건혁(Jack) · 2026-07-13T06:53
- 코멘트(원문):

  > @<B62326D5-BE2F-6C22-BDD5-19CE8D112C90> @<8A8E7F25-5884-64CC-9CD9-804A85DF8F64> Aurora Postgres 15 버전 기준으로 커뮤니티 지원이 2027년 11월, Aurora DB는 2028년 2월 29일입니다. 가능하면 17 버전 사용을 권장하고 현재 사용중이거나 사용 예정인 Extension 등이 17 버전에서의 지원 여부는 리스트업 후 검토해보겠습니다.
- 답변:

좋습니다. 말씀하신 EOL 여유를 고려해 엔진 버전을 PostgreSQL 17로 올리겠습니다. 10월 릴리스 이후 다년 운영을 감안하면 15(커뮤니티 2027-11·Aurora 2028-02 EOL)보다 17이 지원 런웨이가 넉넉합니다. SRS의 '15.x 확정'을 '17.x'로 갱신하겠습니다(§3.1.2·§4.4·Appendix B #18). Aurora PostgreSQL·Global Database가 17을 지원하는 것도 확인해 반영하겠습니다.

Extension 17 호환은 말씀하신 대로 리스트업·검토 결과에 따르겠습니다. Prisma·스키마 자체는 버전 영향이 거의 없고, 혹시 특정 Extension이 17에서 미지원이면 그때 대안(마이너 조정 또는 대체)을 함께 정하겠습니다. 정확한 마이너 버전과 Extension 확정은 인프라/LLD 소관으로 두겠습니다.
- 조치: §3.1.2·§4.4·Appendix B #18 'PostgreSQL 15.x → 17.x' 갱신 · Aurora/Global DB 17 지원 확인 · Extension 17 호환 검토 결과 반영(인프라/Jack) — 확정 후 반영
- 상태: 답변(확정 대기)

## C-15 · docs/specs/SRS.md:1112 · [thread 79389] · status=active 🆕
- 리뷰어: 임건혁(Jack) · 2026-07-13T06:55
- 코멘트(원문):

  > @<B62326D5-BE2F-6C22-BDD5-19CE8D112C90> @<8A8E7F25-5884-64CC-9CD9-804A85DF8F64> @<E616BABA-1CD7-6573-A367-AFAF4633BD3C> 
  > 모니터링 스택은 Loki, Tempo, Mimir (Prometheus full compatible) 사용 및 중앙 Grafana에서 대시보드 + 알람 처리하고 있습니다.

- 답변:

공유 감사합니다. §6.3.2를 실제 중앙 스택에 맞춰 갱신하겠습니다 — GW는 구조화 로그(Pino)·OTel로 생성·노출하고, 중앙 수집·저장은 Loki·Tempo·Mimir(Prometheus 호환) + 중앙 Grafana(대시보드·알람)로 명시하겠습니다. 수집 에이전트·백엔드 세부는 인프라(③-I) 소관으로 둡니다.
- 조치: §6.3.2 백엔드 스택을 Loki·Tempo·Mimir·중앙 Grafana로 갱신 — 확정 후 반영
- 상태: 답변(확정 대기)

## C-16 · docs/specs/SRS.md:233 · [thread 79434] · status=active 🆕
- 리뷰어: 김성훈(Scott) · 2026-07-13T10:30
- 코멘트(원문):

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
- 답변:

문서를 확인해 보니 말씀하신 대로였습니다. AXS webhook 구독(`POST /v1/webhook/subscribe`)의 요청 본문은 events·callbackUrl·hmac 세 필드뿐이고 organizationId가 없습니다. 인증도 파트너 단위 client_credentials 하나여서, 구독과 콜백은 통합 파트너 기준으로 이벤트 타입별 콜백 하나가 붙을 뿐이고 조직 구분은 전달되는 payload의 organizationId로만 옵니다. 게다가 AXS 서버가 US·EU 리전만 있어 발신도 그 두 곳에서 나옵니다. 그래서 클리닉별 리전 콜백을 등록하는 옵션①은 AXS로는 불가능합니다.

대신 옵션②를 기본 메커니즘으로 채택하겠습니다. 단일 콜백으로 이벤트를 받은 수신 GW가 payload의 organizationId로 클리닉과 매핑 리전을 조회한 뒤, 로컬에 저장하기 전에 대상 리전으로 넘겨 거기서 at-rest 저장·처리하고 응답하는 방식입니다. 수신 리전에는 PHI를 영속 저장하지 않고 경유만 시킵니다. 한국 클리닉이라면 AXS(US/EU)에서 발신되어 우리 US/EU 수신부가 서울로 넘기는 흐름이 되는데, 이 교차 리전 전달은 AXS 구조상 사실상 불가피합니다. 다만 그 구간이 ACK 경로에 들어가므로 '즉시 2xx·p95<100ms' 목표는 교차 리전인 경우의 여유를 §7.6.3에 함께 적겠습니다.

payload를 at-rest로 저장하는 곳은 대상(매핑) 리전뿐이라는 원칙은 §7.6.3·§2.1.1·FR-RGN-03에 그대로 못박겠습니다. 옵션①은 나중에 조직별 콜백을 지원하는 다른 target이 생기면 최적화로 열어두되, 현재 설계 기준은 옵션②입니다. v1.0은 단일 리전이라 지금은 원칙과 리전-ready 설계만 반영하고, 실제 다중 리전 집행은 gw/1.2에서 진행하겠습니다.

- 조치: §7.6.7 대상 리전 판정을 저장 前(수신 시점)으로 · §7.6.3 옵션② 위임·불변식·교차리전 ACK 여유 · §2.1.1 수신≠대상 시 경유·대상 리전만 at-rest · FR-RGN-03 링크 · Appendix B 주권 결정(옵션①=미래 target 노트) — 확정 후 반영
- 상태: 답변 게시함(Scott 합의 대기·차주 반영)
## C-17 · docs/specs/SRS.md:1732 · [thread 79435] · status=active 🆕
- 리뷰어: 김성훈(Scott) · 2026-07-13T10:34
- 코멘트(원문):

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

- 답변:

맞습니다. 현재 Redis 용도에 assertion jti 일회 소비가 없어 탈취된 assertion이 exp 이내 재사용될 수 있습니다. RFC 7523 프로파일(iss·sub=client_id·정확한 aud·짧은 exp·iat·고유 jti·허용 alg 고정)을 §7.1.1에 명시하고, jti를 Redis SET NX EX로 일회 소비하도록 추가하겠습니다(키스페이스에 jti 소비 항목 신설). 이는 gw/1.1로 연기된 token_denylist(폐기 목록)와는 별개의 재사용 방지 통제입니다.
- 조치: §7.1.1 RFC 7523 claim 프로파일 + jti 일회 소비(Redis SET NX EX) 추가·redis-keyspace에 jti 항목 신설 — 확정 후 반영
- 상태: 답변(확정 대기)

## C-18 · docs/specs/SRS.md:1763 · [thread 79436] · status=active 🆕
- 리뷰어: 김성훈(Scott) · 2026-07-13T10:37
- 코멘트(원문):

  > ### Entra 토큰 검증 조건이 JWKS·subject 확인에 그침
  >
  > issuer, tenant, audience, delegated scope 및 ID token 거부 조건을 정의하지 않습니다.
  > 구현자가 서명만 검사하면 다른 리소스용 토큰을 Admin API가 받아들이는 confused-deputy 문제가 생길 수 있습니다.
  >
  > 단일 tenant, 정확한 iss, aud=GW Admin API, 필수 scope, tid/oid, 사용자 토큰만 허용하고 app-only·ID token은 거부한다고 해야 합니다.
  > Microsoft도 API가 자신을 대상으로 발급된 access token인지 검증하도록 요구합니다
  > - Access token validation (https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens)
  > - Claims validation (https://learn.microsoft.com/en-us/entra/identity-platform/claims-validation).

- 답변:

맞습니다. Entra 토큰 검증이 서명·subject 확인에 그쳐 confused-deputy 위험이 있습니다. §7.1.4에 단일 tenant·정확한 iss·aud=GW Admin API·필수 scope·tid/oid 확인, 그리고 사용자 access token만 허용하고 app-only·ID token은 거부하는 조건을 명문화하겠습니다(MS access token/claims validation 가이드와 정합).
- 조치: §7.1.4 Entra 토큰 검증 조건(iss·tenant·aud·scope·tid/oid·app-only/ID token 거부) 명문화 — 확정 후 반영
- 상태: 답변(확정 대기)

## C-19 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:1833 · [thread 79437] · status=active 🆕
- 리뷰어: 김성훈(Scott) · 2026-07-13T10:43
- 코멘트(원문):

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

- 답변:

지적 정확합니다. §7.1.1과 OpenAPI가 "OAuth2 client_credentials + RFC 7521/7523"을 표방하면서도 실제 /v1/auth/token 계약은 표준 형태가 아니었습니다(application/json·camelCase·grant_type 없음·응답 accessToken/expiresAt(ms)). 이미 private_key_jwt(RFC 7523)를 인증 방식으로 택했으니 인증 메커니즘은 그대로 두고 wire format만 표준으로 맞추겠습니다.

요청은 application/x-www-form-urlencoded로 바꾸고 grant_type=client_credentials, client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer, client_assertion=<서명 JWT>(및 선택 scope)를 받습니다. client_id는 assertion의 sub에서 도출하므로 별도 필드는 선택으로 둡니다. 응답은 access_token·token_type: Bearer·expires_in(초)로 표준화합니다. 문서 전반은 시간을 Unix ms로 쓰지만, 이 엔드포인트는 표준 상호운용 경계라 OAuth2 관례대로 expires_in(상대 초)을 예외로 두겠습니다.

RFC 7523·ADR-13(비대칭 private_key_jwt) 결정 자체는 그대로이고, 변경은 OpenAPI TokenRequest/TokenResponse와 §7.1.1 서술·예시에 한정됩니다. 아직 구현 착수 전이라 소비자(EzServer) 영향도 작습니다.

- 조치: OpenAPI /v1/auth/token content-type→x-www-form-urlencoded · TokenRequest(grant_type·client_assertion_type·client_assertion·선택 scope, client_id 선택) · TokenResponse(access_token·token_type·expires_in 초) · 예시 갱신 · §7.1.1 서술 정합 — 확정 후 반영

- 상태: 답변(확정 대기)

## C-20 · docs/specs/SRS.md:1727 · [thread 79438] · status=active 🆕
- 리뷰어: 김성훈(Scott) · 2026-07-13T10:48
- 코멘트(원문):

  > 여기서 선언한 "OAuth2 client_credentials + RFC 7523"과 실제 OpenAPI TokenRequest(L1833)의 계약이 불일치. 정합화 코멘트는 openapi.yaml L1833 참조.

- 답변:

앞의 comment와 같은 사안입니다. openapi.yaml L1833(C-19) 스레드에서 wire format을 OAuth2 표준(form-urlencoded·grant_type·client_assertion·access_token/expires_in)으로 맞추기로 했고, §7.1.1의 "OAuth2 client_credentials + RFC 7523" 선언도 그 표준 계약과 일치하도록 서술·예시를 갱신하겠습니다.

- 조치: §7.1.1 선언 ↔ OpenAPI 계약 정합(C-19 연동)
- 상태: 답변(확정 대기)

## C-21 · docs/specs/SRS.md:1862 · [thread 79449] · status=active 🆕
- 리뷰어: 고형용(Larry) · 2026-07-13T13:31
- 코멘트(원문):

  > ## PreSigned Region 책임 경계가 모호합니다.
  > - 1862L: FR-RGN-03 (PHI 리전 밖 미이동). 해석된 리전 외 storage/엔드포인트로의 데이터 이동을 정책(OPA)으로 차단. (§6.1·§6.5 연계)
  > - 1890L: **GW는 presigned URL을 발급하지 않고, 업로드 세션·storage를 소유하지 않는다.** 파일 업로드 presigned **발급 주체는 CleverSpace(경로②)·AXS(경로③)** 이며, GW는 발급 요청을 **중계(B/C bypass, §4.1.4)** 할 뿐이다. 파일 **바이트**는 발급 주체의 storage로 **직접** 업로드한다(GW 미경유, PHI control plane 미경유).
  > - 1321L: > **GW가 하지 않는 일**: presigned **직접 발급(서명)**·업로드 **세션 소유**·region **storage 소유** — **GW 범위 아님**. CleverSpace/AXS presign 스키마를 GW가 통합·변환하지도 않는다. GW는 발급 요청을 **중계**하고 정책(인증·버전·egress)만 적용한다.
  >
  > GW가 "리전 외 Storage/Endpoint 이동 차단"이 명시되어있어서, GW 책임은 Presigned URL 발급 요청 전 단계의 리전 등 라우팅으로 한정하고, CleverSpace는 GW가 해석한 리전에 맞는 presigned url을 발급해야 한다로 변경 제안드립니다.
- 답변:

동의합니다. 지적하신 대로 GW는 storage·presigned·리전 storage를 소유하지 않으니 "리전 밖 이동을 GW가 차단한다"는 표현은 정확하지 않습니다. GW는 파일 바이트를 보지도 않으므로 이미 발급된 URL을 사후에 막을 수단이 없습니다. 그래서 책임 경계를 제안하신 방향으로 정리하겠습니다.

GW의 책임은 발급 요청 전 단계로 한정합니다. 클리닉의 매핑 리전을 해석하고, 그 리전을 발급 주체(CleverSpace②/AXS③)에게 전달하며, 인증·버전·egress 정책만 적용합니다. presigned URL은 발급 주체가 GW가 해석한 리전에 맞춰 발급하고, 파일 바이트는 그 storage로 직접 올라갑니다(GW 미경유). 즉 리전 준수는 '바이트 차단'이 아니라 '발급 단계에서 올바른 리전으로 라우팅·발급'으로 보장합니다.

추가로, GW가 중계하는 발급 응답의 리전·호스트가 해석한 리전과 다르면 거부하는 정도의 guardrail은 둘 수 있으나 이는 보조 수단이고, 1차 보장은 발급 주체가 리전을 준수하는 것입니다. GW가 CleverSpace로 해석 리전을 어떻게 전달할지(헤더/파라미터)는 ② CleverSpace 계약에서 확정하겠습니다. FR-RGN-03(§1862)·§7.4 서술을 이 경계에 맞게 정정하겠습니다.
- 조치: FR-RGN-03/§1862 재서술(업로드 경로=발급 단계 라우팅으로 리전 보장·'바이트 차단' 표현 제거) · §7.4 책임 경계 명시(GW=리전 해석·전달·정책 / 발급주체=리전 맞춤 발급) · GW→발급주체 리전 전달 방식=② CleverSpace 계약 · (선택)중계 응답 리전 검증 guardrail=LLD — 확정 후 반영
- 상태: 답변(확정 대기)

---

## 인덱스 (위치·상태)
- C-01 · docs/specs/SRS.md:2278 · `답변(확정 대기)`
- C-02 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:2247 · `답변(확정 대기)`
- C-03 · docs/specs/SRS.md:924 · `답변(확정 대기)`
- C-04 · docs/specs/SRS.md:1052 · `답변(확정 대기)`
- C-05 · (파일 미지정 · 일반 코멘트) · `답변(확정 대기)`
- C-06 · docs/specs/SRS.md:1440 · `답변(확정 대기)`
- C-07 · docs/specs/SRS.md:1461 · `답변(확정 대기)`
- C-08 · docs/specs/SRS.md:1476 · `답변(확정 대기)`
- C-09 · docs/specs/SRS.md:2227 · `답변(확정 대기)`
- C-10 · docs/specs/SRS.md:1342 · `답변(확정 대기)`
- C-11 · docs/specs/SRS.md:2294 · `답변(확정 대기)`
- C-12 · (파일 미지정 · 일반 코멘트) · `답변(확정 대기)`
- C-13 · docs/specs/SRS.md:239 · `답변(확정 대기)`
- C-14 · docs/specs/SRS.md:1103 · `답변(확정 대기)`
- C-15 · docs/specs/SRS.md:1112 · `답변(확정 대기)`
- C-16 · docs/specs/SRS.md:233 · `답변 게시함(Scott 합의 대기·차주 반영)`
- C-17 · docs/specs/SRS.md:1732 · `답변(확정 대기)`
- C-18 · docs/specs/SRS.md:1763 · `답변(확정 대기)`
- C-19 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:1833 · `답변(확정 대기)`
- C-20 · docs/specs/SRS.md:1727 · `답변(확정 대기)`
- C-21 · docs/specs/SRS.md:1862 · `답변(확정 대기)`
