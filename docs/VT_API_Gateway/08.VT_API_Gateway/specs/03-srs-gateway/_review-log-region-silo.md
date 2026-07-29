# ③ GW SRS — 리뷰 코멘트 추적 (region-silo · PR #12207)

> **작업용 문서**. 각 스레드=시간순 대화(cid·↳parent). `다음 답변(초안)`=미게시 답변(사용자 확인 후 게시). 반영=vt-api-gateway `docs/srs-region-silo` 브랜치.

- **PR**: https://dev.azure.com/ewoosoft/es-platforms/_git/vt-api-gateway/pullrequest/12207
- **주제**: GW 저장소 리전 완전 분리(region silo) — R2 결정 반영 (SRS·DBML·OpenAPI·env-reference)
- **리뷰어**: Jack·Scott·Teddy(필수) · Thomas(옵션) · 우리=전규현
- **커밋**: `d848472`(region-silo 전면) · `da8451a`(§7.6.3 PHI 삭제 규정)
- **최종 fetch**: (없음 — 리뷰 대기)
- **상태**: 리뷰 대기

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

(리뷰 대기 — fetch 시 여기에 `## C-01 …` 로 추가)
