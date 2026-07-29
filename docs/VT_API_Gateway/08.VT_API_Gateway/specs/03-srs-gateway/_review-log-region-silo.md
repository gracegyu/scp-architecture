# ③ GW SRS — 리뷰 코멘트 추적 (region-silo · PR #12207)

> **작업용 문서**. 각 스레드=시간순 대화(cid·↳parent). `다음 답변(초안)`=미게시 답변(사용자 확인 후 게시). 반영=vt-api-gateway `docs/srs-region-silo` 브랜치.

- **PR**: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/12207
- **주제**: GW 저장소 리전 완전 분리(region silo) — R2 결정 반영 (SRS·DBML·OpenAPI·env-reference)
- **리뷰어**: Jack·Scott·Teddy(필수) · Thomas(옵션) · 우리=전규현
- **커밋**: `d848472`·`da8451a`·`0a5c9fa`(handoff)·`ec4a476`(handoff 정정) + 리뷰 반영분(아래·미커밋)
- **최종 fetch**: 2026-07-29T07:50 · **20 thread** (R1 6 + R2 5 + R3 5 + R4 4 · Nemesis v0.5.0)
- **상태**: R1~R7(Nemesis)+Jack C-29~40 처리(push …·`ab5441a`·`55d724b`) · Jack 삭제분: C-32(미처리·무시)·C-37(withdrawn·apex만 유지) · **신규 Nemesis U7/U8(81528·29·33·34+요약) 미처리**

---

## 처리 절차 (코멘트 올라오면)

1. **fetch** — PR threads/comments를 끌어온다:
   ```bash
   az devops invoke --area git --resource pullRequestThreads \
     --route-parameters project=es-platforms repositoryId=vt-api-gateway pullRequestId=12207 \
     --organization https://dev.azure.com/ewoosoft --api-version 7.1 -o json
   ```
   (스레드별 `comments[].content`·`author`·`publishedDate`·`threadContext.filePath`/`rightFileStart.line` 추출.)
2. 각 스레드를 아래에 **`## C-NN · <file:line> · [thread <id>]`** 로 추가(원문 인용).
3. 우리 판단 + **다음 답변(초안·미게시)** 작성 → **사용자 확인 후** PR에 게시.
4. **조치**(무엇을·어떻게)·**반영**(브랜치 반영 상태)·**상태**(Active/Resolved) 기록.
5. 반영은 `docs/srs-region-silo`에 커밋(§참조·정합성 재검증 후 push).

> 답변 스타일: 서술문(개조식 지양) · 내부 라벨(C-NN·태그) 남발 금지 · 대외 이모지 없음 · `#숫자` 오링크 회피.
> 리뷰가 스펙 자체를 바꾸면 v1.0.5 구현세션 알림·IP도 함께 갱신(머지 후 태그 `spec-v1.0.5`).

---

## 예상 논점 (리뷰 오기 전 대비 — 초안 미확정)

- **Jack(infra)**: 리전별 RDS·리전 호스트 DNS/zone 토폴로지·Region Directory 발행 주체·egress EIP union·KMS 리전 키의 실현성/비용 → 대부분 ③-I 소관 위임으로 답할 여지.
- **Scott(arch)**: 전역 apex/GeoDNS 폐기(기존 확정 대체)·마이그레이션 비용 수용·호주 first-open → R2 결정·§2.3.9·Agenda R2-1 근거.
- **Teddy(EzServer)**: 온보딩 discovery(Region Directory)·리전 호스트 접속·webhook 방향 → §2.3.1·§7.3.6·§2.3.6 계약 확인.
- **CodeReviewAgent(자동)**: 이전처럼 §참조 정합·예시값·자기참조 등 미세 지적 가능 → 이미 전수 검증했으나 재확인.

---

## 코멘트

> Nemesis(자동·Thomas 계정) v0.5.0. 지적 5건(🔧3·💡2) + 요약 sweep 2건 — **전부 타당**(부분수정 누락 자기모순·삭제 시 구획 주석 collateral). 모두 반영·push(`c102870`). 아래 답변은 **전규현 명의로 게시 완료 · 6 thread 모두 Resolved(fixed)**.

## C-01 · docs/specs/SRS.md:648 · [thread 81416] · 🔧
- **[민진우(Thomas)/Nemesis · 2026-07-29T06:35 · cid 81416.1]**
  > §2.3.1 "활성화 게이트 = C/S 승인" 불릿이 `(설치 확인 + region 확정/override)`로 남아, 인접 갱신 불릿·§7.3.1(리전=배포 상수·override 없음)과 정면 모순. `region 확정/override` → "올바른 리전 GW 확인"으로 고쳐야 함.
- **[전규현(우리) · 2026-07-29T06:57 · cid 81416.2 ↳1]** (게시완료)
  > 맞습니다. 부분 수정에서 이 불릿이 누락됐습니다. '설치 확인 + region 확정/override'를 '설치 확인 + 올바른 리전 GW 확인'으로 정정했습니다(§7.3.1 리전=배포 상수와 정합).
- 조치: §2.3.1 활성화 게이트 불릿 문구 정정 · 반영: push `c102870` · 상태: **Resolved(fixed)**

## C-02 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:138 · [thread 81417] · 🔧
- **[Nemesis · cid 81417.1]**
  > `/v1/enroll/complete` 138줄 "승인(설치 확인 + region 확정/다른 리전 override)"이 다음 139줄 "리전은 배포 상수라 override 없음"과 자기모순. 138줄의 override 표현 제거 필요.
- **[전규현(우리) · 2026-07-29T06:58 · cid 81417.2 ↳1]** (게시완료)
  > 맞습니다. 같은 description 블록 안에서 138줄과 139줄이 모순됐습니다. 138줄의 '+ region 확정/다른 리전 override'를 '올바른 리전 GW 확인'으로 정정했습니다.
- 조치: enroll/complete description 정정 · 반영: push `c102870` · 상태: **Resolved(fixed)**

## C-03 · docs/specs/design/dbml/vt-api-gateway.dbml:103 · [thread 81418] · 🔧
- **[Nemesis · cid 81418.1]**
  > clinic 블록 주석이 `region: clinic과 1:1 → 컬럼 인라인 … relocation 시 mapping_version+1`로 남음. 이번에 `clinic.region` 컬럼은 삭제됐고 같은 블록은 "region 컬럼 없음(배포 상수)"이라 SSOT 자기모순. 삭제/정정 필요.
- **[전규현(우리) · 2026-07-29T06:58 · cid 81418.2 ↳1]** (게시완료)
  > 맞습니다. clinic.region 컬럼을 삭제하고도 '1:1 인라인 컬럼' 주석이 남아 설계 SSOT 자기모순이었습니다. '리전=배포 상수(컬럼 없음) · mapping_version은 리전 내 캐시 무효화·CAS 마커'로 정정했습니다.
- 조치: DBML clinic 블록 region 주석 정정 · 반영: push `c102870` · 상태: **Resolved(fixed)**

## C-04 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:1471 · [thread 81419] · 💡
- **[Nemesis · cid 81419.1]**
  > `/v1/admin/regions` 블록 삭제 시 그 뒤 `PUBLIC PLANE` 구분선·`Webhook 수신` 섹션 주석, 그리고 `/v1/admin/clinics/{clinicId}/devices` 앞 `디바이스 긴급 정지(kill)·감사` 구획 주석까지 collateral 삭제됨. 존치 엔드포인트의 구획/설명 주석이라 복원 권장.
- **[전규현(우리) · 2026-07-29T06:59 · cid 81419.2 ↳1]** (게시완료)
  > 맞습니다. region 카탈로그 블록을 지우면서 인접 구획 주석(PUBLIC PLANE 구분선·Webhook 수신 섹션 주석·디바이스 kill/audit 구획)까지 함께 삭제됐습니다. 존치 엔드포인트의 구획/설명 주석을 원문대로 복원했습니다(webhook 호스트는 리전 라벨 반영).
- 조치: OpenAPI 구획 주석 3건 복원 · 반영: push `c102870` · 상태: **Resolved(fixed)**

## C-05 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:37 · [thread 81420] · 💡
- **[Nemesis · cid 81420.1]**
  > `clinics` 태그 설명이 "클리닉 관리·리전 등록/변경 …"으로 남음. `regions` 태그·리전 변경 엔드포인트는 삭제됐고 리전은 배포 상수라 "리전 등록/변경"은 없는 기능. 정정 권장.
- **[전규현(우리) · 2026-07-29T06:59 · cid 81420.2 ↳1]** (게시완료)
  > 맞습니다. clinics 태그 설명의 '리전 등록/변경'은 이제 없는 기능을 가리킵니다. '클리닉 관리 (생성은 enroll이 흡수·리전은 배포 상수 §2.3.1·§7.3.1)'로 정정했습니다.
- 조치: clinics 태그 설명 정정 · 반영: push `c102870` · 상태: **Resolved(fixed)**

## C-06 · [thread 81421] · 요약(Other) + sweep 2건
- **[Nemesis · cid 81421.1]**
  > 전반 일관·철저 평가(폐기 개념 거의 빠짐없이 제거·PHI 삭제 규정 정확 반영). 주결함=자기모순 3건(C-01~03). 추가 sweep: DBML `mapping_version` 주석(114)·SRS §6.4.1 "drift 감지"가 §7.3.2(리전 간 drift 소멸·리전 내 캐시/CAS 한정)와 어긋남 · DBML `country_code` 주석(110) "region 추천/표시 참고"는 리전=상수라 의미 흐려짐.
- **[전규현(우리) · 2026-07-29T06:59 · cid 81421.2 ↳1]** (게시완료)
  > 리뷰 감사합니다. 지적하신 자기모순 3건과 권장 2건을 모두 반영했고, 요약의 sweep도 함께 처리했습니다 — mapping_version 주석(DBML·§6.4.1)의 'drift 감지'를 §7.3.2에 맞춰 '리전 내 캐시 무효화·CAS'로, country_code 주석을 '배포 리전과 별개·온보딩 리전 선택 참고'로 정정했습니다.
- 조치: sweep(DBML 114·376·110 · SRS 1669) 정정 · 반영: push `c102870` · 상태: **Resolved(fixed)**

---

## Round 2 — Nemesis Update 1/2 (handoff 파일 대상 · 2026-07-29T06:49~06:58)

> handoff 2개(0a5c9fa·ec4a476) 대상 재리뷰. 인라인 3건(💡·전부 권장) + 요약 2건. **전반 매우 견고** 평가. **전건 정정·push(`3b15792`)·답변 게시(전규현)·6→11 전 thread Resolved(fixed)**.
> 참고: 요약이 "직전 must-fix 3건 미해소"라 하는데, 이는 Nemesis가 **handoff-only diff**를 봐서다 — 그 3건은 별도 커밋 `c102870`에서 이미 정정·push됨.

## C-07 · docs/handoff/region-silo-infra.md:16 · [thread 81433] · 💡
- **[Nemesis · cid 81433.1]**
  > KMS 항목의 `토큰 서명` 앵커 §7.2가 오앵커(§7.2=디바이스 레지스트리·서명/KMS 없음). 토큰 서명=§7.1(.1)·외부 target 자격 KMS=§7.5.2. 하단 참조 목록에도 §7.2 누락(불일치). §7.2 → §7.1/§7.5.2 정정 권장.
- **[전규현(우리) · 2026-07-29T07:15 · cid 81433.2 ↳1]** (게시완료)
  > 맞습니다. §7.2는 디바이스 레지스트리라 토큰 서명 앵커로 오기였습니다. §7.6.3(payload)·§7.5.2(target 자격)·§7.1.1(토큰 서명)로 정정하고 하단 참조 목록에도 반영했습니다.
- 조치: infra KMS 앵커·참조 정정(§7.2→§7.1.1·§7.5.2) · 반영: push `3b15792` · 상태: **Resolved(fixed)**

## C-08 · docs/handoff/*.md:5 (ezserver·infra) · [thread 81434] · 💡 · ⏳확인필요
- **[Nemesis · cid 81434.1]**
  > 두 handoff 헤더 `배경: 7/30 주간회의 R2 결정`이 현재 날짜(2026-07-29)·기병합 커밋(d848472)보다 뒤라 시점 어긋남. 실제 결정 일자로 정정 권장.
- **[전규현(우리) · 2026-07-29T07:15 · cid 81434.2 ↳1]** (게시완료)
  > 맞습니다. R2는 2026-07-29 화상회의에서 결정된 사안이라 '7/30 주간회의 결정'이 시점상 어긋났습니다. 배경 일자를 'R2 결정(2026-07-29 화상회의)'로 정정했습니다(7/30 주간회의는 공유/안건).
- 조치: **R2 실제 결정 일자 확인 후** 두 handoff(및 PR 본문·기타)의 "7/30 주간회의 R2 결정" 배경 일자 정정 · 반영: push `3b15792`(7/29 정정) · 상태: **Resolved(fixed)**

## C-09 · [thread 81435] · 요약(Update 1)
- **[Nemesis · cid 81435.1]**
  > handoff 2개 순수 추가·위상/범위 적절·인용 섹션 전부 실재·서술 일치. 지적=권장 2건(KMS §7.2·배경 일자). 직전 must-fix 3건은 이 diff(handoff만)로 미해소.
- **[전규현(우리) · 2026-07-29T07:15 · cid 81435.2 ↳1]** (게시완료)
  > 리뷰 감사합니다. 권장 2건 중 §7.2 오앵커는 정정했고 배경 일자도 R2 결정일(2026-07-29 화상회의)로 정정했습니다. 직전 must-fix 3건은 이 handoff diff가 아니라 별도 커밋 c102870에서 이미 정정·push했습니다(이 증분이 handoff만 건드려 미반영으로 보인 것).
- 조치: 요약 응대 · 반영: — · 상태: **Resolved(fixed)**

## C-10 · docs/handoff/region-silo-ezserver.md:25 · [thread 81447] · 💡
- **[Nemesis · cid 81447.1]**
  > 본문 항목6이 인라인으로 §2.3.9·§7.3.4를 올바르게 인용하나, 하단 `## 참조` 목록에서 **§7.3.4 누락**. 인라인/참조 목록 불일치. 참조에 §7.3.4 추가(§2.3.9 옆) 권장.
- **[전규현(우리) · 2026-07-29T07:15 · cid 81447.2 ↳1]** (게시완료)
  > 맞습니다. 인라인 §7.3.4가 하단 참조 목록에서 빠졌습니다. 참조 목록에 §7.3.4를 §2.3.9 옆에 추가했습니다.
- 조치: ezserver 참조 목록 §7.3.4 추가 · 반영: push `3b15792` · 상태: **Resolved(fixed)**

## C-11 · [thread 81448] · 요약(Update 2)
- **[Nemesis · cid 81448.1]**
  > handoff 인용 섹션(§2.3.6·§7.6.6·§4.5.1·§7.3.6 등) 직접 대조 결과 SRS와 정확히 부합. 신규 지적=§7.3.4 참조 누락 1건. 직전 지적(§7.2·배경 일자)·이전 must-fix 3건은 이 diff와 무관하게 미해소.
- **[전규현(우리) · 2026-07-29T07:15 · cid 81448.2 ↳1]** (게시완료)
  > 감사합니다. §7.3.4 참조 누락은 정정했습니다. §7.2 오앵커·배경 일자(→2026-07-29 화상회의)도 정정 완료이고, 그 이전 must-fix 3건은 c102870에서 이미 해소됐습니다.
- 조치: 요약 응대 · 반영: — · 상태: **Resolved(fixed)**


---

## Round 3 — Nemesis Update 3 (SRS/OpenAPI 본문 재리뷰 · 2026-07-29T07:10~07:11)

> region-silo 본문 반영 재리뷰. 인라인 4 + 요약 1. **직전 must-fix 3건 해소 확인**(c102870 반영됨). 신규 = clinic→region 해석 잔재(🔧) + OpenAPI 예시 + **companion SSOT 3파일 드리프트**. **전건 정정·push(`eab47a3`)·답변 게시(전규현)·5 thread 모두 Resolved(fixed)**.

## C-12 · docs/specs/SRS.md:2093 (§7.6.7) · [thread 81451] · 🔧
- **[Nemesis · cid 81451.1]**
  > Dispatcher '동작'의 `대상 해석(org_mapping→clinic→region, §6.4·§7.3)`이 clinic→region 해석 단계를 포함. 바로 아래 2094("교차리전 없음")·§7.3.1("런타임 리전 해석 없음")과 모순. `→region` 제거 필요.
- **[전규현 · cid 81451.2 ↳1]** (게시완료)
  > 맞습니다. clinic→region 해석은 리전 완전 분리에서 존재하지 않는 단계입니다. Dispatcher 동작의 대상 해석을 org_mapping→clinic→그 클리닉 MQTT 토픽으로 정리해 리전 해석 단계를 제거했습니다.
- 조치: §7.6.7 동작 bullet `→region` 제거 · 반영: push `eab47a3` · 상태: **Resolved(fixed)**

## C-13 · docs/specs/SRS.md:2076 (§7.6.6) · [thread 81452] · 🔧
- **[Nemesis · cid 81452.1]**
  > "리전은 토픽에 넣지 않는다" bullet의 `교차리전은 대상 리전 브로커로 발행`이 silo(§7.6.7 교차리전 없음·§2.1.1 독립)와 모순. "자기 리전 브로커로 발행"으로 정정.
- **[전규현 · cid 81452.2 ↳1]** (게시완료)
  > 맞습니다. 리전 완전 분리에서는 교차리전 발행이 발생하지 않습니다. '교차리전은 대상 리전 브로커로 발행'을 '자기 리전 브로커로 발행'으로 정정했습니다.
- 조치: §7.6.6 bullet 교차리전 발행 문구 정정 · 반영: push `eab47a3` · 상태: **Resolved(fixed)**

## C-14 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:1709 · [thread 81453] · 🔧 (플레이스홀더 혼재)
- **[Nemesis · cid 81453.1]**
  > AccessToken claims example가 `region: apne2`(구체) + `aud: axs.gw.<region>.<도메인>`(플레이스홀더) 혼재라 broken. ClinicResolution.hosts는 구체값이므로 aud도 `axs.gw.apne2.vatech.com`으로 통일 권장.
- **[전규현 · cid 81453.2 ↳1]** (게시완료)
  > 맞습니다. 한 예시 안에서 region은 구체값인데 aud는 플레이스홀더라 서로 어긋나 있었습니다. ClinicResolution.hosts가 구체 리전 라벨을 쓰는 것과 맞춰 aud도 axs.gw.apne2.vatech.com으로 구체값 통일했습니다.
- 조치: aud example 구체값 통일(권장 채택) · 반영: push `eab47a3` · 상태: **Resolved(fixed)**

## C-15 · docs/specs/design/openapi/vt-api-gateway.openapi.yaml:2123 · [thread 81454] · 💡
- **[Nemesis · cid 81454.1]**
  > Target.inboundHost example가 플레이스홀더. ClinicResolution.hosts는 구체 리전 라벨이므로 `axs.webhook.gw.apne2.vatech.com`처럼 구체값 통일 권장.
- **[전규현 · cid 81454.2 ↳1]** (게시완료)
  > Target.inboundHost example도 같은 기준으로 구체 리전 라벨 axs.webhook.gw.apne2.vatech.com으로 통일했습니다. 예시 전반에서 리전 라벨 호스트가 구체값으로 일관되도록 맞췄습니다.
- 조치: inboundHost example 구체값 통일(권장 채택 — 전 예시 일관성 우선) · 반영: push `eab47a3` · 상태: **Resolved(fixed)**

## C-16 · [thread 81455] · 요약(Update 3) + no-location 2건 + companion SSOT
- **[Nemesis · cid 81455.1]**
  > 방향 정합·YAML 인용 보정 양호. **직전 must-fix 3건 해소 확인**. 신규 (본문) clinic→region 잔재: §2.3.6.1 다이어그램(894 `DISP→ 대상 해석 org_mapping→clinic→region`)·§4.1.3(1330 `ClinicID→region→토픽`). (구조적·최대 우려) **companion SSOT 미동기화** — `redis-keyspace.md`(gw:cache:regions←삭제된 region_catalog)·`api-surface-matrix.md`(region_catalog 행·/v1/admin/regions·GET /v1/regions)·`UnitTCL.md`(TC-DATA-01 Aurora Global·TC-ENR-01 GeoDNS·REG.1/REG.5·TC-REG-19/21/25/27/28/30 region_catalog·clinic.region). baseline 전 정정 또는 Appendix B 추적 권장.
- **[전규현 · cid 81455.2 ↳1]** (게시완료)
  > 리뷰와 must-fix 3건 해소 확인 감사합니다. 지적하신 본문 잔재는 모두 정정했습니다 — §7.6.7·§7.6.6·§2.3.6.1 다이어그램·§4.1.3에서 clinic→region 해석 단계를 제거했습니다. companion 문서 세 개의 드리프트도 동기화했습니다: redis-keyspace는 리전 목록 캐시를 Region Directory 기준으로 정리, api-surface-matrix는 삭제된 테이블·엔드포인트(region_catalog·/v1/admin/regions·GET /v1/regions)를 반영, UnitTCL은 폐기 개념 테스트(Aurora Global·GeoDNS·REG 삭제분)를 갱신했습니다. baseline 전에 모두 정정 완료했습니다.
- 조치: 본문 4곳(894·1330 포함) + companion 3파일 동기화 · 반영: push `eab47a3` · 상태: **Resolved(fixed)**


---

## Round 4 — Nemesis Update 4 + Thomas 질문 (2026-07-29T07:33~07:50)

> **중요**: Update 4는 `eab47a3` **push 직전 스냅샷**을 봄 → 이미 해소한 must-fix 4건(894/2093/2076/1330)·OpenAPI 2건(1709/2123)·536/533·companion 3파일을 "미해소"로 재기재하나 **전부 stale**(eab47a3에 반영됨). 진짜 신규 = 규범 절 resolver 잔재(🔧)·handoff 앵커(💡)·§2.3.6.2 다이어그램 자기모순(신규 유입). + Thomas 본인 질문 1건. **전건 정정·push(`c6fe5f1`)·답변 게시(전규현)·R4 4 thread 모두 Resolved(fixed)**.

## C-17 · docs/specs/SRS.md:1284 (§4.1.2 규칙 3) · [thread 81467] · 🔧
- **[Nemesis · cid 1]**
  > 규칙 3 마지막 문장이 `리전 목적지=서브도메인 라벨 + Vatech-Clinic-Id(어느 리전, §7.3 resolver) 직교 조합(멀티 Region)`으로 런타임 resolver·클리닉→리전 직교 조합을 서술. 같은 diff에서 §2.3.0 ③는 "리전=배포 상수(런타임 해석 없음)"로 정정됐는데 규범 절인 규칙 3은 누락. §3.1.2 라인 1156 PDP 나열의 `resolver`도 동류.
- **[전규현 · 게시완료]** 맞습니다. §4.1.2 규칙 3은 다이어그램이 아니라 라우팅 규범 절인데 '§7.3 resolver 직교 조합'이 남아 §7.3.1(런타임 리전 해석 없음·리전=배포 상수)과 모순이었습니다. '구체 host는 서브도메인 라벨로 정하고 리전 부분은 배포 상수 GW_REGION으로 고정(런타임 resolver 없음)'으로 정정했습니다. 함께 지적하신 §3.1.2 PDP 조회 대상 나열의 resolver도 제거했습니다.
- 조치(예정): §4.1.2 규칙3 + §3.1.2 resolver 잔재 제거 · 반영: push `c6fe5f1` · 상태: **Resolved(fixed)**

## C-18 · docs/handoff/region-silo-infra.md:16 · [thread 81468] · 💡
- **[Nemesis · cid 1]**
  > KMS 항목의 `§7.5.2 target 자격` 앵커 오기. §7.5.2는 AXS connector 절이고, target 자격·시크릿 KMS 저장 정본은 §7.1.3(§2.3.4가 §7.1.3·OpenAPI Target 참조). §7.5.2 → §7.1.3 권장. 하단 참조(라인 24)도 동일.
- **[전규현 · 게시완료]** 맞습니다. target 자격·시크릿의 KMS 저장 정본은 §7.1.3(외부 토큰·secret 저장·§2.3.4가 이 절 참조)이고 §7.5.2는 AXS connector 절이라 앵커가 어긋났습니다. KMS 항목과 하단 참조 목록의 'target 자격' 앵커를 §7.5.2 → §7.1.3으로 정정했습니다(§7.6.3 payload·§7.1.1 토큰 서명은 그대로).
- 조치(예정): handoff infra 16·24 앵커 §7.5.2→§7.1.3 · 반영: push `c6fe5f1` · 상태: **Resolved(fixed)**

## C-19 · docs/specs/SRS.md:917 (§2.3.6.2 다이어그램) · [thread 81469 요약 내] · 💡(신규 유입)
- **[Nemesis · cid 1]**
  > §2.3.6.2 fallback 다이어그램 스텝 `WHX->>WHX: 전역 매핑으로 home 리전 판정`이, 이번 diff가 새로 추가한 바로 위 TBD 노트(904 — "전역 매핑 없음·clinic→region 전역 인덱스는 silo 원칙과 충돌·지금 해결 안 함")와 정면 상충. 구현자가 다이어그램만 보면 노트가 금지한 전역 인덱스를 만들게 됨. `home 리전 판정(discovery 방식 TBD)`로 완화 권장.
- **[전규현 · 게시완료]** 맞습니다. 제가 이번에 추가한 TBD 노트가 "전역 매핑 없음"을 못박았는데 바로 아래 다이어그램 스텝은 "전역 매핑으로 home 리전 판정"이라 새 자기모순이 생겼습니다. 스텝을 'home 리전 판정(discovery 방식 TBD·§2.3.6.2 노트)'로 완화해 노트와 정합화했습니다.
- 조치(예정): §2.3.6.2 다이어그램 917 스텝 완화 · 반영: push `c6fe5f1` · 상태: **Resolved(fixed)**

## C-20 · docs/specs/SRS.md:1428 (§4.5.1 비-prod 도메인) · [thread 81463] · 질문(Thomas 본인)
- **[민진우(Thomas) · cid 1]**
  > dev환경 domain은 region 구분이 없는데요. 1개의 region 있어서 그런가요?
- **[전규현 · 게시완료]** 네, dev는 서울 단일 리전이라 도메인에 리전 라벨을 넣지 않습니다. 리전 라벨 호스트(gw.<region>.<도메인>)는 리전이 여럿일 때 서브도메인으로 리전을 구분하려는 규약이라, 리전이 하나면 구분 대상이 없어 라벨이 불필요합니다. prod은 나중에 리전을 추가해도 비파괴적이도록 v1.0(서울 단일)부터 라벨을 유지하지만, dev는 단일 리전 전제라 gw.dev.ezcld.net처럼 라벨 없이 둡니다. 확인해보니 스펙 §4.5.1 비-prod 노트가 'dev도 리전 라벨 포함'으로 잘못 적혀 있어 '단일 리전 환경은 리전 라벨 생략'으로 정정했습니다.
- 조치(예정): §4.5.1 비-prod 노트 "리전 라벨 포함"→"단일 리전 환경은 라벨 생략" 정정 · 반영: push `c6fe5f1` · 상태: **Resolved(fixed)**

## C-21 · [thread 81469] · 요약(Update 4)
- **[Nemesis · cid 1]** (요약 — handoff/방향 정합 양호. 직전 must-fix 4건·OpenAPI 2건·companion "미해소"로 재기재하나 eab47a3 미반영 스냅샷 기준. 신규 = §4.1.2 규칙3·§2.3.6.2 다이어그램.)
- **[전규현 · 게시완료]** 리뷰 감사합니다. 요약에서 미해소로 재기재된 항목(본문 clinic→region 4곳·OpenAPI 2건·536/533·companion 3파일)은 이 리뷰 직전 커밋에서 이미 정정·push했습니다 — 리뷰가 그 push 이전 스냅샷을 본 것으로 보입니다. 신규 지적은 모두 반영했습니다: §4.1.2 규칙 3·§3.1.2의 resolver 잔재 제거, §2.3.6.2 fallback 다이어그램의 '전역 매핑' 스텝을 바로 위 TBD 노트와 정합하게 완화했습니다.
- 조치(예정): 요약 응대(stale 안내 + 신규 반영) · 반영: push `c6fe5f1` · 상태: **Resolved(fixed)**


---

## Round 5 — Nemesis Update 5 (2026-07-29T17:2x · 자동 모니터링 중 수신)

> 대규모 sweep의 **부분수정 누락 4건**(inline)+요약. 요약 "참고"의 §4.1.2 규칙3·§2.3.6.2 917·handoff §7.5.2는 **c6fe5f1에서 이미 해소**(Update 5가 c6fe5f1 직전 스냅샷)—stale. 신규 4건은 전부 타당. **전건 정정·push(`34496d3`)·답변 게시(전규현)·5 thread 모두 Resolved(fixed)**.

## C-22 · docs/specs/UnitTCL.md:33 (TC-DATA-02/03) · [thread 81476] · 🔧
- **[Nemesis · cid 1]**
  > TC-DATA-01은 단일-DB로 재작성됐으나 TC-DATA-02("전역 복제 제외")·TC-DATA-03("cross-cluster FK 불가")은 폐기된 2-클러스터/전역 복제 프레이밍이 남아 §2.1.1과 자기모순. 단일-DB 모델로 재작성 필요.
- **[전규현 · 게시완료]** 맞습니다. TC-DATA-01을 단일-DB로 바꾸면서 02·03이 옛 2-클러스터·전역 복제 프레이밍으로 남았습니다. TC-DATA-02는 '리전 DB에만 저장(리전 간 복제 없음·전역 DB 없음)'으로, TC-DATA-03은 단일 datasource라 이제 테이블 간 하드 FK가 걸리므로 'cross-cluster 불가·soft-ref'가 아니라 '하드 FK 적용·참조 대상 실재 필수·위반 시 거부'로 재작성했습니다. 이어지는 TC-DATA-04의 'soft-ref 대상 부재'도 같은 맥락에서 'nullable FK 미해석 시 null 저장'으로 함께 정정했습니다(clinic_id는 nullable FK).
- 조치(예정): TC-DATA-02/03/04 단일-DB·하드 FK로 재작성 · 반영: push `34496d3` · 상태: **Resolved(fixed)**

## C-23 · docs/specs/SRS.md:1778 (§7.1.1) · [thread 81477] · 🔧
- **[Nemesis · cid 1]**
  > §7.1.1 본문은 서명키를 "리전별·리전 로컬"로 정정했으나 바로 아래 하위 bullet의 "전역보관"이 남아 정면 모순. `전역보관`→`리전별 보관(리전 로컬)`. 미래 트리거 "리전 간 토큰 검증"도 함께 다듬기 권장.
- **[전규현 · 게시완료]** 맞습니다. 같은 sweep에서 서명키 보관 위치를 '리전별·리전 로컬'로 고쳐 놓고 바로 아래 하위 항목의 '전역보관'을 놓쳤습니다. '리전별 보관(리전 로컬)'으로 정정했습니다. 함께 지적하신 미래 트리거의 '리전 간 토큰 검증'도 각 리전이 자기 토큰을 자체 검증하는 모델과 맞게 '리전 간 토큰 상호 검증이 필요해질 경우'로 다듬었습니다.
- 조치(예정): §7.1.1 하위 bullet 전역보관→리전별 보관 + 미래 트리거 문구 · 반영: push `34496d3` · 상태: **Resolved(fixed)**

## C-24 · docs/specs/SRS.md:1274 (§4.1.1) · [thread 81478] · 💡
- **[Nemesis · cid 1]**
  > §4.1.1 면 판별 bullet의 "apex = GW 고유 API"가 R2로 폐기된 전역 apex를 규범 절에 남김. §4.1.2 규칙1은 정정됐는데 이 bullet 누락. "GW 고유 API 호스트(gw.<region>.<도메인>)"로 정정 권장. OpenAPI 주석 7·61·admin tag 45의 "apex"도 동류.
- **[전규현 · 게시완료]** 맞습니다. §4.1.2 규칙 1은 'apex→GW 고유 API 호스트'로 고쳤는데 §4.1.1 면 판별 bullet의 'apex ='가 누락됐습니다. 'GW 고유 API 호스트(gw.<region>.<도메인>) = GW 고유 API'로 정정했습니다. 지적하신 OpenAPI 헤더 주석(범위·라우팅)과 admin 태그 설명의 'apex' 표기도 'GW 고유 API 호스트'로 정리했습니다(스키마 필드명 apex는 리전 API 호스트를 가리키는 정의 필드라 유지).
- 조치(예정): §4.1.1 apex= 정정 + OpenAPI 주석 4곳(7·19·45·61) · 반영: push `34496d3` · 상태: **Resolved(fixed)**

## C-25 · docs/specs/SRS.md:2049 (§7.6.3) · [thread 81479] · 💡
- **[Nemesis · cid 1]**
  > §7.6.3 메타 컬럼 목록이 삭제된 WebhookEvent.region을 아직 검색 컬럼으로 나열. 리전=배포 상수라 단일 리전 배포의 모든 행이 동일 리전이라 필터 무의미. region 제거 권장.
- **[전규현 · 게시완료]** 맞습니다. WebhookEvent.region 필드를 삭제했고 리전은 배포 상수라 단일 리전 배포의 모든 행이 같은 리전이라 region 필터가 무의미합니다. §7.6.3 메타 컬럼 목록에서 region을 제거했고, 같은 목록이 남아 있던 OpenAPI admin 설명(webhook 이벤트 메타)에서도 제거했습니다.
- 조치(예정): §7.6.3 + OpenAPI 1032 메타 컬럼 region 제거 · 반영: push `34496d3` · 상태: **Resolved(fixed)**

## C-26 · [thread 81480] · 요약(Update 5)
- **[Nemesis · cid 1]** (요약 — 직전 잔재 상당수 해소 확인. 신규=부분수정 누락 4건. 참고로 §4.1.2 규칙3·917·handoff §7.5.2 "여전히 열림"이라 하나 c6fe5f1 미반영 스냅샷 기준.)
- **[전규현 · 게시완료]** 리뷰 감사합니다. 직전 지적 해소 확인 감사드립니다. 신규 4건은 모두 반영했습니다 — TC-DATA-02/03(+04) 단일-DB·하드 FK로 재작성, §7.1.1 '전역보관'→'리전별 보관', §4.1.1과 OpenAPI 주석의 'apex' 표기 정리, §7.6.3 메타 컬럼의 region 제거. 참고로 남기신 §4.1.2 규칙 3·§2.3.6.2 다이어그램·handoff §7.5.2 앵커는 이 리뷰 직전 커밋에서 이미 정정·push했습니다(리뷰가 그 push 이전 스냅샷 기준).
- 조치(예정): 요약 응대(stale 안내 + 신규 반영) · 반영: push `34496d3` · 상태: **Resolved(fixed)**


---

## Round 6 — Jack(임건혁) 인프라 리뷰 (2026-07-29 18:07 수신 · 개별 초안 · 원문 전체)

> 작성자 = **임건혁(Jack)** 전건(Nemesis 아님·식별=thread id). 성격 = 실질 인프라 설계 반론·추가 요구. 빈 스레드 81490·81492 제외. **스펙 미수정·초안 미게시 — 사용자 검토 후 진행.** 유형: [결정] · [스펙추가] · [문구정정=즉시] · [③-I]. 각 코멘트 **원문 전체** 기록.

## C-29 · docs/specs/SRS.md §4.5.1 · [thread 81481 + 81463] · 임건혁(Jack) · [결정] 🔧 DNS zone 스킴
- **[임건혁(Jack) · thread 81481]** (원문 전체)
  > **[infra/DNS] §4.5.1 — 리전 호스트와 Region Directory의 부모 zone이 다릅니다. 지금 구조면 리전마다 위임을 새로 받아야 합니다.**
  >
  > §4.5.1 예시를 zone 트리로 펴보면 부모가 둘로 갈립니다.
  >
  > ```
  > 리전 호스트:        gw.apne2.vatech.com       -> 부모 zone = apne2.vatech.com
  > Region Directory:   regions.gw.vatech.com     -> 부모 zone = gw.vatech.com
  > ```
  >
  > 문제는 우리가 `vatech.com` 을 소유한 게 아니라 정보전략실에서 **위임**받는다는 점입니다. 지금 안대로면 리전을 열 때마다 `apne2.vatech.com`, `use1.vatech.com` … **회사 apex 바로 밑 라벨을 리전마다 새로 위임**받아야 합니다. 근거로 든 AWS 방식(`ec2.ap-northeast-2.amazonaws.com`)은 AWS가 `amazonaws.com` 을 통째로 소유하니 성립하는 것이고, 위임받는 쪽에는 그대로 적용되지 않습니다.
  >
  > **대안 — `gw.<도메인>` 한 zone만 위임받고 리전을 그 안의 라벨로 둡니다.**
  >
  > ```
  > api.apne2.gw.vatech.com            axs.apne2.gw.vatech.com
  > axs.webhook.apne2.gw.vatech.com    admin.apne2.gw.vatech.com
  > regions.gw.vatech.com              (동일 트리 안에 자연스럽게 위치)
  > dev:  api.apne2.gw.dev.ezcld.net
  > ```
  >
  > - 위임 1회로 끝, 리전 추가 = 레코드 추가(추가 위임 협의 없음)
  > - 리전별 와일드카드 `*.apne2.gw.…` 그대로 성립
  > - Directory가 같은 트리 안에 들어가 "부모 zone 두 개" 문제가 사라짐
  >
  > Appendix B #2 에 "zone 관리 토폴로지 = ③-I 결정" 이라고 적어두셨는데, **본문 예시가 이미 특정 트리를 못박고 있는 게** 실제 문제입니다. EzServer·AXS 콜백·ACM cert가 이 예시를 따라가면 되돌리는 비용이 큽니다. 예시를 위 형태로 바꾸거나, 최소한 "구체 트리는 ③-I 확정" 으로 중립화해 주세요.
  >
  > 참고로 cert 수량은 어느 안이든 **리전당 2장**(`*.<region>.gw.…` + `*.webhook.<region>.gw.…`, 와일드카드는 라벨 1개만 커버) + **us-east-1 1장**(아래 Region Directory 코멘트) 입니다.
- **[임건혁(Jack) · thread 81463 — dev-도메인 스레드 재응답]** (원문 전체)
  > [infra] 인프라 쪽에서도 같은 지점이 걸립니다. 지금 문서가 서로 안 맞습니다.
  >
  > - `docs/env-reference.md:100` — `GW_PUBLIC_APEX` 설명은 "**리전 라벨 포함**·전역 apex 아님" 인데 dev 값은 `gw.dev.ezcld.net` (라벨 없음)
  > - `docs/env-reference.md:34` — dev 공개 호스트 `gw.dev.ezcld.net`, 와일드카드 2개도 `*.gw.dev.ezcld.net` 기준
  > - §4.5.1 — dev 베이스 도메인이 `gw.dev.ezcld.net` 이라고 되어 있어, 규칙을 그대로 적용하면 `gw.apne2.gw.dev.ezcld.net` 이 됩니다
  >
  > "리전 1개라서" 로 넘기면 **dev와 prod의 호스트 형태가 달라집니다.** EzServer nginx의 `Vatech-Target` -> 서브도메인 변환 규칙, 토큰 iss/aud, 와일드카드 cert 범위가 전부 호스트 형태에 붙어 있어서, 환경마다 모양이 다르면 dev에서 검증한 게 prod를 안 덮습니다. §2.7.1의 "리전 라벨 없는 고정 host 금지" 와도 어긋나고요.
  >
  > dev cert·zone·토큰 iss/aud가 이미 현재 호스트 기준으로 잡혀 있어서, 형태가 바뀌면 재발급이 따라옵니다. 별도로 올린 zone 토폴로지 코멘트와 묶어서 **베이스 도메인 + 리전 라벨 규칙을 한 번에 확정**한 뒤 dev를 맞추는 쪽이 재작업이 적습니다. EzServer가 Region Directory URL을 코드에 굽기 전에 정해져야 합니다.
- **[전규현 · 게시완료]** 동의합니다. gw.<도메인>을 한 번 위임받고 리전을 그 안의 라벨로 두는 방식으로 가면 위임 1회로 끝나고 리전 추가가 레코드 추가로 끝나며 Region Directory도 같은 트리에 들어옵니다. 본문 §4.5.1 예시가 특정 트리를 못박은 것도 맞아, 호스트 스킴을 `<svc>.<region>.gw.<도메인>`으로 개정하겠습니다(API=`api.`·프록시=`{target}.`·webhook=`{target}.webhook.`·admin=`admin.`·Directory=`regions.gw.<도메인>`). 이 스킴에서는 dev도 리전 라벨을 포함하므로(예 `api.apne2.gw.dev.ezcld.net`) 앞서 논의한 dev/prod 형태 불일치가 해소됩니다 — dev-도메인 스레드의 "단일 리전이라 라벨 생략"은 이 스킴 채택으로 대체됩니다. 구체 base domain은 정보전략실 위임 확정 후 ③-I가 최종화합니다. cert는 리전당 2장(`*.<region>.gw.…`+`*.webhook.<region>.gw.…`) + Region Directory용 us-east-1 1장으로 카운트합니다.
- 조치: 호스트 스킴 <svc>.<region>.gw.<도메인> 전면 개정(§4.5.1·§2.7.1·OpenAPI·handoff·env·UnitTCL·DBML·README) + dev-도메인 답변(C-20) 대체 + GW_PUBLIC_APEX→HOST·apex필드→apiHost · 반영: push `ab5441a` · 게시·81481/81463 · 상태: **Resolved(fixed)**

## C-30 · docs/specs/SRS.md §7.3.6 · [thread 81482] · 임건혁(Jack) · [스펙추가] 💡
- **[임건혁(Jack) · thread 81482]** (원문 전체)
  > **[infra/Region Directory] §7.3.6 — 무결성 수단이 HTTPS뿐입니다. 발행 파이프라인·캐시·인증서도 정해야 합니다.**
  >
  > 이 JSON 하나가 **신규 enroll 전량의 목적지**를 정하고, EzServer에 굽히는 유일한 부트스트랩 앵커입니다. 문서에는 "무결성(HTTPS·버전)" 만 있어서 인프라가 받기에 부족합니다. 아래 4가지를 스펙/③-I 항목에 넣어주세요.
  >
  > 1. **파일 자체 서명** — HTTPS는 전송 구간만 보장합니다. 버킷 오배포·발행 실수·DNS 탈취 중 어느 하나라도 신규 device가 통째로 다른 곳에 enroll 됩니다. **detached JWS(검증키는 EzServer 내장)** 또는 최소한 EzServer 측 pinning을 요구합니다. 서명키 보관·회전은 ③-I가 가져갑니다.
  > 2. **발행 경로는 §7.7.5 compat matrix와 동일 패턴으로** — git → CI에서 JSON Schema 검증 → S3 put, **write IAM은 CI 발행 identity 전용(사람·앱 role deny)**. 콘솔/CLI 수기 업로드 경로는 두지 않겠습니다. §7.7.5에 이미 확립된 패턴이라 재사용이 제일 싸고, 리전 목록 변경이 리뷰 없이 나가는 걸 막습니다.
  > 3. **캐시 TTL** — `status: draining/planned` 전파 속도가 곧 CloudFront TTL입니다. 값(60s 제안)과 무효화 절차를 명시해 주세요. 지금은 "캐시 가능" 만 있습니다.
  > 4. **인증서** — CloudFront 앞단이면 `regions.gw.<도메인>` cert는 **us-east-1 ACM 필수**이고 리전 와일드카드로 덮이지 않습니다. 별도 프로비저닝 항목으로 카운트하겠습니다.
- **[전규현 · 게시완료]** 동의합니다. Region Directory가 신규 enroll 전량의 목적지·부트스트랩 앵커라 HTTPS(전송 구간)만으로는 부족합니다. §7.3.6에 네 가지를 명시하겠습니다 — 파일 detached JWS 서명(검증키 EzServer 내장·키 보관/회전 ③-I), 발행 파이프라인=§7.7.5 compat matrix 패턴(git→CI JSON Schema 검증→S3·write IAM=CI 발행 identity 전용·수기 업로드 금지), 캐시 TTL(60s)·무효화 절차, CloudFront 앞단이면 us-east-1 ACM cert. 발행 주체·키 관리는 ③-I 소관으로 남깁니다.
- 조치: §7.3.6 무결성 4항목(JWS 서명·§7.7.5 발행 패턴·TTL 60s·us-east-1 cert) 추가 · 반영: push `55d724b` · 상태: **Resolved(fixed)**

## C-31 · docs/specs/SRS.md §6.3.1·Appendix B #9 · [thread 81483] · 임건혁(Jack) · [스펙추가] 🔧
- **[임건혁(Jack) · thread 81483]** (원문 전체)
  > **[infra/DR] §6.3.1·Appendix B #9 — region silo에서는 리전 단위 DR이 존재하지 않습니다. 그 말이 문서에 없습니다.**
  >
  > 리전 간 복제 없음 + PHI 리전 밖 미이동(FR-RGN-03)을 같이 놓으면 **교차리전 스냅샷 복사도 금지**됩니다. 즉:
  >
  > - Multi-AZ = **AZ 장애만** 커버
  > - RDS 자동 백업·스냅샷 = 리전 로컬
  > - 리전 전체 소실 = **복구 수단 없음**
  >
  > 기존 Aurora Global 안에서는 최소한 non-PHI 클러스터에 대해 교차리전 이야기가 있었는데, 이번 변경으로 그것도 없어졌습니다. Aurora 폐기 자체는 동의하지만(복제가 사라졌으니 RDS가 맞습니다) **DR 공백은 별도로 문서화가 필요**합니다.
  >
  > 요청:
  > - §6.3.1에 **"리전 단위 재해는 가용성 목표 범위 밖(주권상 교차리전 백업 불가)"** 을 명시하거나,
  > - 예외를 둘 거면 그 조건(예: 동일 관할권 내 2nd 리전으로의 암호화 스냅샷 복사 — 이 경우 교차리전 KMS grant가 필요해 "리전 간 배선 없음" 과 충돌)을 스펙에 적어주세요.
  >
  > Appendix B #9(RTO/RPO)는 이 전제가 정해져야 답할 수 있습니다. 지금 상태로 넘어오면 인프라가 못 받는 요구가 됩니다.
- **[전규현 · 게시완료]** 동의합니다. 복제 없음 + PHI 리전 밖 금지(FR-RGN-03)를 함께 놓으면 교차리전 스냅샷 복사도 막혀 리전 단위 재해는 복구 수단이 없습니다. §6.3.1에 "리전 단위 재해는 가용성 목표 범위 밖(주권상 교차리전 백업 불가)"을 명시하고, 예외를 둘 경우(동일 관할권 2nd 리전 암호화 스냅샷)는 교차리전 KMS grant가 필요해 "리전 간 배선 없음"과 충돌한다는 점까지 적겠습니다. Appendix B #9(RTO/RPO)는 이 전제 확정 후 답하겠습니다.
- 조치: §6.3.1 DR 공백 명시(리전 재해=목표 밖·교차리전 백업 불가) + B#9 전제 · 반영: push `55d724b` · 상태: **Resolved(fixed)**

## C-32 · §2.7.1·handoff #6 · [thread 81484] · 임건혁(Jack) · [스펙추가] 🔧
- **[임건혁(Jack) · thread 81484]** (원문 전체)
  > **[infra/ECR] §2.7.1·handoff #6 — "리전 스택 통째" 목록에 ECR 교차리전 복제가 빠졌습니다.**
  >
  > 우리 런타임 base는 digest 고정입니다(리포 CLAUDE.md 규약):
  >
  > ```
  > 118688039229.dkr.ecr.ap-northeast-2.amazonaws.com/es-base/node24-slim@sha256:<digest>
  > ```
  >
  > ECR은 리전 서비스라 타 리전 EKS가 이 이미지를 당기면 **교차리전 pull** 이 됩니다.
  >
  > - pull 지연·리전 간 전송료
  > - **apne2 ECR 장애 시 타 리전에서 신규 pod 기동 불가** — "각 리전이 독립 스택" 이라는 전제가 이미지 레이어에서 깨집니다
  >
  > handoff `region-silo-infra.md` 항목 6(리전 스택 증분)에 **ECR cross-region replication rule(앱 이미지 + es-base 양쪽)** 을 추가해 주세요. base 이미지는 DevOps 소유라 replication 설정 주체도 같이 정리하겠습니다.
- **[전규현 · 미게시(무시·thread 삭제됨)]** 동의합니다. es-base가 digest 고정이라 타 리전 EKS가 apne2 ECR을 교차리전 pull하면 지연·전송료가 생기고, apne2 ECR 장애 시 타 리전 신규 pod 기동이 막혀 "각 리전 독립 스택" 전제가 이미지 레이어에서 깨집니다. handoff의 리전 스택 증분 항목에 ECR cross-region replication(앱 이미지 + es-base 양쪽)을 추가하겠습니다. es-base는 DevOps 소유라 replication 설정 주체도 함께 정리하는 데 동의합니다.
- 조치: **무시** — Jack이 원 코멘트(thread 81484)를 스스로 삭제(미처리 상태)해 스펙 미반영·답변 안 함 · 상태: **무시(withdrawn·미처리 삭제)**

## C-33 · §2.1.1·§7.5.3·handoff #4 · [thread 81485] · 임건혁(Jack) · [스펙추가] 💡
- **[임건혁(Jack) · thread 81485]** (원문 전체)
  > **[infra/egress] §2.1.1·§7.5.3·handoff #4 — EIP whitelist 대상이 AXS만 적혀 있습니다.**
  >
  > "AXS whitelist = 전 리전 EIP 합집합" 은 맞는데, 리전이 늘면 **AXS 말고도 union이 필요한 곳**이 같이 늘어납니다. 현재 문서·handoff에 누락된 것들:
  >
  > - **LMP** — enroll마다 라이선스·Clinic-ID 검증(§2.3.1), B안이면 JWKS fetch. 전 리전 GW → LMP 아웃바운드가 생깁니다. LMP 쪽 whitelist도 union 대상입니다.
  > - **CleverSpace(내부 B)** — 내부망 전제로 "egress 고정 IP 불필요" 라고 되어 있는데, 리전이 늘면 타 리전에서 오는 트래픽이 더는 내부망 전제로 안 묶입니다. 리전 간 연결 방식(전용 회선/피어링/공개 경로 중 무엇인지)이 정해져야 합니다.
  > - **Entra JWKS·중앙 관측 백엔드·CI→Parameter Store** — 리전마다 아웃바운드가 생깁니다.
  >
  > 프로비저닝 쪽에서는 **리전당 NAT 수를 고정(2AZ)** 하고 EIP를 미리 풀로 잡아두는 방식으로 가겠습니다. 그래야 union 크기가 예측 가능합니다. AXS 등록 IP 개수 상한 확인(④)은 이미 문서에 있는 대로 진행해 주세요.
- **[전규현 · 게시완료]** 동의합니다. AXS 외에도 리전이 늘면 union이 필요한 아웃바운드가 함께 늘어납니다 — LMP(enroll 검증·JWKS), Entra JWKS, 중앙 관측 백엔드, CI→Parameter Store. §2.1.1·§7.5.3·handoff의 union 대상을 AXS 단독이 아니라 이 목록으로 확장하겠습니다. CleverSpace 내부망 전제도 리전 증가 시 재검토가 필요하고 리전 간 연결 방식이 미정이라는 점을 명시하겠습니다. 리전당 NAT 2AZ 고정·EIP 풀 선확보는 ③-I 방식으로 존중합니다.
- 조치: §2.1.1·handoff#4 egress union 대상 확장(AXS 외 LMP·Entra·관측·CI) · 반영: push `55d724b` · 상태: **Resolved(fixed)**

## C-34 · docs/specs/SRS.md §2.1.1 · [thread 81486] · 임건혁(Jack) · [문구정정] 💡
- **[임건혁(Jack) · thread 81486]** (원문 전체)
  > **[infra] §2.1.1 — "전역인 것은 딱 하나 = Region Directory" 는 사실과 다릅니다.**
  >
  > 인프라 관점에서 실제로 리전 경계를 넘는 것들이 이미 있습니다:
  >
  > | 전역 의존 | 성격 |
  > |---|---|
  > | **ECR** | 이미지 pull, 다만 ECR 이미지에 PHI가 들어가진 않으니 무방할듯 합니다.|
  > | **LMP** | enroll 검증·JWKS — 전 리전에서 아웃바운드 |
  > | **Entra/MS365 JWKS** | 모든 리전 admin API가 같은 IdP 검증 |
  > | **CI → Parameter Store** | compat matrix를 CI가 전 리전에 발행(§7.7.5) |
  >
  >
  > 요청: §2.1.1에 **전역 의존 목록 + 각각 비-PHI 근거**를 표로 추가해 주세요. 문장을 "전역 데이터(클리닉·PHI)는 없다. 단 비-PHI 전역 의존은 아래와 같다" 로 바꾸는 정도면 충분합니다.
- **[전규현 · 게시완료]** 동의합니다. "전역인 것은 Region Directory 하나"는 부정확합니다 — ECR·LMP·Entra JWKS·CI→Parameter Store가 리전 경계를 넘습니다. §2.1.1을 "전역 데이터(클리닉·PHI)는 없다. 단 비-PHI 전역 의존은 아래"로 바꾸고 각 항목의 비-PHI 근거를 표로 추가하겠습니다.
- 조치: §2.1.1 전역 의존 표(ECR·LMP·Entra·CI) 추가 · 반영: push `ab5441a` · 상태: **Resolved(fixed)**

## C-35 · docs/specs/SRS.md §2.7.1 · [thread 81487] · 임건혁(Jack) · [결정·defer] 🔧 중국 파티션
- **[임건혁(Jack) · thread 81487]** (원문 전체)
  > **[infra] 중국 리전은 "독립 스택 하나 더" 가 아닙니다 — 별도 파티션입니다.**
  >
  > 배경에 중국이 동기로 적혀 있고 §2.7.1이 "리전 추가 = 독립 스택 통째로 얹기" 라고 정리했는데, AWS 中国는 인프라 관점에서 전혀 다른 물건입니다.
  >
  > - **별도 파티션** (`amazonaws.com.cn`) — 별도 계정·별도 IAM·별도 Terraform provider·글로벌 파티션과 IAM 신뢰관계 없음
  > - **글로벌 ECR 접근 불가** — es-base 포함 이미지 파이프라인을 따로 구축해야 함
  > - **Entra 연동·중앙 관측·CI 접근** 전부 경계 밖
  > - **ICP 备案** 필요 (도메인·호스팅)
  > - **CloudFront 전역 배포 불가** — 중국은 별도 CDN
  >
  > 마지막 항목 때문에 **"Region Directory를 리전 독립 URL 하나에 둔다"는 §7.3.6 전제가 중국에서 깨집니다.** 중국 EzServer가 읽을 Directory는 결국 별도 URL이 되고, 그러면 "유일한 부트스트랩 앵커" 도 하나가 아니게 됩니다.
  >
  > 중국이 범위 안이면 §2.7.1을 **같은 파티션 리전 증분 / 별도 파티션(랜딩존 신설)** 두 케이스로 나눠 써주세요. 비용·기간도 자릿수가 다릅니다.
- **[전규현 · 게시완료]** 지적 정확합니다. AWS 중국은 별도 파티션(amazonaws.com.cn)이라 §2.7.1의 "독립 스택 증분"과 성격이 다릅니다 — 별도 계정·IAM·Terraform provider, 글로벌 ECR 접근 불가(별도 이미지 파이프라인), Entra 연동 불가(별도 인증 방안 필요), 중앙 관측·CI 경계 밖, ICP 备案, CloudFront 불가로 Region Directory URL이 별도가 됩니다. 다만 v1.0·gw/1.2는 중국 진입 범위가 아니므로, 지금은 스펙에 이 사실만 명시하고(§2.7.1을 "동일 파티션 리전 증분"과 "별도 파티션 랜딩존 신설 — 범위 밖·추후"로 구분) 실제 지원이 필요해질 때 스펙/설계를 별도 업그레이드하는 것으로 남기겠습니다. 언급하신 ECR 별도 배치·Entra 대체 인증 등 파티션별 추가 지원 항목도 그 미래 작업 목록으로 함께 적어 두겠습니다.
- 조치: §2.7.1에 중국=별도 파티션 defer 명시(범위 밖·추후 업그레이드·파티션별 추가 지원 목록) · 반영: push `55d724b` · 상태: **Resolved(fixed)**

## C-36 · SRS 1146·1153·1157·2040·2171 + env-reference · [thread 81488] · 임건혁(Jack) · [문구정정] 🔧
- **[임건혁(Jack) · thread 81488]** (원문 전체)
  > **[infra/IAM] IRSA -> EKS Pod Identity 로 정정 필요합니다.**
  >
  > 우리 EKS는 **Pod Identity**(pod-identity-association) 를 씁니다. IRSA 아닙니다. ServiceAccount에 `eks.amazonaws.com/role-arn` 애노테이션이 없는 게 정상이고, 파드 권한은 pod-identity-association 으로 확인합니다.
  >
  > 문서에 IRSA로 적힌 곳:
  >
  > - `docs/specs/SRS.md:1146` — "pod→AWS 접근은 **IRSA**로 부여한다"  ← 이번 PR에서 손댄 문단
  > - `docs/specs/SRS.md:1153` — SQS "서버리스·**IRSA** 접근·DLQ 내장"
  > - `docs/specs/SRS.md:1157` — "Secrets Store CSI / External Secrets(**IRSA** 연계)"
  > - `docs/specs/SRS.md:2040` — §7.6.3 큐 "서버리스·**IRSA**·DLQ 내장"
  > - `docs/specs/SRS.md:2171` — §7.7.5 "read=ESO/**IRSA**"
  > - `docs/env-reference.md:27, 51, 52, 60`
- **[전규현 · 게시완료]** 정정하겠습니다. IRSA가 아니라 EKS Pod Identity(pod-identity-association)를 쓰는 게 맞습니다. 지적하신 SRS 1146·1153·1157·2040·2171과 env-reference 27·51·52·60의 IRSA 표기를 Pod Identity로 모두 바꾸겠습니다.
- 조치: SRS 5곳 + env-reference 4곳 IRSA→EKS Pod Identity · 반영: push `ab5441a` · 상태: **Resolved(fixed)**

## C-37 · docs/env-reference.md (GW_REGION·GW_PUBLIC_APEX) · [thread 81489] · 임건혁(Jack) · [스펙추가+문구정정] 🔧
- **[임건혁(Jack) · thread 81489]** (원문 전체)
  > **[infra/env] `GW_REGION` — Parameter Store 보관은 문제없습니다(앞선 차트 주입 요청 철회). 다만 4곳 복제와 `AWS_REGION` 정합이 비어 있습니다.**
  >
  > 먼저 정정합니다. 차트 주입을 요청드렸는데 **철회**합니다 — `.env` 를 쓰지 않고 **컨테이너 주입 env 로만 동작**하며 PS/Secrets 는 ESO/CSI 가 동기화하는 구조라, 앱이 부팅 중 PS 를 직접 조회하지 않습니다. PS 에 둬도 부팅 경로 의존이 늘지 않습니다. 게다가 경로 규약이 이미 "prod 은 멀티리전이라 **리전별 prod 계정에 각각 생성**" 이라, 리전 상수를 담기에 PS 가 오히려 자연스럽습니다. **`GW_REGION`·`AWS_REGION` 모두 PS 유지로 갑니다.**
  >
  > 대신 표를 보다 확인된 두 가지만 반영 부탁드립니다.
  >
  > **1. 경로 규약상 `GW_REGION` 이 4곳에 복제됩니다.**
  >
  > PS 경로가 `/{env}/{app}/{VAR}` 라 `core`·`admin`·`receiver`·`dispatcher` 각각에 같은 값을 넣어야 합니다. `docs/env-reference.md:48` 에도 "4개 서비스(core/admin/receiver/dispatcher) **동일 값**" 이라고 적혀 있는데, 이는 곧 **하나만 틀려도 그 앱만 다른 리전으로 동작**한다는 뜻입니다. region silo 에서 이 오설정은 토큰 iss/aud·`ClinicResolution` region echo·주권 판정·로그 라벨이 전부 어긋나는데도 **앱은 정상 기동**합니다(값이 있으니 fail-closed 에 안 걸림).
  >
  > → 공용 경로(`/{env}/common/GW_REGION`)를 두거나, IaC 에서 **단일 변수로 4곳 fan-out** 하도록 못박아 주세요. 사람이 4번 넣는 운영은 하지 않겠습니다.
  >
  > **2. `GW_REGION` ↔ `AWS_REGION` 정합을 강제하는 게 없습니다.**
  >
  > `apne2` 와 `ap-northeast-2` 는 값 공간이 달라 중복이 아니라 **매핑**입니다. 현재 표는 "보통 일치하나 별개 키" 라고만 되어 있어 매핑이 어긋나도 잡히지 않습니다.
  >
  > → 부팅 시 **매핑 assertion(불일치 시 fail-closed)** 을 앱 요구사항으로 넣거나, 매핑 표를 한 곳에 두고 파생시켜 주세요. `GW_REGION` 이 이미 "공통 4" 필수값이니 존재 검사에 정합 검사만 얹으면 됩니다.
  >
  > ---
  >
  > **별건 — `GW_PUBLIC_APEX` 네이밍**
  >
  > apex 개념을 폐기했는데 변수명은 남아 있고 설명은 "전역 apex 아님" 이라 서로 싸웁니다. `GW_PUBLIC_HOST` 나 `GW_REGION_HOST` 로 바꿔주세요. Region Directory 스키마의 `apex` 필드명도 동일합니다(`host`/`apiHost`).
- **[전규현 · 게시 후 삭제(Jack root 삭제·orphan 정리)]** 동의합니다. PS 경로가 /{env}/{app}/{VAR}라 GW_REGION이 core·admin·receiver·dispatcher 4곳에 복제되고, 하나만 틀려도 그 앱만 다른 리전으로 정상 기동하는 위험이 있어 공용 경로 또는 IaC 단일 변수→4곳 fan-out을 스펙에 못박겠습니다(사람이 4번 입력 금지). GW_REGION↔AWS_REGION은 값 공간이 다른 매핑이라 부팅 시 매핑 assertion(불일치 fail-closed)을 앱 요구로 넣겠습니다. 별건인 GW_PUBLIC_APEX와 Region Directory의 apex 필드명도 폐기어라 GW_PUBLIC_HOST/host류로 리네이밍하겠습니다(스키마 필드명은 계약 변경이라 함께 처리). 차트 주입 철회·PS 보관 확정 반영 감사합니다.
- 조치: **Jack이 원 코멘트(thread 81489)를 스스로 삭제(withdrawn)** — 이미 반영한 apex 리네이밍(push `ab5441a`)은 정합상 유지, GW_REGION fan-out·assertion은 요구 철회로 미반영. 스레드 Resolved · 상태: **Resolved(withdrawn·apex only)**

## C-38 · docs/specs/SRS.md §3.1.2 · [thread 81491] · 임건혁(Jack) · [스펙추가/③-I] 💡
- **[임건혁(Jack) · thread 81491]** (원문 전체)
  > **[infra/RDS] §3.1.2 — RDS 전환은 동의. 다만 프로비저닝 파라미터가 비어 있습니다.**
  >
  > Aurora Global 폐기 동의합니다. 교차리전 복제가 사라졌으니 Aurora를 미리 살 근거가 없어졌고 RDS for PostgreSQL Multi-AZ가 맞습니다. Aurora가 자동으로 주던 것들이 이제 **명시 설정 항목**이 되므로 아래를 스펙 또는 ③-I 항목으로 확정해 주세요.
  >
  > 1. **Multi-AZ 형태** — `Multi-AZ instance`(스탠바이 1) vs `Multi-AZ DB cluster`(3-instance) 중 어느 쪽인지. 전자는 failover 60~120초 + 마이너 패치 시 다운, 후자는 훨씬 빠르지만 비쌉니다. 99.9%(월 43분) 목표면 instance로 충분하다고 보되, **유지보수 창(§2.6·B#9)** 과 **blue/green 업그레이드 사용**을 전제로 깔아야 합니다.
  > 2. **스토리지 오토스케일링** — Aurora는 자동 확장이었습니다. RDS는 `max_allocated_storage` 를 명시하지 않으면 안 늘어납니다. 상한값 필요.
  > 3. **스토리지 클래스·IOPS** — gp3 기준 baseline IOPS/throughput. `webhook_event.payload_encrypted` 가 같은 인스턴스에 들어오면서 쓰기 프로파일이 바뀌었으니 사이징 입력이 필요합니다(Appendix B #15·#36).
  > 4. **PostgreSQL 17.x extension 호환 검토** — Appendix B #18에 제 몫으로 잡혀 있는 항목, RDS 기준으로 다시 보겠습니다.
- **[전규현 · 게시완료]** 동의합니다. Aurora가 자동으로 주던 것들이 RDS에선 명시 항목이 됩니다 — Multi-AZ 형태(instance vs cluster), 스토리지 오토스케일 상한(max_allocated_storage), gp3 IOPS/throughput(payload_encrypted 동거로 쓰기 프로파일 변화·Appendix B #15·#36), PG17 extension 호환(B#18)을 §3.1.2 또는 ③-I 항목으로 확정하겠습니다. 99.9% 목표면 instance + blue/green·유지보수 창 전제라는 판단도 함께 반영하겠습니다.
- 조치: §3.1.2 RDS 프로비저닝 파라미터 항목화(Multi-AZ 형태·오토스케일·IOPS·PG17 ext·③-I) · 반영: push `55d724b` · 상태: **Resolved(fixed)**

## C-39 · docs/specs/SRS.md §2.3.9 · [thread 81493] · 임건혁(Jack) · [스펙추가] 🔧
- **[임건혁(Jack) · thread 81493]** (원문 전체)
  > **[infra/KMS] §2.3.9 — 마이그레이션 시 교차리전 재암호화가 필요합니다. "리전 간 배선 없음" 과 충돌합니다.**
  >
  > §2.3.9 공통 이동 대상에 `webhook_event(payload·KMS)` 가 들어 있는데, payload는 **구 리전 CMK로 envelope 암호화**되어 있습니다. 이관하려면:
  >
  > 1. 구 리전 CMK로 복호화
  > 2. 신 리전 CMK로 재암호화
  >
  > 이 순간만큼은 **한쪽이 상대 리전 CMK에 대한 grant를 갖거나, 평문이 리전 경계를 넘거나** 둘 중 하나가 됩니다. §2.1.1의 "리전 간 배선 없음" 과 정면으로 충돌하고, 주권 관점에서도 그냥 넘길 수 없는 구간입니다.
  >
  > §2.3.9에 이 단계를 **명시적 예외**로 적어주세요 — 어느 쪽에서 복호화하는지, grant를 어느 방향으로 임시 부여하는지, 커트오버 후 회수 절차까지. handoff `region-silo-infra.md` 항목 5(KMS 리전 키)에도 "마이그레이션 시 교차리전 grant 절차" 를 붙이겠습니다.
  >
  > gw/1.2 이후 항목이라 지금 설계까지는 아니어도, **"이건 공짜가 아니다" 는 표시**는 지금 남겨두는 게 맞습니다.
- **[전규현 · 게시완료]** 동의합니다. §2.3.9 이동 대상의 webhook_event payload는 구 리전 CMK로 암호화돼 있어 이관 시 복호화→재암호화 구간에서 교차리전 grant 또는 평문의 리전 경계 이동이 불가피해 "리전 간 배선 없음"과 충돌합니다. §2.3.9에 이 단계를 명시적 예외로 적겠습니다 — 복호화 위치·grant 방향·커트오버 후 회수 절차. handoff KMS 항목에도 "마이그레이션 시 교차리전 grant 절차"를 붙이겠습니다. gw/1.2 이후라 상세 설계는 그때지만 "공짜가 아님" 표시는 지금 남기겠습니다.
- 조치: §2.3.9·handoff#5 KMS 마이그레이션 교차리전 재암호화 예외 명시 · 반영: push `55d724b` · 상태: **Resolved(fixed)**

## C-40 · §4.5.1(1410·1422·1426)·§6.6.2(1694)·§7.9(2289) · [thread 81494] · 임건혁(Jack) · [문구정정] 💡
- **[임건혁(Jack) · thread 81494]** (원문 전체)
  > **[infra/DNS] §4.5.1 — admin "내부 전용" 서술이 실제 구성과 다릅니다. 문구 정정 요청 (접근통제는 mesh로 처리)**
  >
  > 먼저 접근통제 자체는 이미 성립합니다. admin은 4-way의 **별도 Deployment**라 공개 ingress의 VirtualService에 **admin Service로 가는 route가 없습니다** — "닿는데 막힌다"가 아니라 upstream이 없는 상태입니다. 여기에 **Istio DENY AuthorizationPolicy**를 얹어 route 설정 실수까지 커버하겠습니다(Istio는 DENY를 ALLOW보다 먼저 평가하므로 VirtualService 변경에 영향받지 않습니다).
  >
  > **사설 hosted zone·전용 내부 ALB 신설은 하지 않습니다.** 리전마다 곱해지는 비용 대비 얻는 게 이름 enumeration 방지 수준이라, 공개 와일드카드에 `admin.` 이 매칭되어 TLS 핸드셰이크 후 거부 응답이 나가는 것은 수용합니다.
  >
  > 그래서 요청은 **문구 정정**입니다. 지금 스펙이 우리가 만들지 않을 구성을 약속하고 있습니다.
  >
  > | 위치 | 현재 | 정정 |
  > |---|---|---|
  > | §4.5.1 표 (`SRS.md:1410`) | "전용 ingress+**NetworkPolicy**·**사설 zone/내부 ALB**" · "GW core와 **물리 분리**" | "별도 Deployment + 공개 ingress에 **mesh DENY AuthorizationPolicy**(route 미등록)" · "**논리 격리**" |
  > | §4.5.1 4-way 표 (`:1422`) | "전용 ingress+**NetworkPolicy**" | 〃 |
  > | §4.5.1 (`:1426`) | "인증서·**사설 zone** 실제 구성=③-I" | "인증서·ingress 정책 실제 구성=③-I" |
  > | §6.6.2 (`:1694`) | "전용 ingress·**NetworkPolicy**" | 〃 |
  > | §7.9 (`:2289`) | "전용 ingress·**NetworkPolicy**" | 〃 |
  >
  > 집행 수단은 **NetworkPolicy가 아니라 Istio AuthorizationPolicy** 입니다. 스펙에 NetworkPolicy로 박혀 있으면 ③-I가 쓰지 않는 수단으로 대조당합니다. "물리 분리"도 마찬가지로, 실제로는 별도 Deployment + mesh 정책에 의한 **논리 격리**입니다.
  >
  > ---
  >
  > **참고 — 리전당 실제 LB 구성** (스펙의 "내부 ALB" 표현이 현실과 다릅니다)
  >
  > | 용도 | 구성 |
  > |---|---|
  > | 프론트엔드 | CloudFront (**VPC origin**) → **internal NLB** |
  > | 백엔드 | **ALB** (공개) |
  > | 모니터링 | **internal ALB** |
  >
  > 즉 `console.`(③-C UI)은 애초에 공개 백엔드 ALB에 붙지 않고 CloudFront + internal NLB 경로입니다 — DENY 대상도 아니고 "공개 와일드카드 밑" 문제도 해당되지 않습니다. **정리 대상은 `admin.` 하나입니다.**
  >
  > (별건: 프론트엔드가 CloudFront면 그 배포용 인증서는 **us-east-1 ACM** 이라, 리전 내 ALB용 와일드카드 cert와 별개로 카운트됩니다. Region Directory 코멘트의 cert 항목과 같은 맥락입니다.)
  >
  > **구현 시 주의** — DENY에 사내 CIDR 조건(`remoteIpBlocks`)을 같이 걸 거면 ALB 뒤라서 XFF 처리가 전제입니다. `numTrustedProxies`(gatewayTopology)를 안 잡으면 소스가 ALB 사설 IP로 잡혀 정책이 무의미해지거나 전량 차단됩니다. `ipBlocks`(직접 소스)와 `remoteIpBlocks`(XFF 유래)는 다른 필드입니다.
- **[전규현 · 게시 후 삭제(Jack root 삭제·orphan 정리)]** 동의합니다. admin 접근통제가 사설 zone/내부 ALB/NetworkPolicy가 아니라 별도 Deployment + 공개 ingress route 미등록 + Istio DENY AuthorizationPolicy(논리 격리)로 성립한다는 실제 구성에 맞게 문구를 정정하겠습니다 — §4.5.1 표(1410)·4-way 표(1422)·1426, §6.6.2(1694), §7.9(2289)의 "NetworkPolicy·사설 zone·물리 분리"를 "mesh DENY AuthorizationPolicy·route 미등록·논리 격리"로. console.은 CloudFront+internal NLB라 대상이 아니고 정리 대상은 admin. 하나라는 점, XFF/numTrustedProxies 주의도 반영하겠습니다.
- 조치: admin 5곳 문구 정정(NetworkPolicy·사설 zone·물리 분리 → mesh DENY AuthorizationPolicy·route 미등록·논리 격리) · 반영: push `ab5441a` · 상태: **Resolved(fixed)**

> 빈 스레드: 81490·81492(Jack 게시 내용 없음 — placeholder/삭제 추정, 대응 불요).

---
## Round 7 — Nemesis Update 6 (2026-07-30 07:4x)

> 신규 2건(둘 다 💡). **§4.1.2 규칙3·§2.3.6.2 917 해소 확인**(c6fe5f1). 요약이 "미해소"로 재기재한 TC-DATA-02/03·§7.1.1 전역보관·§4.1.1 apex·§7.6.3 region은 **34496d3에 이미 반영**(Update 6가 34496d3 직전 스냅샷)—stale. 신규 2건 전건 정정·push(`82a4442`)·답변 게시(전규현)·Resolved(fixed).

## C-27 · docs/specs/SRS.md:1270 (§4.1.1 A행) · [thread 81496] · 💡
- **[Nemesis · cid 1]**
  > §4.1.1 "두 면" 표 A행이 host는 리전화했으나 API surface 나열의 `region resolve`가 잔존. §7.3.1·§2.3.3·§2.2 노드는 모두 "클리닉 자기뷰"로 치환됨. `region resolve`→`클리닉 자기뷰(GET /v1/clinics/me·리전 echo)` 권장. 동류: §2.2 주석 라인 401 "region 참조".
- **[전규현 · 게시완료]** 맞습니다. §7.3.1·§2.3.3·§2.2 노드는 모두 '클리닉 자기뷰'로 바뀌었는데 §4.1.1 A행 API surface 나열에 'region resolve'가 남았습니다. '클리닉 자기뷰(리전 echo)'로 정정했습니다. 지적하신 §2.2 다이어그램 주석의 'region 참조'도 같은 다이어그램 엣지 라벨(클리닉 자기뷰·리전=상수)과 맞게 정리했습니다.
- 조치: §4.1.1 A행 region resolve + §2.2 주석 401 정정 · 반영: push `82a4442` · 상태: **Resolved(fixed)**

## C-28 · [thread 81497] · 요약(Update 6) + §2.3.6.2 participant(910)
- **[Nemesis · cid 1]**
  > (요약) §4.1.2 규칙3·§2.3.6.2 917 해소 확인. 신규 recommendation 2건: §4.1.1 A행 region resolve(위) + §2.3.6.2 participant 라인 910 "수신 리전 X·최근접"이 X를 "대표 수신점(GeoDNS 최근접 아님)"으로 재정의한 §2.3.6.2·§7.3.5(GeoDNS 폐기)와 상충. "·최근접"→"대표 수신점" 권장. 미해소 재기재(TC-DATA·전역보관·apex·§7.6.3 region)는 34496d3 미반영 스냅샷 기준.
- **[전규현 · 게시완료]** 리뷰와 §4.1.2 규칙 3·§2.3.6.2 다이어그램 해소 확인 감사합니다. 신규 2건 모두 반영했습니다 — §4.1.1 A행(및 §2.2 주석)의 'region resolve/참조'를 '클리닉 자기뷰'로, §2.3.6.2 participant 라벨의 '수신 리전 X·최근접'을 '대표 수신점'으로 정정했습니다(GeoDNS 최근접 폐기와 정합). 참고로 남기신 미해소 4건(TC-DATA-02/03·§7.1.1 전역보관·§4.1.1 apex·§7.6.3 region)은 이 리뷰 직전 커밋에서 이미 정정·push했습니다(리뷰가 그 push 이전 스냅샷 기준).
- 조치: §2.3.6.2 participant 910 "·최근접"→"대표 수신점" + 요약 응대 · 반영: push `82a4442` · 상태: **Resolved(fixed)**
