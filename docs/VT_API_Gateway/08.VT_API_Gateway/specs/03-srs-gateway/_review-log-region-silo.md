# ③ GW SRS — 리뷰 코멘트 추적 (region-silo · PR #12207)

> **작업용 문서**. 각 스레드=시간순 대화(cid·↳parent). `다음 답변(초안)`=미게시 답변(사용자 확인 후 게시). 반영=vt-api-gateway `docs/srs-region-silo` 브랜치.

- **PR**: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/12207
- **주제**: GW 저장소 리전 완전 분리(region silo) — R2 결정 반영 (SRS·DBML·OpenAPI·env-reference)
- **리뷰어**: Jack·Scott·Teddy(필수) · Thomas(옵션) · 우리=전규현
- **커밋**: `d848472`·`da8451a`·`0a5c9fa`(handoff)·`ec4a476`(handoff 정정) + 리뷰 반영분(아래·미커밋)
- **최종 fetch**: 2026-07-29T07:50 · **20 thread** (R1 6 + R2 5 + R3 5 + R4 4 · Nemesis v0.5.0)
- **상태**: R1~R7(Nemesis) 전건 게시·Resolved(push …·`34496d3`·`82a4442`) · **Jack 인프라 13건 = 초안 작성·검토 대기**

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

## Round 6 — Jack(임건혁) 인프라 리뷰 (2026-07-29 18:07 · 자동 모니터링 마감 시점 수신)

> **성격이 다름**: Nemesis 잔재 지적과 달리 실질 인프라 설계 반론·추가 요구. 상당수가 결정/논의 필요라 **초안 미작성 — 접수·분류만**(사용자 트리아지 후 진행). 빈 스레드 81490·81492 제외. dev-도메인(81463)은 Jack이 재응답(현재 fixed 표시지만 논의 재개).

### A. 즉시 반영 가능(Jack이 정정안·범위까지 제공)
- **81488 [IAM] IRSA→EKS Pod Identity 정정** — SRS 1146·1153·1157·2040·2171 + env-reference 27·51·52·60. 단순 치환.
- **81494 [DNS] admin "내부 전용/물리분리/NetworkPolicy" 문구가 실제(mesh DENY AuthorizationPolicy·논리격리)와 불일치** — Jack이 정정표 제공(§4.5.1 1410·1422·1426·§6.6.2 1694·§7.9 2289). console.은 대상 아님(CloudFront+internal NLB), 정리 대상은 admin. 하나. NetworkPolicy→Istio AuthorizationPolicy.
- **81486 [전역 의존] "전역=Region Directory 하나"는 부정확** — §2.1.1에 비-PHI 전역 의존 표(ECR·LMP·Entra JWKS·CI→Parameter Store) 추가. "전역 데이터(클리닉·PHI) 없음. 단 비-PHI 전역 의존은 아래" 로.
- **81489 별건 [env] GW_PUBLIC_APEX 리네이밍** — apex 폐기했는데 변수명·설명 잔존 → GW_PUBLIC_HOST/GW_REGION_HOST. Region Directory 스키마 apex 필드도 host/apiHost로.

### B. 스펙 추가 필요(내용은 명확·문안 작성 필요)
- **81482 [Region Directory] §7.3.6 무결성이 HTTPS뿐** — ① 파일 detached JWS 서명(검증키 EzServer 내장) ② 발행 파이프라인=§7.7.5 compat matrix 패턴(git→CI JSON Schema 검증→S3, write IAM=CI 전용) ③ 캐시 TTL(60s 제안)+무효화 ④ us-east-1 ACM cert.
- **81483 [DR] §6.3.1·B#9 리전 단위 DR 부재 명시** — 복제 없음+PHI 리전밖 금지=교차리전 스냅샷도 금지 → 리전 전체 소실 시 복구수단 없음. "리전 재해=가용성 목표 밖" 명시 or 예외조건(동일 관할권 2nd 리전 암호화 스냅샷=교차리전 KMS grant 필요·"배선 없음"과 충돌).
- **81484 [ECR] §2.7.1·handoff#6 교차리전 복제 누락** — es-base digest 고정→타 리전 EKS가 교차리전 pull·apne2 ECR 장애 시 타 리전 pod 기동 불가. handoff #6에 ECR cross-region replication(앱+es-base) 추가.
- **81485 [egress] union이 AXS만** — LMP(enroll 검증·JWKS)·CleverSpace(리전 늘면 내부망 전제 깨짐)·Entra JWKS·중앙 관측·CI→PS도 리전마다 아웃바운드. §2.1.1·§7.5.3·handoff#4.
- **81491 [RDS] §3.1.2 프로비저닝 파라미터 공백** — Aurora가 자동 주던 게 명시 항목화: Multi-AZ 형태(instance vs cluster)·스토리지 오토스케일 상한·gp3 IOPS/throughput·PG17 extension 호환(B#18). 대체로 ③-I.
- **81493 [KMS] §2.3.9 마이그레이션 교차리전 재암호화가 "배선 없음"과 충돌** — 구 CMK 복호화→신 CMK 재암호화 구간은 교차리전 grant or 평문 리전 경계 이동 불가피. §2.3.9에 명시적 예외(복호화 위치·grant 방향·회수 절차). handoff#5에도. gw/1.2라 "공짜 아님" 표시만 지금.

### C. 결정 필요(호스트 스킴·범위 — 사용자/Jack/Scott)
- **81481 + 81463 [DNS zone] 호스트 스킴 재검토** — Jack: vatech.com은 위임받는 것이라 gw.<region>.<도메인> 예시대로면 리전마다 회사 apex 밑 라벨 새 위임 필요(AWS amazonaws.com 소유 논리 미적용). 대안=gw.<도메인> 한 zone만 위임+리전을 내부 라벨(`api.apne2.gw.vatech.com`·dev=`api.apne2.gw.dev.ezcld.net`). 이러면 dev도 리전 라벨 포함돼 dev/prod 형태 일치(81463 Jack 재응답과 연결). **호스트 스킴 전면 영향(§4.5.1·OpenAPI servers·handoff·env-reference)** — 내가 앞서 한 "dev 라벨 생략"(C-20/c6fe5f1)과 방향이 갈림. cert=리전당 2장+us-east-1 1장.
- **81487 [중국] 별도 파티션(amazonaws.com.cn)** — 독립 스택 아님(별도 계정·IAM·provider·ECR 불가·Entra/관측/CI 경계밖·ICP 备案·CloudFront 불가→Region Directory URL 단일 전제 깨짐). §2.7.1을 동일 파티션/별도 파티션 2케이스로. 중국 범위 여부 결정 필요.
- **81489-1/2 [env] GW_REGION 4곳 복제·AWS_REGION 매핑** — PS 경로 /{env}/{app}/{VAR}라 core·admin·receiver·dispatcher 4곳 동일값(하나만 틀려도 그 앱만 다른 리전·fail-closed 미포착). 공용경로 or IaC 단일→4 fan-out. + GW_REGION↔AWS_REGION 매핑 assertion(부팅 fail-closed) 앱 요구. (PS 보관·차트 주입 철회는 Jack 확정.)

> 주의: 81463은 내가 이미 Resolved(fixed)로 닫았으나 Jack 재응답으로 논의 재개 상태. 81481 zone 결정과 함께 봐야 함.


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
