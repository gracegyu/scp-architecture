# ③ GW SRS — 리뷰 코멘트 추적 (_review-log)

> **작업용 문서**(드래프팅 repo). 정본 아님 · **vt-api-gateway로 이관하지 않음**. 반영 편집은 **vt-api-gateway PR 브랜치(`docs/gw-srs-initial`)** 에만. 코멘트는 **원문 그대로** 보존 · 답변/조치는 우리가 채움.

- **PR**: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/11766
- **리뷰어**: 필수 Scott·Thomas / 옵션 Jack·James·Larry·Nick
- **상태 범례**: `대기` · `답변` · `반영예정` · `반영완료` · `해결`(PR Resolved) · `보류`
- **최종 fetch**: 2026-07-13 · thread 12 · 전부 CodeReviewAgent v0.4.1 자동리뷰(사람 리뷰어 코멘트 아직 없음)

---

## C-01 · docs/specs/SRS.md:2278 · [thread 79265] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T04:59
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > Appendix A Decision Log의 ADR-13 행이 공개키 컬럼을 `device.fingerprint`로 표기하고 있으나, 이 컬럼은 문서 전반(§1.4·§7.1.1·§7.2.6·DBML)에서 `device.client_public_key`로 명칭이 정정되었습니다. DBML 주석에도 "구 명칭 'fingerprint'을 정확화"라고 명시되어 있어, 본문 중 유일하게 남은 옛 명칭입니다. 구현자가 존재하지 않는 컬럼(`fingerprint`)을 참조하지 않도록 `device.client_public_key`로 통일해야 합니다.

- 답변:
- 조치:
- 상태: 대기

## C-02 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:2247 · [thread 79266] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T04:59
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > `Target` 스키마의 timeout 예시값이 서로 모순됩니다. `connectTimeoutMs`(D1)=3000 + `responseTimeoutMs`(D2)=10000 = 13000ms 인데 `totalDeadlineMs`(D3)=12000ms 입니다. §7.5.4의 D1~D3 모델상 total_deadline은 프록시 호출 총 예산이므로, 연결에 3s를 쓰면 응답은 9s만에 잘려 D2(10s 응답 대기)가 실제로는 도달할 수 없게 됩니다. 예시값은 최소한 `connect + response ≤ total_deadline` 불변식을 만족하도록 조정하는 편이 좋습니다(예: total_deadline 14000 이상 또는 response_timeout 축소).

- 답변:
- 조치:
- 상태: 대기

## C-03 · docs/specs/SRS.md:924 · [thread 79267] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T04:59
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > "발행은 CI/ops 흐름이라 ... 별도 번호(§2.3.8)를 주지 않고 본 절에 함께 둔다"라고 서술하지만, 실제로 §2.3.8("운영자·Console 인증")이 다른 주제로 존재합니다. 매트릭스 발행 흐름에 부여하지 않겠다고 언급한 번호(§2.3.8)가 이미 별개 절에 사용되고 있어 독자가 혼동할 수 있습니다. 해당 괄호 참조를 삭제하거나 "별도 하위 절을 만들지 않는다" 정도로 표현을 완화하는 것이 좋습니다.

- 답변:
- 조치:
- 상태: 대기

## C-04 · docs/specs/SRS.md:1052 · [thread 79268] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T04:59
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > 참조 표기 오타 — "FR-SES-06 해당 없음, §7.4·§7.4 FR-SES 매핑."에서 `§7.4`가 중복되어 있습니다(`§7.4·§7.4`). 하나로 정리하는 편이 좋습니다.

- 답변:
- 조치:
- 상태: 대기

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
- 조치:
- 상태: 대기

## C-06 · docs/specs/SRS.md:1440 · [thread 79271] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T05:12
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > §5.5의 `presigned URL TTL: 5~15분(§7.4.2)` 항목이 **존재하지 않는 하위 절 §7.4.2**를 참조한다. §7.4는 presigned 발급을 target(CleverSpace/AXS)에 위임하면서 하위 절(7.4.1~7.4.5)이 모두 제거된 flat 절이 되었는데, 옛 번호 참조만 남았다. 더구나 §7.4는 "GW는 presigned를 발급하지 않는다"고 명시하므로, presigned URL TTL(5~15분)을 GW의 성능 요구로 §5.5에 두고 §7.4.2로 연결하는 것은 위임 원칙과도 모순된다. TTL이 발급 주체(② One Pager/④) 소유임을 반영해 항목을 옮기거나 참조를 정정해야 한다(같은 §7.4.2 dangling 참조가 §6.1 line 1461에도 있음).

- 답변:
- 조치:
- 상태: 대기

## C-07 · docs/specs/SRS.md:1461 · [thread 79272] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T05:12
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > §6.1의 안전 규칙 "객체 키·메타데이터에도 PHI를 담지 않는다(§7.4.2)"가 **존재하지 않는 §7.4.2**를 참조한다. §7.4에는 객체 키/메타데이터를 다루는 하위 절이 없다(GW가 storage·서명을 소유하지 않으므로). PHI 비저장 규칙은 안전성 크리티컬 항목이므로, 실재하는 절(§6.4 / §7.3.3 등)로 참조를 정정해야 traceability가 유지된다.

- 답변:
- 조치:
- 상태: 대기

## C-08 · docs/specs/SRS.md:1476 · [thread 79273] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T05:12
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > §6.2 보안 8항목 표의 Integrity 행이 **존재하지 않는 §7.4.5(checksum/ETag)·§7.4.4(idempotency)**를 참조한다. §7.4는 하위 절이 없고, 무결성·멱등은 §7.4 "위임 경계"상 발급 주체(CleverSpace②/AXS④) 책임으로 명시돼 있다. 같은 행의 `§7.6.4`(멱등)·`§7.6.2`(HMAC)는 실재하지만 `§7.4.4`·`§7.4.5`는 dangling이므로 참조를 제거·정정해야 한다.

- 답변:
- 조치:
- 상태: 대기

## C-09 · docs/specs/SRS.md:2227 · [thread 79274] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T05:12
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > §7.9.1 관리 API 열거에 §7.8.5(line 2209)가 정의한 **전 클리닉 횡단 조회 `GET /v1/admin/clients`가 누락**되어 있다. §7.9.1은 클리닉 드릴다운 `GET /v1/admin/clinics/{clinicId}/clients`만 나열하는데, §7.8.5는 두 엔드포인트(횡단 + 드릴다운)를 모두 정의하며 "특정 버전 미만 클리닉 전체" 업그레이드 캠페인의 핵심은 횡단 API다. 관리 API 정본 절(§7.9.1)에도 `GET /v1/admin/clients`를 함께 명시해야 OpenAPI 계약과 정합한다(Appendix B #48도 드릴다운만 언급).

- 답변:
- 조치:
- 상태: 대기

## C-10 · docs/specs/SRS.md:1342 · [thread 79276] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T05:12
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > §4.4 Software Interface 표가 캐시를 `Redis | 구현 시 확정`으로 적었으나, §3.1.2·§1.4·§6.4는 캐시 엔진을 **Valkey(Amazon ElastiCache for Valkey)로 이미 "채택/확정"**했다. 제품명(Redis vs Valkey)과 확정 상태("구현 시 확정" vs 이미 채택)가 다른 절과 어긋난다. §1.4가 정의한 "Redis(호환)=Valkey" 관례를 감안해도, 확정 사항을 미확정처럼 적어 혼동을 준다 — §3.1.2와 동일하게 `ElastiCache for Valkey(확정)`로 통일하는 것이 좋다.

- 답변:
- 조치:
- 상태: 대기

## C-11 · docs/specs/SRS.md:2294 · [thread 79278] · status=active
- 리뷰어: 민진우(Thomas) · 2026-07-13T05:12
- 코멘트(원문):

  > From CodeReviewAgent(v0.4.1),
  > Appendix B #20이 "비AWS 포터블 배포(**§2.1.2** 초안) 폐기"라며 §2.1.2를 참조하지만 본 문서에는 §2.1.2가 없다(§2.1 → §2.1.1 → §2.2). 폐기된 초안 절 번호를 가리키는 dangling 참조라 독자가 근거를 찾을 수 없다. 참조를 삭제하거나 "구 §2.1.2 초안(현재 삭제)" 정도로 표기하는 것이 좋다.

- 답변:
- 조치:
- 상태: 대기

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
- 조치:
- 상태: 대기

---

## 인덱스 (위치·상태)
- C-01 · docs/specs/SRS.md:2278 · `대기`
- C-02 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:2247 · `대기`
- C-03 · docs/specs/SRS.md:924 · `대기`
- C-04 · docs/specs/SRS.md:1052 · `대기`
- C-05 · (파일 미지정 · 일반 코멘트) · `대기`
- C-06 · docs/specs/SRS.md:1440 · `대기`
- C-07 · docs/specs/SRS.md:1461 · `대기`
- C-08 · docs/specs/SRS.md:1476 · `대기`
- C-09 · docs/specs/SRS.md:2227 · `대기`
- C-10 · docs/specs/SRS.md:1342 · `대기`
- C-11 · docs/specs/SRS.md:2294 · `대기`
- C-12 · (파일 미지정 · 일반 코멘트) · `대기`

