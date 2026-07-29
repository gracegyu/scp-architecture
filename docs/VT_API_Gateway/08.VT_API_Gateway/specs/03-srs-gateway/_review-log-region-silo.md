# ③ GW SRS — 리뷰 코멘트 추적 (region-silo · PR #12207)

> **작업용 문서**. 각 스레드=시간순 대화(cid·↳parent). `다음 답변(초안)`=미게시 답변(사용자 확인 후 게시). 반영=vt-api-gateway `docs/srs-region-silo` 브랜치.

- **PR**: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/12207
- **주제**: GW 저장소 리전 완전 분리(region silo) — R2 결정 반영 (SRS·DBML·OpenAPI·env-reference)
- **리뷰어**: Jack·Scott·Teddy(필수) · Thomas(옵션) · 우리=전규현
- **커밋**: `d848472`·`da8451a`·`0a5c9fa`(handoff)·`ec4a476`(handoff 정정) + 리뷰 반영분(아래·미커밋)
- **최종 fetch**: 2026-07-29T07:50 · **20 thread** (R1 6 + R2 5 + R3 5 + R4 4 · Nemesis v0.5.0)
- **상태**: R1·R2·R3·R4 전건 게시·Resolved(push `c102870`·`3b15792`·`eab47a3`·`c6fe5f1`) · **20 thread 전부 Resolved(fixed)**

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
